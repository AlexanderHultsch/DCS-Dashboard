# Cockpit pages: fix round 1

Spec for the fixes after the first test of the COCKPIT pages on the tablet ([COCKPIT.md](COCKPIT.md) describes the pages). Status: built and tested in an isolated setup (simulated DCS-BIOS, checked in a browser, pilot and CP/G seat at 1180 x 820 and 1024 x 768, layout checker report empty). The test on the iPad and in DCS is open (section 14). Where the result differs from the plan, a "What was built" paragraph says how.

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

**What was built.** `S = min(area width / 640, area height / 600)`, capped at 1.6. 640 x 600 du is a fixed budget: POWER and COMM use all of it, the other pages are smaller. So S depends only on the screen, and every page of both seats is drawn at the same S. The app area is smaller than assumed: the header, the master lamp row and the strip above the gear leave about 627 px of height at 1180 x 820 and about 575 px at 1024 x 768. The height is the limit, so S = 1.045 at 1180 x 820 and 0.958 at 1024 x 768 (planned: 1.16 and 1.07). A part of 56 du is then 58.5 px and 53.7 px wide. The page widens a touch area to 56 px where the neighbours allow, and cuts it back where two areas would overlap (the knob buttons are the exception, see section 14).

## 3. The part kit (one place)

All parts are defined once, in `aircraft/panel_kit.py` (the AH-64D file only places parts and sets text). The kit is a small layout compiler: a page entry names a part and a centre point, never a size, and the compiler writes the resolved geometry (boxes in du, label positions, plate, ears, screws) into the page data in the format the page already draws. The page therefore draws what it is given and has no hard-coded sizes.

| Part | Size (du) | Used for |
| --- | --- | --- |
| `PUSH` square pushbutton | bezel 84 x 84, face 60 x 60 | all square pushbuttons (GUARD, XPNDR, EMERG HYD, TAIL WHEEL, A/S, GND ORIDE, APU, the 6 station buttons, FIRE / PRI / RES) |
| `PUSH` frame variant | white frame 100 x 100, 4 stroke, centred on the button by construction | GUARD, XPNDR, TAIL WHEEL, A/S, GND ORIDE, PRI, RES |
| `PUSH_SMALL` | 56 x 56 | the four EUFD keys (P, ENTER, STOPWATCH, SWAP) |
| `ROUND` pushbutton | 64 | DEFOG, IDENT, PRESS TO TEST, ACM cap |
| `PLUNGER` | 100 | JETT |
| `TOGGLE` | ring 56, lever 40, touch square 60 (a guarded one: a band of 60 per position) | all toggle switches (NAV, ANTI COL, NVS, CKT A / B, GEN RST, SQL x 5, ICS, ARM, CMWS, BYPASS, FIRE TEST, ZEROIZE, MASTER ZEROIZE, CMWS JETT, PARK BRAKE, RTR BRK, ENG START) |
| `ROTARY` | tick ring 100, knob 72 | MSTR IGN, CMWS PWR, WIPER |
| `KNOB_L` / `KNOB_M` / `KNOB_S` | 96 / 72 / 56 | L: MASTER, IHADSS, FLIR, EUFD BRT. M: FORM, SIGNAL, PRIMARY, FLOOD, STBY INST, SYM BRT, AUDIO, LAMP, SENS, ALT SET. S: the 5 radio volumes and the 5 AUX knobs |
| `MARK` | dot 10, touch square 56 beside the knob, marks 64 apart | the selector marks of the dual-function knobs (IHADSS, FLIR) |
| `ROCKER` | 52 x 120 | EUFD WCA / IDM / RTS |
| `CHIP` | 64 x 22 | PULL chips |
| `DIAL` | 112 | the CMWS threat dial (the page adds its lamps and letters) |
| `LEVER` | grip 40 x 40, slot = grip + 8 on every side, travel chosen by the page (360 to 440, even) | the power lever grips |
| `SLIDER` | slot 56 x 240, grip is a `LEVER` grip | FRICT |
| `DISPLAY` | the only part whose size the page chooses (even du); the text area is the glass less 6 on every side | EUFD 568 x 280, CMWS status 104 x 96 |
| `FLAP` | the button + 8 on each side | the plain hinged cover of the APU button (a control of its own) |
| `GUARD_COVER` | the guarded part + 12 du on each side, frame 14 wide, padlock 24 | all guarded parts; derived from the part, never typed in |
| `HAZARD_PAD` | the part (or its cover) + 20 du on each side, more where the pad holds a label | JETT pad, EMERG HYD pad, CMWS JETT pad |
| `HOUSING` and `HAZARD_STRIP` | dark housing = the part (or its cover) + 12 on each side; strip 32 wide against a housing side | the three fire buttons |
| `EAR` | rectangular corner ear 52 x 52, flush in the plate corner, 2 border | the four corners of every plate, `SCREW_L` centred in it |
| `SCREW_L` / `SCREW_M` / `SCREW_S` | diameter 26 / 18 / 12 | section 4 |
| Label styles | `TITLE` 32, `NAME` 24, `POS` 20, `SMALL` 16 | every printed text; one font, one weight per style; the page stretches each text to the width the kit estimated (19, 14, 12, 10 du per character), so the font does not change the layout |

