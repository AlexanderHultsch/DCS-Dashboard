# DCS-Dashboard

A simple tablet dashboard for the **AH-64D Apache** in DCS World. A small Python bridge connects to DCS via [DCS-BIOS](https://github.com/DCS-Skunkworks/dcs-bios) and serves an HTML page you open on an iPad or any tablet. Big touch buttons replace keyboard combinations for cockpit commands and George, the AI copilot.

**Status:** Stage 1 (read data) is built and tested on Windows. Results: [docs/STAGE1.md](docs/STAGE1.md#results). Stage 2 (control) is tested on Windows. Results: [docs/STAGE2.md](docs/STAGE2.md#results). Stage 3 (dashboard): the tabs COCKPIT, FLIGHT, FIGHT, MPD and KU are built. COCKPIT is tested in an isolated setup only, the Flight, Fight, MPD and KU views are ready for their first test run in DCS. The old Startup view (tested on Windows) is replaced by the COCKPIT pages.

## Aircraft

**For the AH-64D only, for now.** Other aircraft may follow later, so the basic structure is kept reusable:

- Aircraft-independent: the bridge (`dashboard.py`, `bridge/`), settings, logging, the command and readback logic, and the page engine (tabs, controls, knob bar, cursor pad).
- AH-64D-specific: `aircraft/ah64d.py` (the views and their controls, seat prefixes, MPD indication numbers, trim data), the MPD / TEDAC / KU drawings in `web/index.html`, the control positions in `lua/DCS-Dashboard-Export.lua` and the `[keys]` in `config.toml`.
- The aircraft is chosen with `aircraft = "AH-64D"` in `config.toml`; a second aircraft would be a second module in `aircraft/` plus its own drawings.

## Plan

1. **Read** – test which data we can read from DCS (both seats, in flight). Details: [docs/STAGE1.md](docs/STAGE1.md)
2. **Control** – test which cockpit controls we can set from outside. Details: [docs/STAGE2.md](docs/STAGE2.md)
3. **Dashboard** – HTML page with tabs COCKPIT, FLIGHT, FIGHT, MPD and KU (built), George (later). Details: [docs/STAGE3.md](docs/STAGE3.md)

Overview: [docs/SPEC.md](docs/SPEC.md)

## Requirements

- Windows, DCS World with the AH-64D module
- Python 3.12 or newer
- Single player (multiplayer servers may block exports)

## Getting started

In the paths below, `<Saved Games>` is your DCS Saved Games folder, usually `%USERPROFILE%\Saved Games\DCS` (or `DCS.openbeta`).

### 1. Python

Open a command prompt and run `python --version`. It must show 3.12 or newer. If not, install Python from [python.org](https://www.python.org/downloads/) and tick **Add python.exe to PATH** in the installer.

No extra Python packages are needed for Stage 1.

### 2. This repo

Download it with **Code → Download ZIP** on GitHub and unzip it, or clone it with git (URL under **Code** on GitHub).

### 3. DCS-BIOS

1. Download `DCS-BIOS_x.y.z.zip` from the [latest DCS-BIOS release](https://github.com/DCS-Skunkworks/dcs-bios/releases/latest).
2. Unzip it and copy the `DCS-BIOS` folder into `<Saved Games>\Scripts\`. Create the `Scripts` folder if it does not exist.
3. If `<Saved Games>\Scripts\Export.lua` does not exist, copy the `Export.lua` from the zip there. If it exists, add this line at the end:

   ```lua
   dofile(lfs.writedir() .. [[Scripts\DCS-BIOS\BIOS.lua]])
   ```

4. Check that `<Saved Games>\Scripts\DCS-BIOS\doc\json\AH-64D.json` exists. It comes with the DCS-BIOS zip.

### 4. Export script

1. Copy `lua\DCS-Dashboard-Export.lua` from this repo into `<Saved Games>\Scripts\`.
2. Add this line at the end of `<Saved Games>\Scripts\Export.lua`, after the DCS-BIOS line:

   ```lua
   dofile(lfs.writedir() .. [[Scripts\DCS-Dashboard-Export.lua]])
   ```

After an update of the repo, copy the export script again and restart the mission.

### 5. Config

Copy `config.example.toml` to `config.toml` in the repo folder. `saved_games = "auto"` finds the DCS Saved Games folder by itself; set a path only if that fails. `config.toml` stays on your machine and is never committed.

### 6. Run Stage 1

1. In the repo folder run `python stage1_read.py`. If Windows asks to allow Python on the network, allow it for private networks.
2. Start DCS and an AH-64D mission. Changed values appear in the console.
3. Stop with Ctrl+C. The script prints a summary. The full log is in `logs\dcs-dashboard.log`.

The test procedure is in [docs/STAGE1.md](docs/STAGE1.md#test-run-windows-manual).

### 7. Run Stage 2

1. Add the `window_title` line and the `[keys]` section from `config.example.toml` to your `config.toml`.
2. Start DCS in windowed or borderless mode and an AH-64D mission, cold and dark, battery off.
3. In the repo folder run `python stage2_sweep.py` and press Enter when asked. Do not touch the controls for about 2 minutes.
4. Turn the battery on (George needs power), run `python stage2_sweep.py keys` and answer each key test with y, n or s.
5. Restart the mission, switch to the CP/G seat (key `2`) and repeat steps 3 and 4.

Results are in `logs\stage2_results.csv`. The test procedure is in [docs/STAGE2.md](docs/STAGE2.md#test-run-windows-manual).

### 8. Run the dashboard

1. Start DCS in windowed or borderless mode. The tablet and the PC must be on the same network.
2. Double-click `start_dashboard.bat` in the repo folder (or run `python dashboard.py`). It prints the address to open, for example `http://<PC address>:8080`. If Windows asks to allow Python on the network, allow it for private networks.
3. Open that address in the tablet's browser. On an iPad: Share → Add to Home Screen. The page then runs full screen with its own icon; scrolling and zooming are switched off. To get a new icon after an update, remove the home screen app and add it again.
4. Load an AH-64D mission. The tabs are COCKPIT, FLIGHT, FIGHT, MPD and KU. All of them follow the seat you are in.
5. Stop with Ctrl+C or close the window.

The power levers are moved by keypresses, so DCS must be the active window on the PC; the dashboard brings it to the front itself. The test procedure is in [docs/STAGE3.md](docs/STAGE3.md#test-run-windows-manual).

**COCKPIT.** The COCKPIT tab shows a simple map of the cockpit of the current seat. Each box is a cockpit panel. Tap a box to open the page of that panel: the real labels, switch positions and lamps, laid out as on the panel (POWER, EMERGENCY, FIRE DET/EXTG, ARMAMENT, EUFD, COMM and more; the pilot and the CP/G have their own pages). A long hold on the COCKPIT tab lists all pages of the seat. On a page the tab reads `◀ COCKPIT`; one tap returns to the map. Guarded controls (the fire buttons, the extinguisher discharge, store jettison, zeroize and the CMWS flare jettison) need two steps: tap the cover to lift it, then press the control and hold it for 1 second. On COMM, holding a radio knob for 0.6 seconds pulls it out or pushes it in. Details: [docs/COCKPIT.md](docs/COCKPIT.md).

The gear button at the bottom right opens the settings: logging on or off (remembered on the PC), keep the tablet screen on, and information such as the detected DCS folder and the address for another tablet. The iPad cannot lock the rotation from a web page; use the rotation lock in Control Center. In portrait the page shows a hint to turn the iPad.

The export script writes one `export timing` line per minute of model time to the DCS log (`dcs.log`, source DCS-Dashboard), so its cost inside DCS can be read. After an update of the repo, copy the export script again to `<Saved Games>\Scripts\` and restart the mission, as in step 4 of Getting started. Only the updated script writes the timing line.
