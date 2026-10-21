# F-16C Viper – research notes

Working notes for adding the F-16C Viper (Block 50) to the dashboard. Our own notes only: the manual, its text and its pictures are copyrighted and are never committed. They are downloaded from the link below when needed and kept outside the repo.

Status: built except the keypress controls (the HOTAS key hats, speed brake, trim and nosewheel steering, which wait for the keybind export), tested only against the simulated DCS-BIOS, not in DCS. Phases 0 to 6 and 8 done; phases 7 and 9 need the module.

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

Everything that needs DCS or a look on the iPad, and the limitations of the build, is in the F-16C section of [../FIXES.md](../FIXES.md#f-16c-viper-under-development).

## Questions

Collected during the work for the owner's review. Choices the build took as recommended are written as `Decided:` in [SPEC.md](SPEC.md); the open ones are `Question:` there. One line each, by topic.

**Engine changes to consider**

- DEFOG lever (21 positions, `DEFOG_LEVER`): decided a chooser with 5 positions (MIN, 5, 10, 15, MAX), because the chooser does not scroll and a slider only sends 0 to 65535. Worth an engine change (a chooser that scrolls, or a slider with a maximum)?
- FUEL QTY SEL TEST (`FUEL_QTY_SEL_T_KNB`) has no readback and the kit has no command-only control: decided to leave TEST off. Add engine support for a command-only control?
- DED inverse and big characters (`DED_Ln_FORMAT`): decided to draw plain lines in version 1. Worth an engine change?
- THROTTLE OFF / IDLE: the engine has no guarded grid control, so the guarded button THROTTLE CUTOFF is on FUEL / EPU / START and FLIGHT cell [2,4] is empty (decided). Or add a guarded grid button and put it back on FLIGHT?
- ECM module buttons and RWR POWER are toggles in DCS-BIOS: decided push buttons (1, then 0 after 0.3 s), which may only flash the module in. Check in DCS; if needed, add a latching push button?
- The ECM T lamps and the AR RDY lamp are blue in DCS-BIOS and drawn white, because the kit has no blue lamp. Add blue?

**Look**

- The `f16c` colours (plate, cross-head screws, semi-bold labels) are read from the manual pictures only. Check them against DCS once you own the module.
- Guarded controls use the engine's guard cover, not the red flip guard of the real switches. Keep?

**Panel pages (decided as recommended, owner review)**

- EPU switch: one dashboard cover; the DCS covers `EPU_SW_COVER_OFF` and `EPU_SW_COVER_ON` are not used (check in DCS whether the switch moves with them closed).
- ENG CONT: guarded with its DCS cover `ENG_CONT_SW_COVER`; the cold start needs a cover tap before steps 59 and 62.
- FLCS BIT, MANUAL PITCH, EPU/GEN and OBOGS BIT: drawn spring-loaded although DCS-BIOS defines plain toggles.
- Autopilot PITCH switch: a plain three-position selector, not spring-loaded (DCS holds it with a solenoid; a momentary press would drop the autopilot). Reverses the spring rule of the spec.
- Guarded: EMER STORES JETT, HOOK and ALT GEAR; not DN LOCK REL and GND JETT ENABLE.
- UHF: the channel and the 10 / 1 / 0.1 MHz knobs are step rockers (more than 8 positions); A-3-2 and 0.025 are chooser knobs. Not the chooser knobs the spec first planned.
- IFF shares a page with the UHF backup panel and keeps only the C & I knob.
- Eyebrow lamps and the two indexers are one page.
- ALT REL and the ejection handle are left off.
- Controls on instruments have a page, INSTRUMENTS.
- CAUTION: the six blank cells stay inert; `LIGHT_CAUTION_1` to `LIGHT_CAUTION_6` stay unused.
- The diluter lever and the DL switch are kept although the manual says N/I (cold start names them).
- Scroll rule kept at 540 du: 8 of the 21 pages scroll (FUEL / EPU / START too); AUDIO is 546 du and stays a fixed page.
- Panels are grouped as in the spec (24 map boxes).

**FLIGHT, FIGHT, MFD, DED (decided as recommended, owner review)**

- HOTAS core set: key hats TMS, DMS, CMS and TRIM, two speed brake keys and NWS; the other grip controls are not planned. Their cells are reserved, not built.
- FLIGHT shows the cold start gauges as bars; HORN SILENCER and F-ACK have no cell. TMS, DMS and CMS are on FIGHT, TRIM on FLIGHT.
- FIGHT has no cell for A-A, A-G, FCR power and RWR power.
- MFD: the OSB numbering is the one of the shared `mfcd` layout (11 at the far right of the bottom row); a tap on a rocker sends one 0.3 s press and does not repeat.
- DED: the IFF override button, BRT and CONT wheels, TFR WX and the FLIR controls are left off; the DCS switch is four buttons in a cross.
- Lamp row: none on the MFD tab, MASTER CAUTION on the DED tab.

**Still open**

- The key names in the spec are placeholders until the keybind export (the NWS key may be the Missile Step button itself).

## Plan

| Phase | What | Who | Output | Status |
| --- | --- | --- | --- | --- |
| 0 | Scope and decisions | user, Claude | Decisions above | done |
| 1 | Collect sources | user, Claude | Table above | manual and DCS-BIOS done; keybinds and screenshots need the module |
| 2 | Read the manual: every cockpit panel, the HOTAS, the HUD control panel, ICP / DED, MFD, autopilot, the defensive panels, the cold start | Claude | [PANELS.md](PANELS.md): 75 panel sections, 398 controls; [STARTUP.md](STARTUP.md): cold start in 117 steps up to Before Taxi | done |
| 3 | Match with DCS-BIOS, with the per-id check of input kind, readback and position order | Claude | [BIOS.md](BIOS.md): 398 rows (236 read + command, 107 read only, 55 none) plus 40 DCS-BIOS-only controls; Build and Position order columns; 1 id without readback, 99 guessed position orders; cold start: 62 of 117 steps fully possible, 36 checks, 6 keybinds | done |
| 4 | Reference pictures per panel, quality, screenshot needs | Claude, then user (screenshots) | [PICTURES.md](PICTURES.md): 74 panels, 42 good, 27 partial, 5 poor; 6 screenshots needed (throttle, canopy switch and handle, handcrank, ANTI-G TEST, right console fittings, chaff/flare button) | done |
| 5 | Compare with the engine: page list scroll, coverage per aircraft, reuse of the MFD and keypad layouts, the F-16C look | Claude, user decides | [ENGINE.md](ENGINE.md): 6 changes F1–F6 (page list scroll, coverage per aircraft, `f16c` look, MFD on the `mfcd` layout, DED tab as a kit page, export table empty), decided as recommended, owner review at the end | done |
| 6 | F-16C spec with the real fit check: COCKPIT map, panel pages, FLIGHT / FIGHT with 2 × 2 key hats, MFD, DED | Claude writes, user reviews | [SPEC.md](SPEC.md): 5 tabs, COCKPIT map with 21 panel pages and 3 link boxes, FLIGHT / FIGHT with reserved 2 × 2 key hat cells, MFD, DED kit page; fit check per page (estimate: 7 scroll pages plus the DED tab; built: 8); 29 questions for the owner | done (owner review at the end) |
| 7 | Research in DCS (needs the module): keybinds, screenshots, position orders that are guesses | user flies, Claude analyses | updated BIOS.md and SPEC.md | open |
| 8 | Engine fixes, then the build in batches, each tested; AH-64D and A-10C rechecked every step | Claude delegates | `aircraft/f16c.py`: 21 panel pages, FLIGHT, FIGHT, MFD and DED, with engine changes F1 to F8 ([ENGINE.md](ENGINE.md)). Tested against the simulated DCS-BIOS, the AH-64D and A-10C rechecked. Not built: the keypress controls (HOTAS key hats, speed brake keys, NWS), the MFD screen, inverse DED characters | done |
| 9 | Test run in DCS, open points updated | user flies, Claude fixes | FIXES.md | open |
