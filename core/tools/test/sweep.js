// usage: node sweep.js [--acft NAME] [--seat N] [--size WxH]     (the test bridge must be running: python3 bridge.py)
// Sweep of the pages of one aircraft in headless Chromium at 1180x820 and 1024x768, in every seat. NAME is the _ACFT_NAME to send
// (default AH-64D_BLK_II, e.g. A-10C_2); the seats, tabs, pages and sides come from /layout of the bridge.
// Per seat the DCS-BIOS data is made fresh with sim.py (--reset, aircraft, seat, sample texts) and re-sent every second.
// Per size and seat it opens every tab (with the sides of its display switch), every panel page through its map box and through the
// long-hold page list, the settings page, and in an aircraft with two seats the debug seat (long hold on the badge), measures every
// visible touch target (elements with a click / pointer listener; the hit area is the ::before of the key classes when the page
// grows it, else the box) and reports
//   - targets smaller than 56 x 56 px, and pairs whose hit areas overlap by 6 px or more in both directions
//   - things cut off at the window edge or by an overflow:hidden parent, text wider than its box, a page wider than the window
//   - page and console errors (the favicon 404 is ignored)
// Chooser options (one selector per view) and the knob bar (one knob per view) are measured with the pop-up open.
// Screenshots: logs/test/shots/<aircraft>/s<seat>_<W>x<H>_<view>.png. Results: logs/test/sweep_<aircraft>_results.json and
// logs/test/sweep_<aircraft>_table.txt. Environment: DASHBOARD_URL (default http://127.0.0.1:8080), CHROMIUM_PATH (a Chromium binary;
// default: the browser of the playwright package). Exit code 1 if a check fails; the findings are listed, not checked.
const fs = require('fs');
const path = require('path');
const { execFile, execFileSync } = require('child_process');
const { chromium } = require('playwright');

const HERE = __dirname;
const REPO = path.join(HERE, '..', '..', '..');
const OUT = path.join(REPO, 'logs', 'test');
const SIM = path.join(HERE, 'sim.py');
const PYTHON = process.platform === 'win32' ? 'python' : 'python3';
const BROWSER = process.env.CHROMIUM_PATH || undefined;
const BASE = process.env.DASHBOARD_URL || 'http://127.0.0.1:8080';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const slug = (s) => s.replace(/[^A-Za-z0-9]+/g, '_').replace(/^_|_$/g, '').toLowerCase();

const args = process.argv.slice(2);
let ACFT = 'AH-64D_BLK_II';
let seatArg = null;
let sizes = [[1180, 820], [1024, 768]];
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--acft') ACFT = args[++i];
  else if (args[i] === '--seat') seatArg = parseInt(args[++i], 10);
  else if (args[i] === '--size') sizes = [args[++i].split('x').map(Number)];
}

