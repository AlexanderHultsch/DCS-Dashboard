# DCS-Dashboard

A tablet dashboard for the **AH-64D Apache** in DCS World. A small Python bridge connects to DCS via [DCS-BIOS](https://github.com/DCS-Skunkworks/dcs-bios) and serves an HTML page you open on an iPad or any tablet. Touch panels replace keyboard combinations and mouse clicks for cockpit commands.

- **COCKPIT**: a map of the cockpit and one page per panel (POWER, FIRE, ARMAMENT, EUFD, COMM, lights and more), drawn like the real panels, for the pilot and the CP/G seat.
- **FLIGHT, FIGHT**: power levers, symbology, trim display, weapons, sights, countermeasures.
- **MPD, KU**: both MPD bezels with live button labels, the TEDAC (CP/G), the cursor pad and the keyboard unit.
- **GEORGE**: direct buttons for the AI crew member (search, targets, weapon, request control).

The dashboard follows the seat you are in. Everything is plain Python (standard library only) and one HTML file. Full description: [docs/SPEC.md](docs/SPEC.md).

**Status:** the cold start from the tablet works in DCS. The panel pages, FLIGHT, FIGHT, MPD and KU are tested against a simulated DCS-BIOS and are waiting for a full test run in DCS. Open points: [docs/FIXES.md](docs/FIXES.md).

## Requirements

- Windows, DCS World with the AH-64D module, single player (multiplayer servers may block exports)
- Python 3.12 or newer
- A tablet with a current browser (iPadOS 16 or newer, or a current Chrome) on the same network as the PC; designed for 1180 × 820 landscape, works from 1024 × 768

## Getting started

In the paths below, `<Saved Games>` is your DCS Saved Games folder, usually `%USERPROFILE%\Saved Games\DCS` (or `DCS.openbeta`).

1. **Python.** Run `python --version` in a command prompt; it must show 3.12 or newer. Otherwise install Python from [python.org](https://www.python.org/downloads/) and tick **Add python.exe to PATH**. No extra packages are needed.
2. **This repo.** Download it with **Code → Download ZIP** on GitHub and unzip it, or clone it with git.
3. **DCS-BIOS.** Download `DCS-BIOS_x.y.z.zip` from the [latest release](https://github.com/DCS-Skunkworks/dcs-bios/releases/latest), unzip it and copy the `DCS-BIOS` folder into `<Saved Games>\Scripts\`. If `<Saved Games>\Scripts\Export.lua` does not exist, copy the one from the zip there; if it exists, add this line at the end:

   ```lua
   dofile(lfs.writedir() .. [[Scripts\DCS-BIOS\BIOS.lua]])
   ```

4. **Export script.** Copy `core\lua\DCS-Dashboard-Export.lua` into `<Saved Games>\Scripts\` and add this line at the end of `Export.lua`, after the DCS-BIOS line:

   ```lua
   dofile(lfs.writedir() .. [[Scripts\DCS-Dashboard-Export.lua]])
   ```

   After an update of the repo, copy the script again and restart the mission.
5. **Config (optional).** The defaults fit a standard install and the DCS folder is found automatically. To change something (another DCS folder, ports, rebound keys), copy `config\config.example.toml` to `config\config.toml` and keep only the lines you change. That file stays on your machine and is never committed.
6. **Run.** Start DCS in windowed or borderless mode, then double-click `start_dashboard.bat` (or run `python core\dashboard.py`). It prints the address to open, for example `http://<PC address>:8080`. If Windows asks to allow Python on the network, allow it for private networks.
7. **Tablet.** Open that address in the tablet's browser. On an iPad: Share → Add to Home Screen; the page then runs full screen with its own icon. Load an AH-64D mission.

Stop the bridge with Ctrl+C or close the window.

The power levers, the canopy and a few other controls are moved by keypresses, so DCS must be the active window on the PC; the dashboard brings it to the front itself. The keys must match your DCS bindings; the defaults are in `aircraft\ah64d.py` and can be overridden in `[keys]` of `config\config.toml`.

The GEORGE tab uses its own keys (`LCtrl+LAlt` plus a letter), which are not DCS defaults. Bind them once in DCS under Options, Controls, in the AH-64D Pilot, CPG and George AI Helper entries; the table is in [docs/SPEC.md](docs/SPEC.md), section GEORGE. George needs electrical power.

The gear button at the bottom right opens the settings: logging on or off, keep the tablet screen on, and information such as the detected DCS folder. The iPad cannot lock the rotation from a web page; use the rotation lock in Control Center.

## Repository

```
start_dashboard.bat   starts the dashboard
core/                 the generic bridge: web server, DCS-BIOS, keys, config, log, panel layout kit,
                      the HTML page (web/), the DCS export script (lua/), the layout checker (tools/)
aircraft/ah64d.py     everything specific to the AH-64D: views, controls, labels, default keybinds
config/               config.example.toml (config.toml and settings.json are local and ignored)
logs/                 rolling log, created at runtime (ignored)
docs/                 SPEC.md (the spec), FIXES.md (open points and fixes in progress)
```

Other aircraft may follow later: the bridge and the page engine are aircraft-independent, an aircraft is one file in `aircraft/` plus its drawings. See [docs/SPEC.md](docs/SPEC.md).

The first research scripts (read and control sweep) that proved what DCS allows are kept in git under the tag `research-v1`.