Also in the kit: a printed bracket over a group of parts (SOL, AUX on COMM) and a printed vertical rule (EXT / INTR LT).

**What was built.** The sizes above are the ones in `aircraft/panel_kit.py`. They differ from the plan in these places:

- `ROCKER` is 52 x 120, not 52 x 100. The 56 px rule needs it: two halves of 60 du are 57 px at S = 0.958, two halves of 50 du would be 48 px.
- `SLIDER` and `LEVER` are not one part with a 40 x 200 track. The grip is 40 x 40 (`LEVER`). A lever is a slot around its grip, the page chooses its travel; the slider is a fixed slot of 56 x 240.
- `DISPLAY`, `DIAL`, `MARK`, `FLAP`, `PUSH_SMALL`, `HOUSING` and `HAZARD_STRIP` are new. The plan had no part for the EUFD glass, the CMWS threat dial, the selector marks, the APU cover, the EUFD keys or the fire button housings.
- A `TOGGLE` has one touch square of 60 du. Only a guarded one has a band per position.
- The `CHIP` text is 48 % of the chip height with no letter spacing, so `PULL IN` and `PULL OUT` both fit inside the 64 x 22 outline (a margin of 8 px at 1024 x 768 in Arial Narrow, 3.5 px in the wider Arial).

Rules:

- **A part carries its own frame, cover and legend.** A framed button is one part (button plus frame, centred by construction), a guarded part is one part (part plus cover), a hazard pad is sized from what is inside. Nothing is placed twice by hand.
- **The same part is the same size everywhere**, on every page and both seats. A page cannot change a size; at most it picks the variant.
- Parts sit on a **1 du grid** (whole-number centres), fine enough to follow the photos; plate sizes are multiples of 2 du. Screw alignment does not come from the grid but from the named lines in section 4.

## 4. Page frame and the screw system

- A page has one **plate**: width and height in du (multiples of 2), corner radius 6 (nearly rectangular as on the photos), border 3. Content keeps at least 36 du from the plate edge and at least 12 du from every ear.
- **Corner ears:** four identical rectangular `EAR` parts, one in each plate corner, flush with the plate edges. The photos show ears of different heights and some overlapping their neighbours; they are all the same here (the look should be tidy, screw alignment has priority).
- **Outer screws** (`SCREW_L`): one in the centre of each ear, so exactly 26 du from the two plate edges of its corner. All four corner screws therefore share two x values and two y values, on every page.
- **Edge screws** (`SCREW_M`, optional flag `edge_screws`): at the middle of the top and bottom edge, on the same horizontal lines as the corner screws (and optionally the left / right edge on the same vertical lines).
- **Inner screws** (`SCREW_S`, optional): a page cannot give free coordinates. An inner screw is placed by naming two **lines** from the page's line table: the plate lines (`L`, `R`, `T`, `B`, `CX`, `CY`), the corner screw lines, or the centre line of a placed part (`part.cx`, `part.cy`). So an inner screw always shares an x or y with something visible.
- **Rotation:** the three screw drawings are fixed; the slot angle comes from a short fixed list by position index (for example 15, 100, 65, 140 degrees), so a plate looks natural but never random.
- A plate with several panels (ARMAMENT + VIDEO + MASTER ZEROIZE, CENTER) has one plate per panel; the plates share a width (or sit on a common edge line) and a fixed 16 du gap.

