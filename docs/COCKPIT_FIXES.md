# Cockpit pages: fix round 1

Spec for the fixes after the first test of the COCKPIT pages on the tablet ([COCKPIT.md](COCKPIT.md) describes the pages). Status: spec only, nothing built yet.

Sources: the 11 tablet screenshots of the pilot pages (iPad Air, no DCS data), the dashboard log and `dcs.log` of the same session, and the code.

## 1. What the test showed

Every finding of the test list was checked against the screenshots and the code.

| # | Finding | Confirmed | Cause | Fix in |
| --- | --- | --- | --- | --- |
| 1 | Switches are not intuitive to operate | Yes. A switch is split into invisible bands (3 stacked touch zones) that nobody can see or guess. | Plate switches are touch bands inside the drawing | 6 |
| 2 | Pop-ups appear in the middle of the screen | Yes. The knob bar is centred in the controls area (`openBar`: left / top from the area centre), not at the control. | Fixed placement, no clamping logic per control | 5 |
| 3 | Knobs look like flat discs | Yes. `knobArt` draws two plain circles and a pointer. | No rim, no grip, no shading | 7 |
| 4 | Screws are not aligned, on nearly every page | Yes. Every page lists its screws as free `[x, y, r]` coordinates measured from one photo, with random sizes (radius 9 to 19) and angles `(x + y) % 90`. Corner ears (brackets) shift them further. | No shared frame, no standard screw | 4 |
| 5 | Same buttons have different sizes on different pages | Yes. Square pushbuttons measure about 56 to 166 css px across the pages at 1180 x 820 (EUFD keys 56, JETT stations 137, ARMAMENT 98, EMERGENCY 155 to 166, TAIL WHEEL 164). Two causes: every photo has its own pixel density (button face 38 to 124 photo px), and each page is scaled separately to fill the screen. | Per-page photo scale | 2, 3 |
| 6 | Labels collide with items, buttons overlap the base plate | Yes, see the page list in section 9. | Labels are hand-placed `print` entries with no collision check | 3, 8 |
| 7 | FIRE page did not work on the first try | Partly explained by the log (section 10): the ENG 1 FIRE press is sent but `not confirmed` (twice), the CMWS JETT switch too; PRI and JETT presses are confirmed. The three buttons with a real DCS cover are the ones that fail. | DCS needs its own cover open | 10 |
| 8 | Back button uses an emoji | Yes. `◀` (U+25C0) in the tab label is drawn as the blue emoji on iOS. The TEDAC AZ hat labels use U+25C0 / U+25B6 too. | Text glyph | 11 |
| 9 | TAIL WHEEL cover and button are not centred to each other | Yes, not intended. The white frame is a separate `outline` art entry, drawn about 32 px from the button on the left and about 15 px on the right (top 30, bottom 15). | Frame and button are two unrelated coordinates | 3 |

Two root causes explain most of this: **every page is drawn on its own from photo coordinates**, and **there is no shared set of parts**. The fix is a shared kit and a page frame (sections 2 to 4), then re-laying the pages on it (section 9).

Good news from the same session: the export timing line works. `dcs.log` shows about 3 to 4 ms per second of model time (0.3 to 0.4 % of one core, max frame 5 ms). Nothing to do.

## 2. One scale for all pages

- **Design unit (du).** All panel geometry is written in design units, not in photo pixels. One du is the same size on every page.
- **Global scale.** The page does not fit each panel to the screen separately. It computes one scale `S = min(areaWidth / widestPanel, areaHeight / tallestPanel)` over all pages of the seat (and the same value for both seats, so the pilot and the CP/G pages match) and renders every page at `S`, centred. Small panels (FIRE, TAIL WHEEL) therefore become smaller than today, large ones (COMM, POWER) stay about the size they are. Cap `S` at 1.6.
- **Budget.** The largest page must stay at or under 640 x 600 du so `S` is about 1.16 at 1180 x 820 and about 1.07 at 1024 x 768. Every standard part below is sized so its touch area is at least 56 css px at that `S`.
- The photo is the reference for what is on a panel, its text and the arrangement of the parts. It is not the reference for pixel sizes.

## 3. The part kit (one place)

