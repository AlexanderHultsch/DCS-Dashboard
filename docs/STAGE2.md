# Stage 2 – Check what is controllable

Detailed spec for Stage 2 of [SPEC.md](SPEC.md). Goal: a pass / fail list of every control we can set from outside, for both seats.

Status: tested on Windows.

## What Stage 1 tells us

- DCS-BIOS readback works for switches, buttons, levers and lamps in both seats, so most commands can be checked automatically.
- The AH-64D control list (`AH-64D.json`) has 562 controls with inputs: 273 pilot, 284 CP/G, 5 radio frequencies.
- George has no DCS-BIOS entry. Its menu is only reachable by keypresses.
- The default AH-64D keybinds are in the DCS install (`Mods/aircraft/AH-64D/Input/`). George defaults: `LCtrl+V` show / hide menu, `W` `S` `A` `D` up / down / left / right.

## Scope

In:

- Route 1, DCS-BIOS commands: every control of the current seat, swept automatically with readback.
- Route 2, keypresses to the DCS window: George commands and the keyboard combinations listed in `config.toml`, confirmed by the user.
- Answer the open question from [SPEC.md](SPEC.md): can a keypress reach DCS while it is the window in focus and the command comes from another program?

Out (deferred):

- Route 3, commands through the export script. Only built if keypresses prove unreliable.
- The radio frequency inputs (`set_string`): skipped, radios on the dashboard are still an open question.
- Controls of the other seat: the dashboard follows the current seat, so each seat is tested while sitting in it.
- Interfaces other than `set_state` (`fixed_step`, `variable_step`, `action`) for controls that have `set_state`. The dashboard sends absolute positions.
- Automated tests. Everything is checked by the test run on Windows.

Only the Python standard library is used. Keypresses use `ctypes` (Windows `SendInput`), which is part of the standard library.

## Files

```
bridge/dcsbios.py      + load all controls with inputs, send a command
bridge/keys.py         new: parse "LCtrl+V", bring the DCS window to front, send a keypress with scan codes
stage2_sweep.py        test script: DCS-BIOS sweep (default) and keypress test (argument "keys")
config.example.toml    + [keys] and the DCS window title
```

`bridge/config.py`, `bridge/log.py` and the Lua export script stay unchanged.

## Config

New keys in `config.example.toml`:

```toml
[dcs]
# Part of the DCS window title, used to bring DCS to the front before a keypress.
window_title = "Digital Combat Simulator"

[keys]
# DCS keybinds sent as keypresses. Modifiers and key joined by "+".
# Defaults from the DCS install; change them if you rebound them in DCS.
power_left_idle = "RAlt+Home"
power_right_idle = "RShift+Home"
power_left_up = "RAlt+PageUp"
power_right_up = "RShift+PageUp"
power_left_down = "RAlt+PageDown"
power_right_down = "RShift+PageDown"
power_left_off = "RAlt+End"
power_right_off = "RShift+End"
george_show_hide = "LCtrl+V"
george_up = "W"
george_down = "S"
george_left = "A"
george_right = "D"
```

For now the power lever keys and the George keys are tested. Keyboard combinations for cockpit commands without a DCS-BIOS entry can be added to `[keys]` later the same way. Supported: modifiers `LCtrl` `RCtrl` `LShift` `RShift` `LAlt` `RAlt` `LWin`; keys `A`–`Z`, `0`–`9`, `F1`–`F12`, `Home` `End` `PageUp` `PageDown` `Insert` `Delete`, arrow keys `Up` `Down` `Left` `Right`, `Space`, `Enter`.

## Route 1 – DCS-BIOS sweep

Command: one UDP line per command to `127.0.0.1:command_port` (default 7778), format `IDENTIFIER VALUE\n`, for example `PLT_MASTER_IGN_SW 1`.

Which controls:

- All controls of the current seat: identifier starts with `PLT_` when `SEAT_POSITION` is 0, `CPG_` when it is 1.
- Blocklist, never sent: every identifier that contains `JETT`, `FIRE_ENG`, `FIRE_APU`, `FIRE_PRIME`, `FIRE_RES`, `ZERO`, `CHOP`, `BUCS` or `TRIGGER`. That covers the jettison controls, fire buttons and extinguishers, zeroize switches, CHOP, BUCS, the weapons trigger and the M4 trigger, with their covers. 29 pilot and 27 CP/G controls, reported as `skipped`.

Positions per control, with `max_value` from the `set_state` input:

- `max_value` up to 20 (switches, buttons, selectors): every position 0 … `max_value`.
- Larger `max_value` (dials and levers, 0–65535): 0, half, `max_value`.
- No `set_state` input (3 controls): `action` sends `TOGGLE` twice, `variable_step` sends `+step` then `-step`; pass if the readback changes and comes back.

For each control:

1. Read the current position from the DCS-BIOS stream.
2. For each test position: send it, then wait up to 0.5 s until the readback equals it. Dials: within 1 % of `max_value`.
3. Send the original position again and check it the same way.
4. Result:
   - `pass`: every position and the restore were read back.
   - `fail`: at least one position was not read back. The note lists the failed positions.
   - `sent-unverified`: the control has no integer output (4 pilot power lever IDLE / LIFT controls).
   - `skipped`: blocklisted.

Before the sweep starts the script waits until every output of the seat has been seen at least once (Stage 1: the first full update takes about 15 s), prints the seat, the number of controls and the expected time, and waits for Enter. Expected time: about 7 minutes per seat.

Ctrl+C stops the sweep: the control in progress is set back to its original position and the results so far are written.

Expected side effects: the battery switch, the APU button and the power levers are moved for under a second each. In a cold and dark cockpit with the battery off this has no lasting effect. MPD and KU buttons are pressed, so MPD pages and the KU scratchpad may change. Restart the mission after the sweep.

Guarded controls (switch under a cover) may fail while their cover is closed. Such failures are checked in the review, not handled in code.

## Route 2 – Keypresses

DCS reads the keyboard through scan codes, so keys are sent with `SendInput` and `KEYEVENTF_SCANCODE`, not as characters.

For each entry in `[keys]`:

1. The console shows the name and the key, and waits for Enter.
2. The script taps LShift, brings the first visible window whose title contains `window_title` to the front and waits 0.3 s. The tap is needed because Windows only lets a background program change the active window right after it sent input; LAlt would put the window into menu mode and swallow the next key. If the window does not come to the front, no key is sent and the result is `fail` with note `no focus`.
3. It presses the modifiers, presses the key, holds it, releases everything in reverse order.
4. The user looks at DCS, clicks back into the console and answers `y` (worked), `n` (did not work) or `s` (skip).

George hat directions are sent twice: a short press (0.1 s) and a long press (1 s), because George treats them differently. `george_show_hide` is sent once. Every other entry, such as the power lever keys, is sent once. That makes 17 tests per seat with the default config.

The log records whether bringing DCS to the front worked. That answers the focus question for the tablet: in Stage 3 the keypress comes from the bridge while the user flies with DCS in front.

DCS should run in windowed or borderless mode for this part, with the console visible next to it.

## Results file and log

`logs/stage2_results.csv`, appended per run, one line per control or key:

```
control,seat,route,result,note
PLT_MASTER_IGN_SW,PLT,dcsbios,pass,
PLT_APU_BTN,PLT,dcsbios,fail,1
george_up short,PLT,keys,pass,
```

The rolling log `logs/dcs-dashboard.log` (Stage 1 setup) gets every command sent, every readback and the result, with source `stage2`:

```
2026-10-11 10:00:01.120 | stage2  | PLT_MASTER_IGN_SW    | sent 1
2026-10-11 10:00:01.180 | stage2  | PLT_MASTER_IGN_SW    | read 1
2026-10-11 10:00:01.420 | stage2  | PLT_MASTER_IGN_SW    | pass
```

The console prints one line per control (result and note) and a progress counter. At the end: counts per result.

## stage2_sweep.py