**What was built.** As planned: the four ear screws on every plate, the line table for further screws, the slot angles (15, 100, 65, 140 degrees) by position index, one plate per panel on a shared edge line 16 du apart (`PanelGroup`). A page that collides with itself is an error at start: `Panel.build()` raises a `LayoutError` when the aircraft file is loaded. The edge and inner screws (`Panel.screw`, `edge_screws`) exist, but no page uses them: every plate has its four ear screws only.

## 5. Pop-up placement

Applies to the knob bar and to the new switch chooser (section 6).

- **Anchored to the control.** The pop-up opens at the control, not in the middle of the screen.
  - Switch chooser: centred on the switch.
  - Knob bar (420 x 120): centred on the knob horizontally, directly below it (8 px gap); if there is no room below, directly above; if neither fits, centred on the knob.
- **Never out of bounds.** After placing, the pop-up is clamped into the safe rectangle: the screen minus the tab bar and lamp row above, an 8 px margin on every side, and the gear (44 x 44 plus its 8 px offset) at the bottom right. This is one function (`place(anchorRect, popupSize)`), used by both pop-ups.
- The full-screen scrim stays (a tap outside closes without a command).
- For the knob bar the knob should stay visible where possible, so the bar sits next to it, not on it.

**What was built.** `placePopup(anchor, width, height, prefer)` in `web/index.html`, used by both pop-ups. The knob bar (420 px wide, or the screen less 24 px, 120 px high) asks for `below`: 8 px under the knob, 8 px above it if there is no room below, else centred on the knob. The chooser asks for `center`. The result is clamped into the screen: 8 px from the left, right and bottom edge and 8 px under the top of the controls area. If it still touches the gear (its 44 x 44 box plus 8 px), it moves left or up, whichever shift is smaller. A plate knob is anchored by its drawn box, an MPD or KU knob by its dial. The scrim stays: a tap outside closes a pop-up without a command.

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
- **Not changed:** guarded switches (ZEROIZE, MASTER ZEROIZE, CMWS JETT) keep cover, then a single tap on the position (no hold, no chooser; see section 10b). The power levers, the FRICT slider, the rockers, buttons and the quick pages (FLIGHT, FIGHT, MPD, KU) are unchanged (decision 3).

**What was built.**

- A switch has one touch area: a round button over the ring of a toggle or the knob of a rotary, widened to 56 px where there is room. There are no bands. The guarded switches (ZEROIZE, MASTER ZEROIZE, CMWS JETT) are the exception: they have no chooser, but one band per position under their cover (60 du each, an equal split), and a band sends its command once the cover is lifted.
- Chooser buttons are 64 px high, at least 64 px wide (as wide as the longest label) and 8 px apart.
- A vertical toggle gets a column, a horizontal one (`orient: "h"`) a row, both in the order of the positions. A rotary gets an arc: each button sits on a circle at the angle of its dial position (`angle`), radius 90 px for two positions, 110 for three, 130 for four. If two buttons would touch, the angles spread around their middle in steps of 5 % (at most five times as wide) until every pair is 8 px apart. The WIPER dial is the case that needs it.
- The current position is lit, a `disabled` one is dashed and does nothing, a `momentary` one carries a spring icon, and the title line is the control label. While a command is sent the switch itself shows an amber outline.
- A tap on a position goes through the same `run` path as every other control (confirmation, toasts) and closes the chooser. A tap on the position that is already set sends nothing. A tap outside closes it without a command.
- The power levers keep one band per mark (a tap on a mark moves the lever, the grip follows the readback). A tap on the FRICT slot opens the knob bar.

