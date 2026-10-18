# DCS-Dashboard – AH-64D

The AH-64D part of the specification of the product as built; the engine that all aircraft share is in [SPEC.md](../SPEC.md).

## 1. Seats

- Each view lists the seats it can be used in: FLIGHT, MPD, KU, GEORGE and the COCKPIT map both seats; a panel page lists the one seat it exists for. FIGHT exists once per seat, two views with the same name, one with `"seats": [0]` and one with `"seats": [1]`. A control can also have its own `seats` (TAIL WHEEL on FLIGHT: pilot only) and is greyed in the other seat.
- The tab bar has one tab per view name. A tab opens the view of that name whose `seats` contain the current seat (real or debug); FIGHT opens the pilot page or the gunner page. The remembered tab is the name.
- The header badge shows the current seat: `PILOT` or `CP/G`. It adds ` – READ ONLY` when the shown view cannot be used in this seat: lamps and positions are shown, all controls are disabled.
- When the seat changes, the view of the same name for the new seat opens (POWER stays POWER, FIGHT shows the page of the new seat); if the new seat has no panel page of that name (CMWS, CENTER, EXT / INTR LT) the COCKPIT map of the new seat opens.
- **Debug seat.** A long hold (0.6 s) on the seat badge looks at the pages of the other seat without sitting in it. With a real seat the hold cycles: none, the other seat, none. With no DCS data or with the bridge offline there is no real seat, and the cycle is: none, `CP/G`, `PILOT`, none. A plain tap on the badge does nothing.
  - The debug seat is view only. The page resolves `{seat}` ids and the seat-specific pages with the debug seat, so the lamps, the positions and the pages are those of that seat (`/state` carries the values of both seats). Every control stays disabled, so no command can leave the page; the bridge never sees the debug seat.
  - The badge reads `DEBUG PILOT` or `DEBUG CP/G` in the amber read-only style, in place of the normal text. Without DCS data the pages show their empty state.
  - The tab bar and the pages follow the debug seat as they follow a real seat. It is held in the page only and is not remembered: a reload clears it.
- The header shows `NO DCS DATA` when no DCS-BIOS packet arrived for 3 s, and `BRIDGE OFFLINE` when the page cannot reach the bridge.
- The bridge refuses commands of a view outside its seats.

## 2. The views


Tabs at the top: **COCKPIT | FLIGHT | FIGHT | MPD | KU | GEORGE**. Ids written as `{seat}_...` stand for `PLT_...` (pilot) or `CPG_...` (CP/G); in this section `{S}` is the same.

### COCKPIT

A simplified cockpit map and one page per cockpit panel with every button, switch, knob and display of that panel, as in the real AH-64D. The quick pages FLIGHT and FIGHT keep their mixed layout; a control can sit on a panel page and on a quick page at the same time, and both show the same DCS state.

**Navigation**

- **Tap COCKPIT:** the cockpit map of the current seat. Each box is a panel; tap a box to open its page.
- **On a panel page** the COCKPIT tab keeps its highlight and shows a back chevron before the word. One tap goes back to the map.
- **Long hold (0.5 s) on COCKPIT:** a list of every page of the current seat, for jumping from page to page.
- The map boxes for the two MPDs, the TEDAC (CP/G only) and the KU open the MPD and KU tabs (MPD L, MPD R or TEDAC preselected).
- A page that does not exist in the current seat is not shown (map and list), it is not greyed out.
- The master lamps (MASTER WARNING, MASTER CAUTION) stay in the top row of the map and of every panel page. `CANOPY` is a small key button on the map (pilot seat).

**Switches.** A tap on a switch (a toggle or a dial) opens a chooser at the switch: one big button per position (at least 64 px, 8 px apart), arranged like the switch (a column, a row for `orient: "h"`, an arc for a dial: each button on a circle at the angle of its dial position, radius 90 px for two positions, 110 for three, 130 for four, spread in steps of 5 % until every pair is 8 px apart). The current position is lit, a `disabled` position is dashed and does nothing, a `momentary` (spring-return) position carries a spring mark, and a title line shows the control label. A tap on a position sends the command and closes the chooser; a tap on the position already set sends nothing; a tap outside closes the chooser without a command. While a command is sent the switch shows an amber outline. The power levers, the FRICT slider, rockers, buttons and guarded switches have no chooser.

