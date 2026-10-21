# DCS-Dashboard – F-16C Viper

Specification of the F-16C Viper (Block 50) dashboard as built in phase 8. It is tested only against a simulated DCS-BIOS, none of it in DCS; the keypress controls are not built, because they wait for the F-16C keybinds (section 8) and the owner does not have the module yet. The engine all aircraft share is in [../SPEC.md](../SPEC.md); the engine changes this aircraft needs and their decisions are in [ENGINE.md](ENGINE.md). Controls are named as in [PANELS.md](PANELS.md), DCS-BIOS identifiers are in [BIOS.md](BIOS.md), reference pictures in [PICTURES.md](PICTURES.md), the cold start in [STARTUP.md](STARTUP.md), the decisions and the method in [RESEARCH.md](RESEARCH.md). The structure follows the A-10C spec, [../A10C/SPEC.md](../A10C/SPEC.md).

Choices made while writing the spec and during the build are written at the end of the section where they are made: a `Decided:` line where the planner took the recommendation (or another choice, which the line says) and the owner reviews it at the end, a `Question:` line where it is still open. All are collected in [RESEARCH.md](RESEARCH.md), Questions.

## 1. Overview

A tablet dashboard for the single-seat F-16C Viper, with the same tabs as every aircraft: **COCKPIT | FLIGHT | FIGHT | MFD | DED**. The same bridge serves all aircraft; it chooses the F-16C files when DCS-BIOS reports the aircraft `F-16C_50` (section 9).

| Tab | Content | A-10C counterpart |
| --- | --- | --- |
| COCKPIT | Map of the cockpit; 21 panel pages and 3 link boxes (section 2) | COCKPIT |
| FLIGHT | Gear, ALT FLAPS, lights, brake switch, speed brake position, engine, fuel and hydraulic bars (section 3); the TRIM key hat and the keys for speed brake and nosewheel steering are reserved, not built yet | FLIGHT |
| FIGHT | Master arm, laser arm, RF, countermeasure counts and controls, ECM (section 4); the TMS, DMS and CMS key hats are reserved, not built yet | FIGHT |
| MFD | Left and right MFD, drawn by the `mfcd` layout of the A-10C, one at a time (section 5) | MFCD |
| DED | The live DED and the ICP keypad as one panel kit page (section 6) | CDU |

Differences to the A-10C: the throttle is not drawn and not moved (DCS-BIOS has only the OFF to IDLE move, `THROTTLE_OFF_IDLE`, which is the guarded button THROTTLE CUTOFF on FUEL / EPU / START), the DED tab is a panel kit page and not a hand-drawn layout, the HOTAS key hats are planned in 2 × 2 grid cells from the start, the controls that sit on instruments get a page (INSTRUMENTS), the panel pages have a look of their own (section 10), and one seat, no trim display and no GEORGE tab as on the A-10C. Built on the engine changes F1 to F8 of [ENGINE.md](ENGINE.md) and the changes E1 to E10 of the A-10C.

**Built (phase 8 of [RESEARCH.md](RESEARCH.md)):** the aircraft file `aircraft/f16c.py` with 21 panel pages, the FLIGHT, FIGHT, MFD and DED tabs, and the engine changes F1 to F8. **Not built yet:** the keypress controls. They need the F-16C default keybinds, which are unknown until they are exported from DCS (section 8): the key hats TMS, DMS, CMS and TRIM, the speed brake keys and the nosewheel steering key. Their cells are reserved in the FLIGHT and FIGHT grids (sections 3 and 4) so nothing moves when they are added. The module, the cockpit screenshots (throttle, canopy switch and handle, handcrank, ANTI-G TEST button, right console fittings, CHAFF/FLARE button; [PICTURES.md](PICTURES.md)) and the DCS checks of phase 7 are still to come. The F-16C file has no `KEYS` until then, so the bridge needs no F-16C key.

## 2. COCKPIT

COCKPIT is a simplified map of the F-16C cockpit and one page for every cockpit panel that has a function in DCS, with every button, switch, knob, lamp and display of that panel. Tap a box on the map to open its page; on a page the COCKPIT tab keeps its highlight and shows a back chevron, and one tap on it goes back to the map; a long hold (0.5 s) on COCKPIT opens a list of every page (the list scrolls, ENGINE.md F1). The boxes MFD L, MFD R and DED / ICP are not pages: they open the MFD tab (left or right side preselected) and the DED tab, as the A-10C map boxes open MFCD and CDU. The F-16C has one seat, so there is no seat badge switch and no seat-dependent page: every page is always on the map and in the list.

Tabs at the top: **COCKPIT | FLIGHT | FIGHT | MFD | DED**.

The panel pages have the F-16C look (section 10); this section says which panels are on which page and where. The instruments (SAI, airspeed and Mach indicator, altimeter, AoA indicator, VVI, ADI, EHSI, fuel flow, engine instruments, magnetic compass, fuel quantity, hydraulic, EPU fuel and cabin pressure gauges, clock, PFLD, the threat warning scope and the HUD) are not panel pages and are not drawn (section 11); FLIGHT shows a few of their values as bars (section 3). The small controls that sit on an instrument (cage knob, set knobs, mode switch, clock knob) and the FUEL QTY SEL panel are on one page, INSTRUMENTS. The HOTAS grips are controls for FLIGHT and FIGHT, not panel pages. The lamp row (section 7) stays at the top of the map and of every panel page.

**Lamps.** The MARKER BEACON lamp has no control and is not on a page; it goes to the lamp row (section 7). The warning lamps of the eyebrows and the AoA indexer and AR status lights are on the EYEBROWS / INDEXERS page, the gear lamps on LANDING GEAR / HMCS, the caution lamps on CAUTION; section 7 repeats the most important ones.

**The map** is a 12 × 7 grid, `[row, col, rows, cols]`, of plain boxes with the panel placard, in the order of the real cockpit, front at the top: the left console in columns 1 to 4 (the long left console in columns 1 to 2, the left auxiliary console and the UHF backup panel beside the throttle in columns 3 to 4), the front dash in columns 5 to 8, the right console in columns 9 to 12 (the right auxiliary console and the front of the right console in columns 9 to 10, the right console in columns 11 to 12). Names in brackets are not boxes (the throttle is on FLIGHT and FIGHT). `:` continues the box above. The sketch shortens some names; the table has the full ones.

```
    left console                          | front dash                                  | right console
    outbd             inbd                |                                             | inbd              outbd
 1  CANOPY/DEFOG      LANDING GEAR/HMCS   | EYEBROWS / INDEXERS                         | CAUTION           LIGHTING/AIR COND
 2  FUEL/EPU/START    CMDS                | MISC       MFD L      DED/ICP    MFD R      | :                 OXYGEN/ANTI-ICE
 3  FLT CONTROL/TRIM  THREAT WARNING      | :          :          :          :          | HUD CONTROL       AVIONICS POWER
 4  ELEC/TEST         UHF/IFF BACKUP      | :          INSTRUMENTS                      | SNSR/VMS/ZEROIZE  :
 5  EXT LIGHTING      :                   |            :                                | :
 6  ECM               (throttle)          |            SEAT                             |
 7  AUDIO             (throttle)          |            :                                |
```

| Page | Grid | Panels on the page |
| --- | --- | --- |
| CANOPY / DEFOG | [1,1,1,2] | Canopy Switch and Canopy Handle (p. 73), DEFOG Lever (p. 74), Canopy Jettison T-Handle (p. 74) |
| FUEL / EPU / START | [2,1,1,2] | FUEL Control Panel (p. 67), EPU Control Panel (p. 64), ENG & JET START Control Panel (p. 63) |
| FLT CONTROL / TRIM | [3,1,1,2] | FLT CONTROL Panel (p. 71), MANUAL TRIM Panel (p. 72), Manual Pitch Override Switch (p. 62) |
| ELEC / TEST | [4,1,1,2] | ELEC Control Panel (p. 64), TEST Panel (p. 72) |
| EXT LIGHTING | [5,1,1,2] | EXT LIGHTING Control Panel (p. 69) |
| ECM | [6,1,1,2] | ECM Control Panel (p. 706) |
| AUDIO | [7,1,1,2] | AUDIO 1 Control Panel (p. 65), AUDIO 2 Control Panel (p. 65) |
| LANDING GEAR / HMCS | [1,3,1,2] | Landing Gear Panel (p. 55), HMCS Control Panel (p. 57), ALT GEAR Handle (p. 57) |
| CMDS | [2,3,1,2] | CMDS Control Panel (p. 697), CHAFF/FLARE Dispense Button (p. 708) |
| THREAT WARNING | [3,3,1,2] | Threat Warning Prime Control Panel (p. 695), Threat Warning Azimuth Indicator (p. 694), Threat Warning Auxiliary Control Panel (p. 696) |
| UHF / IFF BACKUP | [4,3,2,2] | IFF Control Panel (p. 67), UHF Backup Control Panel (p. 260) |
| EYEBROWS / INDEXERS | [1,5,1,4] | Left Eyebrow Lights (p. 45), Right Eyebrow Lights (p. 46), AoA Indexer (p. 44), AR Status / NWS Indicator (p. 45) |
| MISC | [2,5,3,1] | Miscellaneous (MISC) Panel (p. 47), Autopilot controls (pp. 129 to 132) |
| MFD L (link) | [2,6,2,1] | opens the MFD tab, left side |
| INSTRUMENTS | [4,6,2,3] | FUEL QTY SEL Panel (p. 54), Standby Attitude Indicator (SAI) (p. 49), Airspeed and Mach Indicator (p. 51), Altimeter (p. 51), Attitude Director Indicator (ADI) (p. 53), Electronic Horizontal Situation Indicator (EHSI) (p. 230), Mechanical Clock (p. 61) |
| SEAT | [6,6,2,3] | Ejection Seat Controls (pp. 81, 82), SEAT ADJ Switch (p. 80) |
| DED / ICP (link) | [2,7,2,1] | opens the DED tab |
| MFD R (link) | [2,8,2,1] | opens the MFD tab, right side |
| CAUTION | [1,9,2,2] | Caution Light Panel (p. 59) |
| HUD CONTROL | [3,9,1,2] | HUD Control Panel (p. 94) |
| SNSR PWR / VMS / ZEROIZE | [4,9,2,2] | SNSR PWR Control Panel (p. 75), VOICE MESSAGE Switch (p. 80), ZEROIZE Switch (p. 80) |
| LIGHTING / AIR COND | [1,11,1,2] | Interior LIGHTING Control Panel (p. 76), AIR COND Control Panel (p. 76) |
| OXYGEN / ANTI-ICE | [2,11,1,2] | OXYGEN Regulator Panel (p. 77), ENGINE ANTI-ICE Switch (p. 78), ANT SEL Panel (p. 78) |
| AVIONICS POWER | [3,11,2,2] | AVIONICS POWER Control Panel (p. 78) |

24 boxes: 3 link boxes and 21 panel pages. A box is named after the placard of its panel; a page with several panels joins the names with ` / `.

**Rules for the pages**