## 7. Knob look

One shared drawing per knob size, so all knobs look the same family. Layers, bottom to top:

1. a soft drop shadow;
2. a dark rim (skirt) with a radial gradient;
3. a **grip ring**: 24 raised ridges around the rim (a dashed ring in a lighter grey), the visible cue that it turns;
4. the cap: radial gradient with the highlight at the upper left, a thin bevel ring;
5. a raised pointer ridge from the centre to the rim (dark edge, light core) with a small tip at the rim. It rotates with the value as today.

`KNOB_L` gets a second, wider skirt. The rotary selectors use the same drawing in a dark colourway. The drawing is defined once (an SVG symbol reused for every knob), so it costs nothing at runtime. The printed scale marks (MIN, MAX, OFF, BRT) stay page text and move with the labels (section 8).

**What was built.** One drawing function (`knobFace` in `web/index.html`) and one set of gradient definitions (`knobDefs`) draw every knob of a panel page. There is no SVG symbol: each knob draws its own circles from the function. Two colourways: grey for the knobs, dark for the rotary selectors. A knob of 44 du radius or more (`KNOB_L`) gets the second rim. The grip ring has 24 ridges. The pointer turns by the control's `sweep`. The MPD, TEDAC and KU knobs keep their CSS drawing.

## 8. Labels and the layout checker

- Every label is attached to a part by an anchor (`above`, `below`, `left`, `right`) with a fixed gap of 8 du, in one of the four styles. A free-floating label needs an explicit reason (titles, bracket text) and is placed on the grid.
- Position labels of switches and dials (OFF, BATT, ...) come from the part's own label layout (a fixed set of presets per part), not from per-page numbers.
- **Checker.** `tools/check_panels.js` runs in the browser console. For every page of the seat it measures all label, part, screw and plate boxes and reports:
  1. a label box overlapping a part, another label, a screw or the plate edge (closer than 6 du);
  2. a part overlapping a part or the plate edge (closer than 12 du);
  3. outer screws not at the centre of their ear, or not on the two shared x and two shared y lines; a part or label closer than 12 du to an ear; inner screws not on a named line (0.5 du tolerance);
  4. parts of the same kind with different rendered sizes anywhere (all pages, both seats);
  5. touch areas under 56 css px, or touch areas overlapping by 6 px or more (guard covers excepted);
  6. a page wider or taller than 640 x 600 du.
  Acceptance for every page: the report is empty at 1180 x 820 and 1024 x 768, pilot and CP/G.

**What was built.** Labels attach to a part by an anchor and the fixed 8 du gap (`Panel.label`); a free label (`Panel.mark`) needs a reason. The label presets of the toggles, rotaries and knobs live in the kit. There are two checks:

- **At start.** `Panel.check()` tests every page in du: collisions of parts, labels, touch squares, screws and printed lines, the 36 du plate margin and the 12 du clearance to the ears.
- **In the browser.** `tools/check_panels.js` is pasted into the browser console (or run through a browser tool). It opens every page of the current seat from the long-hold page list, measures the drawn labels, parts, screws, ears and plates, and prints a JSON report with `pages`, `sizes`, `problems` and `info`. An empty `problems` is the acceptance. Run it in both seats at both sizes, with a reload after a resize. As built:
  - a part is its body, frame, cover and pad together; two parts must not overlap, and a part keeps 12 du from the plate edge and from an ear; a label keeps 6 du from the plate edge;
  - a guard cover must be exactly the part (or its frame) + 12 du;
  - every part kind, with its frame and cover, has one drawn size on all pages of the seat;
  - the corner screws sit in the centre of their ear and share two x and two y lines on every plate; plates of one page are 16 du apart on a shared edge line;
  - an inner or edge screw that shares no line with anything goes to `info`, not `problems` (no page has one);
  - a touch area under 56 px, or two touch areas overlapping by 6 px or more in both directions, is a problem. Guard covers, the APU flap and an element inside another are not compared;
  - the PULL chip is exempt from the 56 px floor. It hangs 8 du under its knob and is small by design; the page gives it a 32 px floor (`CHIP_TOUCH_MIN`), and the long press on its knob is the large target;
  - a page larger than 640 x 600 du is a problem.
  - Result: `problems` and `info` empty, 11 pilot pages and 10 CP/G pages, at 1180 x 820 and 1024 x 768.

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

