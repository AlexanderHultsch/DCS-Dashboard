# DCS-Dashboard – Spec

The specification of the product as built. Open points and the fix log are in [FIXES.md](FIXES.md).

## 1. Purpose and principles

A self-made helper dashboard on a tablet (iPad) for the AH-64D in DCS World. It replaces keyboard combinations and mouse clicks for cockpit commands and shows the cockpit state: a COCKPIT map with one page per cockpit panel, quick pages for flight and fight, both MPDs, the TEDAC and the KU. Flying itself stays on stick, collective and pedals. It is an open-source hobby project.

Principles:

- Keep it simple: the smallest code that works, few dependencies (Python standard library only), no extra layers.
- Not every edge case is handled: a crash or a lost packet is fine, a restart fixes it.
- One interface: the Python bridge is the only way the dashboard talks to DCS.
- Debuggable: a size-limited rolling log makes problems traceable from the log files alone.

Public repo rules:

- No personal data in code, docs, logs or commits: no names, emails, IP addresses, user paths or machine names.
- Everything machine-specific (DCS Saved Games folder, ports, keybind overrides) lives in the optional local `config/config.toml`; the repo ships only `config/config.example.toml`.
- Logs and local config (`logs/`, `config/config.toml`, `config/settings.json`) are in `.gitignore` and never committed.
- Commits use the GitHub no-reply address.

### Fixed decisions

