# F-16C Viper – engine changes

What the dashboard engine (bridge, page, panel kit, export script, test kit) had to change so that the F-16C can use it next to the AH-64D and the A-10C II. F1 to F6 were planned in phase 5; F7 and F8 came up during the build. All eight are built. Based on [BIOS.md](BIOS.md) (the build type of every control) and on what the engine already does after the A-10C work ([../A10C/ENGINE.md](../A10C/ENGINE.md), E1 to E10, all built). The owner asked to go through all phases without stopping; the decisions below follow the recommendation and are listed for review at the end of the work (see [RESEARCH.md](RESEARCH.md), Questions).

Already enough for the F-16C, no change: several aircraft and the automatic aircraft choice (E1), one seat (E2), no trim display (E3), no levers (E4; the throttle is a keybind, only the cut-off `THROTTLE_OFF_IDLE` is in DCS-BIOS), panel kit with LAMP, BAR, scroll pages and the step rocker, key hats for the HOTAS (E8), per-aircraft memory (E9), the export script table per aircraft (E7; the F-16C table starts empty).

## Overview

| # | Change | Why | Decision | Size |
| --- | --- | --- | --- | --- |
| F1 | Page list scrolls | The long-hold page list cannot scroll; it already cuts off the 29 A-10C entries, and the F-16C has more than 40 panel pages | The page list scrolls inside its card, like a scroll page (frame, a moved touch never taps) | small |
| F2 | Coverage check per aircraft | `core/tools/test/coverage.py` only knows the A-10C docs | Takes the aircraft folder as an argument (`docs/A10C`, `docs/F16C`) | small |
| F3 | F-16C plate look | The owner wants a realistic F-16C look of its own | A third plate look `f16c` in the panel kit and the page, next to `ah64d` and `a10c` | small |
| F4 | MFD tab | Both F-16C MFDs have 20 OSBs and four corner rockers (GAIN, SYM, BRT, CON) | Reuse the A-10C `mfcd` layout: its four corner rocker places become usable by any aircraft (a control with that slot is drawn as a rocker; an empty place is drawn only if the aircraft lists it as inert, as the A-10C DSP, CON and SYM) | small |
| F5 | DED tab | The DED (live, 5 lines) and the ICP keypad form one unit | A panel kit page used as a tab (layout `panel` without `"panel": true`, so it is a tab and not a map page), with the DED as a kit display; no new hand-drawn layout. The layout checker and the sweep must cover such a tab (F8) | small |
| F6 | Export script | MFD labels would need the export script, as for the AH-64D MPD | F-16C table empty in version 1 (MFD screens stay empty, as on the A-10C) | none |
| F7 | Grid selector in two columns | CMDS MODE (6 positions) and CMDS PRGM (5) did not fit a 1 × 1 grid cell of FIGHT | A selector in a grid cell with more than 4 positions draws its buttons in two columns (`core/web/index.html`) | small |
| F8 | Layout checker measures kit tabs | `check_panels.js` opened only the pages of the long-hold page list, so the DED tab (a kit page used as a tab) was never measured | The checker also opens every kit page that is a tab (`core/tools/check_panels.js`) | small |

## Details

### F1 Page list scrolls

Before F1 the page list (long hold on COCKPIT) was a fixed card with two columns; with more entries than fit, the card grew past the screen and entries were cut off (found on the A-10C by the sweep). The list area now scrolls vertically inside the card (native thin scroll bar, no shaded edges or chevrons), the CLOSE button stays, a drag never opens a page. Fixes the A-10C at the same time. Not yet checked on the iPad ([../FIXES.md](../FIXES.md)).

### F2 Coverage check per aircraft

`coverage.py` read `docs/A10C/SPEC.md`, `BIOS.md` and the A-10C JSON. It now takes `--docs docs/<folder>` and reads that folder and the module of the aircraft file `aircraft/<folder in lower case>.py`; for any aircraft but the A-10C its page-to-panel table comes from the `Panels:` line of every page section of the spec. Default stays the A-10C. A tab without a page section (the F-16C DED) cannot be named.