**What was built.** All 21 pages (11 pilot, 10 CP/G) are laid out on the kit; there are no photo coordinates left. Sizes as built, in du:

| Page | Size | Plates |
| --- | --- | --- |
| TAIL WHEEL / NVS | 600 x 224 | 1 |
| EMERGENCY | 580 x 276 | 1 |
| STORES JETT | 556 x 408 | 1 |
| FIRE DET/EXTG | 600 x 456 | 1 |
| POWER | 640 x 600 (pilot), 312 x 576 (CP/G, the two levers) | 1 |
| EXT / INTR LT | 612 x 456 (pilot), INTR LT 428 x 360 (CP/G) | 1 |
| CMWS | 616 x 552 | 2: indicator 616 x 288, control panel 616 x 248 |
| ARMAMENT | 608 x 600 (pilot), 608 x 244 (CP/G) | 3 (ARMAMENT 352 x 244, MASTER ZEROIZE 240 x 244, VIDEO 608 x 340) or 2 |
| EUFD | 640 x 524 | 1 |
| CENTER | 640 x 530 | 3: CHK OVSP TEST and GEN RST 640 x 210, WINDSHIELD WIPER 376 x 304, PARK BRAKE and ALT SET 248 x 304 |
| COMM | 640 x 600 | 1 |
| WIPER / DEFOG (CP/G) | 376 x 304 | 1 |

Where the arrangement does not follow the photo, decisions 7 to 11 in section 13 give the reason.

## 10. FIRE and the real covers

**Evidence** (dashboard log, 11 Oct, pilot seat, FIRE and CMWS pages):

| Control | Real DCS cover | Result |
| --- | --- | --- |
| `PLT_JETT_BTN` | none | `pressed` (confirmed) |
| `PLT_FIRE_PRIME_EXT` | none | `pressed` (confirmed) |
| `PLT_FIRE_ENG1_BTN` | `PLT_FIRE_ENG1_CVR` | `pressed, not confirmed` (twice) |
| `PLT_CMWS_JETT` | `PLT_CMWS_JETT_CVR` | `1 sent, not confirmed` |

So the tablet cover works (`guard open` is logged each time), but a command to a part that has a real cover does not take effect while DCS's own cover is closed. This answers the open point from the spec.

**Fix.** The tablet cover also moves the real one:

- A control that has a real cover gets `"cover": "{seat}_FIRE_ENG1_CVR"` in the data. The parts: ENG 1 / APU / ENG 2 FIRE (`{S}_FIRE_ENG1_CVR`, `_APU_CVR`, `_ENG2_CVR`), MASTER ZEROIZE (`{S}_INST_MZERO_CVR`), CMWS JETT (`PLT_CMWS_JETT_CVR`). PRI, RES, JETT and ZEROIZE have none in DCS-BIOS.
- `guard open` makes the bridge set the real cover to 1 and wait up to 0.5 s until the readback shows it open. If it does not open, the guard open is refused (`cover did not open`) and the cover on the tablet stays shut.
- The real cover is closed again by the bridge (not the page): after the guarded command was accepted and about 1 s later, or when the guard window runs out, even if the tablet is gone. The cover ids are read from DCS-BIOS like any other id (`read_names`), and the tablet cover follows the real cover's readback.
- The log gets `cover open` and `cover closed` lines.
- **Retest** in a throwaway mission, pilot and CP/G seat: ENG 1 FIRE, APU FIRE, ENG 2 FIRE (press arms, a second guarded press makes it safe), then PRI and RES (with a fire button armed), JETT with a station armed, MASTER ZEROIZE, CMWS JETT. Expected: `pressed` or `sent` without `not confirmed`, and the RDY lamp lights on the fire page. If ENG 1 is still `not confirmed` with the cover open, the next hypothesis is that the fire button's own value is not 1 while armed. The confirmation then uses the RDY lamp (`{S}_ENG_1_READY_L`) instead of the button.