- **Plates.** A page is one plate per physical panel inside the 640 × 600 du budget of the panel kit (touch minimum 56 px, see [../SPEC.md](../SPEC.md) section 7). Several panels on one page are separate plates, 16 du apart, as on the AH-64D CENTER page. Lamps and displays are drawn on the plate; a lamp is a touch target only where the real lamp is part of a button (MASTER CAUTION, the threat warning buttons, the ECM module buttons).
- **Fit.** The yardstick is the AH-64D COMM page: 26 touch targets (volume knobs, PULL chips, switches) fill the whole budget. Every page below has a `Fit` line with its size in du as built (the estimate from the real panel kit parts, method below, is in brackets), and says `fits` or `scroll page`. A page that does not fit is a **scroll page** (next rules); it is never split and no plate moves to another page. As built, 8 of the 21 pages are scroll pages (CANOPY / DEFOG, FUEL / EPU / START, FLT CONTROL / TRIM, ELEC / TEST, LANDING GEAR / HMCS, CMDS, UHF / IFF BACKUP, INSTRUMENTS), and so is the DED tab (section 6); the other 13 fit. The estimate named seven; FUEL / EPU / START became a scroll page when the throttle cutoff button joined the ENG & JET START plate, and the built pages are larger than the estimates almost everywhere (turned plate names, the stacking rules of `PanelGroup`). AUDIO ended 6 du over the 540 du margin and stays a fixed page.
- **How the estimate is made.** Each plate is laid out in rows of parts, and a part takes a cell (width × height in du: the part, its printed name of 24 du, its position labels of 20 du and an 8 du gap): TOGGLE 100 × 124 (guarded 112 × 152), PUSH 100 × 108 (guarded 116 × 140), ROUND 88 × 88, PUSH_SMALL 72 × 72, KNOB_S 100 × 104 (with a PULL chip 100 × 134), KNOB_M 108 × 120, ROTARY 140 × 156, step rocker (ROCKER) 84 × 156, SLIDER 108 × 300, LAMP 80 × 48, LAMP_WIDE 144 × 48, BAR 80 × 252 (the 40 × 200 bar with its percentage and name), a display its own size plus 8. In the estimate, `R rows × C parts` is the number of rows of a plate and the most parts in one row (a lamp counts as a part). A row is as wide as its cells less 8 du and as high as its tallest cell; a plate is its rows plus the 36 du margin on every side (72 du more in both directions); the plates of a page are 16 du apart and packed left to right in cockpit order, a new row when the next plate does not fit in 640 du. This gives the A-10C CAUTION page its 640 × 640 du (12 rows of LAMP_WIDE). Every cell of a part with a touch target (lamps and bars have none) is at least 72 du wide and high, so every touch target can be widened to 58 du, which is 56 px at the scale 0.958 of a 1024 × 768 screen (a 56 du knob or PUSH_SMALL, the 60 du toggle square and the 52 × 60 du half of a rocker all reach it). **Decision rule:** the A-10C estimates were wrong for 9 of 23 pages, so a page counts as `fits` only up to 540 du high (600 du less 10 %); a taller estimate makes it a scroll page. No page is wider than 640 du.
- **No function in DCS.** A control that the manual calls N/I, "no function" or "not functional" is left off the page and listed in section 11 with its DCS-BIOS identifier. Exceptions stay: lamps (so a lamp grid stays whole: CAUTION, TF-FAIL) and the two controls the cold start names although the manual calls them N/I (the DL switch, step 49; the diluter lever, steps 99 and 108). A position that does nothing stays on the dial, greyed out (ADF on the UHF function knob, A on the A-3-2 knob, BIT on the CMDS PRGM knob, AUTO BRT on the HUD brightness switch, CAL on the INS knob). The weapon release (ALT REL) and the ejection handle are also left off (section 11).
- **Scroll page.** Only a page whose plates do not fit is flagged `scroll` in the aircraft file; every other page keeps the fixed 640 × 600 du budget. A scroll page keeps the width of 640 du and the scale of every page (parts stay the same size) and is as tall as its plates, at most 1800 du (`scroll=True` on the `Panel` or `PanelGroup`). Only its plate area scrolls, vertically; the tabs, the lamp row and the settings button stay fixed. The scroll area has a visible frame, an always visible scroll bar at its right edge and a shaded edge with a small chevron where more of the page is hidden. A touch that moves is a scroll and never a tap, a hold or a knob turn. The page opens at the top. ENGINE.md says the same for the page list (F1).
- **Throttle.** The throttle lever has no DCS-BIOS output; only the move between OFF and IDLE is `THROTTLE_OFF_IDLE` (`likely`), as the guarded button THROTTLE CUTOFF on FUEL / EPU / START (the engine has guarded controls on panel pages only, not in the FLIGHT grid). MIL and MAX AB are the real throttle. No page has a lever.
- **Step rockers.** A dial that has no absolute DCS-BIOS input, only a step input, is an up / down rocker (a `hat` with `steps`, [../SPEC.md](../SPEC.md) section 8) and shows no state: SET INDEX (`AIRSPEED_SET_KNB`), barometric setting (`ALT_BARO_SET_KNB`), heading set (`EHSI_HDG_SET_KNB`), course set (`EHSI_CRS_SET_KNB`) and clock wind (`CLOCK_WIND`), all on INSTRUMENTS. The windows beside them show the result.
- **Selectors with many positions.** A knob with more than 8 positions is a step rocker even where DCS-BIOS gives it an absolute input: the UHF channel knob (20 presets) and the 10, 1 and 0.1 MHz knobs (10 positions). The chooser does not scroll (FIXES.md) and a ring of marks would be too dense; the windows beside the rockers show the result. The A-3-2 and 0.025 MHz knobs (3 and 4 positions) are chooser knobs. A selector with a long list of positions that must stay a chooser (DEFOG) is cut to 5 positions.
- **Spring-loaded switches.** A switch that springs back in the cockpit is drawn with its rest position and held for the press time: the JFS, probe heat, FLCS PWR TEST, canopy, altimeter mode and SEAT ADJ switches, the MAL & IND LTS switch, the MFD rockers and the ICP rocker, DCS and DRIFT C/O switches (those listed as spring in BIOS.md), and the FLCS BIT, OBOGS BIT, EPU/GEN and MANUAL PITCH switches, which DCS-BIOS defines as plain toggles (check in DCS). The PITCH switch of the autopilot is not in the list: it is a plain three-position selector, because DCS holds it with a solenoid and a momentary press would drop the autopilot (check in DCS).
- **Guarded controls.** Controls that end the flight or cannot be undone get the guarded-control rule of the AH-64D spec (a cover, then a tap): EMER STORES JETTISON, HOOK, ALT GEAR (LANDING GEAR / HMCS), FUEL MASTER (real DCS cover `FUEL_MASTER_CV`), TANK INERTING, the EPU switch, ENG CONT (real cover `ENG_CONT_SW_COVER`), the CMDS JETT switch, the CANOPY JETTISON T-handle, ZEROIZE (real cover `ZEROIZE_SW_COVER`) and THROTTLE CUTOFF (OFF / IDLE) on FUEL / EPU / START. Eleven controls; three of them use a real DCS cover, whose position order is guessed (0 = CLOSE, 1 = OPEN, BIOS.md). The EPU switch has a dashboard cover only: its two DCS covers `EPU_SW_COVER_OFF` and `EPU_SW_COVER_ON` are not used (check in DCS whether the switch moves with them closed). The cover is the engine's guard cover on every guarded control, not the red flip guard of the real FUEL MASTER, EPU, ENG CONT and ZEROIZE switches (a look point, FIXES.md). The ejection handle is not on the dashboard.
- **Cold start.** STARTUP.md uses every page except AUDIO, CMDS, THREAT WARNING, MISC, SEAT and LIGHTING / AIR COND. Its gauge checks (fuel flow, steps 31; oil pressure, nozzle, RPM and FTIT, steps 32 to 35 and 61; hydraulic A and B, steps 36 and 37) are on FLIGHT as bars except the fuel flow; the EPU fuel gauge (step 77) is read in DCS.

### Panel pages

Counts: `rows` = rows of the PANELS.md tables of the panels on the page; `id` = rows with a DCS-BIOS identifier; `read only` = lamps, gauges and text (no command); `left off` = rows that are not on the page (section 11). `Plus` = controls that exist only in DCS-BIOS and clearly belong to the page. Pictures are the image names of PICTURES.md. A page lists its panels in the order of the cockpit, front to back and top to bottom. Part sizes and the way the sizes are estimated are in the rules above.

#### CANOPY / DEFOG

- **Panels:** Canopy Switch and Canopy Handle (p. 73), DEFOG Lever (p. 74), Canopy Jettison T-Handle (p. 74).
- **Arrangement:** three plates. In the cockpit the canopy switch and lever are on the left cockpit wall, the DEFOG lever and the CANOPY JETTISON T-handle at the top of the left console. On the page: the canopy plate and the DEFOG plate side by side, the T-handle plate below them.
- **Controls:** 4 rows (2 + 1 + 1), 4 id, 0 read only, 0 left off. On the page: 4 controls and 1 bar. Plus: `CANOPY_POS` (canopy position, read only, shown as the bar). The manual canopy handcrank has no identifier (section 11).
- **Special:** the canopy switch (OPEN, HOLD, CLOSE) is spring-loaded to HOLD: OPEN and CLOSE are held for the press time (the manual says CLOSE must be held until the canopy is down); the canopy lever (LOCKED, UNLOCKED; order guessed) lights the CANOPY warning lamp, which is on the lamp row (section 7); its own position output `CANOPY_LOCK` is not used. The CANOPY JETTISON T-handle (PULL, STOW; order guessed) is a guarded control; DCS-BIOS has no cover for it, so the cover is the dashboard's. The DEFOG lever has 21 positions (MIN to MAX); the page draws a chooser with five of them (MIN, 5, 10, 15, MAX), because the chooser does not scroll and a slider (a `knob`) only sends 0 to 65535 while `DEFOG_LEVER` takes 0 to 20. A value set in the cockpit between these steps is none of the five positions.
- **Picture:** `p073-002.jpg` (poor), `p074-005.jpg` (good), `p074-002.jpg` (good); screenshot needed: Canopy Switch and Canopy Handle.
- **Fit:** scroll page, 580 × 612 du as built (estimate 532 × 596): CANOPY 420 × 332 beside DEFOG 144 × 332, CANOPY JETTISON 264 × 264 below the canopy plate.

Decided: the DEFOG lever is a chooser with five positions (MIN, 5, 10, 15, MAX). The first plan was a slider like the AH-64D friction lever, then a chooser with 21 buttons, which did not fit the screen (owner review).

Question: Worth an engine change, so that the lever shows all 21 positions (a chooser that scrolls, or a slider with a maximum)?

#### FUEL / EPU / START

- **Panels:** FUEL Control Panel (p. 67), EPU Control Panel (p. 64), ENG & JET START Control Panel (p. 63).
- **Arrangement:** three plates in one row in the cockpit (top of the left console), left to right: FUEL, EPU, ENG & JET START. On the page: FUEL on top, EPU and ENG & JET START below it; the ENG & JET START plate also holds the guarded THROTTLE CUTOFF button.
- **Controls:** 13 rows (4 + 4 + 5), 13 id, 4 read only, 2 left off (AB RESET Switch, MAX POWER Switch). On the page: 8 controls and 4 lamps (the RUN lamp and the three EPU lamps). Plus: `THROTTLE_OFF_IDLE` (the throttle cutoff, read and command).
- **Special:** FUEL MASTER (MASTER, OFF) shuts the fuel to the engine and is a guarded control with the real DCS cover `FUEL_MASTER_CV`; TANK INERTING (halon, cannot be undone) is a guarded control without a DCS cover; the ENG FEED knob has four positions (OFF, NORM, AFT, FWD); AIR REFUEL (OPEN, CLOSE). The EPU switch (OFF, NORM, ON) is a guarded control with a dashboard cover only; DCS-BIOS has two covers for it, `EPU_SW_COVER_OFF` (over OFF) and `EPU_SW_COVER_ON` (over ON; the manual lists neither), which are not used; lamps EPU (green), AIR and HYDRAZN (yellow). The JFS switch (START 1, OFF, START 2) is spring-loaded to OFF and held for the press time; START 2 is the cold start position. The ENG CONT switch (PRI, SEC) has a red cover in the cockpit and a real DCS cover, `ENG_CONT_SW_COVER`, so it is a guarded control; RUN lamp green. THROTTLE CUTOFF is a guarded push button (`THROTTLE_OFF_IDLE`, label OFF / IDLE) on the ENG & JET START plate: the move of the throttle between OFF and IDLE, moved here from FLIGHT because the FLIGHT grid cannot hold a guarded control (section 3). AB RESET and MAX POWER are left off (section 11).
- **Picture:** `p067-002.jpg` (partial), `p064-002.jpg` (good), `p063-002.jpg` (partial).
- **Fit:** scroll page, 640 × 708 du as built (estimate 628 × 452, fits): FUEL 640 × 252 above EPU 288 × 264 beside ENG & JET START 336 × 440.

Decided: the EPU switch has one dashboard cover; the two DCS covers are not used, because the engine knows one cover id per control. Check in DCS whether the switch moves with its DCS covers closed (owner review).

Decided: ENG CONT is guarded with its DCS cover, although SEC is reversible (as the A-10C UHF LOAD cover); the cold start then needs a cover tap before steps 59 and 62 (owner review).

#### FLT CONTROL / TRIM

- **Panels:** FLT CONTROL Panel (p. 71), MANUAL TRIM Panel (p. 72), Manual Pitch Override Switch (p. 62).
- **Arrangement:** three plates. In the cockpit FLT CONTROL is at the upper left of the left console, MANUAL TRIM below it, and the manual pitch override switch (a guard on each side) at the upper right near the throttle. On the page: FLT CONTROL on top, MANUAL TRIM and the override switch (MANUAL PITCH) side by side below it, because a column of three plates is impossible in a `PanelGroup`.
- **Controls:** 12 rows (7 + 4 + 1), 12 id, 1 read only, 2 left off (MANUAL TF FLY-UP Switch, LE FLAPS Switch). On the page: 9 controls and 2 lamps (RUN green, FAIL red).
- **Special:** DIGITAL BACKUP (OFF, BACKUP), ALT FLAPS (NORM, EXTEND), FLCS RESET (OFF, RESET) and FLCS BIT (OFF, BIT) are two-position toggles with guessed orders; FLCS BIT springs back to OFF in the cockpit. The ROLL TRIM and PITCH TRIM wheels and the YAW TRIM knob are continuous knobs that show their own position (the indicator outputs `ROLLTRIMIND` and `PITCHTRIMIND` are not used); TRIM/AP DISC (NORM, DISC). The MANUAL PITCH override switch (NORM, OVRD) is held in OVRD while pressed. MANUAL TF FLY-UP and LE FLAPS are left off (section 11).
- **Picture:** `p071-002.jpg` (partial), `p072-002.jpg` (partial), `p062-005.jpg` (good).
- **Fit:** scroll page, 626 × 664 du as built (estimate 544 × 596): FLT CONTROL 626 × 282 above MANUAL TRIM 454 × 366 beside MANUAL PITCH 156 × 240. The turned plate names take part of the width.

Decided: FLCS BIT, MANUAL PITCH, EPU/GEN and OBOGS BIT are drawn spring-loaded (held 0.5 s, back to rest), although they are plain toggles in DCS-BIOS; check in DCS (owner review).

#### ELEC / TEST

