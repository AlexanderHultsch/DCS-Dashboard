# Fixes and open points

Temporary: the one list of everything still open, sorted by area. Delete an entry when it is fixed or move it to [SPEC.md](SPEC.md) (engine), [AH64D/SPEC.md](AH64D/SPEC.md) (AH-64D), [A10C/SPEC.md](A10C/SPEC.md) (A-10C II), [F16C/SPEC.md](F16C/SPEC.md) (F-16C) or the [test kit README](../core/tools/test/README.md) (developer test kit).

## Open points

### Engine and page (all aircraft)

- [ ] Tidy up this file after the next DCS test run, as was done for the AH-64D: delete what is fixed and move settled rules into the specs.

#### Needs a test in DCS

- [ ] Debug seat on the tablet: the long hold works with a finger on the badge.

#### Needs a look on the iPad

- [ ] Knob grip look: the ridge count (24) and the second rim of the large knobs may need tuning.
- [ ] Chooser: button size, the arc of the dials, placement near the screen edges.
- [ ] Page list (long hold on COCKPIT): it scrolls inside its card with the native thin scroll bar and no shaded edges. A long hold on the AH-64D COCKPIT tab may open and close the list again on release (seen in emulation only).

#### Known limitations

- [ ] The layout is made for 1024 × 768 and larger; smaller screens overlap.
- [ ] The panel pages need CSS container queries: Safari / iPadOS 16 or newer, or current Chrome.
- [ ] Refusal log lines show the unexpanded `{seat}_...` id (cosmetic).
- [ ] The chooser does not scroll: a selector with many positions does not fit the screen (the F-16C DEFOG lever has 21 positions and shows 5).
- [ ] The buttons of a selector in a quick page grid cell are 44 px, under the 56 px rule (A-10C and F-16C FLIGHT and FIGHT; more than four positions draw two columns).
- [ ] The panel kit has no blue lamp colour (the F-16C ECM T lamps and the AR RDY lamp are drawn white).
- [ ] The panel kit has no latching push button (a button that stays in); the F-16C ECM module buttons are push buttons that send 1 and then 0.
- [ ] No command-only control without readback: a DCS-BIOS control that has no output named like its id cannot be a selector or a page control of its own (the F-16C FUEL QTY SEL TEST is left off).
- [ ] No 4-way hat on panel kit pages (the F-16C ICP DCS switch is four buttons in a cross).
- [ ] No slider with a maximum for a lever with several positions: a `knob` sends 0 to 65535 only (the F-16C DEFOG lever).
- [ ] No guarded control in the quick page grid: guarded controls exist on panel pages only (the F-16C THROTTLE CUTOFF is on FUEL / EPU / START, not on FLIGHT).
- [ ] The A-10C MFCD slots `ADJ` and `BRT` are aliases of the generic corner slots `TL` and `BR` (`MFCD_GEO` in `core/web/index.html`). Rename them in `aircraft/a10c.py` and drop the aliases when the A-10C work resumes.

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
- [ ] THROTTLE page: the flap lever plate has no placard title.
- [ ] FIGHT: the text CMSP 1 / CMSP 2 is wider than its box at 1024 × 768 (found by `core/tools/test/sweep.js --acft A-10C_2`).
- [ ] The text of the CMSP, CMSC, UHF, TACAN and VHF FM windows is clipped by about 3 px (found by the same sweep).
- [ ] About 20 groups of touch targets are under 56 px (found by the same sweep). To measure and fix when the work resumes.
- [ ] The FLIGHT lamp row wraps to two lines at 1024 × 768 (accepted for now).

### F-16C Viper (under development)

#### Needs a test in DCS

