# Cockpit pages

Spec of the COCKPIT part of Stage 3 ([STAGE3.md](STAGE3.md)): a **COCKPIT** tab that shows a simplified cockpit map, and one page per cockpit panel with every button, switch, knob and display of that panel, as in the real AH-64D.

Status: built and tested in an isolated setup (simulated DCS-BIOS, no real DCS ports, checked in a browser). The real DCS test run is open. AH-64D only; the structure stays reusable for other aircraft.

Fixes after the first test on the tablet (screws, sizes, pop-ups, switch chooser, real covers, back icon): [COCKPIT_FIXES.md](COCKPIT_FIXES.md).

Sources used: the DCS AH-64D Flight Manual (cockpit overview, pages 104 to 127), the DCS cockpit definition (`clickabledata.lua`), the DCS-BIOS module (`AH-64D.lua`, value and position tables) and the Stage 2 results. Controls are named by their DCS-BIOS id; `{S}` stands for `PLT` (pilot) or `CPG` (copilot/gunner).

## Goals

- Learn and operate the aircraft the way the cockpit is laid out: the same panels, the same labels, the same switch positions.
- Quick pages stay for flying and fighting: **FLIGHT** and **FIGHT** keep their mixed layout. A control can sit on a panel page and on a quick page at the same time; both always show the same DCS state, because the tablet shows the readback from DCS and nothing else.
- Every control of a panel is on its page, including the ones that can do harm. Those are protected against accidental taps (see [Guarded controls](#guarded-controls)).

## Navigation

Tabs: **COCKPIT | FLIGHT | FIGHT | MPD | KU**. COCKPIT replaces the old STARTUP tab, which is removed. A STARTUP tab name saved in the browser opens COCKPIT.

- **COCKPIT, tap:** the cockpit map of the current seat. Each box is a panel; tap a box to open its page.
- **On a panel page** the COCKPIT tab reads `◀ COCKPIT`. One tap goes back to the map. It is always in the same place, so no extra button is needed on the page.
- **COCKPIT, long hold (0.5 s):** a list of every page of the current seat, for jumping from page to page without the map.
- The map boxes for the two MPDs, the TEDAC (CP/G only) and the KU open the existing MPD and KU tabs (MPD L, MPD R or TEDAC preselected).
- A page that does not exist in the current seat is not shown (map and list), it is not greyed out. The map follows the seat badge, as the other views do.
- When the seat changes while a panel page is open, the page of the same name for the new seat opens (POWER stays POWER, EMERGENCY stays EMERGENCY). If the new seat has no page of that name (for example CMWS, CENTER or EXT / INTR LT), the COCKPIT map of the new seat opens.
- The MSTR WARN and MSTR CAUT lamps stay in the top row of the map and of every panel page.
- `CANOPY` stays a small key button, on the map.

## Cockpit map

A 12 × 7 grid, `[row, col, rows, cols]`, drawn as plain boxes with the panel placard. Heavily simplified: the order of the real cockpit, none of the detail. The cells are in the tables below.

Pilot (manual page 104 to 121):

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

| Page | Grid (PLT) |
| --- | --- |
| KU | [1,1,1,3] |
| TAIL WHEEL / NVS | [2,1,1,3] |
| EMERGENCY | [3,1,1,3] |
| POWER | [4,1,2,3] |
| STORES JETT | [6,1,1,3] |
| EXT / INTR LT | [7,1,1,3] |
| FIRE DET/EXTG | [1,4,1,3] |
| EUFD | [1,7,1,3] |
| ARMAMENT | [2,4,1,3] |
| CANOPY (key) | [2,7,1,3] |
| MPD L / MPD R | [3,4,3,3] / [3,7,3,3] |
| CENTER | [6,5,2,4] |
| CMWS | [1,10,2,3] |
| COMM | [3,10,3,3] |

CP/G (manual page 123 to 127):

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

| Page | Grid (CPG) |
| --- | --- |
| KU | [1,1,1,3] |
| EMERGENCY | [2,1,1,3] |
| POWER | [3,1,2,3] |
| TAIL WHEEL / NVS | [5,1,1,3] |
| INTR LT | [6,1,1,3] |
| STORES JETT | [7,1,1,3] |
| FIRE DET/EXTG | [1,4,1,2] |
| ARMAMENT | [1,6,1,2] |
| EUFD | [1,8,1,3] |
| MPD L / TEDAC / MPD R | [2,4,3,2] / [2,6,3,2] / [2,8,3,3] |
| COMM | [2,11,2,2] |
| WIPER / DEFOG | [4,11,1,2] |

The CP/G has no CMWS, no EXT LT, no VIDEO, no CHECK OVERSPEED / GENERATOR RESET panel, no PARK BRAKE, no master ignition, no APU, no engine start, no rotor brake. The CP/G wiper and defog are on the right console, on their own page WIPER / DEFOG below COMM; the pilot's are on the instrument panel (CENTER page).

## Naming convention

- **Page name** = the placard of the panel in upper case (`FIRE DET/EXTG`, `STORES JETT`, `TAIL WHEEL / NVS`).
- **Control label** = the text printed on the panel. A rocker is shown as `WCA ▲▼`, a knob by its name (`FLOOD`).
- **Positions** are listed in the order printed on the panel, top to bottom or left to right, with all real positions, also unusable ones (greyed out).
- **Control id** = the DCS-BIOS identifier with the seat as `{S}` (`{S}_FIRE_ENG1_BTN`). A function without a DCS-BIOS entry (keypress) uses a lower-case name from `[keys]` (`canopy`, `power_left`).
- All text in English, as in the cockpit.

## Control properties

Every control is a data entry in `aircraft/ah64d.py` (the generic bridge and page stay free of AH-64D knowledge). Existing properties are kept; the new ones are marked.

| Property | Meaning |
| --- | --- |
| `id` | DCS-BIOS identifier, `{S}` for the seat |
| `label` | placard text |
| `type` | `selector`, `button`, `lever`, `hat` (rocker, one or two axes), `knob`, `key`, `display`, `controls`, `stick` as today |
| `positions` | list of `{value, label}`; `disabled` greys one out; `momentary` marks a spring-return position |
| `rest` | resting value of a spring-loaded switch, and `hold` the press time |
| `lamp`, `legend` | lamp inside the button (read from DCS-BIOS) |
| `requires` | another control that must be in a position first (the APU cover) |
| `seats` | `[0]` pilot, `[1]` CP/G, omitted = both |
| `guard` (new) | `true` for a [guarded control](#guarded-controls) |
| `at` (new) | position and size on the panel drawing, `[x, y, w, h]` in the pixels of the reference photo, scaled like the MPD, TEDAC and KU drawings |
| `lamps` (new, per control) | two lamps on the face of a button, `{id, color, legend}`, upper and lower half (FIRE and RDY on the fire buttons, ARM and SAFE on A/S) |
| `ids` (new, `display` only) | a display made of several DCS-BIOS strings (the 14 lines of the EUFD, the CMWS status) |

Further properties the panel pages use:

| Property | Meaning |
| --- | --- |
| `style` | how a control is drawn: `rotary` (round selector knob with a pointer), `cover` (the APU cover), `slider` (FRICT), `cap` (the ACM cap), `chip` (the PULL chips of the COMM knobs), `plunger` (JETT), `flat` (the EUFD keys) |
| `shape: "round"` | a round button (DEFOG, IDENT, PRESS TO TEST, JETT) |
| `orient: "h"` | a horizontal selector (FIRE TEST, GEN RST, the wiper switch, PARK BRAKE) |
| `sweep` | knob: pointer angles in degrees at the minimum and at the maximum value |
| `angle` | per position of a `rotary` selector: pointer angle |
| `y` / `x` | per position: where its mark is on the drawing, vertical or horizontal; the touch bands are split halfway between the marks |
| `group`, `mark`, `dot` | dual-function knobs: members with the same `group` share one knob, and each member has a selector mark (`mark` for the touch area, `dot` for the dot). IHADSS BRT / CON and FLIR LVL / GAIN work this way |
| `pull` | a knob's pull-to-disable id (the COMM volume knobs); the knob shows as pulled out when it reads 1, and a 0.6 s hold on the knob toggles it |
| `page`, `pages` | `display` with pages: `page` is the id that holds the page name, `pages` lists the ids shown for each name (CMWS) |

Page definition. Panel pages are `VIEWS` entries flagged `"panel": True`, one entry per seat where the seats differ (built by `panel_pages` in `aircraft/ah64d.py`):

```
{"name": "FIRE DET/EXTG", "seats": [1], "panel": True, "layout": "panel", "map": [row, col, rows, cols], "box": [w, h],
 "lamps": [...], "print": [...], "art": [...], "controls": [...], "indicators": [...]}
```

`map` is the cell on the cockpit map. `box` is the size of the drawing in photo pixels. `print` lists the placard text as `[text, x, y, size, width, rotation]`. `art` lists the drawn parts (plate, bracket, screw, slot, glass, line, arrow, path, outline, hazard). `lamps` is the top row with the master lamps. `indicators` (optional, page level) are free lamps drawn on the panel: the CMWS threat sectors and the D and R letters, each with a bright and a dim DCS-BIOS id.

The COCKPIT view (layout `map`) is one entry for both seats. It holds `links` (the map boxes that open the KU, MPD and TEDAC tabs, each with `view`, `side`, `seats` and `map`) and the canopy key. There is no `PANELS` table: the map cell is part of each page. A new aircraft file defines its own.

Controls are placed with `at`, so the page is a 1:1 drawing of the panel with invisible touch areas (56 px or more where the layout allows; the three-position toggle bands are about 40 to 50 px, the PULL chips are smaller) and the knob pop-up bar for knobs.

## Guarded controls

A guarded control can end the flight or cannot be undone in the mission: shut off an engine or the APU (the FIRE buttons stop the fuel flow), discharge an extinguisher bottle (primary and reserve), drop stores (JETT), wipe the radio and crypto data (zeroize), jettison the countermeasure flares. All of them are on the tablet, only on their own panel page (never on FLIGHT or FIGHT), and need two deliberate steps.

1. **Lift the cover.** The control is covered by a red and white hazard-striped frame with a padlock. The middle of the frame is clear, so the lamps and the control underneath stay visible. Tap the cover to lift it. It closes again after 5 seconds, or after the press. Only one cover can be open at a time.
2. **Tap the control.** One tap on the button, or on the position of a guarded switch, sends the command and the cover closes.

The bridge enforces it, so a second tab, a bug in the page or a stale tab cannot bypass it:

- Opening a cover sends `{"id": ..., "guard": "open"}`. The bridge opens a 5 second window for that id only.
- A command for a guarded id is accepted only inside its window, and the window is used up by the press. Otherwise the answer is `refused: guard closed`.
- Every guard event goes into the log: `guard open`, `pressed`, `refused: guard closed`, and for the parts with a real cover `cover open`, `cover closed` and `refused: cover did not open`.
- The press itself uses the existing confirmed press: the bridge holds until DCS-BIOS shows the button, and the page shows the amber not-confirmed hint if it did not arrive.

Where the real cockpit has a cover (FIRE ENG 1, APU and ENG 2, master zeroize, CMWS flare jettison), DCS-BIOS has a cover control (`{S}_FIRE_ENG1_CVR`, `_APU_CVR`, `_ENG2_CVR`, `{S}_INST_MZERO_CVR`, `PLT_CMWS_JETT_CVR`). DCS does not react to the button while its own cover is closed (the first test: ENG 1 FIRE and CMWS JETT were sent but not confirmed). So these controls carry a `cover` property with that id, and the bridge opens and closes DCS's own cover for them. Lifting the tablet cover sets the real cover to 1 and waits up to 0.5 seconds for the DCS-BIOS readback; if it does not open, the answer is `refused: cover did not open` and the tablet cover stays shut. The bridge closes the real cover again about 1 second after the command was accepted, when the 5 second window runs out unused, or at once when another guarded control is lifted. PRI, RES, JETT and ZEROIZE have no cover in DCS-BIOS and only use the tablet cover.

The guarded switches ZEROIZE, MASTER ZEROIZE and CMWS JETT list ON on top and OFF at the bottom.

Controls with `guard`: `{S}_FIRE_ENG1_BTN`, `{S}_FIRE_APU_BTN`, `{S}_FIRE_ENG2_BTN`, `{S}_FIRE_PRIME_EXT`, `{S}_FIRE_RES_EXT`, `{S}_JETT_BTN`, `{S}_EMERG_ZERO_SW`, `{S}_INST_MZERO_SW`, `PLT_CMWS_JETT`. The six station select buttons only arm a station and light up; they are normal buttons, and JETT is guarded.

## Pages

The tables list each control with its DCS-BIOS id, type, positions (value = label), lamp, seats, and the Stage 2 result (`ok` passed, `fail` failed for the reason given, `new` not tested yet because it was blocked then). Values are from DCS-BIOS and the DCS cockpit definition.

### POWER (left console)

Pilot: everything. CP/G: the two power levers only.

| Label | Id | Type | Positions | Lamp | Seats | Stage 2 |
| --- | --- | --- | --- | --- | --- | --- |
| RTR BRK | `PLT_ROTOR_BRK` | selector | 2 OFF, 1 BRK (greyed out), 0 LOCK | | PLT | BRK fail (needs conditions) |
| MSTR IGN | `PLT_MASTER_IGN_SW` | selector | 0 OFF, 1 BATT, 2 EXT PWR (greyed out) | | PLT | EXT PWR fail (no ground power) |
| APU cover | `PLT_APU_BTN_CVR` | selector | 0 CLOSED, 1 OPEN | | PLT | ok |
| APU | `PLT_APU_BTN` | button, `requires` the cover open | press | `PLT_APU_L` ON | PLT | ok, only with the cover open |
| ENG START NO 1 / NO 2 | `PLT_ENG1_START`, `PLT_ENG2_START` | selector, rest 1 | 2 START (momentary), 1 OFF, 0 IGN ORIDE (momentary) | | PLT | ok |
| PWR LVR NO 1 / NO 2 | `{S}_ENG_L_PW_LVR`, `{S}_ENG_R_PW_LVR` | lever (keypress, readback) | OFF 0, IDLE 16383, FLY 58981, LOCKOUT 65535 (greyed out) | | both | keys ok in the pilot seat, DCS-BIOS fail; CP/G keys not tested |
| FRICT | `PLT_PW_LVR_FRIC` | knob | 0 to 65535 | | PLT | ok |

### TAIL WHEEL / NVS

| Label | Id | Type | Positions | Lamp | Seats | Stage 2 |
| --- | --- | --- | --- | --- | --- | --- |
| TAIL WHEEL | `{S}_T_WHEEL_UNLOCK_BTN` | button | press | `{S}_T_WHEEL_UNLOCK_L` UNLOCK | both | ok |
| NVS MODE | `{S}_NVS_MODE` | selector | 2 FIXED, 1 NORM, 0 OFF | | both | FIXED fail (needs the NVS on) |

### EMERGENCY

| Label | Id | Type | Positions | Lamp | Seats | Stage 2 |
| --- | --- | --- | --- | --- | --- | --- |
| GUARD | `{S}_EMERG_GUARD_BTN` | button | press | `{S}_EMERG_GUARD_L` | both | ok |
| XPNDR | `{S}_EMERG_XPNDR_BTN` | button | press | `{S}_EMERG_XPNDR_L` | both | ok |
| ZEROIZE | `{S}_EMERG_ZERO_SW` | selector, `guard` | 0 / 1 (toggle) | | both | new |
| EMERG HYD | `{S}_EMERG_HYD_BTN` | button | press | `{S}_EMERG_HYD_L` | both | ok |

### STORES JETT

| Label | Id | Type | Positions | Lamp | Seats | Stage 2 |
| --- | --- | --- | --- | --- | --- | --- |
| L OUTBD | `{S}_JETT_STORE_LO` | button | press (arms the station) | `{S}_JETT_L_OUTBOARD_L` | both | new |
| L INBD | `{S}_JETT_STORE_LI` | button | press | `{S}_JETT_L_INBOARD_L` | both | new |
| R INBD | `{S}_JETT_STORE_RI` | button | press | `{S}_JETT_R_INBOARD_L` | both | new |
| R OUTBD | `{S}_JETT_STORE_RO` | button | press | `{S}_JETT_R_OUTBOARD_L` | both | new |
| L TIP | `{S}_JETT_STORE_LW` | button | press | `{S}_JETT_L_TIP_L` | both | new |
| R TIP | `{S}_JETT_STORE_RW` | button | press | `{S}_JETT_R_TIP_L` | both | new |
| JETT | `{S}_JETT_BTN` | button, `guard` | press | | both | new |

### EXT / INTR LT

Pilot: both blocks. CP/G: INTR LT only (no STBY INST knob).

| Label | Id | Type | Positions | Seats | Stage 2 |
| --- | --- | --- | --- | --- | --- |
| NAV | `PLT_EXTL_NAV_L_SW` | selector | 2 BRT, 1 OFF, 0 DIM | PLT | ok |
| FORM | `PLT_EXTL_FROMATION_L_KNB` | knob | OFF to BRT | PLT | ok |
| ANTI COL | `PLT_EXTL_ACOL_L_SW` | selector | 2 WHT, 1 OFF, 0 RED | PLT | ok |
| SIGNAL | `{S}_INTL_SIGNAL_L_KNB` | knob | DIM to BRT | both | ok |
| PRIMARY | `{S}_INTL_PRIMARY_L_KNB` | knob | OFF to BRT | both | ok |
| FLOOD | `{S}_INTL_FLOOD_L_KNB` | knob | OFF to BRT | both | ok |
| STBY INST | `PLT_INTL_STBYINST_L_KNB` | knob | OFF to BRT | PLT | ok |
| PRESS TO TEST | `{S}_INTL_TEST_BTN` | button | press | both | ok |

### FIRE DET/EXTG (glareshield)

Both seats. The manual describes the lamps: a yellow FIRE and a green RDY light on each of ENG 1, APU and ENG 2, and a DISCH light on PRI and RES. A fire button press arms the extinguisher for that compartment and shuts off its fuel.

| Label | Id | Type | Positions | Lamps | Stage 2 |
| --- | --- | --- | --- | --- | --- |
| ENG 1 | `{S}_FIRE_ENG1_BTN` | button, `guard` | press (toggles armed / safe) | FIRE `{S}_ENG_1_FIRE_L`, RDY `{S}_ENG_1_READY_L` | new |
| APU | `{S}_FIRE_APU_BTN` | button, `guard` | press | FIRE `{S}_APU_FIRE_L`, RDY `{S}_APU_READY_L` | new |
| ENG 2 | `{S}_FIRE_ENG2_BTN` | button, `guard` | press | FIRE `{S}_ENG_2_FIRE_L`, RDY `{S}_ENG_2_READY_L` | new |
| PRI | `{S}_FIRE_PRIME_EXT` | button, `guard` | press (discharge) | DISCH `{S}_FIRE_EXT_DISCH_PRI_L` | new |
| RES | `{S}_FIRE_RES_EXT` | button, `guard` | press (discharge) | DISCH `{S}_FIRE_EXT_DISCH_RES_L` | new |
| TEST | `{S}_FIRE_DETECT_TEST` | selector, rest 1 | 0 "1" (momentary), 1 OFF, 2 "2" (momentary) | | ok |

### ARMAMENT (and VIDEO, MASTER ZEROIZE)

The pilot page carries the ARMAMENT panel, the MASTER ZEROIZE placard and the VIDEO panel. The CP/G page has ARMAMENT and MASTER ZEROIZE only. MASTER ZEROIZE is a plain placard drawn without a photo. On the VIDEO panel IHADSS BRT / CON share one knob and FLIR LVL / GAIN share one knob; a small mark next to the knob selects the function.

| Label | Id | Type | Positions | Lamp | Seats | Stage 2 |
| --- | --- | --- | --- | --- | --- | --- |
| A/S | `{S}_MASTER_ARM_BTN` | button | press | ARM `{S}_MASTER_ARM_ARM_L`, SAFE `{S}_MASTER_ARM_SAFE_L` | both | ok |
| GND ORIDE | `{S}_GROUND_OVERRIDE_BTN` | button | press | `{S}_GROUND_OVERRIDE_L` | both | ok |
| MASTER ZEROIZE | `{S}_INST_MZERO_SW` | selector, `guard` | 0 / 1 (toggle) | | both | new |
| IHADSS BRT | `PLT_VIDEO_IHADSS_BRT` | knob | MIN to MAX | | PLT | ok |
| IHADSS CON | `PLT_VIDEO_IHADSS_CON` | knob | MIN to MAX | | PLT | ok |
| SYM BRT | `PLT_VIDEO_SYM_BRT` | knob | MIN to MAX | | PLT | ok |
| ACM | `PLT_VIDEO_AUTO_CON` | selector | 0 OFF, 1 ACM | | PLT | ok |
| FLIR LVL | `PLT_VIDEO_FLIR_LVL` | knob | MIN to MAX | | PLT | ok |
| FLIR GAIN | `PLT_VIDEO_FLIR_GAIN` | knob | MIN to MAX | | PLT | ok |

The master zeroize switch sits on the instrument panel next to the armament panel (manual page 105 and 124), so it lives on this page.

### EUFD

| Label | Id | Type | Positions | Seats | Stage 2 |
| --- | --- | --- | --- | --- | --- |
| display | `{S}_EUFD_LINE1` to `_LINE14` | display, `ids` | 14 lines of 56 characters, shown as on the real display | both | readable |
| WCA ▲▼ | `{S}_EUFD_WCA` | hat | 2 up, 1 off, 0 down | both | ok |
| IDM ▲▼ | `{S}_EUFD_IDM` | hat, rest 1 | 2 up, 1 off, 0 down | both | ok |
| RTS ▲▼ | `{S}_EUFD_RTS` | hat, rest 1 | 2 up, 1 off, 0 down | both | ok |
| BRT | `{S}_EUFD_BRT` | knob | DIM to BRT | both | ok |
| P (preset) | `{S}_EUFD_PRESET` | button | press | both | ok |
| ⏎ (enter) | `{S}_EUFD_ENT` | button | press | both | ok |
| ⏱ (stopwatch) | `{S}_EUFD_STOPWATCH` | button | press to start / stop, hold to reset | both | ok |
| ⟳ (swap) | `{S}_EUFD_SWAP` | button | press | both | ok |

### CMWS (pilot only, on the right side of the pilot cockpit)

| Label | Id | Type | Positions | Seats | Stage 2 |
| --- | --- | --- | --- | --- | --- |
| PWR | `PLT_CMWS_PW` | selector, rest 1 | 0 OFF, 1 ON, 2 TEST (momentary) | PLT | ok |
| STATUS | `PLT_CMWS_FLARE_LETTER`, `_FLARE_COUNT`, `_CHAFF_LETTER`, `_CHAFF_COUNT`, `_BIT_LINE_1`, `_BIT_LINE_2`, `_PAGE` | display, `ids`, `pages` | page MAIN `F 60` / `C 30`, page TEST the two test lines, page NONE blank | PLT | in use |
| THREAT lamps | `PLT_CMWS_FWD_LEFT_BRT_L`, `_FWD_RIGHT_`, `_AFT_LEFT_`, `_AFT_RIGHT_`, `PLT_CMWS_D_BRT_L`, `PLT_CMWS_R_BRT_L` (and the matching `_DIM_L`) | lamps | orange, bright and dim | PLT | readable |
| AUDIO | `PLT_CMWS_VOL` | knob | MIN to MAX | PLT | ok |
| LAMP | `PLT_CMWS_LAMP` | knob | MIN to MAX | PLT | ok |
| ARM / SAFE | `PLT_CMWS_ARM` | selector | 1 ARM, 0 SAFE | PLT | ok |
| CMWS / NAV | `PLT_CMWS_MODE` | selector | 1 CMWS, 0 NAV | PLT | ok |
| BYPASS / AUTO | `PLT_CMWS_BYPASS` | selector | 1 BYPASS, 0 AUTO | PLT | ok |
| JETTISON | `PLT_CMWS_JETT` | selector, `guard` | 0 / 1 | PLT | new |

### CENTER (pilot only, instrument panel)

| Label | Id | Type | Positions | Seats | Stage 2 |
| --- | --- | --- | --- | --- | --- |
| CHK OVSP TEST, CKT A | `PLT_CHK_OSPD_ENG_A` | selector, rest 1 | 2 ENG 1, 1 OFF, 0 ENG 2 (spring return) | PLT | ok |
| CHK OVSP TEST, CKT B | `PLT_CHK_OSPD_ENG_B` | selector, rest 1 | 2 ENG 1, 1 OFF, 0 ENG 2 (spring return) | PLT | ok |
| GEN RST | `PLT_GEN_RESET` | selector, rest 1 | 0 GEN 1, 1 off, 2 GEN 2 (spring return) | PLT | ok |
| DEFOG | `PLT_DEFOG_BTN` | button | press | PLT | ok |
| WINDSHIELD WIPER | `PLT_WIPER_SW` | selector | 0 PARK, 1 OFF, 2 LO, 3 HI | PLT | ok |
| PARK BRAKE | `PLT_PARK_BRAKE` | selector | 0 IN, 1 PULLED | PLT | ok |
| ALT SET | `PLT_ALT_SET_KNB` | knob | 0 to 65535 | PLT | ok |

### COMM (right console)

Both seats, one drawing for both. The volume knobs of VHF, UHF, FM 1, FM 2, HF, VCR and ADF have a PULL chip (a `chip` control, the `pull` id of the knob) for the pull-to-disable position. The chips are small (about 16 to 18 px high, the SQL switches need the room); holding the knob for 0.6 s toggles the pull as well (a ring fills during the hold), a short tap on the knob opens the knob bar.

| Label | Id | Type | Positions | Seats | Stage 2 |
| --- | --- | --- | --- | --- | --- |
| VHF, UHF, FM 1, FM 2, HF volume | `{S}_COM_VHF_VOL`, `_UHF_`, `_FM1_`, `_FM2_`, `_HF_` | knob | MIN to MAX | both | ok |
| VHF, UHF, FM 1, FM 2, HF disable (pull) | `{S}_COM_VHF_PW`, `_UHF_`, `_FM1_`, `_FM2_`, `_HF_` | selector | 0 In, 1 Out | both | ok |
| SQL ×5 | `{S}_COM_VHF_SQL`, `_UHF_`, `_FM1_`, `_FM2_`, `_HF_` | selector, rest 1 | 2 ENABLE, 1 off, 0 DISABLE (spring return) | both | ok |
| MASTER | `{S}_COM_MASTER_VOL` | knob | MIN to MAX | both | ok |
| SENS | `{S}_COM_SENS_KNB` | knob | MIN to MAX | both | ok |
| ICS | `{S}_COM_ICS_MODE` | selector | 0 HOT MIC, 1 VOX, 2 PTT | both | passes after 3 s |
| IDENT | `{S}_COM_IDENT_BTN` | button | press | both | ok |
| IFF, RLWR, ATA, VCR, ADF volume | `{S}_COM_IFF_VOL`, `_RLWR_`, `_ATA_`, `_VCR_`, `_ADF_` | knob | MIN to MAX | both | ok |
| VCR, ADF disable (pull) | `{S}_COM_VCR_PW`, `{S}_COM_ADF_PW` | selector | 0 In, 1 Out | both | ok |

### WIPER / DEFOG (CP/G only)

The same drawing as the wiper block of the pilot's CENTER page.

| Label | Id | Type | Positions | Seats | Stage 2 |
| --- | --- | --- | --- | --- | --- |
| DEFOG | `CPG_DEFOG_BTN` | button | press | CPG | ok |
| WINDSHIELD WIPER | `CPG_WIPER_SW` | selector | 0 PARK, 1 OFF, 2 LO, 3 HI | CPG | ok |

### Existing tabs

MPD (left, right, cursor, TEDAC for the CP/G) and KU are unchanged. Their boxes on the map open them.

### Not on a page

- **Processor select panel (CP/G):** the manual marks it not implemented; the DCS-BIOS switch fails the Stage 2 sweep.
- **SAI:** cage and pitch trim fail the sweep; only the altimeter setting knob is used (CENTER).
- **Canopy jettison, M4 rifle, sun visors, stick fold:** not needed.
- **Grip controls with guards** (CHOP, BUCS, emergency jettison, weapons trigger): not part of this change. The cyclic and collective grip controls stay on FLIGHT and FIGHT, without the guarded ones.
- **Radio frequencies:** not on a page, as before.

## What was removed

The STARTUP tab is gone (the `Startup` view is removed from `VIEWS`). Its controls moved to the POWER, TAIL WHEEL / NVS, EXT / INTR LT and CENTER pages and to the map (CANOPY). The MPD L and MPD R mode selectors of the old tab are the MODE knob of each display on the MPD tab. FLIGHT and FIGHT stay as they are, including TAIL WHEEL on FLIGHT and the CMWS controls on FIGHT.

## Speed and load

Measured in the test setup with a simulated DCS-BIOS stream and a tablet polling five times a second: 7.5 KB per reply (about 1 ms), 2 % of one core in the bridge (29 MB), and 0.006 to 0.021 ms per page redraw, on every tab including the 89-control MPD page. The page builds and redraws only the open tab, so the new pages cost no more than the MPD page. With all panel controls the reply grows to about 11 KB. The cost inside DCS (the export script, about 43 MPD text calls per second) was not measured; build step 0 added a timing line for it. The export script writes one `export timing` line per minute of model time to the DCS log (`dcs.log`, source DCS-Dashboard), not to the dashboard log. The updated script has to be copied to the Saved Games Scripts folder again to take effect.

## Build steps

One step at a time, each checked in a browser against a simulated DCS-BIOS (no real DCS ports). All steps are done and checked this way. The test run in DCS after each step is open.

0. **Measure the export script.** Done. The Lua script times its own work and writes one summary line per minute to the DCS log (`dcs.log`, source DCS-Dashboard). Check: the line appears with a number in a DCS run (open).
1. **Map, navigation, panel layout and guard**, with two small pages: TAIL WHEEL / NVS and EMERGENCY (it has a guarded control: ZEROIZE). Done. Includes the `panel` layout with `at` coordinates, the COCKPIT tab (tap, back, long hold list), the bridge guard window and its log lines. Check: map and list per seat, a guarded press only works after the cover is lifted, `refused: guard closed` otherwise, the window closes after 5 s, no scrolling, nothing under the gear.
2. **POWER and EXT / INTR LT.** Done. Check: the cold start still works end to end; every position as in the tables.
3. **FIRE DET/EXTG, ARMAMENT / VIDEO / MASTER ZEROIZE, STORES JETT.** Done. Check: lamps follow the simulated DCS-BIOS, the guard applies to the listed controls and no others.
4. **EUFD (live text), CMWS, CENTER.** Done. Check: the 14 lines render as 56-character rows; CMWS counts match FIGHT.
5. **COMM, and the CP/G WIPER / DEFOG page.** Done. Check: all 12 knobs reachable through the knob bar; the squelch switches are spring return.
6. **Remove STARTUP, update README and STAGE3.md.** Done. The page falls back to COCKPIT for a saved STARTUP tab, and goes to the COCKPIT map when a seat change leaves a page with no page of the same name.

Each step ends with a test run in DCS by the user (open).

## Test run for the guarded controls

These controls were never sent before (they were skipped in Stage 2), so nothing is known about how DCS reacts. Use a throwaway mission, cold and dark, and do these last, because several cannot be undone in the mission:

1. Station selects: each lights its lamp and toggles back.
2. ENG 1 FIRE, APU FIRE, ENG 2 FIRE: lift the cover, tap once (RDY lamp on, fuel off), lift the cover again and tap again (safe). The log shows `cover open`, `pressed` and about 1 second later `cover closed`, and `pressed` is not followed by `not confirmed`.
3. PRI and RES discharge, with a fire button armed.
4. JETT with a station armed.
5. ZEROIZE, MASTER ZEROIZE, CMWS JETT: MASTER ZEROIZE and CMWS JETT open and close their real cover with the tablet cover.

## Open points

- Are the fire buttons confirmed by their own readback once the real cover is open? Still to be tested in DCS (test run, step 2). If ENG 1 is still `not confirmed` with the cover open, the confirmation uses the RDY lamp (`{S}_ENG_1_READY_L`) instead of the button.
- The CP/G power lever keys (`RAlt` / `RShift` with `Home` and so on) are only tested in the pilot seat.
- Lamp colours of the DISCH lights (manual does not say; check in DCS).
- The master zeroize switch has no photo; MASTER ZEROIZE is a plain placard. The CP/G COMM and WIPER / DEFOG pages use the same drawings as the pilot's COMM and CENTER pages. The photos used for drawing the pages are kept outside the repo.
- The FRICT slider direction and the end of the SIGNAL knob sweep were taken from the photo, not from DCS. Check them in DCS.
- The five top-row PULL chips on COMM are small (about 16 to 18 px high) because the SQL switches need the room. Holding the knob for 0.6 s toggles the pull instead; check in DCS that this is comfortable on the tablet.
- The panel pages need a browser with CSS container queries: Safari / iPadOS 16 or newer, or current Chrome.
- Grip controls with guards (CHOP, BUCS, emergency jettison) may follow later with the same guard mechanism.
