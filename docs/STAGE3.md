# Stage 3 – Tablet dashboard

Detailed spec for Stage 3 of [SPEC.md](SPEC.md). Goal: a dashboard page on the tablet that replaces the keyboard and mouse for cockpit commands.

Status: Aircraft view tested on Windows. Fight, MPD and KU views built, waiting for the test run.

Stage 3 is built one view at a time. Built so far: **Aircraft** (start-up and flight, pilot seat), **Fight** (weapons, sights, countermeasures, both seats), **MPD** (both MPD bezels, both seats) and **KU** (keyboard unit, both seats); George is not built yet.

## What Stage 2 tells us

- Every Aircraft control except the power levers works through DCS-BIOS commands with readback.
- The power levers only move by keypress, one key per lever (`power_*` entries in `[keys]`). Keys for both levers together do not work.
- Some switch positions do not work: master ignition EXT PWR (no ground power), rotor brake BRK.
- The APU button only works with its cover open.
- Bringing DCS to the front before a keypress works every time.

## Design rules

- **Cockpit names and positions.** Every control uses the label printed in the cockpit and shows all of its real positions, in cockpit order, even positions we do not use. A position that cannot be set (see Stage 2) is shown greyed out and cannot be selected.
- **The tablet shows the cockpit, not the last tap.** Every control shows the position read back from DCS. A switch moved in the cockpit with the mouse moves on the tablet too.
- **Big touch targets**: 56 × 56 CSS pixels where space allows; at least 44 px on the three-row AIRCRAFT view and as on the real bezel on the MPD view (about 0.7 of the button spacing).
- **Landscape first.** Designed for an iPad Air in landscape (1180 × 820 CSS pixels), but laid out with a CSS grid that also fits other tablets from about 1024 × 768 up. Portrait works but is not optimised.
- **Plain look.** Dark background, white stencil-style labels, lamp colours as in the cockpit. No images, no frameworks, no external files.

## Aircraft view

Pilot seat only (`"seats": [0]`), controls grouped like the cockpit. Values are the DCS-BIOS readback values.

### Lamps (top row)

| Label | DCS-BIOS | Colour |
| --- | --- | --- |
| MASTER WARNING | `PLT_MASTER_WARNING_L` | red |
| MASTER CAUTION | `PLT_MASTER_CAUTION_L` | amber |
| ENG 1 FIRE | `PLT_ENG_1_FIRE_L` | red |
| APU FIRE | `PLT_APU_FIRE_L` | red |
| ENG 2 FIRE | `PLT_ENG_2_FIRE_L` | red |
| APU ON | `PLT_APU_L` | green (check against the cockpit in the test run) |

Lamps are display only, except MASTER WARNING and MASTER CAUTION.

MASTER WARNING and MASTER CAUTION are lighted pushbuttons as in the cockpit: tapping the lamp presses `PLT_INTL_MWARN_BTN` / `PLT_INTL_MCAUTION_BTN` (0.3 s).

### Controls

