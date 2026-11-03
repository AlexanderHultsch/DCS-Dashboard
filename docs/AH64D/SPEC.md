# DCS-Dashboard – AH-64D

Specification of the AH-64D Apache (Block II) dashboard as built. It is the mature aircraft of the dashboard and was tested in DCS, in both seats; what is still open for a DCS test or a look on the iPad is listed in [../FIXES.md](../FIXES.md). The engine all aircraft share is in [../SPEC.md](../SPEC.md); the engine changes this aircraft needs and their decisions are in [ENGINE.md](ENGINE.md). Controls are named as in [PANELS.md](PANELS.md), DCS-BIOS identifiers are in [BIOS.md](BIOS.md), reference pictures in [PICTURES.md](PICTURES.md), the cold start in [STARTUP.md](STARTUP.md), the decisions and the method in [RESEARCH.md](RESEARCH.md). The structure follows the A-10C and F-16C specs, [../A10C/SPEC.md](../A10C/SPEC.md) and [../F16C/SPEC.md](../F16C/SPEC.md); the AH-64D has two more tabs than they have (KU and GEORGE), so it has thirteen sections.

Choices made while writing the spec and during the build are written at the end of the section where they are made: a `Decided:` line where the planner took the recommendation (or another choice, which the line says) and the owner reviews it at the end, a `Question:` line where it is still open. All are collected in [RESEARCH.md](RESEARCH.md), Questions.

## 1. Overview

A tablet dashboard for the two-seat AH-64D Apache, with the tabs **COCKPIT | FLIGHT | FIGHT | MPD | KU | GEORGE**. The same bridge serves all aircraft; it chooses the AH-64D files when DCS-BIOS reports the aircraft `AH-64D_BLK_II` (`_ACFT_NAME`, the `DCS_NAMES` of `aircraft/ah64d.py`; [../SPEC.md](../SPEC.md) section 9).

| Tab | Content | A-10C / F-16C counterpart |
| --- | --- | --- |
| COCKPIT | Map of the cockpit, one per seat; 21 panel pages (11 pilot, 10 CP/G, 13 page names), the CANOPY key and 3 link boxes (pilot) or 4 (CP/G) (section 2) | COCKPIT |
| FLIGHT | Trim display (read only), controls overlay key, symbology hat, monocle key, TAIL WHEEL (pilot) and the two power levers (section 3) | FLIGHT |
| FIGHT | One page per seat: the pilot page with master arm, ground override, the WAS and sight select hats, flare and chaff with their counts and the CMWS controls; the gunner page with the grip controls (TADS FOV, sensor, IAT, OFS) (section 4) | FIGHT |
| MPD | LEFT MPD, RIGHT MPD and (CP/G) TEDAC, one at a time, drawn 1:1 after a photo, with the cursor pad and the TKR pad (section 5) | MFCD / MFD |
| KU | The keyboard unit with its live scratchpad, drawn 1:1 after a photo (section 6) | CDU / DED |
| GEORGE | Direct buttons for George, the AI crew member, which can only be controlled by keypress (section 7) | none (AH-64D only) |

Differences to the A-10C and the F-16C: two seats (PILOT and CP/G, a seat badge, a debug seat and pages that exist in one seat only), the power levers are moved by keypress and read back from DCS-BIOS, a trim display, the KU and GEORGE tabs, an MPD tab drawn after a photo, a panel look of its own (section 11), and no scroll page: every panel page fits the 640 × 600 du budget. The engine changes the other two aircraft needed are in [../A10C/ENGINE.md](../A10C/ENGINE.md) and [../F16C/ENGINE.md](../F16C/ENGINE.md).

**Built:** the aircraft file `aircraft/ah64d.py` with 21 panel pages, the FLIGHT, FIGHT (two pages), MPD (with TEDAC and TKR), KU and GEORGE tabs, and all keypress controls (power levers, canopy, monocle, controls overlay, trim reset, George; section 9). **Not on the dashboard:** section 12.

### Seats

Two seats, PILOT and CP/G. The generic seat handling is in [../SPEC.md](../SPEC.md) section 5; what the AH-64D does with it:

- Each view lists the seats it can be used in: FLIGHT, MPD, KU, GEORGE and the COCKPIT map both seats; a panel page lists the one seat it exists for. FIGHT exists once per seat, two views with the same name, one with `"seats": [0]` and one with `"seats": [1]`. A control can also have its own `seats` (TAIL WHEEL on FLIGHT: pilot only) and is greyed in the other seat.
- The tab bar has one tab per view name. A tab opens the view of that name whose `seats` contain the current seat (real or debug); FIGHT opens the pilot page or the gunner page. The remembered tab is the name, stored on the tablet for the AH-64D only.
- The seats are declared in `aircraft/ah64d.py` (`SEATS`: prefix `PLT` and `CPG`, labels `PILOT` and `CP/G`; `SEAT_OUTPUT` is `SEAT_POSITION`). The header badge shows the current seat: `PILOT` or `CP/G`. It adds ` – READ ONLY` when the shown view cannot be used in this seat: lamps and positions are shown, all controls are disabled.
- When the seat changes, the view of the same name for the new seat opens (POWER stays POWER, FIGHT shows the page of the new seat); if the new seat has no panel page of that name (CMWS, CENTER, EXT / INTR LT) the COCKPIT map of the new seat opens.
- **Debug seat.** A long hold (0.6 s) on the seat badge looks at the pages of the other seat without sitting in it. With a real seat the hold cycles: none, the other seat, none. With no DCS data or with the bridge offline there is no real seat, and the cycle is: none, `CP/G`, `PILOT`, none. A plain tap on the badge does nothing.
  - The debug seat is view only. The page resolves `{seat}` ids and the seat-specific pages with the debug seat, so the lamps, the positions and the pages are those of that seat (`/state` carries the values of both seats). Every control stays disabled, so no command can leave the page; the bridge never sees the debug seat.
  - The badge reads `DEBUG PILOT` or `DEBUG CP/G` in the amber read-only style, in place of the normal text. Without DCS data the pages show their empty state.
  - The tab bar and the pages follow the debug seat as they follow a real seat. It is held in the page only and is not remembered: a reload clears it.
- The header shows `NO DCS DATA` when no DCS-BIOS packet arrived for 3 s, and `BRIDGE OFFLINE` when the page cannot reach the bridge.
- The bridge refuses commands of a view outside its seats.

Question: Does the long hold on the seat badge work with a finger on the tablet?

## 2. COCKPIT

COCKPIT is a simplified map of the AH-64D cockpit and one page for every cockpit panel, with every button, switch, knob and display of that panel, as in the real AH-64D. The quick pages FLIGHT and FIGHT keep their mixed layout; a control can sit on a panel page and on a quick page at the same time, and both show the same DCS state. Tap a box on the map to open its page; on a page the COCKPIT tab keeps its highlight and shows a back chevron, and one tap on it goes back to the map; a long hold (0.5 s) on COCKPIT opens a list of every page of the current seat. The boxes KU, MPD L, MPD R and TEDAC (CP/G only) are not pages: they open the KU and MPD tabs (MPD L, MPD R or TEDAC preselected), as the A-10C map boxes open MFCD and CDU. The AH-64D has two seats, so the map and the list follow the seat badge, and a page that does not exist in the current seat is not shown (map and list), it is not greyed out.

Tabs at the top: **COCKPIT | FLIGHT | FIGHT | MPD | KU | GEORGE**. Ids written as `{seat}_...` stand for `PLT_...` (pilot) or `CPG_...` (CP/G); in this section `{S}` is the same.

The panel pages have the AH-64D look (section 11); this section says which panels are on which page and where. The lamp row (section 8) stays at the top of the map and of every panel page. The grips are controls for FLIGHT and FIGHT, not panel pages. **Not on a page:** the CP/G processor select panel (not implemented in DCS), the SAI (cage and pitch trim do not work; only the altimeter setting knob is used, on CENTER), canopy jettison, M4 rifle, sun visors, stick fold, radio frequencies; the full list is section 12.

**Navigation**