| Topic | Decision |
| --- | --- |
| Aircraft | AH-64D only, pilot and CP/G seat. Aircraft data is a file in `aircraft/`, see [section 8](#8-the-bridge-interface) |
| Game mode | Single player only |
| Platform | DCS World on Windows (Steam or standalone), Python 3.12 or newer; tablet and PC share the local network |
| Language | Python for the bridge; plain HTML, CSS and JavaScript for the dashboard (no framework, no external files); Lua only for the small DCS-side export script |
| Code | Public GitHub repo `DCS-Dashboard`, only the main branch; usable by anyone |
| Dashboard | One HTML page served by the bridge, used in a tablet browser over the local network, no login |
| Debug log | Rolling log file with a size limit: 5 MB per file, the last 3 files kept, about 15 MB in total |
| AI | Not part of the product; see [section 10](#10-future-development-and-out-of-scope) |

## 2. Repository layout and architecture

```
start_dashboard.bat        starts `python core\dashboard.py`, keeps the window open on an error
README.md                  install and getting started
core/                      generic infrastructure
  dashboard.py             entry point: DCS-BIOS reader, web server, command handling
  config.py                loads the optional config, defaults, Saved Games detection
  dcsbios.py               DCS-BIOS control list, stream decoding, commands
  export.py                decoding of the export script packets
  keys.py                  keypresses (SendInput, scan codes), bringing the DCS window to the front
  log.py                   rolling log
  panel_kit.py             layout compiler of the panel pages
  web/                     index.html (the page: HTML, CSS and JavaScript in one file), apple-touch-icon.png
  lua/                     DCS-Dashboard-Export.lua (DCS-side export script)
  tools/                   check_panels.js (layout checker, run in the browser console)
aircraft/ah64d.py          all AH-64D data: views, controls, labels, MPD indications, trim data, default keybinds
config/                    config.example.toml (tracked); config.toml (optional, ignored: machine settings and
                           keybind overrides); settings.json (ignored: logging switch)
logs/                      generated at runtime (ignored)
docs/                      SPEC.md (this spec) and FIXES.md (a temporary working note)
```

```
DCS World · AH-64D (gaming PC)
 ├─ DCS-BIOS (Lua) ............ switches, lamps, display text; accepts commands
 └─ Export script (Lua) ....... control positions, MPD text (core/lua/DCS-Dashboard-Export.lua)
        │ UDP multicast (DCS-BIOS stream), UDP (export script)     ▲ DCS-BIOS commands (UDP), keypresses
        ▼                                                          │
Python bridge (core/dashboard.py) · the only interface
 ├─ State store ......... current values from both sources
 ├─ Command sender ...... DCS-BIOS commands, keypresses
 ├─ Web server .......... serves the page, the layout, the state; takes commands
 └─ Rolling log ......... commands, refusals, errors (size-limited files in logs/)
        ▲▼ HTTP (GET /state at 5 Hz, POST /command)
Tablet dashboard (HTML page, follows the current seat)
```

- **Polling, not WebSocket.** The page asks for `/state` five times per second. That is plenty for switches and lamps on the local network and keeps the bridge to the Python standard library (`http.server`).
- **Threads.** One background thread reads the DCS-BIOS stream into the current values; the web server (`ThreadingHTTPServer`) answers each request in its own thread; further threads read the export script packets, watch the trim reset key and close the real DCS covers. A lock protects the values, a second lock makes sure only one command (or key sequence) is sent at a time.
- **The view is data.** The controls of each view are one Python list in `aircraft/ah64d.py`, served as `/layout`. The page draws whatever the lists contain. The panel pages of the COCKPIT tab are written by the panel kit (`core/panel_kit.py`, [section 7](#7-the-panel-kit)): the aircraft file names a part and its centre, the kit gives it its standard size, places the labels, adds the plate and screws, and writes the page data.
- **The tablet shows the cockpit, not the last tap.** Every control shows the position read back from DCS. A switch moved in the cockpit with the mouse moves on the tablet too.
- **Local network only, no login.** The server listens on `[dashboard] host` and `port` (default `0.0.0.0:8080`). On start it prints the address to open, for example `http://<PC address>:8080`.

## 3. Configuration

`config/config.toml` is optional. Without it the dashboard runs with the built-in defaults (`DEFAULTS` in `core/config.py`). To change something, copy `config/config.example.toml` to `config/config.toml` and keep only the lines to change; sections are merged key by key over the defaults. Environment variables like `%USERPROFILE%` are expanded in `saved_games`.

| Section / key | Default | Meaning |
| --- | --- | --- |
| `[dcs] saved_games` | `"auto"` | DCS Saved Games folder. `auto` asks Windows for the Saved Games folder and uses `DCS` or `DCS.openbeta`, whichever has DCS-BIOS installed (`Scripts/DCS-BIOS`). If none is found the bridge stops and asks for the setting |
| `[dcs] window_title` | `"Digital Combat Simulator"` | Part of the DCS window title; the bridge brings that window to the front before a keypress |
| `[dcs] aircraft` | `"AH-64D"` | Aircraft profile: the file in `aircraft/` (lower case, only letters and digits, so `AH-64D` loads `aircraft/ah64d.py`) |
| `[dcs_bios] export_multicast`, `export_port` | `239.255.50.10`, `5010` | DCS-BIOS stream (UDP multicast) |
| `[dcs_bios] command_port` | `7778` | DCS-BIOS commands (UDP to 127.0.0.1) |
| `[export] port` | `7790` | UDP port the export script sends to; must match `PORT` in `core/lua/DCS-Dashboard-Export.lua` |
| `[dashboard] host`, `port` | `0.0.0.0`, `8080` | Web server for the tablet |
| `[log] file`, `max_mb`, `backups` | `logs/dcs-dashboard.log`, 5, 2 | Rolling log: the active file plus 2 backups of 5 MB, about 15 MB in total |
| `[keys]` | from the aircraft file | Overrides of the default keybinds, per key |

- **Keybinds.** The default DCS keybinds sent as keypresses are in `KEYS` in `aircraft/ah64d.py`. A `[keys]` line in `config/config.toml` overrides one key; the others stay. Format: modifiers and key joined by `+`. Supported modifiers: `LCtrl` `RCtrl` `LShift` `RShift` `LAlt` `RAlt` `LWin`; keys `A`–`Z`, `0`–`9`, `F1`–`F12`, `Home` `End` `PageUp` `PageDown` `Insert` `Delete`, `Up` `Down` `Left` `Right`, `Space`, `Enter`. The bridge checks all keys it needs at start and stops with a message if one is missing or invalid.

  | Key | Default | DCS command |
  | --- | --- | --- |
  | `power_left_idle`, `_up`, `_down`, `_off` | `RAlt+Home`, `RAlt+PageUp`, `RAlt+PageDown`, `RAlt+End` | power lever 1 |
  | `power_right_idle`, `_up`, `_down`, `_off` | `RShift+Home`, `RShift+PageUp`, `RShift+PageDown`, `RShift+End` | power lever 2 |
  | `canopy` | `LCtrl+C` | Open/Close Cockpit Door |
  | `monocle` | `I` | IHADSS show |
  | `controls_overlay` | `RCtrl+Enter` | Show controls indicator |
  | `trim_reset` | `LCtrl+T` | Trimmer reset |

- **settings.json.** `config/settings.json` (ignored) holds the LOGGING switch of the settings page ([section 5](#5-dashboard-design-rules-seat-handling-settings)). It is created by the bridge, not edited by hand.
- **DCS side.** DCS-BIOS (DCS-Skunkworks fork) with its AH-64D module is installed in Saved Games; the control list is read from `<Saved Games>/Scripts/DCS-BIOS/doc/json/AH-64D.json`. If the file is missing the bridge stops and names the path. The export script `core/lua/DCS-Dashboard-Export.lua` is copied to `<Saved Games>/Scripts/` and loaded by one line at the end of `Export.lua`, after the DCS-BIOS line: `dofile(lfs.writedir() .. [[Scripts\DCS-Dashboard-Export.lua]])`. The default keybinds must be bound in the DCS controls settings (the standard AH-64D bindings). DCS should run in windowed or borderless mode so that bringing it to the front works. Windows may ask to allow Python on the network: allow it for private networks.

## 4. What DCS allows

The result of the research phase, on Windows with the AH-64D, both seats, cold and dark and in flight. The original research scripts and their full result tables are kept in git under the tag `research-v1`.

### Reading

- **DCS-BIOS** (multicast stream) delivers switch positions, button states, lamps, levers and text for both seats: master caution and warning, engine and APU lamps (including lamp test and fire test), startup switches, power lever positions, armament buttons and lamps, weapons action and sight select hats, flare and chaff buttons, force trim, KU scratchpad, the 14 EUFD lines, the CMWS counts, the current seat (`SEAT_POSITION`: 0 pilot, 1 CP/G). The `AH-64D.json` control list has 562 controls with inputs (273 pilot, 284 CP/G, 5 radio frequencies).
- DCS-BIOS stream format: each UDP packet starts with the sync bytes `55 55 55 55`, followed by blocks of address (uint16 LE), length (uint16 LE) and data. The bridge keeps a 64 KB memory image and reads the outputs it needs from it: integers as `(word at address & mask) >> shift_by`, strings as `max_length` bytes decoded as latin-1 with trailing NUL bytes removed. Strings arrive in pieces for the first 15 seconds or so.
- **Export script** (Lua, runs inside DCS next to DCS-BIOS, sends UDP to `127.0.0.1`; every call is wrapped in `pcall`, and it chains the existing export hooks so DCS-BIOS keeps working). It sends plain text, one `name=value` per line:
  - the actual control positions at 10 Hz as cockpit arguments: pilot cyclic pitch 470, roll 471, collective 474, pedals 476; CP/G 472, 473, 475, 478 (`plt_cyc_pitch`, `plt_cyc_roll`, `plt_coll`, `plt_pedals`, `cpg_…`);
  - the MPD page text: `list_indication` works for the Apache and gives named text fields (`PB<n>` and others). Only the displays of the occupied seat update. Index map: 7 and 9 pilot MPD left and right, 11 and 13 CP/G MPD left and right (these four at 4 Hz, the others once per second).
  - once per minute of model time it writes one `export timing` line to the DCS log (`dcs.log`, source DCS-Dashboard): about 3 to 4 ms per second of model time (0.3 to 0.4 % of one core).
- **Not usable or limited:** the generic engine values of DCS's export functions do not fit the Apache (`RPM` is NG %, temperature is always 0; TGT, torque, NP and NR exist only in the MPD ENG page text while that page is shown). Indicated airspeed is implausible at low speed. The DCS-BIOS radio strings are unreliable (HF stuck at a start value); the EUFD lines carry the radio frequencies.

### Controlling

- **DCS-BIOS commands** (UDP to 127.0.0.1, one line per command, `IDENTIFIER VALUE`, for example `PLT_MASTER_IGN_SW 1`) work for most cockpit controls and have a readback. 227 of the 273 pilot controls and 238 of the 284 CP/G controls passed an automatic sweep (every position, readback within 0.5 s, original position restored); the blocklisted controls were skipped.
- **Keypresses** are needed for what DCS-BIOS cannot do. DCS reads the keyboard through scan codes, so keys are sent with `SendInput` and `KEYEVENTF_SCANCODE` (`ctypes`, standard library). Before a key the bridge taps LShift and brings the DCS window to the front (Windows only lets a background program change the active window right after it sent input; LAlt would put the window into menu mode), then waits 0.3 s. This worked every time. If the window does not come to the front no key is sent.
- **Power levers:** DCS-BIOS does not move them past the OFF detent, and keys for both levers together do not work. They move by keypress, one key per lever: RAlt (left) or RShift (right) with Home = IDLE, PageUp = one step up, PageDown = one step down, End = OFF. DCS-BIOS reads back 0 OFF, 16383 IDLE, 58981 FLY after each key.
- **Canopy:** DCS-BIOS cannot move it; a key (`canopy`) with the readback `PLT_CANOPY` does.
- **Cockpit logic still applies.** A command that the cockpit would not accept fails without an error: the APU button only works with its cover open; master ignition EXT PWR needs ground power; rotor brake BRK needs conditions; NVS mode FIXED needs the NVS on; push buttons under a DCS cover (fire buttons, CMWS jettison) are ignored while DCS's own cover is closed; ICS mode and the M4 safety need about 3 s to take the position; the CP/G manual tracker position 2 is spring-loaded.
- **Did not work:** the canopy (both seats), CP/G stick fold, MPD mode knobs by a direct command (the bridge uses INC / DEC steps), processor select, TADS select, SAI cage and pitch trim, CP/G left MPD L1–L6. Not followed up; the dashboard does not need them or works around them.
- **George** (the AI copilot menu) has no DCS-BIOS entry and works by keypress (`LCtrl+V`, `W` `S` `A` `D`) only with electrical power; it is not part of the dashboard.

### Blocklist idea

Dangerous or irreversible controls are never part of a sweep or a quick page: every identifier containing `JETT`, `FIRE_ENG`, `FIRE_APU`, `FIRE_PRIME`, `FIRE_RES`, `ZERO`, `CHOP`, `BUCS` or `TRIGGER` (jettison, fire buttons and extinguishers, zeroize, CHOP, BUCS, weapons trigger, M4 trigger, with their covers). On the dashboard these controls exist only on their own COCKPIT panel page, behind a guard ([section 6](#guarded-controls)); the grip controls with guards (CHOP, BUCS, emergency jettison, weapons trigger) are not on the dashboard at all.

## 5. Dashboard design rules, seat handling, settings

### Design rules

- **Cockpit names and positions.** Every control uses the label printed in the cockpit and shows all of its real positions, in cockpit order, even positions we do not use. A position that cannot be set is greyed out and cannot be selected.
- **Big touch targets:** 56 CSS pixels where space allows; at least 44 px on the three-row FLIGHT view and as on the real bezel on the MPD view (about 0.7 of the button spacing).
- **Landscape first.** Designed for an iPad Air in landscape (1180 × 820 CSS pixels), laid out with a CSS grid that also fits other tablets from about 1024 × 768 up. Portrait works but is not optimised. Smaller screens overlap.
- **Plain look.** Dark background, white stencil-style labels, lamp colours as in the cockpit. The panel pages need CSS container queries: Safari / iPadOS 16 or newer, or current Chrome.
- **No emoji-capable code points** in the UI or the aircraft file (they are drawn as coloured emoji on iOS). Arrows, chevrons, the close cross and the spring mark are inline SVG from one small icon set (`ICONS` in `core/web/index.html`: `chev-left`, `close`, `tri-up`, `tri-down`, `tri-left`, `tri-right`, `spring`).

### Seat

- Each view lists the seats it can be used in: FLIGHT, FIGHT, MPD, KU and the COCKPIT map both seats; a panel page lists the one seat it exists for. A control can also have its own `seats` (TAIL WHEEL on FLIGHT: pilot only) and is greyed in the other seat.
- The header badge shows the current seat: `PILOT` or `CP/G`. It adds ` – READ ONLY` when the shown view cannot be used in this seat: lamps and positions are shown, all controls are disabled.
- When the seat changes while a panel page is open, the page of the same name for the new seat opens (POWER stays POWER); if the new seat has no page of that name (CMWS, CENTER, EXT / INTR LT) the COCKPIT map of the new seat opens.
- The header shows `NO DCS DATA` when no DCS-BIOS packet arrived for 3 s, and `BRIDGE OFFLINE` when the page cannot reach the bridge.
- The bridge refuses commands of a view outside its seats.

### Settings and page lock

- A small gear button at the bottom right opens a settings page over the dashboard; `BACK` closes it. A free strip at the bottom of the controls keeps the gear clear of every control.
- **LOGGING** OFF / ON switches writing `logs/dcs-dashboard.log` on the PC (the console output stays). Saved in `config/settings.json`, applied immediately and kept across restarts.
- **KEEP SCREEN ON** OFF / ON uses the browser's screen wake lock, for this tablet only (stored in the browser).
- **INFO** shows the DCS Saved Games folder the bridge uses, the DCS data status and the address to open on another tablet.
- The page is locked for use as a home screen app: no scrolling, no rubber-band bounce, no pinch or double-tap zoom, no text selection or long-press menu. Rotation cannot be locked from a web page on iOS: use the iPad's rotation lock; in portrait a full-screen hint asks to turn the iPad.
- Home screen icon `core/web/apple-touch-icon.png` (180 × 180, "DCS" / "Dashboard", white on grey), name "DCS Dashboard".

### Confirmed presses

The bridge checks DCS-BIOS after sending: a push button is held until DCS reports it pressed (at least 0.3 s, at most 1 s) and then released; a hat is held until its axis shows the direction; a selector until the readback shows the new position (up to 0.5 s). The reply is `{"ok": true, "confirmed": true | false | null}` (`null` = not checked: knobs, cursor, keypresses). The log says `pressed, not confirmed` / `sent, not confirmed`, and the page shows an amber note `<label>: not confirmed by DCS` with a short amber flash on the control. Lost presses come from presses of only one DCS frame, commands waiting behind a slow power lever sequence, keypresses when DCS cannot be brought to the front, and double taps on toggle buttons.

## 6. The views

Tabs at the top: **COCKPIT | FLIGHT | FIGHT | MPD | KU**. Ids written as `{seat}_...` stand for `PLT_...` (pilot) or `CPG_...` (CP/G); in this section `{S}` is the same.

### COCKPIT

A simplified cockpit map and one page per cockpit panel with every button, switch, knob and display of that panel, as in the real AH-64D. The quick pages FLIGHT and FIGHT keep their mixed layout; a control can sit on a panel page and on a quick page at the same time, and both show the same DCS state.

**Navigation**

- **Tap COCKPIT:** the cockpit map of the current seat. Each box is a panel; tap a box to open its page.
- **On a panel page** the COCKPIT tab keeps its highlight and shows a back chevron before the word. One tap goes back to the map.
- **Long hold (0.5 s) on COCKPIT:** a list of every page of the current seat, for jumping from page to page.
- The map boxes for the two MPDs, the TEDAC (CP/G only) and the KU open the MPD and KU tabs (MPD L, MPD R or TEDAC preselected).
- A page that does not exist in the current seat is not shown (map and list), it is not greyed out.
- The master lamps (MASTER WARNING, MASTER CAUTION) stay in the top row of the map and of every panel page. `CANOPY` is a small key button on the map (pilot seat).

**Switches.** A tap on a switch (a toggle or a dial) opens a chooser at the switch: one big button per position (at least 64 px, 8 px apart), arranged like the switch (a column, a row for `orient: "h"`, an arc for a dial: each button on a circle at the angle of its dial position, radius 90 px for two positions, 110 for three, 130 for four, spread in steps of 5 % until every pair is 8 px apart). The current position is lit, a `disabled` position is dashed and does nothing, a `momentary` (spring-return) position carries a spring mark, and a title line shows the control label. A tap on a position sends the command and closes the chooser; a tap on the position already set sends nothing; a tap outside closes the chooser without a command. While a command is sent the switch shows an amber outline. The power levers, the FRICT slider, rockers, buttons and guarded switches have no chooser.

**Knobs.** A tap on a knob opens the knob bar next to it ([Knob bar](#knob-bar)). On COMM, holding a volume knob for 0.6 s pulls it out or pushes it in (a ring fills during the hold).

**Pop-ups** (chooser and knob bar) open at the control, not in the middle of the screen: the bar below its knob (8 px gap; above it if there is no room; else centred on the knob), the chooser centred on the switch. Both are clamped into the screen: 8 px from the edges, below the tab bar, and clear of the gear (its 44 × 44 box plus 8 px, moved left or up, whichever shift is smaller). The scrim stays: a tap outside closes a pop-up without a command. The function is `placePopup(anchor, width, height, prefer)` in `core/web/index.html`.

**The map** is a 12 × 7 grid, `[row, col, rows, cols]`, of plain boxes with the panel placard, in the order of the real cockpit.

Pilot:

```
 1  KU            | FIRE DET/EXTG       EUFD                    | CMWS
 2  TAIL WHL/NVS  | ARMAMENT            [CANOPY]                |
 3  EMERGENCY     | ┌─────────────┐ ┌─────────────┐             | COMM
 4  POWER         | │    MPD L    │ │    MPD R    │             |
 5  (levers)      | └─────────────┘ └─────────────┘             |
 6  STORES JETT   |       CENTER (OVSP/GEN RST, WIPER, PARK BRAKE, ALT SET)
 7  EXT/INTR LT   |
    left console    instrument panel                              right console
```

| Page | Grid (PLT) | Page | Grid (PLT) |
| --- | --- | --- | --- |
| KU | [1,1,1,3] | FIRE DET/EXTG | [1,4,1,3] |
| TAIL WHEEL / NVS | [2,1,1,3] | EUFD | [1,7,1,3] |
| EMERGENCY | [3,1,1,3] | ARMAMENT | [2,4,1,3] |
| POWER | [4,1,2,3] | CANOPY (key) | [2,7,1,3] |
| STORES JETT | [6,1,1,3] | MPD L / MPD R | [3,4,3,3] / [3,7,3,3] |
| EXT / INTR LT | [7,1,1,3] | CENTER | [6,5,2,4] |
| CMWS | [1,10,2,3] | COMM | [3,10,3,3] |

CP/G:

```
 1  KU            | FIRE DET/EXTG  ARMAMENT          EUFD         |
 2  EMERGENCY     | ┌───────────┐ ┌──────────┐ ┌───────────┐     | COMM
 3  POWER         | │   MPD L   │ │  TEDAC   │ │   MPD R   │     |
 4  (levers)      | └───────────┘ └──────────┘ └───────────┘     | WIPER / DEFOG
 5  TAIL WHL/NVS  |                                              |
 6  INTR LT       |                                              |
 7  STORES JETT   |                                              |
    left console    instrument panel                               right console
```

| Page | Grid (CPG) | Page | Grid (CPG) |
| --- | --- | --- | --- |
| KU | [1,1,1,3] | FIRE DET/EXTG | [1,4,1,2] |
| EMERGENCY | [2,1,1,3] | ARMAMENT | [1,6,1,2] |
| POWER | [3,1,2,3] | EUFD | [1,8,1,3] |
| TAIL WHEEL / NVS | [5,1,1,3] | MPD L / TEDAC / MPD R | [2,4,3,2] / [2,6,3,2] / [2,8,3,3] |
| INTR LT | [6,1,1,3] | COMM | [2,11,2,2] |
| STORES JETT | [7,1,1,3] | WIPER / DEFOG | [4,11,1,2] |

The CP/G has no CMWS, no EXT LT, no VIDEO, no CHECK OVERSPEED / GENERATOR RESET panel, no PARK BRAKE, no master ignition, no APU, no engine start, no rotor brake. The CP/G wiper and defog are on the right console, on their own page WIPER / DEFOG below COMM; the pilot's are on the CENTER page.

**Naming convention**

- **Page name** = the placard of the panel in upper case (`FIRE DET/EXTG`, `STORES JETT`, `TAIL WHEEL / NVS`).
- **Control label** = the text printed on the panel. A rocker shows its name between two arrows (`WCA`), a knob its name (`FLOOD`).
- **Positions** are listed in the order printed on the panel, top to bottom or left to right, with all real positions, also unusable ones (greyed out).
- **Control id** = the DCS-BIOS identifier with the seat as `{S}`. A function without a DCS-BIOS entry (keypress) uses a lower-case name from `[keys]` (`canopy`, `power_left`).
- All text in English, as in the cockpit.

#### Guarded controls

A guarded control can end the flight or cannot be undone in the mission: shut off an engine or the APU (the FIRE buttons stop the fuel flow), discharge an extinguisher bottle, drop stores (JETT), wipe the radio and crypto data (zeroize), jettison the countermeasure flares. All are on the tablet, only on their own panel page (never on FLIGHT or FIGHT), and need two deliberate steps:

1. **Lift the cover.** The control is covered by a red and white hazard-striped frame with a padlock. The middle of the frame is clear, so the lamps and the control underneath stay visible. Tap the cover to lift it. It closes again after 5 seconds, or after the press. Only one cover can be open at a time.
2. **Tap the control.** One tap on the button, or on the position of a guarded switch, sends the command and the cover closes. A guarded switch is the one switch without a chooser: under the cover each position is a touch band of its own (60 du, equal split).

The kit draws the cover from the part: the part (or its white frame) and 12 du on every side, a hazard frame 14 du wide, a padlock of 24 du (`cover_at`, never typed in). The bridge enforces the rule, so a second tab, a bug in the page or a stale tab cannot bypass it:

- Opening a cover sends `{"id": ..., "guard": "open"}`. The bridge opens a 5 second window for that id only.
- A command for a guarded id is accepted only inside its window, and the window is used up by the press. Otherwise the answer is `refused: guard closed`.
- The press itself is a confirmed press: the bridge holds until DCS-BIOS shows the button.
- Log lines: `guard open`, `pressed`, `refused: guard closed`, and for the parts with a real cover `cover open`, `cover closed` and `refused: cover did not open`.

**Real DCS covers.** Where the real cockpit has a cover (FIRE ENG 1, APU and ENG 2, master zeroize, CMWS flare jettison), DCS-BIOS has a cover control (`{S}_FIRE_ENG1_CVR`, `_APU_CVR`, `_ENG2_CVR`, `{S}_INST_MZERO_CVR`, `PLT_CMWS_JETT_CVR`), and DCS does not react to the button while its own cover is closed. These controls carry a `cover` property with that id, and the bridge opens and closes DCS's own cover for them. Lifting the tablet cover sets the real cover to 1 and waits up to 0.5 s for the DCS-BIOS readback; if it does not open, the answer is `refused: cover did not open` and the tablet cover stays shut. The bridge closes the real cover again about 1 second after the command was accepted, when the 5 second window runs out unused, or at once when another guarded control is lifted. PRI, RES, JETT and ZEROIZE have no cover in DCS-BIOS and only use the tablet cover.

Controls with `guard`: `{S}_FIRE_ENG1_BTN`, `{S}_FIRE_APU_BTN`, `{S}_FIRE_ENG2_BTN`, `{S}_FIRE_PRIME_EXT`, `{S}_FIRE_RES_EXT`, `{S}_JETT_BTN`, `{S}_EMERG_ZERO_SW`, `{S}_INST_MZERO_SW`, `PLT_CMWS_JETT`. The six station select buttons only arm a station and light up; they are normal buttons, and JETT is guarded. The guarded switches ZEROIZE, MASTER ZEROIZE and CMWS JETT list ON on top and OFF at the bottom.

#### Power levers

Used on the FLIGHT view and on the POWER page.

- One vertical slider per lever, positions bottom to top: OFF, IDLE, FLY, LOCKOUT. The slider snaps to positions only. LOCKOUT is shown above FLY but greyed and cannot be reached.
- Readback to position: the nearest of OFF 0, IDLE 16383, FLY 58981, LOCKOUT 65535.
- Moving the slider sends the keys for that lever, one step at a time, waiting up to 1 s for the readback after each step: OFF → IDLE `power_<side>_idle`; IDLE → FLY `power_<side>_up`; FLY → IDLE `power_<side>_down`; IDLE → OFF `power_<side>_off`. OFF → FLY and FLY → OFF go through IDLE. `<side>` is `left` for PWR LVR 1 (engine 1) and `right` for PWR LVR 2 (engine 2).
- On the panel pages a tap on a mark moves the lever (one touch band per mark); the grip follows the readback. A tap on the FRICT slot opens the knob bar.

#### Lamp row

MASTER WARNING (red) and MASTER CAUTION (amber) with `{seat}_` ids are lighted push buttons as in the cockpit: tapping the lamp presses `{seat}_INTL_MWARN_BTN` / `{seat}_INTL_MCAUTION_BTN` (0.3 s). Every COCKPIT page has the two master lamps in its top row. FLIGHT adds ENG 1 FIRE, APU FIRE and ENG 2 FIRE (red, `PLT_ENG_1_FIRE_L`, `PLT_APU_FIRE_L`, `PLT_ENG_2_FIRE_L`) and APU ON (green, `PLT_APU_L`); FIGHT adds the armament lamps. Lamps are display only, except the master lamps.

#### Panel pages

Value = label in the position lists. `rest` = resting value of a spring-loaded switch (set, held, back to rest). Seats: both unless noted.

**POWER** (left console). Pilot: everything. CP/G: the two power levers only.

| Label | Id | Type | Positions / notes |
| --- | --- | --- | --- |
| RTR BRK | `PLT_ROTOR_BRK` | selector | 2 OFF, 1 BRK (greyed out, needs conditions), 0 LOCK |
| MSTR IGN | `PLT_MASTER_IGN_SW` | selector | 0 OFF, 1 BATT, 2 EXT PWR (greyed out, no ground power) |
| APU cover | `PLT_APU_BTN_CVR` | selector | 0 CLOSED, 1 OPEN |
| APU | `PLT_APU_BTN` | button, `requires` the cover open | press; lamp `PLT_APU_L` ON. Locked while the cover is closed: the page does not send it and the bridge refuses it |
| ENG START NO 1 / NO 2 | `PLT_ENG1_START`, `PLT_ENG2_START` | selector, rest 1 | 2 START (momentary), 1 OFF, 0 IGN ORIDE (momentary); held 0.5 s |
| PWR LVR NO 1 / NO 2 | `{S}_ENG_L_PW_LVR`, `{S}_ENG_R_PW_LVR` | lever (keypress, readback) | OFF 0, IDLE 16383, FLY 58981, LOCKOUT 65535 (greyed out); both seats |
| FRICT | `PLT_PW_LVR_FRIC` | knob | 0 to 65535 |

**TAIL WHEEL / NVS**: TAIL WHEEL `{S}_T_WHEEL_UNLOCK_BTN` (button, lamp `{S}_T_WHEEL_UNLOCK_L` UNLOCK); NVS MODE `{S}_NVS_MODE` (selector: 2 FIXED, needs the NVS on; 1 NORM; 0 OFF).

**EMERGENCY**: GUARD `{S}_EMERG_GUARD_BTN`, XPNDR `{S}_EMERG_XPNDR_BTN` and EMERG HYD `{S}_EMERG_HYD_BTN` (buttons, lamps `{S}_EMERG_GUARD_L`, `{S}_EMERG_XPNDR_L`, `{S}_EMERG_HYD_L`); ZEROIZE `{S}_EMERG_ZERO_SW` (selector, `guard`, 0 / 1 toggle).

**STORES JETT**: six station buttons (press arms the station) with lamps, and the guarded JETT `{S}_JETT_BTN`. Buttons `{S}_JETT_STORE_LO`, `_LI`, `_RI`, `_RO`, `_LW`, `_RW` (L OUTBD, L INBD, R INBD, R OUTBD, L TIP, R TIP); lamps `{S}_JETT_L_OUTBOARD_L`, `_L_INBOARD_L`, `_R_INBOARD_L`, `_R_OUTBOARD_L`, `_L_TIP_L`, `_R_TIP_L`.

**EXT / INTR LT.** Pilot: both blocks. CP/G: INTR LT only (no STBY INST knob).

| Label | Id | Type | Positions | Seats |
| --- | --- | --- | --- | --- |
| NAV | `PLT_EXTL_NAV_L_SW` | selector | 2 BRT, 1 OFF, 0 DIM | PLT |
| FORM | `PLT_EXTL_FROMATION_L_KNB` | knob | OFF to BRT | PLT |
| ANTI COL | `PLT_EXTL_ACOL_L_SW` | selector | 2 WHT, 1 OFF, 0 RED | PLT |
| SIGNAL | `{S}_INTL_SIGNAL_L_KNB` | knob | DIM to BRT | both |
| PRIMARY, FLOOD | `{S}_INTL_PRIMARY_L_KNB`, `{S}_INTL_FLOOD_L_KNB` | knob | OFF to BRT | both |
| STBY INST | `PLT_INTL_STBYINST_L_KNB` | knob | OFF to BRT | PLT |
| PRESS TO TEST | `{S}_INTL_TEST_BTN` | button | press | both |

**FIRE DET/EXTG** (glareshield). A yellow FIRE and a green RDY light on each of ENG 1, APU and ENG 2, and a DISCH light on PRI and RES. A fire button press arms the extinguisher for that compartment and shuts off its fuel (press again: safe). All buttons are guarded; ENG 1, APU and ENG 2 have a real DCS cover.

| Label | Id | Lamps |
| --- | --- | --- |
| ENG 1 | `{S}_FIRE_ENG1_BTN` | FIRE `{S}_ENG_1_FIRE_L`, RDY `{S}_ENG_1_READY_L` |
| APU | `{S}_FIRE_APU_BTN` | FIRE `{S}_APU_FIRE_L`, RDY `{S}_APU_READY_L` |
| ENG 2 | `{S}_FIRE_ENG2_BTN` | FIRE `{S}_ENG_2_FIRE_L`, RDY `{S}_ENG_2_READY_L` |
| PRI | `{S}_FIRE_PRIME_EXT` (discharge) | DISCH `{S}_FIRE_EXT_DISCH_PRI_L` |
| RES | `{S}_FIRE_RES_EXT` (discharge) | DISCH `{S}_FIRE_EXT_DISCH_RES_L` |
| TEST | `{S}_FIRE_DETECT_TEST` | selector, rest 1: 0 "1" (momentary), 1 OFF, 2 "2" (momentary); not guarded |

**ARMAMENT** (with VIDEO and MASTER ZEROIZE). The pilot page carries the ARMAMENT panel, the MASTER ZEROIZE placard and the VIDEO panel; the CP/G page ARMAMENT and MASTER ZEROIZE only. MASTER ZEROIZE is a plain placard (the switch sits on the instrument panel next to the armament panel). On the VIDEO panel IHADSS BRT / CON share one knob and FLIR LVL / GAIN share one knob; a small mark next to the knob selects the function (`group`, `mark`, `dot`).

| Label | Id | Type | Notes |
| --- | --- | --- | --- |
| A/S | `{S}_MASTER_ARM_BTN` | button | lamps ARM `{S}_MASTER_ARM_ARM_L`, SAFE `{S}_MASTER_ARM_SAFE_L` |
| GND ORIDE | `{S}_GROUND_OVERRIDE_BTN` | button | lamp `{S}_GROUND_OVERRIDE_L` |
| MASTER ZEROIZE | `{S}_INST_MZERO_SW` | selector, `guard` | 0 / 1 (toggle); real cover `{S}_INST_MZERO_CVR` |
| IHADSS BRT, CON | `PLT_VIDEO_IHADSS_BRT`, `PLT_VIDEO_IHADSS_CON` | knob | MIN to MAX, PLT |
| SYM BRT | `PLT_VIDEO_SYM_BRT` | knob | MIN to MAX, PLT |
| ACM | `PLT_VIDEO_AUTO_CON` | selector | 0 OFF, 1 ACM, PLT |
| FLIR LVL, GAIN | `PLT_VIDEO_FLIR_LVL`, `PLT_VIDEO_FLIR_GAIN` | knob | MIN to MAX, PLT |

**EUFD.** The display is on top and the controls sit in a row below it: the three rockers, the BRT knob and the four keys (the text size matters more than the photo layout).

| Label | Id | Type | Positions / notes |
| --- | --- | --- | --- |
| display | `{S}_EUFD_LINE1` to `_LINE14` | display, `ids` | 14 lines of 56 characters, shown as on the real display |
| WCA, IDM, RTS | `{S}_EUFD_WCA`, `_IDM`, `_RTS` | hat (IDM, RTS: rest 1) | 2 up, 1 off, 0 down |
| BRT | `{S}_EUFD_BRT` | knob | DIM to BRT |
| P (preset), ENTER, STOPWATCH, SWAP | `{S}_EUFD_PRESET`, `_ENT`, `_STOPWATCH`, `_SWAP` | button | press; STOPWATCH: press to start / stop, hold to reset |

**CMWS** (pilot only).

| Label | Id | Type | Positions / notes |
| --- | --- | --- | --- |
| PWR | `PLT_CMWS_PW` | selector, rest 1 | 0 OFF, 1 ON, 2 TEST (momentary) |
| STATUS | `PLT_CMWS_FLARE_LETTER`, `_FLARE_COUNT`, `_CHAFF_LETTER`, `_CHAFF_COUNT`, `_BIT_LINE_1`, `_BIT_LINE_2`, `_PAGE` | display, `ids`, `pages` | page MAIN `F 60` / `C 30`, page TEST the two test lines, page NONE blank |
| THREAT lamps | `PLT_CMWS_FWD_LEFT_BRT_L`, `_FWD_RIGHT_`, `_AFT_LEFT_`, `_AFT_RIGHT_`, `PLT_CMWS_D_BRT_L`, `PLT_CMWS_R_BRT_L` (and the matching `_DIM_L`) | page-level `indicators` | orange, bright and dim |
| AUDIO, LAMP | `PLT_CMWS_VOL`, `PLT_CMWS_LAMP` | knob | MIN to MAX |
| ARM / SAFE | `PLT_CMWS_ARM` | selector | 1 ARM, 0 SAFE |
| CMWS / NAV | `PLT_CMWS_MODE` | selector | 1 CMWS, 0 NAV |
| BYPASS / AUTO | `PLT_CMWS_BYPASS` | selector | 1 BYPASS, 0 AUTO |
| JETTISON | `PLT_CMWS_JETT` | selector, `guard` | 0 / 1; real cover `PLT_CMWS_JETT_CVR` |

**CENTER** (pilot only, instrument panel). One wide plate (CHK OVSP TEST and GEN RST) over two plates (WINDSHIELD WIPER, and PARK BRAKE with ALT SET), 16 du apart on shared edge lines. The PARK BRAKE name is printed on two lines.

| Label | Id | Type | Positions |
| --- | --- | --- | --- |
| CHK OVSP TEST, CKT A / B | `PLT_CHK_OSPD_ENG_A`, `_B` | selector, rest 1 | 2 ENG 1, 1 OFF, 0 ENG 2 (spring return) |
| GEN RST | `PLT_GEN_RESET` | selector, rest 1 | 0 GEN 1, 1 off, 2 GEN 2 (spring return) |
| DEFOG | `PLT_DEFOG_BTN` | button | press |
| WINDSHIELD WIPER | `PLT_WIPER_SW` | selector | 0 PARK, 1 OFF, 2 LO, 3 HI |
| PARK BRAKE | `PLT_PARK_BRAKE` | selector | 0 IN, 1 PULLED |
| ALT SET | `PLT_ALT_SET_KNB` | knob | 0 to 65535 |

**COMM** (right console). One drawing for both seats. The ICS name and its PTT label sit in the SOL row, between the FM 1 and FM 2 squelch switches; the switch itself, with VOX and HOT MIC, is below the row. The volume knobs of VHF, UHF, FM 1, FM 2, HF, VCR and ADF have a PULL chip (a `chip` control, 64 × 22 du, touch area at least 32 px) hanging under the knob for the pull-to-disable position; holding the knob for 0.6 s toggles it too, a short tap opens the knob bar.

| Label | Id | Type | Positions |
| --- | --- | --- | --- |
| VHF, UHF, FM 1, FM 2, HF volume | `{S}_COM_VHF_VOL`, `_UHF_`, `_FM1_`, `_FM2_`, `_HF_` | knob | MIN to MAX |
| VHF, UHF, FM 1, FM 2, HF disable (pull) | `{S}_COM_VHF_PW`, `_UHF_`, `_FM1_`, `_FM2_`, `_HF_` | selector | 0 In, 1 Out |
| SQL x 5 | `{S}_COM_VHF_SQL`, `_UHF_`, `_FM1_`, `_FM2_`, `_HF_` | selector, rest 1 | 2 ENABLE, 1 off, 0 DISABLE (spring return) |
| MASTER, SENS | `{S}_COM_MASTER_VOL`, `{S}_COM_SENS_KNB` | knob | MIN to MAX |
| ICS | `{S}_COM_ICS_MODE` | selector | 0 HOT MIC, 1 VOX, 2 PTT (takes about 3 s) |
| IDENT | `{S}_COM_IDENT_BTN` | button | press |
| IFF, RLWR, ATA, VCR, ADF volume | `{S}_COM_IFF_VOL`, `_RLWR_`, `_ATA_`, `_VCR_`, `_ADF_` | knob | MIN to MAX |
| VCR, ADF disable (pull) | `{S}_COM_VCR_PW`, `{S}_COM_ADF_PW` | selector | 0 In, 1 Out |

**WIPER / DEFOG** (CP/G only). The same drawing as the wiper block of the CENTER page; the position labels (PARK, OFF, LO, HI) are flat text in a fan above the dial. DEFOG `CPG_DEFOG_BTN` (button), WINDSHIELD WIPER `CPG_WIPER_SW` (0 PARK, 1 OFF, 2 LO, 3 HI).

**Not on a page:** the CP/G processor select panel (not implemented in DCS), the SAI (cage and pitch trim do not work; only the altimeter setting knob is used, on CENTER), canopy jettison, M4 rifle, sun visors, stick fold, radio frequencies.

### FLIGHT

Follows the current seat. Lamp row as above. A fixed grid of 3 rows × 7 columns (each control has `"grid": [row, col, rows, cols]`), so the power levers and TAIL WHEEL stay in the same place when switching to FIGHT.

| Label | DCS-BIOS / route | Grid | Notes |
| --- | --- | --- | --- |
| TRIM | export script + `{seat}_CYCLIC_TRIM_UD`, see below | rows 1–2, columns 1–2 | read only |
| CTRL IND | key `controls_overlay` | row 3, column 1 | toggles DCS's own controls overlay (no lag) |
| SYMBOLOGY | `{seat}_CYCLIC_SYMBOLOGY` | rows 1–2, column 4 | two-way hat: T/C ↑ (2), H/B ↓ (0), held 0.3 s, back to centre |
| MONOCLE | key `monocle` | row 1, column 5 | push button, no state |
| TAIL WHEEL | `PLT_T_WHEEL_UNLOCK_BTN`, lamp `PLT_T_WHEEL_UNLOCK_L` | row 2, column 5 | lit push button, press = 1, released to 0 after 0.3 s; pilot seat only (greyed in the CP/G seat) |
| PWR LVR 1, 2 | keys, readback `{seat}_ENG_L_PW_LVR` / `{seat}_ENG_R_PW_LVR` | columns 6 and 7 | ids `flight_power_left` / `flight_power_right` |

**Trim display.**

- The export script sends the actual control positions 10 times per second. The bridge receives them on the export port (if the port is busy it logs `export port busy` and runs without them).
- The live position is not drawn (it lags behind the stick); CTRL IND toggles DCS's own overlay for that.
- **Trim point:** when the Force Trim switch (`{seat}_CYCLIC_TRIM_UD`) goes from 2 (held, `TRIM_RELEASED`) back to rest, the bridge stores the cyclic pitch / roll and the pedals at that moment as the seat's trim point and logs `PLT set P … R … Y …`.
- **Trim reset:** while DCS is the active window, the bridge watches the `trim_reset` key by reading only that key's state; on a press it moves the trim point to the centre and logs `PLT reset`.
- `/state` has `controls` (the latest positions), `controls_age` and `trim`: `{"plt": {"pitch", "roll", "pedals", "reset", "age"}, ...}`.
- The page draws a small box with a green ring at the trim point and a green tick on the pedal bar, with the values as text; `NOT TRIMMED` before the first trim, `RESET` after a reset. Directions are set by `CTRL_PITCH_SIGN`, `CTRL_ROLL_SIGN`, `CTRL_PEDAL_SIGN` at the top of the page script.

### FIGHT

Follows the current seat. The same fixed 3 × 7 grid as FLIGHT.

| Lamp | DCS-BIOS | Colour |
| --- | --- | --- |
| MASTER WARNING | `{seat}_MASTER_WARNING_L` | red (tappable) |
| MASTER CAUTION | `{seat}_MASTER_CAUTION_L` | amber (tappable) |
| ARM | `{seat}_MASTER_ARM_ARM_L` | amber |
| SAFE | `{seat}_MASTER_ARM_SAFE_L` | green |
| GND ORIDE | `{seat}_GROUND_OVERRIDE_L` | amber |

| Label | DCS-BIOS | Positions | Notes |
| --- | --- | --- | --- |
| A/S | `{seat}_MASTER_ARM_BTN` | push button | press = 1, released to 0 after 0.3 s; the ARM and SAFE lamps show the result |
| GND ORIDE | `{seat}_GROUND_OVERRIDE_BTN` | push button | as A/S |
| WAS | hat: `{seat}_CYCLIC_WEAPON_UD` / `_LR` | up = G, down = A, left = R, right = M | see Hats |
| SIGHT SEL | hat: `{seat}_COLLECTIVE_SIGHT_SELECT_UD` / `_LR` | up = HMD, down = LINK, left = FCR, right = TADS | see Hats |
| FLARE, CHAFF | `{seat}_CYCLIC_FLARE`, `{seat}_CYCLIC_CHAFF` | push button | as A/S |
| FLARE COUNT, CHAFF COUNT | `PLT_CMWS_FLARE_COUNT`, `PLT_CMWS_CHAFF_COUNT` | display | read only; from the pilot's CMWS panel, shown in both seats |

**Hats.** A hat is drawn as a cross of four buttons. A tap sets the axis (`_UD` or `_LR`) to 2 (up, right) or 0 (down, left) and holds it for 0.3 s; then the bridge returns the axis to the centre, 1. The highlighted direction comes from the readback of the two axes. The TEDAC grip hats of the CP/G (LHG WAS, RHG sight select) are left out on purpose: they do the same as the cyclic WAS and the collective sight select (they work too, as a fallback).

**CMWS (pilot seat only).** Flares only fire with the CMWS panel set up: CMWS PWR ON, FLARE SQUIBS ARM, CMWS MODE CMWS; CMWS OPER BYPASS / AUTO decides whether the CMWS dispenses on its own. Chaff must be armed on the MPD ASE page. On the ground dispensing may be blocked.

| Label | DCS-BIOS | Positions | Grid |
| --- | --- | --- | --- |
| CMWS PWR | `PLT_CMWS_PW` | 2 = TEST (spring-loaded, 0.5 s), 1 = ON, 0 = OFF | row 1, column 5 |
| FLARE SQUIBS | `PLT_CMWS_ARM` | 1 = ARM, 0 = SAFE | row 1, column 6 |
| CMWS MODE | `PLT_CMWS_MODE` | 1 = CMWS, 0 = NAV | row 2, column 5 |
| CMWS OPER | `PLT_CMWS_BYPASS` | 1 = BYPASS, 0 = AUTO | row 2, column 6 |

### MPD

One display at a time, following the current seat (`"layout": "mpd"`). A `LEFT MPD | TEDAC | RIGHT MPD` switch at the top selects which one (remembered on the tablet); TEDAC appears only in the CP/G seat. The display sits flush left, the cursor group uses the rest of the width (pad about 450 px on the iPad Air).

- Laid out 1:1 after a photo of the real MPD: every button, knob and print at its measured position (square spacing, about 100 px pitch on the photo). VID knob on the raised top-left corner, BRT below it, MODE top right with DAY / NT / MONO; \* above R1; FCR / WPN below L6, VID / COM below R6; TSD and A/C offset in the bottom corners next to M and B2–B6.
- Variable action buttons are light grey with a green dot; fixed action buttons are black keys with green text. Buttons are drawn at true size (about 33 px on the iPad Air) with a larger invisible touch area (56 px where neighbours allow). Each press is held 0.3 s.
- **Live labels:** the export script sends the occupied seat's MPD texts (`MPD_INDICATIONS`, `MPD_SEATS`: pilot 7 left / 9 right, CP/G 11 / 13) 4 times per second. The bridge reads the `PB<n>` fields and serves them as `mpd_labels` in `/state` (`{"L": {...}, "R": {...}, "age": ...}`); the page writes each label in MPD green next to its button. Mapping: PB1–6 = T1–T6, PB7–12 = R1–R6, PB13–18 = B6…B1 (PB18 = M), PB19–24 = L6…L1. No labels when no MPD text arrived for 3 s.
- In the CP/G seat the left MPD's L1–L6 do not respond in DCS.

**Cursor.** The CURSOR pad sits to the right of the bezel, for the collective cursor controller `{seat}_COLLECTIVE_CURSOR_LR` / `_UD` (analog, centre 32768). Put a finger anywhere on the pad and push: the distance from the touch point (up to 30 % of the pad) is the deflection, i.e. the cursor speed, like the real force-sensing controller. Lifting the finger sends centre. The page sends `{"x", "y"}` (−1..1) at most every 66 ms; the bridge sends only changed axes and does not wait behind slow commands. `CURSOR_Y_SIGN` at the top of the page script flips up / down. Below the pad: CURSOR SWITCH DISPLAY (`{seat}_COLLECTIVE_CURSOR_DISPLAY`, moves the cursor to the other MPD) and ENTER (`{seat}_COLLECTIVE_CURSOR_ENTER`).

**TEDAC (CP/G seat).** The CP/G's TEDAC display unit, laid out 1:1 after a photo like the MPD. All controls are `CPG_TEDAC_…`, `"side": "T"`, `"seats": [1]`:

- Top: TAD, FCR, PNV, G/S video select buttons; MODE knob DAY / NT / OFF (2 / 1 / 0, knob bar).
- Left: LEV and GAIN knobs (knob bar), R/F and EL rockers. Right: SYM, BRT, CON rockers and \*.
- Bottom: ◀AZ▶ rocker, then four buttons AZ/EL, ACM, FREEZE, FILTER with their names in green on the screen.
- Rockers are spring-loaded: tap the upper / lower half (AZ: left / right half); the bridge holds the position until confirmed and returns it to the centre.

#### Knob bar

Tapping a knob (MPD BRT / VID / MODE, KU BRT, TEDAC knobs, the knobs of the COCKPIT pages) opens a bar at the knob (420 px wide, or the screen less 24 px, 120 px high): below it, above it if there is no room, always inside the screen. BRT / VID / KU BRT and the panel knobs: drag or tap the track; the bridge sets the absolute knob position (`{"value": 0..65535}`, at most every 100 ms while dragging). MODE: three stops DAY / NT / MONO. Tap outside or the close cross to close. The MPD mode selectors use `step_fallback`: if the position is not reached in 0.5 s the bridge turns the knob with INC / DEC steps.

### KU

The keyboard unit, drawn 1:1 after a photo in the same technique as the MPD (`"layout": "ku"`), following the current seat: round number keys, boxed E / N / S / W, the white guide lines of the panel, BRT knob in its recess (knob bar), wide ENTER.

- Top: the scratchpad (`{seat}_KU_DISPLAY`) in green.
- Rows: A–F | 1 2 3, G–L | 4 5 6, M–R | 7 8 9, S–X | . 0 +/-, then Y Z / BKS SPC \* ÷ + −, then the BRT knob, CLR, ←, →, ENTER.
- Keys are pressed for 0.15 s.

## 7. The panel kit

`core/panel_kit.py` is a small layout compiler. A page entry names a part and a centre point, never a size; the compiler writes the resolved geometry (boxes in du, label positions, plate, ears, screws) into the page data in the format the page already draws. The page draws what it is given and has no hard-coded sizes. The photos only say what is on a panel, its text and the arrangement of the parts, not pixel sizes.

**Design units and one scale.** All panel geometry is in design units (du); one du is the same size on every page. Every page is drawn at the same scale `S = min(area width / 640, area height / 600)`, at most 1.6, for both seats: 1.045 at 1180 × 820, 0.958 at 1024 × 768 (the app area is about 627 px and 575 px high). 640 × 600 du is a fixed budget (POWER and COMM use all of it); a larger page is a layout error. A part of 56 du is 58.5 px at the first and 53.7 px at the second size.

**Page definition.** Panel pages are `VIEWS` entries flagged `"panel": True`, one entry per seat where the seats differ. `kit_pages` in `aircraft/ah64d.py` writes the entry from a `Panel` (or a `PanelGroup` of several plates):

```
{"name": "FIRE DET/EXTG", "seats": [1], "panel": True, "layout": "panel", "map": [row, col, rows, cols], "box": [w, h],
 "lamps": [...], "print": [...], "art": [...], "controls": [...], "indicators": [...], "kit": True, "ref": [640, 600]}
```

`map` is the cell on the cockpit map; `box` the size in du; `ref` the 640 × 600 budget the scale is computed from; `kit` marks a page drawn by the kit; `print` the placard text as `[text, x, y, size, width, rotation]`; `art` the drawn parts (plate, ear, screw, bracket, outline, slot, glass, hazard, line, arrow, path, text); `lamps` the top row with the master lamps; `indicators` (optional) free lamps drawn on the panel (the CMWS threat sectors), each with a bright and a dim DCS-BIOS id.

The COCKPIT view (layout `map`) is one entry for both seats. It holds `links` (the map boxes that open the KU, MPD and TEDAC tabs, each with `view`, `side`, `seats` and `map`) and the canopy key.

**Parts and sizes (du)**

| Part | Size | Used for |
| --- | --- | --- |
| `PUSH` | bezel 84 × 84, face 60 × 60; frame variant: white frame 100 × 100, 4 stroke, centred by construction | all square pushbuttons (GUARD, XPNDR, EMERG HYD, TAIL WHEEL, A/S, GND ORIDE, APU, the 6 station buttons, FIRE / PRI / RES) |
| `PUSH_SMALL` | 56 × 56 | the four EUFD keys |
| `ROUND` | 64 | DEFOG, IDENT, PRESS TO TEST, ACM cap |
| `PLUNGER` | 100 | JETT |
| `TOGGLE` | ring 56, lever 40, touch square 60 (a guarded one: a band of 60 per position) | all toggle switches |
| `ROTARY` | tick ring 100, knob 72 | MSTR IGN, CMWS PWR, WIPER |
| `KNOB_L` / `KNOB_M` / `KNOB_S` | 96 / 72 / 56 | L: MASTER, IHADSS, FLIR, EUFD BRT. M: FORM, SIGNAL, PRIMARY, FLOOD, STBY INST, SYM BRT, AUDIO, LAMP, SENS, ALT SET. S: the 5 radio volumes and the 5 AUX knobs |
| `MARK` | dot 10, touch square 56 beside the knob, marks 64 apart | selector marks of the dual-function knobs |
| `ROCKER` | 52 × 120 | EUFD WCA / IDM / RTS |
| `CHIP` | 64 × 22; text 48 % of the height, no letter spacing | PULL chips |
| `DIAL` | 112 | the CMWS threat dial |
| `LEVER` | grip 40 × 40, slot = grip + 8 on every side, travel chosen by the page (360 to 440, even) | the power lever grips |
| `SLIDER` | slot 56 × 240, grip is a `LEVER` grip | FRICT |
| `DISPLAY` | the only part whose size the page chooses (even du); text area = glass less 6 on every side | EUFD 568 × 280, CMWS status 104 × 96 |
| `FLAP` | the button + 8 on each side | the hinged cover of the APU button (a control of its own) |
| `GUARD_COVER` | the guarded part + 12 du on each side, frame 14 wide, padlock 24 | all guarded parts; derived, never typed in |
| `HAZARD_PAD` | the part (or its cover) + 20 du on each side, more where the pad holds a label | JETT, EMERG HYD, CMWS JETT pads |
| `HOUSING`, `HAZARD_STRIP` | dark housing = the part (or its cover) + 12 on each side; strip 32 wide against a housing side | the three fire buttons |
| `EAR` | rectangular corner ear 52 × 52, flush in the plate corner, 2 border | the four corners of every plate |
| `SCREW_L` / `_M` / `_S` | diameter 26 / 18 / 12 | `SCREW_L` centred in each ear |
| Label styles | `TITLE` 32, `NAME` 24, `POS` 20, `SMALL` 16 | every printed text; one font, one weight per style; the page stretches each text to the width the kit estimated (19, 14, 12, 10 du per character), so the font does not change the layout |

Also in the kit: a printed bracket over a group of parts (SOL, AUX on COMM) and a printed vertical rule (EXT / INTR LT).

**Rules**

- A part carries its own frame, cover and legend. A framed button is one part, a guarded part is one part (part plus cover), a hazard pad is sized from what is inside. Nothing is placed twice by hand.
- The same part is the same size everywhere, on every page and both seats. A page cannot change a size; at most it picks the variant. The kit refuses a control that already has `at`.
- Parts sit on a 1 du grid (whole-number centres); plate sizes are multiples of 2 du.
- **Plate:** one per panel (several for a `PanelGroup`, sharing a width or a common edge line, 16 du apart); corner radius 6, border 3. Content keeps at least 36 du from the plate edge and at least 12 du from every ear.
- **Ears and screws:** four identical `EAR` parts, one in each plate corner; one `SCREW_L` in the centre of each ear, so exactly 26 du from the two plate edges of its corner and all four corner screws share two x and two y values on every page. Edge screws (`SCREW_M`, `edge_screws`) and inner screws (`SCREW_S`, `Panel.screw`) exist but no page uses them; an inner screw is placed by naming two lines (plate lines `L`, `R`, `T`, `B`, `CX`, `CY`, corner screw lines, or the centre line of a placed part), never by free coordinates. The slot angle comes from a fixed list by position index (15, 100, 65, 140 degrees).
- **Labels** attach to a part by an anchor (`above`, `below`, `left`, `right`) with a fixed gap of 8 du (`Panel.label`). A free label (`Panel.mark`) needs a reason (titles, bracket text). The position labels of toggles, rotaries and knobs come from fixed presets in the kit.
- **Touch areas:** at least 56 px where the neighbours allow: the page widens a smaller area and cuts it back where two areas would overlap (the PULL chip has a 32 px floor, `CHIP_TOUCH_MIN`; the long press on its knob is the large target). A switch has one touch area and opens the chooser. Only a guarded switch has one band per position, under its cover, and the power levers one band per mark. There are no other invisible bands.
- **Knob look:** one drawing function (`knobFace`) and one set of gradient definitions (`knobDefs`) in the page draw every knob of a panel page: soft shadow, dark rim, a grip ring of 24 ridges, a cap with a highlight at the upper left, a raised pointer that turns by the control's `sweep`. A knob of 44 du radius or more gets a second rim. Two colourways: grey for the knobs, dark for the rotary selectors. MPD, TEDAC and KU knobs keep their CSS drawing.

**Page sizes (du).** TAIL WHEEL / NVS 600 × 224; EMERGENCY 580 × 276; STORES JETT 556 × 408; FIRE DET/EXTG 600 × 456; POWER 640 × 600 (pilot), 312 × 576 (CP/G, the two levers); EXT / INTR LT 612 × 456 (pilot), INTR LT 428 × 360 (CP/G); CMWS 616 × 552 (two plates: indicator 616 × 288, control panel 616 × 248); ARMAMENT 608 × 600 (pilot: ARMAMENT 352 × 244, MASTER ZEROIZE 240 × 244, VIDEO 608 × 340), 608 × 244 (CP/G, two plates); EUFD 640 × 524; CENTER 640 × 530 (three plates: CHK OVSP TEST and GEN RST 640 × 210, WINDSHIELD WIPER 376 × 304, PARK BRAKE and ALT SET 248 × 304); COMM 640 × 600; WIPER / DEFOG (CP/G) 376 × 304.

**Compile-time checks.** `Panel.build()` raises a `LayoutError` when the aircraft file is loaded and a page collides with itself; `Panel.check()` tests every page in du: collisions of parts, labels, touch squares, screws and printed lines, the 36 du plate margin and the 12 du clearance to the ears.

**Layout checker.** `core/tools/check_panels.js` measures the drawn pages in the browser. Paste it into the browser console of the open dashboard (or run it through a browser tool); it opens every page of the current seat from the long-hold page list and prints a JSON report with `pages`, `sizes`, `problems` and `info`. An empty `problems` is the acceptance. Run it in both seats at 1180 × 820 and 1024 × 768, with a reload after a resize. It reports:

- parts (body, frame, cover and pad together) overlapping each other or closer than 12 du to the plate edge or an ear; labels closer than 6 du to the plate edge or overlapping a part, label or screw; a guard cover that is not exactly the part (or its frame) + 12 du; a part kind (with frame and cover) drawn at different sizes on different pages of the seat; a page larger than 640 × 600 du;
- corner screws not in the centre of their ear or not on the two shared x and y lines; plates of one page not 16 du apart on a shared edge line; an inner or edge screw that shares no line with anything goes to `info`;
- a touch area under 56 px, or two touch areas overlapping by 6 px or more in both directions (guard covers, the APU flap, elements inside another, and the PULL chip floor of 32 px excepted).

## 8. The bridge interface

### Aircraft module

`core/dashboard.py` loads `aircraft/<name>.py` for the `[dcs] aircraft` setting. `aircraft/ah64d.py` provides:

| Name | Meaning |
| --- | --- |
| `DCSBIOS_MODULE` | the DCS-BIOS module name (`"AH-64D"`), used to find `AH-64D.json` |
| `KEYS` | the default keybinds (name → combo), see [section 3](#3-configuration); `[keys]` in `config/config.toml` overrides them |
| `VIEWS` | the list of views the bridge serves as `/layout` and checks commands against |
| `SEAT_NAMES` | seat number → id prefix: `{0: "PLT", 1: "CPG"}`; used for the `{seat}` placeholder |
| `CONTROL_NAMES` | the export script names of the control positions (`plt_cyc_pitch`, `plt_cyc_roll`, `plt_coll`, `plt_pedals`, `cpg_…`) |
| `MPD_INDICATIONS` | the export script indication numbers sent at 4 Hz: `(7, 9, 11, 13)` |
| `MPD_SEATS` | seat → (left, right) indication numbers: `{0: (7, 9), 1: (11, 13)}` |
| `TRIM_RELEASED` | the value of the force trim switch when released after a trim (`2`) |

**View.** `{"name", "seats": [0, 1], "lamps": [...], "controls": [...]}` plus, per layout: `"layout"` (`"map"`, `"panel"`, `"mpd"`, `"ku"`; omitted = the fixed grid of FLIGHT / FIGHT), `"links"` (COCKPIT map), and the panel fields of [section 7](#7-the-panel-kit). A lamp is `{"id", "label", "color", "button"?}` (`button` makes it a lighted push button).

**Control fields**

| Property | Meaning |
| --- | --- |
| `id` | DCS-BIOS identifier, `{seat}` / `{S}` for the seat; a key control uses a name from `[keys]` |
| `label` | placard text |
| `type` | `selector`, `button`, `lever`, `hat` (one or two axes: `ud`, `lr`), `knob`, `key`, `display`, `controls` (the trim display), `stick` (the cursor pad) |
| `positions` | list of `{value, label}`; `disabled` greys one out; `momentary` marks a spring-return position (for a hat: `{"up": label, ...}`) |
| `rest` | resting value of a spring-loaded switch; `hold` the press time in seconds |
| `lamp`, `legend`, `lamps` | lamp inside a button; `lamps` = two lamps on the face (`{id, color, legend}`: FIRE and RDY, ARM and SAFE) |
| `requires` | another control that must be in a position first (the APU cover): `{id, value}` |
| `seats` | `[0]` pilot, `[1]` CP/G, omitted = both |
| `grid`, `map` | position on a quick page / on the cockpit map |
| `guard`, `cover` | guarded control; the id of DCS's own cover control |
| `ids`, `page`, `pages` | `display` made of several DCS-BIOS strings (the 14 EUFD lines, the CMWS status); with `page` (the id of the page name) and `pages` (the ids shown for each name) |
| `step`, `step_fallback` | `knob`: step of an `up` / `down` command; selector: turn the knob with INC / DEC steps if the position is not reached |
| `readback`, `states`, `key` | `lever` / `key` controls: the DCS-BIOS id read back, the state names, the `[keys]` name |
| `side`, `slot`, `view` | MPD / TEDAC bezel controls and links |
| `style`, `shape`, `orient`, `sweep`, `angle`, `group`, `pull` | how the panel kit draws it: `rotary`, `cover`, `slider`, `cap`, `chip`, `plunger`, `flat`; `shape: "round"`; `orient: "h"`; knob pointer angles at min / max; angle per position of a rotary; dual-function knob members; the pull-to-disable id of a knob (it shows pulled out when it reads 1, a 0.6 s hold toggles it) |

Written by the kit for every control of a panel page (a page never types them): `at` (touch area `[x, y, w, h]` in du), `kit` (the part and the sizes), `cover_at` (box of the cover), `handle` (grip of the levers and FRICT, `[x, w, h]`), `knob` (`[cx, cy, r]` of a rotary), `mark` / `dot` (members of a dual-function knob), and `positions[].y` (where the lever grip stands).

**Seat placeholder.** Ids may contain `{seat}`. `/layout` serves them unexpanded and the page sends them unexpanded; the bridge expands them from the current seat before it reads or sends.

### Requests

- `GET /` → the page `core/web/index.html`; `GET /apple-touch-icon.png` → the home screen icon.
- `GET /layout` → `{"views": [{"name": "COCKPIT", "seats": [0, 1], "lamps": [...], "controls": [...], "links": [...]}, ...]}`.
- `GET /state` → `{"seat": 0, "age": 0.1, "values": {"PLT_MASTER_IGN_SW": 1, ...}, "controls": {...}, "controls_age": 0.1, "mpd_labels": {...}, "trim": {...}}`; `seat` is `null` before the first packet, `age` the seconds since the last DCS-BIOS packet. About 11 KB per reply with all panel controls.
- `POST /command` with `{"id": "PLT_MASTER_IGN_SW", "value": 1}`, `{"id": "power_left", "value": "FLY"}`, for a hat `{"id": "{seat}_WAS", "value": "up"}`, for a knob `{"value": 0..65535}` or `"up"` / `"down"`, for the cursor `{"x", "y"}`, for a cover `{"id": ..., "guard": "open"}` → `{"ok": true, "confirmed": true | false | null}` or HTTP 409 with `{"error": "..."}`.
- `GET /settings` → `{"logging": true, "saved_games": "...", "address": "http://<PC address>:8080"}`; `POST /settings` with `{"logging": false}` → the same JSON, or HTTP 400. Any other path is 404; a body that is not a JSON object is 400.

### Command checks and refusals

`/command` accepts only controls and positions from the view lists. It refuses (HTTP 409, the page shows the message briefly, the log gets a `refused` line):

| Error | Cause |
| --- | --- |
| `unknown control` | the id is in no view |
| `no DCS data` | no seat known yet |
| `CP/G seat: read only` / `pilot seat: read only` | the view or the control is outside the current seat |
| `display only` | a command for a display |
| `position not available` | a greyed position, an unknown label or an out-of-range knob value |
| `locked: open the cover first` | a `requires` control while its cover is closed (the APU button) |
| `guard closed` | a guarded control outside its 5 s window |
| `cover did not open` | DCS's own cover did not show open within 0.5 s |
| `not guarded` | `guard: open` for a control without `guard` |

New control types need page code only when the type itself is new; adding a view means adding a list.

### Log

The rolling log gets the start, every command with its result (source `dash`), every refusal, every error and the trim events (source `bridge` for start, stop, settings and bridge errors). Values are not logged. One line per event: time with milliseconds, source (7 characters), name (20 characters), text. The console prints the same lines with the time only.

```
2026-10-12 10:00:01.120 | dash    | PLT_MASTER_IGN_SW    | 1 sent
2026-10-12 10:00:05.300 | dash    | power_left           | FLY: keys idle, up
2026-10-12 10:00:09.010 | dash    | PLT_ROTOR_BRK        | 1 refused: position not available
2026-10-12 10:00:12.400 | dash    | PLT_FIRE_ENG1_BTN    | guard open
```

Refusal lines show the unexpanded `{seat}_...` id (cosmetic).

### Adding another aircraft

1. Add a file in `aircraft/` (lower case, letters and digits only) that provides the names of the table above: `DCSBIOS_MODULE`, `KEYS`, `VIEWS`, `SEAT_NAMES`, `CONTROL_NAMES`, `MPD_INDICATIONS`, `MPD_SEATS`, `TRIM_RELEASED`. Panel pages are written with `panel_kit` like `aircraft/ah64d.py`.
2. Set `aircraft = "<name>"` under `[dcs]` in `config/config.toml`.
3. The generic bridge and page stay free of aircraft knowledge, with these exceptions: the drawings of the MPD, TEDAC and KU in `core/web/index.html` and the control positions and MPD indication numbers in `core/lua/DCS-Dashboard-Export.lua` are still AH-64D-specific.

## 9. Manual test run

Preparation: DCS in windowed or borderless mode, DCS-BIOS and the export script installed, the default keybinds bound. PC and tablet on the same network. A throwaway AH-64D mission, cold and dark. Do the guarded controls last, because several cannot be undone in the mission.

1. **Start.** Run `start_dashboard.bat` (it starts `python core\dashboard.py` and prints the address to open). Open the address on the iPad and add it to the home screen. The badge shows `PILOT`; `NO DCS DATA` appears if DCS is not running.
2. **COCKPIT start-up sequence** (pilot seat, tablet only). POWER: MSTR IGN BATT, APU cover OPEN, APU, wait for APU ON, ENG 1 START, ENG 1 power lever IDLE, ENG 2 START, ENG 2 power lever IDLE, both power levers FLY. CENTER: PARK BRAKE IN. TAIL WHEEL / NVS: TAIL WHEEL once. Move a few switches in the cockpit with the mouse: the tablet follows.
3. **Pop-ups.** Chooser (NVS MODE, a squelch switch, ENG 1 START, the MSTR IGN dial, the wiper dial): it opens at the switch, shows the positions like the switch, lights the current one, marks the spring-return ones; a tap outside sends nothing. Knobs (EUFD BRT, a radio volume, a light knob): the bar opens next to the knob and the knob follows DCS. COMM: hold a volume knob for 0.6 s, the PULL chip toggles. Power levers and FRICT: tap each mark of both levers, drag the FRICT bar.
4. **Seat switch.** Switch to the CP/G seat (key `2`) while on a pilot-only page (for example CMWS): the page goes to the CP/G COCKPIT map, which has no CMWS, CENTER or EXT LT page. The badge shows `CP/G`. Switch back: the map shows the pilot pages.
5. **FIGHT** (both seats). A/S (the ARM and SAFE lamps change), GND ORIDE once, WAS and SIGHT SEL in each direction (the selection changes in the cockpit), FLARE and CHAFF once each (the counts change; the CMWS must be on and set up).
6. **Trim.** Hold the Force Trim switch and release it: the ring moves to the trim point and the log shows `PLT set`; press the trimmer reset key: `RESET`.
7. **MPD, KU, TEDAC.** MPD: press buttons on both displays; the live labels follow page changes; the cursor pad moves the cursor in the right direction; the MODE knob works (NT through the INC / DEC fallback). KU: type a few characters, the scratchpad shows them. CP/G seat: spot-check the TEDAC buttons, knobs and rockers.
8. **Guarded controls** (last). Station selects light their lamps and toggle back. ENG 1, APU and ENG 2 FIRE: lift the cover, tap once (RDY lamp on, fuel off), lift the cover again and tap again (safe); DCS's own cover opens with the tablet cover, and the log shows `cover open`, `pressed` and about 1 s later `cover closed`, without `not confirmed`. PRI and RES with a fire button armed, JETT with a station armed, ZEROIZE, MASTER ZEROIZE, CMWS JETT.

Done when a cold start to both power levers at FLY works from the tablet alone, the lamps match the cockpit, the CP/G seat shows only its own pages, and every control acts in both seats.

## 10. Future development and out of scope

**Future development: AI integration.** Not part of the product, and nothing in the dashboard depends on it. If the dashboard works well, an AI assistant (e.g. Claude) could later connect to the bridge through an MCP server. Ideas collected so far:

- Status advisor: reads cautions, lamps and flight and engine data, explains them and suggests next steps.
- Auto startup: runs a routine from cold and dark to ready for takeoff.
- Waypoint entry: enters a coordinate list into the TSD via the KU.
- George control on request.
- Each capability would be a use case with its own on / off toggle on the dashboard.

Other ideas: a WebSocket instead of polling if polling proves too slow; radios on the dashboard; grip controls with guards (CHOP, BUCS, emergency jettison) with the same guard mechanism.

**Out of scope:** AI integration (see above), multiplayer, automatic flying (stick, collective, pedals), cockpit-replica graphics, hardware panels, security beyond the local network.
