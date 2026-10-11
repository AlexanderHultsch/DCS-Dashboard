# Fixes and open points

Temporary: delete the entries when they are fixed or moved to [SPEC.md](SPEC.md).

## Fix specification: debug seat view and gunner FIGHT page

Status: specified, not built. When built and tested, move the result into [SPEC.md](SPEC.md) and delete this section.

### 1. Debug seat view (long hold on the badge)

Goal: look at the pilot or the CP/G pages without sitting in that seat, for debugging.

- **Gesture.** A long hold (0.6 s, like the long press on the COMM knobs) on the seat badge (`PILOT`, `CP/G`, `NO DCS DATA`, `BRIDGE OFFLINE`) steps through the debug views: the seat you are not in, then back to the real state. In `NO DCS DATA` or `BRIDGE OFFLINE` there is no real seat: the cycle is off, `CP/G`, `PILOT`, off. A plain tap on the badge does nothing, as now.
- **View only.** The debug seat only changes what the page shows. The page resolves `{seat}` ids with the debug seat, so lamps, positions and the seat-specific pages are the ones of that seat (the values of both seats are already in `/state`). Every control stays disabled (`usable()` is false), so no command can leave the page. The bridge is not changed and never sees the debug seat.
- **Badge.** `DEBUG CP/G` or `DEBUG PILOT`, in the amber read-only style, in place of the normal text. With no DCS data the pages show their empty state.
- **Not remembered.** The debug seat is held in the page only and is gone after a reload, so it can never linger.
- **Tabs.** The tab bar and the pages follow the debug seat exactly as they follow a real seat (section 2).

### 2. One FIGHT tab, one page per seat

- The pilot and the CP/G get **separate FIGHT pages**: two views named `Fight`, one with `"seats": [0]` and one with `"seats": [1]`. The tab bar shows one FIGHT tab; it opens the page of the current seat (real or debug). The same rule is used for any view name that exists once per seat.
- Page code: `buildTabs` makes one tab per view name (not per view); `showView` / the tab click picks the view of that name whose `seats` contain the current seat; `followSeat` (today only for panel pages) applies to all views, so a seat change switches FIGHT to the page of the new seat. The remembered tab (`TAB_KEY`) is the name.
- **Pilot FIGHT**: today's page with `"seats": [0]` and nothing else changed (A/S, GND ORIDE, WAS, SIGHT SEL, FLARE, CHAFF, the counts, the four CMWS selectors).

### 3. Gunner FIGHT (CP/G seat)

Same 3 x 7 grid and style as the other FIGHT page. Ids are written out as `CPG_...` (the page exists for one seat only). Lamp row: MASTER WARNING and MASTER CAUTION (tappable), ARM, SAFE, GND ORIDE.

| Cells | Control | DCS-BIOS | Notes |
| --- | --- | --- | --- |
| row 1, col 1 | A/S | `CPG_MASTER_ARM_BTN` | as today |
| row 1, col 2 | GND ORIDE | `CPG_GROUND_OVERRIDE_BTN` | as today |
| row 2, col 1 | FLARE | `CPG_CYCLIC_FLARE` | as today |
| row 2, col 2 | CHAFF | `CPG_CYCLIC_CHAFF` | as today |
| row 3, cols 1 and 2 | FLARE COUNT, CHAFF COUNT | `PLT_CMWS_FLARE_COUNT`, `PLT_CMWS_CHAFF_COUNT` | as today |
| row 1, cols 3 and 4 | WAS | `CPG_CYCLIC_WEAPON_UD` / `_LR` | as today (up G, down A, left R, right M); the left-grip WAS stays out unless the cyclic one fails |
| row 2, cols 3 and 4 | SIGHT SEL | `CPG_RHG_SIGHT_UP_DN` / `CPG_RHG_SIGHT_L_R` | **right grip**, replaces the collective one: up HMD, left FCR, right TADS, down LINK |
| row 1, cols 5 and 6 | TADS FOV | `CPG_LHG_TADS_FOV_UP_DN` / `CPG_LHG_TADS_FOV_L_R` | left grip cross: up **Z**, left **N**, right **W**, down **M**. Hat convention as the other hats: up and right 2, down and left 0, rest 1 |
| row 2, cols 5 and 6 | SENSOR | `CPG_LHG_TADS_SEL` | selector FLIR / TV; the third position (DVO) has no function in DCS and is shown greyed |
| row 1, col 7 | IAT | `CPG_LHG_TEDAC_L_IAT` | momentary, forward position: starts an auto-track on the target under the TADS reticle (or updates the aim point inside the gates) |
| row 2, col 7 | OFS | `CPG_LHG_TEDAC_L_IAT` | momentary, aft position, **short** (0.15 s): drops the primary track when the reticle is inside the gates, or returns the TADS to the track when it is outside |
| row 3, col 7 | OFS ALL | `CPG_LHG_TEDAC_L_IAT` | the aft position held **0.8 s** (a press over 0.5 s): deletes all tracks |
| row 3, col 3 | SLAVE | `CPG_RHG_SIGHT_SLAVE` | push button: slaves / de-slaves the selected sight to the acquisition source |