- **Panels:** ELEC Control Panel (p. 64), TEST Panel (p. 72).
- **Arrangement:** two plates. In the cockpit TEST is at the left edge of the left console and ELEC at its lower centre. On the page: ELEC above TEST, the order of the cold start.
- **Controls:** 17 rows (10 + 7), 17 id, 9 read only, 0 left off. On the page: 8 controls and 12 lamps.
- **Special:** MAIN PWR (MAIN PWR, BATT, OFF) and the ELEC CAUTION RESET button, which also clears MASTER CAUTION and ELEC SYS; eight amber lamps in the figure's order: FLCS PMG, MAIN GEN, STBY GEN, EPU GEN, EPU PMG, then under the ACFT BATT bracket TO FLCS, FLCS RLY and FAIL. TEST: FIRE & OHEAT DETECT and MAL & IND LTS test buttons (held while pressed); OBOGS BIT (momentary); PROBE HEAT (PROBE HEAT, OFF, TEST; spring-loaded); EPU/GEN test (momentary); FLCS PWR TEST (MAINT, NORM, TEST; spring-loaded to NORM, held at TEST for cold start step 3); the four FLCS PWR lamps A to D.
- **Picture:** `p064-013.jpg` (good), `p072-013.jpg` (partial).
- **Fit:** scroll page, 592 × 816 du as built (estimate 524 × 584): ELEC 344 × 430 above TEST 592 × 370.

#### EXT LIGHTING

- **Panels:** EXT LIGHTING Control Panel (p. 69).
- **Arrangement:** one plate: the POSITION block (FLASH / STEADY, WING / TAIL, FUSELAGE toggles), ANTI-COLL, FORM, MASTER and AERIAL REFUELING knobs below and beside it.
- **Controls:** 7 rows, 7 id, 0 read only, 0 left off. On the page: 7 controls.
- **Special:** WING / TAIL and FUSELAGE have three positions (BRT, OFF, DIM); ANTI-COLL has eight (OFF, 1, 2, 3, 4, A, B, C); MASTER has five (OFF, ALL, A-C, FORM, NORM; the figure prints COVERT over the middle three); FORM and AERIAL REFUELING are continuous knobs (the manual: wing tips only with WING / TAIL at OFF; the receptacle lights only with AIR REFUEL at OPEN). The external model outputs of DCS-BIOS (section 11) are not used. The COVERT bracket over the middle MASTER positions and the POSITION title are not drawn.
- **Picture:** `p069-085.jpg` (good).
- **Fit:** fits, 620 × 460 du as built (estimate 560 × 344): one plate.

#### ECM

- **Panels:** ECM Control Panel (p. 706).
- **Arrangement:** one plate: the OPR / STBY / OFF toggle, the XMIT toggle and the DIM knob at the left, the RESET and BIT buttons under them, and the two rows of four module buttons (1 to 4, then 5, a blank spare, FRM, SPL) as in the figure. On the page the module buttons are three rows of two, each with its four lamps beside it.
- **Controls:** 13 rows, 13 id, 0 read only, 4 left off (RESET Button, BIT Button, ECM Module Control Button FRM, ECM Module Control Button SPL). On the page: 9 controls (power, XMIT, DIM and six module buttons) and 24 lamps (S, A, F and T for each module).
- **Special:** the ECM power switch has three positions (OPR, STBY, OFF; STBY warms the pod for about 3 minutes); XMIT has 1, 2 and 3 (1 and 2 deception, with CMDS at SEMI or AUTO; 3 noise, with CMDS at MAN); each module button has four lamps: S standby, A active, F failed, T transmitting. Module 6 is the unmarked button. DCS-BIOS defines the module buttons as toggles (0 out, 1 in, latching); the page draws push buttons that send 1 and then 0 after 0.3 s, which may only flash the module in (check in DCS; a latching push button would be an engine addition). The T lamps are blue in DCS-BIOS and are drawn white, because the kit has no blue lamp. RESET and BIT are left off, and so are the FRM and SPL buttons with their lamps (section 11).
- **Picture:** `p706-002.jpg` (partial).
- **Fit:** fits, 626 × 520 du as built (estimate 584 × 512): one plate.

#### AUDIO

- **Panels:** AUDIO 1 Control Panel (p. 65), AUDIO 2 Control Panel (p. 65).
- **Arrangement:** two plates, one above the other as in the cockpit (AUDIO 1 above AUDIO 2, bottom right of the left console).
- **Controls:** 12 rows (8 + 4), 12 id, 0 read only, 4 left off (SECURE VOICE Volume Knob, TF Volume Knob, INTERCOM Volume Knob, HOT MIC CIPHER Switch (Microphone Switch)). On the page: 8 controls.
- **Special:** the COMM 1 (UHF) and COMM 2 (VHF) power / volume knobs are continuous knobs (fully counter-clockwise = radio off), each with its mode knob beside it (OFF, SQL, GD, order guessed; GD tunes 243.0 / 121.5 MHz); MSL and THREAT tone volumes; TACAN volume; the ILS power / volume knob (counter-clockwise = OFF). The SECURE VOICE, TF, INTERCOM and HOT MIC CIPHER controls are left off (section 11).
- **Picture:** `p065-002.jpg` (good).
- **Fit:** fits, 616 × 546 du as built (estimate 544 × 508): AUDIO 1 616 × 324 above AUDIO 2 616 × 206. Six du over the 540 du margin, kept as a fixed page because it is within 600 du.

#### LANDING GEAR / HMCS

- **Panels:** Landing Gear Panel (p. 55), HMCS Control Panel (p. 57), ALT GEAR Handle (p. 57).
- **Arrangement:** three plates. In the cockpit the landing gear panel is at the top of the left auxiliary console with the CMDS panel below it, the HMCS panel under that and the ALT GEAR handle at the lower left of the console. On the page: the landing gear plate on top, the ALT GEAR and HMCS plates side by side below it.
- **Controls:** 14 rows (12 + 1 + 1), 14 id, 2 read only, 0 left off. On the page: 13 controls, 4 lamps and 1 bar. Plus: `GEAR_ALT_BTN` (the push-to-reset button of the ALT GEAR handle, read and command).
- **Special:** the EMER STORES JETTISON button (hold 1 s; drops tanks, racks and free-fall stores), the HOOK switch (UP, DN; the hook cannot be fully retracted from the cockpit) and the ALT GEAR handle (PULL, STOW) are guarded controls without DCS covers. The LG handle is a plain selector (UP, DOWN) with its red warning lamp `LIGHT_GEAR_WARN` in the handle, and the three green WHEELS lamps (nose, left, right) are also on the FLIGHT lamp row (section 7); GND JETT ENABLE; BRAKES channel (CHAN 1, CHAN 2); the PARKING BRAKE / ANTI-SKID switch (PARKING BRAKE, ANTI-SKID, OFF; the figure says PARKING BRAKE, the text ANTI-SKID); DN LOCK REL; STORES CONFIG (CAT I, CAT III); HORN SILENCER; LANDING / TAXI lights (LANDING, OFF, TAXI); the SPEED BRAKE position as a read-only bar (`SPEEDBRAKE_INDICATOR`; the cockpit window shows CLOSED, dots or stripes). HMCS: one symbology brightness knob (`HMCS_INT_KNB`). Drawing simplifications: the WHEELS are three legend lamps (NOSE, LEFT, RIGHT), not the silhouette of the manual figure, and the GEAR WARN lamp stands beside the handle.
- **Picture:** `p055-005.jpg` (partial), `p057-002.jpg` (good), `p057-011.jpg` (partial).
- **Fit:** scroll page, 640 × 898 du as built (estimate 564 × 796): LANDING GEAR 640 × 642 above ALT GEAR 300 × 240 beside HMCS 324 × 200.

Decided: EMER STORES JETT, HOOK and ALT GEAR (one-way) are guarded; DN LOCK REL and GND JETT ENABLE are not (owner review).

#### CMDS

- **Panels:** CMDS Control Panel (p. 697), CHAFF/FLARE Dispense Button (p. 708).
- **Arrangement:** two plates. In the cockpit the CMDS panel is on the left auxiliary console below the landing gear panel (status and quantity windows on top, switches and knobs below) and the CHAFF/FLARE button on the left wall, just aft of the canopy lever. On the page: CMDS above the button.
- **Controls:** 13 rows (12 + 1), 13 id, 2 read only, 4 left off (O1 Switch, O2 Switch, JMR Switch, MWS Switch). On the page: 7 controls, 4 lamps and 2 displays.
- **Special:** the status lamps NO GO, GO, DISP and RDY (`LIGHT_CMDS_NO_GO`, `LIGHT_CMDS_GO`, `LIGHT_CMDS_DISP`, `LIGHT_CMDS_RDY`) and the two count windows (`CMDS_CH_AMOUNT`, `CMDS_FL_AMOUNT`, 4 characters each); RWR, CH and FL toggles (ON, OFF); the JETT switch (JETT, OFF) dumps all chaff and flares in any mode and is a guarded control without a DCS cover; the PRGM knob (BIT, 1, 2, 3, 4; BIT greyed out, N/I) picks the manual program for CMS forward; the MODE knob (OFF, STBY, MAN, SEMI, AUTO, BYP). The CHAFF/FLARE button dispenses program 5 in MAN, SEMI and AUTO. O1, O2, JMR and MWS are left off, and so are the O1 and O2 counts (section 11).
- **Picture:** `p697-011.jpg` (good), `p708-032.jpg` (poor); screenshot needed: CHAFF/FLARE Dispense Button.
- **Fit:** scroll page, 600 × 668 du as built (estimate 576 × 580): CMDS 600 × 448 above CHAFF/FLARE 204 × 204.

#### THREAT WARNING

- **Panels:** Threat Warning Prime Control Panel (p. 695), Threat Warning Azimuth Indicator (p. 694), Threat Warning Auxiliary Control Panel (p. 696).
- **Arrangement:** three plates. In the cockpit the prime control panel and the azimuth indicator are at the upper left of the instrument panel and the auxiliary control panel is on the left auxiliary console. On the page: prime panel and azimuth indicator side by side, the auxiliary panel below.
- **Controls:** 13 rows (6 + 2 + 5), 12 id, 0 read only, 1 left off (Azimuth scope). On the page: 12 controls: 6 prime buttons, 4 auxiliary buttons and 2 brightness knobs (azimuth indicator, DIM).
- **Special:** every button is a lit push button with its lamps on the face (upper and lower legend): HANDOFF (`RWR_HANDOFF_BTN`, lamps `LIGHT_RWR_HANDOFF_H`, `LIGHT_RWR_HANDOFF_UP`), MODE (OPEN, PRIORITY), LAUNCH (MISSILE LAUNCH), TGT SEP (`RWR_T_BTN`), UNKNOWN (U) and SYS TEST (hold 1 s); SEARCH (S), ACT/PWR (ACTIVITY, POWER), ALTITUDE (ALT, LOW) and POWER (`RWR_PWR_BTN`, SYSTEM POWER, a toggle in DCS-BIOS; built as a push button that sends 1 and then 0, check in DCS as for the ECM module buttons). The azimuth scope itself has no DCS-BIOS output and is not drawn; the plate holds its brightness knob (`RWR_INTENS_KNB`). The DIM knob (`RWR_IND_DIM_KNB`) dims both panels.
- **Picture:** `p695-002.jpg` (good), `p694-004.jpg` (good), `p696-002.jpg` (good).
- **Fit:** fits, 600 × 504 du as built (estimate 564 × 468): PRIME 364 × 304 beside AZIMUTH 220 × 304 above AUX 600 × 184.

#### UHF / IFF BACKUP

- **Panels:** IFF Control Panel (p. 67), UHF Backup Control Panel (p. 260).
- **Arrangement:** two plates. In the cockpit the IFF panel is left of centre on the left console and the UHF backup panel at its right side beside the throttle; the C & I knob of the IFF panel moves IFF and UHF control to these two panels (BACK UP). On the page: the IFF plate above the UHF plate.
- **Controls:** 20 rows (7 + 13), 20 id, 2 read only, 9 left off (MASTER Knob, M-4 CODE Switch, ENABLE Switch, MODE 1 & MODE 3 Thumbwheel Selectors, MODE 4 REPLY Switch, MODE 4 MONITOR Switch, Preset Channel Card & Access Door, TONE Button, VOL Knob). On the page: 12 controls and 2 displays. IFF: only the C & I knob works. UHF: the two windows (CHAN, 2 characters; frequency, 7 characters), TEST DISPLAY, STATUS and 9 more controls.
- **Special:** C & I knob (UFC, BACK UP; order guessed). The UHF function knob has four positions (OFF, MAIN, BOTH, ADF; ADF greyed out, no function), the mode knob three (MNL, PRESET, GRD), the A-3-2 knob three (A, 3, 2; A is anti-jam, N/I, greyed out), the squelch toggle two. The preset channel knob (20 presets) and the 10, 1 and 0.1 MHz knobs (10 positions each) have absolute DCS-BIOS inputs but more than 8 positions: each is drawn as a step rocker (up / down, no state; the CHAN and FREQUENCY windows show the result). The A-3-2 knob and the 0.025 MHz knob (00, 25, 50, 75) are chooser knobs. The left-to-right order of the four frequency knobs is assumed. STATUS is "press and hold" in the manual and is held 0.3 s. The IFF MASTER, M-4 CODE, ENABLE, thumbwheel, MODE 4 REPLY and MONITOR controls, the preset card door, the TONE button and the VOL knob are left off (section 11).
- **Picture:** `p067-013.jpg` (partial), `p260-002.jpg` (good).
- **Fit:** scroll page, 600 × 840 du as built (estimate 636 × 688): IFF 264 × 232 above UHF BACKUP 600 × 592.

Decided: the UHF channel (20) and the 10, 1 and 0.1 MHz knobs are step rockers, not chooser knobs, because of their number of positions; A-3-2 and 0.025 MHz are chooser knobs (owner review).

Decided: the IFF panel keeps only the C & I knob and shares the page with the UHF backup panel, because that knob hands control to it (owner review).

#### EYEBROWS / INDEXERS

