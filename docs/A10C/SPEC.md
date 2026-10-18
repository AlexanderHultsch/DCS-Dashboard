# DCS-Dashboard – A-10C II

Specification of the A-10C II Tank Killer dashboard (planned, not built; reviewed and approved 2026-10-18). The engine all aircraft share is in [../SPEC.md](../SPEC.md); the engine changes this aircraft needs and their decisions are in [ENGINE.md](ENGINE.md). Controls are named as in [PANELS.md](PANELS.md), DCS-BIOS identifiers are in [BIOS.md](BIOS.md), reference pictures in [PICTURES.md](PICTURES.md), the cold start in [STARTUP.md](STARTUP.md).

## 1. Overview

A tablet dashboard for the single-seat A-10C II, with the same tabs as every aircraft: **COCKPIT | FLIGHT | FIGHT | MFCD | CDU**. The same bridge serves both aircraft; it chooses the A-10C files when DCS-BIOS reports the aircraft `A-10C_2` (section 9).

| Tab | Content | AH-64D counterpart |
| --- | --- | --- |
| COCKPIT | Map of the cockpit; 23 panel pages and 4 link boxes (section 2) | COCKPIT |
| FLIGHT | Speed brake, trim, gear, flaps, lights, throttle positions and a few values (section 3) | FLIGHT |
| FIGHT | HOTAS core set (DMS, TMS, CMS, coolie hat, China hat, master mode), AHCP arming switches, countermeasure counts (section 4) | FIGHT |
| MFCD | Left and right MFCD, hand-drawn, one at a time (section 5) | MPD |
| CDU | CDU with its live 10-line screen and the UFC, hand-drawn (section 6) | KU |

Differences to the AH-64D: one seat (no seat switch, no debug seat), no GEORGE tab, no trim display, the throttle levers are shown but not moved (DCS-BIOS can only read them), and the HOTAS controls are keypresses only (DCS-BIOS has none of them). Built after the engine changes of [ENGINE.md](ENGINE.md) (E1 to E10).

**Blocked until the module is installed:** the A-10C default keybinds (section 8), four screenshots (flap lever, seat arm handle, auxiliary gear handle, canopy disengage lever; section 2 and PICTURES.md), and the DCS research of phase 7 (the open points of [RESEARCH.md](RESEARCH.md)). The pages that need no keypress (COCKPIT, MFCD, CDU) can be built before that.

## 2. COCKPIT

COCKPIT is a simplified map of the A-10C II cockpit and one page for every cockpit panel that has a function in DCS, with every button, switch, knob and display of that panel. Tap a box on the map to open its page; on a page the COCKPIT tab keeps its highlight and shows a back chevron, and one tap on it goes back to the map; a long hold (0.5 s) on COCKPIT opens a list of every page. The boxes MFCD L, MFCD R, CDU and UFC are not pages: they open the MFCD tab (left or right side preselected) and the CDU tab (the UFC sits on the CDU tab), as the AH-64D map boxes open MPD and KU. The A-10C has one seat, so there is no seat badge switch and no seat-dependent page: every page is always on the map and in the list.

Tabs at the top: **COCKPIT | FLIGHT | FIGHT | MFCD | CDU**.

The panel pages get the A-10C look (drawn later); this section only says which panels are on which page and where. The instruments (ADI, HSI, standby instruments, altimeter, VVI, airspeed, AoA, engine instruments, fuel and hydraulic gauges, accelerometer, compass, clock, RWR scope) are not panel pages and are not drawn (section 3); FLIGHT and FIGHT show a few of their values as text, and the HOTAS grips are controls for FIGHT and FLIGHT: none of them is a panel page. The small controls that sit on an instrument (cage knob, set knobs, clock keys, fuel selector) go with that instrument. The lamp row (section 7) stays at the top of the map and of every panel page.

**Lamps.** These lamps have no control and are not on a page; they go to the lamp row (section 7): GUN READY, STEERING ENGAGED, MARKER BEACON, CANOPY UNLOCKED. CANOPY UNLOCKED is also on the CANOPY / ELEC page. The three air refuel lights are on the FUEL SYSTEM page, next to the RCVR lever, and not on the lamp row. The three fire lamps, the gear lamps and the caution lamps are on their pages; section 7 may repeat them.

**The map** is a 12 × 7 grid, `[row, col, rows, cols]`, of plain boxes with the panel placard, in the order of the real cockpit, front at the top: the left console in columns 1 to 4 (outboard column 1 to 2, inboard column with the throttles 3 to 4), the front dash in columns 5 to 8, the right console in columns 9 to 12 (inboard column 9 to 10, outboard column 11 to 12). Names in brackets are not boxes: the instrument areas of the dash, which are on FLIGHT and FIGHT. `:` continues the box above. The sketch shortens some names; the table has the full ones.

```
    left console                    | front dash                      | right console
    outbd           inbd            |                                 | inbd            outbd
 1  BRAKE/AUX/SAS   FUEL SYSTEM     | UFC                             | CMSP            CANOPY/ELEC
 2  :               THROTTLE        | FIRE / JETT                     | CAUTION         :
 3  IFF             :               | MFCD L  CMSC            MFCD R  | :               ENVIRONMENT
 4  :               LASTE           | :       (ADI HSI)       :       | CDU             :
 5  EMER FLT CTRL   RADIO 1         | GEAR    AHCP    NMSP    (gauge) | AAP/ILS         :
 6  INTERCOM/STALL  UHF             | :       :       :               | TACAN           LIGHTING
 7  :               VHF FM          |                                 | HARS/HMCS       :
```

| Page | Grid | Panels on the page |
| --- | --- | --- |
| BRAKE / AUX LT / SAS | [1,1,2,2] | Emergency Brake System, Auxiliary Lighting Control Panel, SAS Panel |
| IFF | [3,1,2,2] | IFF Panel |
| EMER FLT CTRL | [5,1,1,2] | Emergency Flight Control Panel |
| INTERCOM / STALL | [6,1,2,2] | Intercom Control Panel, Stall Warning Control Panel |
| FUEL SYSTEM | [1,3,1,2] | Fuel System Control Panel, Air Refuel Status Lights |
| THROTTLE | [2,3,2,2] | Throttles Panel, flap lever |
| LASTE | [4,3,1,2] | LASTE Control Panel, ejection seat arm handle |
| RADIO 1 | [5,3,1,2] | AN/ARC-186(V) Radio Control Panel (ARC-210) |
| UHF | [6,3,1,2] | AN/ARC-164 UHF Radio Control Panel |
| VHF FM | [7,3,1,2] | AN/ARC-186(V) VHF FM Radio 2 Control Panel |
| UFC (link) | [1,5,1,4] | opens the CDU tab |
| FIRE / JETT | [2,5,1,4] | Left Engine, APU and Right Engine T-Handles, Fire Extinguisher Discharge, Emergency Jettison Button |
| MFCD L (link) | [3,5,2,1] | opens the MFCD tab, left side |
| CMSC | [3,6,1,2] | Countermeasures Set Control |
| MFCD R (link) | [3,8,2,1] | opens the MFCD tab, right side |
| LANDING GEAR | [5,5,2,1] | Landing Gear and Flap Control Panel, auxiliary gear handle |
| AHCP | [5,6,2,1] | Armament HUD Control Panel, HARS Fast Erect Button |
| NMSP | [5,7,2,1] | Navigation Mode Select Panel |
| CMSP | [1,9,1,2] | Countermeasure Signal Processor Panel |
| CAUTION | [2,9,2,2] | Caution Light Panel |
| CDU (link) | [4,9,1,2] | opens the CDU tab |
| AAP / ILS | [5,9,1,2] | Auxiliary Avionics Panel, ILS Control Panel |
| TACAN | [6,9,1,2] | TACAN Operation and Control Panel |
| HARS / HMCS | [7,9,1,2] | HARS Control Panel, HMCS Control Panel |
| CANOPY / ELEC | [1,11,2,2] | Canopy Switch and Canopy Ejection Handle, Electrical Power Panel |
| ENVIRONMENT | [3,11,3,2] | Environment System Panel |
| LIGHTING | [6,11,2,2] | Lighting Control Panel |