- **Tap COCKPIT:** the cockpit map of the current seat. Each box is a panel; tap a box to open its page.
- **On a panel page** the COCKPIT tab keeps its highlight and shows a back chevron before the word. One tap goes back to the map.
- **Long hold (0.5 s) on COCKPIT:** a list of every page of the current seat, for jumping from page to page.
- The map boxes for the two MPDs, the TEDAC (CP/G only) and the KU open the MPD and KU tabs (MPD L, MPD R or TEDAC preselected).
- A page that does not exist in the current seat is not shown (map and list), it is not greyed out. When the seat changes while a panel page is open, see [Seats](#seats).
- The master lamps (MASTER WARNING, MASTER CAUTION) stay in the top row of the map and of every panel page. `CANOPY` is a small key button on the map (pilot seat).

**Lamp row.** The lamp row is described in [section 8](#8-lamp-row).

**The map** is a 12 × 7 grid, `[row, col, rows, cols]`, of plain boxes with the panel placard, in the order of the real cockpit. The sketches shorten some names; the table has the full ones.

Pilot:

```
 1  KU            | FIRE DET/EXTG       EUFD                    | CMWS
 2  TAIL WHL/NVS  | ARMAMENT            [CANOPY]                |
 3  EMERGENCY     | ┌─────────────┐ ┌─────────────┐             | COMM
 4  POWER         | │    MPD L    │ │    MPD R    │             |
 5  (levers)      | └─────────────┘ └─────────────┘             |
 6  STORES JETT   |       CENTER (OVSP/GEN RST, WIPER, PARK BRAKE, ALT SET)
 7  EXT/INTR LT   |
    left console    instrument panel                              right console
```

CP/G:

```
 1  KU            | FIRE DET/EXTG  ARMAMENT          EUFD         |
 2  EMERGENCY     | ┌───────────┐ ┌──────────┐ ┌───────────┐     | COMM
 3  POWER         | │   MPD L   │ │  TEDAC   │ │   MPD R   │     |
 4  (levers)      | └───────────┘ └──────────┘ └───────────┘     | WIPER / DEFOG
 5  TAIL WHL/NVS  |                                              |
 6  INTR LT       |                                              |
 7  STORES JETT   |                                              |
    left console    instrument panel                               right console
```

| Page | Grid (pilot) | Grid (CP/G) | Panels on the page |
| --- | --- | --- | --- |
| KU (link) | [1,1,1,3] | [1,1,1,3] | opens the KU tab |
| TAIL WHEEL / NVS | [2,1,1,3] | [5,1,1,3] | Tail Wheel / NVS Mode Panel (p. 115) |
| EMERGENCY | [3,1,1,3] | [2,1,1,3] | Emergency Panel (p. 116) |
| POWER | [4,1,2,3] | [3,1,2,3] | Power Quadrant Panel (p. 117); CP/G: the two power levers only |
| STORES JETT | [6,1,1,3] | [7,1,1,3] | Stores Jettison Panel (p. 119) |
| EXT / INTR LT | [7,1,1,3] | none | Exterior Lighting / Interior Lighting Panel (p. 119) |
| INTR LT | none | [6,1,1,3] | Interior Lighting Panel (p. 126) |
| FIRE DET/EXTG | [1,4,1,3] | [1,4,1,2] | Fire Detection / Extinguishing Panel (FIRE DET/EXTG) (p. 106) |
| ARMAMENT | [2,4,1,3] | [1,6,1,2] | Armament Panel (p. 108), Master Zeroize Switch (p. 109), Video Panel (p. 109); CP/G: no Video Panel |
| EUFD | [1,7,1,3] | [1,8,1,3] | Enhanced Up-Front Display (EUFD) (p. 155) |
| CANOPY (key) | [2,7,1,3] | none | the key button `canopy` (not a page) |
| MPD L (link) | [3,4,3,3] | [2,4,3,2] | opens the MPD tab, left display |
| TEDAC (link) | none | [2,6,3,2] | opens the MPD tab, TEDAC |
| MPD R (link) | [3,7,3,3] | [2,8,3,3] | opens the MPD tab, right display |
| CENTER | [6,5,2,4] | none | Check Overspeed Test / Generator Reset Panel (p. 111), Windshield Wiper Control Panel (p. 112), Parking Brake Handle (p. 112), Standby Altimeter (p. 111) (the setting knob only) |
| CMWS | [1,10,2,3] | none | CMWS Control Panel (p. 630) |
| COMM | [3,10,3,3] | [2,11,2,2] | Communications Panel (p. 121) |
| WIPER / DEFOG | none | [4,11,1,2] | Windshield Wiper Control Panel (p. 112) |

The pilot map has 15 boxes: 3 link boxes, the CANOPY key and 11 panel pages. The CP/G map has 14 boxes: 4 link boxes and 10 panel pages. Together 21 panel pages with 13 names (INTR LT and WIPER / DEFOG exist for the CP/G only, EXT / INTR LT, CMWS and CENTER for the pilot only). The CP/G has no CMWS, no EXT LT, no VIDEO, no CHECK OVERSPEED / GENERATOR RESET panel, no PARK BRAKE, no master ignition, no APU, no engine start, no rotor brake. The CP/G wiper and defog are on the right console, on their own page WIPER / DEFOG below COMM; the pilot's are on the CENTER page.

**Naming convention**

- **Page name** = the placard of the panel in upper case (`FIRE DET/EXTG`, `STORES JETT`, `TAIL WHEEL / NVS`).
- **Control label** = the text printed on the panel. A rocker shows its name between two arrows (`WCA`), a knob its name (`FLOOD`).
- **Positions** are listed in the order printed on the panel, top to bottom or left to right, with all real positions, also unusable ones (greyed out).
- **Control id** = the DCS-BIOS identifier with the seat as `{S}`. A function without a DCS-BIOS entry (keypress) uses a lower-case name from `[keys]` (`canopy`, `power_left`).
- All text in English, as in the cockpit.

**Rules for the pages**

- **Plates.** A page is one plate per physical panel inside the 640 × 600 du budget of the panel kit (touch minimum 56 px, see [../SPEC.md](../SPEC.md) section 7, which also has the parts, the plate with its four corner ears, the labels and the one scale for all pages). Several panels on one page are separate plates, 16 du apart on shared edge lines (ARMAMENT, CMWS, CENTER). Lamps and displays are drawn on the plate.
- **Fit.** The yardstick is the COMM page: 26 touch targets (12 knobs, 7 PULL chips, 5 squelch switches, ICS and IDENT) fill the whole budget, and so does POWER (pilot). Every page below has a `Fit` line with its size in du as built. All 21 pages fit 640 × 600 du, so the AH-64D has no scroll page.
- **Every control of a panel is on its page**, including the ones that can do harm (they are guarded, see below) and the ones the manual calls N/I or "no function" when DCS-BIOS has them: GUARD, XPNDR, ZEROIZE and EMERG HYD on EMERGENCY, FRICT on POWER, the L TIP and R TIP buttons on STORES JETT, ACM on ARMAMENT, the AUDIO knob on CMWS, DEFOG and the CKT A / B positions on CENTER, IDENT, IFF, ATA and VCR on COMM. A control without a DCS-BIOS identifier (the canopy jettison handle) is not on a page (section 12). A position that cannot be used is greyed out (BRK, EXT PWR, LOCKOUT).
- **Switches.** A tap on a switch (a toggle or a dial) opens a chooser at the switch: one big button per position (at least 64 px, 8 px apart), arranged like the switch (a column, a row for `orient: "h"`, an arc for a dial: each button on a circle at the angle of its dial position, radius 90 px for two positions, 110 for three, 130 for four, spread in steps of 5 % until every pair is 8 px apart). The current position is lit, a `disabled` position is dashed and does nothing, a `momentary` (spring-return) position carries a spring mark, and a title line shows the control label. A tap on a position sends the command and closes the chooser; a tap on the position already set sends nothing; a tap outside closes the chooser without a command. While a command is sent the switch shows an amber outline. The power levers, the FRICT slider, rockers, buttons and guarded switches have no chooser.
- **Knobs.** A tap on a knob opens the knob bar next to it ([Knob bar](#knob-bar)). On COMM, holding a volume knob for 0.6 s pulls it out or pushes it in (a ring fills during the hold).
- **Pop-ups** (chooser and knob bar) open at the control, not in the middle of the screen: the bar below its knob (8 px gap; above it if there is no room; else centred on the knob), the chooser centred on the switch. Both are clamped into the screen: 8 px from the edges, below the tab bar, and clear of the gear (its 44 × 44 box plus 8 px, moved left or up, whichever shift is smaller). The scrim stays: a tap outside closes a pop-up without a command. The function is `placePopup(anchor, width, height, prefer)` in `core/web/index.html`.
- **Spring-loaded switches.** A spring-loaded switch has a `rest` value (set, held, back to rest): the ENG START switches, the FIRE TEST switch, the CMWS PWR knob (TEST), the CKT A / B and GEN RST switches and the five squelch switches are held 0.5 s; a push button is pressed for 0.3 s and released. `rest` is the resting value of the position list below (`rest 1`).
- **Guarded controls.** A guarded control can end the flight or cannot be undone in the mission: shut off an engine or the APU (the FIRE buttons stop the fuel flow), discharge an extinguisher bottle, drop stores (JETT), wipe the radio and crypto data (zeroize), jettison the countermeasure flares. All are on the tablet, only on their own panel page (never on FLIGHT or FIGHT), and need two deliberate steps:
  1. **Lift the cover.** The control is covered by a red and white hazard-striped frame with a padlock. The middle of the frame is clear, so the lamps and the control underneath stay visible. Tap the cover to lift it. It closes again after 5 seconds, or after the press. Only one cover can be open at a time.
  2. **Tap the control.** One tap on the button, or on the position of a guarded switch, sends the command and the cover closes. A guarded switch is the one switch without a chooser: under the cover each position is a touch band of its own (60 du, equal split).

  The kit draws the cover from the part: the part (or its white frame) and 12 du on every side, a hazard frame 14 du wide, a padlock of 24 du (`cover_at`, never typed in). The bridge enforces the rule, so a second tab, a bug in the page or a stale tab cannot bypass it:
  - Opening a cover sends `{"id": ..., "guard": "open"}`. The bridge opens a 5 second window for that id only.
  - A command for a guarded id is accepted only inside its window, and the window is used up by the press. Otherwise the answer is `refused: guard closed`.
  - The press itself is a confirmed press: the bridge holds until DCS-BIOS shows the button.
  - Log lines: `guard open`, `pressed`, `refused: guard closed`, and for the parts with a real cover `cover open`, `cover closed` and `refused: cover did not open`.

  **Real DCS covers.** Where the real cockpit has a cover (FIRE ENG 1, APU and ENG 2, master zeroize, CMWS flare jettison), DCS-BIOS has a cover control (`{S}_FIRE_ENG1_CVR`, `_APU_CVR`, `_ENG2_CVR`, `{S}_INST_MZERO_CVR`, `PLT_CMWS_JETT_CVR`), and DCS does not react to the button while its own cover is closed. These controls carry a `cover` property with that id, and the bridge opens and closes DCS's own cover for them. Lifting the tablet cover sets the real cover to 1 and waits up to 0.5 s for the DCS-BIOS readback; if it does not open, the answer is `refused: cover did not open` and the tablet cover stays shut. The bridge closes the real cover again about 1 second after the command was accepted, when the 5 second window runs out unused, or at once when another guarded control is lifted. PRI, RES, JETT and ZEROIZE have no cover in DCS-BIOS and only use the tablet cover.

  Controls with `guard`: `{S}_FIRE_ENG1_BTN`, `{S}_FIRE_APU_BTN`, `{S}_FIRE_ENG2_BTN`, `{S}_FIRE_PRIME_EXT`, `{S}_FIRE_RES_EXT`, `{S}_JETT_BTN`, `{S}_EMERG_ZERO_SW`, `{S}_INST_MZERO_SW`, `PLT_CMWS_JETT`. The six station select buttons only arm a station and light up; they are normal buttons, and JETT is guarded. The guarded switches ZEROIZE, MASTER ZEROIZE and CMWS JETT list ON on top and OFF at the bottom.
- **Power levers.** Used on the FLIGHT view and on the POWER page.
  - One vertical slider per lever, positions bottom to top: OFF, IDLE, FLY, LOCKOUT. The slider snaps to positions only. LOCKOUT is shown above FLY but greyed and cannot be reached.
  - Readback to position: the nearest of OFF 0, IDLE 16383, FLY 58981, LOCKOUT 65535.
  - Moving the slider sends the keys for that lever, one step at a time, waiting up to 1 s for the readback after each step: OFF → IDLE `power_<side>_idle`; IDLE → FLY `power_<side>_up`; FLY → IDLE `power_<side>_down`; IDLE → OFF `power_<side>_off`. OFF → FLY and FLY → OFF go through IDLE. `<side>` is `left` for PWR LVR 1 (engine 1) and `right` for PWR LVR 2 (engine 2).
  - On the panel pages a tap on a mark moves the lever (one touch band per mark); the grip follows the readback. A tap on the FRICT slot opens the knob bar.
- **Cold start.** STARTUP.md (pilot) uses every pilot page except EMERGENCY and STORES JETT; the standby altimeter setting is the ALT SET knob of CENTER.

Decided: one scale for all pages, so the small panels (FIRE DET/EXTG, TAIL WHEEL / NVS) no longer fill the screen; four identical rectangular corner ears per plate with the screw in the centre, where the photos show ears of different heights, some overlapping their neighbours (screw alignment has priority) (owner review).

Decided: the rotary positions of the chooser sit on a small circle at their real dial angles (owner review).

Decided: a guarded control needs the cover, then a single tap, with no hold and no chooser; the first fix round had a 1 s hold with a ring, which was removed because lifting the cover is already a deliberate step (owner review).

Decided: the arrangement and the text of the pages follow the photos; the places where they deliberately do not are the EUFD, CENTER, the ICS / PTT labels on COMM, the wiper labels and the PARK BRAKE name (decisions in the page blocks); look at them on the iPad and say which ones to change (owner review).

Question: How do the chooser (button size, the arc of the dials, placement near the screen edges) and the knob grip look (the ridge count of 24, the second rim of the large knobs) feel on the iPad? ([../FIXES.md](../FIXES.md))

### Panel pages

Counts: `rows` = rows of the PANELS.md tables of the panels on the page; `id` = rows with a DCS-BIOS identifier; `read only` = lamps, gauges and text (no command); `left off` = rows that are not on the page (section 12). `Plus` = controls that exist only in DCS-BIOS and clearly belong to the page (here the real covers). Pictures: the AH-64D pages were drawn from the owner's cockpit photos, which are not in the repository, and from the manual figure on the page named in the `Picture` line. A page lists its panels in the order of the cockpit. A page that exists in both seats under one name is one block; the numbers are those of the pilot page, and `CP/G:` says where the CP/G page differs. Position lists read `value label`; `rest` is the resting value of a spring-loaded switch, `momentary` marks a position that springs back, a greyed out position cannot be used. The drawing of the parts and the way the sizes are made are in [../SPEC.md](../SPEC.md) section 7.

#### TAIL WHEEL / NVS

- **Panels:** Tail Wheel / NVS Mode Panel (p. 115).
- **Arrangement:** one plate, the same in both seats (left console). On the page: the TAIL WHEEL push button in a white frame at the left with its UNLOCK lamp, the NVS MODE switch at the right.
- **Controls:** 3 rows, 3 id, 1 read only, 0 left off. On the page: 2 controls and 1 lamp (UNLOCK, amber).
- **Special:** TAIL WHEEL `{S}_T_WHEEL_UNLOCK_BTN` is a push button (press toggles the commanded state, locked or unlocked) with the lamp `{S}_T_WHEEL_UNLOCK_L` UNLOCK, which is lit whenever the wheel is actually unlocked. NVS MODE `{S}_NVS_MODE`: 2 FIXED (needs the NVS on, otherwise DCS does not take it), 1 NORM, 0 OFF. The default NVS sensor is the PNVS in the pilot seat and the TADS in the CP/G seat. TAIL WHEEL is also on FLIGHT (pilot only).
- **Picture:** owner photo (not in the repo), manual figure p. 115.
- **Fit:** fits, 600 × 224 du as built: one plate.

#### EMERGENCY

- **Panels:** Emergency Panel (p. 116).
- **Arrangement:** one plate, the same in both seats (left console), title EMERGENCY. On the page: the GUARD and XPNDR buttons, each in a white frame with its lamp, the guarded ZEROIZE switch, and the EMERG HYD button on a hazard pad.
- **Controls:** 7 rows, 7 id, 3 read only, 0 left off. On the page: 4 controls and 3 lamps (ON, green).
- **Special:** GUARD `{S}_EMERG_GUARD_BTN`, XPNDR `{S}_EMERG_XPNDR_BTN` and EMERG HYD `{S}_EMERG_HYD_BTN` are push buttons with the lamps `{S}_EMERG_GUARD_L`, `{S}_EMERG_XPNDR_L` and `{S}_EMERG_HYD_L`. ZEROIZE `{S}_EMERG_ZERO_SW` is a guarded switch (ON 1 on top, OFF 0 below) with the tablet cover only; DCS-BIOS has no cover for it. The manual calls all four controls N/I; DCS-BIOS has them, and the three buttons passed the sweep in DCS. ZEROIZE has not been sent in DCS yet.
- **Picture:** owner photo (not in the repo), manual figure p. 116.
- **Fit:** fits, 580 × 276 du as built: one plate.

#### POWER

- **Panels:** Power Quadrant Panel (p. 117).
- **Arrangement:** one plate (left console). Pilot: at the left the RTR BRK toggle, the MSTR IGN dial, the APU button under its flap cover and the two ENG START toggles (NO 1 and NO 2, the positions START, OFF and IGN ORIDE printed once between them); in the middle the two power levers (POWER, marks OFF, IDLE, FLY, LOCK OUT); at the right the FRICT slider. CP/G: a narrow plate with the two power levers only.
- **Controls:** 7 rows, 7 id, 1 read only, 0 left off. On the page: 9 controls and 1 lamp (APU ON, green). CP/G: 2 controls (the two power levers, row 6 of the panel); the other 6 rows exist in the pilot station only. Plus: `PLT_APU_BTN_CVR` (the cover of the APU button; read and command).
- **Special:** RTR BRK `PLT_ROTOR_BRK`: 2 OFF, 1 BRK (greyed out, needs conditions), 0 LOCK. MSTR IGN `PLT_MASTER_IGN_SW` (a dial): 0 OFF, 1 BATT, 2 EXT PWR (greyed out, no ground power). The APU button `PLT_APU_BTN` (lamp `PLT_APU_L` ON) `requires` its cover `PLT_APU_BTN_CVR` (0 CLOSED, 1 OPEN, a plain hinged flap and a control of its own) to be open: while the cover is closed the page does not send the button and the bridge refuses it. ENG START NO 1 / NO 2 `PLT_ENG1_START`, `PLT_ENG2_START`, rest 1: 2 START (momentary), 1 OFF, 0 IGN ORIDE (momentary), held 0.5 s. PWR LVR NO 1 / NO 2 (`{S}_ENG_L_PW_LVR`, `{S}_ENG_R_PW_LVR`, readback only; moved by keypress, see Power levers above): OFF 0, IDLE 16383, FLY 58981, LOCKOUT 65535 (greyed out); both seats. FRICT `PLT_PW_LVR_FRIC` is a slider (a knob, 0 to 65535).
- **Picture:** owner photo (not in the repo), manual figure p. 117.
- **Fit:** fits, 640 × 600 du as built (the whole budget; pilot) and 312 × 576 du (CP/G): one plate each.

Decided: the power levers and FRICT keep one touch band per mark and the knob bar (no chooser; owner review).

Question: Are the CP/G power lever keys (`RAlt` / `RShift` with `Home`, `PageUp`, `PageDown`, `End`) right in the CP/G seat? They are tested in the pilot seat only.

Question: Are the hold times right (ENG START switch 0.5 s, APU button 0.3 s), is the APU ON lamp green, and is the FRICT slider direction right (it was taken from the photos, not from DCS)?

#### EXT / INTR LT

- **Panels:** Exterior Lighting / Interior Lighting Panel (p. 119).
- **Arrangement:** pilot only, one plate (left console). On the page: the EXT LT block at the left (NAV toggle, FORM knob, ANTI COL toggle), a printed rule, the INTR LT block at the right (SIGNAL and PRIMARY knobs in the top row, FLOOD and STBY INST knobs below them, the PRESS TO TEST button at the bottom). The CP/G page of its smaller lighting panel is INTR LT, below.
- **Controls:** 8 rows, 8 id, 0 read only, 0 left off. On the page: 8 controls and 1 lamp (the PRESS TO TEST button, amber, read from its own id).
- **Special:** NAV `PLT_EXTL_NAV_L_SW`: 2 BRT, 1 OFF, 0 DIM. FORM `PLT_EXTL_FROMATION_L_KNB` (DCS-BIOS spells it FROMATION), OFF to BRT. ANTI COL `PLT_EXTL_ACOL_L_SW`: 2 WHT, 1 OFF, 0 RED. SIGNAL `{S}_INTL_SIGNAL_L_KNB` (DIM to BRT, with the RST mark), PRIMARY `{S}_INTL_PRIMARY_L_KNB`, FLOOD `{S}_INTL_FLOOD_L_KNB` and STBY INST `PLT_INTL_STBYINST_L_KNB` (OFF to BRT, pilot only) are knobs. PRESS TO TEST `{S}_INTL_TEST_BTN` lights every signal light.
- **Picture:** owner photo (not in the repo), manual figure p. 119.
- **Fit:** fits, 612 × 456 du as built: one plate.

Question: The end of the SIGNAL knob sweep was taken from the photo, not from DCS. Check it in DCS.

#### INTR LT

- **Panels:** Interior Lighting Panel (p. 126).
- **Arrangement:** CP/G only, one plate (left console), title INTR LT. On the page: SIGNAL and PRIMARY knobs in the top row, the FLOOD knob and the PRESS TO TEST button below. It has no NAV, FORM, STBY INST and ANTI COLL controls.
- **Controls:** 4 rows, 4 id, 0 read only, 0 left off. On the page: 4 controls and 1 lamp (the PRESS TO TEST button, amber, read from its own id).
- **Special:** the same knobs as on EXT / INTR LT with the CP/G ids `CPG_INTL_SIGNAL_L_KNB`, `CPG_INTL_PRIMARY_L_KNB`, `CPG_INTL_FLOOD_L_KNB` and the button `CPG_INTL_TEST_BTN`.
- **Picture:** owner photo (not in the repo), manual figure p. 126.
- **Fit:** fits, 428 × 360 du as built: one plate.

#### FIRE DET/EXTG

- **Panels:** Fire Detection / Extinguishing Panel (FIRE DET/EXTG) (p. 106).
- **Arrangement:** one plate, the same in both seats (glareshield, next to the left MPD), title FIRE DET/EXTG. On the page: the ENG 1, APU and ENG 2 fire buttons in a row, each in a dark housing with a hazard strip; below them the PRI button, the TEST switch (horizontal) and the RES button.
- **Controls:** 14 rows, 14 id, 8 read only, 0 left off. On the page: 6 controls and 8 lamps. Plus: `PLT_FIRE_ENG1_CVR`, `PLT_FIRE_APU_CVR`, `PLT_FIRE_ENG2_CVR`, `CPG_FIRE_ENG1_CVR`, `CPG_FIRE_APU_CVR`, `CPG_FIRE_ENG2_CVR` (the real covers).
- **Special:** a FIRE light (yellow in the cockpit, drawn amber) and a green RDY light on each of ENG 1, APU and ENG 2, and a DISCH light on PRI and RES. A fire button press arms the extinguisher for that compartment and shuts off its fuel (press again: safe). Buttons `{S}_FIRE_ENG1_BTN`, `{S}_FIRE_APU_BTN`, `{S}_FIRE_ENG2_BTN`, `{S}_FIRE_PRIME_EXT` (PRI, discharge) and `{S}_FIRE_RES_EXT` (RES, discharge) are all guarded; ENG 1, APU and ENG 2 have a real DCS cover. Lamps: FIRE `{S}_ENG_1_FIRE_L`, `{S}_APU_FIRE_L`, `{S}_ENG_2_FIRE_L`, RDY `{S}_ENG_1_READY_L`, `{S}_APU_READY_L`, `{S}_ENG_2_READY_L`, DISCH `{S}_FIRE_EXT_DISCH_PRI_L`, `{S}_FIRE_EXT_DISCH_RES_L`. TEST `{S}_FIRE_DETECT_TEST`, rest 1: 0 "1" (momentary), 1 OFF, 2 "2" (momentary), held 0.5 s; not guarded.
- **Picture:** owner photo (not in the repo), manual figure p. 106.
- **Fit:** fits, 600 × 456 du as built: one plate.

Question: Are ENG 1, APU and ENG 2 FIRE confirmed by their own readback once the real cover is open? If ENG 1 is still `not confirmed` with the cover open, confirm with the RDY lamp (`{S}_ENG_1_READY_L`) instead of the button.

Question: Does the bridge open and close DCS's own cover (`cover open`, `pressed`, about 1 s later `cover closed`, no `not confirmed`) in both seats? And PRI and RES with a fire button armed have never been sent before; do them last in a throwaway mission.

Question: Lamp colours: the manual does not give the DISCH lights, check them in DCS.

#### STORES JETT

- **Panels:** Stores Jettison Panel (p. 119).
- **Arrangement:** one plate, the same in both seats (left console), title STORES JETTISON. On the page: the four wing station buttons (L OUTBD, L INBD, R INBD, R OUTBD) in a row, L TIP at the left and R TIP at the right below them, and the JETT plunger between them on a hazard pad.
- **Controls:** 11 rows, 11 id, 4 read only, 0 left off. On the page: 7 controls and 6 lamps (ARM, amber). The lamps of L TIP and R TIP are second ids of their button rows (PANELS.md has no row for them).
- **Special:** the station buttons `{S}_JETT_STORE_LO`, `_LI`, `_RI`, `_RO`, `_LW`, `_RW` (L OUTBD, L INBD, R INBD, R OUTBD, L TIP, R TIP) press to arm or disarm a station, with the lamps `{S}_JETT_L_OUTBOARD_L`, `_L_INBOARD_L`, `_R_INBOARD_L`, `_R_OUTBOARD_L`, `_L_TIP_L`, `_R_TIP_L`; they are normal buttons. Only the seat that armed a station can disarm it; once any station is armed, either seat can press JETT. The manual says L TIP and R TIP have no function; DCS-BIOS has the buttons and their lamps, so they are on the page. JETT `{S}_JETT_BTN` jettisons every armed station and is a guarded control with the tablet cover only (no cover in DCS-BIOS).
- **Picture:** owner photo (not in the repo), manual figure p. 119.
- **Fit:** fits, 556 × 408 du as built: one plate.

Question: The six station selects and JETT (with a station armed) have never been sent in DCS; do them last in a throwaway mission.

#### ARMAMENT

- **Panels:** Armament Panel (p. 108), Master Zeroize Switch (p. 109), Video Panel (p. 109).
- **Arrangement:** pilot: three plates, the ARMAMENT plate and the MASTER ZEROIZE plate side by side on top, the VIDEO plate below them (the master zeroize switch sits on the instrument panel next to the armament panel, the video panel at the lower left of the pilot instrument panel). CP/G: the ARMAMENT and MASTER ZEROIZE plates only.
- **Controls:** 12 rows (5 + 1 + 6), 12 id, 3 read only, 0 left off. On the page: 9 controls and 3 lamps. CP/G: 6 rows (the Video Panel exists in the pilot station only), 3 controls and 3 lamps. Plus: `PLT_INST_MZERO_CVR`, `CPG_INST_MZERO_CVR` (the real cover of the master zeroize switch).
- **Special:** A/S `{S}_MASTER_ARM_BTN` is a push button with two lamps on its face, ARM (amber, `{S}_MASTER_ARM_ARM_L`) above SAFE (green, `{S}_MASTER_ARM_SAFE_L`); GND ORIDE `{S}_GROUND_OVERRIDE_BTN` with the lamp `{S}_GROUND_OVERRIDE_L` (ON, amber). MASTER ZEROIZE `{S}_INST_MZERO_SW` is a guarded switch (ON 1 on top, OFF 0) with the real cover `{S}_INST_MZERO_CVR`. On the VIDEO panel IHADSS BRT and CON (`PLT_VIDEO_IHADSS_BRT`, `PLT_VIDEO_IHADSS_CON`) share one knob and FLIR LVL and GAIN (`PLT_VIDEO_FLIR_LVL`, `PLT_VIDEO_FLIR_GAIN`) share one knob (MIN to MAX); a small mark next to the knob selects the function (`group`, `mark`, `dot`). SYM BRT `PLT_VIDEO_SYM_BRT` is a knob (MIN to MAX); ACM `PLT_VIDEO_AUTO_CON` is a cap switch (0 OFF, 1 ACM), N/I in the manual.
- **Picture:** owner photo (not in the repo), manual figure p. 108 (ARMAMENT) and p. 109 (VIDEO); MASTER ZEROIZE has no photo.
- **Fit:** fits, 608 × 600 du as built (pilot; the whole height): ARMAMENT 352 × 244 beside MASTER ZEROIZE 240 × 244 above VIDEO 608 × 340. CP/G 608 × 244 du.

Decided: MASTER ZEROIZE is a plain placard drawn without a photo (owner review).

Question: Check the lamp colours ARM (amber), SAFE (green) and GND ORIDE (amber) in DCS. MASTER ZEROIZE with its real cover has never been sent in DCS; do it last in a throwaway mission.

#### EUFD

- **Panels:** Enhanced Up-Front Display (EUFD) (p. 155).
- **Arrangement:** one plate, the same in both seats (instrument panel). On the page: the display on top, the controls in a row below it: the three rockers (WCA, IDM, RTS), the BRT knob and the four keys in a 2 × 2 block (P and ENTER above STOPWATCH and SWAP).
- **Controls:** 16 rows, 16 id, 8 read only, 0 left off. On the page: 8 controls and 1 display (the 14 lines).
- **Special:** the display `{S}_EUFD_LINE1` to `_LINE14` is 14 lines of 56 characters, shown as on the real display (the text size matters more than the photo layout). The warning, caution, advisory, radio status and information areas of the manual are columns and lines of this text. WCA, IDM and RTS (`{S}_EUFD_WCA`, `_IDM`, `_RTS`) are rockers (IDM and RTS: rest 1): 2 up, 1 off, 0 down; the IDM rocker is the datalink transmit select rocker (`likely`). BRT `{S}_EUFD_BRT` is a knob (DIM to BRT). P `{S}_EUFD_PRESET`, ENTER `{S}_EUFD_ENT`, STOPWATCH `{S}_EUFD_STOPWATCH` (press to start or stop, hold to reset) and SWAP `{S}_EUFD_SWAP` are flat keys drawn with a symbol.
- **Picture:** owner photo (not in the repo), manual figure p. 155 (overview p. 105).
- **Fit:** fits, 640 × 524 du as built: one plate.

Decided: the display is on top and the controls sit in a row below it (three rockers, BRT knob, four keys), not around the glass as on the photo; the glass is 568 × 280 du, nearly the full page width, so the 14 lines of 56 characters stay readable (owner review).

#### CMWS

- **Panels:** CMWS Control Panel (p. 630).
- **Arrangement:** pilot only, two plates, the INDICATOR plate on top and the CONTROL PANEL plate below. On the page: the PWR rotary, the STATUS window, the THREAT dial and the AUDIO and LAMP knobs on the indicator plate; the ARM / SAFE, CMWS / NAV and BYPASS / AUTO toggles and the guarded JETTISON switch (on a hazard pad) on the control plate.
- **Controls:** 13 rows, 13 id, 6 read only, 0 left off. On the page: 7 controls, 1 display and 6 lamps (the THREAT dial: four sectors FWD LEFT, FWD RIGHT, AFT RIGHT, AFT LEFT and the letters D and R, orange, each with a bright and a dim DCS-BIOS id). Plus: `PLT_CMWS_JETT_CVR` (the real cover of the JETTISON switch).
- **Special:** PWR `PLT_CMWS_PW` (a dial), rest 1: 0 OFF, 1 ON, 2 TEST (momentary), held 0.5 s. STATUS is a display of several ids (`PLT_CMWS_FLARE_LETTER`, `_FLARE_COUNT`, `_CHAFF_LETTER`, `_CHAFF_COUNT`, `_BIT_LINE_1`, `_BIT_LINE_2`, `_PAGE`) with pages: page MAIN `F 60` / `C 30`, page TEST the two test lines, page NONE blank. THREAT lamps `PLT_CMWS_FWD_LEFT_BRT_L`, `_FWD_RIGHT_`, `_AFT_LEFT_`, `_AFT_RIGHT_`, `PLT_CMWS_D_BRT_L`, `PLT_CMWS_R_BRT_L` (and the matching `_DIM_L`) are page-level indicators, orange, bright and dim. AUDIO `PLT_CMWS_VOL` (no function in the manual) and LAMP `PLT_CMWS_LAMP` are knobs (MIN to MAX). ARM / SAFE `PLT_CMWS_ARM`: 1 ARM, 0 SAFE. CMWS / NAV `PLT_CMWS_MODE`: 1 CMWS, 0 NAV. BYPASS / AUTO `PLT_CMWS_BYPASS`: 1 BYPASS, 0 AUTO. JETTISON `PLT_CMWS_JETT` is a guarded switch (ON 1 on top, OFF 0) with the real cover `PLT_CMWS_JETT_CVR`; DCS ignores the switch while its cover is closed. The counts are also on FIGHT.
- **Picture:** owner photo (not in the repo), manual figure p. 630 (indicator display p. 631).
- **Fit:** fits, 616 × 552 du as built: INDICATOR 616 × 288 above CONTROL PANEL 616 × 248.

Question: CMWS JETT has never been sent in DCS; do it last in a throwaway mission.

#### CENTER

- **Panels:** Check Overspeed Test / Generator Reset Panel (p. 111), Windshield Wiper Control Panel (p. 112), Parking Brake Handle (p. 112), Standby Altimeter (p. 111).
- **Arrangement:** pilot only (instrument panel), three plates: one wide plate (CHK OVSP TEST and GEN RST) over two plates (WINDSHIELD WIPER, and PARK BRAKE with ALT SET), 16 du apart on shared edge lines. The standby altimeter has no plate of its own: only its barometric setting knob is on the page, as ALT SET, on the PARK BRAKE plate.
- **Controls:** 11 rows (3 + 2 + 1 + 5), 10 id, 3 read only, 4 left off (1000-foot Altitude Scale, 1000-ft Scale Indicator, Altitude Indicator, "Kollsman" Window). On the page: 7 controls.
- **Special:** CKT A / B `PLT_CHK_OSPD_ENG_A`, `_B` (CHK OVSP TEST), rest 1: 2 ENG 1, 1 OFF, 0 ENG 2 (spring return, held 0.5 s); the positions are printed once between the two switches; the ENG 1 and ENG 2 positions are N/I in the manual. GEN RST `PLT_GEN_RESET` (horizontal), rest 1: 0 GEN 1, 1 off, 2 GEN 2 (spring return, held 0.5 s). DEFOG `PLT_DEFOG_BTN` (round button, N/I in the manual). WINDSHIELD WIPER `PLT_WIPER_SW` (a dial): 0 PARK, 1 OFF, 2 LO, 3 HI; PARK springs back to OFF in the cockpit. PARK BRAKE `PLT_PARK_BRAKE` (horizontal): 0 IN, 1 PULLED. ALT SET `PLT_ALT_SET_KNB` is a knob (0 to 65535). The standby altimeter drums and needle (`PLT_ALT_NEEDLE`, `PLT_ALT_1000`, `PLT_ALT_10000`, `PLT_ALT_PRESS_1`, `PLT_ALT_PRESS_10`, `PLT_ALT_PRESS_1100`) are not drawn (section 12).
- **Picture:** owner photo (not in the repo), manual figure p. 111 (overspeed panel and altimeter) and p. 112 (wiper and parking brake).
- **Fit:** fits, 640 × 530 du as built: CHK OVSP TEST 640 × 210 above WINDSHIELD WIPER 376 × 304 beside PARK BRAKE / ALT SET 248 × 304.

Decided: CENTER is one wide plate over two plates, 16 du apart on shared edge lines, not the arrangement of the photo (owner review).

Decided: the wiper labels PARK, OFF, LO and HI are flat text in a fan above the dial, not turned along the dial as on the photo (owner review).

Decided: the PARK BRAKE name is printed on two lines (PARK, BRAKE); on one line it runs into the plate margin and the corner ear (owner review).

#### COMM

- **Panels:** Communications Panel (p. 121).
- **Arrangement:** one plate, one drawing for both seats (right console), title COMM. On the page: the SOL block with the VHF, UHF, FM 1, FM 2 and HF volume knobs, each with its PULL chip under it and its squelch switch below; then MASTER, SENS, the ICS switch and IDENT; the AUX block with the IFF, RLWR, ATA, VCR and ADF volume knobs (VCR and ADF with PULL chips). The ICS name and its PTT label sit in the SOL row, between the FM 1 and FM 2 squelch switches; the switch itself, with VOX and HOT MIC, is below the row.
- **Controls:** 15 rows, 15 id, 0 read only, 0 left off. On the page: 26 touch controls (12 knobs, 7 PULL chips, 5 squelch switches, ICS, IDENT).
- **Special:** volume knobs VHF, UHF, FM 1, FM 2, HF `{S}_COM_VHF_VOL`, `_UHF_`, `_FM1_`, `_FM2_`, `_HF_` and IFF, RLWR, ATA, VCR, ADF `{S}_COM_IFF_VOL`, `_RLWR_`, `_ATA_`, `_VCR_`, `_ADF_` (MIN to MAX). The knobs of VHF, UHF, FM 1, FM 2, HF, VCR and ADF have a PULL chip (a `chip` control, 64 × 22 du, touch area at least 32 px) hanging under the knob for the pull-to-disable position: `{S}_COM_VHF_PW`, `_UHF_`, `_FM1_`, `_FM2_`, `_HF_`, `{S}_COM_VCR_PW`, `{S}_COM_ADF_PW` (0 In, 1 Out; Out mutes the source); holding the knob for 0.6 s toggles it too, a short tap opens the knob bar. SQL x 5 `{S}_COM_VHF_SQL`, `_UHF_`, `_FM1_`, `_FM2_`, `_HF_`, rest 1: 2 ENABLE, 1 off, 0 DISABLE (spring return, held 0.5 s). MASTER `{S}_COM_MASTER_VOL` and SENS `{S}_COM_SENS_KNB` are knobs (MIN to MAX). ICS `{S}_COM_ICS_MODE`: 0 HOT MIC, 1 VOX, 2 PTT (takes about 3 s to reach the position). IDENT `{S}_COM_IDENT_BTN` is a push button. IDENT, IFF and VCR are N/I in the manual and ATA has no function; they stay on the page.
- **Picture:** owner photo (not in the repo), manual figure p. 121 (CP/G p. 127).
- **Fit:** fits, 640 × 600 du as built (the whole budget): one plate.

Decided: the ICS name and its PTT label sit in the SOL row, between the FM 1 and FM 2 squelch switches, and the switch itself with VOX and HOT MIC is below the row, not as on the photo (owner review).

Decided: the PULL chip is exempt from the 56 px touch floor of the layout checker; its floor is 32 px, and the long press (0.6 s) on its knob is the large target (owner review).

Question: Does `PULL OUT` fit and read in the font the iPad uses (it fits in Arial Narrow and Arial; the iPad may use Helvetica Neue), and is the long press (0.6 s) on the knob comfortable?

#### WIPER / DEFOG

- **Panels:** Windshield Wiper Control Panel (p. 112).
- **Arrangement:** CP/G only, one plate (right console, below COMM): the same drawing as the wiper plate of CENTER, title WINDSHIELD WIPER, the DEFOG round button at the left and the wiper dial with its position labels fanned above it.
- **Controls:** 2 rows, 2 id, 0 read only, 0 left off. On the page: 2 controls.
- **Special:** DEFOG `CPG_DEFOG_BTN` is a push button; WINDSHIELD WIPER `CPG_WIPER_SW` (a dial): 0 PARK, 1 OFF, 2 LO, 3 HI.
- **Picture:** owner photo (not in the repo), manual figure p. 112 (CP/G p. 127).
- **Fit:** fits, 376 × 304 du as built: one plate.

Decided: as on CENTER, the wiper labels PARK, OFF, LO and HI are flat text in a fan above the dial (owner review).

### Link boxes

| Box | Opens | Grid (pilot) | Grid (CP/G) | Controls |
| --- | --- | --- | --- | --- |
| KU | KU tab | [1,1,1,3] | [1,1,1,3] | Keyboard Unit (KU) (p. 113), section 6 |
| MPD L | MPD tab, left display | [3,4,3,3] | [2,4,3,2] | the left Multi-Purpose Display, Multi-Purpose Displays (MPD) (p. 164), section 5 |
| TEDAC | MPD tab, TEDAC | none | [2,6,3,2] | TEDAC Display Unit (TDU) (p. 129), section 5 |
| MPD R | MPD tab, right display | [3,7,3,3] | [2,8,3,3] | the right Multi-Purpose Display, Multi-Purpose Displays (MPD) (p. 164), section 5 |

**CANOPY key.** `CANOPY` is a small key button on the pilot map, cell [2,7,1,3]: key `canopy` (default `LCtrl+C`, section 9), readback `PLT_CANOPY` (0 CLOSED, 1 OPEN). DCS-BIOS cannot move the canopy; a key does.

## 3. FLIGHT

The quick page for flying, on the fixed 7 × 3 grid (each control has `"grid": [row, col, rows, cols]`: 3 rows and 7 columns, as on the A-10C and the F-16C): the trim display, the controls overlay key, the symbology hat, the monocle key, TAIL WHEEL (pilot) and the two power levers. The grid is fixed so that the power levers and TAIL WHEEL stay in the same place when switching to FIGHT. FLIGHT follows the current seat and is listed for both. Flight instruments are not drawn (cockpit-replica graphics are out of scope, [../SPEC.md](../SPEC.md) section 11, and section 12 here). The lamp row is in section 8. Sources in [PANELS.md](PANELS.md): Cyclic Grip (p. 136), Tail Wheel / NVS Mode Panel (p. 115), Power Quadrant Panel (p. 117).

**Built**

| Control | Type | Source | Grid |
| --- | --- | --- | --- |
| TRIM | read-only trim display | export script + `{seat}_CYCLIC_TRIM_UD`, see Trim display | [1,1,2,2] |
| CTRL IND | key button; toggles DCS's own controls overlay (no lag) | key `controls_overlay` | [3,1,1,1] |
| SYMBOLOGY | two-way hat: T/C ↑ (2), H/B ↓ (0), held 0.3 s, back to centre | `{seat}_CYCLIC_SYMBOLOGY` | [1,4,2,1] |
| MONOCLE | key button (push button, no state) | key `monocle` | [1,5,1,1] |
| TAIL WHEEL | lit push button, press = 1, released to 0 after 0.3 s; pilot seat only (greyed in the CP/G seat) | `PLT_T_WHEEL_UNLOCK_BTN`, lamp `PLT_T_WHEEL_UNLOCK_L` | [2,5,1,1] |
| PWR LVR 1, 2 | lever (keypress, readback); ids `flight_power_left` / `flight_power_right` | keys `power_*`, readback `{seat}_ENG_L_PW_LVR` / `{seat}_ENG_R_PW_LVR` | [1,6,3,1], [1,7,3,1] |

The power levers work as described under Power levers in section 2. TAIL WHEEL is also on the TAIL WHEEL / NVS page. **Grid** (3 rows × 7 columns; `..` = the cell continues the control on its left or above):

```
       c1        c2        c3        c4        c5        c6        c7
row 1  TRIM      ..                  SYMBOL    MONOCLE   PWR LVR 1 PWR LVR 2
row 2  ..        ..                  ..        TAIL WHL  ..        ..
row 3  CTRL IND                                           ..        ..
```

**Trim display.**

- The export script sends the actual control positions 10 times per second. The bridge receives them on the export port (if the port is busy it logs `export port busy` and runs without them).
- The live position is not drawn (it lags behind the stick); CTRL IND toggles DCS's own overlay for that.
- **Trim point:** when the Force Trim switch (`{seat}_CYCLIC_TRIM_UD`) goes from 2 (held, `TRIM_RELEASED`) back to rest, the bridge stores the cyclic pitch / roll and the pedals at that moment as the seat's trim point and logs `PLT set P … R … Y …`.
- **Trim reset:** while DCS is the active window, the bridge watches the `trim_reset` key by reading only that key's state; on a press it moves the trim point to the centre and logs `PLT reset`.
- `/state` has `controls` (the latest positions), `controls_age` and `trim`: `{"plt": {"pitch", "roll", "pedals", "reset", "age"}, ...}`.
- The page draws a small box with a green ring at the trim point and a green tick on the pedal bar, with the values as text; `NOT TRIMMED` before the first trim, `RESET` after a reset. Directions are set by `CTRL_PITCH_SIGN`, `CTRL_ROLL_SIGN`, `CTRL_PEDAL_SIGN` at the top of the page script.

Question: Are the directions of the trim ring and the tick right after a few trims in DCS? ([../FIXES.md](../FIXES.md))

## 4. FIGHT

The quick page for weapons, sensors and countermeasures, on the fixed 7 × 3 grid as FLIGHT. FIGHT is two pages, one per seat, both named Fight ([Seats](#seats)). The tab bar has one FIGHT tab; it opens the page of the current seat, and a seat change switches to the page of the new seat. The lamp row is in section 8. Sources in [PANELS.md](PANELS.md): Armament Panel (p. 108), Cyclic Grip (p. 136), Collective Mission Grip (p. 140), CMWS Control Panel (p. 630), TEDAC Left Handgrip (LHG) (p. 131), TEDAC Right Handgrip (RHG) (p. 134).

**Hats.** A hat is drawn as a cross of four buttons. A tap sets the axis (`_UD` or `_LR`) to 2 (up, right) or 0 (down, left) and holds it for 0.3 s; then the bridge returns the axis to the centre, 1. The highlighted direction comes from the readback of the two axes. The pilot page uses the cyclic WAS and the collective sight select; the gunner page uses the cyclic WAS and the right-grip sight select. The left-grip WAS (LHG WAS) is left out on purpose: it does the same as the cyclic WAS (it works too, as a fallback). On the pilot page each hat takes two rows × two columns of the grid (WAS: rows 1–2, columns 3–4; SIGHT SEL: rows 1–2, columns 5–6), so every button is at least 56 px high. The gunner page has no room for that, see [Touch sizes per view](#touch-sizes-per-view).

### Pilot page

Ids are written with `{seat}` where the same control exists in the CP/G seat; the page is listed for the pilot seat only (`"seats": [0]`).

| Control | DCS-BIOS | Positions | Notes | Grid |
| --- | --- | --- | --- | --- |
| A/S | `{seat}_MASTER_ARM_BTN` | push button | press = 1, released to 0 after 0.3 s; the ARM and SAFE lamps show the result | [1,1,1,1] |
| GND ORIDE | `{seat}_GROUND_OVERRIDE_BTN` | push button | as A/S | [1,2,1,1] |
| WAS | hat: `{seat}_CYCLIC_WEAPON_UD` / `_LR` | up = G, down = A, left = R, right = M | see Hats | [1,3,2,2] |
| SIGHT SEL | hat: `{seat}_COLLECTIVE_SIGHT_SELECT_UD` / `_LR` | up = HMD, down = LINK, left = FCR, right = TADS | see Hats | [1,5,2,2] |
| FLARE, CHAFF | `{seat}_CYCLIC_FLARE`, `{seat}_CYCLIC_CHAFF` | push button | as A/S | [2,1,1,1], [2,2,1,1] |
| FLARE COUNT, CHAFF COUNT | `PLT_CMWS_FLARE_COUNT`, `PLT_CMWS_CHAFF_COUNT` | display | read only; from the pilot's CMWS panel, also shown on the gunner page | [3,1,1,1], [3,2,1,1] |

**CMWS.** Flares only fire with the CMWS panel set up: CMWS PWR ON, FLARE SQUIBS ARM, CMWS MODE CMWS; CMWS OPER BYPASS / AUTO decides whether the CMWS dispenses on its own. Chaff must be armed on the MPD ASE page. On the ground dispensing may be blocked.

| Control | DCS-BIOS | Positions | Grid |
| --- | --- | --- | --- |
| CMWS PWR | `PLT_CMWS_PW` | 2 = TEST (spring-loaded, 0.5 s), 1 = ON, 0 = OFF | rows 1–2, column 7 ([1,7,2,1]) |
| FLARE SQUIBS | `PLT_CMWS_ARM` | 1 = ARM, 0 = SAFE | row 3, column 5 ([3,5,1,1]) |
| CMWS MODE | `PLT_CMWS_MODE` | 1 = CMWS, 0 = NAV | row 3, column 6 ([3,6,1,1]) |
| CMWS OPER | `PLT_CMWS_BYPASS` | 1 = BYPASS, 0 = AUTO | row 3, column 7 ([3,7,1,1]) |

**Grid** (3 rows × 7 columns; `..` = the cell continues the control on its left or above):

```
       c1        c2        c3        c4        c5        c6        c7
row 1  A/S       GND ORIDE WAS       ..        SIGHT SEL ..        CMWS PWR
row 2  FLARE     CHAFF     ..        ..        ..        ..        ..
row 3  FL COUNT  CH COUNT                      SQUIBS    CMWS MODE CMWS OPER
```

### Gunner page

The page of the CP/G seat (`"seats": [1]`). Ids are written out as `CPG_...` (the page exists for one seat only). 14 controls:

| Control | DCS-BIOS | Positions | Notes | Grid |
| --- | --- | --- | --- | --- |
| A/S | `CPG_MASTER_ARM_BTN` | push button | as on the pilot page | row 1, column 1 ([1,1,1,1]) |
| GND ORIDE | `CPG_GROUND_OVERRIDE_BTN` | push button | as A/S | row 1, column 2 ([1,2,1,1]) |
| FLARE, CHAFF | `CPG_CYCLIC_FLARE`, `CPG_CYCLIC_CHAFF` | push button | as A/S | row 2, columns 1 and 2 ([2,1,1,1], [2,2,1,1]) |
| FLARE COUNT, CHAFF COUNT | `PLT_CMWS_FLARE_COUNT`, `PLT_CMWS_CHAFF_COUNT` | display | read only, as on the pilot page | row 3, columns 1 and 2 ([3,1,1,1], [3,2,1,1]) |
| WAS | hat: `CPG_CYCLIC_WEAPON_UD` / `_LR` | up = G, down = A, left = R, right = M | see Hats | row 1, columns 3 and 4 ([1,3,1,2]) |
| SIGHT SEL | hat: `CPG_RHG_SIGHT_UP_DN` / `CPG_RHG_SIGHT_L_R` | up = HMD, down = LINK, left = FCR, right = TADS | right grip, see Hats | row 2, columns 3 and 4 ([2,3,1,2]) |
| SLAVE | `CPG_RHG_SIGHT_SLAVE` | push button | slaves the selected sight to the acquisition source, or releases it; held 0.3 s | row 3, column 3 ([3,3,1,1]) |
| TADS FOV | hat: `CPG_LHG_TADS_FOV_UP_DN` / `CPG_LHG_TADS_FOV_L_R` | up = Z (zoom), left = N (narrow), right = W (wide), down = M (medium) | left grip, see Hats | row 1, columns 5 and 6 ([1,5,1,2]) |
| SENSOR | `CPG_LHG_TADS_SEL` | 2 = FLIR, 1 = TV, 0 = DVO (greyed out, no function in DCS) | selector | row 2, columns 5 and 6 ([2,5,1,2]) |
| IAT | `CPG_LHG_TEDAC_L_IAT` | 2 (forward), then back to 1 | held 0.3 s | row 1, column 7 ([1,7,1,1]) |
| OFS | `CPG_LHG_TEDAC_L_IAT` | 0 (aft), then back to 1 | held 0.3 s | row 2, column 7 ([2,7,1,1]) |
| OFS ALL | `CPG_LHG_TEDAC_L_IAT` | 0 (aft), then back to 1 | held 0.8 s | row 3, column 7 ([3,7,1,1]) |

Row 3, columns 4 to 6 are free. The control ids of the page are `CPG_WAS`, `CPG_SIGHT_SEL`, `CPG_TADS_FOV`, `CPG_IAT`, `CPG_OFS` and `CPG_OFS_ALL` for the hats and the three tracker buttons; the others use their DCS-BIOS id.

**Grid** (3 rows × 7 columns; `..` = the cell continues the control on its left):

```
       c1        c2        c3        c4        c5        c6        c7
row 1  A/S       GND ORIDE WAS       ..        TADS FOV  ..        IAT
row 2  FLARE     CHAFF     SIGHT SEL ..        SENSOR    ..        OFS
row 3  FL COUNT  CH COUNT  SLAVE                                    OFS ALL
```

**IAT, OFS and OFS ALL** are three buttons on one switch of the left grip: a 3-position switch that springs back to the middle (rest 1). IAT is forward (2), OFS is aft (0), taken from the grip like the other hats; the mapping is to be confirmed in DCS, together with the SENSOR mapping. Each button sends its position, holds it and returns the switch to 1 (`bios`, `value` and `rest` in [section 8 of the generic spec](../SPEC.md#8-the-bridge-interface)). What they do, after the DCS manual:

- **IAT** starts an auto-track on the target under the TADS reticle, or updates the aim point when the reticle is inside the gates.
- **OFS** (short press): drops the primary track when the reticle is inside the gates; outside the gates it returns the TADS to the primary track.
- **OFS ALL** (the aft position held over 0.5 s, here 0.8 s): deletes all tracks.

**Not on the page.** The weapon trigger and the laser trigger. DCS-BIOS has no entry for the laser trigger; the weapon trigger (`CPG_CYCLIC_TRIGGER`) has one, but it is on the [blocklist](../SPEC.md#blocklist-idea) and releases weapons. Both could become key buttons later (key bindings in DCS, like George). Also left out, not asked for: the FCR mode and scan switches, FLIR polarity, the laser tracker mode, MTT promote, the cursor extras, STORE and LMC; they can go into free cells later. The full list is section 12.

Question: The hats WAS, SIGHT SEL and TADS FOV and the SENSOR selector of the gunner page are under 56 px high, because the 7 × 3 grid has no room for two-row hats (a fourth grid row, eight columns or less chrome per cell would give it). Which one? ([../FIXES.md](../FIXES.md))

Question: Do IAT, OFS and OFS ALL do what the grip does, is the switch mapping right (IAT forward = 2, OFS aft = 0, rest 1), and are the TADS FOV letters and the SENSOR mapping (FLIR 2, TV 1) right? ([../FIXES.md](../FIXES.md))

## 5. MPD

One display at a time, following the current seat (`"layout": "mpd"`). A `LEFT MPD | TEDAC | RIGHT MPD` switch at the top selects which one (remembered on the tablet); TEDAC appears only in the CP/G seat. The side is preselected by the map boxes MPD L, MPD R and TEDAC ([Link boxes](#link-boxes)). The display sits flush left, the cursor group uses the rest of the width (pad about 450 px on the iPad Air); in the CP/G seat with the TEDAC selected the TKR group takes its place. Sources in [PANELS.md](PANELS.md): Multi-Purpose Displays (MPD) (p. 164), TEDAC Display Unit (TDU) (p. 129).

- **Controls:** 18 rows (MPD) and 19 rows (TDU), 33 id, 0 read only, 4 left off (MPD screen, Menu page, Variable Action Button label styles, TDU screen: display content, section 12). On the tab: per display 31 buttons (the 24 variable action buttons, FCR, WPN, TSD, VID, COM, A/C, \*), the BRT and VID knobs and the MODE selector; the cursor pad with CURSOR SWITCH DISPLAY and ENTER; the TEDAC with 9 buttons, the MODE selector, 2 knobs and 6 rockers; the TKR pad with SLAVE.
- Laid out 1:1 after a photo of the real MPD: every button, knob and print at its measured position (square spacing, about 100 px pitch on the photo). VID knob on the raised top-left corner, BRT below it, MODE top right with DAY / NT / MONO; \* above R1; FCR / WPN below L6, VID / COM below R6; TSD and A/C offset in the bottom corners next to M and B2–B6.
- Variable action buttons are light grey with a green dot; fixed action buttons are black keys with green text. Buttons are drawn at true size (about 33 px on the iPad Air) with a larger invisible touch area (56 px where neighbours allow). Each press is held 0.3 s.
- **Live labels:** the export script sends the occupied seat's MPD texts (`MPD_INDICATIONS`, `MPD_SEATS`: pilot 7 left / 9 right, CP/G 11 / 13) 4 times per second. The bridge reads the `PB<n>` fields and serves them as `mpd_labels` in `/state` (`{"L": {...}, "R": {...}, "age": ...}`); the page writes each label in MPD green next to its button. Mapping: PB1–6 = T1–T6, PB7–12 = R1–R6, PB13–18 = B6…B1 (PB18 = M), PB19–24 = L6…L1. No labels when no MPD text arrived for 3 s.
- In the CP/G seat the left MPD's L1–L6 do not respond in DCS.

### Cursor

The CURSOR pad sits to the right of the bezel, for the collective cursor controller `{seat}_COLLECTIVE_CURSOR_LR` / `_UD` (analog, centre 32768). Put a finger anywhere on the pad and push: the distance from the touch point (up to 30 % of the pad) is the deflection, i.e. the cursor speed, like the real force-sensing controller. Lifting the finger sends centre. The page sends `{"x", "y"}` (−1..1) at most every 66 ms; the bridge sends only changed axes and does not wait behind slow commands. `CURSOR_Y_SIGN` at the top of the page script flips up / down. Below the pad: CURSOR SWITCH DISPLAY (`{seat}_COLLECTIVE_CURSOR_DISPLAY`, moves the cursor to the other MPD) and ENTER (`{seat}_COLLECTIVE_CURSOR_ENTER`). The cursor group is shown with LEFT MPD and RIGHT MPD and in the pilot seat; with the TEDAC selected (CP/G seat) it is replaced by the TKR group.

### TKR (TEDAC selected, CP/G seat)

The TKR group replaces the cursor group: a pad labelled TKR and the SLAVE button below it (`CPG_RHG_SIGHT_SLAVE`, as on the gunner FIGHT page). The pad is the Sight Manual Tracker of the right grip (`CPG_RHG_MAN_TRK_UP_DN`, `CPG_RHG_MAN_TRK_L_R`), a `stick` control with the flag `digital`. It looks and feels like the cursor pad (a finger anywhere on it, the distance from the touch point is the deflection), but the tracker has three states per axis: 2, 1 (centre) and 0. The bridge turns the deflection into 2 / 0 / 1 with a dead zone of 30 % of the full deflection (`STICK_DIGITAL`) and sends only changes; lifting the finger returns both axes to the centre, 1. DCS ramps the slew rate up while the switch is held (the DCS option MAN TRK ramp-up speed), so the speed is not set by the pad. The up / down sign is shared with the cursor (`CURSOR_Y_SIGN`).

### TEDAC (CP/G seat)

The CP/G's TEDAC display unit, laid out 1:1 after a photo like the MPD. All controls are `CPG_TEDAC_…`, `"side": "T"`, `"seats": [1]`:

- Top: TAD, FCR, PNV, G/S video select buttons; MODE knob DAY / NT / OFF (2 / 1 / 0, knob bar).
- Left: LEV and GAIN knobs (knob bar), R/F and EL rockers. Right: SYM, BRT, CON rockers and \*.
- Bottom: ◀AZ▶ rocker, then four buttons AZ/EL, ACM, FREEZE, FILTER with their names in green on the screen.
- Rockers are spring-loaded: tap the upper / lower half (AZ: left / right half); the bridge holds the position until confirmed and returns it to the centre.

### Knob bar

Tapping a knob (MPD BRT / VID / MODE, KU BRT, TEDAC knobs, the knobs of the COCKPIT pages) opens a bar at the knob (420 px wide, or the screen less 24 px, 130 px high): below it, above it if there is no room, always inside the screen. BRT / VID / KU BRT and the panel knobs: drag or tap the track; the bridge sets the absolute knob position (`{"value": 0..65535}`, at most every 100 ms while dragging). MODE: three stops DAY / NT / MONO. Tap outside or the close cross (56 × 56 px) to close. The MPD mode selectors use `step_fallback`: if the position is not reached in 0.5 s the bridge turns the knob with INC / DEC steps.

Question: Do the MPD live labels follow page changes, does the MODE knob work (NT through the INC / DEC fallback), and are the cursor speed and the up / down direction right? In the CP/G seat: are the TEDAC buttons, knobs and rockers and the TKR pad (all four directions, the dead zone, the slew ramp) right? ([../FIXES.md](../FIXES.md))

## 6. KU

The keyboard unit, drawn 1:1 after a photo in the same technique as the MPD (`"layout": "ku"`), following the current seat: round number keys, boxed E / N / S / W, the white guide lines of the panel, BRT knob in its recess (knob bar), wide ENTER. The map box KU opens this tab. Sources in [PANELS.md](PANELS.md): Keyboard Unit (KU) (p. 113).

- **Controls:** 10 rows, 9 id, 1 read only (the scratchpad), 1 left off (Display Prompt: no DCS-BIOS entry, section 12). On the tab: 49 keys, the BRT knob and the scratchpad display.
- Top: the scratchpad (`{seat}_KU_DISPLAY`) in green.
- Rows: A–F | 1 2 3, G–L | 4 5 6, M–R | 7 8 9, S–X | . 0 +/-, then Y Z / BKS SPC \* ÷ + −, then the BRT knob, CLR, ←, →, ENTER.
- Keys are pressed for 0.15 s.

## 7. GEORGE

George, the AI crew member (gunner when you fly as pilot, pilot when you fly as CP/G), can only be controlled by keypress. The GEORGE tab (`"name": "George"`, both seats) has direct buttons for the useful commands, so the Helper Interface (the ring) does not have to be opened by hand. The lamp row (section 8) has the two master lamps. George needs electrical power; without it the buttons do nothing. The keys must be bound in DCS once, see Binding the George keys in DCS in [section 9](#9-keybinds).

Every button is a `macro` control ([section 8 of the generic spec](../SPEC.md#8-the-bridge-interface)): a fixed key sequence, each step `[key name, hold in seconds, pause after in seconds]`. Hold times: short 0.15 s (`GEORGE_SHORT`), long 1.2 s (`GEORGE_LONG`; the manual calls a press over 0.5 s long, and some commands need a full second). A key with modifiers is pressed staggered: the modifiers go down, 40 ms later the letter goes down, is held, goes up, and 40 ms later the modifiers go up (`MACRO_KEY_GAP` in `core/dashboard.py`), so DCS sees the modifiers before the letter.

| Button | Seat | Key sequence | Notes | Grid |
| --- | --- | --- | --- | --- |
| PHS SEARCH | pilot | ring: Up, short, ring left open | George searches with the PHS; works once George's systems are ready (on the ground with the systems not ready the ring shows the start-up layout instead); the ring stays open so the Target List can appear | [1,1,1,1] |
| AIR AREA SEARCH | pilot | Hide, Show, `george_multi`, long | George must not be tracking; area search works in the air only: on the ground the same press starts George's systems (READY SYSTEMS) or, when they are already started, shuts them down (MASTER OFF); the ring is opened first and stays open so the Target List can appear | [1,2,1,1] |
| POINT SEARCH | pilot | Hide, Show, `george_multi`, short | George must not be tracking, and a TSD point must be selected; the ring is opened first and stays open so the Target List can appear | [1,3,1,1] |
| STORE TARGET | pilot | `george_store`, short | George stores a point only while he is tracking a target, otherwise he says he cannot; works without the ring (the ring does not open) | [2,1,1,1] |
| STOP / TADS FWD | pilot | ring: Down, short | cancels any task of George, including an engagement | [2,2,1,1] |
| WEAPON NEXT | pilot | ring: Left, short, ring left open | cycles NO WPN, GUN, MSL, RKT; the ring stays shown so the selection can be read in it | [3,1,1,1] |
| READY SYSTEMS / MASTER OFF | pilot | `george_multi`, long | on the ground George starts up his systems (TADS, lasers, displays) and announces when done, or, if they are already started, shuts them down; the same press as AIR AREA SEARCH, which one happens depends on whether the aircraft is on the ground | [3,2,1,1] |
| ROE HOLD / FREE | pilot | ring: Up, long, ring left open | toggles George's rules of engagement between HOLD FIRE and FREE FIRE; the ring stays open: yellow text is HOLD FIRE, green text is FREE FIRE (there is no readback, read the colour) | [2,3,1,1] |
| FIRE | pilot | `george_multi`, short | consent to fire the assigned weapon, also in HOLD FIRE | [3,3,1,1] |
| PREV TARGET | pilot | `george_up`, short | moves to the previous entry of the Target List; the TADS slews to it | [1,4,1,1] |
| NEXT TARGET | pilot | `george_down`, short | moves to the next entry of the Target List; the TADS slews to it | [2,4,1,1] |
| EXIT LIST | pilot | `george_left`, short | leaves the Target List and cancels the shoot list | [3,4,1,1] |
| SELECT TARGET | pilot | `george_multi`, short | adds the current entry to the shoot list or removes it (the entries are numbered in the list) | [1,5,1,1] |
| TRACK / ENGAGE | pilot | `george_right`, short | tracks the current target; if it is on the shoot list, starts the multi-target sequence | [2,5,1,1] |
| REQUEST CONTROL | CP/G | `george_request`, short | hands the flight controls to George and takes them back; works without the ring | [1,6,1,2] |
| SHOW RING | both | Hide, Show | opens the ring | [3,6,1,1] |
| HIDE RING | both | Hide | closes the ring and cancels a displayed Target, Search or Point list | [3,7,1,1] |

**Typical order.** On the ground press READY SYSTEMS and wait for George's announcement. In the air start a search with AIR AREA SEARCH (or PHS SEARCH or POINT SEARCH).

**Autonomous engagement.** When George reports targets, the Target List shows on the ring; it only appears if the ring is displayed when he detects them, which is why the three search buttons leave it open.

1. WEAPON NEXT beforehand assigns NO WPN, GUN, MSL or RKT.
2. PREV TARGET and NEXT TARGET move through the list; the TADS slews to the entry.
3. SELECT TARGET adds the entry to the shoot list or removes it again; the entries are numbered in the list.
4. ROE HOLD / FREE toggles the rules of engagement (the ring stays open; yellow text is HOLD FIRE, green text is FREE FIRE; there is no readback, read the colour).
5. TRACK / ENGAGE tracks the current target or, if it is on the shoot list, starts the multi-target sequence. With FREE FIRE George engages each target at once and moves on to the next by himself; with HOLD FIRE he waits for FIRE before every engagement.
6. FIRE gives consent to fire the assigned weapon, also in HOLD FIRE.
7. EXIT LIST leaves the list and cancels the shoot list.

The list buttons only press a direction key, with no Hide first, because Hide would cancel the list. They act on whatever the ring shows and do nothing while the ring is hidden.

**Weapon release.** These buttons release weapons and have no cover or confirmation, by decision for now. POINT SEARCH, SELECT TARGET and FIRE are the same Multifunctional short press, so while George tracks a target with a weapon assigned and no list is shown they all mean "fire". SELECT TARGET and the list buttons are meant to be used only while the Target List is on screen.

**Ring commands always start with Hide.** The bridge cannot read the state of the ring (George has no DCS-BIOS entry), so a ring command must not depend on it. The ring is opened and closed by two separate keys, Show and Hide, and Hide only acts while the ring is shown. A ring command is therefore Hide, Show, direction, Hide (`george_ring` in `aircraft/ah64d.py`): after Hide the ring is closed whatever it was before, Show opens it in a known state, the direction key acts on it, and the last Hide closes it again. PHS SEARCH, WEAPON NEXT and ROE HOLD / FREE leave out the last Hide. Pauses: 0.5 s after the first Hide (`GEORGE_HIDE_PAUSE`), 1.0 s after Show (`GEORGE_SHOW_PAUSE`, the ring needs time to open), 0.6 s after the direction (`GEORGE_KEY_PAUSE`); a ring button takes about 2.8 s (3.0 s with the closing Hide), plus the 0.3 s for bringing DCS to the front. AIR AREA SEARCH, POINT SEARCH and PHS SEARCH use the same ring sequence. While it runs the bridge holds the command lock, so no other command is sent in between. The pauses are multiplied by `macro_pause_scale` ([section 3 of the generic spec](../SPEC.md#3-configuration)); if DCS misses keys, raise it to 1.5 or 2 in `config/config.toml`. The log shows one line per step (`step george_show hold 0.15 pause 1.00`, the pause already scaled), so a missed key can be matched to its step.

**Seats.** A button that works in one seat only (`seats`) is greyed in the other, as TAIL WHEEL is on FLIGHT; the bridge refuses it there. In the pilot seat George is the gunner, in the CP/G seat George is the pilot. SHOW RING and HIDE RING work in both seats.

**Grid** (3 rows × 7 columns; `..` = the cell continues the control on its left):

```
       c1        c2        c3        c4        c5        c6        c7
row 1  PHS       AREA      POINT     PREV TGT  SELECT    REQ CTRL  ..
row 2  STORE     STOP      ROE       NEXT TGT  ENGAGE
row 3  WEAPON    SYSTEMS   FIRE      EXIT LIST           SHOW RING HIDE RING
```

**Deliberately not on the page**

- The FLIGHT and COMBAT commands of George as pilot: in the CP/G seat they depend on the ring mode (GND, FLT, H-B, CMBT, DEFN, cycled with Left, short), and the dashboard cannot read the current mode.

Question: Do the GEORGE buttons work in DCS with the new timing (hold 0.15 s, pauses 0.5 / 1.0 / 0.6 s, staggered keys)? Which ones, and does the Target List appear and take PREV / NEXT TARGET, SELECT TARGET, TRACK / ENGAGE, ROE HOLD / FREE, FIRE and EXIT LIST? ([../FIXES.md](../FIXES.md))

## 8. Lamp row

The row of lamps at the top of every page (as on the A-10C and the F-16C). MASTER WARNING (red) and MASTER CAUTION (amber) with `{seat}_` ids are lighted push buttons as in the cockpit: tapping the lamp presses `{seat}_INTL_MWARN_BTN` / `{seat}_INTL_MCAUTION_BTN` (0.3 s). Lamps are display only, except the master lamps.

| View | Lamps |
| --- | --- |
| COCKPIT map | MASTER WARNING (red, `{seat}_MASTER_WARNING_L`, tappable), MASTER CAUTION (amber, `{seat}_MASTER_CAUTION_L`, tappable) |
| Every panel page | MASTER WARNING, MASTER CAUTION (the two master lamps are in the top row of every COCKPIT page) |
| FLIGHT | MASTER WARNING, MASTER CAUTION, ENG 1 FIRE, APU FIRE and ENG 2 FIRE (red, `PLT_ENG_1_FIRE_L`, `PLT_APU_FIRE_L`, `PLT_ENG_2_FIRE_L`), APU ON (green, `PLT_APU_L`) |
| FIGHT | MASTER WARNING, MASTER CAUTION, ARM (amber), SAFE (green), GND ORIDE (amber) |
| MPD, KU | none |
| GEORGE | MASTER WARNING, MASTER CAUTION |

The FIGHT lamps of the two pages (the gunner page lists `CPG_` ids, the pilot page `{seat}_` ids):

| Lamp | DCS-BIOS | Colour |
| --- | --- | --- |
| MASTER WARNING | `{seat}_MASTER_WARNING_L` | red (tappable) |
| MASTER CAUTION | `{seat}_MASTER_CAUTION_L` | amber (tappable) |
| ARM | `{seat}_MASTER_ARM_ARM_L` | amber |
| SAFE | `{seat}_MASTER_ARM_SAFE_L` | green |
| GND ORIDE | `{seat}_GROUND_OVERRIDE_L` | amber |

The gunner page has MASTER WARNING and MASTER CAUTION (`CPG_MASTER_WARNING_L`, `CPG_MASTER_CAUTION_L`, tappable, as above), ARM, SAFE and GND ORIDE (the colours of the pilot page). The AH-64D has two master lamps, unlike the A-10C and the F-16C, which have MASTER CAUTION only.

Question: Are the lamp colours APU ON (green), ARM (amber), SAFE (green) and GND ORIDE (amber) right in DCS? ([../FIXES.md](../FIXES.md))

## 9. Keybinds

The default keybinds of the AH-64D are in `KEYS` in `aircraft/ah64d.py`. How `[keys]` in `config/config.toml` overrides them, and the key format, are in [section 3 of the generic spec](../SPEC.md#3-configuration). The bridge requires only the keys the controls use: the `power_*` keys because the AH-64D has `lever` controls, `trim_reset` because it has a trim display (E3, E4).

| Key name | Default | DCS command | Used on |
| --- | --- | --- | --- |
| `power_left_idle`, `_up`, `_down`, `_off` | `RAlt+Home`, `RAlt+PageUp`, `RAlt+PageDown`, `RAlt+End` | power lever 1 | FLIGHT, POWER |
| `power_right_idle`, `_up`, `_down`, `_off` | `RShift+Home`, `RShift+PageUp`, `RShift+PageDown`, `RShift+End` | power lever 2 | FLIGHT, POWER |
| `canopy` | `LCtrl+C` | Open/Close Cockpit Door | COCKPIT map (CANOPY key, pilot) |
| `monocle` | `I` | IHADSS show | FLIGHT |
| `controls_overlay` | `RCtrl+Enter` | Show controls indicator | FLIGHT |
| `trim_reset` | `LCtrl+T` | Trimmer reset | FLIGHT (trim display; the bridge watches the key) |
| `george_show` | `LCtrl+LAlt+G` | George AI - Show/Hide | GEORGE |
| `george_hide` | `LCtrl+LAlt+H` | George AI - Hide (AH-64D George AI Helper) | GEORGE |
| `george_up`, `_down`, `_left`, `_right` | `LCtrl+LAlt+I`, `K`, `J`, `L` | George AI - Up, Down, Left, Right (AH-64D George AI Helper) | GEORGE |
| `george_multi` | `LCtrl+LAlt+M` | George AI - Multifunctional Input (Center) | GEORGE |
| `george_store` | `LCtrl+LAlt+T` | George AI - TADS Store Target | GEORGE |
| `george_request` | `LCtrl+LAlt+R` | Request Aircraft Control | GEORGE |

The power lever keys move one lever each, the left lever with `RAlt`, the right one with `RShift` (Power levers, section 2).

### Binding the George keys in DCS

The keys are the `george_*` entries of `KEYS`. Bind them once under Options, Controls: choose the aircraft in the dropdown, double-click the row of the command and press the keys. They are added to the DCS defaults (`LCtrl+V`, `W` `A` `S` `D`), which keep working. `LCtrl+LAlt` was chosen because no DCS default uses it, it is not an AltGr combination, and unlike Ctrl+Shift it does not switch the Windows keyboard layout. Request Aircraft Control already has plain `C` by default; the added key avoids a stray plain C.

| DCS aircraft entry | Command | Key |
| --- | --- | --- |
| AH-64D Pilot and AH-64D CPG | George AI - Show/Hide | `LCtrl+LAlt+G` |
| AH-64D Pilot and AH-64D CPG | George AI - Multifunctional Input (Center) | `LCtrl+LAlt+M` |
| AH-64D Pilot only | George AI - TADS Store Target | `LCtrl+LAlt+T` |
| AH-64D CPG only | Request Aircraft Control | `LCtrl+LAlt+R` |
| AH-64D George AI Helper | George AI - Hide | `LCtrl+LAlt+H` |
| AH-64D George AI Helper | George AI - Up / Down / Left / Right | `LCtrl+LAlt+I` / `K` / `J` / `L` |

Question: Are the CP/G power lever keys (`RAlt` / `RShift` with `Home`, `PageUp`, `PageDown`, `End`) right in the CP/G seat? They are tested in the pilot seat only. ([../FIXES.md](../FIXES.md))

## 10. Engine behaviour for the AH-64D

The engine changes of [../A10C/ENGINE.md](../A10C/ENGINE.md) (E1 to E10) and [../F16C/ENGINE.md](../F16C/ENGINE.md) (F1 to F8) as they apply to this aircraft, and the engine features that exist because of the AH-64D; the engine changes this aircraft needed and their decisions are in [ENGINE.md](ENGINE.md). One bullet each; the details stay in the engine spec [../SPEC.md](../SPEC.md).

- **E1 Aircraft choice.** `aircraft/ah64d.py` has `NAME = "AH-64D"`, `DCS_NAMES = ["AH-64D_BLK_II"]` and `DCSBIOS_MODULE = "AH-64D"`. The bridge reads `_ACFT_NAME` from the DCS-BIOS stream and switches to the AH-64D file when it reads `AH-64D_BLK_II`; the page reloads its layout ([../SPEC.md](../SPEC.md) section 9). `[dcs] aircraft = "auto"` is the default and `"AH-64D"` forces this aircraft; the settings page has an AH-64D button in its AIRCRAFT switch.
- **E2 Seats.** Two seats: `SEATS = [{"prefix": "PLT", "label": "PILOT"}, {"prefix": "CPG", "label": "CP/G"}]` and `SEAT_OUTPUT = "SEAT_POSITION"` (0 pilot, 1 CP/G). The badge shows the seat, a long hold on it is the debug seat, a view or a control has its own `seats`, and the bridge refuses commands outside them ([Seats](#seats)).
- **E3 Trim.** `TRIM_SWITCH = "{seat}_CYCLIC_TRIM_UD"` and `TRIM_RELEASED = 2`: the trim display and the trim tracking exist, and the `trim_reset` key is required (section 3).
- **E4 Power levers.** Two `lever` controls, `power_left` and `power_right` (on FLIGHT `flight_power_left` and `flight_power_right`), read back from `{seat}_ENG_L_PW_LVR` and `{seat}_ENG_R_PW_LVR` and moved by the eight `power_*` keys, which are required for this reason (Power levers, section 2). The fourth position LOCKOUT is greyed out.
- **E5 Displays.** The hand-drawn layouts `mpd` (the two MPDs and the TEDAC, one at a time; the controls carry `side` L, R or T and a `slot`) and `ku` (sections 5 and 6). The COCKPIT map boxes MPD L, MPD R, TEDAC and KU are `links` that open these tabs.
- **E6 Look.** The default plate look `ah64d` of the panel kit (section 11); the AH-64D file passes no `look`.
- **E7 Export script.** The table of `AH-64D_BLK_II` holds the cockpit arguments of the stick and pedals (`CONTROL_NAMES`: `plt_cyc_pitch`, `plt_cyc_roll`, `plt_coll`, `plt_pedals` and the same with `cpg_`) and the MPD indications (`MPD_INDICATIONS = (7, 9, 11, 13)`, `MPD_SEATS = {0: (7, 9), 1: (11, 13)}`); see Reading in What DCS allows below.
- **E8 Keys.** `KEYS` has 21 entries (section 9): the 8 `power_*` keys, `canopy`, `monocle`, `controls_overlay`, `trim_reset` and the 9 `george_*` keys. Controls of the types `key` (canopy, monocle, controls overlay) and `macro` (GEORGE) use them; no key hat and no bar. Every key is already in the key table of `core/keys.py`.
- **E9 Memory and docs.** The remembered tab (the view name) and the MPD side are stored per aircraft in the browser; this spec and the README aircraft section describe the AH-64D.
- **E10 Scroll page.** None: every one of the 21 panel pages fits the 640 × 600 du budget (section 2). The page list of the long hold lists the pages of the current seat (11 pilot, 10 CP/G; it scrolls inside its card, F1 of the F-16C).
- **F2 Coverage check.** `core/tools/test/coverage.py --docs docs/AH64D` takes its page-to-panel table from the `Panels:` line of every page block of section 2. The tabs (FLIGHT, FIGHT, MPD, KU, GEORGE) have no such block and are not covered.

Engine features that exist because of the AH-64D:

- **Guards and real covers.** A `guard` control needs its tablet cover lifted first; the bridge opens a 5 s window for that id only, refuses the command outside it (`refused: guard closed`) and, for a control with a `cover` property, opens and closes DCS's own cover (section 2, Guarded controls; [../SPEC.md](../SPEC.md) section 8).
- **Confirmed presses.** The bridge holds a push button until DCS-BIOS shows it pressed, a hat until its axis shows the direction and a selector until the readback shows the new position, and answers `confirmed` true, false or null ([../SPEC.md](../SPEC.md) section 5).
- **Locked controls.** A control with `requires` is refused while the other control is not in its position: the APU button needs its cover `PLT_APU_BTN_CVR` open (`locked: open the cover first`).
- **Macros.** A `macro` control sends a fixed key sequence under the command lock, the pauses scaled by `macro_pause_scale`: the GEORGE buttons (section 7; [../SPEC.md](../SPEC.md) section 8).
- **Digital stick.** A `stick` control with the flag `digital` sends 2 / 0 / 1 per axis with a dead zone of 30 % (`STICK_DIGITAL`): the TKR pad; the cursor pad is the analog `stick` (section 5).
- **`bios`, `value` and `rest` button fields.** Several buttons act on one multi-position switch: IAT, OFS and OFS ALL on `CPG_LHG_TEDAC_L_IAT` (section 4).
- **Step fallback.** A selector with `step_fallback` turns the knob with INC / DEC steps if the position is not reached in 0.5 s: the MPD and TEDAC MODE knobs (section 5).
- **Displays of several ids.** A `display` with `ids`, `page` and `pages` shows several DCS-BIOS strings: the 14 EUFD lines and the CMWS status (section 2).
- **One FIGHT tab per seat.** Two views named Fight, one with `"seats": [0]` and one with `"seats": [1]`; the tab opens the one of the current seat (section 4).
- **One tab per view name.** The tab bar has one tab per view name, a tab opens the view of that name whose `seats` contain the current seat, and the remembered tab is the name ([Seats](#seats)).

### What DCS allows for the AH-64D

The result of the research phase, on Windows with the AH-64D, both seats, cold and dark and in flight. The original research scripts and their full result tables are kept in git under the tag `research-v1`.

The generic findings (DCS-BIOS stream format, keypresses, the blocklist) are in [section 4 of the generic spec](../SPEC.md#4-what-dcs-allows).

**Reading**

- **DCS-BIOS** (multicast stream) delivers switch positions, button states, lamps, levers and text for both seats: master caution and warning, engine and APU lamps (including lamp test and fire test), startup switches, power lever positions, armament buttons and lamps, weapons action and sight select hats, flare and chaff buttons, force trim, KU scratchpad, the 14 EUFD lines, the CMWS counts, the current seat (`SEAT_POSITION`: 0 pilot, 1 CP/G). The `AH-64D.json` control list has 562 controls with inputs (273 pilot, 284 CP/G, 5 radio frequencies).
- **Export script** (Lua, runs inside DCS next to DCS-BIOS, sends UDP to `127.0.0.1`; every call is wrapped in `pcall`, and it chains the existing export hooks so DCS-BIOS keeps working). It sends plain text, one `name=value` per line, from its table for the aircraft name `AH-64D_BLK_II`:
  - the actual control positions at 10 Hz as cockpit arguments: pilot cyclic pitch 470, roll 471, collective 474, pedals 476; CP/G 472, 473, 475, 478 (`plt_cyc_pitch`, `plt_cyc_roll`, `plt_coll`, `plt_pedals`, `cpg_…`);
  - the MPD page text: `list_indication` works for the Apache and gives named text fields (`PB<n>` and others). Only the displays of the occupied seat update. Index map: 7 and 9 pilot MPD left and right, 11 and 13 CP/G MPD left and right (only these four are sent, at 4 Hz).
- **Not usable or limited:** the generic engine values of DCS's export functions do not fit the Apache (`RPM` is NG %, temperature is always 0; TGT, torque, NP and NR exist only in the MPD ENG page text while that page is shown). Indicated airspeed is implausible at low speed. The DCS-BIOS radio strings are unreliable (HF stuck at a start value); the EUFD lines carry the radio frequencies.

**Controlling**

- **DCS-BIOS commands** (UDP to 127.0.0.1, one line per command, `IDENTIFIER VALUE`, for example `PLT_MASTER_IGN_SW 1`) work for most cockpit controls and have a readback. 227 of the 273 pilot controls and 238 of the 284 CP/G controls passed an automatic sweep (every position, readback within 0.5 s, original position restored); the blocklisted controls were skipped.
- **Power levers:** DCS-BIOS does not move them past the OFF detent, and keys for both levers together do not work. They move by keypress, one key per lever: RAlt (left) or RShift (right) with Home = IDLE, PageUp = one step up, PageDown = one step down, End = OFF. DCS-BIOS reads back 0 OFF, 16383 IDLE, 58981 FLY after each key.
- **Canopy:** DCS-BIOS cannot move it; a key (`canopy`) with the readback `PLT_CANOPY` does.
- **Cockpit logic still applies.** A command that the cockpit would not accept fails without an error: the APU button only works with its cover open; master ignition EXT PWR needs ground power; rotor brake BRK needs conditions; NVS mode FIXED needs the NVS on; push buttons under a DCS cover (fire buttons, CMWS jettison) are ignored while DCS's own cover is closed; ICS mode and the M4 safety need about 3 s to take the position; the CP/G manual tracker position 2 is spring-loaded.
- **Did not work:** the canopy (both seats), CP/G stick fold, MPD mode knobs by a direct command (the bridge uses INC / DEC steps), processor select, TADS select, SAI cage and pitch trim, CP/G left MPD L1–L6. Not followed up; the dashboard does not need them or works around them.
- **George** (the AI crew member and its Helper Interface ring) has no DCS-BIOS entry and works by keypress only (the DCS defaults are `LCtrl+V` and `W` `A` `S` `D`), and only with electrical power. The dashboard reaches it from the GEORGE tab with its own keys ([section 7](#7-george)); the ring state and mode cannot be read.

### Touch sizes per view

The 56 px rule of the [design rules](../SPEC.md#design-rules) holds for every view. Measured with `core/tools/test/sweep.js` (AH-64D, both seats, 1180 × 820 and 1024 × 768); the table gives the smallest touch target of each view in CSS pixels (width × height, the smaller of the two seats), the settings gear left out (own row).

| View | At 1180 × 820 | At 1024 × 768 | Smallest element | Status |
| --- | --- | --- | --- | --- |
| COCKPIT map | 263.5 × 64.7 | 224.5 × 57.3 | CANOPY button (pilot map) | meets 56 px |
| Panel pages | 56 × 62.3 | 56 × 56 | rocker half EUFD WCA (1180); IHADSS BRT mark and touch squares such as CKT A (1024) | meets 56 px |
| FLIGHT | 142.6 × 189.7 | 120.3 × 172.3 | CTRL IND | meets 56 px |
| FIGHT, pilot | 142.6 × 83.3 | 120.3 × 74.7 | FLARE SQUIBS (ARM / SAFE) | meets 56 px |
| FIGHT, CP/G | 99 × 52.9 | 84.2 × 47.1 | hat buttons WAS, SIGHT SEL, TADS FOV; the SENSOR selector is 309.1 × 54.2 and 264.6 × 48.4 | open |
| MPD | 56 × 45.6 | 56 × 39.8 | the FCR, WPN, VID and COM keys, L6 and R6 (at 1024 also R1 and \*) | accepted exception |
| TEDAC | 188 × 56 | 188 × 56 | the LEFT MPD side switch; every TEDAC key and rocker is 56 or more | meets 56 px |
| KU | 66.5 × 56 | 61.5 × 56 | key A | meets 56 px |
| GEORGE | 142.6 × 189.7 | 120.3 × 172.3 | PHS SEARCH | meets 56 px |
| Settings | 92.3 × 56 | 92.3 × 56 | BACK | meets 56 px |
| Settings gear (every view) | 44 × 44 | 44 × 44 | the gear | accepted exception |
| Chooser, knob bar, page list | 56 × 56 | 56 × 56 | close button of the knob bar (chooser buttons 64 × 64, page list CLOSE 101.4 × 56) | meets 56 px |
| Tab bar, badge, lamp row | 85.5 × 56 | 85.5 × 56 | the CP/G badge; tabs 124 × 56; lamps 186 × 56 (1180) and 160 × 56 (1024) | meets 56 px |

- **MPD.** The hit area of an MPD key is 56 px wide; its height is limited by the neighbouring keys (about 0.7 of the button spacing, as on the real bezel), so it falls to 39.8 px at 1024 × 768. The side switch above the display is 56 px high.
- **Open: CP/G FIGHT.** The hats WAS, SIGHT SEL and TADS FOV and the SENSOR selector each take one grid row and two columns, which is below 56 px high. The 7 × 3 grid has no room for two-row hats; see [FIXES.md](../FIXES.md).
- **POWER, APU cover open.** The open cover is 103.8 × 56 px at 1180 × 820 and 95.2 × 56 px at 1024 × 768.

## 11. AH-64D look

The AH-64D panel pages are drawn in the look `ah64d`, the default of the panel kit (E6, [../SPEC.md](../SPEC.md) section 7); the A-10C and the F-16C have looks of their own. The pages were drawn from the owner's cockpit photos and the manual figures named in the `Picture` lines of section 2 (the photos are not in the repository); what follows describes what they show, nothing is copied. The arrangement and the text follow the photos; the places where they deliberately do not are the `Decided` lines of section 2 and the list "Deviations to look at on the tablet" in [../FIXES.md](../FIXES.md).

- **Plates:** one plate per physical panel, dark grey and flat (fill `#26292c`, border `#3d4348`, border 3 du, corner radius 6 du), with the panel name printed in capitals at the top (`TITLE`, 32 du). Several panels on one page are separate plates, 16 du apart on shared edge lines (ARMAMENT, CMWS, CENTER). Four identical rectangular corner ears per plate (52 × 52 du, fill `#33373b`, border `#474e54` 2 du), flush in the plate corners, each with one slotted screw (`SCREW_L`, 26 du across) in its centre; the slot angle comes from the fixed list 15, 100, 65 and 140 degrees by position index. The photos show ears of different heights, some overlapping their neighbours; the screw alignment has priority, so all four ears are equal. Small marks printed on some plates (the `+` of the photos) are `SMALL` text.
- **Labels:** white stencil-style placard capitals in four styles, `TITLE` 32 du, `NAME` 24 du, `POS` 20 du and `SMALL` 16 du, one font and one weight per style; a label hangs at a part (above, below, left or right, 8 du gap), the position labels of toggles, rotaries and knobs come from fixed presets, and the printed brackets (SOL, AUX on COMM) and the vertical rule (EXT / INTR LT) are drawn as on the photos.
- **Toggles and rotaries:** toggle switches with a ring of 56 du and a lever of 40 du; rotary selectors (MSTR IGN, CMWS PWR, the wiper dial) with a ring of ticks of 100 du and a dark knob of 72 du; the CMWS threat dial of 112 du carries its four orange sectors and the letters D and R.
- **Knobs:** one drawing for every knob of a panel page (`knobFace`): soft shadow, dark rim, a grip ring of 24 ridges, a cap with a highlight at the upper left and a raised pointer that turns by the sweep of the control; a knob of 44 du radius or more has a second rim. Grey for the knobs, dark for the rotary selectors. Sizes 96, 72 and 56 du (`KNOB_L`, `KNOB_M`, `KNOB_S`).
- **Buttons:** square push buttons with a bezel of 84 du and a face of 60 du, in a white frame of 100 du where the panel has one (GUARD, XPNDR, TAIL WHEEL, A/S, GND ORIDE, PRI, RES); round buttons of 64 du (DEFOG, IDENT, PRESS TO TEST, the ACM cap); the JETT plunger of 100 du; the four flat EUFD keys of 56 du with a drawn symbol; the EUFD rockers of 52 × 120 du; the PULL chips of 64 × 22 du under the COMM knobs.
- **Levers and sliders:** the power levers and FRICT are a slot around a grip of 40 du (the slot 8 du larger on every side), FRICT a slot of 56 × 240 du.
- **Covers and hazard marks:** a guarded part has the cover of the engine (part plus 12 du on every side, a hazard-striped frame 14 du wide, a padlock of 24 du); the JETT plunger, the EMERG HYD button and the CMWS JETTISON switch sit on a hazard pad (part plus 20 du on every side, yellow and white stripes at 45 degrees); the three fire buttons sit in dark housings with a hazard strip of 32 du; the APU button has a plain hinged flap.
- **Lamps and displays:** lamps are drawn in the face of their button with the legend printed on it (UNLOCK, ON, ARM, SAFE, FIRE, RDY, DISCH) and light up amber or green as the cockpit shows (the manual's yellow FIRE lights are drawn amber); the CMWS threat sectors are orange, bright and dim. Displays are a dark glass (`#121a16`) with green text (`#50dc5c`): the 14 EUFD lines and the CMWS status.
- **MPD, TEDAC and KU:** not panel pages: drawn 1:1 after photos in the page itself (sections 5 and 6): variable action buttons light grey with a green dot, fixed action buttons black with green text, labels and the scratchpad in MPD green.
- **Same mechanics:** touch areas, chooser, knob bar, guard covers and the panel-kit layout rules stay those of the engine; only the drawing of the plates and the parts is the AH-64D's.

## 12. Not on the dashboard

Left off on purpose, one line each. The PANELS.md inventory has 252 rows ([PANELS.md](PANELS.md); [BIOS.md](BIOS.md) gives each row its identifier). 177 rows have at least one identifier on a page or a tab; 50 rows have identifiers and none of them is on the dashboard; 25 rows have no DCS-BIOS identifier (4 keybind, 4 export, 17 no entry). The other 75 rows have no control on any page or tab and are described below: 11 in panels and groups, 18 in the instruments, 5 display contents, 41 hand controls. Every control of a panel that has a page is on its page (section 2); the one panel page with rows left off is CENTER (the four standby altimeter rows).

**Panels and groups**

- **Canopy Jettison Handle (p. 109)** (pilot; the CP/G has one on p. 124 and a third handle is outside for rescue crews): no DCS-BIOS identifier; N/I in the manual. Its safety pin and stowage slot (the Canopy Jettison Handle Pin of the console fittings) are labels in the figures only.
- **Processor Select Panel (p. 127)** (CP/G; `CPG_PROCESSOR_SP_1_L`, `CPG_PROCESSOR_SP_2_L`, `CPG_PROC_SEL_SW`): the whole panel is N/I in the manual and the select did not work in DCS.
- **Items named only in the pilot overview figure (pp. 104 and 394)**: the Boresight Reticle Unit (BRU) and the Data Transfer Unit (DTU) receptacle have no DCS-BIOS entry. The Anti-Torque Pedals have no control either: the pedal position comes from the export script and is the pedal bar of the trim display (FLIGHT).
- **Console fittings named only in the overview figures (pp. 125 and 127)** (utility light, canopy jettison handle pin, first aid kit, HDU storage holster): labels only, no description and no entry; stowage.
- **Display content**: the MPD pages and their label shapes (MPD screen, Menu page, Variable Action Button label styles of the MPD (p. 164)) are no controls; only the button labels are shown on the MPD tab (export script), not the pages. The TDU screen (p. 129) is not drawn. The warning, caution and advisory texts of the EUFD (pp. 158 to 163) are shown as the 14 lines of the EUFD page. The Display Prompt of the KU (p. 113) has no DCS-BIOS entry; the KU tab shows the scratchpad.
- **Hand controls (cyclic and collective grips, TEDAC handgrips)** are not panel pages; what is and what is not on FLIGHT, FIGHT and the MPD tab is under Controls.

**Instruments (not drawn).** The gauge rows of these sections are not panel pages and the flight instruments are not drawn (cockpit-replica graphics are out of scope, [../SPEC.md](../SPEC.md) section 11). The second column says how many rows the section has and how many of them are on the dashboard. Rows without an identifier are fixed scales.

| Instrument | Rows (on the dashboard) | DCS-BIOS ids not drawn |
| --- | --- | --- |
| Standby Magnetic Compass (p. 105) | 1 (0) | `PLT_STANDBY_COMPASS_HDG`, `PLT_STANDBY_COMPASS_PITCH`, `PLT_STANDBY_COMPASS_BANK` |
| Standby Attitude Indicator (SAI) (p. 110) | 9 (0) | `PLT_SAI_POINTER`, `PLT_SAI_PITCH`, `PLT_SAI_BANK`, `PLT_SAI_BALL`, `PLT_SAI_TURN`, `PLT_SAI_FLAG`, `PLT_SAI_CAGE`, `PLT_SAI_PITCH_TRIM` |
| Standby Airspeed Indicator (p. 111) | 2 (0) | `PLT_IAS_NEEDLE` |
| Standby Altimeter (p. 111) | 5 (1) | `PLT_ALT_NEEDLE`, `PLT_ALT_1000`, `PLT_ALT_10000`, `PLT_ALT_PRESS_1`, `PLT_ALT_PRESS_10`, `PLT_ALT_PRESS_1100` |
| Free Air Temperature Gauge (p. 120) | 2 (0) | `PLT_FREE_AIR_TEMP` |

The one control of these instruments on the dashboard is the barometric setting knob ALT SET (`PLT_ALT_SET_KNB`) on CENTER. The SAI cage (`PLT_SAI_CAGE`) and pitch trim (`PLT_SAI_PITCH_TRIM`) did not work in DCS. The CP/G page of the manual lists none of these instruments.

**Controls.** The grips are described by what is on the dashboard and what is left off. The weapon and laser triggers, CHOP, BUCS and emergency jettison are never on the dashboard; the other controls are left out because nobody asked for them, and could go into free cells later.

- **Cyclic Grip (p. 136)** (both seats). On the dashboard: WAS (FIGHT), Symbology Select (FLIGHT), Flare and Chaff (FIGHT), the R / D axis of the Force Trim switch (read for the trim display). Left off: the AT / AL axis of the Force Trim switch (`{S}_CYCLIC_TRIM_LR`); the depress of the Symbology Select (`{S}_CYCLIC_SYMBOLOGY_PRESS`); PTT/RTS (`{S}_CYCLIC_RTS`, `{S}_CYCLIC_RTS_PRESS`); FMC Release (`{S}_CYCLIC_FMC_RELEASE`); the Cage Button (`{S}_CYCLIC_ATA_CAGE`, no function); the Weapon Trigger (`{S}_CYCLIC_TRIGGER`: on the blocklist, it releases weapons).
- **Collective Flight Grip (p. 138)** (both seats, all 9 rows left off). Emergency Jettison (`{S}_COLLECTIVE_JETTISON`, blocklist `JETT`), Engine Chop (`{S}_COLLECTIVE_CHOP`, blocklist `CHOP`, N/I) and the BUCS Trigger (`{S}_COLLECTIVE_BUCS`, blocklist `BUCS`, N/I, CP/G only): grip controls with guards, never on the dashboard. Not asked for: Boresight/Polarity (`{S}_COLLECTIVE_BS_PLRT`), Searchlight (`{S}_COLLECTIVE_SEARCHLIGHT`), Searchlight Position (`{S}_COLLECTIVE_SEARCHLIGHT_UD`, `{S}_COLLECTIVE_SEARCHLIGHT_LR`), NVS Select (`{S}_COLLECTIVE_NVS_SELECT`), Stabilator Control (`{S}_COLLECTIVE_STAB_CONTROL`, `{S}_COLLECTIVE_STAB_RESET`). The Tail Wheel Lock/Unlock Button (`{S}_COLLECTIVE_TAIL_WHEEL`) is the TAIL WHEEL button of the TAIL WHEEL / NVS page and FLIGHT.
- **Collective Mission Grip (p. 140)** (both seats). On the dashboard: the Cursor Controller and the Cursor Display Select Button (MPD tab), the Sight Select Switch (pilot FIGHT). Left off: the FCR Mode Switch (`{S}_COLLECTIVE_FCR_MODE_UD`, `{S}_COLLECTIVE_FCR_MODE_LR`), the FCR Scan Size Switch (`{S}_COLLECTIVE_FCR_SCAN_SIZE_UD`, `{S}_COLLECTIVE_FCR_SCAN_SIZE_LR`), the FCR Scan Switch (`{S}_COLLECTIVE_FCR_SCAN`), the Cued Search Button (`{S}_COLLECTIVE_CUED_SEARCH`, N/I), the Missile Advance Button (`{S}_COLLECTIVE_MISSILE_ADVANCE`), the Alternate Cursor Enter Trigger (`{S}_COLLECTIVE_ALT_CURSOR_ENTER`: the ENTER button of the cursor group does the same). The CP/G sight select of this grip (`CPG_COLLECTIVE_SIGHT_SELECT_UD`, `CPG_COLLECTIVE_SIGHT_SELECT_LR`) is not used: the gunner page uses the right-grip hat.
- **TEDAC Left Handgrip (p. 131)** (CP/G). On the dashboard: IAT / OFS / OFS ALL, the TADS FOV hat, the TADS Sensor Select. Left off: the Weapon Action Switch (`CPG_LHG_WPN_UP_DN`, `CPG_LHG_WPN_L_R`: left out on purpose, it does the same as the cyclic WAS), Store/Update (`CPG_LHG_STORE_UPDATE`), the FCR Mode Switch (`CPG_LHG_FCR_UP_DN`, `CPG_LHG_FCR_L_R`), the Cursor Controller/Enter (`CPG_LHG_CURSOR_UP_DN`, `CPG_LHG_CURSOR_L_R`, `CPG_LHG_CURSOR_ENT`: the collective cursor ids move the cursor), the Cursor Display Select Button (`CPG_LHG_LR_BTN`), the FCR Scan Switch (`CPG_LHG_FCR_SCAN`), the Cued Search Button (`CPG_LHG_CUED_SEARCH`, N/I), the LMC Button (`CPG_LHG_LMC`). Without an identifier: the Weapon Trigger (keybind only, kept on the real grip so a tablet tap never fires a weapon), the Video Record Button (N/I, no entry), the Cage Button (no function, no entry).
- **TEDAC Right Handgrip (p. 134)** (CP/G). On the dashboard: the Sight Select Switch, the Sight Slave Button, the Sight Manual Tracker (TKR). Left off: the FCR Scan Size Switch (`CPG_RHG_FCR_SCAN_UP_DN`, `CPG_RHG_FCR_SCAN_L_R`), the C-SCOPE Button (`CPG_RHG_C_SCOPE`), the FLIR Polarity Button (`CPG_RHG_FLIR_POL`), the Laser Tracker Switch (`CPG_RHG_LASER_TRACK`), the Image Auto Track Polarity Switch (`CPG_RHG_IAT_POL`, N/I), the Display Zoom Button (`CPG_RHG_DISP_ZOOM`), the Cursor Enter Button (`CPG_RHG_ENTER`: the ENTER button of the cursor group does the same), the Heads-Down Display Button (`CPG_RHG_HDD_SW`, no function); DCS-BIOS also has a spare switch of this grip (`CPG_RHG_SPARE`, no function, no PANELS.md row). Without an identifier, keybind only: the LRFD Trigger (the laser trigger; DCS-BIOS has no entry for it, and it fires the laser), the MTT Track Promote Switch and the Missile Advance Button.

**Controls that did not work in DCS** (the dashboard does not need them or works around them): the canopy `CPG_CANOPY` (both seats; the pilot's canopy moves by the `canopy` key), the CP/G stick fold `CPG_STICK_FOLD`, the MPD mode knobs by a direct command (the bridge uses INC / DEC steps), the processor select, the TADS select, the SAI cage and pitch trim, and the CP/G left MPD buttons L1 to L6 (they are on the MPD tab but do not respond). The controls the manual calls N/I or "no function" and that DCS-BIOS has stay on their pages (section 2).

**Outputs and toggles (DCS-BIOS only, 47 rows, none on the dashboard)**

- **Lighting outputs** (`{S}_INT_FLOOD_L`, `PLT_INT_GAUGES_L`, `{S}_INT_PANEL_L`, `{S}_SIGNAL_L`): read-only brightness values; the knobs of EXT / INTR LT and INTR LT give their own position.
- **Sun visors** (`PLT_L_SUNVISOR`, `PLT_R_SUNVISOR`, `PLT_SUNVISOR_L`, `PLT_SUNVISOR_R`): the manual does not cover them.
- **M4 rifle** (`{S}_M4_SAVE`, `{S}_M4_TRIGGER`): stowage in the manual's overview figures; the trigger is on the blocklist, and the safety needs about 3 s to take its position.
- **Canopy and stick fold** (`CPG_CANOPY`, `CPG_STICK_FOLD`, did not work; `{S}_CANOPY_POS`, the canopy position as a gauge): the canopy key reads `PLT_CANOPY`.
- **Spare switch** (`CPG_RHG_SPARE`): DCS-BIOS gives it no function.
- **Vibration gauges** (`VIB_HOOK_SWING`, `VIB_HOOK_TURN`, `VIB_REMOVE`, `VIB_SHEET`, `VIB_SUNSHADE`): not cockpit controls.
- **External aircraft model outputs** (22: `EXT_FORMATION_LIGHTS`, `EXT_GUN_POS_BELT_FEED`, `EXT_GUN_POS_PITCH`, `EXT_GUN_POS_RECOIL`, `EXT_GUN_POS_YAW`, `EXT_LAND_LIGHT`, `EXT_LIGHT_L`, `EXT_LIGHT_R`, `EXT_LIGHT_TAIL`, `EXT_PNVS_POS_YAW`, `EXT_POSITION_LIGHT_LEFT`, `EXT_POSITION_LIGHT_RIGHT`, `EXT_ROTOR`, `EXT_STROBE_L`, `EXT_STROBE_R`, `EXT_TADS_POS_PITCH`, `EXT_TADS_POS_YAW`, `EXT_WIPER_CPG`, `EXT_WIPER_PLT`, `EXT_WOW_LEFT`, `EXT_WOW_RIGHT`, `EXT_WOW_TAIL`): not cockpit controls.
- **Radio frequency strings** (`FM1_RADIO`, `FM2_RADIO`, `HF_RADIO`, `UHF_RADIO`, `VHF_AM_RADIO`): unreliable (HF stays at a start value); the EUFD lines carry the frequencies.
- **Seat** (`SEAT_POSITION`): read by the bridge for the current seat (E2), not a control.

**Ids of rows that are on the dashboard but not used**

- **Power levers:** the finger-lift and detent ids `PLT_ENG_L_PW_LVR_IDLE`, `PLT_ENG_L_PW_LVR_LIFT`, `PLT_ENG_R_PW_LVR_IDLE`, `PLT_ENG_R_PW_LVR_LIFT` (no readback); the levers move by key (E4).
- **Cyclic Grip:** `{S}_CYCLIC_TRIM_LR` and `{S}_CYCLIC_SYMBOLOGY_PRESS` (see Controls).
- **Collective Mission Grip:** `CPG_COLLECTIVE_SIGHT_SELECT_UD`, `CPG_COLLECTIVE_SIGHT_SELECT_LR` (see Controls).
- **CENTER, standby altimeter:** the ids of section 2 (`PLT_ALT_NEEDLE`, `PLT_ALT_1000`, `PLT_ALT_10000`, `PLT_ALT_PRESS_1`, `PLT_ALT_PRESS_10`, `PLT_ALT_PRESS_1100`).

## 13. Manual test run (AH-64D)

Preparation: DCS in windowed or borderless mode, DCS-BIOS and the export script installed, the default keybinds bound. PC and tablet on the same network. A throwaway AH-64D mission, cold and dark. Do the guarded controls last, because several cannot be undone in the mission.

1. **Start.** Run `start_dashboard.bat` (it starts `python core\dashboard.py` and prints the address to open). Open the address on the iPad and add it to the home screen. The badge shows `PILOT`; `NO DCS DATA` appears if DCS is not running. The bridge picks the AH-64D by itself when DCS-BIOS reports `AH-64D_BLK_II`.
2. **COCKPIT start-up sequence** (pilot seat, tablet only). POWER: MSTR IGN BATT, APU cover OPEN, APU, wait for APU ON, ENG 1 START, ENG 1 power lever IDLE, ENG 2 START, ENG 2 power lever IDLE, both power levers FLY. CENTER: PARK BRAKE IN. TAIL WHEEL / NVS: TAIL WHEEL once. Move a few switches in the cockpit with the mouse: the tablet follows.
3. **Pop-ups.** Chooser (NVS MODE, a squelch switch, ENG 1 START, the MSTR IGN dial, the wiper dial): it opens at the switch, shows the positions like the switch, lights the current one, marks the spring-return ones; a tap outside sends nothing. Knobs (EUFD BRT, a radio volume, a light knob): the bar opens next to the knob and the knob follows DCS. COMM: hold a volume knob for 0.6 s, the PULL chip toggles. Power levers and FRICT: tap each mark of both levers, drag the FRICT bar.
4. **Seat switch.** Switch to the CP/G seat (key `2`) while on a pilot-only page (for example CMWS): the page goes to the CP/G COCKPIT map, which has no CMWS, CENTER or EXT LT page. The badge shows `CP/G`. Switch back: the map shows the pilot pages.
5. **Debug seat.** Hold the seat badge for 0.6 s: it reads `DEBUG CP/G` (in the pilot seat), the pages show the CP/G, the FIGHT tab shows the gunner page, and every control is disabled. Hold again: back to `PILOT`. With DCS stopped the cycle is none, `DEBUG CP/G`, `DEBUG PILOT`, none. A reload clears it. On the tablet, check that a finger on the badge works as a long hold.
6. **FIGHT, pilot page.** A/S (the ARM and SAFE lamps change), GND ORIDE once, WAS and SIGHT SEL in each direction (the selection changes in the cockpit), FLARE and CHAFF once each (the counts change; the CMWS must be on and set up).
7. **FIGHT, gunner page and TKR** (CP/G seat). A/S, GND ORIDE, FLARE and CHAFF as above. WAS, SIGHT SEL (right grip: HMD, FCR, TADS, LINK) and SLAVE act in the cockpit. TADS FOV in each direction (Z, N, W, M) and SENSOR FLIR and TV. With a target under the TADS reticle: IAT starts a track, a short OFS drops it or returns the TADS to it, OFS ALL deletes all tracks; note whether IAT really is the forward and OFS the aft position of the grip switch. MPD tab, TEDAC selected: the TKR pad slews the sight in all four directions (note the up / down direction), a small push does nothing (dead zone), releasing the pad stops the slew; LEFT MPD and RIGHT MPD still show the cursor pad.
8. **Trim.** Hold the Force Trim switch and release it: the ring moves to the trim point and the log shows `PLT set`; press the trimmer reset key: `RESET`.
9. **MPD, KU, TEDAC.** MPD: press buttons on both displays; the live labels follow page changes; the cursor pad moves the cursor in the right direction; the MODE knob works (NT through the INC / DEC fallback). KU: type a few characters, the scratchpad shows them. CP/G seat: spot-check the TEDAC buttons, knobs and rockers.
10. **Guarded controls** (last). Station selects light their lamps and toggle back. ENG 1, APU and ENG 2 FIRE: lift the cover, tap once (RDY lamp on, fuel off), lift the cover again and tap again (safe); DCS's own cover opens with the tablet cover, and the log shows `cover open`, `pressed` and about 1 s later `cover closed`, without `not confirmed`. PRI and RES with a fire button armed, JETT with a station armed, ZEROIZE, MASTER ZEROIZE, CMWS JETT.

11. **GEORGE.** Bind the keys in DCS first (the table in [Binding the George keys in DCS](#binding-the-george-keys-in-dcs)). Pilot seat with battery power: SHOW RING and HIDE RING (the ring opens and closes); STOP / TADS FWD (the ring flashes open and closes again, George reacts); WEAPON NEXT (the ring stays open and the weapon label in the ring changes: NO WPN, GUN, MSL, RKT); PHS SEARCH, AIR AREA SEARCH and POINT SEARCH in the air with George not tracking (the ring stays open, a Target List appears when George reports targets; POINT SEARCH needs a TSD point selected); then PREV / NEXT TARGET, SELECT TARGET, TRACK / ENGAGE, ROE HOLD / FREE, FIRE and EXIT LIST on the list; STORE TARGET with a tracked target. CP/G seat: the pilot-only buttons are greyed; REQUEST CONTROL twice, George takes the flight controls, then gives them back.

Done when a cold start to both power levers at FLY works from the tablet alone, the lamps match the cockpit, the CP/G seat shows only its own pages, and every control acts in both seats.