- [ ] F-16C test run in DCS ([F16C/SPEC.md](F16C/SPEC.md), section 12): everything was tested only against a simulated DCS-BIOS. Includes the aircraft change: AH-64D, A-10C and F-16C missions one after the other.
- [ ] F-16C keybinds: export the default keybinds from DCS (Options, Controls, Make HTML). The keypress controls (the HOTAS key hats TMS, DMS, CMS and TRIM, the speed brake keys, nosewheel steering) are not built until the keys are known; their cells are reserved in the FLIGHT and FIGHT grids.
- [ ] F-16C phase 7 (research in DCS): the six screenshots (throttle, canopy switch and handle, handcrank, ANTI-G TEST button, right console fittings, CHAFF/FLARE button; [F16C/PICTURES.md](F16C/PICTURES.md)), the MFD live labels through the export script once the MFD indication numbers are known, and which side the manual is right on where it contradicts itself (MFD format select OSB 13 to 15 on p. 124 against 12 to 14 on p. 126; ANTI-SKID against PARKING BRAKE on p. 56; the unnamed PEDAL ADJ knob on p. 81).
- [ ] F-16C value directions that are guesses (99 identifiers, the full list is in [F16C/BIOS.md](F16C/BIOS.md), "Position orders that are guesses"), by page:
  - CANOPY / DEFOG: `CANOPY_HANDLE`, `CANOPY_JETT_THANDLE`, `DEFOG_LEVER`.
  - FUEL / EPU / START: `FUEL_MASTER_SW`, `FUEL_MASTER_CV`, `TANK_INTERTING_SW`, `AIR_REFUEL_SW`, `ENG_CONT_SW`, `ENG_CONT_SW_COVER`.
  - FLT CONTROL / TRIM: `DIGI_BAK_SW`, `ALT_FLAPS_SW`, `FLCS_RESET_SW`, `BIT_SW`, `TRIM_AP_DISC_SW`, `MANUAL_PITCH_SW`, and the turn directions of the roll, pitch and yaw trim knobs.
  - ELEC / TEST: `OBOGS_SW`, `EPU_GEN_TEST_SW`.
  - EXT LIGHTING, ECM, AUDIO: `POS_FLASH_LIGHT_SW`, `ECM_PW_SW`, `ECM_XMIT_SW`, `ECM_1_BTN` to `ECM_6_BTN`, `COMM1_MODE_KNB`, `COMM2_MODE_KNB`.
  - LANDING GEAR / HMCS: `HOOK_SW`, `GEAR_HANDLE`, `GND_JETT_ENABLE_SW`, `BRAKE_CHAN_SW`, `STORES_CONFIG_SW`, `GEAR_ALT_HANDLE`.
  - CMDS, UHF / IFF BACKUP, THREAT WARNING: `CMDS_PWR_SOURCHE_SW`, `CMDS_CH_EXP_CAT_SW`, `CMDS_FL_EXP_CAT_SW`, `CMDS_JETT_SW`, `IFF_C_I_KNB`, `UHF_FREQ_100_KNB`, `UHF_FREQ_0025_KNB`, `UHF_FUNC_KNB`, `UHF_MODE_KNB`, `UHF_SQUELCH_SW`, `RWR_PWR_BTN`; the left-to-right order of the four UHF frequency knobs.
  - MISC, INSTRUMENTS, SEAT: `LASER_ARM_SW`, `EXT_FUEL_TRANS_SW`, `SEAT_EJECT_SAFE`.
  - SNSR PWR / VMS / ZEROIZE, AVIONICS POWER, OXYGEN: `HDPT_SW_L`, `HDPT_SW_R`, `FCR_PWR_SW`, `VMS_INHIBIT_SW` (the guess rule differs from most toggles, see BIOS.md), `ZEROIZE_SW_COVER`, `MMC_PWR_SW`, `ST_STA_SW`, `MFD_SW`, `UFC_SW`, `GPS_SW`, `DL_SW`, `OXY_DILUTER_LVR`.
  - DED tab and MFD tab: `ICP_DED_SW`, `ICP_DATA_RTN_SEQ_SW`, `ICP_DATA_UP_DN_SW`, the four MFD rockers.
- [ ] ECM module buttons (`ECM_1_BTN` to `ECM_6_BTN`) and RWR POWER (`RWR_PWR_BTN`): DCS-BIOS defines toggles (0 out, 1 in, latching); they are built as push buttons (1, then 0 after 0.3 s), which may only flash the module in. If so, a latching push button is an engine addition.
- [ ] FLCS BIT, MANUAL PITCH, EPU/GEN and OBOGS BIT: drawn spring-loaded (held 0.5 s) although DCS-BIOS defines plain toggles. Do they spring back in DCS?
- [ ] Autopilot PITCH switch (`AP_PITCH_SW`): a plain three-position selector. Does DCS hold ALT HOLD and ATT HOLD with it, and does a tap on the selector keep the autopilot on?
- [ ] SAI cage (`SAI_CAGE`): a DCS-BIOS push button drawn as a PULL chip (IN 0, OUT 1). Check the direction and that the pull cages the SAI.
- [ ] MFD rockers (GAIN, SYM, BRT, CON): one 0.3 s press per tap; the order down, centre, up is guessed. Is a held rocker needed (the manual says it runs to the limit)? Does the OSB numbering of the bottom row (11 at the far right) match the cockpit?
- [ ] FUEL QTY SEL TEST (`FUEL_QTY_SEL_T_KNB`) is not on the dashboard: how does the knob behave in DCS (cold start steps 70 ff.)?
- [ ] EPU switch: it has a dashboard cover only. Does it move with its DCS covers (`EPU_SW_COVER_OFF`, `EPU_SW_COVER_ON`) closed?
- [ ] Guarded controls with a DCS cover (`FUEL_MASTER_CV`, `ENG_CONT_SW_COVER`, `ZEROIZE_SW_COVER`): the cover order (0 closed, 1 open) is a guess; the cold start needs a cover tap before the ENG CONT steps 59 and 62.
- [ ] THROTTLE CUTOFF (`THROTTLE_OFF_IDLE`): does it move the throttle between OFF and IDLE?
- [ ] UHF STATUS: "press and hold" in the manual, 0.3 s here.
- [ ] DEFOG: `DEFOG_LEVER` takes 0 to 20; the chooser has 5 positions. Check that they set MIN, 5, 10, 15 and MAX.

