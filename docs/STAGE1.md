# Stage 1 – Read all data

Detailed spec for Stage 1 of [SPEC.md](SPEC.md). Goal: prove which values we can read live, for both seats and in flight.

## Scope

In:

- DCS-BIOS (AH-64D module): the values listed under [Values we log](#values-we-log).
- Custom export script (Lua): position, attitude, speeds, radar altitude, vertical speed, G, engine and fuel values.
- Try only: MPD page text through `list_indication`, sent by the same export script.
- Rolling log, console output of changes, summary on exit.

Out (deferred):

- USB controls (stick, collective, pedals). Not needed to prove what DCS delivers; picked up later if the dashboard needs it.
- Sending commands (Stage 2), web server and dashboard (Stage 3).
- Automated tests. Everything is checked by the manual test run on Windows.

Use: a debugging tool for short sessions of up to about 10 minutes, not for logging full sessions.

Only the Python standard library is used (Python 3.12+). No dependencies.

## Files

```
bridge/__init__.py            empty
bridge/config.py              load config.toml
bridge/log.py                 rolling log setup and one function to log a line
bridge/dcsbios.py             DCS-BIOS control list and stream decoding
bridge/export.py              decoding of the export script packets
lua/DCS-Dashboard-Export.lua  export script, runs inside DCS
stage1_read.py                test script: the list of DCS-BIOS values, wires the above together
config.example.toml           gets the export port
README.md                     install and getting started
```

The modules in `bridge/` are reused by Stages 2 and 3. They hold plain functions, no classes unless one is clearly simpler.

## Config

`config.toml` (copied from `config.example.toml`) is read with `tomllib`. Environment variables like `%USERPROFILE%` are expanded. If the file is missing, the script stops with a short message telling the user to copy `config.example.toml`.

New keys:

```toml
[export]
# UDP port the export script sends to. Must match PORT in lua/DCS-Dashboard-Export.lua.
port = 7790
```

Changed key: `[log] backups = 2`, so the active file plus 2 backups = 3 files of 5 MB, about 15 MB in total.

The DCS-BIOS control list is read from `<saved_games>/Scripts/DCS-BIOS/doc/json/AH-64D.json`, which comes with the DCS-BIOS zip. If the file is not there, the script stops and names the path it tried.

## Values we log

Every change of every value below is logged. No filter, no rounding in the bridge. The summary on exit says for each value whether it changed, stayed constant, or was never seen, so you always know if something was set or not.

Values not in this list are ignored. Adding a value later means adding its name to the list.

### DCS-BIOS

Names are the DCS-BIOS identifiers of the AH-64D module ([DCS-Skunkworks](https://github.com/DCS-Skunkworks/dcs-bios), `AH-64D.lua`). `PLT_` = pilot, `CPG_` = CP/G. Where both seats have the control, both are logged.

| Group | Names | Values |
| --- | --- | --- |
| Seat | `SEAT_POSITION` | 0 pilot, 1 CP/G |
| Master caution and warning | `PLT_/CPG_MASTER_CAUTION_L`, `PLT_/CPG_MASTER_WARNING_L` | lamp 0/1 |
| Engine and APU lamps | `PLT_/CPG_ENG_1_READY_L`, `PLT_/CPG_ENG_2_READY_L`, `PLT_/CPG_APU_READY_L`, `PLT_/CPG_ENG_1_FIRE_L`, `PLT_/CPG_ENG_2_FIRE_L`, `PLT_/CPG_APU_FIRE_L`, `PLT_APU_L` | lamp 0/1 |
| Startup switches | `PLT_MASTER_IGN_SW`, `PLT_APU_BTN_CVR`, `PLT_APU_BTN`, `PLT_ENG1_START`, `PLT_ENG2_START`, `PLT_ROTOR_BRK`, `PLT_PARK_BRAKE` | switch position |
| Power levers | `PLT_/CPG_ENG_L_PW_LVR`, `PLT_/CPG_ENG_R_PW_LVR` | 0–65535 |
| Armament | `PLT_/CPG_MASTER_ARM_BTN`, `PLT_/CPG_GROUND_OVERRIDE_BTN`, `PLT_/CPG_MASTER_ARM_ARM_L`, `PLT_/CPG_MASTER_ARM_SAFE_L`, `PLT_/CPG_GROUND_OVERRIDE_L` | button / lamp 0/1 |
| Weapons action switch | `PLT_/CPG_CYCLIC_WEAPON_UD`, `PLT_/CPG_CYCLIC_WEAPON_LR`, `CPG_LHG_WPN_UP_DN`, `CPG_LHG_WPN_L_R` | switch position |
| Sight select | `PLT_/CPG_COLLECTIVE_SIGHT_SELECT_UD`, `PLT_/CPG_COLLECTIVE_SIGHT_SELECT_LR` | switch position |
| Flare and chaff | `PLT_/CPG_CYCLIC_FLARE`, `PLT_/CPG_CYCLIC_CHAFF`, `PLT_CMWS_FLARE_COUNT`, `PLT_CMWS_CHAFF_COUNT` | button 0/1, count text |
| Force trim / hold | `PLT_/CPG_CYCLIC_TRIM_UD`, `PLT_/CPG_CYCLIC_TRIM_LR` | switch position |
| KU scratchpad | `PLT_KU_DISPLAY`, `CPG_KU_DISPLAY` | text |
| EUFD | `PLT_EUFD_LINE1` … `PLT_EUFD_LINE14`, `CPG_EUFD_LINE1` … `CPG_EUFD_LINE14` | text |
| Radios | `UHF_RADIO`, `VHF_AM_RADIO`, `FM1_RADIO`, `FM2_RADIO`, `HF_RADIO` | frequency text |
| Standby instruments | `PLT_IAS_NEEDLE`, `PLT_ALT_NEEDLE` | 0–65535 |

`PLT_/CPG_X` stands for both `PLT_X` and `CPG_X`. In code the list is written out in full, about 100 names.

### Export script

| Name | Source | Unit | Format |
| --- | --- | --- | --- |
| `lat`, `lon` | `LoGetSelfData().LatLongAlt` | degrees | `%.5f` |
| `alt` | `LoGetSelfData().LatLongAlt.Alt` | ft MSL | `%.0f` |
| `hdg`, `pitch`, `bank` | `LoGetSelfData()` | degrees | `%.1f` |
| `ias`, `tas` | `LoGetIndicatedAirSpeed()`, `LoGetTrueAirSpeed()` | kt | `%.0f` |
| `ralt` | `LoGetAltitudeAboveGroundLevel()` | ft | `%.0f` |
| `vs` | `LoGetVerticalVelocity()` | ft/min | `%.0f` |
| `g` | `LoGetAccelerationUnits().y` | G | `%.2f` |
| `eng_rpm_l`, `eng_rpm_r` | `LoGetEngineInfo().RPM` | as delivered | `%.1f` |
| `eng_temp_l`, `eng_temp_r` | `LoGetEngineInfo().Temperature` | as delivered | `%.0f` |
| `fuel_int`, `fuel_ext` | `LoGetEngineInfo().fuel_internal`, `.fuel_external` | as delivered | `%.3f` |
| `fuel_flow_l`, `fuel_flow_r` | `LoGetEngineInfo().FuelConsumption` | as delivered | `%.3f` |
| `plt_cyc_pitch`, `plt_cyc_roll`, `plt_coll`, `plt_pedals`, `cpg_cyc_pitch`, `cpg_cyc_roll`, `cpg_coll`, `cpg_pedals` | `GetDevice(0):get_argument_value(470/471/474/476, CP/G 472/473/475/478)` | as delivered | `%.3f` |
| `ind0` … `ind30` | `list_indication(n)`, try only | text | newlines as `\n` |

Conversion in Lua: m to ft × 3.28084, m/s to kt × 1.94384, m/s to ft/min × 196.85, radians to degrees. Engine and fuel values are sent unconverted, because their units for the Apache are part of what Stage 1 finds out. Only non-empty `ind<n>` values are sent.

### Log size

At about 270 lines per second in flight (export values at 10 Hz plus DCS-BIOS needles and lamps), a 10 minute session writes roughly 9 MB, inside the 15 MB limit. Longer sessions roll over and drop the oldest lines.

## Source 1 – DCS-BIOS

Receive: join the multicast group `export_multicast` on `export_port` (defaults `239.255.50.10:5010`).

Control list: from `AH-64D.json`. For each name in the list above, the bridge looks up its output:

- Integer output: `address`, `mask`, `shift_by`.
- String output: `address`, `max_length`.

A listed name that is not in the JSON is logged once as a bridge event at start and reported in the summary as "not in DCS-BIOS".

Stream format: each UDP packet starts with the sync bytes `55 55 55 55`, followed by blocks of `address` (uint16 LE), `length` (uint16 LE) and `length` bytes of data. The bridge keeps a 64 KB memory image, writes each block into it, and after every packet reads the listed outputs from the image and compares them with the last values.

- Integer value: `(word at address & mask) >> shift_by`.
- String value: `max_length` bytes from address, decoded as latin-1, trailing NUL bytes removed.

## Source 2 – Export script

`lua/DCS-Dashboard-Export.lua` is copied to `<saved_games>/Scripts/` and loaded by one line at the end of `<saved_games>/Scripts/Export.lua`, after the DCS-BIOS line:

```lua
dofile(lfs.writedir() .. [[Scripts\DCS-Dashboard-Export.lua]])
```

Rules for the script:

- Chains the existing export hooks (`LuaExportStart`, `LuaExportAfterNextFrame`, `LuaExportStop`), so DCS-BIOS keeps working.
- Uses LuaSocket the same way DCS-BIOS does and sends UDP to `127.0.0.1:PORT` (constant at the top of the file).
- Every 0.1 s of model time (10 Hz): one flight data packet. Every 1 s: one packet per non-empty MPD indication.
- Every call is wrapped in `pcall`, so a missing function does not break DCS. A failed value is simply left out.

Wire format: plain text, one value per line, `name=value`. The bridge splits each line at the first `=`. Numbers are formatted in Lua with fixed decimals (see the table above), so the bridge compares plain strings.

## Log and console

Log file `logs/dcs-dashboard.log` (folder created if missing), Python `RotatingFileHandler`, 5 MB per file, see Config.

One line per event or change:

```
2026-10-10 14:03:20.001 | bridge  | start             | DCS-BIOS 239.255.50.10:5010, export port 7790
2026-10-10 14:03:22.123 | dcsbios | PLT_MASTER_IGN_SW | 1
2026-10-10 14:03:22.140 | export  | ralt              | 3
```

- Sources: `bridge`, `dcsbios`, `export`.
- The first value of each name is logged as well, so the log starts with a full snapshot.
- Bridge events: start, first packet from each source, unknown names, errors while decoding a packet (the packet is skipped), stop.
- The console prints the same lines with the time only (no date).

## stage1_read.py

- Holds the list of DCS-BIOS names from [Values we log](#values-we-log).
- Single-threaded: two UDP sockets, one `select` loop with a 1 s timeout, so Ctrl+C works on Windows.
- Runs until Ctrl+C.
- On exit it prints the summary and writes it to the log:
  - Per source: number of values changed, constant (seen but never changed), never seen, and (DCS-BIOS only) not in DCS-BIOS.
  - The names in each group except "changed", sorted.
  - For DCS-BIOS, "never seen" means the value's address was never in any received block.
  - For the export script, "never seen" covers the names in the table above; `ind<n>` values only count when seen.

## Test run (Windows, manual)

Preparation: see "Getting started" in the README. A single player mission with an AH-64D cold and dark on the ramp.

1. Start `python stage1_read.py`, then the mission. Check: a first packet line for both sources.
2. Pilot seat: flip a few switches, start the APU and both engines. At idle and at flight idle, note the engine page values from the MPD (NG, NP, TGT, torque, fuel) together with the time.
3. Switch to the CPG seat, flip a few switches there.
4. Short hover and a small circuit, land. Note the engine page values once in the hover.
5. Ctrl+C. Keep the log files and the console summary.

Keep the session under about 10 minutes.

## Results

From the test runs on Windows: a short flight with the engines already running, and a cold start with auto start, both seats and a short hover. Result: readable, partly readable, not readable, implausible or not tested.

| Value group | Source | Result | Notes |
| --- | --- | --- | --- |
| Seat | DCS-BIOS | readable | 0 pilot, 1 CP/G; follows seat changes |
| Master caution and warning | DCS-BIOS | readable | Warning blinks with LOW ROTOR RPM; caution seen in the lamp test |
| Engine and APU lamps | DCS-BIOS | readable | Lamp test at power-on, fire test, APU ON while the APU runs |
| Startup switches | DCS-BIOS | readable | APU cover and button, master ignition, ENG 1/2 START (2 = START), rotor brake, parking brake |
| Power levers | DCS-BIOS | readable | 0 OFF, 16383 IDLE, 58981 FLY; PLT and CPG values identical |
| Armament | DCS-BIOS | readable | Master arm and ground override buttons and lamps, both seats |
| Weapons action switch | DCS-BIOS | not tested | HOTAS only, no default key |
| Sight select | DCS-BIOS | not tested | HOTAS only, no default key |
| Flare and chaff | DCS-BIOS | partly readable | Counts readable (60 / 30) when CMWS is on, empty after auto start; buttons not tested |
| Force trim / hold | DCS-BIOS | readable | Pilot only; CP/G not tested |
| KU scratchpad | DCS-BIOS | readable | Text and cursor `#` |
| EUFD | DCS-BIOS | readable | Both seats: radios, fuel in lb, transponder, Zulu time, warnings and advisories |
| Radios | DCS-BIOS | implausible | HF stuck at `134.00` after a cold start (EUFD: `2.0000`); VHF shows +0.001. Use EUFD lines 8–12 |
| Standby instruments | DCS-BIOS | readable | Raw 0–65535; scale not mapped |
| Position | export | readable | |
| Attitude | export | readable | |
| Speeds | export | partly readable | TAS plausible. IAS shows 8–17 kt standing still and is about 10 kt above TAS in slow flight |
| Radar altitude, vertical speed, G | export | readable | 5 ft on the ground |
| Engine values | export | partly readable | `eng_rpm` = NG %, matches the MPD within 0.1. `eng_temp` always 0. No TGT, torque, NP or NR in the export |
| Fuel | export | readable | `fuel_int` = fraction of full internal fuel (× ≈2510 lb = EUFD fuel). `fuel_ext` 0 (no external tanks). `fuel_flow` plausible, probably kg/s per engine, unit not confirmed |
| MPD page text | export | readable | `list_indication` works and gives named text fields. Only the displays of the occupied seat update |

Stage 1 is done when the log covers both seats and the flight, and every row above has a result.

## Build steps

Each step is checked in the dev container by compiling the code, a short smoke run where possible, and reading the diff. The real check is the test run on Windows.

1. Config and log: `bridge/config.py`, `bridge/log.py`, config changes. Check: `python -m py_compile`, a small call that logs one line and shows it in `logs/dcs-dashboard.log`.
2. DCS-BIOS decoding: `bridge/dcsbios.py`. Check: compile, load a small hand-written control list and decode a hand-built packet in a one-off command.
3. Export decoding: `bridge/export.py`. Check: compile, decode a hand-written packet in a one-off command.
4. Test script: `stage1_read.py`. Check: start with no DCS running, send one packet per source from the command line, Ctrl+C, see the summary.
5. Export script: `lua/DCS-Dashboard-Export.lua`. Check: `luac -p` if available, otherwise diff review only. The real check is the Windows test run.
6. Docs: README getting started matches the built files, SPEC.md points to this file. Check: read through.

## Open points from the test runs

- MPD index map as observed: `ind7` / `ind9` pilot MPD left / right, `ind11` / `ind13` CP/G MPD left / right, `ind15` CP/G KU, `ind18` / `ind19` EUFD pilot / CP/G, `ind20` CP/G helmet display, `ind22` pilot helmet display. Fields are named by position (`LABEL n`) and their meaning depends on the page, so each page needs its own parsing.
- TGT, torque, NP and NR only come from the MPD ENG page, and only while that page is shown in the occupied seat.
- `fuel_flow` unit not confirmed (the FUEL page was not opened).
- IAS is implausible at low speed.
- Radios: use the EUFD lines instead of the DCS-BIOS radio strings.
- DCS-BIOS strings arrive in pieces for the first ~15 s, sometimes with NUL bytes inside. The first DCS-BIOS packet of every run is skipped with `truncated block data`, which is harmless.
- Log size is about 1 MB per minute, 93 % of it MPD text (`ind18` / `ind19` alone about 60 %). A 10 minute session fits the 15 MB limit, but only just. Sending MPD text less often, or leaving out `ind18` / `ind19`, would reduce it.
- Not explained: in the first run all DCS-BIOS strings went blank at one moment while the engines kept running. It did not happen again in the cold start.
- Not tested: weapons action switch, sight select, flare and chaff buttons, CP/G force trim (all HOTAS only).
