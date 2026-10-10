# DCS-Dashboard

A simple tablet dashboard for the **AH-64D Apache** in DCS World. A small Python bridge connects to DCS via [DCS-BIOS](https://github.com/DCS-Skunkworks/dcs-bios) and serves an HTML page you open on an iPad or any tablet. Big touch buttons replace keyboard combinations for cockpit commands and George, the AI copilot.

**Status:** Stage 1 (read data) is built and tested on Windows. Results: [docs/STAGE1.md](docs/STAGE1.md#results). Stage 2 (control) is built and ready for its first test run.

## Plan

1. **Read** – test which data we can read from DCS (both seats, in flight). Details: [docs/STAGE1.md](docs/STAGE1.md)
2. **Control** – test which cockpit controls we can set from outside. Details: [docs/STAGE2.md](docs/STAGE2.md)
3. **Dashboard** – HTML page with preset views: Startup, Navigation, Fighting, George.

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

### 5. Config

Copy `config.example.toml` to `config.toml` in the repo folder and check `saved_games`. `config.toml` stays on your machine and is never committed.

### 6. Run Stage 1

1. In the repo folder run `python stage1_read.py`. If Windows asks to allow Python on the network, allow it for private networks.
2. Start DCS and an AH-64D mission. Changed values appear in the console.
3. Stop with Ctrl+C. The script prints a summary. The full log is in `logs\dcs-dashboard.log`.

The test procedure is in [docs/STAGE1.md](docs/STAGE1.md#test-run-windows-manual).

### 7. Run Stage 2

1. Add the `window_title` line and the `[keys]` section from `config.example.toml` to your `config.toml`.
2. Start DCS in windowed or borderless mode and an AH-64D mission, cold and dark, battery off.
3. In the repo folder run `python stage2_sweep.py` and press Enter when asked. Do not touch the controls for about 7 minutes.
4. Run `python stage2_sweep.py keys` and answer each key test with y, n or s.
5. Restart the mission, switch to the CP/G seat (key `2`) and repeat steps 3 and 4.

Results are in `logs\stage2_results.csv`. The test procedure is in [docs/STAGE2.md](docs/STAGE2.md#test-run-windows-manual).