27 boxes: 4 link boxes and 23 panel pages. A box is named after the placard of its panel; a page with several panels joins the names with ` / `.

**Rules for the pages**

- **Plates.** A page is one plate per physical panel inside the 640 × 600 du budget of the panel kit (touch minimum 56 px, see [../SPEC.md](../SPEC.md) section 7). Several panels on one page are separate plates, 16 du apart, as on the AH-64D CENTER page. Lamps and displays are drawn on the plate; a lamp is a touch target only where the real lamp is a button (the IFF REPLY and TEST lamps).
- **Fit.** The yardstick is the AH-64D COMM page: 26 touch targets (volume knobs, PULL chips, switches) fill the whole budget. Up to about 20 touch targets fit; 21 to 26 are tight; more than 26 do not fit. Every page below has a `Fit` line: `fits` or `tight` (check in the layout step). A page that does not fit the 600 du height becomes a **scroll page** (next rule); it is never split and no plate moves to another page.
- **No function in DCS.** A control that the manual calls "no function" is left off the page and listed in section 11, with its DCS-BIOS identifier. Exceptions stay: lamps (so a lamp grid stays whole) and the two switches the cold start uses (SAS MONITOR TEST, STARTUP.md step 160; NVIS LTS, step 13). A position that does nothing (the EMER position of the IFF master dial, ADF on the UHF function dial, DF on the VHF FM mode dial) stays on the dial, greyed out.
- **Scroll page.** Only a page whose plates do not fit is flagged `scroll` in the aircraft file; every other page keeps the fixed 640 × 600 du budget. A scroll page keeps the width of 640 du and the scale of every page (parts stay the same size) and is as tall as its plates. Only its plate area scrolls, vertically; the tabs, the lamp row and the settings button stay fixed. Clear boundaries: the scroll area has a visible frame, an always visible scroll bar at its right edge (iPadOS hides the browser's own), and a shaded edge with a small chevron where more of the page is hidden. Touch: a touch that moves more than 10 px is a scroll and never a tap, a hold or a knob turn; a control acts only on a touch that did not move. The page opens at the top. ENGINE.md E10.
- **Throttle levers.** The two throttle levers are read only in DCS-BIOS: they are shown as gauges on THROTTLE, with no command.
- **Guarded controls.** Controls that end the flight or cannot be undone get the guarded-control rule of the AH-64D spec (a cover, then a tap): the five controls of FIRE / JETT, JTSN on CMSP, the ladder button and the canopy jettison handle on CANOPY / ELEC, LOAD on UHF (it has a real DCS cover, `UHF_COVER`, which the dashboard cover opens).
- **Cold start.** STARTUP.md uses every page except IFF, INTERCOM / STALL, CMSC and HARS / HMCS.

### Panel pages

Counts: `rows` = rows of the PANELS.md tables of the panels on the page; `id` = rows with a DCS-BIOS identifier; `read only` = lamps, gauges and text (no command); `left off` = rows that are not on the page (section 11). `Plus` = controls that exist only in DCS-BIOS and clearly belong to the page. Pictures are the image names of PICTURES.md. A page lists its panels in the order of the cockpit, front to back and top to bottom.

#### BRAKE / AUX LT / SAS

- **Panels:** Emergency Brake System (p. 174), Auxiliary Lighting Control Panel (p. 175), Stability Augmentation System (SAS) Panel (p. 176).
- **Arrangement:** three plates. In the cockpit they are one column, front to back: brake, auxiliary lighting, SAS. On the page: brake above auxiliary lighting on the left, SAS on the right (one column would be too tall).
- **Controls:** 16 rows (2 + 6 + 8), 16 id, 1 read only (the TAKEOFF TRIM lamp), 1 left off (WPN STA STATUS LTS). On the page: 14 controls and 1 lamp.
- **Special:** the EMER BRAKE handle and, above it, an unnamed spring toggle (DCS-BIOS `SEAT_ADJUST`, likely; its title is cut off in the picture). Auxiliary lighting: RSIL dial, NVIS LTS toggle (no function in DCS, kept because the cold start sets it OFF), signal lamp test button (hold), HARS/SAS override toggle, fire detect bleed air test button. SAS: yaw trim knob (L to R), T/O TRIM button with its lamp, four electrically held ENGAGE / OFF toggles (pitch left and right, yaw left and right), and MONITOR TEST (kept although the manual says no function).
- **Picture:** `p174-002.jpg` (partial), `p175-002.jpg` (good), `p177-002.jpg` (good).
- **Fit:** fits (14 touch targets); three plates in two columns, check in the layout step.

#### IFF

- **Panels:** Identify Friend or Foe (IFF) Panel (p. 178).
- **Arrangement:** one plate, as in the figure on p. 179: master mode dial, the four mode toggles M-1, M-2, M-3/A, M-C, the six code wheels (two for Mode 1, four for Mode 3/A), the Mode 4 toggle, the audio / light toggle, and the REPLY and TEST lamps.
- **Controls:** 18 rows, 18 id, 0 read only, 3 left off (RAD TEST, IDENT, code dial). On the page: 15 controls.
- **Special:** master dial with 5 positions (EMER greyed out); the mode toggles have three positions with a shared TEST legend; six digit wheels (Mode 1: two wheels, code 00 to 73; Mode 3/A: four wheels, 0 to 7 each); the REPLY and TEST lamps are push-to-test with a DIM ring (read and command).
- **Picture:** `p179-002.jpg` (good).
- **Fit:** fits (15 touch targets); the six wheels are small, check in the layout step.

#### EMER FLT CTRL

- **Panels:** Emergency Flight Control Panel (p. 180).
- **Arrangement:** one plate: pitch/roll trim switch with the four-way emergency hat, the two emergency retract toggles (SPD BK, FLAP), the aileron and elevator disengage toggles, the FLT CONT toggle, and the four disengage lamps (L-AIL, R-AIL, L-ELEV, R-ELEV; their place is not stated in the figure, they go next to their toggles).
- **Controls:** 11 rows, 11 id, 4 read only (the lamps), 0 left off. On the page: 7 controls and 4 lamps.
- **Special:** the emergency hat has four directions (NOSE DN, NOSE UP, L WING DN, R WING DN) and works only with the trim switch at EMER OVERRIDE; the aileron and elevator toggles have three positions (L, centre, R).
- **Picture:** `p180-002.jpg` (good).
- **Fit:** fits.

#### INTERCOM / STALL

- **Panels:** Intercom Control Panel (p. 182), Stall Warning Control Panel (p. 183).
- **Arrangement:** two plates, intercom above stall warning (stall warning is aft of the intercom in the cockpit).
- **Controls:** 14 rows (12 + 2), 14 id, 0 read only, 1 left off (CALL switch). On the page: 13 controls.
- **Special:** eight listening controls (INT, AIM, FM, VHF, ILS, UHF, TCN, IFF), each a volume knob with an in / out state (two DCS-BIOS ids each, like the AH-64D COMM volume knob with its PULL chip); HM button; VOL knob; rotary selector (INT, FM, VHF, HF). Stall warning: the STALL and PEAK PRFM volume dials.
- **Picture:** `p182-002.jpg` (good), `p183-002.jpg` (good).
- **Fit:** tight: 13 controls plus 8 in / out chips make 21 touch targets. If it does not fit, it is a scroll page.

#### FUEL SYSTEM

- **Panels:** Fuel System Control Panel (p. 158), Air Refuel Status Lights (p. 153).
- **Arrangement:** the fuel plate as listed in PANELS.md, top to bottom: boost pump toggles, EXT TKS toggles, crossfeed and tank gate, the RCVR lever, the four fill disable buttons, the RCVR LT dial. The three air refuel lights are a small second plate (in the cockpit they are on the canopy rail).
- **Controls:** 19 rows (16 + 3 lamps), 19 id, 3 read only (the lamps), 2 left off (LINE CHECK, SIG AMPL). On the page: 14 controls and 3 lamps.
- **Special:** the RCVR lever (CLOSE / OPEN) with the READY, LATCHED and DISCONNECT lights beside it; the fill disable buttons are pull-out buttons (in / out); the "on" positions of the pump toggles have no printed label.
- **Picture:** `p158-002.jpg` (good), `p154-002.jpg` (lights, good).
- **Fit:** fits.

#### THROTTLE

- **Panels:** Throttles Panel (p. 160), flap lever (p. 156).
- **Arrangement:** two plates side by side: the flap lever at the left (in the cockpit it is left of the throttle levers) and the throttles panel at the right, with the two throttle gauges and the friction lever on its left side and the switch column on its right side.
- **Controls:** 10 rows (9 + 1), 10 id, 2 read only (the throttle levers), 0 left off. On the page: 8 controls and 2 gauges.
- **Special:** the throttle levers are gauges (read only). APU switch (START / OFF), engine fuel flow toggles (NORM / OVERRIDE), engine operate toggles (IGN, NORM, MOTOR; spring-loaded, IGN is held), LDG WARN SILENCE button (also on LANDING GEAR), friction lever (`ENGINE_THROTTLE_FRICTION`), flap lever (UP, MVR, DN; DCS-BIOS lists them DN, MVR, UP). The FLAPS DEGREES gauge is on LANDING GEAR.
- **Picture:** `p161-002.jpg` (partial: right lever not shown, friction DECR end cut), flap lever `p508-002.jpg` (poor; screenshot needed).
- **Fit:** fits (8 touch targets); the flap lever plate waits for the screenshot.

#### LASTE

- **Panels:** LASTE Control Panel (p. 163); the ejection seat arm handle.
- **Arrangement:** the LASTE plate (EAC switch, RDR ALTM switch, autopilot select switch, autopilot engage button) and a small second plate for the seat arm handle, which sits at the inboard edge of the console beside LASTE (figure on p. 505).
- **Controls:** 4 rows, 4 id, 0 read only, 0 left off. Plus: `SEAT_ARM` (read and command; 0 = ARM, 1 = DISARM), used by the cold start (STARTUP.md step 4).
- **Special:** autopilot select switch with three positions (PATH, ALT/HDG, ALT); EAC is an electrically held toggle.
- **Picture:** `p165-002.jpg` (good); the seat arm handle has no picture (screenshot needed).
- **Fit:** fits.

#### RADIO 1

- **Panels:** AN/ARC-186(V) Radio Control Panel (p. 167), the ARC-210 radio head of the A-10C II.
- **Arrangement:** one plate, as in the figure: a top row of four buttons (TOD SND, TOD RCV, GPS, RT SELECT), the screen with its three line select buttons beside it and the two brightness buttons, the block of MENU/TIME, XMT/RCV, AM/FM, OFFSET/RCV and ENTER, the SQL knob, the row of five frequency knobs under the screen, and at the bottom the left mode dial, the CHANNEL knob and the right mode dial.
- **Controls:** 24 rows, 24 id, 1 read only (the screen), 0 left off. On the page: 23 controls (14 buttons, 7 knobs, 2 dials) and the screen. Plus: 21 read only controls (20 screen text fields, such as COMSEC mode, active channel, modulation, and `ARC210_PRESENT`).
- **Special:** a display with text (the screen: main frequency and the 20 fields; which fields show on which screen page comes from the DCS research); two 7-position dials with a pull position (ZERO on the left dial, 121 on the right dial); the left-to-right order of the five frequency knobs is assumed.
- **Picture:** `p167-002.jpg` (partial: shadow over the screen and the left knobs).
- **Fit:** tight: 23 touch targets and a screen. If it does not fit, it is a scroll page.

#### UHF

- **Panels:** AN/ARC-164 UHF Radio Control Panel (p. 168). The UHF Frequency Repeater on the dash shows the same two values and is not a second display.
- **Arrangement:** one plate: preset channel selector with the CHAN window, the frequency window (six digits), the five frequency selectors in a row, the mode dial, the function dial, VOL, the squelch toggle, LOAD under its preset cover, TEST DISPLAY, STATUS.
- **Controls:** 16 rows, 16 id, 2 read only (the two windows), 1 left off (T TONE). On the page: 13 controls and 2 windows.
- **Special:** LOAD is under a cover (real DCS cover `UHF_COVER`); 100 MHz selector with 2, 3, A; 0.025 MHz selector with 00, 25, 50, 75; mode dial MNL, PRESET, GRD; function dial OFF, MAIN, BOTH, ADF (ADF greyed out).
- **Picture:** `p168-002.jpg` (partial: LOAD hidden under the open preset card).
- **Fit:** fits.

#### VHF FM

- **Panels:** AN/ARC-186(V) VHF FM Radio 2 Control Panel (p. 171).
- **Arrangement:** one plate: the preset wheel along the bottom with the PRESET window above it, the four frequency knobs with their four windows, LOAD, VOL, mode dial, frequency selection dial, squelch.
- **Controls:** 12 rows, 12 id, 1 read only (the frequency windows), 0 left off. On the page: 10 controls and the windows (the preset window is the same control as the wheel). Plus: 4 read only outputs, the knob turn positions `VHFFM_FREQ1_ROT` to `_FREQ4_ROT`, which turn the drawn knobs.
- **Special:** the frequency knobs step up or down only; the fourth knob has 00, 25, 50, 75; mode dial OFF, TR, DF (DF greyed out); selection dial EMER FM, EMER AM, MAN, PRE.
- **Picture:** `p171-002.jpg` (good).
- **Fit:** fits.

#### FIRE / JETT

- **Panels:** Left Engine "T-Handle" Fire Extinguisher Discharge Select (p. 114), APU "T Handle" Fire Extinguisher Discharge Select (p. 136), RIGHT Engine "T Handle" Fire Extinguisher Discharge Select (p. 147), Fire Extinguisher Discharge (p. 144), Emergency Jettison Button (p. 120).
- **Arrangement:** five small plates, left to right as in the cockpit: EXT STORES JETT button, left engine T-handle, APU T-handle, right engine T-handle, FIRE EXTING DISCH switch. One row or two rows: layout step.
- **Controls:** 8 rows (2 + 2 + 2 + 1 + 1), 8 id, 3 read only (the fire lamps in the handles), 0 left off. On the page: 5 controls and 3 lamps.
- **Special:** every control has a consequence that cannot be undone or ends the flight (guarded controls). The FIRE EXTING DISCH switch has three positions (left, centre, right); spring return is not stated. The three fire lamps are also on the FLIGHT lamp row (section 7).
- **Picture:** `p114-002.jpg`, `p136-002.jpg`, `p147-002.jpg`, `p144-002.jpg`, `p120-000.jpg` (all good).
- **Fit:** fits.

#### LANDING GEAR

- **Panels:** Landing Gear and Flap Control Panel (p. 125); the auxiliary landing gear extension handle.
- **Arrangement:** the gear plate (LIGHTS LAND toggle, downlock override button, gear handle with its lamp, anti-skid toggle, the L, N and R SAFE lamps, the FLAPS DEGREES gauge) and a small second plate for the auxiliary gear handle and its lock button (they are on the dash, not on this panel).
- **Controls:** 10 rows, 10 id, 5 read only (handle lamp, three SAFE lamps, flap gauge), 1 left off (TEMS DATA). On the page: 4 controls, 4 lamps and 1 gauge. Plus: `AUX_GEAR` and `AUX_GEAR_LOCK` (read and command; the cold start uses the handle, STARTUP.md step 44), and `GEAR_HORN_SILENCE` repeated from THROTTLE.
- **Special:** LIGHTS LAND has three positions (LAND, OFF, TAXI); the anti-skid toggle is electrically held; the gear handle (UP, DOWN) has a red lamp in the handle.
- **Picture:** `p126-002.jpg` (partial: LGD GEAR DOWN legend and handle lamp hidden); the auxiliary gear handle has no picture (screenshot needed).
- **Fit:** fits.

#### AHCP

- **Panels:** Armament HUD Control Panel (AHCP) (p. 129), HARS Fast Erect Button (p. 133).
- **Arrangement:** the AHCP plate with its toggles top to bottom (MASTER, GUN/PAC, LASER, TGP, ALT SCE, HUD MODE day/night and norm/standby, CICU, JTRS, IFFCC), and the FAST ERECT button as a small plate below it (in the cockpit it is below the AHCP).
- **Controls:** 11 rows (10 + 1), 11 id, 0 read only, 0 left off.
- **Special:** MASTER, GUN/PAC, LASER, ALT SCE and IFFCC have three positions (ARM, SAFE, TRAIN; ARM, SAFE, GUNARM; ARM, SAFE, TRAIN; BARO, DELTA, RADAR; ON, TEST, OFF); HUD MODE is two toggles (DAY / NIGHT and NORM / STBY).
- **Picture:** `p129-002.jpg` (partial: lower position labels hidden behind the levers), `p133-002.jpg` (good).
- **Fit:** fits (11 touch targets); the plate is tall, check in the layout step.

#### CMSC

- **Panels:** Countermeasures Set Control (CMSC) (p. 136, operation p. 497).
- **Arrangement:** one plate, as in the figure: the three text windows JMR, MWS and CHAFF / FLARE, the two arrow buttons at their left edge, the two small lamps under CHAFF and FLARE, the RWR PRI and SEP buttons, the BRT and AUD knobs at the lower left, the ML lamp beside AUD.
- **Controls:** 13 rows, 13 id, 6 read only (three windows, three lamps), 1 left off (RWR UNK button). On the page: 6 controls (4 buttons, 2 knobs), 3 windows, 3 lamps.
- **Special:** three display windows of 8 characters (JMR, MWS, CHAFF / FLARE); the ML lamp is red; the lower arrow button (`CMSC_MWS`) is "No Function" in DCS-BIOS but not described in the manual (check in DCS).
- **Picture:** `p136-006.jpg` (good), `p497-002.jpg` (good).
- **Fit:** fits.

#### NMSP

- **Panels:** Navigation Mode Select Panel (NMSP) (p. 140).
- **Arrangement:** one plate: the row of lit buttons (HARS, EGI, STR PT, ANCHR, TCN, ILS), the PTR ABLE / STOW toggle, the two HOMING lamps (UHF above FM).
- **Controls:** 10 rows, 10 id, 2 read only (the homing lamps), 1 left off (TISL button: TISL is not available in the A-10C II). On the page: 7 controls and 2 lamps.
- **Special:** each button has a green triangle (`NMSP_*_LED`, read only) that shows as the lit state of the button.
- **Picture:** `p141-002.jpg` (partial: ABLE label hidden behind the PTR lever, homing legends dim).
- **Fit:** fits.

#### CMSP

- **Panels:** Countermeasure Signal Processor (CMSP) Panel (p. 491).
- **Arrangement:** one plate: the display (two lines of four segments) on top, the four SET buttons under the segments, the NXT rocker, RTN button, JTSN switch and BRT knob, the four system switches (MWS, JMR, RWR, DISP) and the mode dial.
- **Controls:** 15 rows, 15 id, 2 read only (the two display lines), 0 left off. On the page: 13 controls and the display.
- **Special:** a display of two lines of 19 characters (4 segments each); the mode dial has five positions (OFF, STBY, MAN, SEMI, AUTO; the DCS-BIOS order is not documented); the system switches have three positions (MENU, ON, OFF; MENU on DISP is momentary); JTSN dumps all chaff and flares (guarded control).
- **Picture:** `p491-002.jpg` (good).
- **Fit:** fits (13 touch targets and a display).

#### CAUTION

- **Panels:** Caution Light Panel (p. 195).
- **Arrangement:** one plate with the lamps in 12 rows of 4 columns, as in the figure and in the order of PANELS.md (row by row, left to right). Two lamps are blank (row 3 column 2, row 7 column 4).
- **Controls:** 49 rows, 48 id, 48 read only, 1 left off (INU AIR HOT: not exported, no function). On the page: 48 lamps (46 legends and 2 blank).
- **Special:** lamps only, no touch target. The longest legend is L-MAIN FUEL LOW (15 characters). Five lamps are "no function" in DCS (ANTI-SKID, SEAT NOT ARMED, SERVICE AIR HOT, WINDSHIELD HOT, IFF MODE-4) and stay on the grid.
- **Picture:** `p195-002.jpg` (good).
- **Fit:** tight. Lamps are not touch targets (no 56 px minimum); rows of about 40 du with a small two-line legend fit the about 528 du usable height. If it does not fit, it is a scroll page.

#### AAP / ILS

- **Panels:** Auxiliary Avionics Panel (AAP) (p. 203), ILS Control Panel and ILS Operation (p. 199).
- **Arrangement:** two plates, AAP above ILS (in the cockpit the ILS panel is directly below the AAP). AAP: the CDU and EGI power switches in the top row, the PAGE and STEER PT dials, the STEER switch at the bottom centre. ILS: the two double knobs and the frequency window.
- **Controls:** 10 rows (5 + 5), 10 id, 1 read only (the ILS window), 0 left off. On the page: 9 controls and the window.
- **Special:** each ILS double knob is two controls (power outer ring `ILS_PWR` and whole MHz base `ILS_MHZ`; volume outer ring `ILS_VOL` and 0.05 base `ILS_KHZ`), drawn as a ring and a base. PAGE dial OTHER, POSITION, STEER, WAYPT (only OTHER allows CDU key entry); STEER PT dial FLT PLAN, MARK, MISSION; the STEER switch is spring-loaded to the centre.
- **Picture:** `p203-002.jpg` (good), `p199-002.jpg` (good).
- **Fit:** fits (9 touch targets, two plates).

#### TACAN

- **Panels:** TACAN Operation and Control Panel (p. 198).
- **Arrangement:** one plate: the channel window on top, the two channel selector knobs, the VOL knob, the TEST button with its lamp, the mode dial.
- **Controls:** 7 rows, 7 id, 2 read only (channel window, test lamp), 0 left off. On the page: 5 controls, the window and the lamp.
- **Special:** the channel window shows 4 characters (three digits and X or Y); the middle selector sets the units digit and, separately, X or Y (`TACAN_XY`); the mode dial has five positions (OFF, REC, T/R, A/A REC, A/A T/R).
- **Picture:** `p198-002.jpg` (good).
- **Fit:** fits.

#### HARS / HMCS

- **Panels:** Heading and Attitude Reference Systems (HARS) Control Panel (p. 200), Helmet Mounted Cueing System (HMCS) Control Panel (p. 201).
- **Arrangement:** two plates, HMCS above HARS (as in the cockpit). HARS: the SYN-IND window on top, then the SLAVE / DG mode switch, the LAT dial, the PUSH TO SYNC knob, the MAG VAR switch and the hemisphere switch. HMCS: the power switch.
- **Controls:** 9 rows (6 + 3), 7 id, 1 read only (SYN-IND), 2 left off (the HVI UNSAFE and REPLACE BATTERY legends have no DCS-BIOS output). On the page: 6 controls and the SYN-IND needle.
- **Special:** SYN-IND is a needle gauge, centred means aligned; the PUSH TO SYNC knob is two controls (press `HARS_PTS`, turn `HARS_HDG`); MAG VAR has three positions (+15, 0, -15); the HMCS switch has three positions (ON, OFF, BAT).
- **Picture:** `p200-002.jpg` (good), `p201-002.jpg` (good).
- **Fit:** fits.

#### CANOPY / ELEC

- **Panels:** Cockpit Canopy Switch and Canopy Ejection Handle (p. 186), Electrical Power Panel (p. 187); the CANOPY UNLOCKED lamp of Marker and Canopy Lights (p. 148).
- **Arrangement:** two plates, canopy above electrical power (front to back as in the cockpit). Electrical: APU GEN, INVERTER and EMER FLOOD in the top row; AC GEN left, AC GEN right and BATTERY in the bottom row.
- **Controls:** 9 rows (3 + 6), 9 id, 0 read only, 0 left off. Plus: `CANOPY_JTSN_UNLOCK` (command), `CANOPY_DISENGAGE` (canopy actuator disengage lever, command) and `CANOPY_POS` (read only, canopy position), and the CANOPY UNLOCKED lamp (also on the lamp row).
- **Special:** the canopy switch (OPEN, HOLD, CLOSE; OPEN and CLOSE are held); the ladder button under a cover (real DCS cover `LADDER_EXTEND_COVER`); the canopy jettison handle (guarded control, with its unlock); the INVERTER switch is spring-loaded (TEST); the three-position toggles of the electrical panel (PWR, OFF/RESET).
- **Picture:** `p187-002.jpg` (partial: ladder button under its cover), `p188-000.jpg` (good). The canopy actuator disengage lever has no picture.
- **Fit:** fits (12 touch targets, two plates).

#### ENVIRONMENT

- **Panels:** Environment System Panel (p. 189).
- **Arrangement:** one tall plate: the oxygen regulator in the upper half (FLOW indicator, supply pressure gauge, the three levers, the quantity gauge, OXY IND TEST button), the air controls below (defog / deice, canopy defog dial, pitot heat, bleed air, TEMP/PRESS, main air supply, flow level dial, CABIN AIR COND, cabin pressure gauge).
- **Controls:** 18 rows, 18 id, 4 read only (flow indicator, pressure gauge, quantity gauge, cabin pressure gauge), 2 left off (rain remove and wash switch, temperature level dial). On the page: 12 controls and 4 gauges.
- **Special:** three oxygen levers (emergency: spring-loaded, only NORMAL works; dilution; supply); several toggles have an unprinted ON label; the order of the flow level dial positions is unclear in the manual (check in DCS); CABIN AIR COND has three positions in the manual and four states in DCS-BIOS.
- **Picture:** `p189-002.jpg` (partial: rain remove labels under the amber lever, ON labels unprinted).
- **Fit:** tight: 12 touch targets and 4 gauges on a panel taller than wide; if it does not fit, it is a scroll page.

#### LIGHTING

- **Panels:** Lighting Control Panel (p. 191).
- **Arrangement:** one plate, row by row as in PANELS.md: the exterior block on top (POSITION, FORMATION, ANTI-COLLISION, NOSE ILLUM), the cockpit block below (ENG INST, AUX INST, SIGNAL LTS, FLT INST, ACCEL & COMP, FLOOD, CONSOLE).
- **Controls:** 11 rows, 11 id, 0 read only, 0 left off: 5 toggles and 6 dials. The six DCS-BIOS-only brightness outputs (`INT_*_L_BRIGHT`) are not shown: the dials give their own position.
- **Special:** the FLOOD dial goes past BRT to TSTORM; POSITION has three positions (FLASH, OFF, STEADY); ANTI-COLLISION is electrically held.
- **Picture:** `p192-002.jpg` (good).
- **Fit:** fits (11 touch targets).

### Link boxes

| Box | Opens | Controls |
| --- | --- | --- |
| MFCD L | MFCD tab, left side | bezel of the left MFCD (p. 121), section 5 |
| MFCD R | MFCD tab, right side | bezel of the right MFCD (p. 144, same bezel), section 5 |
| CDU | CDU tab | Control Display Unit (p. 205), section 6 |
| UFC | CDU tab | Up Front Controller (p. 303), section 6 |

### Pages that may not fit

- **CAUTION:** tight (48 lamps in 12 rows). Lamps are not touch targets, so the 56 px touch minimum does not apply; rows of about 40 du with a small two-line legend fit the about 528 du usable height. Scroll page if the layout check fails.
- **RADIO 1:** tight (23 touch targets and a screen). Scroll page if the check fails.
- **INTERCOM / STALL:** tight (21 touch targets with the in / out chips). Scroll page if the check fails.
- **ENVIRONMENT:** tight (a tall panel). Scroll page if the check fails.
- Every other page fits by the yardstick (20 touch targets or fewer); the IFF code wheels, AHCP and BRAKE / AUX LT / SAS are to check in the layout step.

## 3. FLIGHT

The quick page for take-off, landing and flying, on the fixed 7 × 3 grid (`grid: [row, col, rows, cols]`). Flight instruments are not drawn (cockpit-replica graphics are out of scope, [../SPEC.md](../SPEC.md) section 11); FLIGHT shows the few values a pilot sets or checks from the tablet, as text or simple bars.

| Control | Type | Source | Grid |
| --- | --- | --- | --- |
| SPEED BRAKE | two key buttons EXTEND / RETRACT (hold = keep moving, as the real switch) | keybinds `speed_brake_extend`, `speed_brake_retract`; position shown from `EXT_SPEED_BRAKE_LEFT` (external model, read only) | [1,1,1,1] |
| TRIM | key hat: up / down / left / right (a tap trims one step, a hold keeps trimming) | keybinds `trim_up`, `trim_down`, `trim_left`, `trim_right` | [1,2,2,1] |
| GEAR | selector UP / DOWN with the three SAFE lamps and the handle lamp | `GEAR_LEVER`; `GEAR_L_SAFE`, `GEAR_N_SAFE`, `GEAR_R_SAFE`, `HANDLE_GEAR_WARNING` | [1,3,2,1] |
| FLAPS | selector UP / MVR / DN with the position as text (degrees) | `FLAPS_SWITCH`; `FLAP_POS` | [1,4,2,1] |
| LIGHTS LAND | selector LAND / OFF / TAXI | `LANDING_LIGHTS` | [1,5,1,1] |
| ANTI-SKID | selector | `ANTI_SKID_SWITCH` | [2,5,1,1] |
| NWS | key button (nosewheel steering engage / disengage on the ground) with the STEERING ENGAGED lamp | keybind `nws`; `NOSEWHEEL_STEERING` | [1,6,1,1] |
| THROTTLE L / R | two read-only bars 0 to 100 % | `ENG_THROTTLE_L`, `ENG_THROTTLE_R` | [1,7,3,1] |
| FUEL | total fuel as text (pounds) | `FUEL_QTY_10000`, `FUEL_QTY_1000`, `FUEL_QTY_100` (counters) | [3,1,1,2] |
| EMER BRAKE | selector PULL / IN (DCS-BIOS, no key) | `EMER_BRAKE` | [3,3,1,1] |
| HARS FAST ERECT | button | `HARS_FAST_ERECT` | [3,4,1,1] |

Speed brake, trim and NWS are keypresses with no confirmation (`confirmed: null`), as the AH-64D key buttons. Exact keys: section 8.

## 4. FIGHT

The quick page for weapons and sensors, on the fixed 7 × 3 grid. The HOTAS controls are **key hats**: one grid cell per hat with its four directions (and a centre button where the real hat can be pressed). A tap sends a short press (0.15 s), a hold of 0.6 s on the tablet sends a long press (the key held 1.0 s), as the manual separates short and long. Labels show the function that is the same for every sensor of interest (SOI), and a short generic word where the function depends on the SOI (the dashboard cannot read the SOI: it has no DCS-BIOS output).

| Control | Directions (short / long) | Grid |
| --- | --- | --- |
| DMS (Data Management Switch) | up, down, left, right; short and long (labels: SOI-dependent, e.g. "UP", "DN") | [1,1,1,1] |
| TMS (Target Management Switch) | up: TRACK / MAKE SPI; down: UNHOOK / SPI TO STPT; left: ACK / SPI BCAST; right: MARK / MARK SPI | [1,2,1,1] |
| CMS (Countermeasures Switch) | up: 1 FLARE / NEXT PROG; down: 1 CHAFF / PREV PROG; left: 6 FLARES; right: 6 CHAFF; centre: PROG ON-OFF / ECM ON-OFF | [1,3,1,1] |
| COOLIE HAT | up: SOI HUD / MSG LOOK; down: SOI HMCS / DSMS LOOK; left: L MFCD PAGE / SOI L MFCD; right: R MFCD PAGE / SOI R MFCD | [1,4,1,1] |
| CHINA HAT | forward: FOV-type / SLAVE ALL TO SPI; aft: CAGE-type / TGP TO STPT | [1,5,1,1] |
| MASTER MODE (MMCB) | one button: tap = HUD mode, hold = A-A | [1,6,1,1] |
| MASTER ARM | selector TRAIN / SAFE / ARM | `AHCP_MASTER_ARM`, [2,1,1,1] |
| GUN / PAC | selector GUNARM / SAFE / ARM | `AHCP_GUNPAC`, [2,2,1,1] |
| LASER | selector TRAIN / SAFE / ARM | `AHCP_LASER_ARM`, [2,3,1,1] |
| TGP | selector OFF / ON | `AHCP_TGP`, [2,4,1,1] |
| CHAFF / FLARE | display of the CMSC count text | `CMSC_TXT_CHAFF_FLARE`, [2,5,1,2] |
| CMSP | display of the two CMSP lines | `CMSP1`, `CMSP2`, [3,1,1,3] |
| GUN READY | lamp | `GUN_READY`, [1,7,1,1] |

The CMS and coolie hat functions are the same in every SOI (manual pp. 106–112, PANELS.md "Control Stick" and "Throttles"); the CMS mapping differs between p. 106 and pp. 493 / 496 and is checked in the DCS research (RESEARCH.md). The key hat is a small extension of the existing `hat` control: the same widget, with key names instead of DCS-BIOS axes and a long press (decided in phase 6, ENGINE.md E8; six cells for 20 keys and 40 functions with short and long keep the 7 × 3 grid usable). The trigger and weapon release are not on the dashboard (section 11).

## 5. MFCD

Both MFCDs, hand-drawn like the AH-64D MPD (ENGINE.md E5): one bezel at a time, a switch LEFT MFCD / RIGHT MFCD, the side preselected by the map boxes MFCD L and MFCD R and remembered per aircraft (E9).

- **Bezel:** 20 option select buttons (OSB 1 to 5 on top, 6 to 10 on the right, 11 to 15 at the bottom, 16 to 20 on the left; `LMFD_01` … `LMFD_20`, `RMFD_01` … `RMFD_20`), the ADJ and BRT rockers (`LMFD_ADJ`, `LMFD_BRT` and the right ones) and the DAY / NT / OFF knob (`LMFD_PWR`, `RMFD_PWR`). The DSP, CON and SYM rockers are drawn but inert (no function in DCS; section 11). Drawing reference: PICTURES.md, Left MFCD p121-002.jpg.
- **Screen:** empty in version 1: DCS-BIOS has no MFCD text, and the export script table of the A-10C is empty (E7). The OSB numbers are printed small beside the buttons. Live OSB labels can follow later through `list_indication`, as for the AH-64D MPD, once phase 7 has found the MFCD indication numbers.
- OSB presses are DCS-BIOS buttons with readback; the rockers are 3-position spring switches (down, centre, up) held for the press time.

## 6. CDU

The CDU and the UFC on one tab, hand-drawn like the AH-64D KU (E5). Side by side if both fit at the 56 px touch minimum on a 1180 × 820 screen, else a switch CDU / UFC like the MFCD side switch (decided in the layout step).

- **CDU screen:** live, 10 lines of 24 characters from `CDU_LINE0` … `CDU_LINE9` (DCS-BIOS builds them from the CDU indication; the scratchpad is line 10 of the real screen, inside `CDU_LINE9`). Monospace, green on black, as the real screen.
- **CDU keys:** 8 line select keys (L3, L5, L7, L9, R3, R5, R7, R9: `CDU_LSK_3L` … `CDU_LSK_9R`) beside the screen lines they serve; the function keys SYS, NAV, WP, OSET, FPM, PREV; the letter and digit keys, point and slash; CLR, BCK, SPC, FA, MK; the rockers BRT / DIM (`CDU_BRT`), page (`CDU_PG`), blank (`CDU_SCROLL`) and +/− (`CDU_DATA`). The two unlabelled keys (`CDU_NA1`, `CDU_NA2`) are drawn but inert.
- **AAP PAGE:** the CDU keys work only with the AAP PAGE dial at OTHER, so the CDU tab also shows the AAP PAGE selector (`AAP_PAGE`: OTHER, POSITION, STEER, WAYPT) and the STEER PT selector (`AAP_STEERPT`).
- **UFC:** the keypad (digits 0 to 9 = `UFC_1` … `UFC_10`, SPC, HACK, FUNC, LTR, CLR, ENT, MK, ALT ALRT), the rockers (STEER, DATA, SEL, DEPR, INTEN), the MASTER CAUTION lamp and reset button (`MASTER_CAUTION`, `UFC_MASTER_CAUTION`) and the six A-10C II buttons COM 1, COM SEC, IFF, COM 2, ECCM, IDM. Their positions in the drawing are open (RESEARCH.md: the six unlabelled buttons of the manual figure); they are placed after the DCS research. Several UFC keys act on the HUD only; the dashboard shows no result for them.

## 7. Lamp row

The row of lamps at the top of every page (as on the AH-64D).

| View | Lamps |
| --- | --- |
| COCKPIT map and every panel page | MASTER CAUTION (a lighted push button: `MASTER_CAUTION`, press = `UFC_MASTER_CAUTION`) |
| COCKPIT map | also GUN READY, STEERING ENGAGED, MARKER BEACON, CANOPY UNLOCKED (`GUN_READY`, `NOSEWHEEL_STEERING`, `MARKER_BEACON`, `CANOPY_UNLOCKED`) |
| FLIGHT | MASTER CAUTION, L ENG FIRE, APU FIRE, R ENG FIRE (`L_ENG_FIRE`, `APU_FIRE`, `R_ENG_FIRE`), CANOPY UNLOCKED |
| FIGHT | MASTER CAUTION, GUN READY, missile launch (`CMSC_LAUNCH`) |
| MFCD, CDU | none |

The A-10C has no MASTER WARNING lamp of the AH-64D kind; the caution light panel (48 lamps) is a COCKPIT page.

## 8. Keybinds

DCS-BIOS has no HOTAS control, so these functions are keypresses ([../SPEC.md](../SPEC.md) section 4). The aircraft file holds their defaults in `KEYS`; `[keys]` in `config/config.toml` overrides them (E8). The defaults are **open**: they are taken from the A-10C default keybinds once the module is installed and its control list is exported from DCS (Options, Controls, "Make HTML"). Keys the key table does not know yet (numpad, Tab, Esc, punctuation) are added to `core/keys.py` then (E8). Until then the key controls cannot be built (the bridge checks every needed key at start).

| Key name | DCS command (A-10C) | Used on |
| --- | --- | --- |
| `dms_up`, `dms_down`, `dms_left`, `dms_right` | Data Management Switch directions | FIGHT |
| `tms_up`, `tms_down`, `tms_left`, `tms_right` | Target Management Switch directions | FIGHT |
| `cms_up`, `cms_down`, `cms_left`, `cms_right`, `cms_press` | Countermeasures Switch directions and press | FIGHT |
| `coolie_up`, `coolie_down`, `coolie_left`, `coolie_right` | Coolie hat directions | FIGHT |
| `china_fwd`, `china_aft` | China hat forward and aft | FIGHT |
| `mmcb` | Master Mode Control Button | FIGHT |
| `speed_brake_extend`, `speed_brake_retract` | Speed brake extend and retract | FLIGHT |
| `trim_up`, `trim_down`, `trim_left`, `trim_right` | Trim hat directions | FLIGHT |
| `nws` | Nosewheel steering button | FLIGHT |

A long press is the same key held 1.0 s; no extra key names. The AH-64D keys (power levers, trim reset, canopy, monocle, controls overlay, George) are not needed for the A-10C (E3, E4).

## 9. Engine behaviour for the A-10C

The engine changes of [ENGINE.md](ENGINE.md) (E1 to E10) as they apply to this aircraft.

- **E1 Aircraft choice.** `aircraft/a10c.py` lists `DCS_NAMES = ["A-10C_2"]` and `DCSBIOS_MODULE = "A-10C"`. The bridge reads `_ACFT_NAME` from the DCS-BIOS stream and switches to the A-10C files when it reads `A-10C_2`; the page reloads its layout. `[dcs] aircraft = "auto"` is the default; a fixed value forces an aircraft. The settings page shows the detected aircraft and has a switch AUTO / AH-64D / A-10C for debugging (it overrides the detection until set back to AUTO or the bridge restarts).
- **E2 Seats.** One seat: `SEATS = [{"prefix": "", "label": "A-10C"}]`, `SEAT_OUTPUT = None`. The badge shows `A-10C`; no seat switch, no debug-seat hold; "DCS data present" comes from the packet age.
- **E3 Trim.** No trim display; no trim tracking; `trim_reset` is not required.
- **E4 Throttles.** No `lever` control; the throttle positions are read-only bars on FLIGHT (a read-only bar is a small new display type, decided in phase 6 with the key hat of section 4, ENGINE.md E8). No `power_*` keys required.
- **E5 Displays.** New hand-drawn layouts `mfcd` and `cdu` (CDU and UFC) in the page, next to `mpd` and `ku`.
- **E6 Look.** A second plate style for A-10C panel pages (section 10), chosen by the aircraft file.
- **E7 Export script.** The script's table for `A-10C_2` is empty in version 1; the bridge needs no export data for the A-10C.
- **E8 Keys.** The A-10C `KEYS` (section 8); key table extended when the defaults are known.
- **E9 Memory and docs.** The remembered tab and MFCD side are stored per aircraft; this spec and the README aircraft section describe the A-10C.
- **E10 Scroll page.** Only the panel pages that do not fit are scroll pages (section 2, "Scroll page").

## 10. A-10C look

The A-10C panel pages are drawn in an A-10C style, different from the AH-64D plates (E6). Reference: the manual renders listed in [PICTURES.md](PICTURES.md) (48 of 66 panels have a good picture).

- **Plates:** dark grey, flat panels with a thin lighter edge; corner fasteners (round slotted Dzus heads) instead of the AH-64D ears and screws; panels in a console column sit edge to edge.
- **Labels:** white sans-serif placard text, position labels beside the switches, as in the renders.
- **Switches:** chrome bat-handle toggles; guarded switches with a red or striped cover where the real panel has one; rotary knobs black with a white pointer line.
- **Lamps and buttons:** legend lamps with the text on the lamp face; lit colours green, amber, red and white (the panel kit gets a plain LAMP part and the red / white lit styles, E6).
- **Same mechanics:** touch areas, chooser, knob bar, guard covers and the panel-kit layout rules stay those of the engine; only the drawing style changes. Details (colours, sizes) are fixed in the layout step with the pictures.

## 11. Not on the dashboard

Left off on purpose in version 1, one line each.

**Panels and groups**

- **KY-58 secure voice panel** (6 controls): no function in DCS.
- **TISL control panel** (9 controls) and the TISL button of the NMSP: the Pave Penny pod is removed in the A-10C II and TISL navigation is not available (manual p. 546); the only picture is low resolution.
- **Circuit breaker panel** (38 controls, DCS-BIOS only): rarely used.
- **DVADR** (6 controls, DCS-BIOS only): no manual description, no function known.
- **Antenna panel** (3 switches, DCS-BIOS only): no manual description.
- **VHF AM radio head** (16 controls, DCS-BIOS only): not fitted in the A-10C II, the ARC-210 on RADIO 1 replaces it (DCS-BIOS exports one of the two at run time).
- **HUD**: no DCS-BIOS output; the HUD is not shown.
- **Trigger and weapon release** (stick): keybinds only, kept on the real stick so a tablet tap never fires a weapon.

**Outputs and toggles**

- **External aircraft model outputs** (16: speed brakes, wing and tail lights, weight on wheels of the outside model): not cockpit controls.
- **Mirrors and stick hide** (`MIRROR_TOGGLE`, `STICK_HIDE`): view toggles, not cockpit controls.
- **Ground safety override** (`GND_SAFE_OVERRIDE` with its cover) and **anti-G suit test button** (`SUIT_TEST`): DCS-BIOS only; the manual does not describe them and their place in the cockpit is not known.
- **Lighting brightness outputs** (6, `INT_*_L_BRIGHT`): the dials of LIGHTING give their own position.
- **HMCS legends** HVI UNSAFE and REPLACE BATTERY: no DCS-BIOS output.
- **INU AIR HOT** caution lamp: not exported, no function.

**Controls with no function in DCS** (the manual says so; all but the last row have a DCS-BIOS identifier that does nothing). The cold start does not use them.

| Control | Page it would be on | Identifier |
| --- | --- | --- |
| LINE CHECK button | FUEL SYSTEM | `FSCP_LINE_CHECK` |
| SIG AMPL switch | FUEL SYSTEM | `FSCP_AMPL` |
| TEMS DATA switch | LANDING GEAR | `ENGINE_TEMS_DATA` |
| T TONE toggle | UHF | `UHF_T_TONE` |
| WPN STA STATUS LTS dial | BRAKE / AUX LT / SAS | `ALCP_WPNSTA` |
| RAD TEST switch | IFF | `IFF_RADTEST` |
| IDENT switch | IFF | `IFF_MIC_IDENT` |
| IFF code dial | IFF | `IFF_CODE` |
| CALL switch | INTERCOM / STALL | `INT_CALL` |
| RWR UNK button | CMSC | `CMSC_UNK` |
| Windshield rain remove and wash switch | ENVIRONMENT | `ENVCP_WRRW` |
| Temperature level dial | ENVIRONMENT | `ENVCP_TEMP_LEVEL` |
| HVI UNSAFE and REPLACE BATTERY legends | HARS / HMCS | none (not exported) |

The NMSP TISL button is in the TISL line above. The SAS MONITOR TEST switch and the NVIS LTS switch also read "no function" in the manual, but the cold start uses them (STARTUP.md steps 160 and 13), so they stay on their page.

## 12. Manual test run (A-10C)

Preparation: the A-10C II module, DCS-BIOS, the export script, the A-10C keybinds (section 8). A throwaway single-player mission, cold and dark on the ground.

1. **Aircraft choice.** Start the bridge, then an AH-64D mission: the AH-64D dashboard appears. Switch to an A-10C mission: the page reloads with the A-10C tabs and the badge `A-10C`, without a restart. In the settings page, switch to AH-64D and back to AUTO.
2. **Cold start from the tablet.** Follow [STARTUP.md](STARTUP.md) on the COCKPIT pages as far as the tablet allows (power, APU, engines with the real throttle, avionics, MFCDs, CDU alignment, countermeasures, SAS). Note every step that fails or shows "not confirmed".
3. **COCKPIT.** Every page opens from the map and from the page list; switches, knobs and lamps follow the cockpit when you move them with the mouse.
4. **CDU.** The 10 screen lines match the cockpit; type a waypoint name with the keys; the line select keys act on their lines; AAP PAGE at OTHER.
5. **MFCD.** OSB 1 to 20 of both MFCDs change pages; ADJ, BRT and DAY / NT / OFF act.
6. **FLIGHT.** Speed brake extend and retract (the position bar moves), trim in four directions, gear and flaps on the ground (gear handle only with the override, as in the cockpit), landing lights, NWS, throttle bars follow the real throttle.
7. **FIGHT.** Each key hat direction short and long with the TGP and the TAD as SOI; CMS flare and chaff (counts change); MASTER ARM, GUN / PAC, LASER, TGP.
8. **Open points.** Check the items of [RESEARCH.md](RESEARCH.md) "Open points" that need DCS (CMS mapping, UFC buttons, OSB page links, ARC-210 knob order, AAP STEER, MFCD DSP / CON / SYM).

Done when a cold start to taxi works from the tablet plus the real throttle, and every page acts in DCS.