| Label | DCS-BIOS | Positions (value = label) | Route | Notes |
| --- | --- | --- | --- | --- |
| MSTR IGN | `PLT_MASTER_IGN_SW` | 0 = OFF, 1 = BATT, 2 = EXT PWR | DCS-BIOS | EXT PWR greyed |
| APU cover | `PLT_APU_BTN_CVR` | 0 = CLOSED, 1 = OPEN | DCS-BIOS | |
| APU | `PLT_APU_BTN` | push button | DCS-BIOS | press = 1, released to 0 after 0.3 s; locked while the cover is closed |
| ENG 1 START | `PLT_ENG1_START` | 2 = START, 1 = OFF, 0 = IGN ORIDE | DCS-BIOS | START and IGN ORIDE are spring-loaded: set, held 0.5 s, back to OFF |
| ENG 2 START | `PLT_ENG2_START` | 2 = START, 1 = OFF, 0 = IGN ORIDE | DCS-BIOS | as ENG 1 START |
| PWR LVR 1 | readback `PLT_ENG_L_PW_LVR` | OFF, IDLE, FLY, LOCKOUT | keys | slider, see below; LOCKOUT greyed |
| PWR LVR 2 | readback `PLT_ENG_R_PW_LVR` | OFF, IDLE, FLY, LOCKOUT | keys | as ENG 1 |
| RTR BRK | `PLT_ROTOR_BRK` | 2 = OFF, 1 = BRK, 0 = LOCK | DCS-BIOS | BRK greyed |
| PARK BRAKE | `PLT_PARK_BRAKE` | 0 = IN, 1 = PULLED | DCS-BIOS | |
| TAIL WHEEL | `PLT_T_WHEEL_UNLOCK_BTN` | push button | DCS-BIOS | press = 1, released to 0 after 0.3 s; locks / unlocks the tail wheel |
| NAV | `PLT_EXTL_NAV_L_SW` | 2 = BRT, 1 = OFF, 0 = DIM | DCS-BIOS | EXT LT panel |
| ANTI COL | `PLT_EXTL_ACOL_L_SW` | 2 = WHT, 1 = OFF, 0 = RED | DCS-BIOS | EXT LT panel |
| MPD L, MPD R | `PLT_MPD_L_MODE`, `PLT_MPD_R_MODE` | 2 = DAY, 1 = NT, 0 = MONO | DCS-BIOS | if the position is not reached in 0.5 s the bridge turns the knob with INC / DEC steps (NT did not take a direct command in Stage 2) |
| CANOPY | readback `PLT_CANOPY` | 0 = CLOSED, 1 = OPEN | key `canopy` (LCtrl+C) | DCS-BIOS cannot move the canopy; state mapping to be checked in the test run |

The view is laid out in three rows; buttons are at least 44 px here.

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
- `<side>` is `left` for PWR LVR 1 (engine 1) and `right` for PWR LVR 2 (engine 2).

## Fight view

Follows the current seat (`"seats": [0, 1]`). Ids written as `{seat}_...` are expanded to `PLT_...` in the pilot seat and `CPG_...` in the CP/G seat.

### Lamps (top row)

| Label | DCS-BIOS | Colour |
| --- | --- | --- |
| MASTER WARNING | `{seat}_MASTER_WARNING_L` | red |
| MASTER CAUTION | `{seat}_MASTER_CAUTION_L` | amber |
| ARM | `{seat}_MASTER_ARM_ARM_L` | amber (check against the cockpit in the test run) |
| SAFE | `{seat}_MASTER_ARM_SAFE_L` | green (check against the cockpit in the test run) |
| GND ORIDE | `{seat}_GROUND_OVERRIDE_L` | amber (check against the cockpit in the test run) |

The ARM, SAFE and GND ORIDE colours are not confirmed yet. Lamps are display only, except MASTER WARNING and MASTER CAUTION.

MASTER WARNING and MASTER CAUTION are tappable here too ({seat}_INTL_MWARN_BTN / {seat}_INTL_MCAUTION_BTN).

### Controls

| Label | DCS-BIOS | Positions | Notes |
| --- | --- | --- | --- |
| A/S | `{seat}_MASTER_ARM_BTN` | push button | press = 1, released to 0 after 0.3 s; the ARM and SAFE lamps show the result |
| GND ORIDE | `{seat}_GROUND_OVERRIDE_BTN` | push button | press = 1, released to 0 after 0.3 s |
| WAS | hat: `{seat}_CYCLIC_WEAPON_UD` / `{seat}_CYCLIC_WEAPON_LR` | up = G, down = A, left = R, right = M | see Hats below |
| SIGHT SEL | hat: `{seat}_COLLECTIVE_SIGHT_SELECT_UD` / `{seat}_COLLECTIVE_SIGHT_SELECT_LR` | up = HMD, down = LINK, left = FCR, right = TADS | see Hats below |
| FLARE | `{seat}_CYCLIC_FLARE` | push button | press = 1, released to 0 after 0.3 s |
| CHAFF | `{seat}_CYCLIC_CHAFF` | push button | press = 1, released to 0 after 0.3 s |
| FLARE COUNT | `PLT_CMWS_FLARE_COUNT` | display | read only; from the pilot's CMWS panel, shown in both seats |
| CHAFF COUNT | `PLT_CMWS_CHAFF_COUNT` | display | read only; from the pilot's CMWS panel, shown in both seats |