- IAT, OFS and OFS ALL are three buttons on one switch (3 positions, spring to rest 1): they send the position, hold it, and return to 1 (`rest`, `hold`), like the other momentary selectors. Which of 0 and 2 is IAT and which is OFS is taken from the grip (IAT forward, OFS aft, forward = 2 as for the other hats) and **must be confirmed in DCS**, together with the SENSOR mapping (FLIR forward = 2, TV 1, DVO 0).
- Not on the page because DCS-BIOS has no entry: the weapon trigger and the LRFD (laser) trigger. They could become key buttons later (needs key bindings in DCS, like George).
- Left out on purpose (not asked for): FCR mode and scan switches, FLIR polarity, laser tracker mode, MTT promote, cursor extras, STORE and LMC. They can be added to free cells later.
- Free cells: row 3, cols 4 to 6.

### 4. MPD / TEDAC tab: manual tracker instead of the cursor

- In the CP/G seat, when the TEDAC is selected on the MPD tab, the **CURSOR group** (pad, CURSOR SWITCH DISPLAY, ENTER) is replaced by the **TKR group**: a track pad and the SLAVE button. LEFT MPD and RIGHT MPD keep the cursor group, the pilot seat is unchanged.
- **TKR pad** = the right-grip Sight Manual Tracker (`CPG_RHG_MAN_TRK_UP_DN`, `CPG_RHG_MAN_TRK_L_R`). The pad looks and feels like the cursor pad (finger anywhere, the distance from the touch point is the deflection), but the tracker has **three states per axis** (0, 1 = centre, 2): the bridge turns the deflection into 0 / 1 / 2 with a dead zone of 30 % of the full deflection, sends only changes, and returns to 1 when the finger lifts. DCS ramps the slew rate while the switch is held (option MAN TRK ramp-up speed).
- Implementation: the existing `stick` control gets a flag `"digital": true`; `move_stick` in the bridge then sends 2 / 0 / 1 instead of the 0 to 65535 range. The page code of the pad is reused. The up / down sign has to be confirmed in DCS, like the cursor (`CURSOR_Y_SIGN`).
- SLAVE sits under the pad in both places (TEDAC tab and gunner FIGHT).

### 5. Build steps and checks

1. Page: debug seat (badge hold, `resolve`, `usable`, badge text), tab per name, `followSeat` for all views. Check against the fake DCS-BIOS: the hold cycles in every status, controls are disabled, a reload clears it, the tab follows a real seat change and the debug seat.
2. Aircraft data: split FIGHT into the pilot page and the gunner page (table above); add the TKR group to the TEDAC selection. Check: `/layout` has both FIGHT views, every id exists in DCS-BIOS (startup check), POST each new control in seat 1 (momentary hold and return to rest, refused in seat 0).
3. Bridge: `digital` stick. Check: pad deflections produce 0 / 1 / 2 with the dead zone, only changes are sent, release sends 1.
4. Browser at 1180 x 820 and 1024 x 768, both seats and the debug seat: no overlap, nothing clipped, every touch target at least 44 px, the MPD tab with TEDAC shows the TKR group and the other two displays keep the cursor.
5. Docs: move this section into SPEC.md (views, bridge interface), update the test list below.