All parts are defined once, in `aircraft/panel_kit.py` (the AH-64D file only places parts and sets text). The kit is sent to the page with the layout (`/layout` gets a `kit` entry), so the page has no hard-coded sizes. A page entry names a part and a centre point, never a size.

| Part | Size (du) | Used for |
| --- | --- | --- |
| `PUSH` square pushbutton | bezel 84 x 84, face 60 x 60 | all square pushbuttons (GUARD, XPNDR, EMERG HYD, TAIL WHEEL, A/S, GND ORIDE, the 6 station buttons, FIRE / PRI / RES, EUFD keys use `PUSH_SMALL` 56 x 56) |
| `PUSH` frame variant | white frame 100 x 100, 4 stroke, centred on the button by construction | GUARD, XPNDR, TAIL WHEEL, A/S, GND ORIDE |
| `ROUND` pushbutton | 64 | DEFOG, IDENT, PRESS TO TEST, ACM cap |
| `PLUNGER` | 100 | JETT |
| `TOGGLE` | ring 56, lever 40 | all toggle switches (NAV, ANTI COL, NVS, CKT A / B, GEN RST, SQL x 5, ICS, ARM, CMWS, BYPASS, FIRE TEST, ZEROIZE, MASTER ZEROIZE, CMWS JETT, PARK BRAKE, RTR BRK, ENG START) |
| `ROTARY` | 100 | MSTR IGN, CMWS PWR, WIPER |
| `KNOB_L` / `KNOB_M` / `KNOB_S` | 96 / 72 / 56 | L: MASTER, IHADSS, FLIR, EUFD BRT. M: FORM, SIGNAL, PRIMARY, FLOOD, STBY INST, SYM BRT, AUDIO, LAMP, SENS, ALT SET. S: the 5 radio volumes and the 5 AUX knobs |
| `ROCKER` | 52 x 100 | EUFD WCA / IDM / RTS |
| `CHIP` | 64 x 22 | PULL chips |
| `SLIDER`, `LEVER` | track 40 x 200, slot per page | FRICT, power levers |
| `GUARD_COVER` | the guarded part + 12 du on each side, frame 14 wide, padlock 24 | all guarded parts; derived from the part, never typed in |
| `HAZARD_PAD` | the part (or its cover) + 20 du on each side | JETT pad, EMERG HYD pad, CMWS strip |
| `SCREW_L` / `SCREW_M` / `SCREW_S` | 26 / 18 / 12 | section 4 |
| Label styles | `TITLE` 32, `NAME` 24, `POS` 20, `SMALL` 16 | every printed text; one font, one weight per style |

Rules:

- **A part carries its own frame, cover and legend.** A framed button is one part (button plus frame, centred by construction), a guarded part is one part (part plus cover), a hazard pad is sized from what is inside. Nothing is placed twice by hand.
- **The same part is the same size everywhere**, on every page and both seats. A page cannot change a size; at most it picks the variant.
- Parts sit on a **10 du grid**; centres are multiples of 5 du.

## 4. Page frame and the screw system

- A page has one **plate**: width and height in du (multiples of 10), corner radius 16, border 3, no ears (see decision 1). Content keeps at least 36 du from the plate edge.
- **Outer screws** (`SCREW_L`): four, exactly on the corners of an inner rectangle 24 du from each edge. All four corner screws therefore share two x values and two y values, on every page.
- **Edge screws** (`SCREW_M`, optional flag `edge_screws`): at the middle of the top and bottom edge, on the same horizontal lines as the corner screws (and optionally the left / right edge on the same vertical lines).
- **Inner screws** (`SCREW_S`, optional): a page cannot give free coordinates. An inner screw is placed by naming two **lines** from the page's line table: the plate lines (`L`, `R`, `T`, `B`, `CX`, `CY`), the corner screw lines, or the centre line of a placed part (`part.cx`, `part.cy`). So an inner screw always shares an x or y with something visible.
- **Rotation:** the three screw drawings are fixed; the slot angle comes from a short fixed list by position index (for example 15, 100, 65, 140 degrees), so a plate looks natural but never random.
- A plate with several panels (ARMAMENT + VIDEO + MASTER ZEROIZE, CENTER) has one plate per panel; the plates share a width (or sit on a common edge line) and a fixed 16 du gap.