- **Panels:** Left Eyebrow Lights (p. 45), Right Eyebrow Lights (p. 46), AoA Indexer (p. 44), AR Status / NWS Indicator (p. 45).
- **Arrangement:** four plates. In the cockpit: the left eyebrow (MASTER CAUTION, TF-FAIL, F-ACK, IFF IDENT) above the MISC panel, the right eyebrow with eight warning lamps above the right MFD, the AoA indexer at the left and the AR status / NWS indicator at the right of the HUD frame. On the page: left eyebrow beside the AoA indexer, right eyebrow beside the AR / NWS indicator.
- **Controls:** 20 rows (4 + 8 + 4 + 4), 20 id, 15 read only, 0 left off. On the page: 5 controls and 15 lamps. The two dimming levers are continuous knobs (`AOA_INDEX_BRT_KNB`, `AR_STATUS_BRT_KNB`).
- **Special:** MASTER CAUTION is a lit push button (lamp `LIGHT_MASTER_CAUTION`, press `MASTER_CAUTION` resets it) and is also on the lamp row; F-ACK (`F_ACK_BTN`) and IFF IDENT (`IFF_ID_BTN`) are push buttons; TF-FAIL has no function in the Block 50 and stays as a lamp. Right eyebrow, left to right as in the figure: ENG FIRE, ENGINE, HYD / OIL PRESS (one id for the split light), FLCS, DBU ON, TO / LDG CONFIG (one id), CANOPY, OXY LOW. AoA indexer: red (high), green (on speed), yellow (low) as `LIGHT_AOA_UP`, `LIGHT_AOA_MID`, `LIGHT_AOA_DN`. AR status / NWS: RDY (blue in DCS-BIOS, drawn white), AR / NWS (green), DISC (red). Drawing simplifications: the eyebrows are lamp grids (the real strips are diagonal) and the AoA indexer is the three lamps HIGH, OPT and LOW (the real one has chevrons).
- **Picture:** `p045-002.jpg` (good), `p046-002.jpg` (good), `p044-002.jpg` (good), `p045-013.jpg` (good).
- **Fit:** fits, 624 × 508 du as built (estimate 624 × 444): LEFT EYEBROW 364 × 284 beside AoA INDEXER 244 × 284 above RIGHT EYEBROW 364 × 208 beside AR / NWS 244 × 208.

Decided: the eyebrow lamps and the two indexers are one page (controls: F-ACK, IFF IDENT, MASTER CAUTION, two dimming levers); the lamp row carries the main ones (owner review).

#### MISC

- **Panels:** Miscellaneous (MISC) Panel (p. 47), Autopilot controls (pp. 129 to 132).
- **Arrangement:** one narrow plate in the cockpit (top to bottom: RF, ECM lamp, LASER ARM, ALT REL, MASTER ARM, ADV MODE, then ROLL and PITCH at the bottom). On the page it is one plate of three rows of two: RF and the ECM lamp, LASER ARM and MASTER ARM, ROLL and PITCH. The autopilot has no panel of its own: its ROLL and PITCH switches are on this panel, the paddle switch is on the stick (section 4, not built) and the heading set knob is on INSTRUMENTS.
- **Controls:** 8 rows (8 + 0), 8 id, 1 read only, 2 left off (ALT REL Button, ADV MODE Button). On the page: 5 controls and 1 lamp (ECM, green).
- **Special:** RF switch (NORM, QUIET, SILENT; limits emissions of the radar, IFF, datalink, ECM pod, TACAN and radar altimeter); LASER ARM (LASER ARM, OFF); MASTER ARM (MASTER ARM, OFF, SIMULATE); autopilot ROLL (HDG SEL, ATT HOLD, STRG SEL) and PITCH (ALT HOLD, A/P OFF, ATT HOLD); the PITCH switch is a plain three-position selector, not spring-loaded: in the cockpit a solenoid holds it in ALT HOLD or ATT HOLD, and a momentary press would drop the autopilot (check in DCS). ALT REL (the backup weapon release) and ADV MODE with its two lamps are left off (section 11).
- **Picture:** `p047-002.jpg` (partial).
- **Fit:** fits, 522 × 412 du as built (estimate 364 × 312): one plate.

Decided: ALT REL is left off the dashboard like the stick weapon release, so a tablet tap never releases a weapon (owner review).

#### INSTRUMENTS

- **Panels:** FUEL QTY SEL Panel (p. 54), Standby Attitude Indicator (SAI) (p. 49), Airspeed and Mach Indicator (p. 51), Altimeter (p. 51), Attitude Director Indicator (ADI) (p. 53), Electronic Horizontal Situation Indicator (EHSI) (p. 230), Mechanical Clock (p. 61).
- **Arrangement:** the controls that sit on the flight instruments, plus the FUEL QTY SEL panel (bottom of the centre column, right of the EHSI). The instruments themselves are not drawn. On the page: four plates in a 2 × 2 grid, not in this order: AIR DATA / SAI / ADI (the air data, SAI and ADI knobs) beside FUEL QTY SEL in the first row, EHSI beside CLOCK in the second.
- **Controls:** 14 rows (2 + 1 + 1 + 2 + 1 + 6 + 1), 14 id, 3 read only, 0 left off. On the page: 15 touch parts and 4 displays (the EHSI range, course and the two mode windows). The control rows make 15 parts because the heading set, course set and clock knobs are a step rocker plus a push button each and the SAI knob has a PULL chip.
- **Special:** FUEL QTY SEL knob (NORM, RSVR, INT WING, EXT WING, EXT CTR; TEST is the separate id `FUEL_QTY_SEL_T_KNB`, which has no readback and is left off, section 11) and the EXT FUEL TRANS switch (NORM, WING FIRST). Step rockers (up / down, no state, the result shows on the instrument): SET INDEX (`AIRSPEED_SET_KNB`), barometric setting (`ALT_BARO_SET_KNB`), heading set (`EHSI_HDG_SET_KNB`), course set (`EHSI_CRS_SET_KNB`) and clock wind (`CLOCK_WIND`). Beside them: the heading and course push buttons (`EHSI_HDG_SET_BTN`, `EHSI_CRS_SET`), the EHSI mode button (`EHSI_MODE`), the clock set pull (`CLOCK_SET`), the altimeter mode switch (ELEC, PNEU; the OFF centre position is the rest; spring-loaded), the ADI pitch trim knob (`ADI_PITCH_TRIM`, continuous) and the SAI PULL TO CAGE knob (turn `SAI_PITCH_TRIM`, pull `SAI_CAGE`, drawn with a PULL chip IN 0 / OUT 1; `SAI_CAGE` is a push button in DCS-BIOS, check the direction in DCS). The EHSI shows its range (`EHSI_RANGE`), course (`EHSI_COURSE`) and the selected mode (`EHSI_MODE_LEFT`, `EHSI_MODE_RIGHT`) as text. The gauge rows of these instruments are not drawn (section 11).
- **Picture:** `p054-002.jpg` (good), `p049-002.jpg` (good), `p051-002.jpg` (partial), `p051-017.jpg` (good), `p053-002.jpg` (good), `p230-002.jpg` (good), `p061-011.jpg` (good).
- **Fit:** scroll page, 640 × 952 du as built (estimate 568 × 748): AIR DATA / SAI / ADI 380 × 468 beside FUEL QTY SEL 244 × 468, above EHSI 380 × 468 beside CLOCK 244 × 266.

Decided: the controls on instruments get a page, INSTRUMENTS (the A-10C left them out); the cold start needs the altimeter (steps 112, 113), the SAI cage (69) and FUEL QTY SEL (70 to 76), HDG SEL the heading knob (owner review).

Decided: FUEL QTY SEL TEST (`FUEL_QTY_SEL_T_KNB`) is left off: it has no readback and the engine has no command-only control. The cold start (steps 70 ff.) needs it in DCS (owner review).

Question: Add engine support for a command-only control, so that TEST can be on the knob?

#### SEAT

- **Panels:** Ejection Seat Controls (pp. 81, 82), SEAT ADJ Switch (p. 80).
- **Arrangement:** two plates: the seat arming lever (left side of the seat; the ejection handle is at the front) and the SEAT ADJ switch (top left of the right console). On the page they stand side by side.
- **Controls:** 4 rows (3 + 1), 3 id, 0 read only, 2 left off (Ejection Handle, Emergency Manual Chute Lever). On the page: 2 controls and 1 bar. Plus: `SEAT_HEIGHT` (seat height, read only, shown as a bar).
- **Special:** the arming lever (ARMED, LOCKED; order guessed) lights the SEAT NOT ARMED caution when it is up (the lamp is on CAUTION); the SEAT ADJ switch (UP, OFF, DOWN) is spring-loaded and held while pressed. The ejection handle (`SEAT_EJECT_HANDLE`) is left off: the manual says it is not modelled (Left Ctrl + E starts the sequence), and the emergency manual chute lever is not exported (section 11).
- **Picture:** `p081-002.jpg` (partial), `p080-008.jpg` (partial), arming lever `p081-007.jpg` (legible).
- **Fit:** fits, 464 × 336 du as built (estimate 424 × 316): SEAT ARMING 160 × 240 beside SEAT ADJ 288 × 336.

Decided: the ejection handle is left off because the manual says it is not modelled (owner review).

#### CAUTION

- **Panels:** Caution Light Panel (p. 59).
- **Arrangement:** one plate with the lamps in 8 rows of 4 columns, as in the figure and in the order of PANELS.md (row by row, left to right). Six cells are blank: row 6 column 3, row 7 columns 3 and 4, row 8 columns 2, 3 and 4.
- **Controls:** 26 rows, 26 id, 26 read only, 0 left off. On the page: 26 lamps (all amber, each a wide legend lamp of 136 × 40 du) and 6 blank cells. Lamps only, no touch target.
- **Special:** the longest legend is ATF NOT ENGAGED (15 characters, two lines as printed). Four lamps have no function in the Block 50 or are not implemented (NUCLEAR, ATF NOT ENGAGED, EEC, BUC) and stay on the grid. The six unnamed DCS-BIOS caution lights `LIGHT_CAUTION_1` to `LIGHT_CAUTION_6` have no legend and are not matched to the blank cells (section 11). MASTER CAUTION is on the lamp row of every page.
- **Picture:** `p059-002.jpg` (good).
- **Fit:** fits, 640 × 448 du as built (as estimated): one plate.

Decided: the six blank cells stay inert and `LIGHT_CAUTION_1` to `LIGHT_CAUTION_6` stay unused (their cell order is unknown; owner review).

#### HUD CONTROL

- **Panels:** HUD Control Panel (p. 94).
- **Arrangement:** one plate of toggles in two rows of three, in the order of the figure (right console, left part, above SNSR PWR).
- **Controls:** 8 rows, 8 id, 0 read only, 2 left off (Altitude Switch, Test Switch). On the page: 6 controls.
- **Special:** all six have three positions: SCALES (VV/VAH, VAH, OFF), FLIGHTPATH MARKER (ATT/FPM, FPM, OFF), DED/PFLD (DED, PFL, OFF), DEPRESSIBLE RETICLE (STBY, PRI, OFF), VELOCITY (CAS, TAS, GND SPD) and BRIGHTNESS (DAY, AUTO BRT, NIGHT; AUTO BRT is N/I and greyed out). The ALTITUDE and TEST switches are left off (section 11). The HUD glass is not drawn (section 11).
- **Picture:** `p094-002.jpg` (partial).
- **Fit:** fits, 462 × 312 du as built (estimate 364 × 312): one plate.

#### SNSR PWR / VMS / ZEROIZE

- **Panels:** SNSR PWR Control Panel (p. 75), VOICE MESSAGE Switch (p. 80), ZEROIZE Switch (p. 80).
- **Arrangement:** three plates. In the cockpit SNSR PWR is at the lower left of the right console, the VOICE MESSAGE switch below it and the ZEROIZE switch at the bottom left. On the page: SNSR PWR on top, VOICE MESSAGE beside ZEROIZE below it.
- **Controls:** 6 rows (4 + 1 + 1), 6 id, 0 read only, 0 left off. On the page: 6 controls.
- **Special:** SNSR PWR: LEFT HDPT, RIGHT HDPT and FCR (ON, OFF) and RDR ALT (RDR ALT, STBY, OFF). VOICE MESSAGE: VOICE MESSAGE, INHIBIT. ZEROIZE (OFP, OFF, DATA) erases keys and data and is a guarded control with the real DCS cover `ZEROIZE_SW_COVER`.
- **Picture:** `p075-002.jpg` (partial), `p080-002.png` (good), `p080-005.jpg` (good).
- **Fit:** fits, 544 × 508 du as built (estimate 464 × 420): SNSR PWR 544 × 240 above VOICE MESSAGE 232 × 252 beside ZEROIZE 296 × 252.

#### LIGHTING / AIR COND

- **Panels:** Interior LIGHTING Control Panel (p. 76), AIR COND Control Panel (p. 76).
- **Arrangement:** two plates: the interior LIGHTING panel (upper centre-left of the right console) and the AIR COND panel to its right. On the page they stand side by side.
- **Controls:** 8 rows (6 + 2), 8 id, 0 read only, 1 left off (TEMP Knob). On the page: 7 controls: five brightness knobs, the MAL & IND LTS switch and the AIR SOURCE knob.
- **Special:** PRIMARY CONSOLES, PRIMARY INST PNL, PRIMARY DATA ENTRY DISPLAY, FLOOD CONSOLES and FLOOD INST PNL are continuous knobs; the MAL & IND LTS switch (BRT, DIM) is spring-loaded with a centre rest in DCS-BIOS (the manual lists BRT and DIM only); AIR SOURCE (OFF, NORM, DUMP, RAM). The TEMP knob is left off (section 11). The four DCS-BIOS-only lighting outputs are not used (section 11).
- **Picture:** `p076-002.jpg` (good), `p076-017.jpg` (good).
- **Fit:** fits, 640 × 460 du as built (estimate 608 × 308): INTERIOR LIGHTING 392 × 460 beside AIR COND 232 × 256.

