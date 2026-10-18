# A-10C II Tank Killer – research notes

Working notes for adding the A-10C II to the dashboard. Our own notes only: the flight manual, its text and its pictures are copyrighted and are never committed. They are downloaded from the link below when needed and kept outside the repo.

## Decisions

- Aircraft: A-10C II Tank Killer only.
- Layout: every aircraft gets the same tabs (COCKPIT with panel pages, FLIGHT, FIGHT, displays, keyboard). Aircraft-specific sub-pages where needed, for example MFCD instead of MPD, CDU and UFC instead of KU. GEORGE is AH-64D only.
- Reference material (manual pages, screenshots) is used to draw the panels, as for the AH-64D; it stays out of the repo.

## Sources

| Source | Where | Notes |
| --- | --- | --- |
| Flight manual (EN, about 40 MB) | https://www.digitalcombatsimulator.com/upload/iblock/715/t05fb1h8itdhcvcf6fyi3h5944fvv4fx/DCS_A-10C_II_Flight_Manual_EN.pdf | Not yet read: the cloud environment needs `www.digitalcombatsimulator.com` in its allowed domains |
| DCS-BIOS module | `Scripts/DCS-BIOS/lib/modules/aircraft_modules/A-10C.lua` (DCS-Skunkworks), control list `doc/json/A-10C.json` | One module `A-10C` for both `A-10C` and `A-10C_2`; 749 controls |
| Default keybinds | DCS controls settings, exported as HTML | Needs the module installed |
| Cockpit screenshots | One per panel, straight on | Needs the module installed; only for panels the manual shows poorly |

DCS-BIOS panel groups with the most controls: CDU 63, Caution Lights Panel 48, Circuit Breaker Panel 38, UFC 31, Left and Right MFCD 26 each, IFF 22, Intercom Panel 20, Engine Instruments 20, HSI 19, ARC-210 18, NMSP 17, Light System Control Panel 17, Fuel System Control Panel 15, CMSP 15, UHF Radio 14, Environment Control Panel 13, CMSC 13.

## Plan

| Phase | What | Who | Output | Status |
| --- | --- | --- | --- | --- |
| 0 | Scope and layout | user, Claude | Decisions above | done |
| 1 | Collect sources | user, Claude | Table above | manual blocked by network policy |
| 2 | Read the manual: text extraction, chapter map, read only the cockpit, MFCD, CDU, UFC, HOTAS, start-up and weapons chapters | Claude | `PANELS.md`: one entry per panel with every control, its positions, lamps, displays and the manual page | open |
| 3 | Match with DCS-BIOS | Claude | Per panel: DCS-BIOS identifier of each control; gaps (keybind or `list_indication` candidates) | open |
| 4 | Reference pictures per planned panel page | Claude, then user (screenshots) | Pictures outside the repo; list of panels that need screenshots | open |
| 5 | Compare with the engine | Claude | List of engine changes, each with a user decision: single seat (no CP/G), MFCD / CDU / UFC drawings, export script arguments, trim display | open |
| 6 | A-10C spec | Claude writes, user reviews | Spec of views, panel pages, controls, keybinds | open |
| 7 | Research in DCS (needs the module) | user flies, Claude analyses | Read test and control sweep adapted from the `research-v1` tag; export arguments and MFCD indication numbers | open |
| 8 | Build plan and build | Claude delegates | Verified steps | open |
