# F-16C Viper – research notes

Working notes for adding the F-16C Viper (Block 50) to the dashboard. Our own notes only: the manual, its text and its pictures are copyrighted and are never committed. They are downloaded from the link below when needed and kept outside the repo.

Status: planned. Phases 0 to 4 done, nothing built.

## Decisions

- Aircraft: F-16C Viper only (DCS-BIOS module `F-16C_50`).
- Tabs: the same scheme as the other aircraft: **COCKPIT | FLIGHT | FIGHT | MFD | DED**. COCKPIT is the cockpit map with one page per panel that has a function in DCS; MFD shows both MFDs, one at a time; DED shows the live DED with the ICP keypad. GEORGE is AH-64D only.
- HOTAS: the core set, as keypresses (DCS-BIOS has no grip controls).
- Look: an F-16C-specific, realistic panel look of its own (not the AH-64D or A-10C plate style).
- Module: not owned yet. So the A-10C order applies: build first from the manual and DCS-BIOS; keybinds, screenshots and the DCS checks (phase 7) follow when the module is installed. The keypress controls wait for the keybind export.
- Aircraft choice: automatic, as for every aircraft (`_ACFT_NAME` `F-16C_50`).
- Reference material (manual pages, screenshots) is used to draw the panels; it stays out of the repo.

## Sources

| Source | Where | Notes |
| --- | --- | --- |
| Early Access Guide (EN, 774 pages, 58 MB) | https://www.digitalcombatsimulator.com/upload/iblock/e78/33zl8132hi71d3tv0194vvkzpzl3mrr6/DCS%20F-16C%20Early%20Access%20Guide%20EN.pdf | Needs `www.digitalcombatsimulator.com` in the cloud environment's allowed domains. Printed page numbers equal PDF page numbers. Relevant: cockpit overview pp. 43–82, HOTAS pp. 83–89, HUD control panel pp. 94–97, ICP and DED pp. 98–121, MFD pp. 122–126, autopilot pp. 129–132, start-up pp. 133–140, defensive systems (RWR, CMDS, ECM panels) pp. 692–708, radios in the appendix from p. 730 |
| DCS-BIOS module | `Scripts/DCS-BIOS/lib/modules/aircraft_modules/F-16C_50.lua` (DCS-Skunkworks), control list `doc/json/F-16C_50.json` | One module `F-16C_50`, also used by the F-16D and F-16I variants; about 520 controls |
| Default keybinds | DCS controls settings, exported as HTML | Needs the module installed (phase 7) |
| Cockpit screenshots | One per panel, straight on | Needs the module installed; only for panels the manual shows poorly |

DCS-BIOS panel groups with the most controls: warning, caution and indicator lights 129, UFC (ICP) 29, left and right MFD 24 each, UHF 16, fuel system 14, ECM 13, control interface 13, CMDS 13, RWR 12, audio panel 12, ADI 12, IFF 10. Live text: the five DED lines (`DED_LINE_1` … `DED_LINE_5`), the CMDS counts, the UHF channel and frequency, the EHSI text.

## Method

The A-10C method, improved with what the A-10C build taught:

1. **Control types decided while mapping (phase 3).** A script reads the DCS-BIOS list and gives every id its input kind (absolute value, steps only, relative only), whether the bridge can read it back under its own name, and the position order from the DCS-BIOS description. BIOS.md gets a "how to build" column; every position order that is a guess is listed for phase 7.
2. **Real fit check in the spec (phase 6).** Each panel page is laid out roughly with the real panel kit part sizes before the spec is approved, so the spec says which pages scroll. The A-10C estimates were wrong for 9 of 23 pages.
3. **HOTAS key hats in 2 × 2 grid cells** from the start; FLIGHT and FIGHT are planned with that.
4. **Test kit from day one** (`core/tools/test`): layout checker, command test, sweep and screenshots after every step, and the AH-64D and A-10C checks after every step, so nothing that works breaks.
5. **Engine fixes first** (phase 5): the long-hold page list must scroll (it already cuts off the A-10C list); the id coverage check becomes per aircraft; the MFD and DED tabs reuse the A-10C MFCD and CDU layouts where they fit.
6. **Smaller build batches** of about four panel pages, each reviewed against the reference pictures.

## Open points

None yet.

## Plan

| Phase | What | Who | Output | Status |
| --- | --- | --- | --- | --- |
| 0 | Scope and decisions | user, Claude | Decisions above | done |
| 1 | Collect sources | user, Claude | Table above | manual and DCS-BIOS done; keybinds and screenshots need the module |
| 2 | Read the manual: every cockpit panel, the HOTAS, the HUD control panel, ICP / DED, MFD, autopilot, the defensive panels, the cold start | Claude | [PANELS.md](PANELS.md): 75 panel sections, 398 controls; [STARTUP.md](STARTUP.md): cold start in 117 steps up to Before Taxi | done |
| 3 | Match with DCS-BIOS, with the per-id check of input kind, readback and position order | Claude | [BIOS.md](BIOS.md): 398 rows (236 read + command, 107 read only, 55 none) plus 40 DCS-BIOS-only controls; Build and Position order columns; 1 id without readback, 99 guessed position orders; cold start: 62 of 117 steps fully possible, 36 checks, 6 keybinds | done |
| 4 | Reference pictures per panel, quality, screenshot needs | Claude, then user (screenshots) | [PICTURES.md](PICTURES.md): 74 panels, 42 good, 27 partial, 5 poor; 6 screenshots needed (throttle, canopy switch and handle, handcrank, ANTI-G TEST, right console fittings, chaff/flare button) | done |
| 5 | Compare with the engine: page list scroll, coverage per aircraft, reuse of the MFD and keypad layouts, the F-16C look | Claude, user decides | ENGINE.md | open |
| 6 | F-16C spec with the real fit check: COCKPIT map, panel pages, FLIGHT / FIGHT with 2 × 2 key hats, MFD, DED | Claude writes, user reviews | SPEC.md | open |
| 7 | Research in DCS (needs the module): keybinds, screenshots, position orders that are guesses | user flies, Claude analyses | updated BIOS.md and SPEC.md | open |
| 8 | Engine fixes, then the build in batches, each tested; AH-64D and A-10C rechecked every step | Claude delegates | aircraft/f16c.py and page code | open |
| 9 | Test run in DCS, open points updated | user flies, Claude fixes | FIXES.md | open |