### F3 F-16C plate look

A third look in `Panel(..., look=...)`: the colours, fasteners and label style of the F-16C consoles, chosen from the reference pictures in the layout step. As built: near-black plates, four cross-head screws at the places of the A-10C Dzus fasteners (same size and 22 du inset, drawn as `cross`), and semi-bold labels. The layout checker accepts both fastener kinds. Same part sizes and rules as every look.

### F4 MFD tab

The `mfcd` layout drew the A-10C bezel: 20 OSBs, the ADJ and BRT rockers, the PWR knob, and printed, inert DSP, CON and SYM rockers. As built, the four corner rocker places are generic slots `TL`, `TR`, `BL` and `BR`: an aircraft control with that slot is drawn there as a rocker (F-16C: GAIN at `TL`, SYM at `TR`, BRT at `BL`, CON at `BR`). The A-10C slots `ADJ` and `BRT` stay as aliases of `TL` and `BR`, so `aircraft/a10c.py` keeps its slot names (alternative: rename them and drop the aliases). Two view fields are new and both aircraft carry them: `titles` (side letter to the name on the side switch and in the title of the knob bar, for example `{"L": "LEFT MFD", "R": "RIGHT MFD"}`) and `inert` (the printed, inert rockers to draw, A-10C `["DSP", "CON", "SYM"]`, F-16C `[]`). The `DAY / NT / OFF` print is drawn only for a view that has a `PWR` control; the F-16C has none (the MFDs are powered from the avionics panel). The A-10C looks exactly as before.

### F5 DED tab

The F-16C DED and ICP are drawn with the panel kit as one page: the DED as a kit display of the five live lines (`DED_L1` … `DED_L5`; the `DED_LINE_n` ids are deprecated in DCS-BIOS), the ICP keys, rockers and knobs below it. The view is a tab, not a map page. It is a scroll page (640 × 844 du). The kit display shows plain text; the inverse and big marks of `DED_Ln_FORMAT` are not drawn.

### F6 Export script

The F-16C entry of the export script table exists and is empty (`["F-16C_50"] = {indications = {}, controls = {}}`).

### F7 Grid selector in two columns

The page draws the buttons of a selector in a grid cell one below the other. With more than 4 positions the stack becomes two columns (class `stack two`), so that CMDS MODE (6) and CMDS PRGM (5) fit a 1 × 1 cell. A-10C selectors have at most 4 positions and are unchanged. The buttons stay at the grid minimum of 44 px, under the 56 px rule (an existing point of the A-10C FLIGHT and FIGHT grids, see [../FIXES.md](../FIXES.md)).

### F8 Layout checker measures kit tabs

`core/tools/check_panels.js` opened every kit page from the long-hold page list, which holds only map pages. It now also opens every view that is a kit page and a tab (`kit` without `panel`) from the tab bar and measures it like the others, and it counts the cross-head screws of the `f16c` look (`.k-cross`) next to the Dzus fasteners (`.k-dzus`). `check_page.js` takes the seat names from `/layout`, so a one-seat aircraft needs no seat argument.

## Decisions

| # | Decision | Date |
| --- | --- | --- |
| F1 | As recommended | 2026-10-20 (owner review at the end) |
| F2 | As recommended | 2026-10-20 (owner review at the end) |
| F3 | Own `f16c` look (owner's wish) | 2026-10-20 |
| F4 | As recommended | 2026-10-20 (owner review at the end) |
| F5 | As recommended | 2026-10-20 (owner review at the end) |
| F6 | As recommended | 2026-10-20 (owner review at the end) |
| F7 | Decided during the build, the only way to fit the six-position CMDS MODE in a grid cell | 2026-10-21 (owner review at the end) |
| F8 | Decided during the build, needed to measure the DED tab | 2026-10-21 (owner review at the end) |