### Hats

A hat is drawn as a cross of four buttons. A tap sets the axis (`_UD` or `_LR`) to 2 (up, right) or 0 (down, left) and holds it for 0.3 s. Then the bridge returns the axis to the centre, 1. The highlighted direction comes from the readback of the two axes.

The TEDAC grip hats of the CP/G (LHG WAS, RHG sight select) are left out on purpose: they do the same as the cyclic WAS and the collective sight select. If the cyclic WAS does not act in the CP/G seat in DCS, swap to the TEDAC ones (both passed in Stage 2).

## MPD view

Both MPD bezels side by side, laid out like the cockpit, following the current seat (`"layout": "mpd"`). The screen in the middle stays empty.

- Frame of 8 columns × 11 rows; rows are 0.78 of the column width, as on the real bezel.
- Top: VID knob, T1–T6, MODE knob with DAY / NT / MONO labels (tap a label). Left: BRT knob, L1–L6, FCR, WPN, TSD. Right: \*, R1–R6, VID, COM, A/C. Bottom: TSD, M (B1), B2–B6, A/C.
- Variable action buttons are light grey squares without text; fixed action buttons are black keys with white text.
- Knobs: tap the left half for down, the right half for up (`{seat}_MPD_<L|R>_BRT` / `_VIDEO`, step 3200); the pointer shows the readback.
- Buttons are pressed for 0.15 s. In the CP/G seat the left MPD's L1–L6 did not respond in Stage 2.

## KU view

The keyboard unit, laid out like the cockpit (`"layout": "ku"`), following the current seat.

- Top: the scratchpad (`{seat}_KU_DISPLAY`) in green.
- Rows: A–F | 1 2 3, G–L | 4 5 6, M–R | 7 8 9, S–X | . 0 +/-, then Y Z / BKS SPC \* ÷ + −, then the BRT knob, CLR, ←, →, ENTER. E, N, S and W are boxed; the white guide lines of the panel are drawn.
- Keys are pressed for 0.15 s.

## Seat

- Each view lists the seats it can be used in: Aircraft the pilot seat, Fight both seats.
- The header shows the current seat: `PILOT` or `CP/G`. It adds ` – READ ONLY` when the shown view cannot be used in this seat (Aircraft in the CP/G seat): lamps and positions are shown, all controls are disabled.
- The header shows `NO DCS DATA` when no DCS-BIOS packet arrived for 3 s, and `BRIDGE OFFLINE` when the page cannot reach the bridge.
- The bridge refuses commands of a view outside its seats.

## Settings and page lock

- A gear button at the bottom right opens a settings page over the dashboard; `BACK` closes it. A free strip at the bottom of the controls keeps the gear clear of every control.
- **LOGGING** OFF / ON switches writing `logs/dcs-dashboard.log` on the PC (the console output stays). Saved in `settings.json` next to `dashboard.py` (git-ignored) and applied at the next start.
- **KEEP SCREEN ON** OFF / ON uses the browser's screen wake lock, for this tablet only (stored in the browser).
- **INFO** shows the DCS Saved Games folder the bridge uses, the DCS data status and the address to open on another tablet.
- `saved_games = "auto"` in `config.toml` asks Windows for the Saved Games folder and uses `DCS` or `DCS.openbeta`, whichever has DCS-BIOS installed.
- The page is locked for use as a home screen app: no scrolling, no rubber-band bounce, no pinch or double-tap zoom, no text selection or long-press menu. Rotation cannot be locked from a web page on iOS: use the iPad's rotation lock; in portrait a full-screen hint asks to turn the iPad.
- Home screen icon `web/apple-touch-icon.png` (180 × 180, "DCS" / "Dashboard", white on grey), name "DCS Dashboard".
- `start_dashboard.bat` starts the bridge with a double-click and keeps the window open if it stops with an error.