#### OXYGEN / ANTI-ICE

- **Panels:** OXYGEN Regulator Panel (p. 77), ENGINE ANTI-ICE Switch (p. 78), ANT SEL Panel (p. 78).
- **Arrangement:** three plates. In the cockpit the oxygen regulator is at the bottom centre of the right console, the engine anti-ice switch and the ANT SEL panel at its upper right. On the page: the oxygen plate on the left, the anti-ice plate and ANT SEL one above the other on the right.
- **Controls:** 8 rows (5 + 1 + 2), 8 id, 2 read only, 1 left off (EMERGENCY Lever). On the page: 5 controls, 1 lamp and 1 bar (the supply pressure `OXYGEN_PRESSURE`).
- **Special:** the FLOW indicator is a white lamp (`FLOW_INDICATOR_LIGHT`; the gauge `FLOW_INDICATOR` is left off, section 11); the SUPPLY lever (PBG, ON, OFF) and the diluter lever (100%, NORM) are drawn as toggles; ANTI-ICE ENGINE (ON, AUTO, OFF); ANT SEL IFF and UHF (UPPER, NORM, LOWER). The EMERGENCY lever is left off (N/I). The diluter lever is N/I too, but the cold start names it (steps 99 and 108), so it stays.
- **Picture:** `p077-008.jpg` (good), `p078-002.jpg` (partial).
- **Fit:** fits, 640 × 448 du as built (estimate 604 × 520): OXYGEN 372 × 448 beside ANTI-ICE 252 × 216 above ANT SEL 252 × 216.

Decided: the diluter lever is kept although the manual says N/I, because cold start steps 99 and 108 name it (owner review).

#### AVIONICS POWER

- **Panels:** AVIONICS POWER Control Panel (p. 78).
- **Arrangement:** one plate. In the cockpit: a top row of toggles (MMC, ST STA, MFD, UFC, MAP), GPS and DL in the middle, the INS knob and the MIDS LVT knob at the bottom. On the page: MMC, ST STA, MFD, UFC and GPS in the first row (MAP is left off), DL, INS and MIDS LVT in the second.
- **Controls:** 9 rows, 9 id, 0 read only, 1 left off (MAP Switch). On the page: 8 controls.
- **Special:** all toggles are ON / OFF (which direction is ON is not printed; the order is guessed); the INS knob has seven positions (OFF, STOR HDG, ALIGN NORM, NAV, CAL, IN FLT ALIGN, ATT; CAL has no function and is greyed out); MIDS LVT (ZERO, OFF, ON; ZERO wipes the terminal). The DL switch is N/I but the cold start names it (step 49), so it stays. The MAP switch is left off (section 11). The INS knob labels are shortened for the chooser (NORM for ALIGN NORM, IN FLT for IN FLT ALIGN) and its knob angles are a compromise, not the real panel angles.
- **Picture:** `p078-011.jpg` (partial).
- **Fit:** fits, 624 × 412 du as built (estimate 564 × 344): one plate.

Decided: the DL switch is kept although the manual says N/I, because cold start step 49 names it (owner review).

### Link boxes

| Box | Opens | Controls |
| --- | --- | --- |
| MFD L | MFD tab, left side | bezel of the left MFD (p. 122), section 5 |
| MFD R | MFD tab, right side | bezel of the right MFD (the same bezel), section 5 |
| DED / ICP | DED tab | Data Entry Display (DED) (p. 101) and Integrated Control Panel (ICP) (p. 99), section 6 |

### Panels that are not on a COCKPIT page

Every section of [PANELS.md](PANELS.md) is on a page above or is one of these. The DCS-BIOS columns of BIOS.md say how each is built.

| Section of PANELS.md | Where it is |
| --- | --- |
| Side Stick Controller (SSC) (p. 83) | FLIGHT and FIGHT (key hats TMS, DMS, CMS, TRIM and the NWS key, sections 3, 4 and 8); the rest in section 11 |
| Throttle (p. 86) | FUEL / EPU / START (THROTTLE CUTOFF) and FLIGHT (the speed brake keys, sections 3 and 8); the rest in section 11 |
| Fuel Flow Indicator (p. 50) | instrument, not drawn (section 11) |
| Engine Instruments (p. 50) | instrument, not drawn; FLIGHT shows RPM, FTIT, NOZ and OIL as bars (section 3); section 11 |
| Angle-of-Attack (AoA) Indicator (p. 52) | instrument, not drawn (section 11) |
| Vertical Velocity Indicator (VVI) (p. 52) | instrument, not drawn (section 11) |
| Magnetic Compass (p. 58) | instrument, not drawn (section 11) |
| Fuel Quantity Indicator (p. 58) | instrument, not drawn; FLIGHT shows FUEL AL and FUEL FR as bars (section 3); section 11 |
| Pilot Fault List Display (PFLD) (p. 59) | section 11 |
| Hydraulic Pressure Indicators (p. 61) | instrument, not drawn; FLIGHT shows HYD A and HYD B as bars (section 3); section 11 |
| EPU Fuel Quantity Indicator (p. 61) | instrument, not drawn (section 11) |
| Cabin Pressure Gauge (p. 61) | instrument, not drawn (section 11) |
| AVTR Control Panel (p. 66) | section 11 |
| Manual Canopy Control Handcrank (p. 62) | section 11 |
| ANTI-G TEST Button (p. 62) | section 11 |
| KY-58 Secure Voice Panel (p. 77) | section 11 |
| PLAIN/CIPHER Switch (p. 77) | section 11 |
| NUCLEAR CONSENT Switch (p. 80) | section 11 |
| Other right console fittings (pp. 75, 127) | section 11 |
| Head-Up Display (HUD) (p. 90) | section 11 (no DCS-BIOS output); its control panel is HUD CONTROL |
| Integrated Control Panel (ICP) (p. 99) | DED tab, section 6 |
| Data Entry Display (DED) (p. 101) | DED tab, section 6 |
| Multi-Function Display (MFD) bezel (p. 122) | MFD tab, section 5 |
| MFD Format Selection Master Menu (p. 124) | MFD tab, section 5 (the same 20 OSBs) |

### Scroll pages

As built, 8 of the 21 pages are taller than the 540 du of the decision rule and are scroll pages (rule "Fit" above). The other 13 fit in 640 × 600 du. The DED tab is a scroll page too (section 6).

| Page | Size (du) | Why |
| --- | --- | --- |
| CANOPY / DEFOG | 580 × 612 | three plates, the tall DEFOG plate |
| FUEL / EPU / START | 640 × 708 | three plates, with the throttle cutoff button on ENG & JET START |
| FLT CONTROL / TRIM | 626 × 664 | three plates in two columns |
| ELEC / TEST | 592 × 816 | two plates and 12 lamps |
| LANDING GEAR / HMCS | 640 × 898 | one plate of 10 controls, 4 lamps and a bar, and two more plates |
| CMDS | 600 × 668 | two plates, a guarded switch and two rotary knobs |
| UHF / IFF BACKUP | 600 × 840 | 11 UHF controls with two windows, and the IFF plate |
| INSTRUMENTS | 640 × 952 | four plates of knobs, rockers and displays in a 2 × 2 grid |

Decided: a page counts as fitting only up to 540 du (600 du less the 10 % margin of the decision rule). As built every scroll page is taller than 600 du (612 to 952), so the margin decides nothing; AUDIO (546 du) is the only page between 540 and 600 du and stays a fixed page (owner review).

Decided: a page groups neighbouring panels (the CHAFF/FLARE button with CMDS, HMCS and ALT GEAR with LANDING GEAR, SEAT ADJ with the seat controls, FCR power with the other sensor power switches); the 24 map boxes are not split further (owner review).

## 3. FLIGHT

The quick page for start, take-off, landing and flying, on the fixed 7 × 3 grid (`grid: [row, col, rows, cols]`: 3 rows and 7 columns, as on the A-10C and the AH-64D). Flight instruments are not drawn (cockpit-replica graphics are out of scope, [../SPEC.md](../SPEC.md) section 11); FLIGHT shows the values a pilot checks from the tablet as read-only bars: engine, fuel and hydraulics for the cold start and the speed brake position. The throttle is the real one: the tablet only has the move between OFF and IDLE, as a guarded button on FUEL / EPU / START. Sources in [PANELS.md](PANELS.md): Side Stick Controller (SSC) (p. 83), Throttle (p. 86).

**Built**

| Control | Type | Source | Grid |
| --- | --- | --- | --- |
| SPD BRK | read-only bar: speed brake position | `SPEEDBRAKE_INDICATOR` | [1,4,1,1] |
| GEAR | selector UP / DOWN | `GEAR_HANDLE` | [1,5,1,1] |
| ALT FLAPS | selector NORM / EXTEND | `ALT_FLAPS_SW` | [1,6,1,1] |
| LAND / TAXI | selector LANDING / OFF / TAXI | `LAND_TAXI_LIGHT_SW` | [1,7,1,1] |
| BRAKE / SKID | selector PARKING / ANTI-SKID / OFF (the texts are shortened: the longer ones wrapped and overlapped at 1024 × 768) | `ANTI_SKID_SW` | [2,5,1,1] |
| RPM | read-only bar: engine RPM | `ENGINE_TACHOMETER` | [2,6,1,1] |
| FTIT | read-only bar: fan turbine inlet temperature | `ENGINE_FTIT` | [2,7,1,1] |
| FUEL AL | read-only bar: aft and left fuel needle | `FUEL_AL` | [3,1,1,1] |
| FUEL FR | read-only bar: forward and right fuel needle | `FUEL_FR` | [3,2,1,1] |
| NOZ | read-only bar: nozzle position | `ENGINE_NOZZLE_POSITION` | [3,4,1,1] |
| OIL | read-only bar: oil pressure | `ENGINE_OIL_PRESSURE` | [3,5,1,1] |
| HYD A | read-only bar: hydraulic system A pressure | `SYSA_PRESSURE` | [3,6,1,1] |
| HYD B | read-only bar: hydraulic system B pressure | `SYSB_PRESSURE` | [3,7,1,1] |

The gear lamps, the gear handle warning and the other warning lamps are not on the grid but in the lamp row (section 7). The gear handle is a plain selector; the downlock release is `DN_LOCK_BTN` on LANDING GEAR / HMCS. The grid cell [2,4] is empty. THROTTLE OFF / IDLE (`THROTTLE_OFF_IDLE`, the move between OFF and IDLE only, `likely`, BIOS.md) is not on FLIGHT: a tap in flight would stop the engine, so it must be guarded, and the engine has guarded controls on panel pages only, not in the grid. It is the guarded button THROTTLE CUTOFF on the ENG & JET START plate of FUEL / EPU / START (section 2).

**Not built yet (keypress controls).** They wait for the F-16C keybinds (section 8); each is a `key` control or a key hat, with no confirmation (`confirmed: null`), as the AH-64D key buttons. Their cells are reserved now.

| Control | Type | Keybinds | Grid |
| --- | --- | --- | --- |
| TRIM | key hat: up, down, left, right (a tap trims one step, a hold keeps trimming) | `trim_up`, `trim_down`, `trim_left`, `trim_right` | [1,1,2,2] |
| SPD BRK EXTEND | key button (hold = keep moving, as the real switch) | `speed_brake_extend` | [1,3,1,1] |
| SPD BRK RETRACT | key button (hold = keep moving) | `speed_brake_retract` | [2,3,1,1] |
| NWS | key button (nosewheel steering on and off on the ground) | `nws` | [3,3,1,1] |

The key hat TRIM takes 2 × 2 cells so that every direction is at least 56 px (section 4, "Cell size"). A tap trims one step and a hold keeps trimming. The stick direction is named as on the hat: up is forward (nose down), down is aft (nose up).

**Grid** (3 rows × 7 columns; `*` = reserved, not built; `..` = the cell continues the control on its left or above):

```
       c1        c2        c3        c4        c5        c6        c7
row 1  *TRIM     ..        *SB EXT   SPD BRK   GEAR      ALT FLAP  LAND/TAX
row 2  ..        ..        *SB RET             BRK/SKID  RPM       FTIT
row 3  FUEL AL   FUEL FR   *NWS      NOZ       OIL       HYD A     HYD B
```

Question: The HOTAS core set is the key hats TMS, DMS, CMS and TRIM, the two speed brake keys and the NWS key. RDR CURSOR / ENABLE, MAN RNG / UNCAGE, DOG FIGHT, EXPAND / FOV, the paddle switch, the UHF / VHF transmit switch and ANT ELEV are not in it (section 11), because a 3 × 7 page holds three 2 × 2 hats at most and both grids are full. Which of them should replace something? Open until the keys are built; the build kept the core set.

Decided: FLIGHT shows the gauges the cold start checks (RPM, FTIT, NOZ, OIL, HYD A, HYD B, fuel; steps 32 to 37, 61, 70 to 75); HORN SILENCER and F-ACK have no cell (they are on LANDING GEAR / HMCS and EYEBROWS / INDEXERS) (owner review).

