# Stage 3 – Tablet dashboard

Detailed spec for Stage 3 of [SPEC.md](SPEC.md). Goal: a dashboard page on the tablet that replaces the keyboard and mouse for cockpit commands.

Status: draft, waiting for review.

Stage 3 is built one view at a time. This first part covers the **Startup** view only. Navigation, Fighting and George follow once Startup works in DCS.

## What Stage 2 tells us

- Every Startup control except the power levers works through DCS-BIOS commands with readback.
- The power levers only move by keypress, one key per lever (`power_*` entries in `[keys]`). Keys for both levers together do not work.
- Some switch positions do not work: master ignition EXT PWR (no ground power), rotor brake BRK.
- The APU button only works with its cover open.
- Bringing DCS to the front before a keypress works every time.

## Design rules

- **Cockpit names and positions.** Every control uses the label printed in the cockpit and shows all of its real positions, in cockpit order, even positions we do not use. A position that cannot be set (see Stage 2) is shown greyed out and cannot be selected.
- **The tablet shows the cockpit, not the last tap.** Every control shows the position read back from DCS. A switch moved in the cockpit with the mouse moves on the tablet too.
- **Big touch targets**: at least 56 × 56 CSS pixels, enough space between controls.
- **Landscape first.** Designed for an iPad Air in landscape (1180 × 820 CSS pixels), but laid out with a CSS grid that also fits other tablets from about 1024 × 768 up. Portrait works but is not optimised.
- **Plain look.** Dark background, white stencil-style labels, lamp colours as in the cockpit. No images, no frameworks, no external files.

## Startup view

Pilot controls, grouped like the cockpit. Values are the DCS-BIOS readback values.

### Lamps (top row)

| Label | DCS-BIOS | Colour |
| --- | --- | --- |
| MASTER WARNING | `PLT_MASTER_WARNING_L` | red |
| MASTER CAUTION | `PLT_MASTER_CAUTION_L` | amber |
| ENG 1 FIRE | `PLT_ENG_1_FIRE_L` | red |
| APU FIRE | `PLT_APU_FIRE_L` | red |
| ENG 2 FIRE | `PLT_ENG_2_FIRE_L` | red |
| APU ON | `PLT_APU_L` | green (check against the cockpit in the test run) |

Lamps are display only. Master caution and warning have no DCS-BIOS input, so they cannot be reset from the tablet.

### Controls

| Label | DCS-BIOS | Positions (value = label) | Route | Notes |
| --- | --- | --- | --- | --- |
| MSTR IGN | `PLT_MASTER_IGN_SW` | 0 = OFF, 1 = BATT, 2 = EXT PWR | DCS-BIOS | EXT PWR greyed |
| APU cover | `PLT_APU_BTN_CVR` | 0 = CLOSED, 1 = OPEN | DCS-BIOS | |
| APU | `PLT_APU_BTN` | push button | DCS-BIOS | press = 1, released to 0 after 0.3 s; locked while the cover is closed |
| ENG 1 START | `PLT_ENG1_START` | 2 = START, 1 = OFF, 0 = IGN ORIDE | DCS-BIOS | START and IGN ORIDE are spring-loaded: set, held 0.5 s, back to OFF |
| ENG 2 START | `PLT_ENG2_START` | 2 = START, 1 = OFF, 0 = IGN ORIDE | DCS-BIOS | as ENG 1 START |
| ENG 1 power lever | readback `PLT_ENG_L_PW_LVR` | OFF, IDLE, FLY, LOCKOUT | keys | slider, see below; LOCKOUT greyed |
| ENG 2 power lever | readback `PLT_ENG_R_PW_LVR` | OFF, IDLE, FLY, LOCKOUT | keys | as ENG 1 |
| RTR BRK | `PLT_ROTOR_BRK` | 2 = OFF, 1 = BRK, 0 = LOCK | DCS-BIOS | BRK greyed |
| PARK BRAKE | `PLT_PARK_BRAKE` | 0 = IN, 1 = PULLED | DCS-BIOS | |

A selector shows one button per position, the current position highlighted. Tapping a position sends it. Tapping a greyed position does nothing.

### Power lever sliders

- One vertical slider per lever, positions bottom to top: OFF, IDLE, FLY, LOCKOUT. The slider snaps to positions only; there are no values in between. LOCKOUT is shown above FLY but greyed and cannot be reached.
- Readback to position: the nearest of OFF 0, IDLE 16383, FLY 58981, LOCKOUT 65535.
- Moving the slider sends the keys for that lever, one step at a time, waiting up to 1 s for the readback after each step:
  - OFF → IDLE: `power_<side>_idle`
  - IDLE → FLY: `power_<side>_up`
  - FLY → IDLE: `power_<side>_down`
  - IDLE → OFF: `power_<side>_off`
  - OFF → FLY and FLY → OFF go through IDLE.
- `<side>` is `left` for ENG 1 and `right` for ENG 2.

### Seat