**Done.** The data, the bridge and the page work as described, with one difference: the tablet cover does not follow the readback of the real cover. It opens when the bridge answers `guard open` and closes after 5 s or after the tap. The cover ids are read from DCS-BIOS (`read_names`), so the bridge sees the real cover. In the isolated setup (simulated DCS-BIOS) the log shows `cover open`, `guard open`, `pressed` and about 1 s later `cover closed` for ENG 1 FIRE. The retest in DCS is open (section 14).

### 10b. Guard without the hold

A guarded control already needs a deliberate first step: the cover has to be opened by hand. So the second step is a plain tap.

- The 1 second hold and its ring are removed (`HOLD_MS`, the ring drawing in `addGuard`). With the cover open, one tap on the button, or on the position of a guarded switch (ZEROIZE, MASTER ZEROIZE, CMWS JETT), sends the command.
- Everything else stays: the cover tap sends `guard open`, the cover closes after 5 seconds or after the tap, only one cover is open at a time, the bridge accepts a guarded command only inside its window and uses the window up. The long press of the COMM knobs (PULL) is a different feature and stays.
- The docs that describe the hold (README, COCKPIT.md, STAGE3.md) are corrected in step 8.

**Done.** `HOLD_MS` and the ring around a guarded button are gone from the page. The ring that remains belongs to the long press (0.6 s) of the COMM volume knobs, which toggles the PULL chip. A guarded switch has one band per position under its cover; the other switches use the chooser (section 6).

## 11. Back button and glyphs

- The `◀ COCKPIT` label becomes an inline SVG chevron plus the word. The chevron uses `currentColor` (so it is dark on the white active tab and light on the dark tabs, matching the text), stroke 3, round caps, height 1.1 em.
- No emoji-capable code point in the UI. The arrows of the TEDAC AZ hat (`◀`, `▶`) and the up and down triangles of the rockers and TEDAC hats are drawn as SVG from one small icon set (`ICONS`: `chev-left`, `tri-up`, `tri-down`, `tri-left`, `tri-right`). The log lines keep plain text (`up`, `down`).
- Rule for the checker: no U+23E9 to U+23FA, U+25B6, U+25C0, U+2600 to U+27BF or U+1F000 and above in `web/index.html` or `aircraft/ah64d.py`.

**Done.** On a panel page the COCKPIT tab keeps its highlight and shows the chevron icon before the word. The icon set (`ICONS` in `web/index.html`) has `chev-left`, `close` (the knob bar), `tri-up`, `tri-down`, `tri-left`, `tri-right` (the rocker and TEDAC hats) and `spring` (the spring-return mark in the chooser). The rule was checked by a scan of those two files, the bridge, the kit and the checker: no code point of the banned ranges. The scan is not part of the repo.

## 12. Build steps

Each step is checked in a browser against the simulated DCS-BIOS at 1180 x 820 and 1024 x 768, both seats, and the checker (section 8) from step 3 on. I review every step myself against the screenshots.