- `python stage2_sweep.py`: DCS-BIOS sweep of the current seat.
- `python stage2_sweep.py <text>`: sweep only the controls of the current seat whose identifier contains `<text>`, for quick checks.
- `python stage2_sweep.py keys`: keypress test.
- Single-threaded like Stage 1: the DCS-BIOS socket is read in the wait loops, no extra threads.
- Reuses `bridge.config`, `bridge.log` and the DCS-BIOS decoding from `bridge.dcsbios`.

## Test run (Windows, manual)

Preparation: Stage 1 setup. DCS in windowed or borderless mode. Single player mission, AH-64D cold and dark, battery off.

1. Pilot seat. Start `python stage2_sweep.py`, press Enter when asked, do not touch the controls for about 2 minutes.
2. Turn the battery on (George needs power), start `python stage2_sweep.py keys` and go through the key list.
3. Restart the mission, switch to the CP/G seat (key `2`), repeat steps 1 and 2.
4. Keep `logs/stage2_results.csv` and the log files.

## Results

From the test run on Windows, cold and dark: one sweep per seat (about 1.5 minutes each), the George keys with battery power, and a few manual follow-ups.

| Seat | pass | fail | skipped (blocklist) | sent-unverified |
| --- | --- | --- | --- | --- |
| Pilot | 227 | 12 | 29 | 5 |
| CP/G | 238 | 18 | 27 | 1 |

Keypresses: George 9 / 9 pass in both seats, power levers 8 / 8 pass in the pilot seat. Bringing DCS to the front worked every time, so the bridge can send keys while DCS is in front. George needs electrical power; with the battery off it answers "no power".

Reviewed failures:

- Cockpit logic or missing preconditions: master ignition EXT PWR (no external power), APU button (passes with the cover open, fails with it closed), NVS mode position 2, rotor brake BRK.
- Passed with a 3 s wait instead of 0.5 s: ICS mode, M4 safety.
- Spring-loaded, always back to centre: CP/G manual tracker (2).
- Not reached, also not with a 3 s wait: canopy (both seats), CP/G stick fold, MPD mode knobs (both seats), processor select, TADS select, SAI cage, SAI pitch trim, CP/G left MPD L1–L6. Probably missing preconditions. Not followed up, the dashboard does not need them.
- Power levers: not controllable by DCS-BIOS (it does not move them past the OFF detent), and the keys for both levers together (PageUp / PageDown) do not work. Controllable by keypress, one key per lever: RAlt (left) or RShift (right) with Home = IDLE, PageUp = one step up, PageDown = one step down, End = OFF. All 8 passed, and DCS-BIOS read back 0 OFF, 16383 IDLE, 58981 FLY after each key.

Everything the Fighting and Navigation views need passed: master arm, ground override, weapons action switch, sight select, flare, chaff, force trim, KU keys and MPD buttons (except CP/G left MPD L1–L6). For the Startup view, master ignition, APU cover, engine start switches and parking brake passed; the APU button works once the cover is open; the power levers work by keypress.

Conclusion: a single command works for most controls, but some only work after other steps (cover open, power on, finger lift). Stage 3 uses only controls that passed, in the order a pilot would use them.

Stage 2 is done when every control of both seats has a result and the failures are reviewed.

## Build steps

Each step is checked by compiling the code and reading the diff. The real check is the test run on Windows.

1. `bridge/dcsbios.py`: load all controls with inputs, send a command. Check: compile, list the controls of each seat with their test positions, count blocklisted controls.
2. `stage2_sweep.py` route 1. Check: start with DCS running in a cold cockpit, sweep a handful of controls (for example a filter on the command line), read the CSV.
3. `bridge/keys.py` and route 2. Check: send one key to Notepad as the target window, then one George command in DCS.
4. Config and docs: `config.example.toml`, README, SPEC.md points to this file.

## Open points

- Does a DCS-BIOS command reach the controls of the other seat? Not tested, the dashboard follows the current seat.
- Do the George W / S / A / D keys only act while the George menu is shown, or also as other DCS commands? Watch during the keypress test.
- Keyboard combinations for cockpit commands: the power levers and George for now. A later combination goes into `[keys]` and becomes a dashboard button.
