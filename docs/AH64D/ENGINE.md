# AH-64D – engine features

What the dashboard engine (bridge, page, panel kit, export script, test kit) does for the AH-64D, and which engine features exist because of this aircraft. The AH-64D was the first aircraft, so there was no phase of planned engine changes as for the A-10C ([../A10C/ENGINE.md](../A10C/ENGINE.md), E1 to E10) and the F-16C ([../F16C/ENGINE.md](../F16C/ENGINE.md), F1 to F8): the engine grew out of this aircraft, and the other two reuse most of it. This file is a record of what is built, not a plan. It is based on the code (the Where column is checked against the files), on the engine spec [../SPEC.md](../SPEC.md) and on the first specs and fix specs of the git tag `research-v1` (`docs/STAGE3.md`, `docs/COCKPIT.md`, `docs/COCKPIT_FIXES.md`).

Not used by the AH-64D: scroll pages (every one of the 21 panel pages fits 640 × 600 du), key hats and read-only bars, the LAMP and BAR parts of the kit, the `mfcd` and `cdu` layouts, the looks `a10c` and `f16c`. What the engine does for the AH-64D in general (the seats, the views, the command checks) is in [SPEC.md](SPEC.md) section 10 and [../SPEC.md](../SPEC.md) sections 8 and 9.

## Overview

