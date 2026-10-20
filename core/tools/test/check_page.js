// usage: node check_page.js <width> <height> [seat 0|1] [_ACFT_NAME, default AH-64D_BLK_II]   (the seat only counts for an aircraft with two seats)
// Opens the dashboard in headless Chromium, runs core/tools/check_panels.js in the page, prints its JSON report.
// Screenshot: logs/test/shot_<width>x<height>_<seat>.png. Environment: DASHBOARD_URL (default http://127.0.0.1:8080),
// CHROMIUM_PATH (a Chromium binary; default: the browser of the playwright package).
const fs = require('fs');
const path = require('path');
const { execFile, execFileSync } = require('child_process');
const { chromium } = require('playwright');

const HERE = __dirname;
const REPO = path.join(HERE, '..', '..', '..');
const OUT = path.join(REPO, 'logs', 'test');
const CHECKER = path.join(HERE, '..', 'check_panels.js');
const BASE_URL = process.env.DASHBOARD_URL || 'http://127.0.0.1:8080';
const PYTHON = process.platform === 'win32' ? 'python' : 'python3';

(async () => {
  const [w, h, seatArg, acftArg] = process.argv.slice(2);
  const width = parseInt(w, 10);
  const height = parseInt(h, 10);
  const seat = seatArg === undefined ? 0 : parseInt(seatArg, 10);
  if (!width || !height || ![0, 1].includes(seat)) {
    console.error('usage: node check_page.js <width> <height> [seat 0|1] [_ACFT_NAME]');
    process.exit(2);
  }
  const acft = acftArg === undefined ? 'AH-64D_BLK_II' : acftArg;
  fs.mkdirSync(OUT, { recursive: true });
  const SIM = path.join(HERE, 'sim.py');
  execFileSync(PYTHON, [SIM, `_ACFT_NAME=${acft}`]);
  let layout = null;
  for (let i = 0; i < 30 && !(layout && acft.startsWith(layout.aircraft)); i++) {
    await new Promise((r) => setTimeout(r, 500));
    layout = await (await fetch(BASE_URL + '/layout')).json();
  }
  if (!layout || !acft.startsWith(layout.aircraft)) throw new Error(`the bridge does not switch to ${acft} (/layout shows ${layout && layout.aircraft})`);
  const twoSeats = layout.seats.length > 1;
  const simArgs = [SIM, `_ACFT_NAME=${acft}`, ...(twoSeats ? [`SEAT_POSITION=${seat}`] : [])];
  const sim = () => execFile(PYTHON, simArgs, () => {});
  execFileSync(PYTHON, simArgs);
  const keepAlive = setInterval(sim, 1000); // the page treats DCS data older than 3 s as stale

  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined, headless: true, args: ['--no-sandbox'] });
  try {
    const page = await browser.newPage({ viewport: { width, height } });
    const logs = [];
    page.on('console', (msg) => logs.push(msg.text()));
    await page.goto(BASE_URL, { waitUntil: 'load' });
    const label = layout.seats[twoSeats ? seat : 0].label;
    await page.waitForFunction((label) => {
      const el = document.getElementById('seat');
      return el && el.textContent.includes(label) && !/NO DCS|OFFLINE/.test(el.textContent);
    }, label, { timeout: 15000 });
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(OUT, `shot_${width}x${height}_${seat}.png`) });
    const src = fs.readFileSync(CHECKER, 'utf8');
    const result = await page.evaluate(`(async () => {\n${src}\n})()`);
    void result;
    const report = [...logs].reverse().find((t) => t.startsWith('{') && t.includes('"problems"'));
    if (!report) throw new Error('no report from checker; console: ' + logs.slice(-5).join(' | '));
    console.log(report);
  } finally {
    clearInterval(keepAlive);
    await browser.close();
  }
})().catch((e) => { console.error(e); process.exit(1); });