## How it works

```
Tablet browser  --GET /            -->  dashboard.py  (serves web/index.html)
                --GET /layout      -->  the view definitions (Aircraft, Fight) as JSON
                --GET /state  5 Hz -->  seat, data age, current values
                --POST /command    -->  checks it, sends DCS-BIOS command or keys
                                            |
                                  DCS-BIOS stream (thread) --> current values
```

- **Polling, not WebSocket.** The page asks for `/state` five times per second. That is plenty for switches and lamps on the local network, and it keeps the bridge to the Python standard library (`http.server`). [SPEC.md](SPEC.md) says WebSocket; this replaces it for now. A WebSocket can come later if polling proves too slow.
- **Threads.** One background thread reads the DCS-BIOS stream into the current values; the web server (`ThreadingHTTPServer`) answers each request in its own thread. A lock protects the values, a second lock makes sure only one command (or key sequence) is sent at a time.
- **The view is data.** The controls of each view are one Python list in `dashboard.py`, served as `/layout`. The page draws whatever the lists contain. Adding a view later means adding a list, not new page code (unless a new control type is needed).
- **Seat placeholder.** Ids in a view may contain `{seat}`. `/layout` serves them unexpanded and the page sends them unexpanded; the bridge expands them from the current seat (`PLT_` or `CPG_`) before it reads or sends.
- **Only listed controls.** `/command` accepts only controls and positions from the view lists, refuses greyed positions, refuses the push button while its cover is closed, refuses commands of a view outside its seats (for example Aircraft in the CP/G seat), and refuses displays (display only). Each refusal returns an error message the page shows briefly.
- **Local network only, no login** (as in SPEC.md). The server listens on `[dashboard] host` and `port` from `config.toml` (default `0.0.0.0:8080`).
- New control types: `knob` (value "up" / "down", sends ±step), `key` (a keypress from `[keys]`, e.g. the canopy), lamps with a `button`, and selectors with `step_fallback`.

### Requests

- `GET /layout` → `{"views": [{"name": "Aircraft", "seats": [0], "lamps": [...], "controls": [...]}, {"name": "Fight", "seats": [0, 1], ...}]}`
- `GET /state` → `{"seat": 0, "age": 0.1, "values": {"PLT_MASTER_IGN_SW": 1, ...}}`; `seat` is `null` before the first packet.
- `POST /command` with `{"id": "PLT_MASTER_IGN_SW", "value": 1}`, `{"id": "power_left", "value": "FLY"}` or, for a hat, `{"id": "{seat}_WAS", "value": "up"}` → `{"ok": true}` or HTTP 409 with `{"error": "..."}`. Displays are read only: a command for a display returns `{"error": "display only"}`.
- `GET /settings` → `{"logging": true, "saved_games": "...", "address": "http://<PC address>:8080"}`; `POST /settings` with `{"logging": false}` → the same JSON, or HTTP 400.

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
web/apple-touch-icon.png  home screen icon
start_dashboard.bat       starts dashboard.py
```

Reused unchanged: `bridge/config.py`, `bridge/log.py`, `bridge/dcsbios.py`, `bridge/keys.py`, the `[dashboard]` and `[keys]` config. No new dependencies. The export script is not needed for the dashboard.

## Test run (Windows, manual)

Preparation: Stage 2 setup, DCS in windowed or borderless mode. PC and tablet on the same network. Windows may ask to allow Python on the network: allow it for private networks.

**Aircraft view**

1. Start `python dashboard.py`. It prints the address to open, for example `http://<PC address>:8080`.
2. Open the address on the iPad, add it to the home screen for full screen.
3. AH-64D mission, cold and dark, pilot seat, AIRCRAFT tab. Start up using only the tablet: MSTR IGN BATT, APU cover OPEN, APU, wait for APU ON, ENG 1 START, ENG 1 power lever IDLE, ENG 2 START, ENG 2 power lever IDLE, both power levers FLY, PARK BRAKE IN, TAIL WHEEL once.
4. Move a few switches in the cockpit with the mouse and check the tablet follows.
5. Switch to the CP/G seat: the AIRCRAFT tab shows `CP/G – READ ONLY`, controls disabled.
6. Keep the log.

