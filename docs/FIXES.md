# Fixes and open points

Temporary: the one list of everything still open, sorted by area. Delete an entry when it is fixed or move it to [SPEC.md](SPEC.md) (engine), [AH64D/SPEC.md](AH64D/SPEC.md) (AH-64D), [A10C/SPEC.md](A10C/SPEC.md) (A-10C II) or the [test kit README](../core/tools/test/README.md) (developer test kit).

## Open points

### Engine and page (all aircraft)

- [ ] Tidy up this file after the next DCS test run, as was done for the AH-64D: delete what is fixed and move settled rules into the specs.

#### Needs a test in DCS

- [ ] Debug seat on the tablet: the long hold works with a finger on the badge.

#### Needs a look on the iPad

- [ ] Knob grip look: the ridge count (24) and the second rim of the large knobs may need tuning.
- [ ] Chooser: button size, the arc of the dials, placement near the screen edges.

#### Known limitations

- [ ] The layout is made for 1024 × 768 and larger; smaller screens overlap.
- [ ] The panel pages need CSS container queries: Safari / iPadOS 16 or newer, or current Chrome.
- [ ] Refusal log lines show the unexpanded `{seat}_...` id (cosmetic).

### AH-64D (mature)

#### Needs a test in DCS

- [ ] Fire buttons: are ENG 1, APU and ENG 2 FIRE confirmed by their own readback once the real cover is open? If ENG 1 is still `not confirmed` with the cover open, confirm with the RDY lamp (`{S}_ENG_1_READY_L`) instead of the button.
- [ ] Real covers: the bridge opens DCS's own cover for ENG 1, APU and ENG 2 FIRE, MASTER ZEROIZE and CMWS JETT (waits up to 0.5 s for the readback, closes it about 1 s after the command). Check in both seats: the log shows `cover open`, `pressed`, about 1 s later `cover closed`, and no `not confirmed`.
- [ ] Guarded controls never sent before: station selects, PRI and RES (with a fire button armed), JETT (with a station armed), ZEROIZE, MASTER ZEROIZE, CMWS JETT. Do them last in a throwaway mission.
- [ ] Hold times: ENG START switch (0.5 s) and APU button (0.3 s).
- [ ] Lamp colours: APU ON (green), ARM (amber), SAFE (green), GND ORIDE (amber), DISCH lights of PRI and RES.
- [ ] Flare and chaff counts: only checked against the simulated DCS-BIOS, which has no text values.
- [ ] Flares and chaff in the air with the CMWS set up; note which presses show "not confirmed".
- [ ] If the cyclic WAS does not act in the CP/G seat, swap to the left-grip WAS hat (LHG WAS).
- [ ] MPD MODE NT and the INC / DEC fallback.
- [ ] CANOPY state mapping (0 = CLOSED, 1 = OPEN).
- [ ] Trim display: confirm the ring and tick directions after a few trims.
- [ ] MPD live labels: check that they follow page changes.
- [ ] Cursor pad: check the speed and the up / down direction.
- [ ] TEDAC and the KU in the CP/G seat.
- [ ] CP/G power lever keys (`RAlt` / `RShift` with `Home` and so on): only tested in the pilot seat.
- [ ] FRICT slider direction and the end of the SIGNAL knob sweep: taken from the photos, not from DCS.
- [ ] GEORGE PHS SEARCH once George's systems are ready (on the ground with the systems not ready the ring shows the start-up layout, so Up does nothing useful).
- [ ] GEORGE POINT SEARCH with a TSD point selected and George not tracking (without it: no effect).
- [ ] GEORGE STORE TARGET while George tracks a target (the key works; without a tracked target George says he cannot).
- [ ] GEORGE AIR AREA SEARCH in the air: does a target list appear?
- [ ] GEORGE READY SYSTEMS / MASTER OFF on the ground, in both states: systems not started (George starts up and announces) and systems already started (George shuts down).
- [ ] George ring commands: confirm that the ring really stays hidden after STOP / TADS FWD (no problem reported so far).
- [ ] GEORGE Target List: it appears with the ring left open after a search, and PREV TARGET / NEXT TARGET move through it.
- [ ] GEORGE SELECT TARGET numbers the entries, and TRACK / ENGAGE starts the shoot-list sequence.
- [ ] GEORGE ROE HOLD / FREE toggles (the ring text colour changes) and the ring stays open.
- [ ] GEORGE FIRE gives consent in HOLD FIRE.
- [ ] GEORGE EXIT LIST cancels the list and the shoot list.
- [ ] George ring commands with the new timing (hold 0.15 s, pauses 0.5 / 1.0 / 0.6 s, staggered keys): which buttons work; if keys are missed raise `macro_pause_scale` (1.5, 2) in config/config.toml and read the per-step lines in the log.
- [ ] Gunner FIGHT: IAT, OFS and OFS ALL do what the grip does, and the switch mapping is right (IAT forward = 2, OFS aft = 0, rest 1).
- [ ] Gunner FIGHT: the TADS FOV letters (Z N W M on the up, left, right and down buttons) and the SENSOR mapping (FLIR 2, TV 1).
- [ ] Gunner FIGHT: SIGHT SEL from the right grip (HMD, FCR, TADS, LINK) and SLAVE.
- [ ] TKR pad (MPD tab, TEDAC selected): the direction of all four axes (the up / down sign is shared with the cursor, `CURSOR_Y_SIGN` in `core/web/index.html`), the dead zone, the slew ramp.