let layout = null;
let LABELS = [];
let HOME = '';
let SHOTS = '';
const state = { args: [] };
const findings = [];
const checks = [];
const stats = [];
let ctx = null;
const add = (kind, element, detail, extra = {}) => findings.push({ size: ctx.size, seat: ctx.seat, view: ctx.view, kind, element, detail, ...extra });
const check = (name, ok, info) => {
  checks.push({ size: ctx.size, seat: ctx.seat, name, ok, info: ok ? '' : info });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${ctx.size} seat ${ctx.seat}  ${name}${ok || info === undefined ? '' : '  ' + JSON.stringify(info)}`);
  if (!ok) add('FAIL', name, JSON.stringify(info));
};

// ---- page side ----------------------------------------------------------------------------------------------------
const MEASURE = ({ scope, minSize, overlap }) => {
  const TOL = 0.5;
  const KEYS = '.mkey,.mknob,.ckey,.rhalf,.kkey,.pbtn,.ppos,.pstap,.pcap,.pmark,.pchipb,.pslot';
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  const round = (v) => Math.round(v * 10) / 10;
  const cls = (el) => (el.getAttribute('class') || el.tagName.toLowerCase()).split(/\s+/)[0];
  const text = (el) => (el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 18);
  const owner = (el) => (typeof controls !== 'undefined' ? controls.find((c) => c.el === el || c.el.contains(el)) : null);
  const name = (el) => {
    const c = owner(el);
    return cls(el) + (text(el) ? ' "' + text(el) + '"' : '') + (c && c.def ? ' <' + String(c.def.id).replace('{seat}_', '') + '>' : '');
  };
  const inScope = (el) => !!el.closest(scope);
  const targets = [];
  (window.__sw || []).forEach((el) => {
    if (!el.isConnected || !inScope(el)) return;
    if (el.id === 'kscrim' || el.id === 'pages' || el.id === 'settings' || el.id === 'chooser' || el.id === 'kbar') return;
    const cs = getComputedStyle(el);
    if (cs.pointerEvents === 'none' || cs.visibility === 'hidden') return;
    const r = el.getBoundingClientRect();
    if (!(r.width > 0 && r.height > 0)) return;
    let w = r.width;
    let h = r.height;
    if (el.matches(KEYS)) {
      const pb = getComputedStyle(el, '::before');
      const pw = parseFloat(pb.width);
      const ph = parseFloat(pb.height);
      if (pb.content !== 'none' && pb.position === 'absolute' && pw > 0 && ph > 0) { w = pw; h = ph; }
    }
    const cx = r.x + r.width / 2;
    const cy = r.y + r.height / 2;
    targets.push({ el, name: name(el), cls: cls(el), vis: [r.width, r.height], w, h, x0: cx - w / 2, x1: cx + w / 2, y0: cy - h / 2, y1: cy + h / 2, cx, cy, cover: /gcover|pcover/.test(el.className.toString()), chip: el.classList.contains('pchipb') });
  });
  const out = { n: targets.length, small: [], overlaps: [], cut: [], covered: [], scroll: 0, doc: null };
  targets.forEach((t) => {
    if (!t.chip && (t.w < minSize - TOL || t.h < minSize - TOL)) out.small.push({ name: t.name, cls: t.cls, w: round(t.w), h: round(t.h), vw: round(t.vis[0]), vh: round(t.vis[1]) });
  });
  if (overlap) {
    targets.forEach((a, i) => targets.slice(i + 1).forEach((b) => {
      if (a.cover || b.cover || a.el.contains(b.el) || b.el.contains(a.el)) return;
      const ow = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0);
      const oh = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0);
      if (ow >= 6 && oh >= 6) out.overlaps.push({ a: a.name, b: b.name, ca: a.cls, cb: b.cls, ow: round(ow), oh: round(oh) });
    }));
  }
  targets.forEach((t) => {
    if (t.cx < 0 || t.cx > vw || t.cy < 0 || t.cy > vh || t.cover) return;
    const top = document.elementFromPoint(t.cx, t.cy);
    if (top && top !== t.el && !t.el.contains(top) && !top.contains(t.el) && !/gcover|pcover/.test(top.className.toString())) out.covered.push({ name: t.name, by: name(top) });
  });

  // cut off: window edge, overflow:hidden ancestors, text wider than its box
  const isHidden = (v) => v === 'hidden' || v === 'clip';
  const isScroll = (v) => v === 'auto' || v === 'scroll';
  const probe = (el, r, label, kind) => {
    let scrolled = false;
    const clips = [];
    for (let cur = el.parentElement; cur && cur !== document.documentElement; cur = cur.parentElement) {
      const s = getComputedStyle(cur);
      const ar = cur.getBoundingClientRect();
      if (isScroll(s.overflowX) || isScroll(s.overflowY)) {
        if (cur.scrollHeight > cur.clientHeight + 1 || cur.scrollWidth > cur.clientWidth + 1) scrolled = true;
        clips.push({ cur, l: ar.left + cur.clientLeft, t: ar.top + cur.clientTop, r: ar.left + cur.clientLeft + cur.clientWidth, b: ar.top + cur.clientTop + cur.clientHeight, soft: true });
      } else if (isHidden(s.overflowX) || isHidden(s.overflowY)) {
        const svg = cur instanceof SVGElement;
        clips.push({ cur, l: svg ? ar.left : ar.left + cur.clientLeft, t: svg ? ar.top : ar.top + cur.clientTop, r: svg ? ar.right : ar.left + cur.clientLeft + cur.clientWidth, b: svg ? ar.bottom : ar.top + cur.clientTop + cur.clientHeight });
      }
    }
    if (scrolled) { out.scroll++; return; }
    const tol = kind === 'text' ? 3 : 1;
    const d = { l: -r.left, t: -r.top, r: r.right - vw, b: r.bottom - vh };
    if (Math.max(d.l, d.t, d.r, d.b) > tol) out.cut.push({ kind: 'window', name: label, by: round(Math.max(d.l, d.t, d.r, d.b)), rect: [r.left, r.top, r.right, r.bottom].map(round) });
    clips.filter((c) => !c.soft).forEach((c) => {
      const e = { l: c.l - r.left, t: c.t - r.top, r: r.right - c.r, b: r.bottom - c.b };
      if (Math.max(e.l, e.t, e.r, e.b) > tol) out.cut.push({ kind: 'clipped by ' + cls(c.cur), name: label, by: round(Math.max(e.l, e.t, e.r, e.b)), rect: [r.left, r.top, r.right, r.bottom].map(round) });
    });
  };
  targets.forEach((t) => { if (!t.cover) probe(t.el, t.el.getBoundingClientRect(), t.name, 'target'); });
  const seen = new Set(targets.map((t) => t.el));
  document.querySelectorAll(scope).forEach((root) => {
    const all = [root, ...root.querySelectorAll('*')];
    all.forEach((el) => {
      if (seen.has(el)) return;
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
      const svgText = el instanceof SVGTextElement;
      let rect = null;
      if (svgText) {
        rect = el.getBoundingClientRect();
      } else if (!(el instanceof SVGElement)) {
        const own = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim());
        if (own.length) {
          const range = document.createRange();
          range.selectNodeContents(el);
          const rects = [...range.getClientRects()].filter((q) => q.width > 0 && q.height > 0);
          if (rects.length) rect = { left: Math.min(...rects.map((q) => q.left)), top: Math.min(...rects.map((q) => q.top)), right: Math.max(...rects.map((q) => q.right)), bottom: Math.max(...rects.map((q) => q.bottom)) };
        }
        if (isHidden(cs.overflowX) && el.scrollWidth > el.clientWidth + 1 && own.length) out.cut.push({ kind: 'text wider than box', name: name(el), by: el.scrollWidth - el.clientWidth, rect: [] });
      }
      if (rect && rect.right - rect.left > 0) probe(el, rect, name(el), 'text');
    });
  });
  const de = document.documentElement;
  if (de.scrollWidth > vw + 1 || de.scrollHeight > vh + 1 || document.body.scrollWidth > vw + 1 || document.body.scrollHeight > vh + 1) out.doc = [de.scrollWidth, de.scrollHeight, document.body.scrollWidth, document.body.scrollHeight];
  return out;
};

const POPUP_TARGETS = () => {
  const out = [];
  controls.forEach((c) => {
    if (!c.el.isConnected || c.def.guard || (c.def.type !== 'selector' && c.def.type !== 'knob')) return;
    const r = c.el.getBoundingClientRect();
    if (!(r.width > 0 && r.height > 0) || getComputedStyle(c.el).display === 'none') return;
    if (c.def.type === 'selector' && (c.def.style === 'cap' || c.el.querySelector('.pos'))) return;
    if (r.x < 0 || r.y < 0 || r.right > window.innerWidth || r.bottom > window.innerHeight) return;
    out.push({ id: c.def.id, type: c.def.type, n: (c.def.positions || []).length, x: r.x + r.width / 2, y: r.y + r.height / 2 });
  });
  return out;
};

// ---- node side ----------------------------------------------------------------------------------------------------
async function main() {
  const browser = await chromium.launch({ executablePath: BROWSER, headless: true, args: ['--no-sandbox'] });
  try {
    layout = await selectAircraft();
    LABELS = layout.seats.map((x) => x.label);
    HOME = layout.views.find((v) => v.layout === 'map').name.toUpperCase();
    SHOTS = path.join(OUT, 'shots', slug(layout.aircraft));
    fs.mkdirSync(SHOTS, { recursive: true });
    const texts = sampleTexts();
    const seats = seatArg === null ? LABELS.map((_, i) => i) : [seatArg];
    for (const seat of seats) {
      if (!LABELS[seat]) throw new Error(`${layout.aircraft} has no seat ${seat}`);
      const simArgs = [`_ACFT_NAME=${ACFT}`, ...(LABELS.length > 1 ? [`SEAT_POSITION=${seat}`] : []), ...coverControls(seat).map((c) => `${c.id}=0`), ...texts];
      state.base = simArgs;
      state.args = simArgs;
      execFileSync(PYTHON, [SIM, '--reset']);
      execFileSync(PYTHON, [SIM, ...simArgs]);
      const keepAlive = setInterval(() => execFile(PYTHON, [SIM, ...state.args], () => {}), 1000);
      try {
        for (const [w, h] of sizes) await runOne(browser, seat, w, h);
      } finally {
        clearInterval(keepAlive);
      }
    }
  } finally {
    await browser.close();
  }
  report();
}

async function selectAircraft() {
  execFileSync(PYTHON, [SIM, '--reset']);
  let seen = null;
  for (let i = 0; i < 30; i++) {
    execFileSync(PYTHON, [SIM, `_ACFT_NAME=${ACFT}`]);
    await sleep(500);
    seen = await (await fetch(BASE + '/layout')).json();
    if (ACFT.startsWith(seen.aircraft)) return seen;
  }
  throw new Error(`the bridge does not switch to ${ACFT} (/layout shows ${seen && seen.aircraft})`);
}

const expandSeat = (id, seat) => id.replace(/\{seat\}/g, layout.seats[seat].prefix);
const inSeat = (def, seat) => !def.seats || def.seats.includes(seat);

// the cover selectors of the panel pages of a seat (the flap of a button that needs it open); the page is measured with the cover open as well
function coverControls(seat) {
  const out = [];
  layout.views.forEach((v) => {
    if (!v.panel || !v.seats.includes(seat)) return;
    v.controls.forEach((c) => {
      if (c.type === 'selector' && c.style === 'cover' && inSeat(c, seat)) out.push({ view: v.name, id: expandSeat(c.id, seat), open: c.positions[c.positions.length - 1].value });
    });
  });
  return out;
}

// the sides of the display switch of a view (MPD L / T / R, MFCD L / R, CDU C / U) that the controls of a seat belong to
function expectedSides(name, seat) {
  const sides = new Set();
  layout.views.filter((v) => v.name === name && v.seats.includes(seat)).forEach((v) => v.controls.forEach((c) => { if (c.side && inSeat(c, seat)) sides.add(c.side); }));
  return [...sides].sort();
}

function jsonDir() {
  const code = 'import sys; sys.path.insert(0, sys.argv[1]); import config; print(config.load()["dcs"]["saved_games"])';
  const savedGames = execFileSync(PYTHON, ['-c', code, path.join(REPO, 'core')]).toString().trim();
  return path.join(savedGames, 'Scripts', 'DCS-BIOS', 'doc', 'json');
}

// a full-length text for every string output that a display of the aircraft shows (the widest case)
function sampleTexts() {
  const dir = jsonDir();
  const lengths = {};
  fs.readdirSync(dir).filter((f) => f.endsWith('.json')).forEach((f) => {
    Object.values(JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'))).forEach((cat) => Object.values(cat).forEach((c) => c.outputs.forEach((o) => {
      if (o.type === 'string') lengths[c.identifier + o.suffix] = o.max_length;
    })));
  });
  const alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const ids = new Set();
  layout.views.forEach((v) => v.controls.forEach((c) => {
    if (c.type !== 'display') return;
    (c.ids || [c.id]).forEach((id) => { if (id !== c.page) layout.seats.forEach((_, seat) => ids.add(expandSeat(id, seat))); });
  }));
  return [...ids].filter((id) => lengths[id]).map((id) => `${id}=${/COUNT/.test(id) ? '120' : alphabet.slice(0, lengths[id])}`);
}

async function runOne(browser, seat, width, height) {
  ctx = { size: `${width}x${height}`, seat, view: 'start' };
  console.log(`\n=== ${ctx.size} seat ${seat} (${LABELS[seat]}) ===`);
  const context = await browser.newContext({ viewport: { width, height } });
  const page = await context.newPage();
  const cdp = await context.newCDPSession(page);
  const errors = [];
  const commands = [];
  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  page.on('console', (m) => {
    if (m.type() !== 'error') return;
    if (/favicon/.test(m.location().url || '') || /favicon/.test(m.text())) return;
    errors.push('console.error: ' + m.text() + ' ' + (m.location().url || ''));
  });
  page.on('requestfailed', (r) => { if (!/favicon/.test(r.url())) errors.push('requestfailed: ' + r.url() + ' ' + (r.failure() || {}).errorText); });
  page.on('response', (r) => { if (r.status() >= 400 && !/favicon/.test(r.url())) errors.push('http ' + r.status() + ' ' + r.url()); });
  page.on('request', (r) => { if (r.method() === 'POST' && /\/command/.test(r.url())) commands.push(r.postData()); });

  const badge = () => page.evaluate(() => document.getElementById('seat').textContent.trim());
  const active = () => page.evaluate(() => ({ name: views[activeIndex].name, layout: views[activeIndex].layout || null, panel: !!views[activeIndex].panel, side: typeof mpdView !== 'undefined' && mpdView ? mpdView.side : null, seats: views[activeIndex].seats }));
  const switchSides = () => page.evaluate(() => (typeof mpdView !== 'undefined' && mpdView ? Object.keys(mpdView.buttons).filter((s) => getComputedStyle(mpdView.buttons[s]).display !== 'none') : null));
  const rectOf = (sel, nth = 0) => page.evaluate(([sel, nth]) => {
    const el = document.querySelectorAll(sel)[nth];
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return { x: r.x + r.width / 2, y: r.y + r.height / 2, w: r.width, h: r.height };
  }, [sel, nth]);
  const mouseClick = async (x, y) => { await page.mouse.click(x, y); await page.waitForTimeout(250); };
  const clickTab = async (label) => {
    const r = await page.evaluate((label) => {
      const el = [...document.querySelectorAll('#tabs .tab')].find((t) => t.textContent.trim().toUpperCase() === label);
      if (!el) return null;
      const b = el.getBoundingClientRect();
      return { x: b.x + b.width / 2, y: b.y + b.height / 2 };
    }, label);
    if (!r) return false;
    await mouseClick(r.x, r.y);
    return true;
  };
  const hold = async (x, y, ms = 750) => {
    await page.mouse.move(x, y);
    await page.mouse.down();
    await page.waitForTimeout(ms);
    await page.mouse.up();
    await page.waitForTimeout(300);
  };
  const markListeners = () => cdp.send('Runtime.evaluate', {
    expression: `(() => { const out = []; document.querySelectorAll('#tabs, #tabs *, #seat, #gear, #lamps *, #controls *, #settings *, #pages *, #chooser *, #kbar *').forEach((el) => { const l = getEventListeners(el); if (l.click || l.pointerdown || l.pointerup || l.touchstart) out.push(el); }); window.__sw = out; return out.length; })()`,
    includeCommandLineAPI: true,
    returnByValue: true,
  });
  const measure = async (scope, opts = {}) => {
    await markListeners();
    return page.evaluate(MEASURE, { scope, minSize: 56, overlap: true, ...opts });
  };
  const BASE_SCOPE = '#tabs, #seat, #gear, #lamps, #controls';
  const shot = async (name) => page.screenshot({ path: path.join(SHOTS, `s${seat}_${ctx.size}_${slug(name)}.png`) });
  const seen = new Set();
  const record = (res, label, popup = false) => {
    stats.push({ size: ctx.size, seat, view: label, targets: res.n, small: res.small.length, overlaps: res.overlaps.length, cut: res.cut.length, scroll: res.scroll });
    res.small.forEach((s) => add('small', s.name, `${s.w}x${s.h} px (box ${s.vw}x${s.vh})`, { cls: s.cls, w: s.w, h: s.h }));
    res.overlaps.forEach((o) => add('overlap', `${o.a} / ${o.b}`, `${o.ow}x${o.oh} px`, { cls: o.ca + ' / ' + o.cb }));
    res.cut.forEach((c) => add('cut', c.name, `${c.kind} by ${c.by} px ${c.rect.length ? '[' + c.rect.join(' ') + ']' : ''}`, { cls: c.kind }));
    res.covered.forEach((c) => add('covered', c.name, `centre covered by ${c.by}`));
    if (res.doc) add('cut', 'document', `scroll size ${res.doc.join('x')} exceeds the window`, { cls: 'document' });
  };
  const measureView = async (label, opts = {}) => {
    ctx.view = label;
    const res = await measure(BASE_SCOPE);
    record(res, label);
    await shot(label);
    if (opts.popups !== false) {
      const cands = await page.evaluate(POPUP_TARGETS);
      const picks = [];
      const sel = cands.filter((c) => c.type === 'selector').sort((x, y) => y.n - x.n)[0];
      const knob = cands.filter((c) => c.type === 'knob')[0];
      if (sel) picks.push(sel);
      if (knob) picks.push(knob);
      for (const pick of picks) {
        await page.mouse.click(pick.x, pick.y);
        await page.waitForTimeout(200);
        const which = await page.evaluate(() => (document.body.classList.contains('pick-open') ? 'chooser' : document.body.classList.contains('knob-open') ? 'knob bar' : null));
        ctx.view = `${label} [${which || pick.type} ${pick.id.replace('{seat}_', '')}]`;
        check(`${label}: tap on ${pick.type} ${pick.id.replace('{seat}_', '')} opens a pop-up`, !!which, 'no chooser and no knob bar opened');
        if (which) {
          const r2 = await measure(which === 'chooser' ? '#chooser' : '#kbar');
          record(r2, ctx.view);
          const box = await page.evaluate((id) => { const r = document.getElementById(id).getBoundingClientRect(); const a = document.getElementById('controls').getBoundingClientRect(); return { l: r.left, t: r.top, r: r.right, b: r.bottom, area: a.top, w: innerWidth, h: innerHeight }; }, which === 'chooser' ? 'chooser' : 'kbar');
          if (box.l < 7.5 || box.r > box.w - 7.5 || box.t < box.area + 7.5 || box.b > box.h - 7.5) add('cut', which + ' ' + pick.id, `${which} [${[box.l, box.t, box.r, box.b].map(Math.round).join(' ')}] closer than 8 px to the window edge or the tab bar`, { cls: which + ' near edge' });
          if (which === 'chooser') await shot(label + ' chooser');
        }
        await page.evaluate(() => closePopups());
        await page.waitForTimeout(100);
      }
      ctx.view = label;
    }
    if (!seen.has(label)) seen.add(label);
  };

  await page.goto(BASE, { waitUntil: 'load' });
  await page.waitForFunction((label) => {
    const el = document.getElementById('seat');
    return el && el.textContent.includes(label) && !/NO DCS|OFFLINE/.test(el.textContent);
  }, LABELS[seat], { timeout: 20000 });
  await page.waitForTimeout(700);
  check('badge shows ' + LABELS[seat], (await badge()) === LABELS[seat], await badge());
  const tabNames = await page.evaluate(() => [...document.querySelectorAll('#tabs .tab')].map((t) => t.textContent.trim()));
  const wantTabs = [...new Set(layout.views.filter((v) => !v.panel).map((v) => v.name.toUpperCase()))];
  check('tab bar ' + wantTabs.join(' '), JSON.stringify(tabNames) === JSON.stringify(wantTabs), tabNames);
  const tabsOnce = {};

  // ---- tabs
  for (const name of tabNames) {
    ctx.view = 'tab ' + name;
    check('click tab ' + name, await clickTab(name));
    await page.waitForTimeout(300);
    const a = await active();
    check('tab ' + name + ' opens the view of the seat', a.name.toUpperCase() === name && a.seats.includes(seat), a);
    const sides = await switchSides();
    if (sides) {
      const want = expectedSides(a.name, seat);
      check(name + ' switch shows the sides ' + want.join(' '), JSON.stringify([...sides].sort()) === JSON.stringify(want), sides);
      for (const side of sides) {
        const r = await page.evaluate((side) => { const b = mpdView.buttons[side].getBoundingClientRect(); return { x: b.x + b.width / 2, y: b.y + b.height / 2 }; }, side);
        await mouseClick(r.x, r.y);
        const cur = (await active()).side;
        check(name + ' side switch ' + side, cur === side, cur);
        await measureView(name + ' ' + side);
      }
    } else if (name === HOME) {
      await measureView(HOME + ' map');
    } else {
      await measureView(name);
    }
  }

  // ---- the map boxes
  await clickTab(HOME);
  const boxes = await page.evaluate(() => [...document.querySelectorAll('button.mapbox')].map((b) => ({ label: b.textContent.trim(), link: b.classList.contains('link') })));
  const expected = await page.evaluate((seat) => pageEntries(seat).map((e) => ({ label: e.label.toUpperCase(), link: e.link })), seat);
  check('map boxes = page entries of the seat (' + expected.length + ')', JSON.stringify(boxes) === JSON.stringify(expected), { boxes, expected });
  for (const box of boxes) {
    ctx.view = 'map box ' + box.label;
    const r = await page.evaluate((label) => { const b = [...document.querySelectorAll('button.mapbox')].find((x) => x.textContent.trim() === label); const q = b.getBoundingClientRect(); return { x: q.x + q.width / 2, y: q.y + q.height / 2 }; }, box.label);
    await mouseClick(r.x, r.y);
    const a = await active();
    if (box.link) {
      const link = layout.views.find((v) => v.layout === 'map').links.find((l) => l.label.toUpperCase() === box.label && l.seats.includes(seat));
      const want = link.view.toUpperCase();
      const side = link.side || null;
      check('map box ' + box.label + ' opens ' + want + (side ? ' side ' + side : ''), a.name.toUpperCase() === want && (!side || a.side === side), a);
    } else {
      check('map box ' + box.label + ' opens its page', a.panel && a.name.toUpperCase() === box.label && a.seats.includes(seat), a);
      await measureView('page ' + box.label);
      const back = await page.evaluate(() => { const t = document.querySelector('#tabs .tab'); return { x: t.getBoundingClientRect().x + t.getBoundingClientRect().width / 2, y: t.getBoundingClientRect().y + t.getBoundingClientRect().height / 2, chev: !!t.querySelector('svg') }; });
      check('page ' + box.label + ': ' + HOME + ' tab shows the back chevron', back.chev);
      await mouseClick(back.x, back.y);
      check('page ' + box.label + ': one tap on ' + HOME + ' goes back to the map', (await active()).layout === 'map', await active());
      continue;
    }
    await clickTab(HOME);
  }

  // ---- state dependent: a cover selector of a panel page open (the page is drawn differently)
  for (const cover of coverControls(seat)) {
    state.args = [...state.base, `${cover.id}=${cover.open}`];
    execFileSync(PYTHON, [SIM, ...state.args]);
    await page.waitForTimeout(1500);
    await clickTab(HOME);
    const r = await page.evaluate((label) => { const b = [...document.querySelectorAll('button.mapbox')].find((x) => x.textContent.trim() === label); const q = b.getBoundingClientRect(); return { x: q.x + q.width / 2, y: q.y + q.height / 2 }; }, cover.view.toUpperCase());
    await mouseClick(r.x, r.y);
    check(cover.view + ' page opens with ' + cover.id + ' open', (await active()).name === cover.view);
    await measureView('page ' + cover.view + ' (' + cover.id + ' open)');
    state.args = [...state.base];
    execFileSync(PYTHON, [SIM, ...state.args]);
    await page.waitForTimeout(1500);
    await clickTab(HOME);
  }

  // ---- the long-hold page list
  ctx.view = 'page list';
  await clickTab(HOME);
  const tabR = await rectOf('#tabs .tab', 0);
  await hold(tabR.x, tabR.y);
  const listOpen = await page.evaluate(() => document.getElementById('pages').classList.contains('open'));
  check('long hold on ' + HOME + ' opens the page list', listOpen);
  if (listOpen) {
    const names = await page.evaluate(() => [...document.querySelectorAll('#pagelist > *')].map((e) => e.textContent.trim()));
    check('page list = map boxes', JSON.stringify(names) === JSON.stringify(boxes.map((b) => b.label)), { names, boxes: boxes.map((b) => b.label) });
    const res = await measure('#pages');
    record(res, 'page list');
    await shot('page list');
    for (const name of names) {
      const r = await page.evaluate((name) => { const b = [...document.querySelectorAll('#pagelist > *')].find((x) => x.textContent.trim() === name); const q = b.getBoundingClientRect(); return { x: q.x + q.width / 2, y: q.y + q.height / 2 }; }, name);
      await mouseClick(r.x, r.y);
      const a = await active();
      const entry = boxes.find((b) => b.label === name);
      const target = entry.link ? layout.views.find((v) => v.layout === 'map').links.find((l) => l.label.toUpperCase() === name && l.seats.includes(seat)).view.toUpperCase() : name;
      const ok = entry.link ? a.name.toUpperCase() === target : (a.panel && a.name.toUpperCase() === name);
      check('page list entry ' + name + ' opens its page', ok, a);
      await clickTab(HOME);
      const tr = await rectOf('#tabs .tab', 0);
      await hold(tr.x, tr.y);
    }
    await page.evaluate(() => document.getElementById('pageclose').click());
    await page.waitForTimeout(250);
    check('page list closes', !(await page.evaluate(() => document.getElementById('pages').classList.contains('open'))));
  }
  const tr2 = await rectOf('#tabs .tab', 0);
  await mouseClick(tr2.x, tr2.y);

  // ---- settings
  ctx.view = 'settings';
  await clickTab(HOME);
  const gear = await rectOf('#gear');
  await mouseClick(gear.x, gear.y);
  const setOpen = await page.evaluate(() => document.getElementById('settings').classList.contains('open'));
  check('settings page opens', setOpen);
  if (setOpen) {
    const res = await measure('#settings');
    record(res, 'settings');
    await shot('settings');
    const back = await rectOf('#back');
    await mouseClick(back.x, back.y);
    check('settings page closes with BACK', !(await page.evaluate(() => document.getElementById('settings').classList.contains('open'))));
  }

  // ---- debug seat
  if (LABELS.length > 1) {
    const other = 1 - seat;
    const seatR = await rectOf('#seat');
    ctx.view = 'debug seat';
    const before = commands.length;
    await hold(seatR.x, seatR.y);
    const bt = await badge();
    check('long hold on the badge: DEBUG ' + LABELS[other], bt === 'DEBUG ' + LABELS[other], bt);
    check('debug seat is ' + other, (await page.evaluate(() => debugSeat)) === other);
    await clickTab(HOME);
    const dBoxes = await page.evaluate(() => [...document.querySelectorAll('button.mapbox')].map((b) => b.textContent.trim()));
    const dEntries = await page.evaluate((s) => pageEntries(s).map((e) => ({ label: e.label.toUpperCase(), link: e.link })), other);
    const dExpected = dEntries.map((e) => e.label);
    const dPanels = dEntries.filter((e) => !e.link).map((e) => e.label);
    check('debug seat: map shows the pages of ' + LABELS[other], JSON.stringify(dBoxes) === JSON.stringify(dExpected), { dBoxes, dExpected });
    await shot('debug ' + LABELS[other] + ' map');
    let enabled = 0;
    let clicked = 0;
    const readOnlyView = async (label) => {
      const info = await page.evaluate(() => {
        const list = (window.__sw || []).filter((el) => el.isConnected && el.closest('#controls, #lamps') && el.hasAttribute('aria-disabled') && el.getBoundingClientRect().width > 0);
        return list.map((el) => {
          const r = el.getBoundingClientRect();
          return { dis: el.getAttribute('aria-disabled'), x: r.x + r.width / 2, y: r.y + r.height / 2, cls: (el.getAttribute('class') || '').split(' ')[0] };
        });
      });
      enabled += info.filter((i) => i.dis !== 'true').length;
      for (const i of info.slice(0, 20)) {
        if (i.x < 0 || i.y < 0 || i.x > width || i.y > height) continue;
        await page.mouse.click(i.x, i.y);
        clicked++;
        await page.waitForTimeout(40);
        await page.evaluate(() => closePopups());
      }
      return info.length;
    };
    const dTabs = await page.evaluate(() => [...document.querySelectorAll('#tabs .tab')].map((t) => t.textContent.trim()));
    let disabledSeen = 0;
    for (const name of dTabs) {
      await clickTab(name);
      await page.waitForTimeout(250);
      await markListeners();
      const a = await active();
      check('debug seat: tab ' + name + ' opens a view of seat ' + other, a.seats.includes(other), a);
      const sides = await switchSides();
      if (sides) {
        const want = expectedSides(a.name, other);
        check('debug seat: ' + name + ' switch shows the sides ' + want.join(' '), JSON.stringify([...sides].sort()) === JSON.stringify(want), sides);
      }
      disabledSeen += await readOnlyView(name);
      await shot('debug ' + LABELS[other] + ' ' + name);
    }
    for (const label of dPanels.slice(0, 4)) {
      await clickTab(HOME);
      const r = await page.evaluate((label) => { const b = [...document.querySelectorAll('button.mapbox')].find((x) => x.textContent.trim() === label); const q = b.getBoundingClientRect(); return { x: q.x + q.width / 2, y: q.y + q.height / 2 }; }, label);
      await mouseClick(r.x, r.y);
      await markListeners();
      disabledSeen += await readOnlyView('page ' + label);
      if (label === dPanels[0]) await shot('debug ' + LABELS[other] + ' page ' + label);
    }
    check('debug seat: every control disabled (' + disabledSeen + ' controls, ' + clicked + ' clicks)', enabled === 0 && disabledSeen > 50, { enabled, disabledSeen });
    check('debug seat: no command left the page', commands.length === before, commands.slice(before));
    const bt2 = await badge();
    check('debug seat: badge still DEBUG ' + LABELS[other], bt2 === 'DEBUG ' + LABELS[other], bt2);
    const seatR2 = await rectOf('#seat');
    await hold(seatR2.x, seatR2.y);
    const bt3 = await badge();
    check('second long hold returns to ' + LABELS[seat], bt3 === LABELS[seat], bt3);
    check('debug seat cleared', (await page.evaluate(() => debugSeat)) === null);
    const own = layout.views.find((v) => !v.panel && v.seats.includes(seat) && !v.seats.includes(other)) || layout.views.find((v) => !v.panel && v.layout !== 'map');
    await clickTab(own.name.toUpperCase());
    const af = await active();
    check(own.name.toUpperCase() + ' is the page of the real seat again', af.name === own.name && JSON.stringify(af.seats) === JSON.stringify(own.seats), af);
    await markListeners();
    const ownCtl = await page.evaluate(() => (window.__sw || []).filter((el) => el.isConnected && el.closest('#controls') && el.getAttribute('aria-disabled') === 'false' && el.getBoundingClientRect().width > 0).length);
    check('real seat: controls enabled again', ownCtl > 0, ownCtl);
  }

  // ---- errors
  ctx.view = 'errors';
  check('no page or console errors (favicon 404 ignored)', errors.length === 0, errors);
  await context.close();
}

function report() {
  const lines = [];
  const out = (s = '') => { lines.push(s); console.log(s); };
  out('\n==== CHECKS ====');
  const failed = checks.filter((c) => !c.ok);
  out(`${checks.length - failed.length} PASS, ${failed.length} FAIL of ${checks.length}`);
  failed.forEach((c) => out(`FAIL  ${c.size} seat ${c.seat}  ${c.name}  ${(JSON.stringify(c.info) || '').slice(0, 300)}`));

  out('\n==== PER VIEW (targets / small / overlaps / cut) ====');
  stats.forEach((s) => out(`${s.size}  seat ${s.seat}  ${s.view.padEnd(46)} targets ${String(s.targets).padStart(3)}  small ${String(s.small).padStart(3)}  overlaps ${String(s.overlaps).padStart(3)}  cut ${String(s.cut).padStart(3)}${s.scroll ? '  (in a scroller: ' + s.scroll + ')' : ''}`));

  out('\n==== FINDINGS (grouped; views = where seen) ====');
  const groups = new Map();
  findings.filter((f) => f.kind !== 'FAIL').forEach((f) => {
    const sizeKey = f.kind === 'small' ? `${f.w}x${f.h}` : f.detail.replace(/\[.*\]/, '').replace(/\d+(\.\d+)? px/g, 'N px').slice(0, 60);
    const key = [f.size, f.seat, f.kind, f.cls || f.element, sizeKey].join('|');
    const g = groups.get(key) || { f, views: new Set(), count: 0, examples: new Set() };
    g.views.add(f.view);
    g.count++;
    if (g.examples.size < 3) g.examples.add(f.element);
    groups.set(key, g);
  });
  const rows = [...groups.values()].sort((a, b) => a.f.kind.localeCompare(b.f.kind) || a.f.size.localeCompare(b.f.size) || a.f.seat - b.f.seat);
  out(`${rows.length} groups, ${findings.filter((f) => f.kind !== 'FAIL').length} raw findings`);
  rows.forEach((g) => {
    const v = [...g.views];
    out(`${g.f.kind.padEnd(7)} ${g.f.size} seat ${g.f.seat}  x${g.count}  ${[...g.examples].join(' ; ').slice(0, 80)}  =>  ${g.f.detail.slice(0, 90)}  | views: ${v.slice(0, 6).join(', ')}${v.length > 6 ? ' +' + (v.length - 6) : ''}`);
  });
  fs.writeFileSync(path.join(OUT, `sweep_${slug(layout.aircraft)}_results.json`), JSON.stringify({ checks, stats, findings }, null, 1));
  fs.writeFileSync(path.join(OUT, `sweep_${slug(layout.aircraft)}_table.txt`), lines.join('\n') + '\n');
  process.exitCode = failed.length ? 1 : 0;
}

main().catch((e) => { console.error(e); process.exit(1); });