| # | Feature | Why | Where | Size / Status |
| --- | --- | --- | --- | --- |
| 1 | Panel kit and the `ah64d` look | 21 panel pages; drawn page by page from photos, the screws did not line up and the same button had different sizes | `core/panel_kit.py` (`Panel`, `PanelGroup`, `LOOKS`), `kit_pages` in `aircraft/ah64d.py`, `plateSvg` and `plateArt` in `core/web/index.html` | large; built |
| 2 | One global scale | A page fitted to the screen on its own made small panels huge | `fitPlate` and `KIT_SCALE_MAX` in `core/web/index.html`, `REF` in `core/panel_kit.py` | small; built, iPad look open |
| 3 | Switch chooser | Invisible touch bands on a switch were not intuitive | `openChooser`, `layoutChooser` and `arcCentres` in `core/web/index.html` | medium; built, iPad look open |
| 4 | Knob bar | A knob needs an absolute value; a bar at the knob | `openBar`, `renderBar` and `initBar` in `core/web/index.html` | medium; built |
| 5 | Pop-ups at the control | The knob bar opened in the middle of the screen | `placePopup` in `core/web/index.html` | small; built, iPad look open |
| 6 | Guarded controls and real DCS covers | Fire buttons, jettison and zeroize must not be hit by accident; DCS ignores the button while its own cover is closed | `GUARD_WINDOW`, `open_real_cover`, `close_real_cover`, `cover_watcher` and `check_and_send` in `core/dashboard.py`; `addGuard` and `openGuard` in `core/web/index.html`; `cover_at` in `core/panel_kit.py` | large; built; the real covers and the buttons never sent are still to test in DCS (FIXES.md) |
| 7 | Confirmed presses | A press of one DCS frame is lost; the tablet must show what DCS did | `press_and_release`, `hold_until` and `PRESS_MIN` in `core/dashboard.py`; `notConfirmed` in `core/web/index.html` | medium; built, seen in the DCS log |
| 8 | Power levers by keypress | DCS-BIOS does not move the levers past OFF, and keys for both levers together do not work | `LEVER_KEYS` and `move_lever` in `core/dashboard.py`; `power_levers` in `aircraft/ah64d.py`; `buildLever` and `buildPlateLever` in `core/web/index.html` | medium; built, tested in the pilot seat in DCS; CP/G keys open |
| 9 | Trim tracking and the export script | The live stick position lags; the trim point is the stick position when Force Trim is released | `track_trim`, `trim_reset_watcher` and `export_reader` in `core/dashboard.py`; `TRIM_SWITCH` in `aircraft/ah64d.py`; `buildTrim` in `core/web/index.html`; `AIRCRAFT` in `core/lua/DCS-Dashboard-Export.lua` | medium; built; directions open |
| 10 | MPD live labels | DCS-BIOS has no MPD text; `list_indication` has it for the occupied seat | `parse_mpd_labels` and `export_reader` in `core/dashboard.py`; `MPD_INDICATIONS` and `MPD_SEATS` in `aircraft/ah64d.py`; `mpdLabel` in `core/web/index.html` | medium; built; label follow-up open |
| 11 | Seats and the debug seat | Two crew stations with their own ids and pages; a way to see the other seat's pages | `SEATS` and `SEAT_OUTPUT` in `aircraft/ah64d.py`; `current_seat` in `core/dashboard.py`; `cycleDebugSeat`, `activeSeat` and `renderBadge` in `core/web/index.html` | medium; built; finger on the badge open |
| 12 | One tab per view name, one FIGHT page per seat | The pilot and the gunner need different FIGHT pages under one tab | `viewIndex`, `buildTabs` and `followSeat` in `core/web/index.html`; `VIEWS` in `aircraft/ah64d.py` (the two FIGHT views) | small; built; gunner page tests open |
| 13 | `key` controls | The canopy, the monocle, the controls overlay have no DCS-BIOS input | `buildKey` in `core/web/index.html`; the `key` branch of `check_and_send` in `core/dashboard.py`; `KEYS` in `aircraft/ah64d.py` | small; built; canopy state mapping open |
| 14 | `macro` controls (GEORGE) | George has no DCS-BIOS entry; a command is a key sequence | `MACRO_KEY_GAP` and the `macro` branch of `check_and_send` in `core/dashboard.py`; `george_ring` in `aircraft/ah64d.py`; `macro_pause_scale` in `core/config.py` | medium; built; button tests open (FIXES.md) |
| 15 | `bios`, `value` and `rest` button fields | IAT, OFS and OFS ALL are three buttons on one three-position switch | the `button` branch of `check_and_send` in `core/dashboard.py`; `CPG_IAT` in `aircraft/ah64d.py` | small; built; switch mapping open |
| 16 | `digital` stick (TKR pad) | The sight manual tracker has three states per axis, not the analog range | `STICK_DIGITAL` and `move_stick` in `core/dashboard.py`; `tkr_controls` in `aircraft/ah64d.py`; `buildStick` in `core/web/index.html` | small; built; tracker test open |
| 17 | Dual-function knobs and the COMM pull | IHADSS BRT / CON and FLIR LVL / GAIN share one knob each; the COMM volume knobs pull out | `video_knob` and `comm_knob` in `aircraft/ah64d.py`; `knob` and `chip` in `core/panel_kit.py`; `buildPlateKnob`, `addMark`, `buildPlateChip` and `PULL_HOLD_MS` in `core/web/index.html` | medium; built; PULL chip look open |
| 18 | Locked controls (`requires`) | The APU button does nothing while its cover is closed | the `button` branch of `check_and_send` in `core/dashboard.py`; `power_pages` in `aircraft/ah64d.py` | small; built, tested in DCS (APU) |
| 19 | Step fallback | The MPD mode knob does not take a direct command to NT | `reach_by_steps` in `core/dashboard.py`; `mpd_controls` in `aircraft/ah64d.py` | small; built; NT test open |
| 20 | Hand-drawn MPD, TEDAC and KU | The displays are drawn 1:1 after photos; the cursor pad moves the cursor | `mpdSvg`, `tedSvg`, `kuSvg`, `placeMpd` and `placeKu` in `core/web/index.html`; `cursor_controls` in `aircraft/ah64d.py` | large; built; label, cursor and CP/G checks open |
| 21 | Displays of several ids | The EUFD has 14 lines of text, the CMWS status has pages | `buildPlateDisplay` in `core/web/index.html`; `eufd_pages` and `cmws_pages` in `aircraft/ah64d.py` | small; built; count display check open |
| 22 | `core/kit_helpers.py` | Constants and builders the aircraft files share | `kit_page`, `step_rocker`, `readout`, `BUTTON_HOLD` and `KNOB_STEP` in `core/kit_helpers.py`, used by `aircraft/ah64d.py` | small; built |
| 23 | Aircraft choice | The bridge serves every aircraft and follows the one DCS reports | `follow_aircraft` and `select_aircraft` in `core/dashboard.py`; `DCS_NAMES` in `aircraft/ah64d.py` | small; built; the switch between aircraft in DCS is open |
| 24 | Layout checker and test kit | A page cannot be judged by eye on 21 pages in two seats and two sizes | `core/tools/check_panels.js`; `sweep.js` and `smoke.py` in `core/tools/test` | medium; built; run after every change to a page |

