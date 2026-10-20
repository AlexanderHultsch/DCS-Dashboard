# F-16C Viper – engine changes

What the dashboard engine (bridge, page, panel kit, export script, test kit) must change so that the F-16C can use it next to the AH-64D and the A-10C II. Based on [BIOS.md](BIOS.md) (the build type of every control) and on what the engine already does after the A-10C work ([../A10C/ENGINE.md](../A10C/ENGINE.md), E1 to E10, all built). The owner asked to go through all phases without stopping; the decisions below follow the recommendation and are listed for review at the end of the work (see [RESEARCH.md](RESEARCH.md), Questions).

Already enough for the F-16C, no change: several aircraft and the automatic aircraft choice (E1), one seat (E2), no trim display (E3), no levers (E4; the throttle is a keybind, only the cut-off `THROTTLE_OFF_IDLE` is in DCS-BIOS), panel kit with LAMP, BAR, scroll pages and the step rocker, key hats for the HOTAS (E8), per-aircraft memory (E9), the export script table per aircraft (E7; the F-16C table starts empty).

## Overview

| # | Change | Why | Decision | Size |
| --- | --- | --- | --- | --- |
| F1 | Page list scrolls | The long-hold page list cannot scroll; it already cuts off the 29 A-10C entries, and the F-16C has more than 40 panel pages | The page list scrolls inside its card, like a scroll page (frame, a moved touch never taps) | small |
| F2 | Coverage check per aircraft | `core/tools/test/coverage.py` only knows the A-10C docs | Takes the aircraft folder as an argument (`docs/A10C`, `docs/F16C`) | small |
| F3 | F-16C plate look | The owner wants a realistic F-16C look of its own | A third plate look `f16c` in the panel kit and the page, next to `ah64d` and `a10c` | small |
| F4 | MFD tab | Both F-16C MFDs have 20 OSBs and four corner rockers (GAIN, SYM, BRT, CON) | Reuse the A-10C `mfcd` layout: its four corner rocker places become usable by any aircraft (a control with that slot is drawn as a rocker; an empty place is drawn only if the aircraft lists it as inert, as the A-10C DSP, CON and SYM) | small |
| F5 | DED tab | The DED (live, 5 lines) and the ICP keypad form one unit | A panel kit page used as a tab (layout `panel` without `"panel": true`, so it is a tab and not a map page), with the DED as a kit display; no new hand-drawn layout. The layout checker and the sweep must cover such a tab | small |
| F6 | Export script | MFD labels would need the export script, as for the AH-64D MPD | F-16C table empty in version 1 (MFD screens stay empty, as on the A-10C) | none |

## Details

### F1 Page list scrolls

Today the page list (long hold on COCKPIT) is a fixed card with two columns; with more entries than fit, the card grows past the screen and entries are cut off (found on the A-10C by the sweep). The list gets the scroll behaviour of the scroll pages: the list area scrolls vertically inside the card, the CLOSE button stays, a drag never opens a page. Fixes the A-10C at the same time.

### F2 Coverage check per aircraft

`coverage.py` reads `docs/A10C/SPEC.md`, `BIOS.md` and the A-10C JSON. It gets an aircraft argument and reads `docs/<folder>/` and the module of that aircraft file; its page-to-panel table comes from the aircraft's spec. Default stays the A-10C.

### F3 F-16C plate look

A third look in `Panel(..., look=...)`: the colours, fasteners and label style of the F-16C consoles, chosen from the reference pictures in the layout step (dark panels, white placard text, the F-16C screw heads). Same part sizes and rules as every look.

### F4 MFD tab

The `mfcd` layout draws the A-10C bezel: 20 OSBs, the ADJ and BRT rockers, the PWR knob, and printed, inert DSP, CON and SYM rockers. The four corner rocker places become generic: an aircraft control with that slot is drawn there as a rocker; inert printed rockers are drawn only where the aircraft view lists them. The F-16C has no PWR knob on the bezel (the MFDs are powered from the avionics panel). The A-10C stays exactly as it is.

### F5 DED tab

The F-16C DED and ICP are drawn with the panel kit as one page: the DED as a kit display of the five live lines (`DED_L1` … `DED_L5`; the `DED_LINE_n` ids are deprecated in DCS-BIOS), the ICP keys, rockers and knobs below it. The view is a tab, not a map page. If it does not fit 640 × 600 du it is a scroll page.

## Decisions

| # | Decision | Date |
| --- | --- | --- |
| F1 | As recommended | 2026-10-20 (owner review at the end) |
| F2 | As recommended | 2026-10-20 (owner review at the end) |
| F3 | Own `f16c` look (owner's wish) | 2026-10-20 |
| F4 | As recommended | 2026-10-20 (owner review at the end) |
| F5 | As recommended | 2026-10-20 (owner review at the end) |
| F6 | As recommended | 2026-10-20 (owner review at the end) |
