# A-10C II – engine changes

What the dashboard engine (bridge, page, panel kit, export script) must change so that a second aircraft, the single-seat A-10C II, can use it next to the AH-64D. Based on a full read of the code (findings with file and line references were collected during phase 5) and on [BIOS.md](BIOS.md). Every change has options, a recommendation and a decision (all decided on 2026-10-18, see the table at the end). Nothing is built before the A-10C spec (phase 6) is approved.

Already generic and unchanged: DCS-BIOS decoding and commands (`core/dcsbios.py`), keypresses (`core/keys.py`, apart from its key table), log, config loader, HTTP server, settings page, guard covers, knob bar, chooser, the panel-page builders and the multi-line text display of the panel kit.

## Overview

| # | Change | Why | Recommendation | Size |
| --- | --- | --- | --- | --- |
| E1 | Aircraft selection | Only the `[dcs] aircraft` setting chooses the aircraft file; default AH-64D | Automatic from DCS-BIOS `_ACFT_NAME`, setting kept as override | medium |
| E2 | Seats optional | `SEAT_POSITION` is required: the bridge stops at start for the A-10C; the page knows only PILOT / CP/G | Seats defined by the aircraft file; one seat = no badge switch, no debug seat | medium |
| E3 | Trim display optional | Trim tracking reads `{seat}_CYCLIC_TRIM_UD`; the A-10C trim hat is not in DCS-BIOS (the reader thread would stop) | Trim display only for aircraft that define it; not for the A-10C | small |
| E4 | Power levers optional | 8 `power_*` keys and the lever model are required for every aircraft; A-10C throttles are read only in DCS-BIOS | Levers only for aircraft that define them; A-10C throttle shown as a gauge in version 1 | small |
| E5 | Display pages (MFCD, CDU, UFC) | MPD, TEDAC and KU are hand-drawn AH-64D layouts in the page | **Decided:** hand-drawn MFCD, CDU and UFC layouts, like MPD and KU | small in the engine, work in the aircraft file |
| E6 | Panel kit additions | No plain legend lamp outside a dial (caution panel), lit colours only green and amber, plate budget 640 × 600 du | Add a LAMP part and red / white / blue lit styles. **Decided:** A-10C-specific look | small |
| E7 | Export script per aircraft | Cockpit arguments and MPD indication numbers are hard-coded for the AH-64D; the script does not know the aircraft | Tables per aircraft name in the script; A-10C version 1 needs none | small |
| E8 | Keys | Key table lacks numpad, Tab, Esc, punctuation; trim reset key required for every aircraft | Add keys when the A-10C keybinds need them; required keys per aircraft | small |
| E9 | Per-aircraft memory and docs | Remembered tab / MPD side not scoped by aircraft; README and SPEC say "AH-64D only" | Scope by aircraft; docs updated at the end | small |

## Details

### E1 Aircraft selection

Today: `aircraft = "AH-64D"` in `config/config.toml` (default) loads `aircraft/ah64d.py` once at start. In an A-10C mission the user would have to edit the config and restart.

DCS-BIOS always sends the aircraft name as `_ACFT_NAME` (24 characters at address 0x0000 of the stream the bridge already decodes): `AH-64D_BLK_II` for the Apache, `A-10C_2` for the A-10C II, `NONE` without an aircraft.

- Option A – manual: keep the setting; the user sets `aircraft = "A-10C"` before flying the A-10C. No code beyond E2–E4.
- Option B – automatic: every aircraft file lists its DCS names (`DCS_NAMES = ["A-10C_2"]`); the bridge loads all aircraft files at start, reads `_ACFT_NAME` and switches the active aircraft when it changes; the page reloads `/layout` when the bridge reports a new aircraft. The setting stays as an override.
- Recommendation: B. It fits "same layout for every aircraft" and a mission change without restarting. Cost: the bridge must hold one control list per aircraft (both DCS-BIOS JSON files) and the page must reload its layout. **Decided:** automatic, plus a manual switch in the settings page for debugging; the `[dcs] aircraft` setting stays as an override (default `auto`), as recommended.

### E2 Seats optional

Today: the seat output `SEAT_POSITION` is always read (missing → the bridge stops: `Not in DCS-BIOS: SEAT_POSITION`); `SEAT_NAMES` {0: PLT, 1: CPG}, `MPD_SEATS`, the badge texts PILOT / CP/G, the debug seat and the "read only" refusals assume two seats; a missing seat value means `NO DCS DATA` in the page.

- Recommendation: the aircraft file declares its seats and the seat output, for example `SEATS = [{"prefix": "PLT", "label": "PILOT"}, {"prefix": "CPG", "label": "CP/G"}]` and `SEAT_OUTPUT = "SEAT_POSITION"`; the A-10C has one seat and `SEAT_OUTPUT = None` (seat always 0). The page takes the seat labels from `/layout`; with one seat the badge shows the aircraft (for example `A-10C`) and has no debug-seat hold; "DCS data present" is taken from the packet age instead of the seat value. `{seat}` placeholders keep working (the A-10C simply has none in its ids).

### E3 Trim display optional

Today: `track_trim` reads `{seat}_CYCLIC_TRIM_UD` after every DCS-BIOS packet and `trim_reset` is a required key. For an aircraft without that output the reader thread would end on the first packet (KeyError).