Decided: TMS, DMS and CMS are on FIGHT and TRIM on FLIGHT, with the speed brake keys and the SPD BRK bar next to it (owner review).

## 4. FIGHT

The quick page for weapons, sensors and countermeasures, on the fixed 7 × 3 grid.

**Built**

| Control | Type | Source | Grid |
| --- | --- | --- | --- |
| MASTER ARM | selector MASTER ARM / OFF / SIMULATE | `MASTER_ARM_SW` | [1,7,1,1] |
| LASER ARM | selector LASER ARM / OFF | `LASER_ARM_SW` | [2,7,1,1] |
| CH | display of the CMDS chaff count | `CMDS_CH_AMOUNT` | [3,1,1,1] |
| FL | display of the CMDS flare count | `CMDS_FL_AMOUNT` | [3,2,1,1] |
| CMDS MODE | selector OFF / STBY / MAN / SEMI / AUTO / BYP, in two columns | `CMDS_MODE_KNB` | [3,3,1,1] |
| CMDS PRGM | selector BIT / 1 / 2 / 3 / 4 (BIT greyed out), in two columns | `CMDS_PROG_KNB` | [3,4,1,1] |
| ECM | selector OPR / STBY / OFF | `ECM_PW_SW` | [3,5,1,1] |
| XMIT | selector 1 / 2 / 3 | `ECM_XMIT_SW` | [3,6,1,1] |
| RF | selector NORM / QUIET / SILENT | `RF_SW` | [3,7,1,1] |

A selector with more than four positions draws its buttons in two columns (ENGINE.md F7); CMDS MODE (6 positions) and CMDS PRGM (5) did not fit a 1 × 1 cell in one column. MASTER ARM SIMULATE blocks the weapon release. The FCR power switch is on SNSR PWR / VMS / ZEROIZE, the RWR power button on THREAT WARNING and the master mode buttons A-A and A-G on the DED tab (ICP); the LAUNCH lamp is in the lamp row (section 7). The weapon release, the trigger and the ALT REL button are not on the dashboard (section 11).

**Not built yet: the HOTAS key hats.** The HOTAS controls are **key hats**: one 2 × 2 block of grid cells per hat with its four directions. A tap sends a short press (0.15 s), a hold of 0.6 s on the tablet sends a long press (the key held 1.0 s), as the manual separates short (under 0.5 s) and long (over 0.5 s); the long functions that need a full second (the FCR TWS toggle) are covered by the 1.0 s hold. Labels show the function that is the same for every sensor of interest (SOI), and a short generic word where the function depends on the SOI (the dashboard cannot read the SOI: it has no DCS-BIOS output). The key hat is part of the engine (a `hat` with `keys`, [../SPEC.md](../SPEC.md) section 8); the F-16C file has none yet, because the key names need the F-16C keybinds.

| Control | Directions (short / long) | Planned |
| --- | --- | --- |
| TMS (Target Management Switch) | up (forward): designate / SOI to HMCS, FCR spotlight, TGP area track; down (aft): reject / end TDOA, TGP declutter; left: scan interrogate, TGP cycle TV and FLIR / FCR NCTR, start TDOA; right: step target, sighting point / FCR TWS toggle, TGP inertial track. Labels: "DSGNT", "REJECT", "SCAN", "STEP" | FIGHT, [1,1,2,2] |
| DMS (Display Management Switch) | up: SOI to HUD; left: cycle the left MFD format; right: cycle the right MFD format; down: SOI to MFD (HUD, HMCS) or swap the SOI between the MFDs / helmet display on and off. Labels: "SOI HUD", "L MFD", "R MFD", "SWAP" | FIGHT, [1,3,2,2] |
| CMS (Countermeasures Management Switch) | up: dispense manual program 1 to 4 as set on the CMDS PRGM knob; left: dispense program 6; right: ECM off (MAN, SEMI) or stop dispensing (AUTO); down: ECM on (MAN, XMIT 3), one auto program and ECM (SEMI), continuous auto dispensing (AUTO). No long functions. Labels: "PROG", "PROG 6", "STOP", "ECM ON" | FIGHT, [1,5,2,2] |

The CMS functions are the same in every SOI (PANELS.md, Side Stick Controller (SSC) (p. 83); p. 708 adds that forward does nothing while another program runs). The TMS and DMS functions per SOI are in the same section; the exact mapping is checked in the DCS research (phase 7).

**Grid** (3 rows × 7 columns; `*` = reserved, not built; `..` = the cell continues the control on its left or above):

```
       c1        c2        c3        c4        c5        c6        c7
row 1  *TMS      ..        *DMS      ..        *CMS      ..        MSTR ARM
row 2  ..        ..        ..        ..        ..        ..        LASER
row 3  CH        FL        CMDS MOD  CMDS PRG  ECM       XMIT      RF
```

**Cell size.** A key hat in a 1 × 1 grid cell has touch areas of about 44 px, below the 56 px minimum, so every HOTAS key hat takes 2 × 2 cells, as on the AH-64D pilot FIGHT page. A 3 × 7 grid holds three such hats at most; FIGHT uses all three. The grids are planned for this from the start (the A-10C had to rearrange its grids when its key hats were added).

Decided: A-A, A-G, FCR power and RWR power have no cell on FIGHT (they are on the DED tab, SNSR PWR / VMS / ZEROIZE and THREAT WARNING); the nine built cells hold the arm switches, the CMDS counts and controls, ECM and RF (owner review).

## 5. MFD

Both MFDs, drawn by the `mfcd` layout of the A-10C (ENGINE.md F4), one bezel at a time (`"layout": "mfcd"`, `"titles"` LEFT MFD and RIGHT MFD, `"inert"` empty). A switch LEFT MFD / RIGHT MFD stands beside the bezel. The side is preselected by the map boxes MFD L and MFD R and remembered per aircraft (E9). Sources in [PANELS.md](PANELS.md): Multi-Function Display (MFD) bezel (p. 122), MFD Format Selection Master Menu (p. 124).

- **Bezel:** 20 option select buttons (OSB): OSB 1 to 5 along the top (left to right), 6 to 10 down the right side (top to bottom), 11 to 15 along the bottom (11 at the far right, 15 at the far left) and 16 to 20 up the left side (16 at the bottom, 20 at the top): `MFD_L_1` … `MFD_L_20` and `MFD_R_1` … `MFD_R_20`. The four corner rockers GAIN (top left, slot `TL`, `MFD_L_GAIN_SW`, `MFD_R_GAIN_SW`), SYM (top right, `TR`, `MFD_L_SYM_SW`, `MFD_R_SYM_SW`), BRT (bottom left, `BL`, `MFD_L_BRT_SW`, `MFD_R_BRT_SW`) and CON (bottom right, `BR`, `MFD_L_CON_SW`, `MFD_R_CON_SW`). All four work, so none is drawn inert. There is no power knob on the bezel: both MFDs are switched by the MFD toggle of AVIONICS POWER (`MFD_SW`). Drawing reference: PICTURES.md, MFD bezel `p122-002.jpg` (good).
- **Screen:** empty in version 1: DCS-BIOS has no MFD screen output, and the export script table of the F-16C is empty (ENGINE.md F6). The OSB numbers are printed small beside the buttons, because the manual figure prints none. Live OSB labels can follow later through `list_indication`, as for the AH-64D MPD, once phase 7 has found the MFD indication numbers.
- **Master menu:** the format select page of the manual (a second press of a highlighted format select button opens it) uses the same 20 OSBs: format select buttons OSB 12 to 14 (the manual says 13 to 15 on p. 124 and 12 to 14 on p. 126; the figure puts SWAP at OSB 15 and DCLT at OSB 11), formats BLANK (OSB 1), HAD (2), RCCE (4), RESET MENU (5), SMS (6), HSD (7), DTE (8), TEST (9), FLCS (10), FLIR (16), TFR (17), WPN (18), TGP (19), FCR (20). Nothing extra is drawn for it; the cold start uses the DTE format on OSB 8 (step 79).
- OSB presses are DCS-BIOS buttons with readback (held 0.3 s); the rockers are 3-position spring switches (down, centre, up; order guessed), each a `hat` with up and down that sends a 0.3 s press per tap. The manual says a held rocker runs to the limit; the page does not repeat.

Decided: the OSB numbers are those of the shared `mfcd` layout: along the bottom 11 is at the far right and 15 at the far left, as the manual figure shows. No numbering per aircraft was needed (owner review).

Decided: a tap on an MFD rocker sends one 0.3 s press; the page does not repeat presses (owner review).

## 6. DED

The DED and the ICP share the DED tab: one panel kit page used as a tab (`"layout": "panel"` without `"panel": true`, ENGINE.md F5), not a hand-drawn layout. The DED is a kit display of the five live lines, the ICP is drawn below it. Sources in [PANELS.md](PANELS.md): Data Entry Display (DED) (p. 101), Integrated Control Panel (ICP) (p. 99). The map box DED / ICP opens this tab.

- **Panels:** Data Entry Display (DED) (p. 101), Integrated Control Panel (ICP) (p. 99).
- **DED screen:** live, 5 lines of 24 characters from `DED_L1` … `DED_L5` (the older `DED_LINE_1` … `DED_LINE_5` are deprecated, section 11); the format strings `DED_L1_FORMAT` … `DED_L5_FORMAT` mark inverse (`i`) and big (`b`) characters; they are not used and the page draws plain lines (section 11). Monospace, green on black, as the real window. The display is 568 × 200 du (24 characters at about 23 du, 5 lines).
- **ICP arrangement:** as the picture `p099-002.jpg` (good). Top row, in the figure's order without IFF: the override buttons COM 1 (`ICP_COM1_BTN`), COM 2 (`ICP_COM2_BTN`) and LIST (`ICP_LIST_BTN`), then the master mode buttons A-A (`ICP_AA_MODE_BTN`) and A-G (`ICP_AG_MODE_BTN`). Keypad of 4 columns × 3 rows with the second legends printed above the keys: 1 T-ILS, 2 ALOW (N), 3, RCL / 4 STPT (W), 5 CRUS, 6 TIME (E), ENTR / 7 MARK, 8 FIX (S), 9 A-CAL, 0 M-SEL (`ICP_BTN_1` … `ICP_BTN_9`, `ICP_BTN_0`, `ICP_RCL_BTN`, `ICP_ENTR_BTN`); the RCL and ENTR key faces are blank, because their legends are too wide for a key, and the legends stand above the keys. The two wheels SYM (`ICP_HUD_BRT_KNB`, HUD symbology) and RET DEPR (`ICP_RETICLE_DEPRESS_KNB`) are drawn as knobs at the left and right of the top keypad row. Below them the DED INCR / DECR rocker (`ICP_DED_SW`) at the left and the data control switch DCS (RTN and SEQ left and right: `ICP_DATA_RTN_SEQ_SW`; up and down: `ICP_DATA_UP_DN_SW`) at the right, drawn as four buttons in a cross, and under the keypad the DRIFT C/O - NORM - WARN RESET toggle (`ICP_DRIFT_SW`, spring from WARN RESET).
- **Controls:** 29 rows (1 + 28), 29 id, 1 read only (the DED window), 6 left off (IFF override button, BRT knob, CONT knob, TFR WX button, FLIR rocker, FLIR GAIN/LVL/AUTO switch). On the page: 25 controls (5 override and master mode buttons, 12 keypad keys, the 4 buttons of the DCS cross, the DED rocker, the DRIFT toggle, 2 wheels) and the DED display.
- **Picture:** `p099-002.jpg` (good), `p101-000.jpg` (partial: a diagram of DED pages, not the frame).
- **Fit:** scroll page, 640 × 844 du as built (estimate 640 × 820): the DED plate 640 × 272 above the ICP plate 640 × 556 (5 round override buttons; the 4 × 3 keypad of 12 PUSH_SMALL with the two wheels; the rocker, the DCS cross and the DRIFT toggle). The DED, the override buttons and most of the keypad are in the first 600 du; the DRIFT toggle is below the fold. The lamp row has MASTER CAUTION. The labels between the override row and the keypad are tight (FIXES.md).

Decided: the ICP IFF override button (IFF page not implemented) and the BRT and CONT wheels, TFR WX and the FLIR controls (no function in the Block 50) are left off, so the top row has five buttons (owner review).

Decided: the DED draws plain lines in version 1; inverse and big characters (`DED_Ln_FORMAT`) are not drawn, because the kit display has no per-character marks (owner review).

Question: Is an engine change worth it, so that the DED draws inverse and big characters?

Decided: the DCS switch is a cross of four push buttons (four `button` controls on the two DCS-BIOS ids, rest 1, up/right 2, down/left 0), not a drawn rocker and not a hat, because the panel kit has no 4-way hat (owner review).

## 7. Lamp row

The row of lamps at the top of every page (as on the AH-64D and the A-10C).

| View | Lamps |
| --- | --- |
| COCKPIT map | MASTER CAUTION (amber, a lighted push button: lamp `LIGHT_MASTER_CAUTION`, press = `MASTER_CAUTION`, which resets it), AR / NWS (green, `LIGHT_AR_NWS`), MARKER (green, `LIGHT_MARKER_BEACON`), CANOPY (red, `LIGHT_CANOPY`), ENG FIRE (red, `LIGHT_ENG_FIRE`) |
| Every panel page | MASTER CAUTION |
| FLIGHT | MASTER CAUTION, N, L and R (green, `LIGHT_GEAR_N`, `LIGHT_GEAR_L`, `LIGHT_GEAR_R`), GEAR (red, the gear handle warning `LIGHT_GEAR_WARN`), TO / LDG CONFIG (red, `LIGHT_TO_LDG_CONFIG`), ENG FIRE (red), ENGINE (red, `LIGHT_ENGINE`), CANOPY (red) |
| FIGHT | MASTER CAUTION, LAUNCH (red, missile launch: `LIGHT_RWR_MSL_LAUNCH`), ECM (green, `LIGHT_ECM`), NO GO and GO (green, `LIGHT_CMDS_NO_GO`, `LIGHT_CMDS_GO`) |
| MFD | none |
| DED | MASTER CAUTION |

