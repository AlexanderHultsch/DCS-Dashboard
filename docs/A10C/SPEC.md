# DCS-Dashboard – A-10C II

Specification of the A-10C II Tank Killer dashboard (planned, not built). The engine all aircraft share is in [../SPEC.md](../SPEC.md); the engine changes this aircraft needs and their decisions are in [ENGINE.md](ENGINE.md). Controls are named as in [PANELS.md](PANELS.md), DCS-BIOS identifiers are in [BIOS.md](BIOS.md), reference pictures in [PICTURES.md](PICTURES.md), the cold start in [STARTUP.md](STARTUP.md).

## 1. Overview

## 2. COCKPIT

COCKPIT is a simplified map of the A-10C II cockpit and one page for every cockpit panel that has a function in DCS, with every button, switch, knob and display of that panel. Tap a box on the map to open its page; on a page the COCKPIT tab keeps its highlight and shows a back chevron, and one tap on it goes back to the map; a long hold (0.5 s) on COCKPIT opens a list of every page. The boxes MFCD L, MFCD R, CDU and UFC are not pages: they open the MFCD tab (left or right side preselected) and the CDU tab (the UFC sits on the CDU tab), as the AH-64D map boxes open MPD and KU. The A-10C has one seat, so there is no seat badge switch and no seat-dependent page: every page is always on the map and in the list.

Tabs at the top: **COCKPIT | FLIGHT | FIGHT | MFCD | CDU**.

The panel pages get the A-10C look (drawn later); this section only says which panels are on which page and where. The instruments (ADI, HSI, standby instruments, altimeter, VVI, airspeed, AoA, engine instruments, fuel and hydraulic gauges, accelerometer, compass, clock, RWR scope) are displays for FLIGHT and FIGHT, and the HOTAS grips are controls for FIGHT and FLIGHT: none of them is a panel page. The small controls that sit on an instrument (cage knob, set knobs, clock keys, fuel selector) go with that instrument. The lamp row (section 7) stays at the top of the map and of every panel page.

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
- **Fit.** The yardstick is the AH-64D COMM page: 26 touch targets (volume knobs, PULL chips, switches) fill the whole budget. Up to about 20 touch targets fit; 21 to 26 are tight; more than 26 do not fit. Every page below has a `Fit` line: `fits`, `tight` (check in the layout step) or `probably not` (with a proposal).
- **No function in DCS.** A control that the manual calls "no function" is left off the page and listed in section 11, with its DCS-BIOS identifier. Exceptions stay: lamps (so a lamp grid stays whole) and the two switches the cold start uses (SAS MONITOR TEST, STARTUP.md step 160; NVIS LTS, step 13). A position that does nothing (the EMER position of the IFF master dial, ADF on the UHF function dial, DF on the VHF FM mode dial) stays on the dial, greyed out.
- **Throttle levers.** The two throttle levers are read only in DCS-BIOS: they are shown as gauges on THROTTLE, with no command.
- **Guarded candidates.** Some controls end the flight or cannot be undone. They are candidates for the guarded-control rule of the AH-64D spec (a cover, then a tap): the five controls of FIRE / JETT, JTSN on CMSP, the ladder button and the canopy jettison handle on CANOPY / ELEC, LOAD on UHF (it has a real DCS cover, `UHF_COVER`). Whether they get the rule is decided outside this section.
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
- **Fit:** tight: 13 controls plus 8 in / out chips make 21 touch targets. If it does not fit, STALL WARNING moves to the BRAKE / AUX LT / SAS page.

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
- **Fit:** tight: 23 touch targets and a screen. If it does not fit, split the plate: screen and buttons on one page, knobs and dials on a second.

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
- **Special:** every control has a consequence that cannot be undone or ends the flight (guarded candidates). The FIRE EXTING DISCH switch has three positions (left, centre, right); spring return is not stated. The three fire lamps are also candidates for the lamp row.
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
- **Special:** a display of two lines of 19 characters (4 segments each); the mode dial has five positions (OFF, STBY, MAN, SEMI, AUTO; the DCS-BIOS order is not documented); the system switches have three positions (MENU, ON, OFF; MENU on DISP is momentary); JTSN dumps all chaff and flares (guarded candidate).
- **Picture:** `p491-002.jpg` (good).
- **Fit:** fits (13 touch targets and a display).

