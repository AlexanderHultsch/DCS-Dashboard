# A-10C II Tank Killer – research notes

Working notes for adding the A-10C II to the dashboard. Our own notes only: the flight manual, its text and its pictures are copyrighted and are never committed. They are downloaded from the link below when needed and kept outside the repo.

## Decisions

- Aircraft: A-10C II Tank Killer only.
- Layout: every aircraft gets the same tabs (COCKPIT with panel pages, FLIGHT, FIGHT, displays, keyboard). Aircraft-specific sub-pages where needed, for example MFCD instead of MPD, CDU and UFC instead of KU. GEORGE is AH-64D only.
- Reference material (manual pages, screenshots) is used to draw the panels, as for the AH-64D; it stays out of the repo.

## Sources

| Source | Where | Notes |
| --- | --- | --- |
| Flight manual (EN, 814 pages, 34 MB) | https://www.digitalcombatsimulator.com/upload/iblock/715/t05fb1h8itdhcvcf6fyi3h5944fvv4fx/DCS_A-10C_II_Flight_Manual_EN.pdf | Needs `www.digitalcombatsimulator.com` in the cloud environment's allowed domains. Printed page numbers equal PDF page numbers |
| DCS-BIOS module | `Scripts/DCS-BIOS/lib/modules/aircraft_modules/A-10C.lua` (DCS-Skunkworks), control list `doc/json/A-10C.json` | One module `A-10C` for both `A-10C` and `A-10C_2`; 749 controls |
| Default keybinds | DCS controls settings, exported as HTML | Needs the module installed |
| Cockpit screenshots | One per panel, straight on | Needs the module installed; only for panels the manual shows poorly |

DCS-BIOS panel groups with the most controls: CDU 63, Caution Lights Panel 48, Circuit Breaker Panel 38, UFC 31, Left and Right MFCD 26 each, IFF 22, Intercom Panel 20, Engine Instruments 20, HSI 19, ARC-210 18, NMSP 17, Light System Control Panel 17, Fuel System Control Panel 15, CMSP 15, UHF Radio 14, Environment Control Panel 13, CMSC 13.

## Open points

From the manual and the DCS-BIOS mapping, to settle in DCS (phase 7):

- CMS switch on the stick: p. 106 (single flare / chaff, programs on long press) and pp. 493, 496 (left / right program, forward / aft start / stop) disagree.
- Radio 1 (settled): the A-10C II has the ARC-210. DCS-BIOS detects the fitted radio at runtime (cockpit argument 998) and exports either the ARC-210 or the old ARC-186 VHF AM head. The left-to-right order of the five ARC-210 frequency knobs is assumed.
- MFCD: swap of the left and right content (p. 124 says coolie hat down short; the HOTAS table gives that to the HMCS); OSB numbering per side; which bottom OSB links which page.
- Not stated in the manual: trim hat directions, anti-skid second position, boost pump and several environment switch "on" labels, ejection seat arm lever, TISL panel labels (low-resolution figure), CDU blank rocker directions, UFC INTEN directions.
- Circuit breaker panel (38 controls), antenna panel, DVADR, external model and a few Misc controls exist only in DCS-BIOS; listed in BIOS.md.
- No DCS-BIOS control for any stick or throttle grip button (TMS, DMS, coolie, China hat, CMS, trim, speed brake, trigger …): keybinds. The throttle levers are read only in DCS-BIOS: moving them needs keybinds too.
- No DCS-BIOS output for the MFCD screens, the HUD and the RWR scope: MFCD labels need the export script (`list_indication`), as for the AH-64D MPD.
- UFC: six buttons of the manual figure (FWD, MID, AFT, three unlabelled) against six A-10C II buttons in DCS-BIOS (COM1, COM SEC, IFF, COM2, ECCM, IDM); assignment unknown.
- 13 cold-start steps name an MFCD OSB or CDU line select key without its number (BIOS.md, Cold start coverage).
- 3 DCS-BIOS controls are defined although the manual says no function (MFCD DSP, CON, SYM rockers; TEMS DATA): check in DCS.
- Item numbers in text and figures differ on several panels (NMSP, fuel, KY-58, TACAN / ILS order); PANELS.md notes which one it follows.
- TISL: the Pave Penny pod is removed in the A-10C II and TISL navigation is not available (p. 546); the TISL panel is a candidate to leave off the dashboard (its only manual picture is low-resolution anyway).
- Many controls have no function in DCS (whole KY-58 panel, IFF EMER, intercom call, several fuel and SAS test items): inert or left off the dashboard.
- The CDU keys work only with the AAP PAGE dial at OTHER; several UFC keys act on the HUD only.

## Plan

| Phase | What | Who | Output | Status |
| --- | --- | --- | --- | --- |
| 0 | Scope and layout | user, Claude | Decisions above | done |
| 1 | Collect sources | user, Claude | Table above | manual and DCS-BIOS done; keybinds and screenshots need the module |
| 2 | Read the manual: pp. 105–209 (cockpit panels, HOTAS, CDU), 303–311 (UFC, MFCD overview), 482 and 491–503 (HMCS HOTAS, defensive systems), 504–544 (start-up) | Claude | [PANELS.md](PANELS.md): 66 panel sections; [STARTUP.md](STARTUP.md): cold start in 164 steps | done |
| 3 | Match with DCS-BIOS | Claude | [BIOS.md](BIOS.md): every PANELS.md control with its identifier and access, the 72 DCS-BIOS-only controls, gaps, cold start coverage | done |
| 4 | Reference pictures per planned panel page | Claude, then user (screenshots) | Pictures outside the repo; list of panels that need screenshots | open |
| 5 | Compare with the engine | Claude | List of engine changes, each with a user decision: single seat (no CP/G), MFCD / CDU / UFC drawings, export script arguments, trim display | open |
| 6 | A-10C spec | Claude writes, user reviews | Spec of views, panel pages, controls, keybinds | open |
| 7 | Research in DCS (needs the module) | user flies, Claude analyses | Read test and control sweep adapted from the `research-v1` tag; export arguments and MFCD indication numbers | open |
| 8 | Build plan and build | Claude delegates | Verified steps | open |