- The header shows the current seat: `PILOT` or `CP/G`.
- In the CP/G seat the Startup view is read only: lamps and positions are shown, all controls are disabled, and the header says `CP/G – read only`. The bridge also refuses Startup commands while the seat is CP/G.
- The header also shows `NO DCS DATA` when no DCS-BIOS packet arrived for 3 s.

## How it works

```
Tablet browser  --GET /            -->  dashboard.py  (serves web/index.html)
                --GET /layout      -->  the Startup view definition as JSON
                --GET /state  5 Hz -->  seat, data age, current values
                --POST /command    -->  checks it, sends DCS-BIOS command or keys
                                            |
                                  DCS-BIOS stream (thread) --> current values
```

- **Polling, not WebSocket.** The page asks for `/state` five times per second. That is plenty for switches and lamps on the local network, and it keeps the bridge to the Python standard library (`http.server`). [SPEC.md](SPEC.md) says WebSocket; this replaces it for now. A WebSocket can come later if polling proves too slow.
- **Threads.** One background thread reads the DCS-BIOS stream into the current values; the web server (`ThreadingHTTPServer`) answers each request in its own thread. A lock protects the values, a second lock makes sure only one command (or key sequence) is sent at a time.
- **The view is data.** The Startup controls above are one Python list in `dashboard.py`, served as `/layout`. The page draws whatever the list contains. Adding a view later means adding a list, not new page code (unless a new control type is needed).
- **Only listed controls.** `/command` accepts only controls and positions from the view list, refuses greyed positions, refuses the push button while its cover is closed, and refuses everything while the seat is CP/G. Each refusal returns an error message the page shows briefly.
- **Local network only, no login** (as in SPEC.md). The server listens on `[dashboard] host` and `port` from `config.toml` (default `0.0.0.0:8080`).

### Requests

- `GET /layout` → `{"views": [{"name": "Startup", "lamps": [...], "controls": [...]}]}`
- `GET /state` → `{"seat": 0, "age": 0.1, "values": {"PLT_MASTER_IGN_SW": 1, ...}}`; `seat` is `null` before the first packet.
- `POST /command` with `{"id": "PLT_MASTER_IGN_SW", "value": 1}` or `{"id": "power_left", "value": "FLY"}` → `{"ok": true}` or HTTP 409 with `{"error": "..."}`.

### Log

The rolling log gets the start, every command with its result (source `dash`), every refusal and every error. Values are not logged (that is what Stage 1 is for).

```
2026-10-12 10:00:01.120 | dash    | PLT_MASTER_IGN_SW    | 1 sent
2026-10-12 10:00:05.300 | dash    | power_left           | FLY: keys idle, up
2026-10-12 10:00:09.010 | dash    | PLT_ROTOR_BRK        | 1 refused: position not available
```

## Files

```
dashboard.py        new: view list, DCS-BIOS thread, web server, command handling
web/index.html      new: the page; HTML, CSS and JavaScript in one file
README.md           + "Run the dashboard"
```

Reused unchanged: `bridge/config.py`, `bridge/log.py`, `bridge/dcsbios.py`, `bridge/keys.py`, the `[dashboard]` and `[keys]` config. No new dependencies. The export script is not needed for Startup.

## Test run (Windows, manual)

Preparation: Stage 2 setup, DCS in windowed or borderless mode. PC and tablet on the same network. Windows may ask to allow Python on the network: allow it for private networks.

1. Start `python dashboard.py`. It prints the address to open, for example `http://<PC address>:8080`.
2. Open the address on the iPad, add it to the home screen for full screen.
3. AH-64D mission, cold and dark, pilot seat. Start up using only the tablet: MSTR IGN BATT, APU cover OPEN, APU, wait for APU ON, ENG 1 START, ENG 1 power lever IDLE, ENG 2 START, ENG 2 power lever IDLE, both power levers FLY, PARK BRAKE IN.
4. Move a few switches in the cockpit with the mouse and check the tablet follows.
5. Switch to the CP/G seat: the view shows `CP/G – read only`, controls disabled.
6. Keep the log.

Done when a cold start to both power levers at FLY works from the tablet alone, the lamps match the cockpit, and the CP/G seat shows read only.

## Build steps

Each step is verified before the next one starts.

1. `dashboard.py` without keys: view list, DCS-BIOS thread, `/layout`, `/state`, `/command` for DCS-BIOS controls. Check: against a fake DCS-BIOS, `/state` shows the seat and values, a command changes the fake's value, a greyed position, the closed APU cover and the CP/G seat are refused.
2. Power lever commands. Check: with key sending replaced by a recorder, every slider move from every position sends the right key sequence and waits for the readback.
3. `web/index.html`. Check: in a browser against the fake DCS-BIOS at 1180 × 820 and 1024 × 768: all controls and lamps drawn with their positions, greyed positions not selectable, tapping a position changes it, CP/G seat shows read only, `NO DCS DATA` when the fake stops.
4. Docs: README "Run the dashboard", SPEC.md points to this file and notes polling instead of WebSocket.

## Open points

- APU ON lamp colour: check against the cockpit.
- Hold time for the engine START switch (0.5 s) and the APU button (0.3 s): check in the test run.