## Details

### 1 Panel kit and the `ah64d` look

The first tablet test of the COCKPIT pages showed that every page was drawn on its own from photo coordinates, with no shared parts. The panel kit is a layout compiler: a page names a part and a centre, the kit gives the part its standard size, places the labels, adds the plate with four corner ears and a screw in each, and checks the layout when the file is loaded. The photos only say what is on a panel, its text and the arrangement, not pixel sizes. `ah64d` is the default look (dark flat plates, rectangular ears, slotted screws). Parts, sizes and rules: [../SPEC.md](../SPEC.md) section 7; the look: [SPEC.md](SPEC.md) section 11.

### 2 One global scale

All panel geometry is in design units (du). Every page is drawn at the same scale `S = min(area width / 640, area height / 600)`, at most 1.6, in both seats, so the small panels no longer fill the screen. The plan was 1.16 and 1.07; the built values are 1.045 at 1180 × 820 and 0.958 at 1024 × 768, because the header, the lamp row and the strip above the gear leave about 627 px and 575 px of height. Every standard part is sized so that its touch area is at least 56 px at that scale. [../SPEC.md](../SPEC.md) section 7; the fit of the pages: [SPEC.md](SPEC.md) section 2, Rules for the pages.

### 3 Switch chooser

A tap on a switch opens a chooser at the switch: one big button per position (at least 64 px, 8 px apart), arranged like the switch (a column, a row, an arc for a dial). The current position is lit, a disabled one is dashed, a spring-return one carries a spring mark. It replaced the invisible bands, which nobody could see or guess. Guarded switches (one band per position under the cover) and the power levers (one band per mark) are the exceptions. [SPEC.md](SPEC.md) section 2, Switches.

### 4 Knob bar

A tap on a knob opens a bar at the knob (420 px wide, 130 px high); drag or tap the track and the bridge sets the absolute value, at most every 100 ms. The MPD mode knobs have three stops. [SPEC.md](SPEC.md#knob-bar).

### 5 Pop-ups at the control

The bar opens below its knob (above it if there is no room), the chooser is centred on the switch; both stay 8 px inside the screen, below the tab bar and clear of the gear. The scrim stays: a tap outside closes without a command. [SPEC.md](SPEC.md) section 2, Pop-ups.

### 6 Guarded controls and real DCS covers

A guarded control (fire buttons, extinguishers, JETT, ZEROIZE, MASTER ZEROIZE, CMWS JETT) is on its own panel page only, behind a cover drawn by the kit, and needs two steps: lift the cover, then one tap. The bridge enforces it, so a second tab or a stale page cannot bypass it: opening a cover opens a 5 s window for that id only, and a command is accepted inside the window only (`refused: guard closed`). Where the real cockpit has a cover, DCS-BIOS has a cover control, and DCS ignores the button while it is closed (the first test: ENG 1 FIRE and CMWS JETT were sent but not confirmed). So the bridge also opens DCS's own cover, waits up to 0.5 s for the readback, and closes it about 1 s after the command; `cover_watcher` closes covers whose window ran out. [SPEC.md](SPEC.md) section 2, Guarded controls; [../SPEC.md](../SPEC.md) section 8, Command checks and refusals.

### 7 Confirmed presses

The bridge checks DCS-BIOS after sending: a push button is held until DCS shows it pressed (at least 0.3 s, at most 1 s) and then released, a hat until its axis shows the direction, a selector until the readback shows the position. The reply is `confirmed` true, false or null, and the page shows an amber note for false. The reason: a press of one DCS frame, a command waiting behind a slow lever sequence, a key when DCS cannot be brought to the front, a double tap. [../SPEC.md](../SPEC.md) section 5, Confirmed presses.

### 8 Power levers by keypress

DCS-BIOS reads the levers back (0 OFF, 16383 IDLE, 58981 FLY) but does not move them past the OFF detent. One key per lever moves them: `RAlt` (left) or `RShift` (right) with `Home`, `PageUp`, `PageDown`, `End`. A move is made one step at a time, waiting up to 1 s for the readback after each key; OFF to FLY goes through IDLE. The fourth position LOCKOUT is greyed out. The eight `power_*` keys are required only because the AH-64D has `lever` controls (the A-10C throttles are read-only bars). [SPEC.md](SPEC.md) section 2, Power levers, and section 9.

### 9 Trim tracking and the export script

The export script sends the control positions (stick, collective, pedals) 10 times per second. The live position is not drawn, because it lags behind the stick; CTRL IND toggles DCS's own overlay for that. The bridge stores the position at the moment the Force Trim switch goes from held back to rest as the trim point of that seat, and watches the `trim_reset` key (reading only that key's state) to move it to the centre. The page draws a ring at the trim point and a tick on the pedal bar. Only an aircraft with a `TRIM_SWITCH` gets this. The export script has one table per aircraft name; the AH-64D table holds the eight cockpit arguments and the four MPD indications. [SPEC.md](SPEC.md) section 3, Trim display; [../SPEC.md](../SPEC.md) section 4.