#### CAUTION

- **Panels:** Caution Light Panel (p. 195).
- **Arrangement:** one plate with the lamps in 12 rows of 4 columns, as in the figure and in the order of PANELS.md (row by row, left to right). Two lamps are blank (row 3 column 2, row 7 column 4).
- **Controls:** 49 rows, 48 id, 48 read only, 1 left off (INU AIR HOT: not exported, no function). On the page: 48 lamps (46 legends and 2 blank).
- **Special:** lamps only, no touch target. The longest legend is L-MAIN FUEL LOW (15 characters). Five lamps are "no function" in DCS (ANTI-SKID, SEAT NOT ARMED, SERVICE AIR HOT, WINDSHIELD HOT, IFF MODE-4) and stay on the grid.
- **Picture:** `p195-002.jpg` (good).
- **Fit:** tight. Lamps are not touch targets (no 56 px minimum); rows of about 40 du with a small two-line legend fit the about 528 du usable height. Fallback: two pages CAUTION 1 (rows 1 to 6) and CAUTION 2 (rows 7 to 12).

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
- **Special:** the canopy switch (OPEN, HOLD, CLOSE; OPEN and CLOSE are held); the ladder button under a cover (real DCS cover `LADDER_EXTEND_COVER`); the canopy jettison handle (guarded candidate, with its unlock); the INVERTER switch is spring-loaded (TEST); the three-position toggles of the electrical panel (PWR, OFF/RESET).
- **Picture:** `p187-002.jpg` (partial: ladder button under its cover), `p188-000.jpg` (good). The canopy actuator disengage lever has no picture.
- **Fit:** fits (12 touch targets, two plates).

#### ENVIRONMENT

- **Panels:** Environment System Panel (p. 189).
- **Arrangement:** one tall plate: the oxygen regulator in the upper half (FLOW indicator, supply pressure gauge, the three levers, the quantity gauge, OXY IND TEST button), the air controls below (defog / deice, canopy defog dial, pitot heat, bleed air, TEMP/PRESS, main air supply, flow level dial, CABIN AIR COND, cabin pressure gauge).
- **Controls:** 18 rows, 18 id, 4 read only (flow indicator, pressure gauge, quantity gauge, cabin pressure gauge), 2 left off (rain remove and wash switch, temperature level dial). On the page: 12 controls and 4 gauges.
- **Special:** three oxygen levers (emergency: spring-loaded, only NORMAL works; dilution; supply); several toggles have an unprinted ON label; the order of the flow level dial positions is unclear in the manual (check in DCS); CABIN AIR COND has three positions in the manual and four states in DCS-BIOS.
- **Picture:** `p189-002.jpg` (partial: rain remove labels under the amber lever, ON labels unprinted).
- **Fit:** tight: 12 touch targets and 4 gauges on a panel taller than wide; check in the layout step.

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

- **CAUTION:** tight (48 lamps in 12 rows). Lamps are not touch targets, so the 56 px touch minimum does not apply; rows of about 40 du with a small two-line legend fit the about 528 du usable height. Fallback if the layout check fails: CAUTION 1 and CAUTION 2.
- **RADIO 1:** tight (23 touch targets and a screen). Proposal: two pages if the check fails.
- **INTERCOM / STALL:** tight (21 touch targets with the in / out chips). Proposal: STALL WARNING moves to BRAKE / AUX LT / SAS.
- **ENVIRONMENT:** tight (a tall panel). Check in the layout step.
- Every other page fits by the yardstick (20 touch targets or fewer); the IFF code wheels, AHCP and BRAKE / AUX LT / SAS are to check in the layout step.

## 3. FLIGHT

## 4. FIGHT

## 5. MFCD

## 6. CDU

## 7. Lamp row

## 8. Keybinds

## 9. Engine behaviour for the A-10C

## 10. A-10C look

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