#### Needs a look on the iPad

- [ ] F-16C look: the colours (plate `#17191b`, cross-head screws, semi-bold labels) were read from the manual pictures. Compare with DCS screenshots.
- [ ] Guard drawing: guarded controls use the engine's guard cover, not the red flip guard of the real FUEL MASTER, EPU, ENG CONT and ZEROIZE switches. Keep?
- [ ] F-16C scroll pages (eight of the 21 panel pages and the DED tab): the frame, the scroll bar and the shaded edges are clear; a drag never taps or turns a control; the page opens at the top.
- [ ] DED tab: the labels between the override row and the keypad are tight.
- [ ] Scroll pages close to 640 du wide (FLT CONTROL / TRIM, ELEC / TEST): the scroll bar is drawn over the right plate edge. Check the A-10C scroll pages too.

#### Known limitations

- [ ] F-16C: the MFD screen is empty (DCS-BIOS has no MFD text and the export script table of the F-16C is empty).
- [ ] F-16C DED: inverse and big characters (`DED_L1_FORMAT` to `DED_L5_FORMAT`) are not drawn; the five lines are plain text.
- [ ] F-16C DEFOG lever: five positions. A value set in the cockpit between them is none of the positions.
- [ ] F-16C drawing simplifications: the WHEELS are three legend lamps, the eyebrows are lamp grids (the real strips are diagonal), the AoA indexer is three lamps (the real one has chevrons), the ECM modules are three rows of two, the threat warning azimuth scope is not drawn, EXT LIGHTING has no COVERT bracket or POSITION title, the RCL and ENTR key faces of the ICP are blank, the INS knob labels are shortened (NORM, IN FLT) and its angles are a compromise.
- [ ] F-16C cold start ([F16C/STARTUP.md](F16C/STARTUP.md)) stops at Before Taxi step 6; the Taxi steps 7 to 10 (throttle, brakes, nosewheel steering check) are not included.

### Developer test kit

#### Needs a test in DCS

- [ ] The test kit has not been run on Windows yet: the `python` / `python3` choice, the folder creation in `gen_json.lua` and the real Saved Games DCS-BIOS folder.

#### Known limitations

- [ ] `bridge.py` reads the key table of `core/keys.py` up to `class KEYBDINPUT`, so that marker must stay.
- [ ] The docstring of `core/tools/test/smoke.py` still says "_ACFT_NAME=A-10C_2 is re-sent every second".
- [ ] The full sweep takes about 4 minutes.
- [ ] `sim.py` resolves ids over all JSON files of the DCS-BIOS folder: an id that two aircraft share (`CANOPY_POS`, `DEFOG_LEVER` in the A-10C and the F-16C) needs `--json` with the folder of one aircraft.
- [ ] `smoke.py` without `--acft` tests the A-10C (default `A-10C_2`), so a page name of another aircraft is not found: always pass `--acft`, or change the default to the AH-64D.
- [ ] `coverage.py` cannot name a panel kit tab: the F-16C DED tab has no `####` page section in its spec, so it is not covered.

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
| 2026-10-21 | A-10C: the long-hold page list with 29 entries was taller than the screen and cut off entries | The page list scrolls inside its card ([F16C/ENGINE.md](F16C/ENGINE.md) F1) | `core/tools/test/sweep.js --acft A-10C_2` opens every page-list entry (320 PASS); not yet on the iPad |