1. **Back button and icons** (section 11). Small, no other change.
2. **Real covers and guard without hold** (sections 10 and 10b), bridge, data and page. Retest list in DCS.
3. **Kit and page frame**: `aircraft/panel_kit.py` (the layout compiler, parts, plate, ears, screws), global scale in the page, the `place` function (section 5), `tools/check_panels.js`. Proof pages: TAIL WHEEL / NVS and EMERGENCY re-laid on it.
4. **Knob look** (section 7) in the kit.
5. **Pop-up placement** (section 5) for the knob bar.
6. **Switch chooser** (section 6) replacing the touch bands.
7. **Re-lay the other pages** (section 9) in this order: STORES JETT, FIRE, ARMAMENT, EXT / INTR LT, CMWS, POWER, COMM, CENTER, WIPER / DEFOG, EUFD, then the CP/G pages. Checker report empty after each.
8. **Docs** (README, STAGE3, COCKPIT) and the test run on the tablet.

All steps are done and checked this way. Step 8: the docs are done, the test run on the tablet and in DCS is open (section 14). A last cleanup removed the page code that no page uses any more: the branches for pages without the kit, and the knob panel of the removed Startup tab.

## 13. Decisions

1. **Corner ears.** Resolved: kept, rectangular, four identical ears per plate with the screw in the centre. The photos mostly show rectangular corner areas; where they overlap or differ in height they are made equal. Screw alignment has priority.
2. **Guarded controls.** Resolved: cover, then a single tap, no hold, no chooser (section 10b).
3. **Power levers and FRICT.** Default stands: unchanged (tap the mark).
4. **Smaller small panels.** Default stands: with one scale the small panels no longer fill the screen.
5. **Dial layout.** Default stands: rotary positions in the chooser sit on a small circle at their real angles.
6. **Photo fidelity.** Resolved: arrangement and text follow the photos; positions sit on a 1 du grid, fine enough that every dial looks like its photo; sizes come from the kit. Decisions 7 to 11 are the places where the arrangement does not follow the photo.
7. **EUFD arrangement.** Resolved: the display is on top and the controls sit in a row below it (the three rockers, the BRT knob, the four keys), not around the glass as on the photo. The text size matters more than the photo layout: the glass is 568 x 280 du, nearly the full page width, so the 14 lines of 56 characters stay readable.
8. **CENTER.** Resolved: one wide plate (CHK OVSP TEST and GEN RST) over two plates (WINDSHIELD WIPER, and PARK BRAKE with ALT SET), 16 du apart on shared edge lines.
9. **COMM.** Resolved: the ICS name and its PTT label sit in the SOL row, between the FM 1 and FM 2 squelch switches. The switch itself, with VOX and HOT MIC, is below the row.
10. **Wiper labels.** Resolved: PARK, OFF, LO and HI are flat text in a fan above the dial, not turned along the dial as on the photo.
11. **PARK BRAKE name.** Resolved: printed on two lines (PARK, BRAKE). On one line it runs into the plate margin and the corner ear.
12. **PULL chip.** Resolved: exempt from the 56 px touch floor of the checker. Its floor is 32 px, and the long press on its knob is the large target.

## 14. Open points

What is built and checked in the isolated setup still needs the iPad and DCS:

- Whether the fire buttons are confirmed by their own readback once the real cover is open (section 10).
- The real covers in DCS: the bridge opens DCS's own cover for ENG 1, APU and ENG 2 FIRE, MASTER ZEROIZE and CMWS JETT (waits up to 0.5 s for the readback, closes it about 1 s after the command). Only the simulated DCS-BIOS has seen it.
- The FRICT slider direction and the SIGNAL knob end angle were taken from the photos (still open from the first spec).
- The knob grip look on the iPad. The ridge count (24) and the second rim of the large knobs may need tuning.
- The deviations from the photo arrangement (decisions 7 to 11): look at them on the iPad and say which ones to change.
- The PULL chip text. It fits in Arial Narrow and in the wider Arial; the iPad may draw it in Helvetica Neue, so check that `PULL OUT` fits and reads.
- The chooser on the iPad: the button size, the arc of the dials, the placement of the pop-ups near the screen edges.
