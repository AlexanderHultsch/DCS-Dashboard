# Fixes and open points

Temporary: delete the entries when they are fixed or moved to [SPEC.md](SPEC.md).

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
- [ ] GEORGE ring buttons (SHOW RING, HIDE RING): the ring opens and closes in both seats.
- [ ] GEORGE search buttons (PHS SEARCH, AREA SEARCH, POINT SEARCH, STOP / TADS FWD): George reacts; AREA and POINT SEARCH only with George not tracking, POINT SEARCH with a TSD point selected.
- [ ] GEORGE target and control buttons (STORE TARGET with a tracked target; REQUEST CONTROL twice in the CP/G seat: George takes the controls, then gives them back).
- [ ] GEORGE WEAPON NEXT: the ring stays open and the weapon label changes (NO WPN, GUN, MSL, RKT).
- [ ] George ring commands: confirm that Hide, Show, then the direction really leaves the ring hidden at the end, and that the pauses (0.3 / 0.4 / 0.3 s) are long enough; confirm that a long press of 1.2 s is accepted.
- [ ] George keys bound exactly as in the table in [SPEC.md](SPEC.md) (section GEORGE), including the AH-64D George AI Helper entries.

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
- [ ] George: no FIRE button, on purpose (a wrong tap can shoot).
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