#### Needs a look on the iPad

- [ ] PULL chips on COMM: `PULL OUT` fits and reads in the font the iPad uses (checked in Arial Narrow and Arial; the iPad may use Helvetica Neue); the long press (0.6 s) on the knob is comfortable.
- [ ] The deviations from the photos below: say which ones to change.

#### Known limitations

- [ ] CP/G left MPD L1–L6 do not respond in DCS.
- [ ] MPD labels: which labels are boxed (selected) is not shown; long labels can overlap their neighbours.
- [ ] MASTER ZEROIZE has no photo and is a plain placard. The CP/G COMM and WIPER / DEFOG pages use the same drawings as the pilot's COMM and CENTER pages.
- [ ] Grip controls with guards (CHOP, BUCS, emergency jettison) are not on the dashboard.
- [ ] The weapon trigger and the laser trigger are not on the gunner FIGHT page: the laser trigger has no DCS-BIOS entry, and the weapon trigger (`CPG_CYCLIC_TRIGGER`) is on the blocklist. Both could become key buttons later.
- [ ] On the first load with a remembered FIGHT tab in the CP/G seat the pilot page shows for one poll (about 0.2 s) before it switches.
- [ ] George: the FLIGHT and COMBAT commands of George as pilot are not on the dashboard until the ring mode is understood. Open questions for a later test: does the ring always open in the same mode? does Hide and Show reset a list or sub-menu?
- [ ] George: the weapon-release buttons (FIRE, TRACK / ENGAGE, ROE HOLD / FREE, POINT SEARCH, SELECT TARGET) are unguarded on purpose for now. A guard for grid buttons would be a page change: first tap arms for 5 s, second tap fires.
- [ ] George: the ROE state (HOLD FIRE or FREE FIRE) is not readable; read the colour of the ring text.
- [ ] George: the ring state is not readable. The bridge assumes the ring is hidden at the start of a ring command and starts with Hide.
- [ ] AH-64D, gunner FIGHT page: the hats WAS, SIGHT SEL and TADS FOV (99 × 52.9 px at 1180 × 820, 84.2 × 47.1 px at 1024 × 768) and the SENSOR selector (309.1 × 54.2 and 264.6 × 48.4 px) are under the 56 px minimum, because the 7 × 3 grid has no room for two-row hats (they need 24 cells, the grid has 21). Open decision, options: a fourth grid row, eight columns, or less chrome per cell. Until then they are accepted exceptions ([design rules](SPEC.md#design-rules)).
- [ ] MPD: the keys R1 and * are 54.4 px high at 1024 × 768 since the side switch became 56 px. Same accepted exception as the other MPD keys ([touch sizes](AH64D/SPEC.md#touch-sizes-per-view)).

### A-10C II (under development)

#### Needs a test in DCS

- [ ] A-10C II test run in DCS ([A10C/SPEC.md](A10C/SPEC.md), section 12): everything was tested only against a simulated DCS-BIOS. Includes the aircraft change: load an AH-64D mission, then an A-10C mission; the page reloads by itself, the AIRCRAFT switch in the settings works, and the remembered tab and display side stay per aircraft.
- [ ] A-10C value directions: the switches whose position order the DCS-BIOS description does not give (up position assumed to be 1, IFF mode toggles, ARC-210 dials, T-handles, fill disable buttons, CMSP and AAP switches and more). The list by page is in [A10C/RESEARCH.md](A10C/RESEARCH.md), Open points.
- [ ] A-10C keybinds: export the default keybinds from DCS (Options, Controls, Make HTML). The keypress controls (speed brake, trim, nosewheel steering, the HOTAS key hats) are not built until the keys are known.
- [ ] A-10C phase 7 (research in DCS): the full list is in the [open points](A10C/RESEARCH.md#open-points) and the [plan table](A10C/RESEARCH.md#plan) of A10C/RESEARCH.md: keybind export, the four screenshots (flap lever, ejection seat arm handle, auxiliary gear handle, canopy actuator disengage lever), DCS research, and the MFCD live labels through the export script once the MFCD indication numbers are known.

#### Needs a look on the iPad

- [ ] A-10C scroll pages (nine of the 23 panel pages): the frame, the scroll bar and the shaded edges are clear; a drag never taps or turns a control; the page opens at the top.

#### Known limitations

- [ ] A-10C key hat layout: a key hat in a 1 × 1 grid cell has touch areas of about 44 px, below the 56 px minimum. The HOTAS key hats need 2 × 2 cells, so the FLIGHT and FIGHT grids are rearranged when the keys are added.
- [ ] A-10C: the MFCD screen is empty (DCS-BIOS has no MFCD text and the export script table of the A-10C is empty); the six A-10C II UFC buttons stand in one provisional row until their place on the real UFC is known.
- [ ] A-10C (under development): the long-hold page list with 29 entries is taller than the screen and cuts off entries (found by `core/tools/test/sweep.js`). Fix when the A-10C work resumes.
- [ ] THROTTLE page: the flap lever plate has no placard title.
- [ ] FIGHT: the text CMSP 1 / CMSP 2 is wider than its box at 1024 × 768 (found by `core/tools/test/sweep.js --acft A-10C_2`).
- [ ] The text of the CMSP, CMSC, UHF, TACAN and VHF FM windows is clipped by about 3 px (found by the same sweep).
- [ ] About 20 groups of touch targets are under 56 px (found by the same sweep). To measure and fix when the work resumes.
- [ ] The FLIGHT lamp row wraps to two lines at 1024 × 768 (accepted for now).

### Developer test kit

#### Needs a test in DCS

- [ ] The test kit has not been run on Windows yet: the `python` / `python3` choice, the folder creation in `gen_json.lua` and the real Saved Games DCS-BIOS folder.

#### Known limitations

- [ ] `bridge.py` reads the key table of `core/keys.py` up to `class KEYBDINPUT`, so that marker must stay.
- [ ] The docstring of `core/tools/test/smoke.py` still says "_ACFT_NAME=A-10C_2 is re-sent every second".
- [ ] The full sweep takes about 4 minutes.

### Later / ideas

- [ ] Open questions: radios on the dashboard (later?); which keyboard combinations for cockpit commands are used today (each one would become a button).
- [ ] Multiplayer: document how it works after the first multiplayer test with a friend in the same AH-64D.
- [ ] Add a DCS-BIOS source filter if two PCs on the same network ever send DCS-BIOS multicast at the same time.

## Deviations to look at on the tablet

The arrangement and text of the panel pages follow the photos. These are the places where it deliberately does not:

- Corner ears: four identical rectangular ears per plate with the screw in the centre. The photos show ears of different heights, some overlapping their neighbours; screw alignment has priority.
- EUFD: the display is on top and the controls sit in a row below it (three rockers, BRT knob, four keys), not around the glass. The glass is 568 × 280 du so the 14 lines of 56 characters stay readable.
- CENTER: one wide plate (CHK OVSP TEST and GEN RST) over two plates (WINDSHIELD WIPER, and PARK BRAKE with ALT SET), 16 du apart on shared edge lines.
- COMM: the ICS name and its PTT label sit in the SOL row, between the FM 1 and FM 2 squelch switches; the switch itself, with VOX and HOT MIC, is below the row.
- Wiper labels: PARK, OFF, LO and HI are flat text in a fan above the dial, not turned along the dial.
- PARK BRAKE name: printed on two lines (PARK, BRAKE); on one line it runs into the plate margin and the corner ear.
- MASTER ZEROIZE: a plain placard drawn without a photo.
- One scale for all pages: small panels (FIRE, TAIL WHEEL) no longer fill the screen.

## Fix log

| Date | Problem | Fix | Verified |
| --- | --- | --- | --- |
| 2026-10-11 | No way to look at the other seat; shared FIGHT page | Debug seat view, one FIGHT page per seat, gunner controls, TKR pad | Simulated DCS-BIOS in the browser, both seats and sizes; not yet in DCS |
