# Developer test kit

For developers only; users of the dashboard never need it. It lets you retest a change to the bridge, the page or an aircraft file without playing DCS: a test bridge with a fake keyboard, a simulator that sends DCS-BIOS values, and checks that drive the page in a headless browser. It runs on Windows and on Linux.

Everything the kit writes (screenshots, key log, simulator memory, results) goes to `logs/test/`, which git ignores.

## Requirements

- Python 3.12 or newer (the same as the dashboard; `python` on Windows, `python3` on Linux)
- Node.js 18 or newer with the `playwright` package and a Chromium browser. In this folder run `npm install playwright` and `npx playwright install chromium`. To use a Chromium you already have, set `CHROMIUM_PATH` to its binary instead of the second command.
- Lua 5.1, only for `gen_json.lua` (see step 1)

## Use

All commands run from the repository root. On Linux write `python3` instead of `python`.

1. **DCS-BIOS control lists.** The bridge and `sim.py` read the DCS-BIOS JSON files from `<Saved Games>/Scripts/DCS-BIOS/doc/json`, the folder set by `saved_games` in `config/config.toml`.
   - On Windows with DCS-BIOS installed, the real files are used and you have nothing to do.
   - Without DCS (for example on Linux), generate the files from a DCS-BIOS source checkout: `DCSBIOS_REPO=<checkout> lua5.1 core/tools/test/gen_json.lua`. They go to `logs/test/sg` (another folder: pass it as the first argument). Then point the dashboard at that folder in the local, git-ignored `config/config.toml`:

     ```toml
     [dcs]
     saved_games = "<repo>/logs/test/sg"
     ```

2. **Start the test bridge** in its own terminal and leave it running: `python core/tools/test/bridge.py`. It is the normal dashboard (`core/dashboard.py`, port 8080) with a fake `keys` module: no key is ever pressed, every press is logged with its duration to `logs/test/keys.log`. Ctrl+C stops it. Stop the real dashboard first; both use port 8080. With another address, set `DASHBOARD_URL` (default `http://127.0.0.1:8080`) for the checks.

3. **Send values** from a second terminal. The page treats data older than 3 seconds as stale; the checks below send their own values and repeat them every second, so this step is only for looking at the page by hand.

   ```
   python core/tools/test/sim.py --reset
   python core/tools/test/sim.py _ACFT_NAME=AH-64D_BLK_II SEAT_POSITION=0
   python core/tools/test/sim.py _ACFT_NAME=A-10C_2
   ```

   `sim.py NAME=VALUE ...` sets integer outputs by number and string outputs by text. `--json DIR` reads the control lists from `DIR` instead of the configured folder. The simulated memory is kept in `logs/test/sim_state.bin`; `--reset` clears it.

4. **Run the checks** (second terminal, bridge running):

   | Command | What it does | A pass looks like |
   | --- | --- | --- |
   | `node core/tools/test/check_page.js 1180 820 0` | runs `core/tools/check_panels.js` (the layout checker) in the page; arguments: width, height, seat 0 or 1, optional `_ACFT_NAME` (default `AH-64D_BLK_II`, for the A-10C use `A-10C_2`) | the printed report has `"problems":{}`; screenshot in `logs/test/` |
   | `python core/tools/test/smoke.py [--acft NAME] [--seat 0\|1] PAGE ...` | posts one command per control of the named pages (a page or tab name as shown in the dashboard) and checks the DCS-BIOS command that arrives on UDP port 7778, or the key presses in `logs/test/keys.log` for key, macro and lever controls | every line `PASS` (or `SKIP` for display-only controls), last line `all PASS`, exit code 0 |
   | `node core/tools/test/sweep.js [--acft NAME] [--seat N] [--size WxH]` | opens every tab, side and page of an aircraft (default `AH-64D_BLK_II`) in every seat at 1180 x 820 and 1024 x 768, measures the touch targets and cut-off text, tries the debug seat | no `FAIL` line; the findings list (targets under 56 px and so on) is information, not a failure; results in `logs/test/` |
   | `python core/tools/test/coverage.py [PAGE ...]` | compares the DCS-BIOS ids of the A-10C pages with `docs/A10C` | per page `missing [...]`; a change must not raise `TOTAL missing` |

   Run `check_page.js` at 1180 x 820 and 1024 x 768 in both seats of the AH-64D (seat 0 and 1) and once for the A-10C, after any change to a page. For the AH-64D run `smoke.py` once per seat (`--acft AH-64D_BLK_II --seat 0`, then `--seat 1`).