The F-16C has no MASTER WARNING lamp of the AH-64D kind. MASTER CAUTION is the lamp in the button on the left eyebrow (lit by any caution light); pressing it resets it. The ELEC CAUTION RESET button on the ELEC panel (`ELEC_CAUTION`) clears MASTER CAUTION and ELEC SYS and resets the generators (ELEC / TEST). The caution light panel (26 lamps) is a COCKPIT page (CAUTION), the warning lamps are on EYEBROWS / INDEXERS.

Decided: the MFD tab has no lamp row (as the A-10C MFCD tab); the DED tab has MASTER CAUTION because it is a panel kit page (owner review).

## 8. Keybinds

DCS-BIOS has no HOTAS control, so these functions are keypresses ([../SPEC.md](../SPEC.md) section 4). The aircraft file will hold their defaults in `KEYS`; `[keys]` in `config/config.toml` overrides them (E8). The defaults are **open**: they are taken from the F-16C default keybinds once the module is installed and its control list is exported from DCS (Options, Controls, "Make HTML"; phase 7). Keys the key table does not know yet (numpad, Tab, Esc, punctuation) are added to `core/keys.py` then. Until then `KEYS` of the F-16C file is empty and the key controls are not built; the bridge checks every key a control needs at start, so a key control without its key would stop the bridge. The directions are named as on the hat: up is forward, down is aft.

| Key name | DCS command (F-16C) | Used on |
| --- | --- | --- |
| `tms_up`, `tms_down`, `tms_left`, `tms_right` | Target Management Switch directions (forward, aft, left, right) | FIGHT |
| `dms_up`, `dms_down`, `dms_left`, `dms_right` | Display Management Switch directions | FIGHT |
| `cms_up`, `cms_down`, `cms_left`, `cms_right` | Countermeasures Management Switch directions | FIGHT |
| `trim_up`, `trim_down`, `trim_left`, `trim_right` | Trim switch directions (forward = nose down, aft = nose up, left and right = wing down) | FLIGHT |
| `speed_brake_extend`, `speed_brake_retract` | Speed brake extend (aft) and retract (forward) | FLIGHT |
| `nws` | Missile Step button (switches the nosewheel steering on and off on the ground) | FLIGHT |

A long press is the same key held 1.0 s; no extra key names. The AH-64D keys (power levers, trim reset, canopy, monocle, controls overlay, George) are not needed for the F-16C (E3, E4). The F-16C auto-start keys (Left Windows + Home and Left Windows + End, STARTUP.md) are not used.

Question: The key names are placeholders until the keybind export (the NWS key may turn out to be the Missile Step button itself).

## 9. Engine behaviour for the F-16C

The engine changes of [ENGINE.md](ENGINE.md) (F1 to F8) and the A-10C changes (E1 to E10, [../A10C/ENGINE.md](../A10C/ENGINE.md)) as they apply to this aircraft. The F-16C changes F1 to F8 are built; the A-10C changes are built.

- **E1 Aircraft choice.** `aircraft/f16c.py` has `NAME = "F-16C"`, `DCS_NAMES = ["F-16C_50"]` and `DCSBIOS_MODULE = "F-16C_50"` (one module, which also serves the F-16D and F-16I variants). The bridge reads `_ACFT_NAME` from the DCS-BIOS stream and switches to the F-16C file when it reads `F-16C_50`; the page reloads its layout. `[dcs] aircraft = "auto"` stays the default. The settings page lists F-16C as one more button of its AUTO / one button per aircraft switch (the names come from the bridge).
- **E2 Seats.** One seat: `SEATS = [{"prefix": "", "label": "F-16C"}]`, `SEAT_OUTPUT = None`. The badge shows `F-16C`; no seat switch, no debug-seat hold.
- **E3 Trim.** `TRIM_SWITCH = None` and `TRIM_RELEASED = None`: no trim display, no trim tracking; `trim_reset` is not required. The trim wheel positions are on FLT CONTROL / TRIM.
- **E4 Throttle.** No `lever` control and no `power_*` keys. The throttle position has no DCS-BIOS output; THROTTLE OFF / IDLE is the guarded button THROTTLE CUTOFF on FUEL / EPU / START.
- **E5 Displays.** The MFD tab reuses the A-10C `mfcd` layout (F4): the four corner rocker places (`TL`, `TR`, `BL`, `BR`) are drawn where the aircraft has a control with that slot (GAIN, SYM, BRT, CON), and the PWR knob place stays empty; the view carries `titles` and `inert`. The DED tab is a panel kit page used as a tab (F5), so no new hand-drawn layout; the layout checker and the sweep cover it.
- **E6 Look.** A third plate look for F-16C panel pages (section 10), chosen per page by the aircraft file (`look="f16c"`), next to `ah64d` and `a10c` (F3).
- **E7 Export script.** The F-16C table is empty in version 1 (F6); `CONTROL_NAMES`, `MPD_INDICATIONS` and `MPD_SEATS` of the F-16C file are empty and the bridge needs no export data for the F-16C.
- **E8 Keys.** The key hat, the key button and the bar exist. The F-16C `KEYS` (section 8) are empty until the defaults are known; the key table is extended then.
- **E9 Memory and docs.** The remembered tab and MFD side are stored per aircraft in the browser; this spec and the README aircraft section describe the F-16C.
- **E10 Scroll page.** Only the 8 panel pages that do not fit and the DED tab are scroll pages (section 2, "Scroll page"). The page list of the long hold scrolls inside its card (F1); it holds 21 pages and 3 links.
- **F2 Coverage check.** `core/tools/test/coverage.py` takes the aircraft folder (`docs/F16C`); its page-to-panel table comes from the `Panels:` line of every page section of section 2. The DED tab has no such section and is not covered.

## 10. F-16C look

The F-16C panel pages are drawn in a look of their own, different from the AH-64D plates and the A-10C plates (E6, ENGINE.md F3). Reference: the manual renders listed in [PICTURES.md](PICTURES.md) (42 of 74 panels have a good picture); what follows is a description of what they show, nothing is copied.

- **Plates:** near-black, matte, finely grained panels with square corners and a small radius, set into a mid-grey console. The panel name is printed along the left edge, turned 90 degrees (MISC, EXT LIGHTING, ECM, ELEC, FUEL, SNSR PWR, AVIONICS POWER); groups inside a plate are boxed by thin white rules (the ACFT BATT bracket on ELEC, the frame around the ECM lamp on MISC, the lines between the POSITION toggles of EXT LIGHTING). Four black cross-head screws, one in each corner, at the position of the A-10C Dzus fasteners, instead of ears or slotted fasteners. The look is chosen per page (`look="f16c"` on the `Panel` or `PanelGroup`). As built: plate fill `#17191b`, border `#3a3f44`, screws dark grey with a pale ring, labels semi-bold and off-white.
- **Labels:** white sans-serif placard capitals, stencil-like, with the position labels beside or above the lever tips (BRT, OFF, DIM; MASTER ARM, OFF, SIMULATE) and small black-on-white or white-on-black legends on keys.
- **Toggles and levers:** chrome bat-handle levers with a round silver tip on a dark bushing; some with a red flip-up guard over the lever (FUEL MASTER, EPU, ENG CONT, ZEROIZE), and yellow and black hazard stripes around the EMER STORES JETTISON button and DN LOCK REL.
- **Knobs:** black round knobs with a white pointer line (ECM XMIT, EXT LIGHTING, AVIONICS POWER), black or grey knobs with a ribbed edge (FORM, AERIAL REFUELING, the ICP wheels), the scale printed around them.
- **Buttons:** square black keys with a thin lit outline and white numerals (ECM modules); red round buttons (ECM RESET, ALT REL); grey rubber square keys with white legends and a small second legend (ICP); round grey-ringed override buttons; the MASTER CAUTION and eyebrow buttons as dark squares with a dim amber legend.
- **Lamps:** legend lamps in a dark glass square with a bevelled black frame and the legend in amber letters in one or two lines (caution panel, ELEC, EPU lamps), red warning legends in the eyebrow, green and white for the indicator lights; an unlit lamp is black. The kit parts are the LAMP 72 × 40 du and LAMP_WIDE 136 × 40 du.
- **MFD and ICP:** the MFD bezel is black with 20 square grey keys with a white outline and four corner rockers with arrows, the screen black; the DED is a green LED window in a black frame.
- **Same mechanics:** touch areas, chooser, knob bar, guard covers and the panel-kit layout rules stay those of the engine; only the drawing of the plate and the parts changes.

Question: The look follows the manual renders only (no module yet); check colours and the screw drawing against screenshots in phase 7? Blue lamps (ECM T, AR RDY) are drawn white because the kit has no blue lamp, and guarded controls use the engine's guard cover, not the red flip guard.

## 11. Not on the dashboard

Left off on purpose in version 1, one line each.

**Panels and groups**

- **AVTR Control Panel (p. 66)**: the manual describes no control and DCS-BIOS has none; N/I.
- **KY-58 Secure Voice Panel (p. 77)** (4 controls: `KY58_PWR_KNB`, `KY58_MODE_KNB`, `KY58_FILL_KNB`, `KY58_VOL_KNB`): the manual lists none and marks the panel N/I.
- **PLAIN/CIPHER Switch (p. 77)** (`PLAIN_CIPHER_SW`): N/I.
- **NUCLEAR CONSENT Switch (p. 80)**: not implemented; DCS-BIOS has only the NUCLEAR caution lamp (on CAUTION).
- **Other right console fittings (pp. 75, 127)** (utility light, arm rest, DTU receptacle): not exported; a screenshot is needed.
- **Manual Canopy Control Handcrank (p. 62)** and **ANTI-G TEST Button (p. 62)**: named in the figure only and not exported; screenshots needed.
- **Head-Up Display (HUD) (p. 90)**: no DCS-BIOS output; the HUD is not shown (its control panel is HUD CONTROL).
- **Pilot Fault List Display (PFLD) (p. 59)**: no DCS-BIOS output (the HUD repeater switch is `HUD_DED_DATA_SW` on HUD CONTROL).
- **Threat warning scope** (the azimuth scope of Threat Warning Azimuth Indicator (p. 694)): no DCS-BIOS output; the page keeps only its brightness knob.
- **HOTAS controls** (Side Stick Controller (SSC) (p. 83) and Throttle (p. 86)): the weapon release button and the trigger are keybinds only and stay on the real stick, and so is the ALT REL button on MISC (`ALT_REL_BTN`), so a tablet tap never fires a weapon. Not in the core set, keybind only, not planned: the paddle switch, the EXPAND / FOV button, the RDR CURSOR / ENABLE switch, the MAN RNG / UNCAGE knob, the DOG FIGHT switch, the ANT ELEV knob and the UHF / VHF transmit switch. The Throttle Cutoff Release is not exported (`THROTTLE_OFF_IDLE` is the move it allows).

**Instruments (not drawn).** The gauge rows of these sections are not panel pages. The first column says how many rows the section has and how many of them are controls on INSTRUMENTS. Ids marked FLIGHT are bars on FLIGHT. Rows without an identifier are not exported or are fixed scales.

| Instrument | Rows (on INSTRUMENTS) | DCS-BIOS ids not drawn |
| --- | --- | --- |
| Standby Attitude Indicator (SAI) (p. 49) | 7 (1) | `SAI_PITCH`, `SAI_BANK`, `SAI_AIRCRAFTREFERENCESYMBOL`, `SAI_BANK_ARROW`, `SAI_KNB_ARROW`, `SAI_OFF_FLAG` |
| Fuel Flow Indicator (p. 50) | 1 (0) | `FUELFLOWCOUNTER_100`, `FUELFLOWCOUNTER_1K`, `FUELFLOWCOUNTER_10K` |
| Engine Instruments (p. 50) | 4 (0) | `ENGINE_OIL_PRESSURE` (FLIGHT), `ENGINE_NOZZLE_POSITION` (FLIGHT), `ENGINE_TACHOMETER` (FLIGHT), `ENGINE_FTIT` (FLIGHT) |
| Airspeed and Mach Indicator (p. 51) | 6 (1) | `MAX_AIRSPEED`, `MACH_INDICATOR`, `AIRSPEED`, `SET_AIRSPEED` |
| Altimeter (p. 51) | 7 (2) | `ALT_100_FT_PTR`, `ALT_PNEU_FLAG`, `ALT_10000_FT_CNT`, `ALT_1000_FT_CNT`, `ALT_100_FT_CNT`, `ALT_PRESSURE_DRUM_0_CNT`, `ALT_PRESSURE_DRUM_1_CNT`, `ALT_PRESSURE_DRUM_2_CNT`, `ALT_PRESSURE_DRUM_3_CNT` |
| Angle-of-Attack (AoA) Indicator (p. 52) | 5 (0) | `AOA_VALUE` |
| Vertical Velocity Indicator (VVI) (p. 52) | 4 (0) | `VVI` |
| Attitude Director Indicator (ADI) (p. 53) | 13 (1) | `ADI_PITCH`, `ADI_BANK`, `ADI_GS_POINTER`, `ADI_OFF_FLAG`, `ADI_AUX_FLAG`, `ADI_BUBBLE`, `ADI_TURNRATE` |
| Electronic Horizontal Situation Indicator (EHSI) (p. 230) | 19 (6) | `EHSI_RANGE_INVALID` |
| Magnetic Compass (p. 58) | 1 (0) | `STANDBY_COMPASS_HEADING`, `STANDBY_COMPASS_PITCH`, `STANDBY_COMPASS_ROLL` |
| Fuel Quantity Indicator (p. 58) | 3 (0) | `FUEL_AL` (FLIGHT), `FUEL_FR` (FLIGHT), `FUELTOTALIZER_100`, `FUELTOTALIZER_1K`, `FUELTOTALIZER_10K` |
| Hydraulic Pressure Indicators (p. 61) | 2 (0) | `SYSA_PRESSURE` (FLIGHT), `SYSB_PRESSURE` (FLIGHT) |
| EPU Fuel Quantity Indicator (p. 61) | 1 (0) | `HYDRAZIN_VOLUME` |
| Cabin Pressure Gauge (p. 61) | 1 (0) | `COCKPIT_ALITITUDE` |
| Mechanical Clock (p. 61) | 4 (1) | `CLOCK_CURRTIME_H`, `CLOCK_CURRTIME_MS` |

