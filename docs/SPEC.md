# DCS-Dashboard – Spec

The specification of the product as built, for the engine that all aircraft share. The AH-64D is specified in [AH64D/SPEC.md](AH64D/SPEC.md), the A-10C II in [A10C/SPEC.md](A10C/SPEC.md). Open points and the fix log are in [FIXES.md](FIXES.md).

## 1. Purpose and principles

A self-made helper dashboard on a tablet (iPad) for aircraft in DCS World. It replaces keyboard combinations and mouse clicks for cockpit commands and shows the cockpit state. Flying itself stays on stick, collective and pedals. It is an open-source hobby project.

Aircraft: the AH-64D (pilot and CP/G seat) is mature and tested, see [AH64D/SPEC.md](AH64D/SPEC.md); the A-10C II is under development (built except its keypress controls, tested only against a simulated DCS-BIOS), see [A10C/SPEC.md](A10C/SPEC.md). The bridge serves the aircraft that DCS reports, see [Several aircraft](#9-several-aircraft). For the AH-64D the dashboard shows a COCKPIT map with one page per cockpit panel, quick pages for flight and fight, both MPDs, the TEDAC, the KU and direct buttons for George, the AI crew member.

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
| Aircraft | One file per aircraft in `aircraft/`, see [section 8](#8-the-bridge-interface); AH-64D mature and tested (pilot and CP/G seat), A-10C II under development (built except its keypress controls); the bridge follows the aircraft DCS reports |
| Game mode | Single player only |
| Platform | DCS World on Windows (Steam or standalone), Python 3.12 or newer; tablet and PC share the local network |
| Language | Python for the bridge; plain HTML, CSS and JavaScript for the dashboard (no framework, no external files); Lua only for the small DCS-side export script |
| Code | Public GitHub repo `DCS-Dashboard`, only the main branch; usable by anyone |
| Dashboard | One HTML page served by the bridge, used in a tablet browser over the local network, no login |
| Debug log | Rolling log file with a size limit: 5 MB per file, the last 3 files kept, about 15 MB in total |
| AI | Not part of the product (George, the game's own AI crew member, is an AH-64D feature and has buttons on its GEORGE tab, see [AH64D/SPEC.md](AH64D/SPEC.md#george)); see [section 11](#11-future-development-and-out-of-scope) |

## 2. Repository layout and architecture

```
start_dashboard.bat        starts `core\dashboard.py` with `python` (or `py -3`), keeps the window open on an error
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
    test/                  developer test kit (test bridge with a fake keyboard, DCS-BIOS simulator, page checks; see its README.md)
aircraft/ah64d.py          all AH-64D data: views, controls, labels, MPD indications, trim data, default keybinds
aircraft/a10c.py           all A-10C II data: panel pages, views, controls, labels
config/                    config.example.toml (tracked); config.toml (optional, ignored: machine settings and
                           keybind overrides); settings.json (ignored: logging switch, last detected aircraft)
logs/                      generated at runtime (ignored)
docs/                      SPEC.md (this spec: the engine) and FIXES.md (a temporary working note)
  AH64D/                   SPEC.md (the AH-64D spec)
  A10C/                    the A-10C II spec, engine changes, research notes and reference data
```

```
DCS World · AH-64D (example; gaming PC)
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
- **The view is data.** The controls of each view are one Python list in the aircraft file (`aircraft/ah64d.py`, `aircraft/a10c.py`), served as `/layout`. The page draws whatever the lists contain. The panel pages of the COCKPIT tab are written by the panel kit (`core/panel_kit.py`, [section 7](#7-the-panel-kit)): the aircraft file names a part and its centre, the kit gives it its standard size, places the labels, adds the plate and screws, and writes the page data.
- **The tablet shows the cockpit, not the last tap.** Every control shows the position read back from DCS. A switch moved in the cockpit with the mouse moves on the tablet too.
- **Local network only, no login.** The server listens on `[dashboard] host` and `port` (default `0.0.0.0:8080`). On start it prints the address to open, for example `http://<PC address>:8080`.

## 3. Configuration

`config/config.toml` is optional. Without it the dashboard runs with the built-in defaults (`DEFAULTS` in `core/config.py`). To change something, copy `config/config.example.toml` to `config/config.toml` and keep only the lines to change; sections are merged key by key over the defaults. Environment variables like `%USERPROFILE%` are expanded in `saved_games`.

| Section / key | Default | Meaning |
| --- | --- | --- |
| `[dcs] saved_games` | `"auto"` | DCS Saved Games folder. `auto` asks Windows for the Saved Games folder and uses `DCS` or `DCS.openbeta`, whichever has DCS-BIOS installed (`Scripts/DCS-BIOS`). If none is found the bridge stops and asks for the setting |
| `[dcs] window_title` | `"Digital Combat Simulator"` | Part of the DCS window title; the bridge brings that window to the front before a keypress |
| `[dcs] aircraft` | `"auto"` | `"auto"` follows the aircraft that DCS-BIOS reports ([section 9](#9-several-aircraft)). A name (`"AH-64D"`, `"A-10C"`) forces that aircraft; case and punctuation do not matter |
| `[dcs_bios] export_multicast`, `export_port` | `239.255.50.10`, `5010` | DCS-BIOS stream (UDP multicast) |
| `[dcs_bios] command_port` | `7778` | DCS-BIOS commands (UDP to 127.0.0.1) |
| `[export] port` | `7790` | UDP port the export script sends to; must match `PORT` in `core/lua/DCS-Dashboard-Export.lua` |
| `[dashboard] host`, `port` | `0.0.0.0`, `8080` | Web server for the tablet |
| `[dashboard] macro_pause_scale` | `1.0` | Multiplies the pauses between the key presses of the GEORGE buttons of the AH-64D ([GEORGE](AH64D/SPEC.md#george)); raise it (1.5, 2) if DCS misses keys |
| `[log] file`, `max_mb`, `backups` | `logs/dcs-dashboard.log`, 5, 2 | Rolling log: the active file plus 2 backups of 5 MB, about 15 MB in total |
| `[keys]` | from the aircraft file | Overrides of the default keybinds, per key |

- **Keybinds.** The default DCS keybinds sent as keypresses are in `KEYS` in the aircraft file (`aircraft/ah64d.py` for the AH-64D). A `[keys]` line in `config/config.toml` overrides one key; the others stay. Format: modifiers and key joined by `+`. Supported modifiers: `LCtrl` `RCtrl` `LShift` `RShift` `LAlt` `RAlt` `LWin`; keys `A`–`Z`, `0`–`9`, `F1`–`F12`, `Home` `End` `PageUp` `PageDown` `Insert` `Delete`, `Up` `Down` `Left` `Right`, `Space`, `Enter`. The bridge checks all keys it needs at start and stops with a message if one is missing or invalid. The default keys of the AH-64D are in [Keybinds](AH64D/SPEC.md#3-keybinds).
- **settings.json.** `config/settings.json` (ignored) holds the LOGGING switch of the settings page ([section 5](#5-dashboard-design-rules-seat-handling-settings)) and the last detected aircraft (`aircraft`), which is the start aircraft until DCS reports one. The AIRCRAFT switch of the settings page is not saved. The file is created by the bridge, not edited by hand.
- **DCS side.** DCS-BIOS (DCS-Skunkworks fork) is installed in Saved Games, and DCS has the module of each aircraft you fly. The bridge reads the control list of every aircraft file (`<Saved Games>/Scripts/DCS-BIOS/doc/json/<DCSBIOS_MODULE>.json`, for example `AH-64D.json`) and `MetadataStart.json`, which holds the aircraft name `_ACFT_NAME`. If a file is missing the bridge stops and names the path. An aircraft whose file uses an id that is not in its control list is left out and logged (`aircraft | <name> not available, not in DCS-BIOS: ...`); the bridge stops only when no aircraft is left. The export script `core/lua/DCS-Dashboard-Export.lua` is copied to `<Saved Games>/Scripts/` and loaded by one line at the end of `Export.lua`, after the DCS-BIOS line: `dofile(lfs.writedir() .. [[Scripts\DCS-Dashboard-Export.lua]])`. At start the bridge compares the installed copy with the repo copy (line endings ignored) and checks that `Export.lua` names it; it logs `export script | not installed`, `outdated` or `not loaded` and keeps running. After an update of the repo, copy the script again: the script now holds one table per aircraft, and a copy of an older version is `outdated`. The default keybinds must be bound in the DCS controls settings (the standard AH-64D bindings); for the AH-64D the `george_*` keys are not DCS defaults and must be added once, see [GEORGE](AH64D/SPEC.md#george). DCS should run in windowed or borderless mode so that bringing it to the front works. Windows may ask to allow Python on the network: allow it for private networks.

## 4. What DCS allows

The generic findings of the research phase. The results for the AH-64D are in [What DCS allows for the AH-64D](AH64D/SPEC.md#4-what-dcs-allows-for-the-ah-64d).

### Reading

- **DCS-BIOS** (multicast stream) delivers switch positions, button states, lamps, levers and text; what it delivers for the AH-64D is listed in the AH-64D spec.
- DCS-BIOS stream format: each UDP packet starts with the sync bytes `55 55 55 55`, followed by blocks of address (uint16 LE), length (uint16 LE) and data. The bridge keeps a 64 KB memory image and reads the outputs it needs from it: integers as `(word at address & mask) >> shift_by`, strings as `max_length` bytes decoded as latin-1 with trailing NUL bytes removed. Strings arrive in pieces for the first 15 seconds or so.
- **Export script** (Lua, runs inside DCS next to DCS-BIOS, sends UDP to `127.0.0.1`; every call is wrapped in `pcall`, and it chains the existing export hooks so DCS-BIOS keeps working). It sends plain text, one `name=value` per line, from one table per aircraft name (`LoGetSelfData().Name`); nothing is sent for an aircraft that is not in the table, and the table of the A-10C II is empty. What it sends for the AH-64D is listed in the AH-64D spec.

### Controlling

- **DCS-BIOS commands** (UDP to 127.0.0.1, one line per command, `IDENTIFIER VALUE`, for example `PLT_MASTER_IGN_SW 1` in the AH-64D) work for most cockpit controls and have a readback.
- **Keypresses** are needed for what DCS-BIOS cannot do. DCS reads the keyboard through scan codes, so keys are sent with `SendInput` and `KEYEVENTF_SCANCODE` (`ctypes`, standard library). Before a key the bridge taps LShift and brings the DCS window to the front (Windows only lets a background program change the active window right after it sent input; LAlt would put the window into menu mode), then waits 0.3 s. This worked every time. If the window does not come to the front no key is sent.
- **Cockpit logic still applies.** A command that the cockpit would not accept fails without an error.

### Blocklist idea

Dangerous or irreversible controls are never part of a sweep or a quick page: for the AH-64D every identifier containing `JETT`, `FIRE_ENG`, `FIRE_APU`, `FIRE_PRIME`, `FIRE_RES`, `ZERO`, `CHOP`, `BUCS` or `TRIGGER` (jettison, fire buttons and extinguishers, zeroize, CHOP, BUCS, weapons trigger, M4 trigger, with their covers). On the dashboard these controls exist only on their own COCKPIT panel page, behind a guard ([AH-64D, Guarded controls](AH64D/SPEC.md#guarded-controls)); the grip controls with guards (CHOP, BUCS, emergency jettison, weapons trigger) are not on the dashboard at all.

## 5. Dashboard design rules, seat handling, settings

### Design rules

- **Cockpit names and positions.** Every control uses the label printed in the cockpit and shows all of its real positions, in cockpit order, even positions we do not use. A position that cannot be set is greyed out and cannot be selected.
- **Big touch targets:** 56 CSS pixels where space allows; at least 44 px on the three-row FLIGHT view and as on the real bezel on the MPD view (about 0.7 of the button spacing).
- **Landscape first.** Designed for an iPad Air in landscape (1180 × 820 CSS pixels), laid out with a CSS grid that also fits other tablets from about 1024 × 768 up. Portrait works but is not optimised. Smaller screens overlap.
- **Plain look.** Dark background, white stencil-style labels, lamp colours as in the cockpit. The panel pages need CSS container queries: Safari / iPadOS 16 or newer, or current Chrome.
- **No emoji-capable code points** in the UI or the aircraft file (they are drawn as coloured emoji on iOS). Arrows, chevrons, the close cross and the spring mark are inline SVG from one small icon set (`ICONS` in `core/web/index.html`: `chev-left`, `close`, `tri-up`, `tri-down`, `tri-left`, `tri-right`, `spring`).

### Seat

Seats are defined per aircraft (`SEATS` in the aircraft file, served in `/layout`). The two-seat handling of the AH-64D (PILOT / CP/G, the debug seat) is in [Seats](AH64D/SPEC.md#1-seats) of its spec. An aircraft with one seat, like the A-10C II, has no seat switch and no debug seat; the badge shows the aircraft. See [Several aircraft](#9-several-aircraft).

### Settings and page lock

- A small gear button at the bottom right opens a settings page over the dashboard; `BACK` closes it. A free strip at the bottom of the controls keeps the gear clear of every control.
- **LOGGING** OFF / ON switches writing `logs/dcs-dashboard.log` on the PC (the console output stays). Saved in `config/settings.json`, applied immediately and kept across restarts.
- **KEEP SCREEN ON** OFF / ON uses the browser's screen wake lock, for this tablet only (stored in the browser).
- **AIRCRAFT** AUTO / one button per aircraft (the names come from the bridge): AUTO follows the aircraft DCS reports, a button forces that aircraft until set back to AUTO or the bridge restarts. It is not saved. The text below shows the aircraft detected in DCS and the active one.
- **INFO** shows the DCS Saved Games folder the bridge uses, the DCS data status and the address to open on another tablet.
- The page is locked for use as a home screen app: no scrolling, no rubber-band bounce, no pinch or double-tap zoom, no text selection or long-press menu. Rotation cannot be locked from a web page on iOS: use the iPad's rotation lock; in portrait a full-screen hint asks to turn the iPad.
- Home screen icon `core/web/apple-touch-icon.png` (180 × 180, "DCS" / "Dashboard", white on grey), name "DCS Dashboard".

### Confirmed presses

The bridge checks DCS-BIOS after sending: a push button is held until DCS reports it pressed (at least 0.3 s, at most 1 s) and then released; a hat is held until its axis shows the direction; a selector until the readback shows the new position (up to 0.5 s). The reply is `{"ok": true, "confirmed": true | false | null}` (`null` = not checked: knobs, the cursor and TKR pads, keypresses). The log says `pressed, not confirmed` / `sent, not confirmed`, and the page shows an amber note `<label>: not confirmed by DCS` with a short amber flash on the control. Lost presses come from presses of only one DCS frame, commands waiting behind a slow power lever sequence, keypresses when DCS cannot be brought to the front, and double taps on toggle buttons.

## 6. Views

A view is one entry of the `VIEWS` list of the aircraft file ([section 8](#8-the-bridge-interface)). The tab bar has one tab per view name, and a tab opens the view of that name for the current seat. The `layout` of a view tells the page how to draw it: `map` (a cockpit map whose boxes open the panel pages), `panel` (one cockpit panel drawn by the panel kit, [section 7](#7-the-panel-kit)), `mpd` (a display bezel with its buttons and live labels), `ku` (a keyboard unit drawn 1:1 after a photo), `mfcd` (the A-10C II MFCD bezel, one side at a time) and `cdu` (the A-10C II CDU and UFC, one at a time); without a `layout` the page draws the fixed grid of buttons, lamps and displays of the quick pages. The views of the AH-64D are described in [The views](AH64D/SPEC.md#2-the-views) of its spec, those of the A-10C II in [A10C/SPEC.md](A10C/SPEC.md).

## 7. The panel kit

`core/panel_kit.py` is a small layout compiler. A page entry names a part and a centre point, never a size; the compiler writes the resolved geometry (boxes in du, label positions, plate, ears, screws) into the page data in the format the page already draws. The page draws what it is given and has no hard-coded sizes. The photos only say what is on a panel, its text and the arrangement of the parts, not pixel sizes.

**Design units and one scale.** All panel geometry is in design units (du); one du is the same size on every page. Every page is drawn at the same scale `S = min(area width / 640, area height / 600)`, at most 1.6, for both seats: 1.045 at 1180 × 820, 0.958 at 1024 × 768 (the app area is about 627 px and 575 px high). 640 × 600 du is a fixed budget (POWER and COMM use all of it); a larger page is a layout error (exception: a scroll page, see below). A part of 56 du is 58.5 px at the first and 53.7 px at the second size.

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
| `EAR` | rectangular corner ear 52 × 52, flush in the plate corner, 2 border | the four corners of every plate with the look `ah64d` |
| `SCREW_L` / `_M` / `_S` | diameter 26 / 18 / 12 | `SCREW_L` centred in each ear |
| `DZUS` | fastener, diameter 24, centre 22 from both edges of its corner | the four corners of every plate with the look `a10c`, instead of ears and screws |
| `LAMP` / `LAMP_WIDE` | 72 × 40 / 136 × 40 | legend lamps without a touch target (`Panel.lamp`): text on the lamp face, at most two lines, colour green, amber, red or white; it lights while its DCS-BIOS output is above 0 |
| `BAR` | 40 × 200 | read-only vertical bar (`Panel.bar`): track, fill from the bottom, percentage below; no touch action |
| Label styles | `TITLE` 32, `NAME` 24, `POS` 20, `SMALL` 16 | every printed text; one font, one weight per style; the page stretches each text to the width the kit estimated (19, 14, 12, 10 du per character), so the font does not change the layout |

Also in the kit: a printed bracket over a group of parts (SOL, AUX on COMM) and a printed vertical rule (EXT / INTR LT). A push button can be lit in green, amber, red or white.

**Looks.** `Panel(..., look=...)` and `PanelGroup(..., look=...)` choose the plate style for every plate of the page: `"ah64d"` (default: four ears with a screw each) or `"a10c"` (four Dzus fasteners, no ears). The look changes only the drawing of the plate corners; parts, touch areas and layout rules are the same.

**Scroll pages.** `Panel(..., scroll=True)` and `PanelGroup(..., scroll=True)` allow a page taller than 600 du, up to `SCROLL_MAX` (1800 du); `build()` then adds `"scroll": True` to the page data. The page keeps the width of 640 du and the scale of every page, so parts stay the same size. Only the plate area scrolls vertically; the tabs, the lamp row and the settings button stay fixed. The scroll area has a visible frame, its own scroll bar at the right edge (iPadOS hides the browser's own) and a shaded edge with a chevron where more of the page is hidden. A touch that moves is a scroll and never a tap, a hold or a knob turn. A scroll page opens at the top. Every other page keeps the 640 × 600 du budget. The layout checker allows 1800 du for a scroll page.

**Rules**

- A part carries its own frame, cover and legend. A framed button is one part, a guarded part is one part (part plus cover), a hazard pad is sized from what is inside. Nothing is placed twice by hand.
- The same part is the same size everywhere, on every page and both seats. A page cannot change a size; at most it picks the variant. The kit refuses a control that already has `at`.
- Parts sit on a 1 du grid (whole-number centres); plate sizes are multiples of 2 du.
- **Plate:** one per panel (several for a `PanelGroup`, sharing a width or a common edge line, 16 du apart); corner radius 6, border 3. Content keeps at least 36 du from the plate edge and at least 12 du from every ear.
- **Ears and screws:** four identical `EAR` parts, one in each plate corner; one `SCREW_L` in the centre of each ear, so exactly 26 du from the two plate edges of its corner and all four corner screws share two x and two y values on every page. Edge screws (`SCREW_M`, `edge_screws`) and inner screws (`SCREW_S`, `Panel.screw`) exist but no page uses them; an inner screw is placed by naming two lines (plate lines `L`, `R`, `T`, `B`, `CX`, `CY`, corner screw lines, or the centre line of a placed part), never by free coordinates. The slot angle comes from a fixed list by position index (15, 100, 65, 140 degrees).
- **Labels** attach to a part by an anchor (`above`, `below`, `left`, `right`) with a fixed gap of 8 du (`Panel.label`). A free label (`Panel.mark`) needs a reason (titles, bracket text). The position labels of toggles, rotaries and knobs come from fixed presets in the kit.
- **Touch areas:** at least 56 px where the neighbours allow: the page widens a smaller area and cuts it back where two areas would overlap (the PULL chip has a 32 px floor, `CHIP_TOUCH_MIN`; the long press on its knob is the large target). A switch has one touch area and opens the chooser. Only a guarded switch has one band per position, under its cover, and the power levers one band per mark. There are no other invisible bands.
- **Knob look:** one drawing function (`knobFace`) and one set of gradient definitions (`knobDefs`) in the page draw every knob of a panel page: soft shadow, dark rim, a grip ring of 24 ridges, a cap with a highlight at the upper left, a raised pointer that turns by the control's `sweep`. A knob of 44 du radius or more gets a second rim. Two colourways: grey for the knobs, dark for the rotary selectors. MPD, TEDAC and KU knobs keep their CSS drawing.

**Page sizes (du).** The sizes below are those of the AH-64D; the A-10C II pages are in [A10C/SPEC.md](A10C/SPEC.md). TAIL WHEEL / NVS 600 × 224; EMERGENCY 580 × 276; STORES JETT 556 × 408; FIRE DET/EXTG 600 × 456; POWER 640 × 600 (pilot), 312 × 576 (CP/G, the two levers); EXT / INTR LT 612 × 456 (pilot), INTR LT 428 × 360 (CP/G); CMWS 616 × 552 (two plates: indicator 616 × 288, control panel 616 × 248); ARMAMENT 608 × 600 (pilot: ARMAMENT 352 × 244, MASTER ZEROIZE 240 × 244, VIDEO 608 × 340), 608 × 244 (CP/G, two plates); EUFD 640 × 524; CENTER 640 × 530 (three plates: CHK OVSP TEST and GEN RST 640 × 210, WINDSHIELD WIPER 376 × 304, PARK BRAKE and ALT SET 248 × 304); COMM 640 × 600; WIPER / DEFOG (CP/G) 376 × 304.

**Compile-time checks.** `Panel.build()` raises a `LayoutError` when the aircraft file is loaded and a page collides with itself; `Panel.check()` tests every page in du: collisions of parts, labels, touch squares, screws and printed lines, the 36 du plate margin and the 12 du clearance to the ears.

**Layout checker.** `core/tools/check_panels.js` measures the drawn pages in the browser. Paste it into the browser console of the open dashboard (or run it through a browser tool); it opens every page of the current seat from the long-hold page list and prints a JSON report with `pages`, `sizes`, `problems` and `info`. An empty `problems` is the acceptance. Run it in both seats at 1180 × 820 and 1024 × 768, with a reload after a resize. It reports:

- parts (body, frame, cover and pad together) overlapping each other or closer than 12 du to the plate edge or an ear; labels closer than 6 du to the plate edge or overlapping a part, label or screw; a guard cover that is not exactly the part (or its frame) + 12 du; a part kind (with frame and cover) drawn at different sizes on different pages of the seat; a page larger than 640 × 600 du (1800 du tall for a scroll page);
- corner screws not in the centre of their ear or not on the two shared x and y lines (for the look `a10c`: a Dzus fastener not centred 22 du from the two edges of its corner); plates of one page not 16 du apart on a shared edge line; an inner or edge screw that shares no line with anything goes to `info`;
- a touch area under 56 px, or two touch areas overlapping by 6 px or more in both directions (guard covers, the APU flap, elements inside another, and the PULL chip floor of 32 px excepted).


## 8. The bridge interface

### Aircraft module

`core/dashboard.py` loads every file in `aircraft/` at start ([section 9](#9-several-aircraft)). An aircraft file provides:

| Name | Meaning |
| --- | --- |
| `NAME` | the aircraft name: the value of `[dcs] aircraft`, the name on the settings page, in `/layout` and in the remembered tab (`"AH-64D"`, `"A-10C"`) |
| `DCS_NAMES` | the names DCS-BIOS reports in `_ACFT_NAME` for this aircraft (`["AH-64D_BLK_II"]`, `["A-10C_2"]`) |
| `DCSBIOS_MODULE` | the DCS-BIOS module name (`"AH-64D"`, `"A-10C"`), used to find `<module>.json` |
| `SEATS` | the seats, a list of `{"prefix", "label"}`: the prefix replaces `{seat}` in ids, the label is the badge text (`PLT` / `PILOT`, `CPG` / `CP/G`; the A-10C II has one seat with the prefix `""` and the label `A-10C`) |
| `SEAT_OUTPUT` | the DCS-BIOS output that holds the current seat (`"SEAT_POSITION"`); `None` for one seat: the seat is 0 as soon as DCS-BIOS data arrives |
| `TRIM_SWITCH` | the force trim switch id with `{seat}`, or `None` for an aircraft without a trim display (no trim tracking, no `trim_reset` key) |
| `TRIM_RELEASED` | the value of the force trim switch when released after a trim (`2`); `None` without a trim display |
| `KEYS` | the default keybinds (name → combo), see [section 3](#3-configuration); `[keys]` in `config/config.toml` overrides them. The bridge requires only the keys the aircraft's controls use: the lever keys (`power_*`) only for `lever` controls, `trim_reset` only with a `TRIM_SWITCH` |
| `VIEWS` | the list of views the bridge serves as `/layout` and checks commands against |
| `CONTROL_NAMES` | the export script names of the control positions (`plt_cyc_pitch`, `plt_cyc_roll`, `plt_coll`, `plt_pedals`, `cpg_…`); empty for the A-10C II |
| `MPD_INDICATIONS` | the export script indication numbers sent at 4 Hz: `(7, 9, 11, 13)`; empty for the A-10C II |
| `MPD_SEATS` | seat → (left, right) indication numbers: `{0: (7, 9), 1: (11, 13)}`; empty for the A-10C II |

**View.** `{"name", "seats": [0, 1], "lamps": [...], "controls": [...]}` (a name may occur once per seat, as FIGHT: the page has one tab per name and opens the view whose `seats` contain the current seat) plus, per layout: `"layout"` (`"map"`, `"panel"`, `"mpd"`, `"ku"`, `"mfcd"`, `"cdu"`; omitted = the fixed grid of FLIGHT / FIGHT), `"links"` (COCKPIT map), and the panel fields of [section 7](#7-the-panel-kit) (`"scroll": True` for a scroll page). A lamp is `{"id", "label", "color", "button"?}` (`button` makes it a lighted push button).

**Control fields**

| Property | Meaning |
| --- | --- |
| `id` | DCS-BIOS identifier, `{seat}` / `{S}` for the seat; a key control uses a name from `[keys]` |
| `label` | placard text |
| `type` | `selector`, `button`, `lever`, `hat` (one or two axes: `ud`, `lr`; or a step rocker or key hat, see below), `knob`, `key`, `macro`, `display`, `bar` (read only), `controls` (the trim display), `stick` (the cursor pad and the TKR pad) |
| `positions` | list of `{value, label}`; `disabled` greys one out; `momentary` marks a spring-return position (for a hat: `{"up": label, ...}`) |
| `max` | `bar`: the value that fills the bar; the bar shows the output read from DCS-BIOS as a share of `max`, with the percentage as text. It takes no command (`display only`) |
| `steps` (hat) | step rocker: a `hat` with `ud` and `steps` for a dial that has no absolute DCS-BIOS input. `"fixed"` sends `INC` for up and `DEC` for down; a number sends `+N` / `-N`. The step is not read back, so the rocker has no state and the bridge reads no output for it |
| `keys`, `long` | key hat: a `hat` with `keys`, a map from each direction (`up`, `down`, `left`, `right`, optional `press` for the centre) to a `[keys]` name. A tap sends a short press (`KEY_SHORT`, 0.15 s); a hold of 0.6 s on the tablet sends the long press (`KEY_LONG`, the key held 1.0 s), with the request `{"id", "value", "long": true}`. `long` is an optional map from direction to a small label for the long function; only a direction in `long` accepts a long press. Not read back (`confirmed: null`) |
| `rest` | resting value of a spring-loaded switch, or the level a `button` returns to on release (default 0); `hold` the press time in seconds |
| `bios`, `value` | `button`: the DCS-BIOS control it acts on (default the control's `id`) and the level sent while it is pressed (default 1). Together with `rest` this makes several buttons of one multi-position switch: IAT (`value` 2), OFS and OFS ALL (`value` 0, `rest` 1), all on `CPG_LHG_TEDAC_L_IAT`. The press is confirmed against `bios` and `value`, and the bridge holds it at least 0.3 s (`PRESS_MIN`), at most 1 s |
| `digital` | `stick`: the pad sends 2 / 0 / 1 per axis instead of the analog range 0 to 65535: 2 above a dead zone of 30 % of the full deflection (`STICK_DIGITAL`), 0 below minus 30 %, else 1; only changes are sent (the TKR pad) |
| `lamp`, `legend`, `lamps` | lamp inside a button; `lamps` = two lamps on the face (`{id, color, legend}`: FIRE and RDY, ARM and SAFE) |
| `requires` | another control that must be in a position first (the APU cover): `{id, value}` |
| `seats` | `[0]` pilot, `[1]` CP/G, omitted = both |
| `grid`, `map` | position on a quick page / on the cockpit map |
| `guard`, `cover` | guarded control; the id of DCS's own cover control |
| `ids`, `page`, `pages` | `display` made of several DCS-BIOS strings (the 14 EUFD lines, the CMWS status); with `page` (the id of the page name) and `pages` (the ids shown for each name) |
| `step`, `step_fallback` | `knob`: step of an `up` / `down` command; selector: turn the knob with INC / DEC steps if the position is not reached |
| `readback`, `states`, `key` | `lever` / `key` controls: the DCS-BIOS id read back, the state names, the `[keys]` name |
| `steps` (macro) | `macro`: the key sequence, a list of `[key name, hold seconds, pause after seconds]`, key names from `[keys]` |
| `side`, `slot`, `view` | MPD / TEDAC bezel controls and links |
| `style`, `shape`, `orient`, `sweep`, `angle`, `group`, `pull` | how the panel kit draws it: `rotary`, `cover`, `slider`, `cap`, `chip`, `plunger`, `flat`; `shape: "round"`; `orient: "h"`; knob pointer angles at min / max; angle per position of a rotary; dual-function knob members; the pull-to-disable id of a knob (it shows pulled out when it reads 1, a 0.6 s hold toggles it) |

Written by the kit for every control of a panel page (a page never types them): `at` (touch area `[x, y, w, h]` in du), `kit` (the part and the sizes), `cover_at` (box of the cover), `handle` (grip of the levers and FRICT, `[x, w, h]`), `knob` (`[cx, cy, r]` of a rotary), `mark` / `dot` (members of a dual-function knob), and `positions[].y` (where the lever grip stands).

**Seat placeholder.** Ids may contain `{seat}`. `/layout` serves them unexpanded and the page sends them unexpanded; the bridge expands them with the `prefix` of the current seat before it reads or sends. An aircraft with one seat uses ids without `{seat}`.

### Requests

- `GET /` → the page `core/web/index.html`; `GET /apple-touch-icon.png` → the home screen icon.
- `GET /layout` → `{"aircraft": "AH-64D", "seats": [{"prefix": "PLT", "label": "PILOT"}, ...], "views": [{"name": "COCKPIT", "seats": [0, 1], "lamps": [...], "controls": [...], "links": [...]}, ...]}` for the active aircraft.
- `GET /state` → `{"aircraft": "AH-64D", "detected": "AH-64D_BLK_II", "seat": 0, "age": 0.1, "values": {"PLT_MASTER_IGN_SW": 1, ...}, "controls": {...}, "controls_age": 0.1, "mpd_labels": {...}, "trim": {...}}`; `aircraft` is the active aircraft, `detected` the name DCS-BIOS reports (`null` before the first packet), `seat` is `null` before the first packet, `age` the seconds since the last DCS-BIOS packet. About 11 KB per reply with all panel controls. The page polls `/state` and reloads itself when `aircraft` differs from the aircraft of its layout.
- `POST /command` with `{"id": "PLT_MASTER_IGN_SW", "value": 1}`, `{"id": "power_left", "value": "FLY"}`, for a hat `{"id": "{seat}_WAS", "value": "up"}`, for a key hat `{"id": ..., "value": "up", "long": true}` (without `long` for a tap), for a knob `{"value": 0..65535}` or `"up"` / `"down"`, for the cursor and the TKR pad `{"x", "y"}` (−1..1), for a cover `{"id": ..., "guard": "open"}` → `{"ok": true, "confirmed": true | false | null}` or HTTP 409 with `{"error": "..."}`.
- `GET /settings` → `{"logging": true, "aircraft": "AH-64D", "aircraft_mode": "auto", "aircraft_names": ["A-10C", "AH-64D"], "detected": "AH-64D_BLK_II", "saved_games": "...", "address": "http://<PC address>:8080"}`; `aircraft` is the active aircraft, `aircraft_mode` `"auto"` or the forced aircraft. `POST /settings` with `{"logging": false}` or `{"aircraft": "auto"}` / `{"aircraft": "<NAME>"}` (or both) → the same JSON, or HTTP 400 for an unknown aircraft name. Any other path is 404; a body that is not a JSON object is 400.

### Command checks and refusals

`/command` accepts only controls and positions from the view lists. It refuses (HTTP 409, the page shows the message briefly, the log gets a `refused` line):

| Error | Cause |
| --- | --- |
| `unknown control` | the id is in no view |
| `no DCS data` | no seat known yet |
| `CP/G seat: read only` / `pilot seat: read only` (the seat label) | the view or the control is outside the current seat |
| `display only` | a command for a display or a bar |
| `position not available` | a greyed position, an unknown label or an out-of-range knob value |
| `locked: open the cover first` | a `requires` control while its cover is closed (the APU button) |
| `guard closed` | a guarded control outside its 5 s window |
| `cover did not open` | DCS's own cover did not show open within 0.5 s |
| `not guarded` | `guard: open` for a control without `guard` |

**Macro controls.** A `macro` control (the GEORGE buttons) sends a fixed key sequence: `steps` is a list of `[key name, hold seconds, pause after seconds]`, the key names come from `[keys]`. `/command` brings the DCS window to the front once (`DCS not in front` and no key if that fails), then presses the steps in order under the command lock, with the modifiers and the main key staggered by 40 ms (`MACRO_KEY_GAP`), sleeping the pause after each step when it is above 0. The pause is multiplied by `[dashboard] macro_pause_scale` (default 1.0). It logs one line per step before pressing it (`step <key name> hold <s> pause <s>`, the scaled pause) and `pressed` at the end, and answers `{"ok": true, "confirmed": null}` (keypresses are not checked). `seats` and `grid` work as for other controls, and the refusals are the same as for a `key` control. At start the bridge checks the key of every step and stops with `Invalid <key> key in [keys] of config/config.toml, see config/config.example.toml.` if one is missing or invalid.

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

1. Add a file in `aircraft/` (lower case, letters and digits only) that provides the names of the table above: `NAME`, `DCS_NAMES`, `DCSBIOS_MODULE`, `SEATS`, `SEAT_OUTPUT`, `TRIM_SWITCH`, `TRIM_RELEASED`, `KEYS`, `VIEWS`, `CONTROL_NAMES`, `MPD_INDICATIONS`, `MPD_SEATS`. Panel pages are written with `panel_kit` like `aircraft/ah64d.py` and `aircraft/a10c.py`.
2. Nothing else to set: the bridge loads every file in `aircraft/` and follows the aircraft DCS-BIOS reports. `aircraft = "<NAME>"` under `[dcs]` in `config/config.toml` forces one.
3. The generic bridge and page stay free of aircraft knowledge, with these exceptions: the drawings of the MPD, TEDAC and KU (AH-64D) and of the MFCD, CDU and UFC (A-10C II) in `core/web/index.html`, and the tables of control positions and MPD indication numbers per aircraft name in `core/lua/DCS-Dashboard-Export.lua`.

## 9. Several aircraft

One running bridge serves every aircraft file in `aircraft/`. The decisions behind it are in [A10C/ENGINE.md](A10C/ENGINE.md) (E1 to E10); this section describes what is built.

- **Aircraft choice.** The bridge loads every file in `aircraft/` at start and reads the DCS-BIOS aircraft name `_ACFT_NAME` (MetadataStart) from the stream it already decodes. When the name is in the `DCS_NAMES` of an aircraft file, that aircraft becomes the active one: the bridge serves its layout and state, drops the state of the other aircraft (trim points, control positions, MPD texts, guard windows) and logs `aircraft | <NAME>`. The last detected aircraft is stored in `config/settings.json` and is the start aircraft until DCS reports one. `[dcs] aircraft` set to a name forces that aircraft; `"auto"` (default) follows DCS. The AIRCRAFT switch of the settings page (AUTO / one button per aircraft) overrides the detection for debugging, until it is set back to AUTO or the bridge restarts.
- **Page.** `/state` carries `aircraft`; when it differs from the aircraft of the loaded layout, the page reloads and reads `/layout` again. The remembered tab, the MPD / MFCD side and the CDU unit are stored in the browser per aircraft.
- **Seats.** The aircraft file declares its seats (`SEATS`) and the seat output (`SEAT_OUTPUT`). With one seat and `SEAT_OUTPUT = None` the seat is 0 as soon as DCS-BIOS data arrives, the badge shows the aircraft, and there is no debug-seat hold.
- **Trim display.** Only for an aircraft with a `TRIM_SWITCH`; without one the bridge does no trim tracking and needs no `trim_reset` key.
- **Power levers.** The lever keys (`power_*`) are required only for an aircraft with `lever` controls. The A-10C II throttles are read-only bars.
- **Display pages.** The MFCD, CDU and UFC are hand-drawn layouts in the page (`mfcd`, `cdu`), like the AH-64D `mpd` and `ku`.
- **Panel look.** An aircraft chooses the plate look per page (`ah64d` or `a10c`, [section 7](#7-the-panel-kit)).
- **Export script.** One table per aircraft name; the A-10C II table is empty.
- **Keys.** The required keys depend on the aircraft. A key hat (a `hat` with `keys`, [section 8](#8-the-bridge-interface)) carries the HOTAS controls of the A-10C II once its keybinds are known.
- **Scroll page.** A panel page that does not fit 640 × 600 du is a scroll page ([section 7](#7-the-panel-kit)).

## 10. Manual test run

The manual test run of the AH-64D is in [Manual test run (AH-64D)](AH64D/SPEC.md#5-manual-test-run-ah-64d).

## 11. Future development and out of scope

**Future development: AI integration.** Not part of the product, and nothing in the dashboard depends on it. If the dashboard works well, an AI assistant (e.g. Claude) could later connect to the bridge through an MCP server. Ideas collected so far:

- Status advisor: reads cautions, lamps and flight and engine data, explains them and suggests next steps.
- Auto startup: runs a routine from cold and dark to ready for takeoff.
- Waypoint entry: enters a coordinate list into the TSD via the KU.
- George control on request: an AI deciding what George should do. The GEORGE tab only has fixed buttons.
- Each capability would be a use case with its own on / off toggle on the dashboard.

Other ideas: a WebSocket instead of polling if polling proves too slow; radios on the dashboard; grip controls with guards (CHOP, BUCS, emergency jettison) with the same guard mechanism.

**Out of scope:** AI integration (see above), multiplayer, automatic flying (stick, collective, pedals), cockpit-replica graphics, hardware panels, security beyond the local network.