### 6. Tests in DCS (add to the list below when built)

- IAT / OFS / OFS ALL do what the grip does; mapping of the three switch positions.
- TADS FOV letters (Z N W M) and the SENSOR mapping.
- SIGHT SEL from the right grip, SLAVE.
- TKR pad: direction of all four axes, the dead zone, the slew ramp.

## Open points

### Needs a test in DCS

- [ ] Fire buttons: are ENG 1, APU and ENG 2 FIRE confirmed by their own readback once the real cover is open? If ENG 1 is still `not confirmed` with the cover open, confirm with the RDY lamp (`{S}_ENG_1_READY_L`) instead of the button.
- [ ] Real covers: the bridge opens DCS's own cover for ENG 1, APU and ENG 2 FIRE, MASTER ZEROIZE and CMWS JETT (waits up to 0.5 s for the readback, closes it about 1 s after the command). Check in both seats: the log shows `cover open`, `pressed`, about 1 s later `cover closed`, and no `not confirmed`.
- [ ] Guarded controls never sent before: station selects, PRI and RES (with a fire button armed), JETT (with a station armed), ZEROIZE, MASTER ZEROIZE, CMWS JETT. Do them last in a throwaway mission.
- [ ] Hold times: ENG START switch (0.5 s) and APU button (0.3 s).
- [ ] Lamp colours: APU ON (green), ARM (amber), SAFE (green), GND ORIDE (amber), DISCH lights of PRI and RES.
- [ ] Flare and chaff counts: only checked against the simulated DCS-BIOS, which has no text values.
- [ ] Flares and chaff in the air with the CMWS set up; note which presses show "not confirmed".
- [ ] If the cyclic WAS does not act in the CP/G seat, swap to the TEDAC grip hats (LHG WAS, RHG sight select).
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
- [ ] GEORGE AIR AREA SEARCH, POINT SEARCH and PHS SEARCH still work with the changed sequence (Hide, Show first; the ring stays open).

### Needs a look on the iPad

- [ ] Knob grip look: the ridge count (24) and the second rim of the large knobs may need tuning.
- [ ] Chooser: button size, the arc of the dials, placement near the screen edges.
- [ ] PULL chips on COMM: `PULL OUT` fits and reads in the font the iPad uses (checked in Arial Narrow and Arial; the iPad may use Helvetica Neue); the long press (0.6 s) on the knob is comfortable.
- [ ] The deviations from the photos below: say which ones to change.

### Known limitations

- [ ] The layout is made for 1024 × 768 and larger; smaller screens overlap.
- [ ] The panel pages need CSS container queries: Safari / iPadOS 16 or newer, or current Chrome.
- [ ] CP/G left MPD L1–L6 do not respond in DCS.
- [ ] MPD labels: which labels are boxed (selected) is not shown; long labels can overlap their neighbours.
- [ ] Refusal log lines show the unexpanded `{seat}_...` id (cosmetic).
- [ ] MASTER ZEROIZE has no photo and is a plain placard. The CP/G COMM and WIPER / DEFOG pages use the same drawings as the pilot's COMM and CENTER pages.
- [ ] Grip controls with guards (CHOP, BUCS, emergency jettison) are not on the dashboard.
- [ ] George: the FLIGHT and COMBAT commands of George as pilot are not on the dashboard until the ring mode is understood. Open questions for a later test: does the ring always open in the same mode? does Hide and Show reset a list or sub-menu?
- [ ] George: the weapon-release buttons (FIRE, TRACK / ENGAGE, ROE HOLD / FREE, POINT SEARCH, SELECT TARGET) are unguarded on purpose for now. A guard for grid buttons would be a page change: first tap arms for 5 s, second tap fires.
- [ ] George: the ROE state (HOLD FIRE or FREE FIRE) is not readable; read the colour of the ring text.
- [ ] George: the ring state is not readable. The bridge assumes the ring is hidden at the start of a ring command and starts with Hide.
- [ ] Open questions: radios on the dashboard (later?); which keyboard combinations for cockpit commands are used today (each one would become a button).

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