**Knobs.** A tap on a knob opens the knob bar next to it ([Knob bar](#knob-bar)). On COMM, holding a volume knob for 0.6 s pulls it out or pushes it in (a ring fills during the hold).

**Pop-ups** (chooser and knob bar) open at the control, not in the middle of the screen: the bar below its knob (8 px gap; above it if there is no room; else centred on the knob), the chooser centred on the switch. Both are clamped into the screen: 8 px from the edges, below the tab bar, and clear of the gear (its 44 × 44 box plus 8 px, moved left or up, whichever shift is smaller). The scrim stays: a tap outside closes a pop-up without a command. The function is `placePopup(anchor, width, height, prefer)` in `core/web/index.html`.

**The map** is a 12 × 7 grid, `[row, col, rows, cols]`, of plain boxes with the panel placard, in the order of the real cockpit.

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

| Page | Grid (PLT) | Page | Grid (PLT) |
| --- | --- | --- | --- |
| KU | [1,1,1,3] | FIRE DET/EXTG | [1,4,1,3] |
| TAIL WHEEL / NVS | [2,1,1,3] | EUFD | [1,7,1,3] |
| EMERGENCY | [3,1,1,3] | ARMAMENT | [2,4,1,3] |
| POWER | [4,1,2,3] | CANOPY (key) | [2,7,1,3] |
| STORES JETT | [6,1,1,3] | MPD L / MPD R | [3,4,3,3] / [3,7,3,3] |
| EXT / INTR LT | [7,1,1,3] | CENTER | [6,5,2,4] |
| CMWS | [1,10,2,3] | COMM | [3,10,3,3] |

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

| Page | Grid (CPG) | Page | Grid (CPG) |
| --- | --- | --- | --- |
| KU | [1,1,1,3] | FIRE DET/EXTG | [1,4,1,2] |
| EMERGENCY | [2,1,1,3] | ARMAMENT | [1,6,1,2] |
| POWER | [3,1,2,3] | EUFD | [1,8,1,3] |
| TAIL WHEEL / NVS | [5,1,1,3] | MPD L / TEDAC / MPD R | [2,4,3,2] / [2,6,3,2] / [2,8,3,3] |
| INTR LT | [6,1,1,3] | COMM | [2,11,2,2] |
| STORES JETT | [7,1,1,3] | WIPER / DEFOG | [4,11,1,2] |

The CP/G has no CMWS, no EXT LT, no VIDEO, no CHECK OVERSPEED / GENERATOR RESET panel, no PARK BRAKE, no master ignition, no APU, no engine start, no rotor brake. The CP/G wiper and defog are on the right console, on their own page WIPER / DEFOG below COMM; the pilot's are on the CENTER page.

**Naming convention**

- **Page name** = the placard of the panel in upper case (`FIRE DET/EXTG`, `STORES JETT`, `TAIL WHEEL / NVS`).
- **Control label** = the text printed on the panel. A rocker shows its name between two arrows (`WCA`), a knob its name (`FLOOD`).
- **Positions** are listed in the order printed on the panel, top to bottom or left to right, with all real positions, also unusable ones (greyed out).
- **Control id** = the DCS-BIOS identifier with the seat as `{S}`. A function without a DCS-BIOS entry (keypress) uses a lower-case name from `[keys]` (`canopy`, `power_left`).
- All text in English, as in the cockpit.

#### Guarded controls

A guarded control can end the flight or cannot be undone in the mission: shut off an engine or the APU (the FIRE buttons stop the fuel flow), discharge an extinguisher bottle, drop stores (JETT), wipe the radio and crypto data (zeroize), jettison the countermeasure flares. All are on the tablet, only on their own panel page (never on FLIGHT or FIGHT), and need two deliberate steps:

1. **Lift the cover.** The control is covered by a red and white hazard-striped frame with a padlock. The middle of the frame is clear, so the lamps and the control underneath stay visible. Tap the cover to lift it. It closes again after 5 seconds, or after the press. Only one cover can be open at a time.
2. **Tap the control.** One tap on the button, or on the position of a guarded switch, sends the command and the cover closes. A guarded switch is the one switch without a chooser: under the cover each position is a touch band of its own (60 du, equal split).

The kit draws the cover from the part: the part (or its white frame) and 12 du on every side, a hazard frame 14 du wide, a padlock of 24 du (`cover_at`, never typed in). The bridge enforces the rule, so a second tab, a bug in the page or a stale tab cannot bypass it:

- Opening a cover sends `{"id": ..., "guard": "open"}`. The bridge opens a 5 second window for that id only.
- A command for a guarded id is accepted only inside its window, and the window is used up by the press. Otherwise the answer is `refused: guard closed`.
- The press itself is a confirmed press: the bridge holds until DCS-BIOS shows the button.
- Log lines: `guard open`, `pressed`, `refused: guard closed`, and for the parts with a real cover `cover open`, `cover closed` and `refused: cover did not open`.

**Real DCS covers.** Where the real cockpit has a cover (FIRE ENG 1, APU and ENG 2, master zeroize, CMWS flare jettison), DCS-BIOS has a cover control (`{S}_FIRE_ENG1_CVR`, `_APU_CVR`, `_ENG2_CVR`, `{S}_INST_MZERO_CVR`, `PLT_CMWS_JETT_CVR`), and DCS does not react to the button while its own cover is closed. These controls carry a `cover` property with that id, and the bridge opens and closes DCS's own cover for them. Lifting the tablet cover sets the real cover to 1 and waits up to 0.5 s for the DCS-BIOS readback; if it does not open, the answer is `refused: cover did not open` and the tablet cover stays shut. The bridge closes the real cover again about 1 second after the command was accepted, when the 5 second window runs out unused, or at once when another guarded control is lifted. PRI, RES, JETT and ZEROIZE have no cover in DCS-BIOS and only use the tablet cover.

Controls with `guard`: `{S}_FIRE_ENG1_BTN`, `{S}_FIRE_APU_BTN`, `{S}_FIRE_ENG2_BTN`, `{S}_FIRE_PRIME_EXT`, `{S}_FIRE_RES_EXT`, `{S}_JETT_BTN`, `{S}_EMERG_ZERO_SW`, `{S}_INST_MZERO_SW`, `PLT_CMWS_JETT`. The six station select buttons only arm a station and light up; they are normal buttons, and JETT is guarded. The guarded switches ZEROIZE, MASTER ZEROIZE and CMWS JETT list ON on top and OFF at the bottom.

#### Power levers

Used on the FLIGHT view and on the POWER page.

- One vertical slider per lever, positions bottom to top: OFF, IDLE, FLY, LOCKOUT. The slider snaps to positions only. LOCKOUT is shown above FLY but greyed and cannot be reached.
- Readback to position: the nearest of OFF 0, IDLE 16383, FLY 58981, LOCKOUT 65535.
- Moving the slider sends the keys for that lever, one step at a time, waiting up to 1 s for the readback after each step: OFF → IDLE `power_<side>_idle`; IDLE → FLY `power_<side>_up`; FLY → IDLE `power_<side>_down`; IDLE → OFF `power_<side>_off`. OFF → FLY and FLY → OFF go through IDLE. `<side>` is `left` for PWR LVR 1 (engine 1) and `right` for PWR LVR 2 (engine 2).
- On the panel pages a tap on a mark moves the lever (one touch band per mark); the grip follows the readback. A tap on the FRICT slot opens the knob bar.

#### Lamp row

MASTER WARNING (red) and MASTER CAUTION (amber) with `{seat}_` ids are lighted push buttons as in the cockpit: tapping the lamp presses `{seat}_INTL_MWARN_BTN` / `{seat}_INTL_MCAUTION_BTN` (0.3 s). Every COCKPIT page has the two master lamps in its top row. FLIGHT adds ENG 1 FIRE, APU FIRE and ENG 2 FIRE (red, `PLT_ENG_1_FIRE_L`, `PLT_APU_FIRE_L`, `PLT_ENG_2_FIRE_L`) and APU ON (green, `PLT_APU_L`); FIGHT adds the armament lamps. Lamps are display only, except the master lamps.

#### Panel pages

Value = label in the position lists. `rest` = resting value of a spring-loaded switch (set, held, back to rest). Seats: both unless noted.

**POWER** (left console). Pilot: everything. CP/G: the two power levers only.

| Label | Id | Type | Positions / notes |
| --- | --- | --- | --- |
| RTR BRK | `PLT_ROTOR_BRK` | selector | 2 OFF, 1 BRK (greyed out, needs conditions), 0 LOCK |
| MSTR IGN | `PLT_MASTER_IGN_SW` | selector | 0 OFF, 1 BATT, 2 EXT PWR (greyed out, no ground power) |
| APU cover | `PLT_APU_BTN_CVR` | selector | 0 CLOSED, 1 OPEN |
| APU | `PLT_APU_BTN` | button, `requires` the cover open | press; lamp `PLT_APU_L` ON. Locked while the cover is closed: the page does not send it and the bridge refuses it |
| ENG START NO 1 / NO 2 | `PLT_ENG1_START`, `PLT_ENG2_START` | selector, rest 1 | 2 START (momentary), 1 OFF, 0 IGN ORIDE (momentary); held 0.5 s |
| PWR LVR NO 1 / NO 2 | `{S}_ENG_L_PW_LVR`, `{S}_ENG_R_PW_LVR` | lever (keypress, readback) | OFF 0, IDLE 16383, FLY 58981, LOCKOUT 65535 (greyed out); both seats |
| FRICT | `PLT_PW_LVR_FRIC` | knob | 0 to 65535 |

**TAIL WHEEL / NVS**: TAIL WHEEL `{S}_T_WHEEL_UNLOCK_BTN` (button, lamp `{S}_T_WHEEL_UNLOCK_L` UNLOCK); NVS MODE `{S}_NVS_MODE` (selector: 2 FIXED, needs the NVS on; 1 NORM; 0 OFF).

**EMERGENCY**: GUARD `{S}_EMERG_GUARD_BTN`, XPNDR `{S}_EMERG_XPNDR_BTN` and EMERG HYD `{S}_EMERG_HYD_BTN` (buttons, lamps `{S}_EMERG_GUARD_L`, `{S}_EMERG_XPNDR_L`, `{S}_EMERG_HYD_L`); ZEROIZE `{S}_EMERG_ZERO_SW` (selector, `guard`, 0 / 1 toggle).

**STORES JETT**: six station buttons (press arms the station) with lamps, and the guarded JETT `{S}_JETT_BTN`. Buttons `{S}_JETT_STORE_LO`, `_LI`, `_RI`, `_RO`, `_LW`, `_RW` (L OUTBD, L INBD, R INBD, R OUTBD, L TIP, R TIP); lamps `{S}_JETT_L_OUTBOARD_L`, `_L_INBOARD_L`, `_R_INBOARD_L`, `_R_OUTBOARD_L`, `_L_TIP_L`, `_R_TIP_L`.

**EXT / INTR LT.** Pilot: both blocks. CP/G: INTR LT only (no STBY INST knob).

| Label | Id | Type | Positions | Seats |
| --- | --- | --- | --- | --- |
| NAV | `PLT_EXTL_NAV_L_SW` | selector | 2 BRT, 1 OFF, 0 DIM | PLT |
| FORM | `PLT_EXTL_FROMATION_L_KNB` | knob | OFF to BRT | PLT |
| ANTI COL | `PLT_EXTL_ACOL_L_SW` | selector | 2 WHT, 1 OFF, 0 RED | PLT |
| SIGNAL | `{S}_INTL_SIGNAL_L_KNB` | knob | DIM to BRT | both |
| PRIMARY, FLOOD | `{S}_INTL_PRIMARY_L_KNB`, `{S}_INTL_FLOOD_L_KNB` | knob | OFF to BRT | both |
| STBY INST | `PLT_INTL_STBYINST_L_KNB` | knob | OFF to BRT | PLT |
| PRESS TO TEST | `{S}_INTL_TEST_BTN` | button | press | both |

**FIRE DET/EXTG** (glareshield). A yellow FIRE and a green RDY light on each of ENG 1, APU and ENG 2, and a DISCH light on PRI and RES. A fire button press arms the extinguisher for that compartment and shuts off its fuel (press again: safe). All buttons are guarded; ENG 1, APU and ENG 2 have a real DCS cover.

| Label | Id | Lamps |
| --- | --- | --- |
| ENG 1 | `{S}_FIRE_ENG1_BTN` | FIRE `{S}_ENG_1_FIRE_L`, RDY `{S}_ENG_1_READY_L` |
| APU | `{S}_FIRE_APU_BTN` | FIRE `{S}_APU_FIRE_L`, RDY `{S}_APU_READY_L` |
| ENG 2 | `{S}_FIRE_ENG2_BTN` | FIRE `{S}_ENG_2_FIRE_L`, RDY `{S}_ENG_2_READY_L` |
| PRI | `{S}_FIRE_PRIME_EXT` (discharge) | DISCH `{S}_FIRE_EXT_DISCH_PRI_L` |
| RES | `{S}_FIRE_RES_EXT` (discharge) | DISCH `{S}_FIRE_EXT_DISCH_RES_L` |
| TEST | `{S}_FIRE_DETECT_TEST` | selector, rest 1: 0 "1" (momentary), 1 OFF, 2 "2" (momentary); not guarded |

**ARMAMENT** (with VIDEO and MASTER ZEROIZE). The pilot page carries the ARMAMENT panel, the MASTER ZEROIZE placard and the VIDEO panel; the CP/G page ARMAMENT and MASTER ZEROIZE only. MASTER ZEROIZE is a plain placard (the switch sits on the instrument panel next to the armament panel). On the VIDEO panel IHADSS BRT / CON share one knob and FLIR LVL / GAIN share one knob; a small mark next to the knob selects the function (`group`, `mark`, `dot`).

| Label | Id | Type | Notes |
| --- | --- | --- | --- |
| A/S | `{S}_MASTER_ARM_BTN` | button | lamps ARM `{S}_MASTER_ARM_ARM_L`, SAFE `{S}_MASTER_ARM_SAFE_L` |
| GND ORIDE | `{S}_GROUND_OVERRIDE_BTN` | button | lamp `{S}_GROUND_OVERRIDE_L` |
| MASTER ZEROIZE | `{S}_INST_MZERO_SW` | selector, `guard` | 0 / 1 (toggle); real cover `{S}_INST_MZERO_CVR` |
| IHADSS BRT, CON | `PLT_VIDEO_IHADSS_BRT`, `PLT_VIDEO_IHADSS_CON` | knob | MIN to MAX, PLT |
| SYM BRT | `PLT_VIDEO_SYM_BRT` | knob | MIN to MAX, PLT |
| ACM | `PLT_VIDEO_AUTO_CON` | selector | 0 OFF, 1 ACM, PLT |
| FLIR LVL, GAIN | `PLT_VIDEO_FLIR_LVL`, `PLT_VIDEO_FLIR_GAIN` | knob | MIN to MAX, PLT |

**EUFD.** The display is on top and the controls sit in a row below it: the three rockers, the BRT knob and the four keys (the text size matters more than the photo layout).

| Label | Id | Type | Positions / notes |
| --- | --- | --- | --- |
| display | `{S}_EUFD_LINE1` to `_LINE14` | display, `ids` | 14 lines of 56 characters, shown as on the real display |
| WCA, IDM, RTS | `{S}_EUFD_WCA`, `_IDM`, `_RTS` | hat (IDM, RTS: rest 1) | 2 up, 1 off, 0 down |
| BRT | `{S}_EUFD_BRT` | knob | DIM to BRT |
| P (preset), ENTER, STOPWATCH, SWAP | `{S}_EUFD_PRESET`, `_ENT`, `_STOPWATCH`, `_SWAP` | button | press; STOPWATCH: press to start / stop, hold to reset |

**CMWS** (pilot only).

| Label | Id | Type | Positions / notes |
| --- | --- | --- | --- |
| PWR | `PLT_CMWS_PW` | selector, rest 1 | 0 OFF, 1 ON, 2 TEST (momentary) |
| STATUS | `PLT_CMWS_FLARE_LETTER`, `_FLARE_COUNT`, `_CHAFF_LETTER`, `_CHAFF_COUNT`, `_BIT_LINE_1`, `_BIT_LINE_2`, `_PAGE` | display, `ids`, `pages` | page MAIN `F 60` / `C 30`, page TEST the two test lines, page NONE blank |
| THREAT lamps | `PLT_CMWS_FWD_LEFT_BRT_L`, `_FWD_RIGHT_`, `_AFT_LEFT_`, `_AFT_RIGHT_`, `PLT_CMWS_D_BRT_L`, `PLT_CMWS_R_BRT_L` (and the matching `_DIM_L`) | page-level `indicators` | orange, bright and dim |
| AUDIO, LAMP | `PLT_CMWS_VOL`, `PLT_CMWS_LAMP` | knob | MIN to MAX |
| ARM / SAFE | `PLT_CMWS_ARM` | selector | 1 ARM, 0 SAFE |
| CMWS / NAV | `PLT_CMWS_MODE` | selector | 1 CMWS, 0 NAV |
| BYPASS / AUTO | `PLT_CMWS_BYPASS` | selector | 1 BYPASS, 0 AUTO |
| JETTISON | `PLT_CMWS_JETT` | selector, `guard` | 0 / 1; real cover `PLT_CMWS_JETT_CVR` |

**CENTER** (pilot only, instrument panel). One wide plate (CHK OVSP TEST and GEN RST) over two plates (WINDSHIELD WIPER, and PARK BRAKE with ALT SET), 16 du apart on shared edge lines. The PARK BRAKE name is printed on two lines.

| Label | Id | Type | Positions |
| --- | --- | --- | --- |
| CHK OVSP TEST, CKT A / B | `PLT_CHK_OSPD_ENG_A`, `_B` | selector, rest 1 | 2 ENG 1, 1 OFF, 0 ENG 2 (spring return) |
| GEN RST | `PLT_GEN_RESET` | selector, rest 1 | 0 GEN 1, 1 off, 2 GEN 2 (spring return) |
| DEFOG | `PLT_DEFOG_BTN` | button | press |
| WINDSHIELD WIPER | `PLT_WIPER_SW` | selector | 0 PARK, 1 OFF, 2 LO, 3 HI |
| PARK BRAKE | `PLT_PARK_BRAKE` | selector | 0 IN, 1 PULLED |
| ALT SET | `PLT_ALT_SET_KNB` | knob | 0 to 65535 |

**COMM** (right console). One drawing for both seats. The ICS name and its PTT label sit in the SOL row, between the FM 1 and FM 2 squelch switches; the switch itself, with VOX and HOT MIC, is below the row. The volume knobs of VHF, UHF, FM 1, FM 2, HF, VCR and ADF have a PULL chip (a `chip` control, 64 × 22 du, touch area at least 32 px) hanging under the knob for the pull-to-disable position; holding the knob for 0.6 s toggles it too, a short tap opens the knob bar.

| Label | Id | Type | Positions |
| --- | --- | --- | --- |
| VHF, UHF, FM 1, FM 2, HF volume | `{S}_COM_VHF_VOL`, `_UHF_`, `_FM1_`, `_FM2_`, `_HF_` | knob | MIN to MAX |
| VHF, UHF, FM 1, FM 2, HF disable (pull) | `{S}_COM_VHF_PW`, `_UHF_`, `_FM1_`, `_FM2_`, `_HF_` | selector | 0 In, 1 Out |
| SQL x 5 | `{S}_COM_VHF_SQL`, `_UHF_`, `_FM1_`, `_FM2_`, `_HF_` | selector, rest 1 | 2 ENABLE, 1 off, 0 DISABLE (spring return) |
| MASTER, SENS | `{S}_COM_MASTER_VOL`, `{S}_COM_SENS_KNB` | knob | MIN to MAX |
| ICS | `{S}_COM_ICS_MODE` | selector | 0 HOT MIC, 1 VOX, 2 PTT (takes about 3 s) |
| IDENT | `{S}_COM_IDENT_BTN` | button | press |
| IFF, RLWR, ATA, VCR, ADF volume | `{S}_COM_IFF_VOL`, `_RLWR_`, `_ATA_`, `_VCR_`, `_ADF_` | knob | MIN to MAX |
| VCR, ADF disable (pull) | `{S}_COM_VCR_PW`, `{S}_COM_ADF_PW` | selector | 0 In, 1 Out |

**WIPER / DEFOG** (CP/G only). The same drawing as the wiper block of the CENTER page; the position labels (PARK, OFF, LO, HI) are flat text in a fan above the dial. DEFOG `CPG_DEFOG_BTN` (button), WINDSHIELD WIPER `CPG_WIPER_SW` (0 PARK, 1 OFF, 2 LO, 3 HI).

**Not on a page:** the CP/G processor select panel (not implemented in DCS), the SAI (cage and pitch trim do not work; only the altimeter setting knob is used, on CENTER), canopy jettison, M4 rifle, sun visors, stick fold, radio frequencies.

### FLIGHT

Follows the current seat. Lamp row as above. A fixed grid of 3 rows × 7 columns (each control has `"grid": [row, col, rows, cols]`), so the power levers and TAIL WHEEL stay in the same place when switching to FIGHT.

| Label | DCS-BIOS / route | Grid | Notes |
| --- | --- | --- | --- |
| TRIM | export script + `{seat}_CYCLIC_TRIM_UD`, see below | rows 1–2, columns 1–2 | read only |
| CTRL IND | key `controls_overlay` | row 3, column 1 | toggles DCS's own controls overlay (no lag) |
| SYMBOLOGY | `{seat}_CYCLIC_SYMBOLOGY` | rows 1–2, column 4 | two-way hat: T/C ↑ (2), H/B ↓ (0), held 0.3 s, back to centre |
| MONOCLE | key `monocle` | row 1, column 5 | push button, no state |
| TAIL WHEEL | `PLT_T_WHEEL_UNLOCK_BTN`, lamp `PLT_T_WHEEL_UNLOCK_L` | row 2, column 5 | lit push button, press = 1, released to 0 after 0.3 s; pilot seat only (greyed in the CP/G seat) |
| PWR LVR 1, 2 | keys, readback `{seat}_ENG_L_PW_LVR` / `{seat}_ENG_R_PW_LVR` | columns 6 and 7 | ids `flight_power_left` / `flight_power_right` |

**Trim display.**

- The export script sends the actual control positions 10 times per second. The bridge receives them on the export port (if the port is busy it logs `export port busy` and runs without them).
- The live position is not drawn (it lags behind the stick); CTRL IND toggles DCS's own overlay for that.
- **Trim point:** when the Force Trim switch (`{seat}_CYCLIC_TRIM_UD`) goes from 2 (held, `TRIM_RELEASED`) back to rest, the bridge stores the cyclic pitch / roll and the pedals at that moment as the seat's trim point and logs `PLT set P … R … Y …`.
- **Trim reset:** while DCS is the active window, the bridge watches the `trim_reset` key by reading only that key's state; on a press it moves the trim point to the centre and logs `PLT reset`.
- `/state` has `controls` (the latest positions), `controls_age` and `trim`: `{"plt": {"pitch", "roll", "pedals", "reset", "age"}, ...}`.
- The page draws a small box with a green ring at the trim point and a green tick on the pedal bar, with the values as text; `NOT TRIMMED` before the first trim, `RESET` after a reset. Directions are set by `CTRL_PITCH_SIGN`, `CTRL_ROLL_SIGN`, `CTRL_PEDAL_SIGN` at the top of the page script.

### FIGHT

Two pages, one per seat, both named Fight ([Seat](#1-seats)). The tab bar has one FIGHT tab; it opens the page of the current seat, and a seat change switches to the page of the new seat. Both pages use the same fixed 3 × 7 grid as FLIGHT.

#### Pilot page

| Lamp | DCS-BIOS | Colour |
| --- | --- | --- |
| MASTER WARNING | `{seat}_MASTER_WARNING_L` | red (tappable) |
| MASTER CAUTION | `{seat}_MASTER_CAUTION_L` | amber (tappable) |
| ARM | `{seat}_MASTER_ARM_ARM_L` | amber |
| SAFE | `{seat}_MASTER_ARM_SAFE_L` | green |
| GND ORIDE | `{seat}_GROUND_OVERRIDE_L` | amber |

| Label | DCS-BIOS | Positions | Notes |
| --- | --- | --- | --- |
| A/S | `{seat}_MASTER_ARM_BTN` | push button | press = 1, released to 0 after 0.3 s; the ARM and SAFE lamps show the result |
| GND ORIDE | `{seat}_GROUND_OVERRIDE_BTN` | push button | as A/S |
| WAS | hat: `{seat}_CYCLIC_WEAPON_UD` / `_LR` | up = G, down = A, left = R, right = M | see Hats |
| SIGHT SEL | hat: `{seat}_COLLECTIVE_SIGHT_SELECT_UD` / `_LR` | up = HMD, down = LINK, left = FCR, right = TADS | see Hats |
| FLARE, CHAFF | `{seat}_CYCLIC_FLARE`, `{seat}_CYCLIC_CHAFF` | push button | as A/S |
| FLARE COUNT, CHAFF COUNT | `PLT_CMWS_FLARE_COUNT`, `PLT_CMWS_CHAFF_COUNT` | display | read only; from the pilot's CMWS panel, also shown on the gunner page |

**Hats.** A hat is drawn as a cross of four buttons. A tap sets the axis (`_UD` or `_LR`) to 2 (up, right) or 0 (down, left) and holds it for 0.3 s; then the bridge returns the axis to the centre, 1. The highlighted direction comes from the readback of the two axes. The pilot page uses the cyclic WAS and the collective sight select; the gunner page uses the cyclic WAS and the right-grip sight select. The left-grip WAS (LHG WAS) is left out on purpose: it does the same as the cyclic WAS (it works too, as a fallback).

**CMWS.** Flares only fire with the CMWS panel set up: CMWS PWR ON, FLARE SQUIBS ARM, CMWS MODE CMWS; CMWS OPER BYPASS / AUTO decides whether the CMWS dispenses on its own. Chaff must be armed on the MPD ASE page. On the ground dispensing may be blocked.

| Label | DCS-BIOS | Positions | Grid |
| --- | --- | --- | --- |
| CMWS PWR | `PLT_CMWS_PW` | 2 = TEST (spring-loaded, 0.5 s), 1 = ON, 0 = OFF | row 1, column 5 |
| FLARE SQUIBS | `PLT_CMWS_ARM` | 1 = ARM, 0 = SAFE | row 1, column 6 |
| CMWS MODE | `PLT_CMWS_MODE` | 1 = CMWS, 0 = NAV | row 2, column 5 |
| CMWS OPER | `PLT_CMWS_BYPASS` | 1 = BYPASS, 0 = AUTO | row 2, column 6 |

#### Gunner page

The page of the CP/G seat. Ids are written out as `CPG_...` (the page exists for one seat only). The lamp row has MASTER WARNING and MASTER CAUTION (tappable, as above), ARM, SAFE and GND ORIDE (the colours of the pilot page). 14 controls:

| Label | DCS-BIOS | Positions | Notes | Grid |
| --- | --- | --- | --- | --- |
| A/S | `CPG_MASTER_ARM_BTN` | push button | as on the pilot page | row 1, column 1 |
| GND ORIDE | `CPG_GROUND_OVERRIDE_BTN` | push button | as A/S | row 1, column 2 |
| FLARE, CHAFF | `CPG_CYCLIC_FLARE`, `CPG_CYCLIC_CHAFF` | push button | as A/S | row 2, columns 1 and 2 |
| FLARE COUNT, CHAFF COUNT | `PLT_CMWS_FLARE_COUNT`, `PLT_CMWS_CHAFF_COUNT` | display | read only, as on the pilot page | row 3, columns 1 and 2 |
| WAS | hat: `CPG_CYCLIC_WEAPON_UD` / `_LR` | up = G, down = A, left = R, right = M | see Hats | row 1, columns 3 and 4 |
| SIGHT SEL | hat: `CPG_RHG_SIGHT_UP_DN` / `CPG_RHG_SIGHT_L_R` | up = HMD, down = LINK, left = FCR, right = TADS | right grip, see Hats | row 2, columns 3 and 4 |
| SLAVE | `CPG_RHG_SIGHT_SLAVE` | push button | slaves the selected sight to the acquisition source, or releases it; held 0.3 s | row 3, column 3 |
| TADS FOV | hat: `CPG_LHG_TADS_FOV_UP_DN` / `CPG_LHG_TADS_FOV_L_R` | up = Z (zoom), left = N (narrow), right = W (wide), down = M (medium) | left grip, see Hats | row 1, columns 5 and 6 |
| SENSOR | `CPG_LHG_TADS_SEL` | 2 = FLIR, 1 = TV, 0 = DVO (greyed out, no function in DCS) | selector | row 2, columns 5 and 6 |
| IAT | `CPG_LHG_TEDAC_L_IAT` | 2 (forward), then back to 1 | held 0.3 s | row 1, column 7 |
| OFS | `CPG_LHG_TEDAC_L_IAT` | 0 (aft), then back to 1 | held 0.3 s | row 2, column 7 |
| OFS ALL | `CPG_LHG_TEDAC_L_IAT` | 0 (aft), then back to 1 | held 0.8 s | row 3, column 7 |

Row 3, columns 4 to 6 are free. The control ids of the page are `CPG_WAS`, `CPG_SIGHT_SEL`, `CPG_TADS_FOV`, `CPG_IAT`, `CPG_OFS` and `CPG_OFS_ALL` for the hats and the three tracker buttons; the others use their DCS-BIOS id.

**IAT, OFS and OFS ALL** are three buttons on one switch of the left grip: a 3-position switch that springs back to the middle (rest 1). IAT is forward (2), OFS is aft (0), taken from the grip like the other hats; the mapping is to be confirmed in DCS, together with the SENSOR mapping. Each button sends its position, holds it and returns the switch to 1 (`bios`, `value` and `rest` in [section 8 of the generic spec](../SPEC.md#8-the-bridge-interface)). What they do, after the DCS manual:

- **IAT** starts an auto-track on the target under the TADS reticle, or updates the aim point when the reticle is inside the gates.
- **OFS** (short press): drops the primary track when the reticle is inside the gates; outside the gates it returns the TADS to the primary track.
- **OFS ALL** (the aft position held over 0.5 s, here 0.8 s): deletes all tracks.

**Not on the page.** The weapon trigger and the laser trigger. DCS-BIOS has no entry for the laser trigger; the weapon trigger (`CPG_CYCLIC_TRIGGER`) has one, but it is on the [blocklist](../SPEC.md#blocklist-idea) and releases weapons. Both could become key buttons later (key bindings in DCS, like George). Also left out, not asked for: the FCR mode and scan switches, FLIR polarity, the laser tracker mode, MTT promote, the cursor extras, STORE and LMC; they can go into free cells later.

### MPD

One display at a time, following the current seat (`"layout": "mpd"`). A `LEFT MPD | TEDAC | RIGHT MPD` switch at the top selects which one (remembered on the tablet); TEDAC appears only in the CP/G seat. The display sits flush left, the cursor group uses the rest of the width (pad about 450 px on the iPad Air); in the CP/G seat with the TEDAC selected the TKR group takes its place.

- Laid out 1:1 after a photo of the real MPD: every button, knob and print at its measured position (square spacing, about 100 px pitch on the photo). VID knob on the raised top-left corner, BRT below it, MODE top right with DAY / NT / MONO; \* above R1; FCR / WPN below L6, VID / COM below R6; TSD and A/C offset in the bottom corners next to M and B2–B6.
- Variable action buttons are light grey with a green dot; fixed action buttons are black keys with green text. Buttons are drawn at true size (about 33 px on the iPad Air) with a larger invisible touch area (56 px where neighbours allow). Each press is held 0.3 s.
- **Live labels:** the export script sends the occupied seat's MPD texts (`MPD_INDICATIONS`, `MPD_SEATS`: pilot 7 left / 9 right, CP/G 11 / 13) 4 times per second. The bridge reads the `PB<n>` fields and serves them as `mpd_labels` in `/state` (`{"L": {...}, "R": {...}, "age": ...}`); the page writes each label in MPD green next to its button. Mapping: PB1–6 = T1–T6, PB7–12 = R1–R6, PB13–18 = B6…B1 (PB18 = M), PB19–24 = L6…L1. No labels when no MPD text arrived for 3 s.
- In the CP/G seat the left MPD's L1–L6 do not respond in DCS.

**Cursor.** The CURSOR pad sits to the right of the bezel, for the collective cursor controller `{seat}_COLLECTIVE_CURSOR_LR` / `_UD` (analog, centre 32768). Put a finger anywhere on the pad and push: the distance from the touch point (up to 30 % of the pad) is the deflection, i.e. the cursor speed, like the real force-sensing controller. Lifting the finger sends centre. The page sends `{"x", "y"}` (−1..1) at most every 66 ms; the bridge sends only changed axes and does not wait behind slow commands. `CURSOR_Y_SIGN` at the top of the page script flips up / down. Below the pad: CURSOR SWITCH DISPLAY (`{seat}_COLLECTIVE_CURSOR_DISPLAY`, moves the cursor to the other MPD) and ENTER (`{seat}_COLLECTIVE_CURSOR_ENTER`). The cursor group is shown with LEFT MPD and RIGHT MPD and in the pilot seat; with the TEDAC selected (CP/G seat) it is replaced by the TKR group.

**TKR (TEDAC selected, CP/G seat).** The TKR group replaces the cursor group: a pad labelled TKR and the SLAVE button below it (`CPG_RHG_SIGHT_SLAVE`, as on the gunner FIGHT page). The pad is the Sight Manual Tracker of the right grip (`CPG_RHG_MAN_TRK_UP_DN`, `CPG_RHG_MAN_TRK_L_R`), a `stick` control with the flag `digital`. It looks and feels like the cursor pad (a finger anywhere on it, the distance from the touch point is the deflection), but the tracker has three states per axis: 2, 1 (centre) and 0. The bridge turns the deflection into 2 / 0 / 1 with a dead zone of 30 % of the full deflection (`STICK_DIGITAL`) and sends only changes; lifting the finger returns both axes to the centre, 1. DCS ramps the slew rate up while the switch is held (the DCS option MAN TRK ramp-up speed), so the speed is not set by the pad. The up / down sign is shared with the cursor (`CURSOR_Y_SIGN`).

**TEDAC (CP/G seat).** The CP/G's TEDAC display unit, laid out 1:1 after a photo like the MPD. All controls are `CPG_TEDAC_…`, `"side": "T"`, `"seats": [1]`:

- Top: TAD, FCR, PNV, G/S video select buttons; MODE knob DAY / NT / OFF (2 / 1 / 0, knob bar).
- Left: LEV and GAIN knobs (knob bar), R/F and EL rockers. Right: SYM, BRT, CON rockers and \*.
- Bottom: ◀AZ▶ rocker, then four buttons AZ/EL, ACM, FREEZE, FILTER with their names in green on the screen.
- Rockers are spring-loaded: tap the upper / lower half (AZ: left / right half); the bridge holds the position until confirmed and returns it to the centre.

#### Knob bar

Tapping a knob (MPD BRT / VID / MODE, KU BRT, TEDAC knobs, the knobs of the COCKPIT pages) opens a bar at the knob (420 px wide, or the screen less 24 px, 120 px high): below it, above it if there is no room, always inside the screen. BRT / VID / KU BRT and the panel knobs: drag or tap the track; the bridge sets the absolute knob position (`{"value": 0..65535}`, at most every 100 ms while dragging). MODE: three stops DAY / NT / MONO. Tap outside or the close cross to close. The MPD mode selectors use `step_fallback`: if the position is not reached in 0.5 s the bridge turns the knob with INC / DEC steps.

### KU

The keyboard unit, drawn 1:1 after a photo in the same technique as the MPD (`"layout": "ku"`), following the current seat: round number keys, boxed E / N / S / W, the white guide lines of the panel, BRT knob in its recess (knob bar), wide ENTER.

- Top: the scratchpad (`{seat}_KU_DISPLAY`) in green.
- Rows: A–F | 1 2 3, G–L | 4 5 6, M–R | 7 8 9, S–X | . 0 +/-, then Y Z / BKS SPC \* ÷ + −, then the BRT knob, CLR, ←, →, ENTER.
- Keys are pressed for 0.15 s.

### GEORGE

George, the AI crew member (gunner when you fly as pilot, pilot when you fly as CP/G), can only be controlled by keypress. The GEORGE tab (`"name": "George"`, both seats) has direct buttons for the useful commands, so the Helper Interface (the ring) does not have to be opened by hand. The lamp row has the two master lamps. George needs electrical power; without it the buttons do nothing.

Every button is a `macro` control ([section 8 of the generic spec](../SPEC.md#8-the-bridge-interface)): a fixed key sequence, each step `[key name, hold in seconds, pause after in seconds]`. Hold times: short 0.15 s (`GEORGE_SHORT`), long 1.2 s (`GEORGE_LONG`; the manual calls a press over 0.5 s long, and some commands need a full second). A key with modifiers is pressed staggered: the modifiers go down, 40 ms later the letter goes down, is held, goes up, and 40 ms later the modifiers go up (`MACRO_KEY_GAP` in `core/dashboard.py`), so DCS sees the modifiers before the letter.

| Button | Seat | Key sequence | Notes |
| --- | --- | --- | --- |
| PHS SEARCH | pilot | ring: Up, short, ring left open | George searches with the PHS; works once George's systems are ready (on the ground with the systems not ready the ring shows the start-up layout instead); the ring stays open so the Target List can appear |
| AIR AREA SEARCH | pilot | Hide, Show, `george_multi`, long | George must not be tracking; area search works in the air only: on the ground the same press starts George's systems (READY SYSTEMS) or, when they are already started, shuts them down (MASTER OFF); the ring is opened first and stays open so the Target List can appear |
| POINT SEARCH | pilot | Hide, Show, `george_multi`, short | George must not be tracking, and a TSD point must be selected; the ring is opened first and stays open so the Target List can appear |
| STORE TARGET | pilot | `george_store`, short | George stores a point only while he is tracking a target, otherwise he says he cannot; works without the ring (the ring does not open) |
| STOP / TADS FWD | pilot | ring: Down, short | cancels any task of George, including an engagement |
| WEAPON NEXT | pilot | ring: Left, short, ring left open | cycles NO WPN, GUN, MSL, RKT; the ring stays shown so the selection can be read in it |
| READY SYSTEMS / MASTER OFF | pilot | `george_multi`, long | on the ground George starts up his systems (TADS, lasers, displays) and announces when done, or, if they are already started, shuts them down; the same press as AIR AREA SEARCH, which one happens depends on whether the aircraft is on the ground |
| ROE HOLD / FREE | pilot | ring: Up, long, ring left open | toggles George's rules of engagement between HOLD FIRE and FREE FIRE; the ring stays open: yellow text is HOLD FIRE, green text is FREE FIRE (there is no readback, read the colour) |
| FIRE | pilot | `george_multi`, short | consent to fire the assigned weapon, also in HOLD FIRE |
| PREV TARGET | pilot | `george_up`, short | moves to the previous entry of the Target List; the TADS slews to it |
| NEXT TARGET | pilot | `george_down`, short | moves to the next entry of the Target List; the TADS slews to it |
| EXIT LIST | pilot | `george_left`, short | leaves the Target List and cancels the shoot list |
| SELECT TARGET | pilot | `george_multi`, short | adds the current entry to the shoot list or removes it (the entries are numbered in the list) |
| TRACK / ENGAGE | pilot | `george_right`, short | tracks the current target; if it is on the shoot list, starts the multi-target sequence |
| REQUEST CONTROL | CP/G | `george_request`, short | hands the flight controls to George and takes them back; works without the ring |
| SHOW RING | both | Hide, Show | opens the ring |
| HIDE RING | both | Hide | closes the ring and cancels a displayed Target, Search or Point list |

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

**Deliberately not on the page**

- The FLIGHT and COMBAT commands of George as pilot: in the CP/G seat they depend on the ring mode (GND, FLT, H-B, CMBT, DEFN, cycled with Left, short), and the dashboard cannot read the current mode.

**Binding the keys in DCS.** The keys are the `george_*` entries of `KEYS` ([section 3](#3-keybinds)). Bind them once under Options, Controls: choose the aircraft in the dropdown, double-click the row of the command and press the keys. They are added to the DCS defaults (`LCtrl+V`, `W` `A` `S` `D`), which keep working. `LCtrl+LAlt` was chosen because no DCS default uses it, it is not an AltGr combination, and unlike Ctrl+Shift it does not switch the Windows keyboard layout. Request Aircraft Control already has plain `C` by default; the added key avoids a stray plain C.

| DCS aircraft entry | Command | Key |
| --- | --- | --- |
| AH-64D Pilot and AH-64D CPG | George AI - Show/Hide | `LCtrl+LAlt+G` |
| AH-64D Pilot and AH-64D CPG | George AI - Multifunctional Input (Center) | `LCtrl+LAlt+M` |
| AH-64D Pilot only | George AI - TADS Store Target | `LCtrl+LAlt+T` |
| AH-64D CPG only | Request Aircraft Control | `LCtrl+LAlt+R` |
| AH-64D George AI Helper | George AI - Hide | `LCtrl+LAlt+H` |
| AH-64D George AI Helper | George AI - Up / Down / Left / Right | `LCtrl+LAlt+I` / `K` / `J` / `L` |

## 3. Keybinds

The default keybinds of the AH-64D are in `KEYS` in `aircraft/ah64d.py`. How `[keys]` in `config/config.toml` overrides them, and the key format, are in [section 3 of the generic spec](../SPEC.md#3-configuration).

| Key | Default | DCS command |
| --- | --- | --- |
| `power_left_idle`, `_up`, `_down`, `_off` | `RAlt+Home`, `RAlt+PageUp`, `RAlt+PageDown`, `RAlt+End` | power lever 1 |
| `power_right_idle`, `_up`, `_down`, `_off` | `RShift+Home`, `RShift+PageUp`, `RShift+PageDown`, `RShift+End` | power lever 2 |
| `canopy` | `LCtrl+C` | Open/Close Cockpit Door |
| `monocle` | `I` | IHADSS show |
| `controls_overlay` | `RCtrl+Enter` | Show controls indicator |
| `trim_reset` | `LCtrl+T` | Trimmer reset |
| `george_show` | `LCtrl+LAlt+G` | George AI - Show/Hide |
| `george_hide` | `LCtrl+LAlt+H` | George AI - Hide (AH-64D George AI Helper) |
| `george_up`, `_down`, `_left`, `_right` | `LCtrl+LAlt+I`, `K`, `J`, `L` | George AI - Up, Down, Left, Right (AH-64D George AI Helper) |
| `george_multi` | `LCtrl+LAlt+M` | George AI - Multifunctional Input (Center) |
| `george_store` | `LCtrl+LAlt+T` | George AI - TADS Store Target |
| `george_request` | `LCtrl+LAlt+R` | Request Aircraft Control |

## 4. What DCS allows for the AH-64D

The result of the research phase, on Windows with the AH-64D, both seats, cold and dark and in flight. The original research scripts and their full result tables are kept in git under the tag `research-v1`.

The generic findings (DCS-BIOS stream format, keypresses, the blocklist) are in [section 4 of the generic spec](../SPEC.md#4-what-dcs-allows).

### Reading

- **DCS-BIOS** (multicast stream) delivers switch positions, button states, lamps, levers and text for both seats: master caution and warning, engine and APU lamps (including lamp test and fire test), startup switches, power lever positions, armament buttons and lamps, weapons action and sight select hats, flare and chaff buttons, force trim, KU scratchpad, the 14 EUFD lines, the CMWS counts, the current seat (`SEAT_POSITION`: 0 pilot, 1 CP/G). The `AH-64D.json` control list has 562 controls with inputs (273 pilot, 284 CP/G, 5 radio frequencies).
- **Export script** (Lua, runs inside DCS next to DCS-BIOS, sends UDP to `127.0.0.1`; every call is wrapped in `pcall`, and it chains the existing export hooks so DCS-BIOS keeps working). It sends plain text, one `name=value` per line:
  - the actual control positions at 10 Hz as cockpit arguments: pilot cyclic pitch 470, roll 471, collective 474, pedals 476; CP/G 472, 473, 475, 478 (`plt_cyc_pitch`, `plt_cyc_roll`, `plt_coll`, `plt_pedals`, `cpg_…`);
  - the MPD page text: `list_indication` works for the Apache and gives named text fields (`PB<n>` and others). Only the displays of the occupied seat update. Index map: 7 and 9 pilot MPD left and right, 11 and 13 CP/G MPD left and right (only these four are sent, at 4 Hz).
- **Not usable or limited:** the generic engine values of DCS's export functions do not fit the Apache (`RPM` is NG %, temperature is always 0; TGT, torque, NP and NR exist only in the MPD ENG page text while that page is shown). Indicated airspeed is implausible at low speed. The DCS-BIOS radio strings are unreliable (HF stuck at a start value); the EUFD lines carry the radio frequencies.

### Controlling

- **DCS-BIOS commands** (UDP to 127.0.0.1, one line per command, `IDENTIFIER VALUE`, for example `PLT_MASTER_IGN_SW 1`) work for most cockpit controls and have a readback. 227 of the 273 pilot controls and 238 of the 284 CP/G controls passed an automatic sweep (every position, readback within 0.5 s, original position restored); the blocklisted controls were skipped.
- **Power levers:** DCS-BIOS does not move them past the OFF detent, and keys for both levers together do not work. They move by keypress, one key per lever: RAlt (left) or RShift (right) with Home = IDLE, PageUp = one step up, PageDown = one step down, End = OFF. DCS-BIOS reads back 0 OFF, 16383 IDLE, 58981 FLY after each key.
- **Canopy:** DCS-BIOS cannot move it; a key (`canopy`) with the readback `PLT_CANOPY` does.
- **Cockpit logic still applies.** A command that the cockpit would not accept fails without an error: the APU button only works with its cover open; master ignition EXT PWR needs ground power; rotor brake BRK needs conditions; NVS mode FIXED needs the NVS on; push buttons under a DCS cover (fire buttons, CMWS jettison) are ignored while DCS's own cover is closed; ICS mode and the M4 safety need about 3 s to take the position; the CP/G manual tracker position 2 is spring-loaded.
- **Did not work:** the canopy (both seats), CP/G stick fold, MPD mode knobs by a direct command (the bridge uses INC / DEC steps), processor select, TADS select, SAI cage and pitch trim, CP/G left MPD L1–L6. Not followed up; the dashboard does not need them or works around them.
- **George** (the AI crew member and its Helper Interface ring) has no DCS-BIOS entry and works by keypress only (the DCS defaults are `LCtrl+V` and `W` `A` `S` `D`), and only with electrical power. The dashboard reaches it from the GEORGE tab with its own keys ([section 2](#george)); the ring state and mode cannot be read.

## 5. Manual test run (AH-64D)

Preparation: DCS in windowed or borderless mode, DCS-BIOS and the export script installed, the default keybinds bound. PC and tablet on the same network. A throwaway AH-64D mission, cold and dark. Do the guarded controls last, because several cannot be undone in the mission.

1. **Start.** Run `start_dashboard.bat` (it starts `python core\dashboard.py` and prints the address to open). Open the address on the iPad and add it to the home screen. The badge shows `PILOT`; `NO DCS DATA` appears if DCS is not running.
2. **COCKPIT start-up sequence** (pilot seat, tablet only). POWER: MSTR IGN BATT, APU cover OPEN, APU, wait for APU ON, ENG 1 START, ENG 1 power lever IDLE, ENG 2 START, ENG 2 power lever IDLE, both power levers FLY. CENTER: PARK BRAKE IN. TAIL WHEEL / NVS: TAIL WHEEL once. Move a few switches in the cockpit with the mouse: the tablet follows.
3. **Pop-ups.** Chooser (NVS MODE, a squelch switch, ENG 1 START, the MSTR IGN dial, the wiper dial): it opens at the switch, shows the positions like the switch, lights the current one, marks the spring-return ones; a tap outside sends nothing. Knobs (EUFD BRT, a radio volume, a light knob): the bar opens next to the knob and the knob follows DCS. COMM: hold a volume knob for 0.6 s, the PULL chip toggles. Power levers and FRICT: tap each mark of both levers, drag the FRICT bar.
4. **Seat switch.** Switch to the CP/G seat (key `2`) while on a pilot-only page (for example CMWS): the page goes to the CP/G COCKPIT map, which has no CMWS, CENTER or EXT LT page. The badge shows `CP/G`. Switch back: the map shows the pilot pages.
5. **Debug seat.** Hold the seat badge for 0.6 s: it reads `DEBUG CP/G` (in the pilot seat), the pages show the CP/G, the FIGHT tab shows the gunner page, and every control is disabled. Hold again: back to `PILOT`. With DCS stopped the cycle is none, `DEBUG CP/G`, `DEBUG PILOT`, none. A reload clears it. On the tablet, check that a finger on the badge works as a long hold.
6. **FIGHT, pilot page.** A/S (the ARM and SAFE lamps change), GND ORIDE once, WAS and SIGHT SEL in each direction (the selection changes in the cockpit), FLARE and CHAFF once each (the counts change; the CMWS must be on and set up).
7. **FIGHT, gunner page and TKR** (CP/G seat). A/S, GND ORIDE, FLARE and CHAFF as above. WAS, SIGHT SEL (right grip: HMD, FCR, TADS, LINK) and SLAVE act in the cockpit. TADS FOV in each direction (Z, N, W, M) and SENSOR FLIR and TV. With a target under the TADS reticle: IAT starts a track, a short OFS drops it or returns the TADS to it, OFS ALL deletes all tracks; note whether IAT really is the forward and OFS the aft position of the grip switch. MPD tab, TEDAC selected: the TKR pad slews the sight in all four directions (note the up / down direction), a small push does nothing (dead zone), releasing the pad stops the slew; LEFT MPD and RIGHT MPD still show the cursor pad.
8. **Trim.** Hold the Force Trim switch and release it: the ring moves to the trim point and the log shows `PLT set`; press the trimmer reset key: `RESET`.
9. **MPD, KU, TEDAC.** MPD: press buttons on both displays; the live labels follow page changes; the cursor pad moves the cursor in the right direction; the MODE knob works (NT through the INC / DEC fallback). KU: type a few characters, the scratchpad shows them. CP/G seat: spot-check the TEDAC buttons, knobs and rockers.
10. **Guarded controls** (last). Station selects light their lamps and toggle back. ENG 1, APU and ENG 2 FIRE: lift the cover, tap once (RDY lamp on, fuel off), lift the cover again and tap again (safe); DCS's own cover opens with the tablet cover, and the log shows `cover open`, `pressed` and about 1 s later `cover closed`, without `not confirmed`. PRI and RES with a fire button armed, JETT with a station armed, ZEROIZE, MASTER ZEROIZE, CMWS JETT.

11. **GEORGE.** Bind the keys in DCS first (the table in [GEORGE](#george)). Pilot seat with battery power: SHOW RING and HIDE RING (the ring opens and closes); STOP / TADS FWD (the ring flashes open and closes again, George reacts); WEAPON NEXT (the ring stays open and the weapon label in the ring changes: NO WPN, GUN, MSL, RKT); PHS SEARCH, AIR AREA SEARCH and POINT SEARCH in the air with George not tracking (the ring stays open, a Target List appears when George reports targets; POINT SEARCH needs a TSD point selected); then PREV / NEXT TARGET, SELECT TARGET, TRACK / ENGAGE, ROE HOLD / FREE, FIRE and EXIT LIST on the list; STORE TARGET with a tracked target. CP/G seat: the pilot-only buttons are greyed; REQUEST CONTROL twice, George takes the flight controls, then gives them back.

Done when a cold start to both power levers at FLY works from the tablet alone, the lamps match the cockpit, the CP/G seat shows only its own pages, and every control acts in both seats.