## 5. Pop-up placement

Applies to the knob bar and to the new switch chooser (section 6).

- **Anchored to the control.** The pop-up opens at the control, not in the middle of the screen.
  - Switch chooser: centred on the switch.
  - Knob bar (420 x 120): centred on the knob horizontally, directly below it (8 px gap); if there is no room below, directly above; if neither fits, centred on the knob.
- **Never out of bounds.** After placing, the pop-up is clamped into the safe rectangle: the screen minus the tab bar and lamp row above, an 8 px margin on every side, and the gear (44 x 44 plus its 8 px offset) at the bottom right. This is one function (`place(anchorRect, popupSize)`), used by both pop-ups.
- The full-screen scrim stays (a tap outside closes without a command).
- For the knob bar the knob should stay visible where possible, so the bar sits next to it, not on it.

## 6. Switch chooser (replaces the invisible bands)

- A tap on a **plate switch** (any toggle, the rotary selectors, 2-position switches) opens the chooser at the switch. The switch has one touch area (the whole switch, at least 56 px), no bands.
- The chooser shows one big button per position (64 x 64 px minimum, label from the position), **arranged like the switch itself**:
  - vertical toggle: a column, in the order printed on the panel, top to bottom (for example ENABLE, OFF, DISABLE; START, OFF, IGN ORIDE; BRT, OFF, DIM; FIXED, NORM, OFF);
  - horizontal toggle (`orient: h`): a row, left to right (GEN 1, OFF, GEN 2; "1", OFF, "2");
  - rotary: the buttons sit on a small circle at the same angles as the positions on the dial (OFF, BATT, EXT PWR; PARK, OFF, LO, HI), so the geometry matches;
  - 2 positions: two buttons in the same orientation as the switch.
- The current position is highlighted (from the DCS readback). A position that cannot be used (`disabled`, for example EXT PWR, BRK) is greyed out and not selectable. A spring-return position (`momentary`) carries a small spring mark; selecting it runs the same press as today (the bridge holds it, then returns to rest).
- A small title line shows the switch name (for example ENG START NO 1).
- A tap on a position sends the command through the existing path (same confirmation and error toasts) and closes the chooser. A tap outside closes it without a command.
- **Not changed:** guarded switches (ZEROIZE, MASTER ZEROIZE, CMWS JETT) keep cover, then press and hold (decision 2). The power levers, the FRICT slider, the rockers, buttons and the quick pages (FLIGHT, FIGHT, MPD, KU) are unchanged (decision 3).

## 7. Knob look

One shared drawing per knob size, so all knobs look the same family. Layers, bottom to top:

1. a soft drop shadow;
2. a dark rim (skirt) with a radial gradient;
3. a **grip ring**: 24 raised ridges around the rim (a dashed ring in a lighter grey), the visible cue that it turns;
4. the cap: radial gradient with the highlight at the upper left, a thin bevel ring;
5. a raised pointer ridge from the centre to the rim (dark edge, light core) with a small tip at the rim. It rotates with the value as today.

`KNOB_L` gets a second, wider skirt. The rotary selectors use the same drawing in a dark colourway. The drawing is defined once (an SVG symbol reused for every knob), so it costs nothing at runtime. The printed scale marks (MIN, MAX, OFF, BRT) stay page text and move with the labels (section 8).

## 8. Labels and the layout checker

- Every label is attached to a part by an anchor (`above`, `below`, `left`, `right`) with a fixed gap of 8 du, in one of the four styles. A free-floating label needs an explicit reason (titles, bracket text) and is placed on the grid.
- Position labels of switches and dials (OFF, BATT, ...) come from the part's own label layout (a fixed set of presets per part), not from per-page numbers.
- **Checker.** `tools/check_panels.js` runs in the browser console. For every page of the seat it measures all label, part, screw and plate boxes and reports:
  1. a label box overlapping a part, another label, a screw or the plate edge (closer than 6 du);
  2. a part overlapping a part or the plate edge (closer than 12 du);
  3. outer screws not on the two shared x and two shared y lines; inner screws not on a named line (0.5 du tolerance);
  4. parts of the same kind with different rendered sizes anywhere (all pages, both seats);
  5. touch areas under 56 css px, or touch areas overlapping by 6 px or more (guard covers excepted);
  6. a page wider or taller than 640 x 600 du.
  Acceptance for every page: the report is empty at 1180 x 820 and 1024 x 768, pilot and CP/G.