The ids marked FLIGHT are drawn as bars on FLIGHT and are not on a COCKPIT page; `SPEEDBRAKE_INDICATOR` is on LANDING GEAR / HMCS and on FLIGHT.

**Outputs and toggles (DCS-BIOS only, 40 controls, 2 used)**

- **Used:** `CANOPY_POS` (CANOPY / DEFOG) and `LIGHT_MARKER_BEACON` (lamp row).
- **External aircraft model outputs** (10: `EXT_FORMATION_LIGHTS`, `EXT_POSITION_LIGHTS_WING`, `EXT_POSITION_LIGHT_FUSELAGE`, `EXT_SPEED_BRAKE_LEFT`, `EXT_SPEED_BRAKE_RIGHT`, `EXT_STROBE_TAIL`, `EXT_TAIL_LIGHT`, `EXT_WOW_LEFT`, `EXT_WOW_NOSE`, `EXT_WOW_RIGHT`): not cockpit controls.
- **Stick hide** (`HIDE_STICK`): a view toggle, not a cockpit control.
- **Interior lighting outputs** (4: `LIGHT_CONSLES`, `LIGHT_CONSLES_FLOOD`, `LIGHT_INST_PNL`, `LIGHT_INST_PNL_FLOOD`): the knobs of LIGHTING / AIR COND give their own position.
- **Radio frequency strings** (`UHF_RADIO`, `VHF_RADIO`): the UHF backup panel shows its own windows; there is no VHF panel in PANELS.md.
- **ADI extras** (`ADI_GS_BAR`, `ADI_GS_FLAG`, `ADI_LOC_BAR`, `ADI_LOC_FLAG`) and **elapsed time clock** (`CLOCK_ELAPSED`, `CLOCK_ELAPSED_TIME_M`, `CLOCK_ELAPSED_TIME_SEC`): instruments and instrument knobs not drawn.
- **Deprecated** (`DED_LINE_1` … `DED_LINE_5`, replaced by `DED_L1` … `DED_L5`; `AIR_SOURCE_KNB`, replaced by `AIR_SOURCE_KNOB`).
- **Unnamed lights** (`LIGHT_CAUTION_1` … `LIGHT_CAUTION_6`, `LIGHT_EDGE`, `LIGHT_ELEC`): no legend in PANELS.md; the cell of the six caution lights is not known.

**Other outputs not shown (ids on PANELS.md rows)**

- **Trim wheel indicators** (`ROLLTRIMIND`, `PITCHTRIMIND`): the trim wheels on FLT CONTROL / TRIM show their own position.
- **EHSI range flag** (`EHSI_RANGE_INVALID`): the EHSI is not drawn; INSTRUMENTS shows its range text only.
- **Canopy lock position** (`CANOPY_LOCK`): the canopy lever (`CANOPY_HANDLE`) and the CANOPY lamp show the state.
- **EPU switch covers** (`EPU_SW_COVER_OFF`, `EPU_SW_COVER_ON`): the EPU switch has a dashboard cover only (section 2, "Guarded controls").
- **CMDS O1 and O2 counts** (`CMDS_O1_AMOUNT`, `CMDS_O2_AMOUNT`): the O1 and O2 switches are left off, and so are their counts.
- **FUEL QTY SEL TEST** (`FUEL_QTY_SEL_T_KNB`): no readback and no command-only control in the engine; the knob has its five other positions.
- **FLOW indicator gauge** (`FLOW_INDICATOR`): OXYGEN / ANTI-ICE uses the lamp `FLOW_INDICATOR_LIGHT`.
- **DED format strings** (`DED_L1_FORMAT`, `DED_L2_FORMAT`, `DED_L3_FORMAT`, `DED_L4_FORMAT`, `DED_L5_FORMAT`): inverse and big characters are not drawn.

**Controls with no function in DCS, or left off** (the manual says N/I or no function; every one has a DCS-BIOS identifier that does nothing, except where the Why says otherwise). The cold start does not use them. The DED tab stands for the ICP.

| Control | Page it would be on | Identifier | Why |
| --- | --- | --- | --- |
| AB RESET Switch | FUEL / EPU / START | `AB_RESET_SW` | N/I |
| MAX POWER Switch | FUEL / EPU / START | `MAX_PWR_SW` | no function |
| MANUAL TF FLY-UP Switch | FLT CONTROL / TRIM | `MAN_TF_FLYUP_SW` | not used in the Block 50 |
| LE FLAPS Switch | FLT CONTROL / TRIM | `LE_FLAPS_SW` | N/I |
| RESET Button | ECM | `ECM_RESET_BTN` | no function |
| BIT Button | ECM | `ECM_BIT_BTN` | N/I |
| ECM Module Control Button FRM | ECM | `ECM_FRM_BTN`, `LIGHT_ECM_FRM_S`, `LIGHT_ECM_FRM_A`, `LIGHT_ECM_FRM_F`, `LIGHT_ECM_FRM_T` | no function |
| ECM Module Control Button SPL | ECM | `ECM_SPL_BTN`, `LIGHT_ECM_SPL_S`, `LIGHT_ECM_SPL_A`, `LIGHT_ECM_SPL_F`, `LIGHT_ECM_SPL_T` | no function |
| SECURE VOICE Volume Knob | AUDIO | `SEC_VOICE_KNB` | no function |
| TF Volume Knob | AUDIO | `TF_KNB` | no function |
| INTERCOM Volume Knob | AUDIO | `INTERCOM_KNB` | N/I |
| HOT MIC CIPHER Switch (Microphone Switch) | AUDIO | `HOT_MIC_SW` | N/I |
| O1 Switch | CMDS | `CMDS_01_EXP_CAT_SW` | no function |
| O2 Switch | CMDS | `CMDS_02_EXP_CAT_SW` | no function |
| JMR Switch | CMDS | `CMDS_JMR_SOURCHE_SW` | no function |
| MWS Switch | CMDS | `CMDS_MWS_SOURCHE_SW` | no function |
| Azimuth scope | THREAT WARNING | none (not exported) | no output |
| MASTER Knob | UHF / IFF BACKUP | `IFF_MASTER_KNB` | N/I |
| M-4 CODE Switch | UHF / IFF BACKUP | `IFF_M4_CODE_SW` | N/I |
| ENABLE Switch | UHF / IFF BACKUP | `IFF_ENABLE_SW` | N/I |
| MODE 1 & MODE 3 Thumbwheel Selectors | UHF / IFF BACKUP | `IFF_M1_SEL_1`, `IFF_M1_SEL_2`, `IFF_M3_SEL_1`, `IFF_M3_SEL_2`, `IFF_CODE_DRUM_DIGIT_1`, `IFF_CODE_DRUM_DIGIT_2`, `IFF_CODE_DRUM_DIGIT_3`, `IFF_CODE_DRUM_DIGIT_4` | N/I |
| MODE 4 REPLY Switch | UHF / IFF BACKUP | `IFF_M4_REPLY_SW` | N/I |
| MODE 4 MONITOR Switch | UHF / IFF BACKUP | `IFF_M4_MONITOR_SW` | N/I |
| Preset Channel Card & Access Door | UHF / IFF BACKUP | `UHF_DOOR` | N/I |
| TONE Button | UHF / IFF BACKUP | `UHF_TONE_BTN` | N/I |
| VOL Knob | UHF / IFF BACKUP | `UHF_VOL_KNB` | no function |
| ALT REL Button | MISC | `ALT_REL_BTN` | weapon release |
| ADV MODE Button | MISC | `ADV_MODE_SW`, `LIGHT_ACTIVE`, `LIGHT_STBY` | not used in the Block 50 |
| Ejection Handle | SEAT | `SEAT_EJECT_HANDLE` | not modelled |
| Emergency Manual Chute Lever | SEAT | none (not exported) | not exported |
| Altitude Switch | HUD CONTROL | `HUD_ALT_SW` | N/I |
| Test Switch | HUD CONTROL | `HUD_TEST_SW` | N/I |
| TEMP Knob | LIGHTING / AIR COND | `TEMP_KNB` | N/I |
| EMERGENCY Lever | OXYGEN / ANTI-ICE | `OXY_EMERG_LVR` | N/I |
| MAP Switch | AVIONICS POWER | `MAP_SW` | not functional in the Block 50 |
| Override button IFF | DED tab | `ICP_IFF_BTN` | IFF page not implemented |
| BRT Knob | DED tab | `ICP_RASTER_BRT_KNB` | no function in the Block 50 |
| CONT Knob | DED tab | `ICP_RASTER_CONTR_KNB` | no function in the Block 50 |
| TFR WX Button | DED tab | `ICP_WX_BTN` | no function in the Block 50 |
| FLIR Increment/Decrement Rocker | DED tab | `ICP_FLIR_SW` | no function in the Block 50 |
| FLIR GAIN/LVL/AUTO Switch | DED tab | `ICP_FLIR_GAIN_SW` | no function in the Block 50 |

The caution lamps NUCLEAR, ATF NOT ENGAGED, EEC and BUC and the TF-FAIL lamp have no function either but stay on their pages (lamps, section 2). ALT REL (`ALT_REL_BTN`) and the ejection handle (`SEAT_EJECT_HANDLE`) are left off for safety and because DCS does not model them. The manual canopy handcrank, the ANTI-G TEST button, the Throttle Cutoff Release and the emergency manual chute lever have no identifier.

## 12. Manual test run (F-16C)

Preparation: the F-16C module, DCS-BIOS, the export script (copied again after an update). The F-16C keybinds (section 8) are needed once the key controls are built. A throwaway single-player mission, cold and dark on the ground.

1. **Aircraft choice.** Start the bridge, then an AH-64D mission: the AH-64D dashboard appears. Switch to an A-10C mission, then to an F-16C mission: the page reloads with the F-16C tabs and the badge `F-16C`, without a restart. In the settings page, switch to another aircraft and back to AUTO.
2. **Cold start from the tablet.** Follow [STARTUP.md](STARTUP.md) on the COCKPIT pages as far as the tablet allows (battery, FLCS power test, JFS, THROTTLE CUTOFF on FUEL / EPU / START and then the real throttle, avionics power, INS alignment, FLCS BIT, EPU test, canopy). Check every gauge step against the FLIGHT bars. Note every step that fails or shows "not confirmed".
3. **COCKPIT.** Every page opens from the map and from the page list (the list scrolls); the eight scroll pages scroll; switches, knobs and lamps follow the cockpit when you move them with the mouse; every guarded control needs its cover first (the FUEL MASTER, ENG CONT and ZEROIZE covers follow the DCS covers; the EPU cover is the dashboard's only).
4. **DED.** The five lines match the cockpit DED; type a steerpoint with the keypad; COM 1, LIST and M-SEL change pages; RTN and SEQ, the DED rocker and DRIFT C/O act (the DED draws no inverse fields).
5. **MFD.** OSB 1 to 20 of both MFDs change pages (check the numbering of the bottom row); the GAIN, SYM, BRT and CON rockers act on a tap.
6. **FLIGHT.** Gear handle (only with the downlock release, as in the cockpit), ALT FLAPS, landing and taxi lights, the brake switch; the bars follow RPM, FTIT, nozzle, oil, hydraulics, fuel and the speed brake; the lamp row follows the gear. Once the keys are built: speed brake extend and retract (the position bar moves), trim in four directions, NWS.
7. **FIGHT.** MASTER ARM, LASER ARM, RF, CMDS mode and program, ECM power and XMIT; the counts text. Once the keys are built: each key hat direction short and long with the FCR, TGP and HSD as SOI; CMS dispenses (the counts change); DMS cycles the MFD formats.
8. **Open points.** Check the F-16C section of [../FIXES.md](../FIXES.md#f-16c-viper-under-development) and the questions of this spec that need DCS: the guessed position orders (99 identifiers, BIOS.md), the spring-back of FLCS BIT, MANUAL PITCH, OBOGS BIT and EPU/GEN, the autopilot PITCH selector, the latching of the ECM module buttons and RWR POWER, the SAI cage, the EPU and other cover ids, the MFD OSB numbering and rockers, the CMS and TMS mapping, and the first screenshots of the look.

Done when a cold start to taxi works from the tablet plus the real throttle, and every page acts in DCS. The F-16C is built (without the keypress controls) and tested only against a simulated DCS-BIOS; this run is the first test in DCS.
