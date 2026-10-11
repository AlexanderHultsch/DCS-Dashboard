// Layout checker for the kit panel pages (docs/COCKPIT_FIXES.md, section 8).
//
// Usage: open the dashboard, choose the seat, then paste this file into the browser console (or run it with a
// browser tool that allows top-level await). It opens every kit page of the current seat through the long-hold
// page list of the COCKPIT tab, measures the drawn labels, parts, screws, ears and the plate, and prints a compact
// JSON report. An empty "problems" object is the acceptance. Run it at 1180 x 820 and 1024 x 768 (reload after a
// resize), in the pilot and in the CP/G seat.
//
// Geometry is compared in design units (du): css px divided by the page scale S (plate css width / plate box width).
// A label box is its rendered text length by its font size (the uppercase text sits inside that height).
await (async () => {
  const LABEL_EDGE = 6;
  const PART_EDGE = 12;
  const EAR_CLEAR = 12;
  const COVER_MARGIN = 12;
  const TOUCH_MIN = 56;
  const TOUCH_OVERLAP = 6;
  const TOL = 0.5;
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const round = (v) => Math.round(v * 10) / 10;

  const tab = () => document.querySelector('.tab');
  async function openList() {
    const r = tab().getBoundingClientRect();
    const ev = (type) => new PointerEvent(type, { bubbles: true, pointerId: 9, pointerType: 'touch', clientX: r.x + 20, clientY: r.y + 10, isPrimary: true });
    tab().dispatchEvent(ev('pointerdown'));
    await sleep(650);
    tab().dispatchEvent(ev('pointerup'));
    await sleep(250);
  }
  const listNames = () => [...document.querySelectorAll('#pagelist > *')].map((e) => e.textContent.trim());

  const overlap = (a, b) => Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0) > TOL && Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0) > TOL;
  const grown = (b, d) => ({ x0: b.x0 - d, y0: b.y0 - d, x1: b.x1 + d, y1: b.y1 + d });
  const join = (a, b) => ({ x0: Math.min(a.x0, b.x0), y0: Math.min(a.y0, b.y0), x1: Math.max(a.x1, b.x1), y1: Math.max(a.y1, b.y1) });
  const inside = (a, b) => a.x0 >= b.x0 - TOL && a.y0 >= b.y0 - TOL && a.x1 <= b.x1 + TOL && a.y1 <= b.y1 + TOL;
  const same = (a, b) => ['x0', 'y0', 'x1', 'y1'].every((k) => Math.abs(a[k] - b[k]) <= TOL);
  const edgeGap = (a, p) => Math.min(a.x0 - p.x0, a.y0 - p.y0, p.x1 - a.x1, p.y1 - a.y1);
  const distinct = (values) => values.reduce((acc, v) => (acc.some((a) => Math.abs(a - v) <= TOL) ? acc : [...acc, v]), []);
  const show = (b) => '[' + [b.x0, b.y0, b.x1 - b.x0, b.y1 - b.y0].map(round).join(' ') + ']';

  function measure(pbox) {
    const [bw, bh] = pbox.dataset.box.split(' ').map(Number);
    const [rw, rh] = pbox.dataset.ref.split(' ').map(Number);
    const o = pbox.getBoundingClientRect();
    const S = o.width / bw;
    const du = (r, g = 0) => ({ x0: (r.left - o.left) / S - g, y0: (r.top - o.top) / S - g, x1: (r.right - o.left) / S + g, y1: (r.bottom - o.top) / S + g });
    const drawn = (el) => du(el.getBoundingClientRect(), (parseFloat(el.getAttribute('stroke-width')) || 0) / 2);
    const plateEl = pbox.querySelector('.k-plate');
    const screws = [...pbox.querySelectorAll('.k-screw')].map((g) => {
      const box = du(g.querySelector('circle').getBoundingClientRect());
      return { size: g.dataset.size, box, x: (box.x0 + box.x1) / 2, y: (box.y0 + box.y1) / 2 };
    });
    const labels = [...pbox.querySelectorAll('text.k-label')].map((el) => {
      const r = du(el.getBoundingClientRect());
      const size = parseFloat(el.getAttribute('font-size'));
      const x = parseFloat(el.getAttribute('x'));
      const y = parseFloat(el.getAttribute('y'));
      const turned = /rotate\((-?90|270)\s/.test(el.getAttribute('transform') || '');
      const box = turned ? { x0: x - size / 2, y0: r.y0, x1: x + size / 2, y1: r.y1 } : { x0: r.x0, y0: y - size / 2, x1: r.x1, y1: y + size / 2 };
      return { text: el.textContent, box };
    });
    const parts = [...pbox.querySelectorAll('[data-kit]')].map((el) => {
      const id = el.dataset.id;
      const bodyEl = el.querySelector('.k-body') || el;
      const body = du(bodyEl.getBoundingClientRect());
      const linked = (sel) => [...pbox.querySelectorAll(sel)].filter((a) => a.dataset.for === id).map(drawn);
      const frames = linked('.k-frame');
      const pads = linked('.k-pad');
      const coverEl = el.querySelector('.gcover');
      const cover = coverEl ? du(coverEl.getBoundingClientRect()) : null;
      const near = [body, ...frames, ...(cover ? [cover] : [])].reduce(join);
      const px = (b) => round((b.x1 - b.x0) * S) + 'x' + round((b.y1 - b.y0) * S);
      return { id, kind: el.dataset.kit, body, frames, pads, cover, near, outer: [near, ...pads].reduce(join), size: px(body), frameSize: frames.map(px), coverSize: cover ? px(cover) : null };
    });
    return { S, bw, bh, rw, rh, plate: plateEl ? drawn(plateEl) : { x0: 0, y0: 0, x1: bw, y1: bh }, ears: [...pbox.querySelectorAll('.k-ear')].map(drawn), screws, labels, parts };
  }

  function touchAreas() {
    const out = [];
    document.querySelectorAll('#controls *').forEach((el) => {
      const cs = getComputedStyle(el);
      if (cs.pointerEvents === 'none' || cs.display === 'none' || cs.visibility === 'hidden') return;
      const hw = el.style.getPropertyValue('--hw');
      const hh = el.style.getPropertyValue('--hh');
      const cover = el.classList.contains('gcover') || el.classList.contains('pcover');
      if (!hw && el.tagName !== 'BUTTON' && !cover) return;
      const b = el.getBoundingClientRect();
      if (!(b.width > 0)) return;
      const w = hw ? parseFloat(hw) : b.width;
      const h = hh ? parseFloat(hh) : b.height;
      const cx = b.x + b.width / 2;
      const cy = b.y + b.height / 2;
      const label = (el.getAttribute('aria-label') || el.textContent || '').trim().slice(0, 14) + '|' + el.className.toString().split(' ')[0];
      out.push({ el, label, cover, w, h, x0: cx - w / 2, x1: cx + w / 2, y0: cy - h / 2, y1: cy + h / 2 });
    });
    return out;
  }

  function check(d) {
    const out = [];
    const info = [];
    d.labels.forEach((l, i) => {
      d.parts.forEach((p) => {
        if (overlap(l.box, p.near)) out.push('label ' + l.text + ' overlaps part ' + p.id);
        p.pads.forEach((pad) => {
          if (overlap(l.box, pad) && !inside(l.box, pad)) out.push('label ' + l.text + ' overlaps the hazard pad of ' + p.id);
        });
      });
      d.labels.slice(i + 1).forEach((m) => {
        if (overlap(l.box, m.box)) out.push('labels ' + l.text + ' and ' + m.text + ' overlap');
      });
      if (d.screws.some((s) => overlap(l.box, s.box))) out.push('label ' + l.text + ' overlaps a screw');
      if (d.ears.some((e) => overlap(l.box, grown(e, EAR_CLEAR)))) out.push('label ' + l.text + ' closer than ' + EAR_CLEAR + ' du to an ear');
      if (edgeGap(l.box, d.plate) < LABEL_EDGE - TOL) out.push('label ' + l.text + ' closer than ' + LABEL_EDGE + ' du to the plate edge');
    });
    d.parts.forEach((p, i) => {
      d.parts.slice(i + 1).forEach((q) => {
        if (overlap(p.outer, q.outer)) out.push('parts ' + p.id + ' and ' + q.id + ' overlap');
      });
      if (d.ears.some((e) => overlap(p.outer, grown(e, EAR_CLEAR)))) out.push('part ' + p.id + ' closer than ' + EAR_CLEAR + ' du to an ear');
      if (edgeGap(p.outer, d.plate) < PART_EDGE - TOL) out.push('part ' + p.id + ' closer than ' + PART_EDGE + ' du to the plate edge');
      if (p.cover && !same(p.cover, grown(p.body, COVER_MARGIN))) out.push('cover of ' + p.id + ' ' + show(p.cover) + ' is not the part ' + show(p.body) + ' + ' + COVER_MARGIN + ' du');
    });
    const corner = d.screws.filter((s) => s.size === 'L');
    if (d.ears.length !== 4 || corner.length !== 4) out.push(d.ears.length + ' ears and ' + corner.length + ' corner screws, 4 each expected');
    d.ears.forEach((e) => {
      const cx = (e.x0 + e.x1) / 2;
      const cy = (e.y0 + e.y1) / 2;
      const hit = corner.filter((s) => s.x > e.x0 && s.x < e.x1 && s.y > e.y0 && s.y < e.y1);
      if (hit.length !== 1 || Math.abs(hit[0].x - cx) > TOL || Math.abs(hit[0].y - cy) > TOL) out.push('corner screw not in the centre of the ear ' + show(e));
    });
    if (distinct(corner.map((s) => s.x)).length !== 2 || distinct(corner.map((s) => s.y)).length !== 2) out.push('corner screws not on two shared x and two shared y lines');
    const xs = [d.plate.x0, d.plate.x1, (d.plate.x0 + d.plate.x1) / 2, ...corner.map((s) => s.x), ...d.parts.map((p) => (p.body.x0 + p.body.x1) / 2)];
    const ys = [d.plate.y0, d.plate.y1, (d.plate.y0 + d.plate.y1) / 2, ...corner.map((s) => s.y), ...d.parts.map((p) => (p.body.y0 + p.body.y1) / 2)];
    d.screws.filter((s) => s.size !== 'L').forEach((s) => {
      const others = d.screws.filter((t) => t !== s);
      const onX = [...xs, ...others.map((t) => t.x)].some((v) => Math.abs(v - s.x) <= TOL);
      const onY = [...ys, ...others.map((t) => t.y)].some((v) => Math.abs(v - s.y) <= TOL);
      if (!onX && !onY) info.push('screw ' + s.size + ' at ' + round(s.x) + ', ' + round(s.y) + ' shares no x or y line');
    });
    const touch = touchAreas();
    touch.forEach((t) => {
      if (t.w < TOUCH_MIN - TOL || t.h < TOUCH_MIN - TOL) out.push('touch area ' + t.label + ' ' + round(t.w) + 'x' + round(t.h) + ' px');
    });
    touch.forEach((a, i) => touch.slice(i + 1).forEach((b) => {
      if (a.cover || b.cover || a.el.contains(b.el) || b.el.contains(a.el)) return;
      const ow = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0);
      const oh = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0);
      if (ow >= TOUCH_OVERLAP && oh >= TOUCH_OVERLAP) out.push('touch areas ' + a.label + ' and ' + b.label + ' overlap ' + round(ow) + 'x' + round(oh) + ' px');
    }));
    if (d.bw > d.rw || d.bh > d.rh) out.push('plate ' + d.bw + 'x' + d.bh + ' du is bigger than ' + d.rw + 'x' + d.rh);
    return { out, info };
  }

  const kitNames = typeof views !== 'undefined' ? new Set(views.filter((v) => v.kit).map((v) => v.name.toUpperCase())) : null;
  const report = { viewport: innerWidth + 'x' + innerHeight, seat: document.getElementById('seat').textContent, pages: {}, sizes: {}, problems: {}, info: {} };
  const sizes = {};
  const note = (kind, size, page) => {
    const list = sizes[kind] || (sizes[kind] = []);
    const [w, h] = size.split('x').map(Number);
    const hit = list.find((e) => Math.abs(e.w - w) <= TOL && Math.abs(e.h - h) <= TOL);
    if (hit) hit.pages.add(page);
    else list.push({ w, h, size, pages: new Set([page]) });
  };
  await openList();
  const names = listNames().filter((n) => !kitNames || kitNames.has(n));
  document.getElementById('pageclose').click();
  for (const name of names) {
    await openList();
    const btn = [...document.querySelectorAll('#pagelist > *')].find((e) => e.textContent.trim() === name);
    if (!btn) continue;
    btn.click();
    await sleep(500);
    const pbox = document.querySelector('#controls .pbox.kit');
    if (!pbox) continue;
    const d = measure(pbox);
    const { out, info } = check(d);
    const parts = {};
    d.parts.forEach((p) => {
      parts[p.kind] = parts[p.kind] || p.size;
      note(p.kind, p.size, name);
      p.frameSize.forEach((s) => note(p.kind + ' frame', s, name));
      if (p.coverSize) note(p.kind + ' cover', p.coverSize, name);
    });
    report.pages[name] = { box: [d.bw, d.bh], S: Math.round(d.S * 10000) / 10000, parts };
    if (out.length) report.problems[name] = out;
    if (info.length) report.info[name] = info;
  }
  Object.keys(sizes).forEach((kind) => {
    report.sizes[kind] = sizes[kind].map((e) => e.size);
    if (sizes[kind].length > 1) {
      (report.problems['all pages'] = report.problems['all pages'] || []).push(kind + ' drawn in ' + sizes[kind].length + ' sizes: '
        + sizes[kind].map((e) => e.size + ' (' + [...e.pages].join(', ') + ')').join(', '));
    }
  });
  tab().held = false;
  tab().click();
  const text = JSON.stringify(report);
  console.log(text);
  return text;
})();