### 10 MPD live labels

The export script sends the MPD text of the occupied seat 4 times per second (`MPD_INDICATIONS`, pilot 7 and 9, CP/G 11 and 13). The bridge reads the `PB<n>` fields and serves them as `mpd_labels`; the page writes each label in MPD green next to its button, and nothing when no text arrived for 3 s. [SPEC.md](SPEC.md) section 5.

### 11 Seats and the debug seat

The seats are declared in the aircraft file; ids with `{seat}` are expanded by the bridge with the prefix of the current seat, and the bridge refuses commands of a view outside its seats. A long hold (0.6 s) on the seat badge looks at the other seat's pages (or, without DCS data, cycles none, CP/G, PILOT, none). The debug seat is view only and lives in the page only: every control is disabled, so no command can leave the page, and the bridge never sees it. [SPEC.md](SPEC.md#seats); [../SPEC.md](../SPEC.md) section 5.

### 12 One tab per view name, one FIGHT page per seat

The tab bar has one tab per view name; a tab opens the view of that name whose `seats` contain the current seat. FIGHT is two views with the same name, one with `"seats": [0]` and one with `"seats": [1]`. The remembered tab is the name, stored per aircraft. [SPEC.md](SPEC.md#seats) and section 4.

### 13 `key` controls

A `key` control sends a keypress from `[keys]` (`canopy`, `monocle`, `controls_overlay`): DCS reads the keyboard through scan codes, so the bridge uses `SendInput`, taps LShift and brings the DCS window to the front first (it worked every time in Stage 2). The canopy has a readback (`PLT_CANOPY`). [SPEC.md](SPEC.md) section 9; [../SPEC.md](../SPEC.md) section 4, Controlling.

### 14 `macro` controls (GEORGE)

A `macro` control is a fixed key sequence, each step `[key name, hold, pause after]`, sent under the command lock with the pauses multiplied by `[dashboard] macro_pause_scale`. The modifiers and the main key are staggered by 40 ms (`MACRO_KEY_GAP`). A ring command always starts with Hide, because the ring state cannot be read: Hide, Show, direction, Hide (`george_ring`). [SPEC.md](SPEC.md) section 7; [../SPEC.md](../SPEC.md) section 8, Macro controls.

### 15 `bios`, `value` and `rest` button fields

A button acts on another DCS-BIOS control (`bios`), sends a level other than 1 (`value`) and returns to a rest level other than 0 (`rest`). With them IAT (`value` 2), OFS and OFS ALL (`value` 0, `rest` 1, a longer hold) are three buttons on `CPG_LHG_TEDAC_L_IAT`; the press is confirmed against `bios` and `value`. [SPEC.md](SPEC.md) section 4; [../SPEC.md](../SPEC.md) section 8, Control fields.

### 16 `digital` stick (TKR pad)

The pad of the Sight Manual Tracker looks and feels like the cursor pad, but the tracker has three states per axis. The bridge turns the deflection into 2, 0 or 1 with a dead zone of 30 % (`STICK_DIGITAL`) and sends only changes; lifting the finger returns both axes to 1. [SPEC.md](SPEC.md#tkr-tedac-selected-cpg-seat).

### 17 Dual-function knobs and the COMM pull

Members with the same `group` share one knob and each has a selector mark next to it (IHADSS BRT / CON, FLIR LVL / GAIN). A knob with a `pull` id shows pulled out when it reads 1, and a hold of 0.6 s on the knob toggles it; the PULL chip under the knob is the small second target (32 px floor, the long press is the large one). [SPEC.md](SPEC.md) section 2, ARMAMENT and COMM.

### 18 Locked controls

A control with `requires` is refused while the other control is not in its position: the APU button needs its cover `PLT_APU_BTN_CVR` open (`locked: open the cover first`), and the page does not send it. [SPEC.md](SPEC.md) section 2, POWER.

### 19 Step fallback

A selector with `step_fallback` turns the knob with INC / DEC steps if the position is not reached in 0.5 s: the MPD and TEDAC MODE knobs (NT did not take a direct command in Stage 2). [SPEC.md](SPEC.md#knob-bar).

### 20 Hand-drawn MPD, TEDAC and KU

The two MPDs, the TEDAC and the KU are drawn 1:1 after photos in the page (`mpd` and `ku` layouts), because their parts are not panel kit parts. The cursor pad is an analog `stick`: the distance from the touch point is the deflection, lifting the finger sends centre. [SPEC.md](SPEC.md) sections 5 and 6.

### 21 Displays of several ids

A `display` with `ids` (and `page` and `pages`) shows several DCS-BIOS strings: the 14 EUFD lines of 56 characters and the CMWS status with its pages MAIN, TEST and NONE. [SPEC.md](SPEC.md) section 2, EUFD and CMWS.

### 22 `core/kit_helpers.py`

The constants and builders the three aircraft files share: the page builder `kit_page`, the step rocker, the readout, the arrow glyphs, the button hold time and the knob step. It was made when the aircraft files carried the same duplicated code; the layout data of the AH-64D was byte-identical before and after.

### 23 Aircraft choice

`aircraft/ah64d.py` has `DCS_NAMES = ["AH-64D_BLK_II"]`; the bridge reads `_ACFT_NAME` from the DCS-BIOS stream and switches to this file when it reads that name, drops the state of the other aircraft and logs `aircraft | AH-64D`. [../SPEC.md](../SPEC.md) section 9.

### 24 Layout checker and test kit

`core/tools/check_panels.js` measures every panel page in the browser (overlaps, label and screw positions, part sizes, touch areas); an empty `problems` is the acceptance. The test kit (`core/tools/test`) runs it in both seats at 1180 × 820 and 1024 × 768, drives every control with `smoke.py`, and measures every tab with `sweep.js`. [../SPEC.md](../SPEC.md) section 7; [SPEC.md](SPEC.md#touch-sizes-per-view).

## Decisions

These are the decisions that shaped the features above, taken from the first specs, the engine spec and the fix round after the first tablet test.

| # | Decision | Where it was decided |
| --- | --- | --- |
| D1 | Polling instead of a WebSocket: the page asks for `/state` five times per second, which keeps the bridge to the Python standard library (`http.server`); a WebSocket can come later if polling proves too slow | `docs/STAGE3.md` in the tag; [../SPEC.md](../SPEC.md) section 2 |
| D2 | The tablet shows the cockpit, not the last tap: every control shows the position read back from DCS | `docs/STAGE3.md`, Design rules; [../SPEC.md](../SPEC.md) section 2 |
| D3 | Only controls that passed the Stage 2 sweep go on the dashboard (later the guarded controls, skipped in the sweep, got their panel pages behind covers); blocklisted controls (JETT, fire, zeroize, CHOP, BUCS, triggers) are never swept or on a quick page | `docs/SPEC.md` in the tag; [../SPEC.md](../SPEC.md) section 4 |
| D4 | The view is data: the controls of each view are a list in the aircraft file, the generic bridge and page stay free of aircraft knowledge | `docs/STAGE3.md`, How it works; [../SPEC.md](../SPEC.md) section 2 |
| D5 | The power levers move by one key per lever, one step at a time, waiting for the readback | `docs/STAGE2.md` results in the tag; [SPEC.md](SPEC.md) section 2 |
| D6 | A guarded control needs the cover, then a single tap; no hold, no chooser (the hold of the first fix round was removed) | `docs/COCKPIT_FIXES.md` section 10b, decision 2 |
| D7 | The bridge enforces the guard with a 5 s window per id; the page alone cannot bypass it | `docs/COCKPIT.md`, Guarded controls |
| D8 | The bridge opens and closes DCS's own cover for the parts that have one, because DCS ignores the button while it is closed | `docs/COCKPIT_FIXES.md` section 10 |
| D9 | One scale for all pages (design units, a 640 × 600 du budget); small panels are allowed to look small | `docs/COCKPIT_FIXES.md` section 2, decision 4 |
| D10 | The kit decides sizes; the photos say only what is on a panel, its text and the arrangement | `docs/COCKPIT_FIXES.md` sections 2 and 13 (decision 6) |
| D11 | Four identical rectangular corner ears per plate with the screw in the centre; screw alignment has priority over the photo | `docs/COCKPIT_FIXES.md` decision 1 |
| D12 | A switch has one touch area and a chooser at the switch, in place of the invisible bands; the rotary positions sit on a small circle at their real angles | `docs/COCKPIT_FIXES.md` section 6, decision 5 |
| D13 | Pop-ups open at the control and stay inside the screen | `docs/COCKPIT_FIXES.md` section 5 |
| D14 | The power levers and FRICT keep one touch band per mark and the knob bar | `docs/COCKPIT_FIXES.md` decision 3 |
| D15 | The PULL chip is exempt from the 56 px floor: 32 px, and the long press on its knob is the large target | `docs/COCKPIT_FIXES.md` decision 12 |
| D16 | No emoji-capable code point in the UI; arrows, chevrons and the cross are inline SVG | `docs/COCKPIT_FIXES.md` section 11 |
| D17 | Confirmed presses: the bridge checks DCS-BIOS after sending and says `confirmed` true, false or null | `docs/STAGE3.md`, Confirmed presses; [../SPEC.md](../SPEC.md) section 5 |
| D18 | The live stick position is not drawn; only the trim point is, and CTRL IND toggles DCS's own overlay | `docs/STAGE3.md`, Trim display; [SPEC.md](SPEC.md) section 3 |
| D19 | The export script sends only the control positions and the four MPDs; the generic engine and flight values do not fit the Apache | `docs/STAGE1.md` results in the tag; [SPEC.md](SPEC.md#what-dcs-allows-for-the-ah-64d) |
| D20 | The MPD, TEDAC and KU are drawn 1:1 after photos, with live MPD labels from the export script | `docs/STAGE3.md`, MPD view; [SPEC.md](SPEC.md) sections 5 and 6 |
| D21 | One FIGHT page per seat under one tab; the debug seat is view only and lives in the page | [../FIXES.md](../FIXES.md) fix log (2026-10-11); [SPEC.md](SPEC.md#seats) |
| D22 | George has buttons as `macro` controls; a ring command starts with Hide because the ring state cannot be read; the weapon-release buttons have no guard for now | [SPEC.md](SPEC.md) section 7; [../FIXES.md](../FIXES.md#ah-64d-mature) |
| D23 | Automatic aircraft choice from `_ACFT_NAME`, with a manual switch in the settings page | [../A10C/ENGINE.md](../A10C/ENGINE.md) E1; [../SPEC.md](../SPEC.md) section 9 |
| D24 | The AH-64D file passes no `look`: `ah64d` stays the default of the kit | [SPEC.md](SPEC.md) section 10 (E6) |