**Fight view**

1. Pilot seat, FIGHT tab: tap A/S and check that the ARM and SAFE lamps change.
2. Tap GND ORIDE once.
3. Tap WAS in each direction: the weapon selection changes in the cockpit.
4. Tap SIGHT SEL in each direction.
5. Tap FLARE and CHAFF once each: the counts change (CMWS must be on).
6. Switch to the CP/G seat (key `2`): the badge shows `CP/G`. Repeat A/S, WAS and SIGHT SEL.
7. The AIRCRAFT tab shows `CP/G – READ ONLY`.
8. Check the lamp colours (ARM, SAFE, GND ORIDE) against the cockpit.

Done when a cold start to both power levers at FLY works from the tablet alone, the lamps match the cockpit, and the CP/G seat shows read only on the AIRCRAFT tab. For the FIGHT tab: every control acts in both seats, the counts change, and the lamp colours match the cockpit.

## Results

### Aircraft view

Tested on Windows with an iPad Air. A cold start to both power levers at FLY worked from the tablet alone. The tester reported that it works and looks good.

### Fight view

Built and checked only against a fake DCS-BIOS in a browser (both seats, 1180 × 820 and 1024 × 768). Not tested in DCS yet.

## Build steps

Each step is verified before the next one starts.

1. `dashboard.py` without keys: view list, DCS-BIOS thread, `/layout`, `/state`, `/command` for DCS-BIOS controls. Check: against a fake DCS-BIOS, `/state` shows the seat and values, a command changes the fake's value, a greyed position, the closed APU cover and the CP/G seat are refused.
2. Power lever commands. Check: with key sending replaced by a recorder, every slider move from every position sends the right key sequence and waits for the readback.
3. `web/index.html`. Check: in a browser against the fake DCS-BIOS at 1180 × 820 and 1024 × 768: all controls and lamps drawn with their positions, greyed positions not selectable, tapping a position changes it, CP/G seat shows read only, `NO DCS DATA` when the fake stops.
4. Docs: README "Run the dashboard", SPEC.md points to this file and notes polling instead of WebSocket.
5. Seat-aware views, hat / display / button without cover, Fight view and TAIL WHEEL in `dashboard.py`. Check: against the fake DCS-BIOS in both seats.
6. Page: tabs AIRCRAFT / FIGHT, hat cross, count displays. Check: in a browser at 1180 × 820 and 1024 × 768 and in both seats.
7. Docs (this update).
8. Settings page, page lock, app icon, `start_dashboard.bat`, Saved Games detection and the logging switch. Check: in a browser against the fake DCS-BIOS at 1024 × 768 and 1180 × 820 (no control under the gear, nothing clipped), logging off writes nothing and survives a restart, the portrait hint covers the screen, the icon is served as PNG.
9. MPD and KU views, NAV / ANTI COL / MPD mode / canopy on AIRCRAFT, tappable master lamps, `knob` and `key` types. Check: against the fake DCS-BIOS (commands, step fallback, canopy key simulated) and in a browser at 1024 × 768 and 1180 × 820 (no overlap, nothing under the gear).

## Open points

- APU ON lamp colour: check against the cockpit.
- Hold time for the engine START switch (0.5 s) and the APU button (0.3 s): check in the test run.
- Lamp colours ARM, SAFE and GND ORIDE: check against the cockpit.
- Flare and chaff counts: only checked against the fake DCS-BIOS, which has no text values.
- If the cyclic WAS does not act in the CP/G seat, swap to the TEDAC grip hats (LHG WAS, RHG sight select).
- Refusal log lines show the unexpanded `{seat}_...` id (cosmetic).
- MPD MODE NT and the INC / DEC fallback: check in DCS.
- CANOPY state mapping (0 = CLOSED, 1 = OPEN): check in DCS.
- CP/G left MPD L1–L6 did not respond in Stage 2.
- The layout is made for 1024 × 768 and larger; smaller screens overlap.