- Recommendation: trim tracking only when the aircraft file defines its trim data (`TRIM_SWITCH`, `TRIM_RELEASED`, `CONTROL_NAMES`); `trim_reset` required only then. The A-10C trim hat is a keybind with no readback, so the A-10C gets no trim display in version 1.

### E4 Power levers optional

Today: the lever model (`LEVER_KEYS`: OFF / IDLE / FLY, one key per step, a fourth position "not available") and its 8 `power_*` keys are required for every aircraft. The A-10C throttles are read only in DCS-BIOS (`ENG_THROTTLE_L` / `_R`); whether DCS has keys to set them to OFF / IDLE is only known after the DCS research (phase 7).

- Recommendation: the lever keys belong to the aircraft file and are required only when the aircraft has `lever` controls. A-10C version 1 shows the two throttle positions as read-only gauges; a throttle command follows if phase 7 finds usable keys.

### E5 Display pages (MFCD, CDU, UFC)

Today: the MPD, TEDAC and KU are hand-drawn AH-64D pages in `core/web/index.html` (fixed SVG bezels, the 24-button PB numbering, `parse_mpd_labels` for the Apache text format).

- Option A – new hand-drawn layouts `mfcd`, `cdu`, `ufc` in the page, like `mpd` and `ku`.
- Option B – build them with the panel kit as panel pages: a CDU plate with a 10-line `display` (`CDU_LINE0` … `CDU_LINE9`, the kit's multi-line display already exists) and its keys; a UFC plate with its keypad; an MFCD plate with the 20 OSBs, rockers and DAY / NT / OFF around an empty screen (no live OSB labels in version 1: DCS-BIOS has no MFCD text).
- Recommendation: B. No new page code; the same look as every other panel; live MFCD labels can follow later through the export script (E7). Open: the CDU has about 60 keys plus the display; it may not fit the 640 × 600 du plate budget at the 56 px touch minimum, so it may need two pages (display with line keys; keyboard) or a larger budget for keypad pages. **Decided: option A** (hand-drawn layouts), see Decisions.
- Tab name: the display tab is named by the aircraft file (MPD for the AH-64D, MFCD or CDU for the A-10C), the same tab position for every aircraft.

### E6 Panel kit additions

- Caution light panel (48 legend lamps) and other indicator lamps need a plain LAMP part (legend lamp, no button); today free lamps exist only inside a dial.
- Lit colours exist only for green and amber on plates; the A-10C needs red, and probably white and blue (to confirm with the pictures in PICTURES.md).
- Plate look: every plate has four corner ears and screws in the AH-64D style. Recommendation: keep one look for every aircraft (simpler, consistent); the A-10C panels look slightly different in reality. **Decided: A-10C-specific look**, see Decisions.
- Plate budget 640 × 600 du: most A-10C panels fit; the CDU is the exception (see E5).

### E7 Export script per aircraft

Today: the cockpit arguments 470–478 (stick and pedal positions) and the MPD indications 7 / 9 / 11 / 13 are hard-coded and sent in every aircraft.

- Recommendation: one script with one table per aircraft name (`LoGetSelfData().Name`): AH-64D as today; A-10C empty in version 1 (no trim display, no MFCD labels). The A-10C arguments and indication numbers come from phase 7 and are added later.

### E8 Keys

- `core/keys.py` knows modifiers, letters, digits, F1–F12, Home / End / PageUp / PageDown / Insert / Delete, arrows, Space and Enter. If an A-10C default keybind (HOTAS: TMS, DMS, coolie hat, CMS, speed brake, trim) uses numpad, Tab, Esc or punctuation keys, the table gets those keys. Known once the A-10C keybinds are exported from DCS (phase 1, needs the module).
- HOTAS buttons on the dashboard use the existing `key` and `macro` controls (one button per direction; a long press is a macro with a 1 s hold); no new control type.

### E9 Per-aircraft memory and docs

- The page remembers the last tab and MPD side in the browser without the aircraft; scope these by aircraft.
- README and SPEC say "AH-64D only" in many places; section 8 of SPEC ("Adding another aircraft") lists fewer exceptions than this analysis found. Update both after the A-10C works.

## Decisions

| # | Decision | Date |
| --- | --- | --- |
| E1 | Automatic from the DCS-BIOS aircraft name (`_ACFT_NAME`); for debugging the aircraft can also be switched by hand in the settings page | 2026-10-18 |
| E2 | As recommended: seats and seat output declared by the aircraft file; one seat = badge shows the aircraft, no debug-seat hold | 2026-10-18 |
| E3 | As recommended: trim display only for aircraft that define it; none for the A-10C in version 1 | 2026-10-18 |
| E4 | As recommended: lever keys only for aircraft with levers; A-10C throttles as read-only gauges in version 1 | 2026-10-18 |
| E5 | Option A: hand-drawn layouts for MFCD, CDU and UFC, like the AH-64D MPD and KU | 2026-10-18 |
| E6 | A-10C-specific look for the A-10C panel pages (not the AH-64D plate style) | 2026-10-18 |
| E7 | As recommended: one export script with a table per aircraft name; A-10C table empty in version 1 | 2026-10-18 |
| E8 | As recommended: add keys when the exported A-10C keybinds need them; HOTAS buttons as key / macro controls; required keys per aircraft | 2026-10-18 |
| E9 | Docs first: update README and SPEC for several aircraft before building; remembered tab and display side scoped by aircraft | 2026-10-18 |