## 9. Pages

Every page is re-laid on the kit and the frame, in this order. The notes list what the test showed on that page (all confirmed on the screenshots) and what else was seen.

| Page | Seen in the test | Extra checks |
| --- | --- | --- |
| **TAIL WHEEL / NVS** | screws; the white frame around the button is off centre (32 / 15 px left / right, 30 / 15 top / bottom) | frame becomes part of `PUSH` |
| **EMERGENCY** | the white frames of GUARD and XPNDR differ in height (about 314 vs 323) and top edge (4 px) and the labels GUARD / XPNDR sit on different baselines | all three frames from one part; labels on one baseline; ZEROIZE cover centred on its switch and under its label |
| **STORES JETT** | the JETT button and its cover are left of and below the centre of the yellow pad (x about 17, y about 11 px); the label JETT sticks out of the pad on the right; screws | pad sized from the cover; label inside the pad |
| **FIRE DET/EXTG** | does not work on the first try (section 10) | PRI and RES labels touch the housings of ENG 1 / ENG 2 above them; title close to the buttons |
| **POWER** | screws; the FRICT slider track runs into the IDLE label; | RTR BRK labels (OFF, BRK, LOCK) crowd the MSTR IGN title; lever mark labels and the FRICT labels get separate columns with at least 12 du between them |
| **EXT / INTR LT** | screws; several labels collide: SIGNAL's DIM with the knob, BRT and RST stacked, PRESS TO TEST (three lines overlapping), OFF labels against the corner screws | label presets per knob |
| **CMWS** | screws; the TEST label is cut by the tick line to the knob; the guard cover overlaps the yellow strip (about 15 px) | strip and cover from `HAZARD_PAD`; ticks on a fixed ring with labels outside |
| **ARMAMENT** (+ VIDEO, MASTER ZEROIZE) | screws | the three plates have different heights and corner insets; the right edge of the MASTER ZEROIZE plate looks cut off |
| **COMM** | screws; the VCR and ADF PULL chips sit on the bottom edge of the plate; knobs run into the corner ears; labels overlap (VOX at the ICS ring, PTT, MASTER, AUX above ATA, FM 1 chip against the SOL bracket) | the largest page: it sets the budget |
| **CENTER** and **WIPER / DEFOG** | screws | WIPER: OFF label directly under the title |
| **EUFD** | not in the test list | plate, screws and keys from the kit |
| **CP/G pages** (POWER, INTR LT, ARMAMENT, COMM, WIPER, TAIL WHEEL, EMERGENCY, STORES, FIRE, EUFD) | not in the test list (pilot seat only) | built from the same parts, so they follow automatically |

## 10. FIRE and the real covers

**Evidence** (dashboard log, 11 Oct, pilot seat, FIRE and CMWS pages):

| Control | Real DCS cover | Result |
| --- | --- | --- |
| `PLT_JETT_BTN` | none | `pressed` (confirmed) |
| `PLT_FIRE_PRIME_EXT` | none | `pressed` (confirmed) |
| `PLT_FIRE_ENG1_BTN` | `PLT_FIRE_ENG1_CVR` | `pressed, not confirmed` (twice) |
| `PLT_CMWS_JETT` | `PLT_CMWS_JETT_CVR` | `1 sent, not confirmed` |

So the tablet cover and the 1 second hold work (`guard open` is logged each time), but a command to a part that has a real cover does not take effect while DCS's own cover is closed. This answers the open point from the spec.

**Fix.** The tablet cover also moves the real one:

- A control that has a real cover gets `"cover": "{seat}_FIRE_ENG1_CVR"` in the data. The parts: ENG 1 / APU / ENG 2 FIRE (`{S}_FIRE_ENG1_CVR`, `_APU_CVR`, `_ENG2_CVR`), MASTER ZEROIZE (`{S}_INST_MZERO_CVR`), CMWS JETT (`PLT_CMWS_JETT_CVR`). PRI, RES, JETT and ZEROIZE have none in DCS-BIOS.
- `guard open` makes the bridge set the real cover to 1 and wait up to 0.5 s until the readback shows it open. If it does not open, the guard open is refused (`cover did not open`) and the cover on the tablet stays shut.
- The real cover is closed again by the bridge (not the page): after the guarded command was accepted and about 1 s later, or when the guard window runs out, even if the tablet is gone. The cover ids are read from DCS-BIOS like any other id (`read_names`), and the tablet cover follows the real cover's readback.
- The log gets `cover open` and `cover closed` lines.
- **Retest** in a throwaway mission, pilot and CP/G seat: ENG 1 FIRE, APU FIRE, ENG 2 FIRE (press arms, a second guarded press makes it safe), then PRI and RES (with a fire button armed), JETT with a station armed, MASTER ZEROIZE, CMWS JETT. Expected: `pressed` or `sent` without `not confirmed`, and the RDY lamp lights on the fire page. If ENG 1 is still `not confirmed` with the cover open, the next hypothesis is that the fire button's own value is not 1 while armed. The confirmation then uses the RDY lamp (`{S}_ENG_1_READY_L`) instead of the button.

## 11. Back button and glyphs

- The `◀ COCKPIT` label becomes an inline SVG chevron plus the word. The chevron uses `currentColor` (so it is dark on the white active tab and light on the dark tabs, matching the text), stroke 3, round caps, height 1.1 em.
- No emoji-capable code point in the UI. The arrows of the TEDAC AZ hat (`◀`, `▶`) and the up and down triangles of the rockers and TEDAC hats are drawn as SVG from one small icon set (`ICONS`: `chev-left`, `tri-up`, `tri-down`, `tri-left`, `tri-right`). The log lines keep plain text (`up`, `down`).
- Rule for the checker: no U+23E9 to U+23FA, U+25B6, U+25C0, U+2600 to U+27BF or U+1F000 and above in `web/index.html` or `aircraft/ah64d.py`.

## 12. Build steps

Each step is checked in a browser against the simulated DCS-BIOS at 1180 x 820 and 1024 x 768, both seats, and the checker (section 8) from step 3 on. I review every step myself against the screenshots.

1. **Back button and icons** (section 11). Small, no other change.
2. **Real covers** (section 10), bridge and data. Retest list in DCS.
3. **Kit and page frame**: `aircraft/panel_kit.py`, the `kit` entry in `/layout`, global scale, plate and screw system, the `place` function (section 5), `tools/check_panels.js`. Proof page: TAIL WHEEL / NVS and EMERGENCY re-laid on it.
4. **Knob look** (section 7) in the kit.
5. **Pop-up placement** (section 5) for the knob bar.
6. **Switch chooser** (section 6) replacing the touch bands.
7. **Re-lay the other pages** (section 9) in this order: STORES JETT, FIRE, ARMAMENT, EXT / INTR LT, CMWS, POWER, COMM, CENTER, WIPER / DEFOG, EUFD, then the CP/G pages. Checker report empty after each.
8. **Docs** (README, STAGE3, COCKPIT) and the test run on the tablet.

## 13. Decisions for you

1. **Corner ears (brackets).** Default: removed, so all plates look the same and the screws can be aligned. Alternative: four identical ears per plate, as a flag.
2. **Guarded switches.** Default: cover, then press and hold on the position (no chooser). Alternative: cover, then the chooser, then the hold on the chosen position.
3. **Power levers and FRICT.** Default: unchanged (tap the mark). Alternative: the chooser for the levers too.
4. **Smaller small panels.** With one scale, TAIL WHEEL, FIRE, EMERGENCY and the CP/G panels no longer fill the screen. Default: yes, accepted.
5. **Dial layout.** Default: rotary positions in the chooser sit on a small circle at their real angles. Alternative: a plain list in dial order.
6. **Photo fidelity.** Arrangement and text follow the photos; positions snap to the 10 du grid and sizes come from the kit.

## 14. Open points

- Whether the fire buttons are confirmed by their own readback once the real cover is open (section 10).
- The FRICT slider direction and the SIGNAL knob end angle were taken from the photos (still open from the first spec).
- The knob grip ring needs a look on the iPad; the ridge count may need tuning to the screen.
