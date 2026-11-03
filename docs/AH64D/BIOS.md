# AH-64D – DCS-BIOS mapping

Maps every control in [PANELS.md](PANELS.md) to its DCS-BIOS identifier. Source: the DCS-Skunkworks DCS-BIOS module `AH-64D` (`Scripts/DCS-BIOS/lib/modules/aircraft_modules/AH-64D.lua`, version v1.2d), which serves the DCS aircraft `AH-64D_BLK_II`. The module has 714 controls: 353 with the prefix `PLT_` (pilot), 328 with the prefix `CPG_` (CP/G) and 33 without a seat (5 radio frequencies, 22 of the external model, 5 vibration gauges, the seat). Input kinds, build types and position orders come from the table that `core/tools/test/bios_check.py` makes for all 714 ids (see its row in `core/tools/test/README.md`), checked against the module Lua and against `aircraft/ah64d.py`, the dashboard's AH-64D data, which was tested in DCS in both seats.

The AH-64D has two crew stations and DCS-BIOS has one control per station, with the prefix `PLT_` or `CPG_`. An identifier that exists in both stations is written once with the placeholder `{S}_` (the dashboard's own convention): `{S}_FIRE_APU_BTN` stands for `PLT_FIRE_APU_BTN` and `CPG_FIRE_APU_BTN`. An identifier that exists for one station only is written in full (`PLT_ENG_1_FIRE_L`). Where the two stations have different identifiers for one control, the cell lists both. The panels that exist in both stations are mapped once, in the Pilot cockpit area; a Note names what differs in the CP/G station.

Sections and control names follow PANELS.md. Columns:

- **DCS-BIOS identifier**: the name used to read and command the control; `—` if there is none. A control with several parts (button and lamp, two axes, left and right MFD) lists all its identifiers.
- **Access**: `read + command` (an input and an output exist), `read only` (lamps, gauges, text: `defineIndicatorLight`, `defineFloat`, `defineString`, `defineIntegerFromGetter`), or `—`. A row with several identifiers shows `read + command` if any of them takes commands; the Note then names the read only ones and the ones without an output.
- **Build**: the dashboard control the identifier becomes, from the classification table: `button` (push button), `selector (N)` (N fixed positions; `spring` = spring-loaded, returns to the middle), `knob` (continuous, 0 to 65535), `step rocker (3200)` (relative only: step up or down, the position comes back as `<id>_KNOB_POS`), `lamp`, `display` (text), `bar or gauge` (0 to 65535), `none` (metadata: the table has no better class for an output made by `defineIntegerFromGetter`). `NO READBACK` is appended where no output is named like the identifier, so the dashboard cannot read the state under its own name. With several identifiers of different builds the cell reads `identifiers: build`. For a control without an identifier the cell holds the gap: `keybind` (needs a DCS key), `export` (needs the export script), or `no entry` (DCS-BIOS has no control and no other source reads it: fixed scales, labels, items the manual only names).
- **Position order**: the value of each position, as DCS-BIOS defines it (the positions list of the control, or the order in the DCS-BIOS description). Where DCS-BIOS gives no order, or the dashboard uses another order or label set, the order of `aircraft/ah64d.py` is used and the Note says so; `tested in DCS` marks an order or label set that the dashboard's tests confirmed (the automatic sweep skipped the controls on the dashboard blocklist). Where neither gives an order the cell starts with `guess:` and the order is a guess for phase 7 (check in DCS). Rules used for guesses: toggles and levers list the PANELS.md positions top to bottom = highest value first; rotary selectors and knobs list them in the order PANELS.md gives, lowest value first; spring-loaded rockers and levers run 0 = DN, 1 = CENTER (rest), 2 = UP; covers run 0 = CLOSE, 1 = OPEN. Buttons are 0 = released, 1 = pressed; lamps 0 = off, 1 = lit; gauges, counters and knobs 0 to 65535; displays are text.
- **Note**: the DCS-BIOS description where it adds to PANELS.md, `likely` when the match is by meaning rather than by name, the cover of a guarded control (`*_CVR`; 0 = CLOSE, 1 = OPEN), `dashboard blocklist` for a control whose identifier is on the dashboard blocklist ([SPEC.md](../SPEC.md#blocklist-idea); on the dashboard it sits behind a guard), what differs in the CP/G station, and for controls without an identifier the reason.

## Pilot cockpit

### Standby Magnetic Compass (p. 105)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Standby magnetic compass | PLT_STANDBY_COMPASS_HDG, PLT_STANDBY_COMPASS_PITCH, PLT_STANDBY_COMPASS_BANK | read only | bar or gauge | 0 to 65535 along the scale | likely; Standby Compass Heading is the card; Standby Compass Pitch and Standby Compass Bank are its tilt (no PANELS.md row for them); pilot only, the CP/G has no compass |

### Master Warning / Master Caution Lighted Pushbuttons (p. 106)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. MSTR WARN Button | {S}_INTL_MWARN_BTN | read + command | button | 0 = released, 1 = pressed | Master Warning Button; CP/G: the same pair on p. 124, acting on the CP/G station only |
| 1. MSTR WARN light | {S}_MASTER_WARNING_L | read only | lamp | 0 = off, 1 = lit | Master Warning Indicator |
| 2. MSTR CAUT Button | {S}_INTL_MCAUTION_BTN | read + command | button | 0 = released, 1 = pressed | Master Caution Button |
| 2. MSTR CAUT light | {S}_MASTER_CAUTION_L | read only | lamp | 0 = off, 1 = lit | Master Caution Indicator |

### Fire Detection / Extinguishing Panel (FIRE DET/EXTG) (p. 106)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. ENG 1 FIRE Button | {S}_FIRE_ENG1_BTN | read + command | button | 0 = released, 1 = pressed | ENG 1 Fire Pushbutton; CP/G: the same panel on p. 124; the three fire buttons are common to both stations; cover {S}_FIRE_ENG1_CVR (0 = CLOSE, 1 = OPEN), DCS ignores the button while its cover is closed; dashboard blocklist |
| 1. ENG 1 FIRE light | {S}_ENG_1_FIRE_L | read only | lamp | 0 = off, 1 = lit | Engine 1 Fire Indicator |
| 1. ENG 1 RDY light | {S}_ENG_1_READY_L | read only | lamp | 0 = off, 1 = lit | Engine 1 Ready Indicator |
| 2. APU FIRE Button | {S}_FIRE_APU_BTN | read + command | button | 0 = released, 1 = pressed | APU Fire Pushbutton; cover {S}_FIRE_APU_CVR (0 = CLOSE, 1 = OPEN), DCS ignores the button while its cover is closed; dashboard blocklist |
| 2. APU FIRE light | {S}_APU_FIRE_L | read only | lamp | 0 = off, 1 = lit | APU Fire Indicator |
| 2. APU RDY light | {S}_APU_READY_L | read only | lamp | 0 = off, 1 = lit | APU Ready Indicator |
| 3. ENG 2 FIRE Button | {S}_FIRE_ENG2_BTN | read + command | button | 0 = released, 1 = pressed | ENG 2 Fire Pushbutton; cover {S}_FIRE_ENG2_CVR (0 = CLOSE, 1 = OPEN), DCS ignores the button while its cover is closed; dashboard blocklist |
| 3. ENG 2 FIRE light | {S}_ENG_2_FIRE_L | read only | lamp | 0 = off, 1 = lit | Engine 2 Fire Indicator |
| 3. ENG 2 RDY light | {S}_ENG_2_READY_L | read only | lamp | 0 = off, 1 = lit | Engine 2 Ready Indicator |
| 4. PRI Button | {S}_FIRE_PRIME_EXT | read + command | button | 0 = released, 1 = pressed | Primary Fire Extinguisher Discharge Pushbutton; no cover in DCS-BIOS; dashboard blocklist |
| 4. PRI DISCH light | {S}_FIRE_EXT_DISCH_PRI_L | read only | lamp | 0 = off, 1 = lit | Primary Fire Extinguisher Discharge Indicator |
| 5. TEST Switch | {S}_FIRE_DETECT_TEST | read + command | selector (3) spring | 0 = 1, 1 = Off, 2 = 2 | Fire Detection Circuit Test Switch; positions 1 and 2 are TEST 1 and TEST 2; spring-loaded, rest is the middle |
| 6. RES Button | {S}_FIRE_RES_EXT | read + command | button | 0 = released, 1 = pressed | Reserve Fire Extinguisher Discharge Pushbutton; no cover in DCS-BIOS; dashboard blocklist |
| 6. RES DISCH light | {S}_FIRE_EXT_DISCH_RES_L | read only | lamp | 0 = off, 1 = lit | Reserve Fire Extinguisher Discharge Indicator |

### Armament Panel (p. 108)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. A/S Button | {S}_MASTER_ARM_BTN | read + command | button | 0 = released, 1 = pressed | A/S Pushbutton, ARM/SAFE; CP/G: the same panel on p. 124; both buttons are common to both stations |
| 1. ARM light | {S}_MASTER_ARM_ARM_L | read only | lamp | 0 = off, 1 = lit | Master Arm Armed Indicator |
| 1. SAFE light | {S}_MASTER_ARM_SAFE_L | read only | lamp | 0 = off, 1 = lit | Master Arm Safe Indicator |
| 2. GND ORIDE Button | {S}_GROUND_OVERRIDE_BTN | read + command | button | 0 = released, 1 = pressed | GND ORIDE Pushbutton |
| 2. ON light | {S}_GROUND_OVERRIDE_L | read only | lamp | 0 = off, 1 = lit | Ground Override Indicator |

### Video Panel (p. 109)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. IHADSS BRT Knob (outer) | PLT_VIDEO_IHADSS_BRT | read + command | knob | continuous, 0 to 65535 | Pilot IHADSS BRT Control Knob; pilot only, the CP/G has no Video Panel |
| 1. IHADSS CON Knob (inner) | PLT_VIDEO_IHADSS_CON | read + command | knob | continuous, 0 to 65535 | Pilot IHADSS CON Control Knob |
| 2. SYM BRT Knob | PLT_VIDEO_SYM_BRT | read + command | knob | continuous, 0 to 65535 | Pilot SYM BRT Control Knob |
| 3. ACM Switch | PLT_VIDEO_AUTO_CON | read + command | selector (2) | 0 = OFF, 1 = ACM | Pilot Automatic Contrast Mode Switch; DCS-BIOS gives no position names; order from aircraft/ah64d.py, tested in DCS |
| 4. FLIR LVL Knob (outer) | PLT_VIDEO_FLIR_LVL | read + command | knob | continuous, 0 to 65535 | Pilot FLIR LVL Control Knob |
| 4. FLIR GAIN Knob (inner) | PLT_VIDEO_FLIR_GAIN | read + command | knob | continuous, 0 to 65535 | Pilot FLIR GAIN Control Knob |

### Canopy Jettison Handle (p. 109)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Canopy Jettison Handle | — | — | no entry | — | No jettison control in DCS-BIOS (CP/G: also none). PLT_CANOPY (Pilot Canopy, 0 = CLOSE, 1 = OPEN) is the canopy position, not the handle; DCS-BIOS cannot move the canopy, a key does |

### Master Zeroize Switch (p. 109)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Master Zeroize Switch | {S}_INST_MZERO_SW | read + command | selector (2) | 0 = OFF, 1 = ON | Master Zeroize Switch; CP/G: the same on p. 124; cover {S}_INST_MZERO_CVR (0 = CLOSE, 1 = OPEN); DCS-BIOS gives no position names, order from aircraft/ah64d.py, not covered by the automatic sweep; dashboard blocklist |

### Standby Attitude Indicator (p. 110)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Bank Angle Scale | — | — | no entry | — | Fixed scale; pilot only, the CP/G has no standby attitude indicator |
| 2. Bank Angle Indicator | PLT_SAI_POINTER | read only | bar or gauge | 0 to 65535 along the scale | likely; Pilot SAI ArrowPointer; the arrow pointer on the bank scale |
| 3. Attitude Sphere | PLT_SAI_PITCH, PLT_SAI_BANK | read only | bar or gauge | 0 to 65535 along the scale | likely; Pilot SAI Pitch and Pilot SAI Bank as separate outputs |
| 4. Aircraft Symbol (Waterline) | — | — | no entry | — | No output of its own; its height is moved by turning the PULL TO CAGE knob (PLT_SAI_PITCH_TRIM) |
| 5. Pitch Scale | — | — | no entry | — | Printed on the sphere; it moves with PLT_SAI_PITCH |
| 6. Slip Indicator (Ball) | PLT_SAI_BALL | read only | bar or gauge | 0 to 65535 along the scale | Pilot SAI Slip Ball |
| 7. Rate-of-Turn Indicator | PLT_SAI_TURN | read only | bar or gauge | 0 to 65535 along the scale | Pilot SAI Turn |
| 8. PULL TO CAGE Knob | PLT_SAI_CAGE, PLT_SAI_PITCH_TRIM | read + command | PLT_SAI_CAGE: button; PLT_SAI_PITCH_TRIM: step rocker (3200) | PLT_SAI_CAGE: 0 = released, 1 = pressed; PLT_SAI_PITCH_TRIM: step up or down only, no absolute value | Pull is PLT_SAI_CAGE (Pilot SAI Cage Knob, pull to cage); turn is PLT_SAI_PITCH_TRIM (adjust aircraft reference symbol, the knob rotation comes back as PLT_SAI_PITCH_TRIM_KNOB_POS); cage and pitch trim did not work in DCS |
| OFF warning flag | PLT_SAI_FLAG | read only | bar or gauge | 0 to 65535 along the scale | Pilot SAI Off Flag |

### Standby Airspeed Indicator (p. 111)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Airspeed Indicator | PLT_IAS_NEEDLE | read only | bar or gauge | 0 to 65535 along the scale | Pilot Standby Airspeed Indicator Needle; pilot only, the CP/G has no standby airspeed indicator |
| 2. Indicated Airspeed Scale | — | — | no entry | — | Fixed outer scale; the pointer is PLT_IAS_NEEDLE |

### Standby Altimeter (p. 111)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. 1000-foot Altitude Scale | — | — | no entry | — | Fixed scale; pilot only, the CP/G has no standby altimeter |
| 2. 1000-ft Scale Indicator | PLT_ALT_NEEDLE | read only | bar or gauge | 0 to 65535 along the scale | Pilot Altimeter Needle |
| 3. Altitude Indicator | PLT_ALT_1000, PLT_ALT_10000 | read only | bar or gauge | 0 to 65535 along the scale | likely; Pilot Altimeter 1000 Drum and 10000 Drum |
| 4. "Kollsman" Window | PLT_ALT_PRESS_1, PLT_ALT_PRESS_10, PLT_ALT_PRESS_1100 | read only | bar or gauge | 0 to 65535 along the scale | likely; Pilot Altimeter Pressure 0001, 0010 and 1100 Drum |
| 5. Barometric Setting Knob | PLT_ALT_SET_KNB | read + command | knob | continuous, 0 to 65535 | Pilot Altimeter Barometric Setting Knob |

### Check Overspeed Test / Generator Reset Panel (p. 111)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. CKT A Switch | PLT_CHK_OSPD_ENG_A | read + command | selector (3) spring | 0 = ENG 2, 1 = Off, 2 = ENG 1 | Pilot CKT A Check Overspeed Test Switch; spring-loaded, rest is the middle; reverse order of PANELS; pilot only, the CP/G has no such panel |
| 2. CKT B Switch | PLT_CHK_OSPD_ENG_B | read + command | selector (3) spring | 0 = ENG 2, 1 = Off, 2 = ENG 1 | Pilot CKT B Check Overspeed Test Switch; spring-loaded, rest is the middle; reverse order of PANELS |
| 3. GEN RST Switch | PLT_GEN_RESET | read + command | selector (3) spring | 0 = GEN 1, 1 = Off, 2 = GEN 2 | Pilot Generator Reset Switch; spring-loaded, rest is the middle; PANELS does not state the spring action |

### Windshield Wiper Control Panel (p. 112)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. DEFOG Button | {S}_DEFOG_BTN | read + command | button | 0 = released, 1 = pressed | Defog Button; CP/G: the same panel on its right console (p. 127) |
| 2. WINDSHIELD WIPER Knob | {S}_WIPER_SW | read + command | selector (4) | 0 = PARK, 1 = OFF, 2 = LO, 3 = HI | Wiper Control Switch |

### Parking Brake Handle (p. 112)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| PARK BRAKE Handle | PLT_PARK_BRAKE | read + command | selector (2) | 0 = IN, 1 = PULLED | Pilot Parking Brake Handle; DCS-BIOS labels the positions Stow and Pull, the dashboard IN and PULLED; tested in DCS; pilot only, the CP/G has no handle |

### Keyboard Unit (KU) (p. 113)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Display Prompt | — | — | no entry | — | Not an output of its own; {S}_KU_DISPLAY (22 characters) is the scratchpad line; CP/G: its own unit on p. 125, same ids with CPG_ |
| 2. Scratchpad Display | {S}_KU_DISPLAY | read only | display | text | Keyboard Unit Display; 22 characters |
| 3. Arithmetic Buttons | {S}_KU_MULTI, {S}_KU_DIV, {S}_KU_PLUS, {S}_KU_MINUS | read + command | button | 0 = released, 1 = pressed | multiply, divide, add, subtract (the Keyboard Unit * / + - keys) |
| 4. CLR Button | {S}_KU_CLR | read + command | button | 0 = released, 1 = pressed | Keyboard Unit CLR Key |
| 5. Scroll Arrows | {S}_KU_LEFT, {S}_KU_RIGHT | read + command | button | 0 = released, 1 = pressed | Keyboard Unit Left and Right Key |
| 6. ENTER Button | {S}_KU_ENT | read + command | button | 0 = released, 1 = pressed | Keyboard Unit ENTER Key |
| 7. Display Brightness Knob | {S}_KU_BRT | read + command | knob | continuous, 0 to 65535 | Scratchpad Keyboard Brightness Knob |
| 8. BKS Button | {S}_KU_BKS | read + command | button | 0 = released, 1 = pressed | Keyboard Unit BKS Key |
| 9. SPC Button | {S}_KU_SPC | read + command | button | 0 = released, 1 = pressed | Keyboard Unit SPC Key |
| Letter, number and N / E / S / W keys | {S}_KU_A, {S}_KU_B, {S}_KU_C, {S}_KU_D, {S}_KU_E, {S}_KU_F, {S}_KU_G, {S}_KU_H, {S}_KU_I, {S}_KU_J, {S}_KU_K, {S}_KU_L, {S}_KU_M, {S}_KU_N, {S}_KU_O, {S}_KU_P, {S}_KU_Q, {S}_KU_R, {S}_KU_S, {S}_KU_T, {S}_KU_U, {S}_KU_V, {S}_KU_W, {S}_KU_X, {S}_KU_Y, {S}_KU_Z, {S}_KU_0, {S}_KU_1, {S}_KU_2, {S}_KU_3, {S}_KU_4, {S}_KU_5, {S}_KU_6, {S}_KU_7, {S}_KU_8, {S}_KU_9, {S}_KU_DOT, {S}_KU_SIGN, {S}_KU_SLASH | read + command | button | 0 = released, 1 = pressed | Keyboard Unit A to Z and 0 to 9 keys (N, E, S and W are letter keys), plus the . (dot), +/- (sign) and / (slash) keys |

### Tail Wheel / NVS Mode Panel (p. 115)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. TAIL WHEEL Button | {S}_T_WHEEL_UNLOCK_BTN | read + command | button | 0 = released, 1 = pressed | TAIL WHEEL Pushbutton, LOCK/UNLOCK; CP/G: the same panel on p. 125 |
| UNLOCK light | {S}_T_WHEEL_UNLOCK_L | read only | lamp | 0 = off, 1 = lit | Tail Wheel Unlock Indicator |
| 2. NVS MODE Switch | {S}_NVS_MODE | read + command | selector (3) | 0 = OFF, 1 = NORM, 2 = FIXED | NVS MODE Switch; reverse order of PANELS; FIXED needs the NVS on; the default NVS sensor is the PNVS in the pilot seat and the TADS in the CP/G seat |

### Emergency Panel (p. 116)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. GUARD Button | {S}_EMERG_GUARD_BTN | read + command | button | 0 = released, 1 = pressed | Guard Button; CP/G: the same panel on p. 125 |
| 1. GUARD ON light | {S}_EMERG_GUARD_L | read only | lamp | 0 = off, 1 = lit | Emergency Guard Indicator |
| 2. XPNDR Button | {S}_EMERG_XPNDR_BTN | read + command | button | 0 = released, 1 = pressed | XPNDR Button |
| 2. XPNDR ON light | {S}_EMERG_XPNDR_L | read only | lamp | 0 = off, 1 = lit | Emergency Transponder Indicator |
| 3. ZEROIZE Switch | {S}_EMERG_ZERO_SW | read + command | selector (2) | 0 = OFF, 1 = ON | Zeroize Switch; DCS-BIOS gives no position names, order from aircraft/ah64d.py, not covered by the automatic sweep; no cover in DCS-BIOS; dashboard blocklist |
| 4. EMERG HYD Button | {S}_EMERG_HYD_BTN | read + command | button | 0 = released, 1 = pressed | EMERG HYD Pushbutton |
| 4. EMERG HYD ON light | {S}_EMERG_HYD_L | read only | lamp | 0 = off, 1 = lit | Emergency Hydraulics Indicator |

### Power Quadrant Panel (p. 117)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. RTR BRK Switch | PLT_ROTOR_BRK | read + command | selector (3) | 0 = LOCK, 1 = BRK, 2 = OFF | Pilot Rotor Brake Switch; reverse order of PANELS; BRK needs conditions (inhibited while an ENG POWER lever is past IDLE); CP/G: only the ENG POWER levers (row 6), none of the other controls of this panel |
| 2. MSTR IGN Knob | PLT_MASTER_IGN_SW | read + command | selector (3) | 0 = OFF, 1 = BATT, 2 = EXT PWR | Pilot Master Ignition Switch; EXT PWR needs ground power |
| 3. FRICT Lever | PLT_PW_LVR_FRIC | read + command | knob | continuous, 0 to 65535 | Pilot Power Lever Friction Adjustment Lever |
| 4. APU Button | PLT_APU_BTN | read + command | button | 0 = released, 1 = pressed | Pilot APU Pushbutton; cover PLT_APU_BTN_CVR (0 = CLOSE, 1 = OPEN), PANELS does not list the cover; the button works only with the cover open |
| 4. APU ON light | PLT_APU_L | read only | lamp | 0 = off, 1 = lit | Pilot APU On Indicator |
| 5. ENG START Switches | PLT_ENG1_START, PLT_ENG2_START | read + command | selector (3) spring | 0 = IGN ORIDE, 1 = OFF, 2 = START | One switch per engine; spring-loaded, rest is the middle (START and IGN ORIDE momentary); reverse order of PANELS |
| 6. ENG POWER Levers | {S}_ENG_L_PW_LVR, {S}_ENG_R_PW_LVR, PLT_ENG_L_PW_LVR_IDLE, PLT_ENG_L_PW_LVR_LIFT, PLT_ENG_R_PW_LVR_IDLE, PLT_ENG_R_PW_LVR_LIFT | read + command | {S}_ENG_L_PW_LVR, {S}_ENG_R_PW_LVR: knob; PLT_ENG_L_PW_LVR_IDLE, PLT_ENG_R_PW_LVR_IDLE: selector (2) NO READBACK; PLT_ENG_L_PW_LVR_LIFT, PLT_ENG_R_PW_LVR_LIFT: button NO READBACK | {S}_ENG_L_PW_LVR, {S}_ENG_R_PW_LVR: continuous, 0 to 65535; readback 0 = OFF, 16383 = IDLE, 58981 = FLY, 65535 = LOCK OUT; PLT_ENG_L_PW_LVR_IDLE, PLT_ENG_R_PW_LVR_IDLE: 0 = off, 1 = on; PLT_ENG_L_PW_LVR_LIFT, PLT_ENG_R_PW_LVR_LIFT: 0 = released, 1 = pressed | Pilot Power Lever Smoothly (Left and Right) for the lever position; Power Lever Idle/Off and Finger Lift (Left and Right) are command inputs of the pilot station only; DCS-BIOS does not move the levers past the OFF detent, so the dashboard moves them by key and reads the position back; the readback values are tested in DCS; lowest value first, the reverse of PANELS; no output: PLT_ENG_L_PW_LVR_IDLE, PLT_ENG_L_PW_LVR_LIFT, PLT_ENG_R_PW_LVR_IDLE, PLT_ENG_R_PW_LVR_LIFT |

### Stores Jettison Panel (p. 119)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. L OUTBD Button | {S}_JETT_STORE_LO | read + command | button | 0 = released, 1 = pressed | L OUTBD Station Select Pushbutton, ARM/SAFE; plain button on the dashboard, it only arms the station; CP/G: the same panel on p. 125; only the seat that armed a station can disarm it; dashboard blocklist |
| 1. L OUTBD ARM light | {S}_JETT_L_OUTBOARD_L | read only | lamp | 0 = off, 1 = lit | Jettison Left Outboard Indicator |
| 2. L INBD Button | {S}_JETT_STORE_LI | read + command | button | 0 = released, 1 = pressed | L INBD Station Select Pushbutton, ARM/SAFE; plain button on the dashboard, it only arms the station; dashboard blocklist |
| 2. L INBD ARM light | {S}_JETT_L_INBOARD_L | read only | lamp | 0 = off, 1 = lit | Jettison Left Inboard Indicator |
| 3. R INBD Button | {S}_JETT_STORE_RI | read + command | button | 0 = released, 1 = pressed | R INBD Station Select Pushbutton, ARM/SAFE; plain button on the dashboard, it only arms the station; dashboard blocklist |
| 3. R INBD ARM light | {S}_JETT_R_INBOARD_L | read only | lamp | 0 = off, 1 = lit | Jettison Right Inboard Indicator |
| 4. R OUTBD Button | {S}_JETT_STORE_RO | read + command | button | 0 = released, 1 = pressed | R OUTBD Station Select Pushbutton, ARM/SAFE; plain button on the dashboard, it only arms the station; dashboard blocklist |
| 4. R OUTBD ARM light | {S}_JETT_R_OUTBOARD_L | read only | lamp | 0 = off, 1 = lit | Jettison Right Outboard Indicator |
| 5. L TIP Button | {S}_JETT_STORE_LW, {S}_JETT_L_TIP_L | read + command | {S}_JETT_STORE_LW: button; {S}_JETT_L_TIP_L: lamp | {S}_JETT_STORE_LW: 0 = released, 1 = pressed; {S}_JETT_L_TIP_L: 0 = off, 1 = lit | PANELS says no function; DCS-BIOS has the button (L TIP Station Select Pushbutton, ARM/SAFE) and its lamp (Jettison Left Tip Indicator, no PANELS row); plain button on the dashboard; dashboard blocklist; read only: {S}_JETT_L_TIP_L |
| 6. JETT Button | {S}_JETT_BTN | read + command | button | 0 = released, 1 = pressed | JETT Pushbutton; guarded on the dashboard; no cover in DCS-BIOS; dashboard blocklist |
| 7. R TIP Button | {S}_JETT_STORE_RW, {S}_JETT_R_TIP_L | read + command | {S}_JETT_STORE_RW: button; {S}_JETT_R_TIP_L: lamp | {S}_JETT_STORE_RW: 0 = released, 1 = pressed; {S}_JETT_R_TIP_L: 0 = off, 1 = lit | PANELS says no function; DCS-BIOS has the button (R TIP Station Select Pushbutton, ARM/SAFE) and its lamp (Jettison Right Tip Indicator, no PANELS row); plain button on the dashboard; dashboard blocklist; read only: {S}_JETT_R_TIP_L |

### Exterior Lighting / Interior Lighting Panel (p. 119)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. NAV Switch | PLT_EXTL_NAV_L_SW | read + command | selector (3) | 0 = DIM, 1 = OFF, 2 = BRT | Pilot Navigation Lights Switch; reverse order of PANELS; pilot only (the CP/G Interior Lighting Panel has no NAV, FORM, STBY INST and ANTI COLL controls) |
| 2. SIGNAL Knob | {S}_INTL_SIGNAL_L_KNB | read + command | knob | continuous, 0 to 65535 | Signal Lights Control Knob; CP/G: the same knob on its Interior Lighting Panel (p. 126) |
| 3. PRIMARY Knob | {S}_INTL_PRIMARY_L_KNB | read + command | knob | continuous, 0 to 65535 | Primary Lights Control Knob |
| 4. FORM Knob | PLT_EXTL_FROMATION_L_KNB | read + command | knob | continuous, 0 to 65535 | Pilot Formation Lights Control Knob; The identifier is spelled FROMATION |
| 5. FLOOD Knob | {S}_INTL_FLOOD_L_KNB | read + command | knob | continuous, 0 to 65535 | Flood Lights Control Knob |
| 6. STBY INST Knob | PLT_INTL_STBYINST_L_KNB | read + command | knob | continuous, 0 to 65535 | Pilot Standby Instrument Lights Control Knob |
| 7. ANTI COLL Switch | PLT_EXTL_ACOL_L_SW | read + command | selector (3) | 0 = RED, 1 = OFF, 2 = WHT | Pilot Anti-Collision Lights Switch; reverse order of PANELS |
| 8. PRESS TO TEST Button | {S}_INTL_TEST_BTN | read + command | button | 0 = released, 1 = pressed | Light Test Button |

### Free Air Temperature Gauge (p. 120)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Temperature Indicator | PLT_FREE_AIR_TEMP | read only | bar or gauge | 0 to 65535 along the scale | Pilot Free Air Temperature Gage; pilot only, the CP/G has none |
| 2. Temperature Scale | — | — | no entry | — | Fixed scale |

### Communications Panel (p. 121)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. FM1 Knob | {S}_COM_FM1_VOL, {S}_COM_FM1_PW | read + command | {S}_COM_FM1_VOL: knob; {S}_COM_FM1_PW: selector (2) | {S}_COM_FM1_VOL: continuous, 0 to 65535; {S}_COM_FM1_PW: 0 = In, 1 = Out | CP/G: the same panel on its right console (p. 127); PW is the pull-out position of the knob (Out mutes the source) |
| 2. FM2 Knob | {S}_COM_FM2_VOL, {S}_COM_FM2_PW | read + command | {S}_COM_FM2_VOL: knob; {S}_COM_FM2_PW: selector (2) | {S}_COM_FM2_VOL: continuous, 0 to 65535; {S}_COM_FM2_PW: 0 = In, 1 = Out | PW is the pull-out position of the knob (Out mutes the source) |
| 3. HF Knob | {S}_COM_HF_VOL, {S}_COM_HF_PW | read + command | {S}_COM_HF_VOL: knob; {S}_COM_HF_PW: selector (2) | {S}_COM_HF_VOL: continuous, 0 to 65535; {S}_COM_HF_PW: 0 = In, 1 = Out | PW is the pull-out position of the knob (Out mutes the source) |
| 4. VHF Knob | {S}_COM_VHF_VOL, {S}_COM_VHF_PW | read + command | {S}_COM_VHF_VOL: knob; {S}_COM_VHF_PW: selector (2) | {S}_COM_VHF_VOL: continuous, 0 to 65535; {S}_COM_VHF_PW: 0 = In, 1 = Out | PW is the pull-out position of the knob (Out mutes the source) |
| 5. UHF Knob | {S}_COM_UHF_VOL, {S}_COM_UHF_PW | read + command | {S}_COM_UHF_VOL: knob; {S}_COM_UHF_PW: selector (2) | {S}_COM_UHF_VOL: continuous, 0 to 65535; {S}_COM_UHF_PW: 0 = In, 1 = Out | PW is the pull-out position of the knob (Out mutes the source) |
| 6. SQL Switches | {S}_COM_FM1_SQL, {S}_COM_FM2_SQL, {S}_COM_HF_SQL, {S}_COM_VHF_SQL, {S}_COM_UHF_SQL | read + command | selector (3) spring | 0 = DISABLE, 1 = Off, 2 = ENABLE | One switch per radio (FM1, FM2, HF, VHF, UHF); spring-loaded, rest is the middle; ENABLE and DISABLE are the two directions (which one is forward is not stated) |
| 7. SENS Knob | {S}_COM_SENS_KNB | read + command | knob | continuous, 0 to 65535 | SENS Control Knob |
| 8. MASTER Knob | {S}_COM_MASTER_VOL | read + command | knob | continuous, 0 to 65535 | MASTER Volume Control Knob |
| 9. ICS Switch | {S}_COM_ICS_MODE | read + command | selector (3) | 0 = HOT MIC, 1 = VOX, 2 = PTT | ICS Mode Switch; reverse order of PANELS; takes about 3 s to reach the position |
| 10. IDENT Button | {S}_COM_IDENT_BTN | read + command | button | 0 = released, 1 = pressed | IDENT Button |
| 11. IFF Knob | {S}_COM_IFF_VOL | read + command | knob | continuous, 0 to 65535 | IFF Volume Control Knob |
| 12. RLWR Knob | {S}_COM_RLWR_VOL | read + command | knob | continuous, 0 to 65535 | RLWR Volume Control Knob |
| 13. ATA Knob | {S}_COM_ATA_VOL | read + command | knob | continuous, 0 to 65535 | ATA Volume Control Knob; PANELS says no function |
| 14. VCR Knob | {S}_COM_VCR_VOL, {S}_COM_VCR_PW | read + command | {S}_COM_VCR_VOL: knob; {S}_COM_VCR_PW: selector (2) | {S}_COM_VCR_VOL: continuous, 0 to 65535; {S}_COM_VCR_PW: 0 = In, 1 = Out | PW is the pull-out position of the knob (Out mutes the source) |
| 15. ADF Knob | {S}_COM_ADF_VOL, {S}_COM_ADF_PW | read + command | {S}_COM_ADF_VOL: knob; {S}_COM_ADF_PW: selector (2) | {S}_COM_ADF_VOL: continuous, 0 to 65535; {S}_COM_ADF_PW: 0 = In, 1 = Out | PW is the pull-out position of the knob (Out mutes the source) |

### CMWS Control Panel (p. 630)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Control Indicator Display | PLT_CMWS_PAGE, PLT_CMWS_BIT_LINE_1, PLT_CMWS_BIT_LINE_2 | read only | display | text | Page text NONE, MAIN or TEST, and the two test lines (BIT/SYS, I/P/PASS); the counts are on rows 9 and 10, the lamps on rows 11 to 13; the CMWS panel is pilot only, all its identifiers are PLT_ |
| 2. Power/Test Knob | PLT_CMWS_PW | read + command | selector (3) spring | 0 = Off, 1 = On, 2 = Test | Pilot CMWS PWR Switch; spring-loaded, rest is On (Test is momentary) |
| 3. AUDIO Knob | PLT_CMWS_VOL | read + command | knob | continuous, 0 to 65535 | Pilot CMWS Audio Volume Knob; PANELS says no function |
| 4. LAMP Knob | PLT_CMWS_LAMP | read + command | knob | continuous, 0 to 65535 | Pilot CMWS Lamp Knob |
| 5. ARM/SAFE Switch | PLT_CMWS_ARM | read + command | selector (2) | 0 = SAFE, 1 = ARM | Pilot CMWS Flare Squibs Switch |
| 6. CMWS/NAV Switch | PLT_CMWS_MODE | read + command | selector (2) | 0 = NAV, 1 = CMWS | Pilot CMWS Mode Switch; reverse order of PANELS |
| 7. JETTISON Switch | PLT_CMWS_JETT | read + command | selector (2) | 0 = OFF, 1 = ON | Pilot CMWS Flare Jettison Switch; cover PLT_CMWS_JETT_CVR (0 = CLOSE, 1 = OPEN); DCS-BIOS gives no position names, order from aircraft/ah64d.py, not covered by the automatic sweep; DCS ignores the switch while its cover is closed; dashboard blocklist |
| 8. BYPASS/AUTO Switch | PLT_CMWS_BYPASS | read + command | selector (2) | 0 = AUTO, 1 = BYPASS | Pilot CMWS Operation Switch; reverse order of PANELS |
| 9. Flare Inventory | PLT_CMWS_FLARE_LETTER, PLT_CMWS_FLARE_COUNT | read only | display | text | Flare Letter (F) and Flare Count |
| 10. Chaff Inventory | PLT_CMWS_CHAFF_LETTER, PLT_CMWS_CHAFF_COUNT | read only | display | text | Chaff Letter (C) and Chaff Count |
| 11. Quadrant Arrows | PLT_CMWS_FWD_LEFT_BRT_L, PLT_CMWS_FWD_LEFT_DIM_L, PLT_CMWS_FWD_RIGHT_BRT_L, PLT_CMWS_FWD_RIGHT_DIM_L, PLT_CMWS_AFT_LEFT_BRT_L, PLT_CMWS_AFT_LEFT_DIM_L, PLT_CMWS_AFT_RIGHT_BRT_L, PLT_CMWS_AFT_RIGHT_DIM_L | read only | none | 0 = off, 1 = lit | defineIntegerFromGetter output, 0 or 1; sector lights forward left, forward right, aft left and aft right, each bright (threat shown) and dim (display on, no threat) |
| 12. Dispense Indicator | PLT_CMWS_D_BRT_L, PLT_CMWS_D_DIM_L | read only | none | 0 = off, 1 = lit | likely; defineIntegerFromGetter output, 0 or 1; D light, bright and dim |
| 13. Ready Indicator | PLT_CMWS_R_BRT_L, PLT_CMWS_R_DIM_L | read only | none | 0 = off, 1 = lit | likely; defineIntegerFromGetter output, 0 or 1; R light, bright and dim |

### Items named only in the pilot overview figure (pp. 104 and 394)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Boresight Reticle Unit (BRU) | — | — | no entry | — | No DCS-BIOS control |
| Data Transfer Unit (DTU) receptacle | — | — | no entry | — | No DCS-BIOS control |
| Anti-Torque Pedals | — | — | export | — | The export script sends the pedal position (cockpit argument 476, plt_pedals); no DCS-BIOS control |

## Copilot/Gunner cockpit

### Interior Lighting Panel (p. 126)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. SIGNAL Knob | CPG_INTL_SIGNAL_L_KNB | read + command | knob | continuous, 0 to 65535 | Gunner Signal Lights Control Knob; CP/G half of {S}_INTL_SIGNAL_L_KNB (Exterior Lighting / Interior Lighting Panel in the Pilot cockpit area) |
| 2. PRIMARY Knob | CPG_INTL_PRIMARY_L_KNB | read + command | knob | continuous, 0 to 65535 | Gunner Primary Lights Control Knob; CP/G half of {S}_INTL_PRIMARY_L_KNB |
| 3. FLOOD Knob | CPG_INTL_FLOOD_L_KNB | read + command | knob | continuous, 0 to 65535 | Gunner Flood Lights Control Knob; CP/G half of {S}_INTL_FLOOD_L_KNB |
| 4. PRESS TO TEST Button | CPG_INTL_TEST_BTN | read + command | button | 0 = released, 1 = pressed | Gunner Light Test Button; CP/G half of {S}_INTL_TEST_BTN |

### Processor Select Panel (p. 127)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. SP1 light | CPG_PROCESSOR_SP_1_L | read only | lamp | 0 = off, 1 = lit | Gunner Processor Select SP 1 Indicator; CP/G only; the whole panel is N/I in the manual |
| 1. SP2 light | CPG_PROCESSOR_SP_2_L | read only | lamp | 0 = off, 1 = lit | Gunner Processor Select SP 2 Indicator |
| 2. PROCESSOR SELECT Switch | CPG_PROC_SEL_SW | read + command | selector (3) | 0 = SP 1, 1 = AUTO, 2 = SP 2 | Gunner Processor Select Switch; the processor select did not work in DCS |

### Console fittings named only in the overview figures (pp. 125 and 127)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Utility Light | — | — | no entry | — | No DCS-BIOS control |
| Canopy Jettison Handle Pin | — | — | no entry | — | No DCS-BIOS control; label only |
| First Aid Kit | — | — | no entry | — | No DCS-BIOS control; label only |
| HDU Storage Holster | — | — | no entry | — | No DCS-BIOS control; label only |

### TEDAC Display Unit (TDU) (p. 129)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| TDU screen | — | — | no entry | — | No DCS-BIOS output; the export script sends the text of the four MPDs only (list_indication 7, 9, 11 and 13), not the TDU picture |
| 1. TAD Button | CPG_TEDAC_TAD_SEL | read + command | button | 0 = released, 1 = pressed | Gunner TEDAC Display TAD Video Select Button |
| 2. FCR Button | CPG_TEDAC_FCR_SEL | read + command | button | 0 = released, 1 = pressed | Gunner TEDAC Display FCR Video Select Button |
| 3. PNV Button | CPG_TEDAC_PNV_SEL | read + command | button | 0 = released, 1 = pressed | Gunner TEDAC Display PNV Video Select Button |
| 4. G/S Button | CPG_TEDAC_GS_SEL | read + command | button | 0 = released, 1 = pressed | Gunner TEDAC Display G/S Video Select Button |
| 5. TDU Display Knob | CPG_TEDAC_DISP_MODE | read + command | selector (3) | 0 = OFF, 1 = NT, 2 = DAY | likely; Gunner TEDAC Display Mode Knob is the DAY / NT / OFF knob; reverse order of PANELS; DCS-BIOS and aircraft/ah64d.py agree on the order |
| 6. FLIR LEV Knob | CPG_TEDAC_FLIR_LEV | read + command | knob | continuous, 0 to 65535 | Gunner TEDAC Display FLIR LEV Control Knob |
| 7. FLIR GAIN Knob | CPG_TEDAC_FLIR_GAIN | read + command | knob | continuous, 0 to 65535 | Gunner TEDAC Display FLIR GAIN Control Knob |
| 8. SYM Rocker Switch | CPG_TEDAC_SYM | read + command | selector (3) spring | 0 = Decrease, 1 = Off, 2 = Increase | Gunner TEDAC Display SYM Rocker Switch; spring-loaded, rest is the middle; PANELS does not say which direction raises, DCS-BIOS names 2 = Increase |
| 9. BRT Rocker Switch | CPG_TEDAC_BRT | read + command | selector (3) spring | 0 = Decrease, 1 = Off, 2 = Increase | Gunner TEDAC Display BRT Rocker Switch; spring-loaded, rest is the middle; PANELS does not say which direction raises, DCS-BIOS names 2 = Increase |
| 10. CON Rocker Switch | CPG_TEDAC_CON | read + command | selector (3) spring | 0 = Decrease, 1 = Off, 2 = Increase | Gunner TEDAC Display CON Rocker Switch; spring-loaded, rest is the middle; PANELS does not say which direction raises, DCS-BIOS names 2 = Increase |
| 11. Asterisk Button | CPG_TEDAC_MULTI | read + command | button | 0 = released, 1 = pressed | Gunner TEDAC Display Asterisk (*) Button |
| 12. R/F Rocker Switch | CPG_TEDAC_RF | read + command | selector (3) spring | 0 = Decrease, 1 = Off, 2 = Increase | Gunner TEDAC Display R/F Rocker Switch; spring-loaded, rest is the middle; PANELS: up is the longer focus range, down the shorter, DCS-BIOS names the ends Decrease and Increase |
| 13. EL Rocker Switch | CPG_TEDAC_EL | read + command | selector (3) spring | 0 = Decrease, 1 = Off, 2 = Increase | Gunner TEDAC Display EL Rocker Switch; spring-loaded, rest is the middle; PANELS: N/I, DCS-BIOS has the control |
| 14. AZ Rocker Switch | CPG_TEDAC_AZ | read + command | selector (3) spring | 0 = Left, 1 = Off, 2 = Right | Gunner TEDAC Display AZ Rocker Switch; spring-loaded, rest is the middle; PANELS: N/I, DCS-BIOS has the control |
| 15. AZ/EL Button | CPG_TEDAC_BORESIGHT | read + command | button | 0 = released, 1 = pressed | Gunner TEDAC Display AZ/EL Boresight Enable Button; PANELS: N/I, DCS-BIOS has the control |
| 16. ACM Button | CPG_TEDAC_ACM | read + command | button | 0 = released, 1 = pressed | Gunner TEDAC Display ACM Button; PANELS: N/I, DCS-BIOS has the control |
| 17. FREEZE Button | CPG_TEDAC_FREEZE | read + command | button | 0 = released, 1 = pressed | Gunner TEDAC Display FREEZE Button |
| 18. FILTER Button | CPG_TEDAC_FILTER | read + command | button | 0 = released, 1 = pressed | Gunner TEDAC Display FILTER Button; PANELS: N/I, DCS-BIOS has the control |

### TEDAC Left Handgrip (LHG) (p. 131)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Image Auto Track/Offset Switch | CPG_LHG_TEDAC_L_IAT | read + command | selector (3) spring | 0 = OFS, 1 = Off, 2 = IAT | Gunner Image AutoTrack/Offset Switch; spring-loaded, rest is the middle; IAT forward (2), OFS aft (0) after PANELS |
| 2. TADS Field-Of-View Switch | CPG_LHG_TADS_FOV_UP_DN, CPG_LHG_TADS_FOV_L_R | read + command | selector (3) spring | CPG_LHG_TADS_FOV_UP_DN: 0 = Medium, 1 = Off, 2 = Zoom; CPG_LHG_TADS_FOV_L_R: 0 = Narrow, 1 = Off, 2 = Wide | Two axes, spring-loaded, rest is the middle; after PANELS the UP_DN axis has Z forward (2) and M aft (0), the L_R axis N left (0) and W right (2) |
| 3. Video Record Button | — | — | no entry | — | No DCS-BIOS control; N/I in DCS |
| 4. TADS Sensor Select Switch | CPG_LHG_TADS_SEL | read + command | selector (3) | 0 = DVO, 1 = TV, 2 = FLIR | Gunner TADS Sensor Select Switch; FLIR forward (2), TV centre (1), DVO aft (0) after PANELS; DVO has no function; not spring-loaded |
| 5. Weapon Action Switch (WAS) | CPG_LHG_WPN_UP_DN, CPG_LHG_WPN_L_R | read + command | selector (3) spring | CPG_LHG_WPN_UP_DN: 0 = ATA, 1 = Off, 2 = GUN; CPG_LHG_WPN_L_R: 0 = RKT, 1 = Off, 2 = MSL | Two axes, spring-loaded, rest is the middle; after PANELS the UP_DN axis has GUN forward (2) and ATA aft (0), the L_R axis RKT left (0) and MSL right (2); the cyclic switch does the same |
| 6. Store/Update Switch | CPG_LHG_STORE_UPDATE | read + command | selector (3) spring | 0 = UPDT, 1 = Off, 2 = STORE | Gunner STORE/Update Switch; spring-loaded, rest is the middle; STORE forward (2), UPDT aft (0) after PANELS |
| 7. FCR Mode Switch | CPG_LHG_FCR_UP_DN, CPG_LHG_FCR_L_R | read + command | selector (3) spring | CPG_LHG_FCR_UP_DN: 0 = ATM, 1 = Off, 2 = GTM; CPG_LHG_FCR_L_R: 0 = TPM, 1 = Off, 2 = RMAP | Two axes, spring-loaded, rest is the middle; after PANELS the UP_DN axis has GTM forward (2) and ATM aft (0), the L_R axis TPM left (0) and RMAP right (2) |
| 8. Cursor Controller/Enter (CURSOR) | CPG_LHG_CURSOR_UP_DN, CPG_LHG_CURSOR_L_R, CPG_LHG_CURSOR_ENT | read + command | CPG_LHG_CURSOR_UP_DN, CPG_LHG_CURSOR_L_R: selector (3) spring; CPG_LHG_CURSOR_ENT: button | CPG_LHG_CURSOR_UP_DN: 0 = Down, 1 = Off, 2 = Up; CPG_LHG_CURSOR_L_R: 0 = Left, 1 = Off, 2 = Right; CPG_LHG_CURSOR_ENT: 0 = released, 1 = pressed | Gunner Cursor Controller, two axes with three positions each, spring-loaded, rest is the middle (not analog like the collective cursor controller); CPG_LHG_CURSOR_ENT is Gunner Cursor Controller, Enter |
| 9. Cursor Display Select (L/R) Button | CPG_LHG_LR_BTN | read + command | button | 0 = released, 1 = pressed | Gunner Cursor Display Select (L/R) Button |
| 10. Weapon Trigger | — | — | keybind | — | No weapon trigger on the TEDAC left handgrip in DCS-BIOS; the cyclic trigger {S}_CYCLIC_TRIGGER is another control (Cyclic Grip) |
| 11. FCR Scan Switch | CPG_LHG_FCR_SCAN | read + command | selector (3) spring | 0 = C, 1 = Off, 2 = S | Gunner FCR Scan Switch; spring-loaded, rest is the middle; S-SCAN forward (2), C-SCAN aft (0) after PANELS; DCS-BIOS gives the letters S and C |
| 12. Cued Search (CUED) Button | CPG_LHG_CUED_SEARCH | read + command | button | 0 = released, 1 = pressed | Gunner CUED Search Button; PANELS: N/I, DCS-BIOS has the control |
| 13. Linear Motion Compensation (LMC) Button | CPG_LHG_LMC | read + command | button | 0 = released, 1 = pressed | Gunner Linear Motion Compensation Button |
| 14. Cage Button | — | — | no entry | — | No function; no DCS-BIOS control on this grip |

### TEDAC Right Handgrip (RHG) (p. 134)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. FCR Scan Size Switch | CPG_RHG_FCR_SCAN_UP_DN, CPG_RHG_FCR_SCAN_L_R | read + command | selector (3) spring | CPG_RHG_FCR_SCAN_UP_DN: 0 = Medium, 1 = Off, 2 = Zoom; CPG_RHG_FCR_SCAN_L_R: 0 = Narrow, 1 = Off, 2 = Wide | Two axes, spring-loaded, rest is the middle; after PANELS the UP_DN axis has Z forward (2) and M aft (0), the L_R axis N left (0) and W right (2) |
| 2. C-SCOPE Button | CPG_RHG_C_SCOPE | read + command | button | 0 = released, 1 = pressed | Gunner C-Scope Button |
| 3. FLIR Polarity Button | CPG_RHG_FLIR_POL | read + command | button | 0 = released, 1 = pressed | Gunner FLIR Polarity Button |
| 4. Laser Tracker (LT) Switch | CPG_RHG_LASER_TRACK | read + command | selector (3) | 0 = M, 1 = O, 2 = A | Gunner Laser Tracker Mode Switch; A forward (2), O centre (1), M aft (0) after PANELS; not spring-loaded |
| 5. Sight Select Switch | CPG_RHG_SIGHT_UP_DN, CPG_RHG_SIGHT_L_R | read + command | selector (3) spring | CPG_RHG_SIGHT_UP_DN: 0 = LINK, 1 = Off, 2 = HMD; CPG_RHG_SIGHT_L_R: 0 = FCR, 1 = Off, 2 = TADS | Two axes, spring-loaded, rest is the middle; after PANELS the UP_DN axis has HMD forward (2) and LINK aft (0), the L_R axis FCR left (0) and TADS right (2) |
| 6. Image Auto Track Polarity Switch | CPG_RHG_IAT_POL | read + command | selector (3) | 0 = B, 1 = A, 2 = W | Gunner Image Auto Tracker Polarity Switch; PANELS: N/I, positions not stated; DCS-BIOS has three positions, not spring-loaded |
| 7. Sight Slave Button | CPG_RHG_SIGHT_SLAVE | read + command | button | 0 = released, 1 = pressed | Gunner Sight Slave Button |
| 8. Sight Manual Tracker | CPG_RHG_MAN_TRK_UP_DN, CPG_RHG_MAN_TRK_L_R | read + command | selector (3) spring | CPG_RHG_MAN_TRK_UP_DN: 0 = Down, 1 = Off, 2 = Up; CPG_RHG_MAN_TRK_L_R: 0 = Left, 1 = Off, 2 = Right | Gunner Sight Manual Tracker Controller, the thumb force controller; two axes with three positions each, spring-loaded, rest is the middle (the dashboard TKR pad sends 2, 1 or 0 per axis) |
| 9. Display Zoom Button | CPG_RHG_DISP_ZOOM | read + command | button | 0 = released, 1 = pressed | Gunner Display Zoom Button |
| 10. LRFD Trigger | — | — | keybind | — | No DCS-BIOS control for the laser trigger |
| 11. MTT Track Promote Switch | — | — | keybind | — | No DCS-BIOS control by this name; the only other switch of the grip is an unnamed spare switch (see DCS-BIOS controls not in PANELS.md) |
| 12. Cursor Enter Button | CPG_RHG_ENTER | read + command | button | 0 = released, 1 = pressed | Gunner Cursor Enter Button |
| 13. Heads-Down Display (HDD) Button | CPG_RHG_HDD_SW | read + command | button | 0 = released, 1 = pressed | Gunner HDD/HOD Select Button; PANELS says no function; DCS-BIOS has the control |
| 14. Missile Advance Button | — | — | keybind | — | No DCS-BIOS control on the right handgrip; the collective mission grip has {S}_COLLECTIVE_MISSILE_ADVANCE (Collective Mission Grip) |

## Hand controls (cyclic and collective grips)

### Cyclic Grip (p. 136)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Force Trim/Hold Mode Switch | {S}_CYCLIC_TRIM_UD, {S}_CYCLIC_TRIM_LR | read + command | selector (3) spring | {S}_CYCLIC_TRIM_UD: 0 = D, 1 = Off, 2 = R; {S}_CYCLIC_TRIM_LR: 0 = AT, 1 = Off, 2 = A | Two axes, spring-loaded, rest is the middle; after PANELS the UD axis has R forward (2) and D aft (0), the LR axis AT left (0) and AL right (2); DCS-BIOS spells AL as A |
| 2. Weapon Action Switch (WAS) | {S}_CYCLIC_WEAPON_UD, {S}_CYCLIC_WEAPON_LR | read + command | selector (3) spring | {S}_CYCLIC_WEAPON_UD: 0 = A, 1 = Off, 2 = G; {S}_CYCLIC_WEAPON_LR: 0 = M, 1 = Off, 2 = R | Two axes, spring-loaded, rest is the middle; after PANELS the UD axis has G forward (2) and A aft (0); the LR axis disagrees with PANELS: DCS-BIOS lists 0 = M and 2 = R, PANELS has R on the left and M on the right; check in DCS |
| 3. Symbology Select Switch | {S}_CYCLIC_SYMBOLOGY, {S}_CYCLIC_SYMBOLOGY_PRESS | read + command | {S}_CYCLIC_SYMBOLOGY: selector (3) spring; {S}_CYCLIC_SYMBOLOGY_PRESS: button | {S}_CYCLIC_SYMBOLOGY: 0 = HB, 1 = Off, 2 = CT; {S}_CYCLIC_SYMBOLOGY_PRESS: 0 = released, 1 = pressed | The axis is spring-loaded, rest is the middle, CT forward (2) and HB aft (0) after PANELS; {S}_CYCLIC_SYMBOLOGY_PRESS is the depress (Symbology Select Switch - Depress) |
| 4. PTT/RTS Switch | {S}_CYCLIC_RTS, {S}_CYCLIC_RTS_PRESS | read + command | {S}_CYCLIC_RTS: selector (3) spring; {S}_CYCLIC_RTS_PRESS: none | {S}_CYCLIC_RTS: 0 = RADIO, 1 = Off, 2 = ICS; {S}_CYCLIC_RTS_PRESS: action only, no absolute value | The axis is spring-loaded, rest is the middle, RADIO left (0) and ICS right (2) after PANELS; {S}_CYCLIC_RTS_PRESS is the depress (PTT/RTS Switch - Depress), an input-only action; no output: {S}_CYCLIC_RTS_PRESS |
| 5. Chaff Dispense (C) Button | {S}_CYCLIC_CHAFF | read + command | button | 0 = released, 1 = pressed | Chaff Dispense |
| 6. Flare Dispense (FLARE) Button | {S}_CYCLIC_FLARE | read + command | button | 0 = released, 1 = pressed | Flare Dispense |
| 7. Weapon Trigger | {S}_CYCLIC_TRIGGER | read + command | selector (3) spring | 0 = Off, 1 = Half, 2 = Full | Weapons Trigger; positions Off, Half (first detent) and Full (second detent); spring-loaded, rest is the middle; cover {S}_CYCLIC_TRIGGER_COVER (0 = CLOSE, 1 = OPEN); dashboard blocklist |
| 8. Cage Button | {S}_CYCLIC_ATA_CAGE | read + command | button | 0 = released, 1 = pressed | likely; ATA Missile Cage/Uncage Button; PANELS says no function; DCS-BIOS has the ATA missile cage/uncage button |
| 9. FMC Release Button | {S}_CYCLIC_FMC_RELEASE | read + command | button | 0 = released, 1 = pressed | FMC Release Button |

### Collective Flight Grip (p. 138)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Emergency Jettison (JETT) Button | {S}_COLLECTIVE_JETTISON | read + command | button | 0 = released, 1 = pressed | Emergency Jettison Switch; cover {S}_COLLECTIVE_JETTISON_COVER (0 = CLOSE, 1 = OPEN); dashboard blocklist |
| 2. Boresight/Polarity Switch | {S}_COLLECTIVE_BS_PLRT | read + command | selector (3) spring | 0 = B/S, 1 = Off, 2 = PLRT | Boresight/Polarity Switch; PANELS gives two positions and no order; DCS-BIOS has a 3-position switch, spring-loaded, rest is the middle |
| 3. Searchlight Switch | {S}_COLLECTIVE_SEARCHLIGHT | read + command | selector (3) spring | 0 = STOW, 1 = Off, 2 = ON | Searchlight; ON forward (2), STOW aft (0) after PANELS; DCS-BIOS lists the whole switch as spring-loaded, rest is the middle |
| 4. Searchlight Position Switch | {S}_COLLECTIVE_SEARCHLIGHT_UD, {S}_COLLECTIVE_SEARCHLIGHT_LR | read + command | selector (3) spring | {S}_COLLECTIVE_SEARCHLIGHT_UD: 0 = RET, 1 = Off, 2 = EXT; {S}_COLLECTIVE_SEARCHLIGHT_LR: 0 = L, 1 = Off, 2 = R | Searchlight Position, two axes, spring-loaded, rest is the middle; after PANELS the UD axis has EXT forward (2) and RET aft (0), the LR axis L left (0) and R right (2) |
| 5. NVS Select Switch | {S}_COLLECTIVE_NVS_SELECT | read + command | selector (3) spring | 0 = PNVS, 1 = Off, 2 = TADS | NVS Select Switch; PANELS gives two positions (TADS forward, PNVS aft); DCS-BIOS has a 3-position switch, spring-loaded, rest is the middle |
| 6. Stabilator Control Switch | {S}_COLLECTIVE_STAB_CONTROL, {S}_COLLECTIVE_STAB_RESET | read + command | {S}_COLLECTIVE_STAB_CONTROL: selector (3) spring; {S}_COLLECTIVE_STAB_RESET: button | {S}_COLLECTIVE_STAB_CONTROL: 0 = NU, 1 = Off, 2 = ND; {S}_COLLECTIVE_STAB_RESET: 0 = released, 1 = pressed | The axis is spring-loaded, rest is the middle, ND forward (2) and NU aft (0) after PANELS; {S}_COLLECTIVE_STAB_RESET is the depress (Stabilator Control Switch - Reset) |
| 7. Engine Chop (CHOP) Button | {S}_COLLECTIVE_CHOP | read + command | button | 0 = released, 1 = pressed | CHOP Button; PANELS: N/I, DCS-BIOS has the control; cover {S}_COLLECTIVE_CHOP_COVER (0 = CLOSE, 1 = OPEN; DCS-BIOS names no positions for it, the cover rule is used); dashboard blocklist |
| 8. Tail Wheel Lock/Unlock Button | {S}_COLLECTIVE_TAIL_WHEEL | read + command | button | 0 = released, 1 = pressed | Tail Wheel Lock/Unlock |
| 9. BUCS Trigger (CPG only) | {S}_COLLECTIVE_BUCS | read + command | button | 0 = released, 1 = pressed | BUCS Trigger; PANELS: N/I and no function in the pilot seat; DCS-BIOS has the control in both stations; cover {S}_COLLECTIVE_BUCS_COVER (0 = CLOSE, 1 = OPEN); dashboard blocklist |

### Collective Mission Grip (p. 140)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. FCR Mode Switch | {S}_COLLECTIVE_FCR_MODE_UD, {S}_COLLECTIVE_FCR_MODE_LR | read + command | selector (3) spring | {S}_COLLECTIVE_FCR_MODE_UD: 0 = ATM, 1 = Off, 2 = GTM; {S}_COLLECTIVE_FCR_MODE_LR: 0 = TPM, 1 = Off, 2 = RMAP | Two axes, spring-loaded, rest is the middle; after PANELS the UD axis has GTM forward (2) and ATM aft (0), the LR axis TPM left (0) and RMAP right (2) |
| 2. FCR Scan Size Switch | {S}_COLLECTIVE_FCR_SCAN_SIZE_UD, {S}_COLLECTIVE_FCR_SCAN_SIZE_LR | read + command | selector (3) spring | {S}_COLLECTIVE_FCR_SCAN_SIZE_UD: 0 = M, 1 = Off, 2 = Z; {S}_COLLECTIVE_FCR_SCAN_SIZE_LR: 0 = N, 1 = Off, 2 = W | Two axes, spring-loaded, rest is the middle; after PANELS the UD axis has Z forward (2) and M aft (0), the LR axis N left (0) and W right (2) |
| 3. Cursor Controller/Enter (CURSOR) | {S}_COLLECTIVE_CURSOR_LR, {S}_COLLECTIVE_CURSOR_UD, {S}_COLLECTIVE_CURSOR_ENTER | read + command | {S}_COLLECTIVE_CURSOR_LR, {S}_COLLECTIVE_CURSOR_UD: knob; {S}_COLLECTIVE_CURSOR_ENTER: button | {S}_COLLECTIVE_CURSOR_LR, {S}_COLLECTIVE_CURSOR_UD: continuous, 0 to 65535; {S}_COLLECTIVE_CURSOR_ENTER: 0 = released, 1 = pressed | Cursor Controller L/R and U/D are analog axes, centre 32768 (the dashboard cursor pad sends the deflection from the centre); {S}_COLLECTIVE_CURSOR_ENTER is the press (Cursor Enter) |
| 4. Sight Select Switch | {S}_COLLECTIVE_SIGHT_SELECT_UD, {S}_COLLECTIVE_SIGHT_SELECT_LR | read + command | selector (3) spring | {S}_COLLECTIVE_SIGHT_SELECT_UD: 0 = LINK, 1 = Off, 2 = HMD; {S}_COLLECTIVE_SIGHT_SELECT_LR: 0 = FCR, 1 = Off, 2 = TADS | Two axes, spring-loaded, rest is the middle; after PANELS the UD axis has HMD forward (2) and LINK aft (0), the LR axis FCR left (0) and TADS right (2); TADS does nothing in the pilot seat |
| 5. Cursor Display Select Button | {S}_COLLECTIVE_CURSOR_DISPLAY | read + command | button | 0 = released, 1 = pressed | Cursor Display Select Button |
| 6. FCR Scan Switch | {S}_COLLECTIVE_FCR_SCAN | read + command | selector (3) spring | 0 = Continuous, 1 = Off, 2 = Single | FCR Scan Switch; spring-loaded, rest is the middle; S-SCAN forward (2), C-SCAN aft (0) after PANELS; DCS-BIOS names the ends Single and Continuous |
| 7. Cued Search (CUED) Button | {S}_COLLECTIVE_CUED_SEARCH | read + command | button | 0 = released, 1 = pressed | CUED Search Switch; PANELS: N/I, DCS-BIOS has the control |
| 8. Missile Advance Button | {S}_COLLECTIVE_MISSILE_ADVANCE | read + command | button | 0 = released, 1 = pressed | Missile Advance Switch |
| 9. Alternate Cursor Enter Trigger | {S}_COLLECTIVE_ALT_CURSOR_ENTER | read + command | button | 0 = released, 1 = pressed | Alternate Cursor Enter |

## Displays (EUFD, MPD)

### Enhanced Up-Front Display (EUFD) (p. 155)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Warning/Caution/Advisory (WCA) Scroll Rocker | {S}_EUFD_WCA | read + command | selector (3) spring | 0 = Down, 1 = Off, 2 = Up | Up-Front Display WCA Rocker Switch; spring-loaded, rest is the middle; PANELS lists up and down only |
| 5. Brightness Control Knob | {S}_EUFD_BRT | read + command | knob | continuous, 0 to 65535 | Up-Front Display Brightness Knob |
| 6. Preset Button | {S}_EUFD_PRESET | read + command | button | 0 = released, 1 = pressed | Up-Front Display Preset Button |
| 7. Enter Button | {S}_EUFD_ENT | read + command | button | 0 = released, 1 = pressed | Up-Front Display ENTER Button |
| 8. Datalink (DL) Transmit Select Rocker | {S}_EUFD_IDM | read + command | selector (3) spring | 0 = Down, 1 = Off, 2 = Up | likely; Up-Front Display IDM Rocker Switch; DCS-BIOS names it the IDM rocker switch; spring-loaded, rest is the middle |
| 9. Radio Transmit Select (RTS) Rocker | {S}_EUFD_RTS | read + command | selector (3) spring | 0 = Down, 1 = Off, 2 = Up | Up-Front Display RTS Rocker Switch; spring-loaded, rest is the middle |
| 12. Stopwatch Button | {S}_EUFD_STOPWATCH | read + command | button | 0 = released, 1 = pressed | Up-Front Display Stopwatch Button - Press to start/stop, Hold to reset |
| 13. Swap Button | {S}_EUFD_SWAP | read + command | button | 0 = released, 1 = pressed | Up-Front Display Swap Button |
| 2. Warning Message Area | {S}_EUFD_LINE1, {S}_EUFD_LINE2, {S}_EUFD_LINE3, {S}_EUFD_LINE4, {S}_EUFD_LINE5, {S}_EUFD_LINE6, {S}_EUFD_LINE7 | read only | display | text | likely; the display is 14 lines of 56 characters; in the DCS-BIOS display module the warning list starts at column 1 of lines 1 to 7 (caution list at column 20, advisory list at column 39 of the same lines) |
| 3. Caution Message Area | {S}_EUFD_LINE1, {S}_EUFD_LINE2, {S}_EUFD_LINE3, {S}_EUFD_LINE4, {S}_EUFD_LINE5, {S}_EUFD_LINE6, {S}_EUFD_LINE7 | read only | display | text | likely; lines 1 to 7 as for the Warning Message Area; the caution list starts at column 20 |
| 4. Advisory Message Area | {S}_EUFD_LINE1, {S}_EUFD_LINE2, {S}_EUFD_LINE3, {S}_EUFD_LINE4, {S}_EUFD_LINE5, {S}_EUFD_LINE6, {S}_EUFD_LINE7 | read only | display | text | likely; lines 1 to 7 as for the Warning Message Area; the advisory list starts at column 39 (the preset list uses the same columns) |
| 10. Information Display Area | {S}_EUFD_LINE14 | read only | display | text | likely; line 14: fuel, transponder fields and the time; the stopwatch is on line 13 |
| 11. Radio Status Area | {S}_EUFD_LINE8, {S}_EUFD_LINE9, {S}_EUFD_LINE10, {S}_EUFD_LINE11, {S}_EUFD_LINE12 | read only | display | text | likely; lines 8 to 12 hold the five radios in the order VHF, UHF, FM1, FM2, HF; the lines are the source of the frequencies, the separate DCS-BIOS radio frequency strings are unreliable (see Radio frequencies in the DCS-BIOS controls not in PANELS.md) |
| 11. Radio Status Area - sixth line | {S}_EUFD_LINE13 | read only | display | text | likely; line 13 holds the extra HF transmission line; PANELS: N/I |
| 11. Radio Status Area - GUARD receiver, power and standby network fields | {S}_EUFD_LINE8, {S}_EUFD_LINE9, {S}_EUFD_LINE10, {S}_EUFD_LINE11, {S}_EUFD_LINE12 | read only | display | text | likely; the same lines 8 to 12; the guard, power and standby network fields are characters of these lines |
| 11. Radio Status Area - transmit select indicators | {S}_EUFD_LINE8, {S}_EUFD_LINE9, {S}_EUFD_LINE10, {S}_EUFD_LINE11, {S}_EUFD_LINE12 | read only | display | text | likely; the same lines 8 to 12; the first columns carry the transmit select fields; the symbols are characters of the lines |

### Multi-Purpose Displays (MPD) (p. 164)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Variable Action Buttons T1 to T6 (top row) | {S}_MPD_L_T1, {S}_MPD_L_T2, {S}_MPD_L_T3, {S}_MPD_L_T4, {S}_MPD_L_T5, {S}_MPD_L_T6, {S}_MPD_R_T1, {S}_MPD_R_T2, {S}_MPD_R_T3, {S}_MPD_R_T4, {S}_MPD_R_T5, {S}_MPD_R_T6 | read + command | button | 0 = released, 1 = pressed | Left MPD (MPD_L) and right MPD (MPD_R) of either station; T1 far left to T6 far right |
| 1. Variable Action Buttons L1 to L6 (left column) | {S}_MPD_L_L1, {S}_MPD_L_L2, {S}_MPD_L_L3, {S}_MPD_L_L4, {S}_MPD_L_L5, {S}_MPD_L_L6, {S}_MPD_R_L1, {S}_MPD_R_L2, {S}_MPD_R_L3, {S}_MPD_R_L4, {S}_MPD_R_L5, {S}_MPD_R_L6 | read + command | button | 0 = released, 1 = pressed | left MPD (MPD_L) and right MPD (MPD_R); L1 top to L6 bottom; CP/G: CPG_MPD_L_L1 to CPG_MPD_L_L6 did not respond in DCS |
| 1. Variable Action Buttons R1 to R6 (right column) | {S}_MPD_L_R1, {S}_MPD_L_R2, {S}_MPD_L_R3, {S}_MPD_L_R4, {S}_MPD_L_R5, {S}_MPD_L_R6, {S}_MPD_R_R1, {S}_MPD_R_R2, {S}_MPD_R_R3, {S}_MPD_R_R4, {S}_MPD_R_R5, {S}_MPD_R_R6 | read + command | button | 0 = released, 1 = pressed | left MPD (MPD_L) and right MPD (MPD_R); R1 top to R6 bottom |
| 1. Variable Action Buttons B1 to B6 (bottom row) | {S}_MPD_L_B1, {S}_MPD_L_B2, {S}_MPD_L_B3, {S}_MPD_L_B4, {S}_MPD_L_B5, {S}_MPD_L_B6, {S}_MPD_R_B1, {S}_MPD_R_B2, {S}_MPD_R_B3, {S}_MPD_R_B4, {S}_MPD_R_B5, {S}_MPD_R_B6 | read + command | button | 0 = released, 1 = pressed | left MPD (MPD_L) and right MPD (MPD_R); B1 far left to B6 far right; B1 is also the M button (row 7) |
| 2. VID Knob | {S}_MPD_L_VIDEO, {S}_MPD_R_VIDEO | read + command | knob | continuous, 0 to 65535 | Video Control Knob; left MPD (MPD_L) and right MPD (MPD_R) |
| 3. BRT Knob | {S}_MPD_L_BRT, {S}_MPD_R_BRT | read + command | knob | continuous, 0 to 65535 | Brightness Control Knob; left MPD (MPD_L) and right MPD (MPD_R) |
| 4. Mode Knob | {S}_MPD_L_MODE, {S}_MPD_R_MODE | read + command | selector (3) | 0 = MONO, 1 = NIGHT, 2 = DAY | DCS-BIOS spells NT as NIGHT; reverse order of PANELS; a direct command did not work in DCS, the dashboard turns the knob with INC / DEC steps; left MPD (MPD_L) and right MPD (MPD_R) |
| 5. Asterisk (*) Button | {S}_MPD_L_AST, {S}_MPD_R_AST | read + command | button | 0 = released, 1 = pressed | PANELS: N/I, DCS-BIOS has the control; left MPD (MPD_L) and right MPD (MPD_R) |
| 6. Fixed Action Button FCR | {S}_MPD_L_FCR, {S}_MPD_R_FCR | read + command | button | 0 = released, 1 = pressed | left MPD (MPD_L) and right MPD (MPD_R) |
| 6. Fixed Action Button WPN | {S}_MPD_L_WPN, {S}_MPD_R_WPN | read + command | button | 0 = released, 1 = pressed | left MPD (MPD_L) and right MPD (MPD_R) |
| 6. Fixed Action Button TSD | {S}_MPD_L_TSD, {S}_MPD_R_TSD | read + command | button | 0 = released, 1 = pressed | left MPD (MPD_L) and right MPD (MPD_R) |
| 6. Fixed Action Button VID | {S}_MPD_L_VID, {S}_MPD_R_VID | read + command | button | 0 = released, 1 = pressed | left MPD (MPD_L) and right MPD (MPD_R) |
| 6. Fixed Action Button COM | {S}_MPD_L_COM, {S}_MPD_R_COM | read + command | button | 0 = released, 1 = pressed | left MPD (MPD_L) and right MPD (MPD_R) |
| 6. Fixed Action Button A/C | {S}_MPD_L_AC, {S}_MPD_R_AC | read + command | button | 0 = released, 1 = pressed | left MPD (MPD_L) and right MPD (MPD_R) |
| 7. M Button (VAB B1) | {S}_MPD_L_B1, {S}_MPD_R_B1 | read + command | button | 0 = released, 1 = pressed | B1/M (Menu) Button, the same ids as B1 in the bottom row; left MPD (MPD_L) and right MPD (MPD_R) |
| MPD screen | — | — | export | — | No DCS-BIOS control. The export script sends the MPD text (list_indication 7 and 9 for the pilot's left and right MPD, 11 and 13 for the CP/G's, 4 times per second); the dashboard reads the button labels from its PB fields |
| Menu page | — | — | export | — | No DCS-BIOS control; the page text comes with the MPD text of the export script |
| Variable Action Button label styles | — | — | export | — | No DCS-BIOS control; the export script sends the label text of each button (PB fields), the dashboard does not read the label shapes |

## DCS-BIOS controls not in PANELS.md

These controls exist in DCS-BIOS but no panel of PANELS.md describes them (the manual does not cover them, or they belong to the cockpit or the external model). Columns as above, with the DCS-BIOS identifier first; the description is the DCS-BIOS one, the Note gives the build and the position order. `{S}_` is used as in the areas above.

### Lighting (DCS-BIOS only)

| DCS-BIOS identifier | Access | Description | Note |
| --- | --- | --- | --- |
| {S}_INT_FLOOD_L | read only | Flood Lightning (light green) | bar or gauge; 0 to 65535 |
| PLT_INT_GAUGES_L | read only | Pilot Gauges Lightning (light green) | bar or gauge; 0 to 65535 |
| {S}_INT_PANEL_L | read only | Panel Lightning (light green) | bar or gauge; 0 to 65535 |
| {S}_SIGNAL_L | read only | Signal Light (multi color) | bar or gauge; 0 to 65535 |

### Sunvisors (DCS-BIOS only)

| DCS-BIOS identifier | Access | Description | Note |
| --- | --- | --- | --- |
| PLT_L_SUNVISOR | read + command | Pilot Left Sunvisor | selector (2); two positions, DCS-BIOS names none |
| PLT_R_SUNVISOR | read + command | Pilot Right Sunvisor | selector (2); two positions, DCS-BIOS names none |
| PLT_SUNVISOR_L | read + command | Pilot Left Sunvisor | knob; continuous, 0 to 65535 |
| PLT_SUNVISOR_R | read + command | Pilot Right Sunvisor | knob; continuous, 0 to 65535 |

### M4 rifle (DCS-BIOS only)

| DCS-BIOS identifier | Access | Description | Note |
| --- | --- | --- | --- |
| {S}_M4_SAVE | read + command | M4 Safety | selector (3); 0 = Safe, 1 = Semi, 2 = Auto; takes about 3 s to reach the position |
| {S}_M4_TRIGGER | read + command | M4 Trigger | button; 0 = released, 1 = pressed; dashboard blocklist |

### Canopy and stick fold (DCS-BIOS only)

| DCS-BIOS identifier | Access | Description | Note |
| --- | --- | --- | --- |
| CPG_CANOPY | read + command | Gunner Canopy | selector (2); 0 = CLOSE, 1 = OPEN; did not work in DCS (the canopy, in both seats); DCS-BIOS cannot move the canopy, a key does; the pilot's PLT_CANOPY is read back by the dashboard |
| CPG_STICK_FOLD | read + command | Gunner Stick Folding | selector (2); 0 = UP, 1 = DOWN; did not work in DCS |
| {S}_CANOPY_POS | read only | Canopy Position | bar or gauge; 0 to 65535 |

### TEDAC Right Handgrip (DCS-BIOS only)

| DCS-BIOS identifier | Access | Description | Note |
| --- | --- | --- | --- |
| CPG_RHG_SPARE | read + command | Gunner Spare Switch | selector (3) spring; 0 = Down, 1 = Off, 2 = Up; DCS-BIOS gives it no function; PANELS has no row for it |

### Vibration gauges (DCS-BIOS only)

| DCS-BIOS identifier | Access | Description | Note |
| --- | --- | --- | --- |
| VIB_HOOK_SWING | read only | Vibration Hook Swinging | bar or gauge; 0 to 65535 |
| VIB_HOOK_TURN | read only | Vibration Hook Turning | bar or gauge; 0 to 65535 |
| VIB_REMOVE | read only | Vibration Remove Before Flight | bar or gauge; 0 to 65535 |
| VIB_SHEET | read only | Vibration Sheet | bar or gauge; 0 to 65535 |
| VIB_SUNSHADE | read only | Vibration SunShade | bar or gauge; 0 to 65535 |

### External Aircraft Model (DCS-BIOS only)

| DCS-BIOS identifier | Access | Description | Note |
| --- | --- | --- | --- |
| EXT_FORMATION_LIGHTS | read only | Formation Lights (yellow green) | none (metadata); 0 to 65535 |
| EXT_GUN_POS_BELT_FEED | read only | Gun Belt Feed | none (metadata); 0 to 65535 |
| EXT_GUN_POS_PITCH | read only | Gun Pitch | none (metadata); 0 to 65535 |
| EXT_GUN_POS_RECOIL | read only | Gun Recoil | none (metadata); 0 to 65535 |
| EXT_GUN_POS_YAW | read only | Gun Yaw | none (metadata); 0 to 65535 |
| EXT_LAND_LIGHT | read only | Landing Light (white) | none (metadata); 0 or 1 |
| EXT_LIGHT_L | read only | Left Light (white) | none (metadata); 0 or 1 |
| EXT_LIGHT_R | read only | Right Light (white) | none (metadata); 0 or 1 |
| EXT_LIGHT_TAIL | read only | Tail Light (white) | none (metadata); 0 or 1 |
| EXT_PNVS_POS_YAW | read only | PNVS Yaw | none (metadata); 0 to 65535 |
| EXT_POSITION_LIGHT_LEFT | read only | Left Position Light (red) | none (metadata); 0 or 1 |
| EXT_POSITION_LIGHT_RIGHT | read only | Right Position Light (green) | none (metadata); 0 or 1 |
| EXT_ROTOR | read only | Rotor Move | none (metadata); 0 to 65535 |
| EXT_STROBE_L | read only | Left Strobe Light (red) | none (metadata); 0 or 1 |
| EXT_STROBE_R | read only | Right Strobe Light (red) | none (metadata); 0 or 1 |
| EXT_TADS_POS_PITCH | read only | TADS Pitch | none (metadata); 0 to 65535 |
| EXT_TADS_POS_YAW | read only | TADS Yaw | none (metadata); 0 to 65535 |
| EXT_WIPER_CPG | read only | Wiper Gunner | none (metadata); 0 to 65535 |
| EXT_WIPER_PLT | read only | Wiper Pilot | none (metadata); 0 to 65535 |
| EXT_WOW_LEFT | read only | Weight ON Wheels Left Gear | none (metadata); 0 or 1 |
| EXT_WOW_RIGHT | read only | Weight ON Wheels Right Gear | none (metadata); 0 or 1 |
| EXT_WOW_TAIL | read only | Weight ON Wheels Tail Gear | none (metadata); 0 or 1 |

### Radio frequencies (DCS-BIOS only)

| DCS-BIOS identifier | Access | Description | Note |
| --- | --- | --- | --- |
| FM1_RADIO | read + command | FM1 Radio | display; text, 6 characters; the DCS-BIOS radio strings are unreliable (HF stays at a start value); the EUFD lines carry the frequencies |
| FM2_RADIO | read + command | FM2 Radio | display; text, 6 characters; the DCS-BIOS radio strings are unreliable (HF stays at a start value); the EUFD lines carry the frequencies |
| HF_RADIO | read + command | HF Radio | display; text, 6 characters; the DCS-BIOS radio strings are unreliable (HF stays at a start value); the EUFD lines carry the frequencies |
| UHF_RADIO | read + command | UHF Radio | display; text, 7 characters; the DCS-BIOS radio strings are unreliable (HF stays at a start value); the EUFD lines carry the frequencies |
| VHF_AM_RADIO | read + command | VHF AM Radio | display; text, 7 characters; the DCS-BIOS radio strings are unreliable (HF stays at a start value); the EUFD lines carry the frequencies |

### Seat (DCS-BIOS only)

| DCS-BIOS identifier | Access | Description | Note |
| --- | --- | --- | --- |
| SEAT_POSITION | read only | Player's current seat position (0 = Pilot, 1 = CP/G) | none (metadata); 0 or 1 |

## Summary

Rows counted over all area tables above the "DCS-BIOS controls not in PANELS.md" section (one per PANELS.md row, so the Access `—` rows are the rows without an identifier); the DCS-BIOS-only column counts the rows of the "DCS-BIOS controls not in PANELS.md" section, because the area tables have no rows of their own for DCS-BIOS-only controls.

| Access | PANELS.md rows | DCS-BIOS-only rows |
| --- | --- | --- |
| read + command | 177 | 14 |
| read only | 50 | 33 |
| — | 25 | 0 |
| Total | 252 | 47 |

The "DCS-BIOS controls not in PANELS.md" section has 47 rows (14 read + command, 33 read only); a row with `{S}_` stands for two controls, so the rows cover 53 of the module's 714 controls. The identifiers in the area tables (cells and Notes, `{S}_` counted for both stations) cover the other 661: 714 in all.

### Gaps

Every row without a DCS-BIOS identifier in the area sections above, grouped by its gap (25 rows).

#### keybind (4)

- TEDAC Left Handgrip (LHG): 10. Weapon Trigger
- TEDAC Right Handgrip (RHG): 10. LRFD Trigger
- TEDAC Right Handgrip (RHG): 11. MTT Track Promote Switch
- TEDAC Right Handgrip (RHG): 14. Missile Advance Button

#### export (4)

- Items named only in the pilot overview figure: Anti-Torque Pedals
- Multi-Purpose Displays (MPD): MPD screen
- Multi-Purpose Displays (MPD): Menu page
- Multi-Purpose Displays (MPD): Variable Action Button label styles

#### no entry (17)

- Canopy Jettison Handle: Canopy Jettison Handle
- Standby Attitude Indicator: 1. Bank Angle Scale
- Standby Attitude Indicator: 4. Aircraft Symbol (Waterline)
- Standby Attitude Indicator: 5. Pitch Scale
- Standby Airspeed Indicator: 2. Indicated Airspeed Scale
- Standby Altimeter: 1. 1000-foot Altitude Scale
- Keyboard Unit (KU): 1. Display Prompt
- Free Air Temperature Gauge: 2. Temperature Scale
- Items named only in the pilot overview figure: Boresight Reticle Unit (BRU)
- Items named only in the pilot overview figure: Data Transfer Unit (DTU) receptacle
- Console fittings named only in the overview figures: Utility Light
- Console fittings named only in the overview figures: Canopy Jettison Handle Pin
- Console fittings named only in the overview figures: First Aid Kit
- Console fittings named only in the overview figures: HDU Storage Holster
- TEDAC Display Unit (TDU): TDU screen
- TEDAC Left Handgrip (LHG): 3. Video Record Button
- TEDAC Left Handgrip (LHG): 14. Cage Button
