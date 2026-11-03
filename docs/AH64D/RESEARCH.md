# AH-64D Apache – research notes

Working notes for the AH-64D Apache (Block II) in the dashboard. Our own notes only: the manual, its text and its pictures are copyrighted and are never committed, and neither are the owner's cockpit photos. They are read from the places named below and kept outside the repo.

Status: built and mature, tested in DCS in both seats; the tests that are still open are in the AH-64D section of [../FIXES.md](../FIXES.md#ah-64d-mature). Phases 0 to 6 and 8 done; phase 7 done as far as the owner tested; phase 9 open.

## Decisions

- Aircraft: AH-64D Apache only (DCS-BIOS module `AH-64D`, the DCS aircraft `AH-64D_BLK_II`).
- Tabs: **COCKPIT | FLIGHT | FIGHT | MPD | KU | GEORGE**. COCKPIT is the cockpit map with one page per panel; the MPD tab also holds the TEDAC (CP/G seat). KU and GEORGE exist for the AH-64D only.
- Two seats: PILOT and CP/G, a seat badge, a debug seat that looks at the pages of the other seat, and pages that exist in one seat only.
- Look: the plate look `ah64d` of the panel kit (the default look), drawn from the owner's cockpit photos.
- Keypresses where DCS-BIOS cannot do it: the power levers, the canopy, the monocle, the controls overlay, the trim reset and George (the game's AI crew member).
- AI: not part of the product. George is the game's own AI crew member and only has buttons on the GEORGE tab.
- Aircraft choice: automatic, as for every aircraft (`_ACFT_NAME` `AH-64D_BLK_II`).
- Reference material (manual pages, photos) is used to draw the panels; it stays out of the repo.

## Sources

| Source | Where | Notes |
| --- | --- | --- |
| DCS AH-64D Flight Manual (EN) | In the DCS install under `Mods/aircraft/AH-64D/Doc/` | A PDF; printed page numbers equal PDF page numbers. Relevant: cockpit overview and panels pp. 104–127, TEDAC pp. 128–135, cyclic and collective grips pp. 136–141, EUFD pp. 155–163, MPD p. 164, start-up procedures pp. 255–266, CMWS (Aircraft Survivability Equipment chapter) pp. 630–631 |
| Quick Start Manuals | In the same folder | Short introductions to the module; the inventory ([PANELS.md](PANELS.md)) and the cold start ([STARTUP.md](STARTUP.md)) follow the Flight Manual |
| DCS-BIOS module | `Scripts/DCS-BIOS/lib/modules/aircraft_modules/AH-64D.lua` (DCS-Skunkworks, v1.2d), control list `doc/json/AH-64D.json` | One module `AH-64D` for the DCS aircraft `AH-64D_BLK_II`; 714 controls (353 `PLT_`, 328 `CPG_`, 33 without a seat), 562 of them take commands (273 pilot, 284 CP/G, 5 radio frequencies) |
| Default keybinds | In the DCS install under `Mods/aircraft/AH-64D/Input/`, and the owner's exported or changed binds | The defaults are the standard AH-64D binds; the George keys are not DCS defaults and were bound once by the owner ([SPEC.md](SPEC.md#9-keybinds)) |
| Cockpit photos | One per panel, straight on, taken by the owner | Kept outside the repo and not listed by file name; the panel pages were drawn from them ([PICTURES.md](PICTURES.md)) |
| DCS cockpit definition `clickabledata.lua` | In the DCS install, in the AH-64D module | Which parts of the cockpit can be clicked, with their value ranges; read together with the DCS-BIOS position tables |
| Our own research | Git tag `research-v1` | The Stage 1 to 3 specs (`docs/STAGE1.md`, `STAGE2.md`, `STAGE3.md`), the COCKPIT specs and the original research scripts, with the full result tables |

Live text in DCS-BIOS: the 14 EUFD lines of each seat (they carry the radio frequencies), the KU scratchpad of each seat, the CMWS counts and status, the current seat (`SEAT_POSITION`). The MPD button labels come from the export script (`list_indication`), not from DCS-BIOS.

## Method

The AH-64D was the first aircraft. The dashboard did not exist when it started, so it went through the method of the first specs (tag `research-v1`, `docs/SPEC.md`), not through the phases of the A-10C and the F-16C.

**Stage by stage, each ending with a go / no-go decision**

1. **Stage 1, read all data.** DCS-BIOS stream decoding and a Lua export script, a log of every value, test runs on Windows in both seats, cold start and a short flight. Every value group got a result: readable, partly readable, implausible. Radios and the generic engine values did not fit the Apache, the MPD text and the control positions did. Go: the dashboard can read what it needs ([SPEC.md](SPEC.md#what-dcs-allows-for-the-ah-64d)).
2. **Stage 2, check what is controllable.** A sweep of every DCS-BIOS control of the current seat with readback (pilot 227 pass, 12 fail, 29 skipped on the blocklist, 5 sent-unverified; CP/G 238, 18, 27, 1), a keypress test (George 9 of 9 in both seats, power levers 8 of 8 in the pilot seat), and a review of every failure. Go: only controls that passed go on the dashboard, in the order a pilot uses them.
3. **Stage 3, the dashboard.** One view at a time: STARTUP (later replaced by COCKPIT), FLIGHT, FIGHT, MPD, KU. Each view was built, checked in a browser against a simulated DCS-BIOS and then, as far as the owner tested, in DCS with the iPad. STARTUP got a cold start to both power levers at FLY from the tablet alone.
4. **COCKPIT pages.** A cockpit map and one page for every panel, 21 pages in both seats, with guarded controls. The first tablet test found nine problems (screws not aligned, the same button in different sizes, pop-ups in the middle of the screen, invisible switch bands, a FIRE page that did not work because DCS's own cover was closed, ...). The fix round gave the panel kit, one scale for all pages, the switch chooser and the real covers.
5. **Later work from the tablet and DCS tests.** The GEORGE tab (key sequences, changed after tests in DCS: staggered keys, longer holds, a pause scale), the debug seat, one FIGHT page per seat with the gunner controls and the TKR pad, the 56 px touch rule for every view.

**What the A-10C and F-16C method added, applied to the AH-64D afterwards (this doc set).** The two later aircraft were planned in phases 0 to 9 with one document per phase. The AH-64D got the same documents after the build, written from the manual, the DCS-BIOS module and the aircraft file, and checked against what the tests in DCS showed:

- [PANELS.md](PANELS.md): the inventory of every control the manual names (252 rows in 34 panels), not only the ones that got a page.
- [BIOS.md](BIOS.md): every one of the 714 DCS-BIOS controls with its input kind, build type and position order, from the classification table of `core/tools/test/bios_check.py`, checked against `aircraft/ah64d.py`; a position order that the tests confirmed is marked `tested in DCS`, one that is a guess starts with `guess:`.
- [STARTUP.md](STARTUP.md): the pilot's cold start in 135 steps.
- [PICTURES.md](PICTURES.md): which picture shows each panel. The photos are not available to these notes, so the quality column is derived from the build history.
- [ENGINE.md](ENGINE.md): the engine features that exist because of this aircraft, with their place in the code and the decisions behind them.
- [SPEC.md](SPEC.md): the 13 sections of the other two aircraft, with a fit line per page, the touch sizes measured with `core/tools/test/sweep.js`, the list of what is not on the dashboard and the manual test run.

Limits, said plainly: these documents describe what is built, they did not plan it; the AH-64D was not rebuilt with the later method. The engine changes the A-10C and the F-16C needed ([../A10C/ENGINE.md](../A10C/ENGINE.md), [../F16C/ENGINE.md](../F16C/ENGINE.md)) were not needed for the AH-64D, because the engine grew out of it. PICTURES.md rates no panel good and one partial (MASTER ZEROIZE has no photo); the rest is "not rated".

## Open points

Everything that needs DCS or a look on the iPad, and the limitations of the build, is in the AH-64D section of [../FIXES.md](../FIXES.md#ah-64d-mature).

## Questions

Collected from [SPEC.md](SPEC.md) for the owner's review: 32 lines, 19 `Question:` and 13 `Decided:`. Choices the build took as recommended (or another choice, which the line says) are written as `Decided:` there; the open ones are `Question:`. One line each, by topic. The question about the CP/G power lever keys is in the spec twice (POWER page and Keybinds) and is listed under both.

**Seats**

- Question: Does the long hold on the seat badge (the debug seat) work with a finger on the tablet?

**Panel pages: rules and look**

- Decided: one scale for all pages, so the small panels no longer fill the screen; four identical rectangular corner ears per plate with the screw in the centre, where the photos show ears of different heights (owner review).
- Decided: the rotary positions of the chooser sit on a small circle at their real dial angles (owner review).
- Decided: a guarded control needs the cover, then a single tap, with no hold and no chooser; the 1 s hold of the first fix round was removed (owner review).
- Decided: the arrangement and the text of the pages follow the photos; the places where they do not are the EUFD, CENTER, the ICS / PTT labels on COMM, the wiper labels and the PARK BRAKE name (owner review).
- Question: How do the chooser (button size, arc of the dials, placement near the screen edges) and the knob grip (24 ridges, second rim of the large knobs) feel on the iPad?

**POWER**

- Decided: the power levers and FRICT keep one touch band per mark and the knob bar, no chooser (owner review).
- Question: Are the CP/G power lever keys (`RAlt` / `RShift` with `Home`, `PageUp`, `PageDown`, `End`) right in the CP/G seat? They are tested in the pilot seat only.
- Question: Are the hold times right (ENG START 0.5 s, APU button 0.3 s), is the APU ON lamp green, and is the FRICT slider direction right (taken from the photos, not from DCS)?

**EXT / INTR LT**

- Question: The end of the SIGNAL knob sweep was taken from the photo, not from DCS: check it in DCS.

**FIRE DET/EXTG**

- Question: Are ENG 1, APU and ENG 2 FIRE confirmed by their own readback once the real cover is open, or must the RDY lamp confirm them?
- Question: Does the bridge open and close DCS's own cover in both seats (`cover open`, `pressed`, `cover closed`, no `not confirmed`)? PRI and RES with a fire button armed have never been sent; do them last in a throwaway mission.
- Question: The manual does not give the colours of the DISCH lights: check them in DCS.

**STORES JETT**

- Question: The six station selects and JETT with a station armed have never been sent in DCS; do them last in a throwaway mission.

**ARMAMENT**

- Decided: MASTER ZEROIZE is a plain placard drawn without a photo (owner review).
- Question: Check the lamp colours ARM (amber), SAFE (green) and GND ORIDE (amber) in DCS; MASTER ZEROIZE with its real cover has never been sent in DCS.

**EUFD**

- Decided: the display is on top and the controls sit in a row below it, not around the glass as on the photo; the glass is 568 × 280 du so the 14 lines of 56 characters stay readable (owner review).

**CMWS**

- Question: CMWS JETT has never been sent in DCS; do it last in a throwaway mission.

**CENTER**

- Decided: one wide plate over two plates, 16 du apart on shared edge lines, not the arrangement of the photo (owner review).
- Decided: the wiper labels PARK, OFF, LO and HI are flat text in a fan above the dial, not turned along the dial as on the photo (owner review).
- Decided: the PARK BRAKE name is printed on two lines, because on one line it runs into the plate margin and the corner ear (owner review).

**COMM**

- Decided: the ICS name and its PTT label sit in the SOL row between the FM 1 and FM 2 squelch switches, and the switch itself with VOX and HOT MIC is below the row, not as on the photo (owner review).
- Decided: the PULL chip is exempt from the 56 px touch floor of the layout checker; its floor is 32 px and the long press (0.6 s) on its knob is the large target (owner review).
- Question: Does `PULL OUT` fit and read in the font the iPad uses (Helvetica Neue instead of Arial Narrow and Arial), and is the long press on the knob comfortable?

**WIPER / DEFOG**

- Decided: as on CENTER, the wiper labels are flat text in a fan above the dial (owner review).

**FLIGHT**

- Question: Are the directions of the trim ring and the tick right after a few trims in DCS?

**FIGHT**

- Question: The hats WAS, SIGHT SEL and TADS FOV and the SENSOR selector of the gunner page are under 56 px high, because the 7 × 3 grid has no room for two-row hats (a fourth grid row, eight columns or less chrome per cell would give it). Which one?
- Question: Do IAT, OFS and OFS ALL do what the grip does, is the switch mapping right (IAT forward = 2, OFS aft = 0, rest 1), and are the TADS FOV letters and the SENSOR mapping (FLIR 2, TV 1) right?

**MPD**

- Question: Do the MPD live labels follow page changes, does the MODE knob work (NT through the INC / DEC fallback), are the cursor speed and the up / down direction right, and in the CP/G seat do the TEDAC controls and the TKR pad (four directions, dead zone, slew ramp) work?

**GEORGE**

- Question: Do the GEORGE buttons work in DCS with the new timing (hold 0.15 s, pauses 0.5 / 1.0 / 0.6 s, staggered keys), which ones, and does the Target List appear and take PREV / NEXT TARGET, SELECT TARGET, TRACK / ENGAGE, ROE HOLD / FREE, FIRE and EXIT LIST?

**Lamp row**

- Question: Are the lamp colours APU ON (green), ARM (amber), SAFE (green) and GND ORIDE (amber) right in DCS?

**Keybinds**

- Question: Are the CP/G power lever keys right in the CP/G seat? (The same question as under POWER.)

## Plan

| Phase | What | Who | Output | Status |
| --- | --- | --- | --- | --- |
| 0 | Scope and decisions | user, Claude | Decisions above | done |
| 1 | Read all data (Stage 1): DCS-BIOS stream, export script, a log of every value, both seats, cold start and a short flight | user flies, Claude builds | Tag `research-v1` (Stage 1 spec, `stage1_read.py`, result table); summary in [SPEC.md](SPEC.md#what-dcs-allows-for-the-ah-64d) (section 10, What DCS allows) | done |
| 2 | Control sweep (Stage 2): every DCS-BIOS control of the current seat with readback, the keypress test for George and the power levers, review of the failures | user flies, Claude builds | Tag `research-v1` (Stage 2 spec, `stage2_sweep.py`); pilot 227 pass, 12 fail, 29 skipped, 5 sent-unverified; CP/G 238, 18, 27, 1; power levers by keypress | done |
| 3 | Dashboard first views (Stage 3): STARTUP (later replaced by COCKPIT), FLIGHT, FIGHT, MPD with the TEDAC, KU; bridge, page, settings, confirmed presses | Claude builds, user tests | `core/dashboard.py`, `core/web/index.html`, `aircraft/ah64d.py`; Stage 3 spec in the tag; a cold start from the tablet alone worked | done |
| 4 | COCKPIT pages and panel kit: the cockpit map, one page per panel (21 pages in both seats), guarded controls with the bridge guard window | Claude builds, user tests | `docs/COCKPIT.md` in the tag; the map and the pages in `aircraft/ah64d.py` | done |
| 5 | Fix rounds from the tablet tests: the panel kit with one scale and aligned screws, the switch chooser, pop-ups at the control, the knob look, the real DCS covers, a tap on a guarded control instead of the hold | user tests on the iPad, Claude fixes | `docs/COCKPIT_FIXES.md` in the tag (9 findings, 12 decisions); `core/panel_kit.py`, `core/tools/check_panels.js` | done |
| 6 | GEORGE tab, debug seat, gunner FIGHT page, TKR pad | user tests, Claude builds | GEORGE tab with 17 buttons, one FIGHT page per seat, `digital` stick; [SPEC.md](SPEC.md) sections 4 and 7 | done |
| 7 | Research in DCS: the keys, the covers, the lamp colours, the position orders, the buttons never sent | user flies, Claude analyses | Test results in the specs and in [../FIXES.md](../FIXES.md#ah-64d-mature) | done as far as the owner tested; the open tests are in FIXES.md |
| 8 | Docs in the common format of the three aircraft | Claude writes | [PANELS.md](PANELS.md): 252 rows in 34 panels; [BIOS.md](BIOS.md): 714 DCS-BIOS controls, all covered; [STARTUP.md](STARTUP.md): 135 steps; [PICTURES.md](PICTURES.md); [ENGINE.md](ENGINE.md); [SPEC.md](SPEC.md): 13 sections | done |
| 9 | Test run in DCS ([SPEC.md](SPEC.md) section 13), open points updated | user flies, Claude fixes | FIXES.md | open |
