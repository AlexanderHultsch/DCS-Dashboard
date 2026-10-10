# Stage 1 – Read all data

Detailed spec for Stage 1 of [SPEC.md](SPEC.md). Goal: prove which values we can read live, for both seats and in flight.

## Scope

In:

- DCS-BIOS (AH-64D module): switches, lamps, EUFD and KU text, radios, standby instruments, current seat.
- Custom export script (Lua): position, attitude, speeds, radar altitude, vertical speed, G, engine and fuel values.
- Try only: MPD page text through `list_indication`, sent by the same export script.
- Rolling log, console output of changes, summary on exit.

Out (deferred):

- USB controls (stick, collective, pedals). Not needed to prove what DCS delivers; picked up later if the dashboard needs it.
- Sending commands (Stage 2), web server and dashboard (Stage 3).
- Automated tests. Everything is checked by the manual test run on Windows.

Only the Python standard library is used (Python 3.12+). No dependencies.

## Files

```
bridge/__init__.py            empty
bridge/config.py              load config.toml
bridge/log.py                 rolling log setup and one function to log a line
bridge/dcsbios.py             DCS-BIOS control list and stream decoding
bridge/export.py              decoding of the export script packets
lua/DCS-Dashboard-Export.lua  export script, runs inside DCS
stage1_read.py                test script: wires the above together
config.example.toml           gets the export port and the DCS-BIOS JSON path
README.md                     setup section for Stage 1
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

The DCS-BIOS control list is read from `<saved_games>/Scripts/DCS-BIOS/doc/json/AH-64D.json`. If the file is not there, the script stops and names the path it tried.

## Source 1 – DCS-BIOS

Receive: join the multicast group `export_multicast` on `export_port` (defaults `239.255.50.10:5010`).

Control list: from `AH-64D.json`. Every output of every control is one value. The value name is the output's name as in the JSON (control identifier, plus suffix if the output has one).

- Integer output: `address`, `mask`, `shift_by`, `max_value`.
- String output: `address`, `max_length`.

Stream format: each UDP packet starts with the sync bytes `55 55 55 55`, followed by blocks of `address` (uint16 LE), `length` (uint16 LE) and `length` bytes of data. The bridge keeps a 64 KB memory image, writes each block into it, and after every packet reads all outputs from the image and compares them with the last values.

- Integer value: `(word at address & mask) >> shift_by`.
- String value: `max_length` bytes from address, decoded as latin-1, trailing NUL bytes removed.
- Noise filter: outputs with `max_value` 65535 are analog gauges (needles). They count as changed only when they move by 655 or more (1 % of full scale). All other outputs count every change.

## Source 2 – Export script

`lua/DCS-Dashboard-Export.lua` is copied to `<saved_games>/Scripts/` and loaded by one line at the end of `<saved_games>/Scripts/Export.lua`:

```lua
dofile(lfs.writedir() .. [[Scripts\DCS-Dashboard-Export.lua]])
```

Rules for the script:

- Chains the existing export hooks (`LuaExportStart`, `LuaExportAfterNextFrame`, `LuaExportStop`), so DCS-BIOS keeps working.
- Uses LuaSocket the same way DCS-BIOS does and sends UDP to `127.0.0.1:PORT` (constant at the top of the file).
- Every 0.5 s of model time: one flight data packet. Every 1 s: one MPD text packet.
- Every call is wrapped in `pcall`, so a missing function does not break DCS. A failed value is simply left out.

Wire format: plain text, one value per line, `name=value`. The bridge splits each line at the first `=`. Numbers are formatted in Lua with fixed decimals, so the bridge compares plain strings and needs no noise filter.

Flight data packet:

| Name | Source | Unit | Format |
| --- | --- | --- | --- |
| `lat`, `lon` | `LoGetSelfData().LatLongAlt` | degrees | `%.5f` |
| `alt` | `LoGetSelfData().LatLongAlt.Alt` | ft MSL | `%.0f` |
| `hdg`, `pitch`, `bank` | `LoGetSelfData()` | degrees | `%.1f` |
| `ias`, `tas` | `LoGetIndicatedAirSpeed()`, `LoGetTrueAirSpeed()` | kt | `%.0f` |
| `ralt` | `LoGetAltitudeAboveGroundLevel()` | ft | `%.0f` |
| `vs` | `LoGetVerticalVelocity()` | ft/min | `%.0f` |
| `g` | `LoGetAccelerationUnits().y` | G | `%.2f` |
| `eng_rpm_l`, `eng_rpm_r` | `LoGetEngineInfo().RPM` | % | `%.1f` |
| `eng_temp_l`, `eng_temp_r` | `LoGetEngineInfo().Temperature` | °C | `%.0f` |
| `fuel_int`, `fuel_ext` | `LoGetEngineInfo().fuel_internal`, `.fuel_external` | as delivered | `%.3f` |
| `fuel_flow_l`, `fuel_flow_r` | `LoGetEngineInfo().FuelConsumption` | as delivered | `%.3f` |

Conversion: m to ft × 3.28084, m/s to kt × 1.94384, m/s to ft/min × 196.85, radians to degrees. Engine and fuel values are sent unconverted, because their units for the Apache are part of what Stage 1 finds out.

MPD text packet (try only): for each index 0 to 30, `list_indication(index)`. Non-empty results are sent as `ind<index>=<text>`, with newlines replaced by `\n`.

## Log and console

Log file `logs/dcs-dashboard.log` (folder created if missing), Python `RotatingFileHandler`, 5 MB per file, see Config.

One line per event or change:

```
2026-10-10 14:03:22.123 | dcsbios | PLT_MASTER_IGN_SW | 1
2026-10-10 14:03:22.140 | export  | ralt              | 3
2026-10-10 14:03:20.001 | bridge  | start             | DCS-BIOS 239.255.50.10:5010, export port 7790
```

- Sources: `bridge`, `dcsbios`, `export`.
- The first value of each name is logged as well, so the log starts with a full snapshot.
- Bridge events: start, first packet from each source, errors while decoding a packet (the packet is skipped), stop.
- The console prints the same lines with the time only (no date).

## stage1_read.py

- Single-threaded: two UDP sockets, one `select` loop with a 1 s timeout, so Ctrl+C works on Windows.
- Runs until Ctrl+C.
- On exit it prints the summary and writes it to the log:
  - Per source: number of values changed, constant (seen but never changed), and never seen.
  - The names of the constant and never-seen values, sorted.
  - For DCS-BIOS, "never seen" means its address was never in any received block.

## Test run (Windows, manual)

Preparation: DCS-BIOS installed, export script installed, `config.toml` set up, a single player mission with an AH-64D cold and dark on the ramp.

1. Start `python stage1_read.py`, then the mission. Check: a first packet line for both sources.
2. Pilot seat: flip a few switches, start the APU and both engines. At idle and at flight idle, note the engine page values from the MPD (NG, NP, TGT, torque, fuel) together with the time.
3. Switch to the CPG seat, flip a few switches there.
4. Short hover and a small circuit, land. Note the engine page values once in the hover.
5. Ctrl+C. Keep the log files and the console summary.

## Results

Filled in by hand after the test run. Result: readable, not readable or implausible.

| Value group | Source | Result | Notes |
| --- | --- | --- | --- |
| Switches, pilot seat | DCS-BIOS | | |
| Switches, CPG seat | DCS-BIOS | | |
| Lamps, master caution and warning | DCS-BIOS | | |
| EUFD text | DCS-BIOS | | |
| KU text | DCS-BIOS | | |
| Radio frequencies | DCS-BIOS | | |
| Standby instruments | DCS-BIOS | | |
| Current seat | DCS-BIOS | | Which output tracks the seat? |
| Position | export | | |
| Attitude | export | | |
| Speeds | export | | |
| Radar altitude, vertical speed, G | export | | |
| Engine values | export | | Compare with the noted MPD values |
| Fuel | export | | Compare with the noted MPD values |
| MPD page text | export | | Try only |

Stage 1 is done when the log covers both seats and the flight, and every row above has a result.

## Build steps

Each step is checked in the dev container by compiling the code, a short smoke run where possible, and reading the diff. The real check is the test run on Windows.

1. Config and log: `bridge/config.py`, `bridge/log.py`, config changes. Check: `python -m py_compile`, a small call that logs one line and shows it in `logs/dcs-dashboard.log`.
2. DCS-BIOS decoding: `bridge/dcsbios.py`. Check: compile, load a small hand-written control list and decode a hand-built packet in a one-off command.
3. Export decoding: `bridge/export.py`. Check: compile, decode a hand-written packet in a one-off command.
4. Test script: `stage1_read.py`. Check: start with no DCS running, send one packet per source from the command line, Ctrl+C, see the summary.
5. Export script: `lua/DCS-Dashboard-Export.lua`. Check: `luac -p` if available, otherwise diff review only. The real check is the Windows test run.
6. Docs: README setup section, SPEC.md points to this file. Check: read through.

## Open points to verify on the first run

- The exact path of `AH-64D.json` in the installed DCS-BIOS.
- Which DCS-BIOS output, if any, tells the current seat.
- The MPD indication indices for the Apache, if `list_indication` works at all.
