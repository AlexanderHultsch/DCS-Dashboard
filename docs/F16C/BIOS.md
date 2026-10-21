# F-16C Viper – DCS-BIOS mapping

Maps every control in [PANELS.md](PANELS.md) to its DCS-BIOS identifier. Source: the DCS-Skunkworks DCS-BIOS module `F-16C_50` (`Scripts/DCS-BIOS/lib/modules/aircraft_modules/F-16C_50.lua`, version V1.15f, commit 11c6209 of 2026-10-08), which also serves the F-16D and F-16I variants. The module has 522 controls. Input kinds, build types and position orders come from the table that `core/tools/test/bios_check.py` makes for all 522 ids (see its row in `core/tools/test/README.md`), checked against the module Lua.

Sections and control names follow PANELS.md. Columns:

- **DCS-BIOS identifier**: the name used to read and command the control; `—` if there is none. A control with several parts (button and lamp, two axes, left and right MFD) lists all its identifiers.
- **Access**: `read + command` (an input and an output exist), `read only` (lamps, gauges, text: `defineIndicatorLight`, `defineFloat`, `defineString`, `defineFloatFromDrawArgument`, `defineBitFromDrawArgument`, `defineIntegerFromGetter`), or `—`. A row with several identifiers shows `read + command` if any of them takes commands; the Note then names the read only ones.
- **Build**: the dashboard control the identifier becomes, from the classification table: `button` (push button), `selector (N)` (N fixed positions; `spring` = spring-loaded, returns to the middle), `knob` (continuous, 0 to 65535), `step rocker (3200)` (relative only: step up or down, the position comes back as `<id>_KNOB_POS`), `lamp`, `display` (text), `bar or gauge` (0 to 65535), `none` (metadata of the external model). `NO READBACK` is appended where no output is named like the identifier, so the dashboard cannot read the state under its own name. With several identifiers of different builds the cell reads `identifiers: build`. For a control without an identifier the cell holds the gap: `keybind` (needs a DCS key), `export` (needs the export script), `no function in DCS`, or `not exported`.
- **Position order**: the value of each position, as DCS-BIOS defines it (the positions list of the control, or the order in the DCS-BIOS description). Where DCS-BIOS gives no order the cell starts with `guess:` and the order is a guess for phase 7 (check in DCS). Rules used for guesses: toggles and levers list the PANELS.md positions top to bottom = highest value first (the order that held for toggles on the A-10C); rotary selectors and knobs list them in the order PANELS.md gives, lowest value first; spring-loaded rockers and levers run 0 = DN, 1 = CENTER (rest), 2 = UP; covers run 0 = CLOSE, 1 = OPEN. Buttons are 0 = released, 1 = pressed; lamps 0 = off, 1 = lit; gauges, counters and knobs 0 to 65535; displays are text.
- **Note**: the DCS-BIOS description or positions where they differ from PANELS.md, `likely` when the match is by meaning rather than by name, and for controls without an identifier the reason. For a guessed 2-position toggle the DCS-BIOS description is given too: its `A/B` form names the two positions but does not say which is 0.

## Hands-on controls (HOTAS)

### Side Stick Controller (SSC) (p. 83)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Weapon Release Button | — | — | keybind | — |  |
| 2. Trim Switch (4-way) | — | — | keybind | — |  |
| 3. Trigger (2-position) | — | — | keybind | — |  |
| 4. Missile Step Button | — | — | keybind | — | The AR/NWS lamp is LIGHT_AR_NWS (AR Status / NWS Indicator) |
| 5. Target Management Switch (TMS) (4-way) | — | — | keybind | — |  |
| 6. Display Management Switch (DMS) (4-way) | — | — | keybind | — |  |
| 7. Countermeasures Management Switch (CMS) (4-way) | — | — | keybind | — |  |
| 8. Paddle Switch | — | — | keybind | — |  |
| 9. Expand / FOV Button | — | — | keybind | — |  |

### Throttle (p. 86)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Throttle lever | THROTTLE_OFF_IDLE | read + command | button | 0 = released, 1 = pressed | likely; Throttle Off/Idle: only the move between OFF and IDLE; the lever position is not an output, so MIL and MAX AB (axis) need a keybind |
| Throttle Cutoff Release | — | — | not exported | — | No separate control; the OFF to IDLE move is THROTTLE_OFF_IDLE on the Throttle lever row |
| 1. UHF VHF Transmit Switch (4-way) | — | — | keybind | — |  |
| 2. MAN RNG / UNCAGE Knob | — | — | keybind | — |  |
| 3. DOG FIGHT Switch (3-position) | — | — | keybind | — |  |
| 4. ANT ELEV Knob | — | — | keybind | — |  |
| 5. RDR CURSOR / ENABLE Switch | — | — | keybind | — |  |
| 6. SPD BRK Switch (3-position, aft momentary) | — | — | keybind | — | The speed brake position is SPEEDBRAKE_INDICATOR (Landing Gear Panel) |

## Instrument panel

### AoA Indexer (p. 44)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Dimming Lever | AOA_INDEX_BRT_KNB | read + command | knob | continuous, 0 to 65535 | AOA Indexer Dimming Lever |
| 2. High AoA light | LIGHT_AOA_UP | read only | lamp | 0 = off, 1 = lit | AoA Light up (red) |
| 3. Optimal AoA light | LIGHT_AOA_MID | read only | lamp | 0 = off, 1 = lit | AoA Light mid (green) |
| 4. Low AoA light | LIGHT_AOA_DN | read only | lamp | 0 = off, 1 = lit | AoA Light down (yellow) |

### AR Status / NWS Indicator (p. 45)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Dimming Lever | AR_STATUS_BRT_KNB | read + command | knob | continuous, 0 to 65535 | AR Status Indicator Dimming Lever |
| 2. RDY light | LIGHT_RDY | read only | lamp | 0 = off, 1 = lit | RDY Light (blue) |
| 3. AR / NWS light | LIGHT_AR_NWS | read only | lamp | 0 = off, 1 = lit | AR NWS Light (green) |
| 4. DISC light | LIGHT_DISC | read only | lamp | 0 = off, 1 = lit | DISC Light (red) |

### Left Eyebrow Lights (p. 45)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. MASTER CAUTION button | MASTER_CAUTION, LIGHT_MASTER_CAUTION | read + command | MASTER_CAUTION: button; LIGHT_MASTER_CAUTION: lamp | MASTER_CAUTION: 0 = released, 1 = pressed; LIGHT_MASTER_CAUTION: 0 = off, 1 = lit | Button plus its lamp; read only: LIGHT_MASTER_CAUTION |
| 2. TF-FAIL warning light | LIGHT_TF_FAIL | read only | lamp | 0 = off, 1 = lit | TF FAIL Light (red) |
| 3. F-ACK button | F_ACK_BTN | read + command | button | 0 = released, 1 = pressed | F-ACK Button |
| 4. IFF IDENT button | IFF_ID_BTN | read + command | button | 0 = released, 1 = pressed | IFF IDENT Button |

### Right Eyebrow Lights (p. 46)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. ENG FIRE warning light | LIGHT_ENG_FIRE | read only | lamp | 0 = off, 1 = lit | ENG FIRE Light (red) |
| 2. ENGINE warning light | LIGHT_ENGINE | read only | lamp | 0 = off, 1 = lit | ENGINE Light (red) |
| 3. HYD / OIL PRESS warning lights | LIGHT_HYD_OIL_PRESS | read only | lamp | 0 = off, 1 = lit | One id for the split light |
| 4. FLCS warning light | LIGHT_FLCS | read only | lamp | 0 = off, 1 = lit | FLCS Light (red) |
| 5. DBU ON warning light | LIGHT_DBU_ON | read only | lamp | 0 = off, 1 = lit | DBU ON Light (red) |
| 6. TO / LDG CONFIG warning lights | LIGHT_TO_LDG_CONFIG | read only | lamp | 0 = off, 1 = lit | One id for the split light |
| 7. CANOPY warning light | LIGHT_CANOPY | read only | lamp | 0 = off, 1 = lit | CANOPY Light (red) |
| 8. OXY LOW warning light | LIGHT_OXY_LOW | read only | lamp | 0 = off, 1 = lit | OXY LOW Light (red) |

### Miscellaneous (MISC) Panel (p. 47)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. RF Switch | RF_SW | read + command | selector (3) | 0 = SILENT, 1 = QUIET, 2 = NORM | Category UFC in DCS-BIOS; reverse order of PANELS |
| 2. ECM light | LIGHT_ECM | read only | lamp | 0 = off, 1 = lit | ECM Light (green) |
| 3. LASER ARM Switch | LASER_ARM_SW | read + command | selector (2) | guess: 0 = OFF, 1 = LASER ARM | LASER ARM Switch, ARM/OFF |
| 4. ALT REL Button | ALT_REL_BTN | read + command | button | 0 = released, 1 = pressed | ALT REL Button - Push to release |
| 5. MASTER ARM Switch | MASTER_ARM_SW | read + command | selector (3) | 0 = MASTER ARM, 1 = OFF, 2 = SIMULATE | MASTER ARM Switch |
| 6. ADV MODE Button | ADV_MODE_SW, LIGHT_ACTIVE, LIGHT_STBY | read + command | ADV_MODE_SW: selector (2); LIGHT_ACTIVE, LIGHT_STBY: lamp | ADV_MODE_SW: guess: 0 = off, 1 = on; LIGHT_ACTIVE, LIGHT_STBY: 0 = off, 1 = lit | Switch (toggle) in DCS-BIOS, a push button in PANELS; the ACTIVE (green) and STBY (yellow) lights come from the module section Advance Mode Switch; read only: LIGHT_ACTIVE, LIGHT_STBY |
| 7. Autopilot ROLL Switch | AP_ROLL_SW | read + command | selector (3) | 0 = STRG SEL, 1 = ATT HOLD, 2 = HDG SEL | Autopilot ROLL Switch; reverse order of PANELS |
| 7. Autopilot PITCH Switch | AP_PITCH_SW | read + command | selector (3) spring | 0 = ATT HOLD, 1 = A/P OFF, 2 = ALT HOLD | Spring-loaded; PANELS says the solenoid holds ALT HOLD and ATT HOLD; reverse order of PANELS |

### Autopilot controls (pp. 129 to 132)

- This section of PANELS.md has no rows of its own; the controls it names are mapped where they are listed: the ROLL and PITCH switches (AP_ROLL_SW, AP_PITCH_SW) on the Miscellaneous (MISC) Panel, the paddle switch on the Side Stick Controller (keybind) and the heading set knob on the EHSI (EHSI_HDG_SET_KNB).
- The steerpoint used by STRG SEL is chosen with the ICP (ICP_BTN_* keys); the DED text is DED_L1 to DED_L5.

### Standby Attitude Indicator (SAI) (p. 49)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Attitude sphere | SAI_PITCH, SAI_BANK | read only | bar or gauge | 0 to 65535 along the scale | Pitch and bank as separate outputs |
| 2. Aircraft symbol (waterline) | SAI_AIRCRAFTREFERENCESYMBOL | read only | bar or gauge | 0 to 65535 along the scale | SAI Aircraft Reference Symbol; moves with the cage knob turn |
| 3. Roll indicator | SAI_BANK_ARROW | read only | bar or gauge | 0 to 65535 along the scale | likely; SAI Bank Arrow |
| 4. Roll indicator scale | — | — | no function in DCS | — | Fixed scale |
| 5. Pitch trim scale | SAI_KNB_ARROW | read only | bar or gauge | 0 to 65535 along the scale | likely; SAI Knob Arrow; the arrow reads against this scale |
| 6. PULL TO CAGE Knob | SAI_CAGE, SAI_PITCH_TRIM | read + command | SAI_CAGE: button; SAI_PITCH_TRIM: knob | SAI_CAGE: 0 = released, 1 = pressed; SAI_PITCH_TRIM: continuous, 0 to 65535 | Pull is SAI_CAGE (SAI Cage Knob, pull to cage); turn is SAI_PITCH_TRIM (adjust aircraft reference symbol) |
| OFF warning flag | SAI_OFF_FLAG | read only | bar or gauge | 0 to 65535 along the scale | SAI Off Flag |

### Fuel Flow Indicator (p. 50)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Fuel flow pointer | FUELFLOWCOUNTER_100, FUELFLOWCOUNTER_1K, FUELFLOWCOUNTER_10K | read only | bar or gauge | 0 to 65535 along the scale | likely; Counter drums for the 100, 1000 and 10000 lb digits, no pointer output |

### Engine Instruments (p. 50)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Engine OIL pressure indicator | ENGINE_OIL_PRESSURE | read only | bar or gauge | 0 to 65535 along the scale | Oil Pressure Indicator |
| 2. Engine NOZ POS indicator | ENGINE_NOZZLE_POSITION | read only | bar or gauge | 0 to 65535 along the scale | Engine Nozzle Position Indicator |
| 3. Engine RPM indicator | ENGINE_TACHOMETER | read only | bar or gauge | 0 to 65535 along the scale | Engine Tachometer Indicator |
| 4. Engine FTIT indicator | ENGINE_FTIT | read only | bar or gauge | 0 to 65535 along the scale | Engine FTIT Indicator |

### Airspeed and Mach Indicator (p. 51)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. VNE indicator | MAX_AIRSPEED | read only | bar or gauge | 0 to 65535 along the scale | likely; Max Airspeed |
| 2. Indicated airspeed scale | — | — | no function in DCS | — | Fixed outer scale; the pointer is AIRSPEED |
| 3. Mach indicator window | MACH_INDICATOR | read only | bar or gauge | 0 to 65535 along the scale | Mach Indicator |
| 4. Airspeed indicator | AIRSPEED | read only | bar or gauge | 0 to 65535 along the scale | Airspeed Indicator |
| 5. Airspeed reference index | SET_AIRSPEED | read only | bar or gauge | 0 to 65535 along the scale | Set Airspeed |
| 6. SET INDEX Knob | AIRSPEED_SET_KNB | read + command | step rocker (3200) | step up or down only, no absolute value | Turn only; the index position is SET_AIRSPEED |

### Altimeter (p. 51)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Altitude scale | — | — | no function in DCS | — | Fixed scale |
| 2. 1000-ft scale indicator | ALT_100_FT_PTR | read only | bar or gauge | 0 to 65535 along the scale | likely; Altimeter 100 ft pointer |
| 3. PNEU flag | ALT_PNEU_FLAG | read only | bar or gauge | 0 to 65535 along the scale | Altimeter PNEU Flag |
| 4. Altitude indicator | ALT_10000_FT_CNT, ALT_1000_FT_CNT, ALT_100_FT_CNT | read only | bar or gauge | 0 to 65535 along the scale | Counters for the 10000, 1000 and 100 ft digits |
| 5. Kollsman window | ALT_PRESSURE_DRUM_0_CNT, ALT_PRESSURE_DRUM_1_CNT, ALT_PRESSURE_DRUM_2_CNT, ALT_PRESSURE_DRUM_3_CNT | read only | bar or gauge | 0 to 65535 along the scale | Pressure setting drums 0 to 3 |
| 6. Barometric Setting Knob | ALT_BARO_SET_KNB | read + command | step rocker (3200) | step up or down only, no absolute value | Turn only; the knob position is ALT_BARO_SET_KNB_KNOB_POS |
| 7. Altimeter Mode Switch | ALT_MODE_LV | read + command | selector (3) spring | 0 = ELEC, 1 = OFF, 2 = PNEU | Spring-loaded; PANELS lists only ELEC and PNEU |

### Angle-of-Attack (AoA) Indicator (p. 52)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. AoA scale tape | — | — | no function in DCS | — | Fixed scale; the value is AOA_VALUE |
| 2. Current AoA marker | AOA_VALUE | read only | bar or gauge | 0 to 65535 along the scale | AoA Value |
| 3. High AoA region marker | — | — | no function in DCS | — | Fixed marker |
| 4. Optimal AoA region marker | — | — | no function in DCS | — | Fixed marker |
| 5. Low AoA region marker | — | — | no function in DCS | — | Fixed marker |

### Vertical Velocity Indicator (VVI) (p. 52)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Vertical velocity tape | — | — | no function in DCS | — | Fixed scale; the value is VVI |
| 2. Current vertical velocity marker | VVI | read only | bar or gauge | 0 to 65535 along the scale | VVI |
| 3. Positive region marker | — | — | no function in DCS | — | Fixed shading |
| 4. Negative region marker | — | — | no function in DCS | — | Fixed shading |

### Attitude Director Indicator (ADI) (p. 53)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Attitude sphere | ADI_PITCH, ADI_BANK | read only | bar or gauge | 0 to 65535 along the scale | Pitch and bank as separate outputs |
| 2. Upper bank angle indicator | ADI_BANK | read only | bar or gauge | 0 to 65535 along the scale | likely; Pointer rides with the sphere |
| 3. Pitch scale | — | — | no function in DCS | — | Printed on the sphere; moves with ADI_PITCH |
| 4. Glideslope deviation indicator | ADI_GS_POINTER | read only | bar or gauge | 0 to 65535 along the scale | ADI GS Pointer |
| 5. Glideslope deviation scale | — | — | no function in DCS | — | Fixed scale |
| 6. Aircraft symbol (waterline) | — | — | no function in DCS | — | Fixed symbol |
| 7. OFF warning flag | ADI_OFF_FLAG | read only | bar or gauge | 0 to 65535 along the scale | ADI Off Flag |
| 8. AUX warning flag | ADI_AUX_FLAG | read only | bar or gauge | 0 to 65535 along the scale | ADI AUX Flag |
| 9. Lower bank angle scale | — | — | no function in DCS | — | Fixed scale |
| 10. Lower bank angle indicator | ADI_BANK | read only | bar or gauge | 0 to 65535 along the scale | likely; Pointer rides with the sphere |
| 11. Slip indicator (ball) | ADI_BUBBLE | read only | bar or gauge | 0 to 65535 along the scale | ADI Bubble |
| 12. Rate-of-turn indicator | ADI_TURNRATE | read only | bar or gauge | 0 to 65535 along the scale | ADI TurnRate |
| 13. Pitch Trim Knob | ADI_PITCH_TRIM | read + command | knob | continuous, 0 to 65535 | ADI Pitch Trim Knob |

### Electronic Horizontal Situation Indicator (EHSI) (p. 230)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Bearing pointer | — | — | not exported | — | No EHSI pointer output in DCS-BIOS |
| 2. Lubber lines | — | — | no function in DCS | — | Fixed marks |
| 3. Range indicator | EHSI_RANGE | read only | display | text of 4 characters | Range Text; EHSI_RANGE_INVALID is on the Range flag row |
| 4. Course indicator | EHSI_COURSE | read only | display | text of 3 characters | Course Text |
| 5. Magnetic heading compass | — | — | not exported | — | No EHSI compass output in DCS-BIOS |
| 6. Heading marker | — | — | not exported | — | No heading marker output in DCS-BIOS |
| 7. Course pointer | — | — | not exported | — | No course pointer output in DCS-BIOS |
| 8. To-From indicator | — | — | not exported | — | No to-from output in DCS-BIOS |
| 9. Course deviation scale | — | — | no function in DCS | — | Fixed scale |
| 10. Course deviation indicator | — | — | not exported | — | No deviation output in DCS-BIOS |
| 11. New mode indicator | — | — | not exported | — | Temporary text (mode name, ADJ HDG, BRT); the standing mode text is on the Selected instrument mode row |
| 12. Aircraft symbol | — | — | no function in DCS | — | Fixed symbol |
| 13. Heading Set Knob | EHSI_HDG_SET_KNB, EHSI_HDG_SET_BTN | read + command | EHSI_HDG_SET_KNB: step rocker (3200); EHSI_HDG_SET_BTN: button | EHSI_HDG_SET_KNB: step up or down only, no absolute value; EHSI_HDG_SET_BTN: 0 = released, 1 = pressed | Turn is EHSI_HDG_SET_KNB; push is EHSI_HDG_SET_BTN |
| 14. Course Set / Brightness Knob | EHSI_CRS_SET_KNB, EHSI_CRS_SET | read + command | EHSI_CRS_SET_KNB: step rocker (3200); EHSI_CRS_SET: button | EHSI_CRS_SET_KNB: step up or down only, no absolute value; EHSI_CRS_SET: 0 = released, 1 = pressed | Turn is EHSI_CRS_SET_KNB; push is EHSI_CRS_SET |
| 15. Instrument Mode Selector | EHSI_MODE | read + command | button | 0 = released, 1 = pressed | EHSI Mode (M) Button |
| 16. Selected instrument mode | EHSI_MODE_LEFT, EHSI_MODE_RIGHT | read only | display | text of 3 characters | Left text is blank or PLS; right text is NAV or TCN |
| 17. Range flag | EHSI_RANGE_INVALID | read only | none | 0 = off, 1 = on | likely; Range Invalid Strikethrough |
| 18. Warning display area | — | — | not exported | — | No INU / ATT text output in DCS-BIOS |
| 19. CDI flag | — | — | not exported | — | No CDI flag output in DCS-BIOS |

### FUEL QTY SEL Panel (p. 54)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. FUEL QTY SEL Knob | FUEL_QTY_SEL_KNB, FUEL_QTY_SEL_T_KNB | read + command | FUEL_QTY_SEL_KNB: selector (5); FUEL_QTY_SEL_T_KNB: selector (2) NO READBACK | FUEL_QTY_SEL_KNB: 0 = NORM, 1 = RSVR, 2 = INT WING, 3 = EXT WING, 4 = EXT CTR; FUEL_QTY_SEL_T_KNB: guess: 0 = not TEST, 1 = TEST | Five positions are FUEL_QTY_SEL_KNB; TEST is the separate FUEL_QTY_SEL_T_KNB (outputs FUEL_QTY_SEL_T_KNB_INT and FUEL_QTY_SEL_T_KNB_STR, none named like the id) |
| 2. EXT FUEL TRANS Switch | EXT_FUEL_TRANS_SW | read + command | selector (2) | guess: 0 = WING FIRST, 1 = NORM | Category Fuel System; DCS-BIOS description: External Fuel Transfer Switch, NORM/ WING FIRST |

## Left auxiliary console

### Landing Gear Panel (p. 55)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. EMER STORES JETTISON Button | EMERG_STORE_JETT | read + command | button | 0 = released, 1 = pressed | Category MMC in DCS-BIOS |
| 2. HOOK Switch | HOOK_SW | read + command | selector (2) | guess: 0 = DN, 1 = UP | HOOK Switch, UP/DN |
| 3. WHEELS Down Lights | LIGHT_GEAR_N, LIGHT_GEAR_L, LIGHT_GEAR_R | read only | lamp | 0 = off, 1 = lit | Nose, left and right gear lights |
| 4. LG Handle | GEAR_HANDLE, LIGHT_GEAR_WARN | read + command | GEAR_HANDLE: selector (2); LIGHT_GEAR_WARN: lamp | GEAR_HANDLE: guess: 0 = DOWN, 1 = UP; LIGHT_GEAR_WARN: 0 = off, 1 = lit | Handle plus its red warning light; read only: LIGHT_GEAR_WARN |
| 5. GND JETT ENABLE Switch | GND_JETT_ENABLE_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ENABLE | Category MMC in DCS-BIOS; DCS-BIOS description: GND JETT ENABLE Switch, ENABLE/OFF |
| 6. BRAKES Channel Switch | BRAKE_CHAN_SW | read + command | selector (2) | guess: 0 = CHAN 2, 1 = CHAN 1 | BRAKES Channel Switch, CHAN 1/CHAN 2 |
| 7. PARKING BRAKE / ANTI-SKID Switch | ANTI_SKID_SW | read + command | selector (3) | 0 = PARKING BRAKE, 1 = ANTI-SKID, 2 = OFF | Defined as an anti-skid switch (spring-style input: 0 down, 1 stop, 2 up) |
| 8. DN LOCK REL Button | DN_LOCK_BTN | read + command | button | 0 = released, 1 = pressed | DN LOCK REL Button - Push to reset |
| 9. STORES CONFIG Switch | STORES_CONFIG_SW | read + command | selector (2) | guess: 0 = CAT III, 1 = CAT I | STORES CONFIG Switch, CAT III/CAT I |
| 10. HORN SILENCER Button | HORN_SILENCE_BTN | read + command | button | 0 = released, 1 = pressed | HORN SILENCER Button - Push to reset |
| 11. LANDING TAXI LIGHTS Switch | LAND_TAXI_LIGHT_SW | read + command | selector (3) | 0 = LANDING, 1 = OFF, 2 = TAXI | Category External Lights in DCS-BIOS |
| 12. SPEED BRAKE Position Indicator | SPEEDBRAKE_INDICATOR | read only | bar or gauge | 0 to 65535 along the scale | Speed Brake Indicator |

### HMCS Control Panel (p. 57)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| HMCS symbology brightness knob | HMCS_INT_KNB | read + command | knob | continuous, 0 to 65535 | HMCS SYMBOLOGY INT Knob |

### ALT GEAR Handle (p. 57)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| ALT GEAR handle | GEAR_ALT_HANDLE, GEAR_ALT_BTN | read + command | GEAR_ALT_HANDLE: selector (2); GEAR_ALT_BTN: button | GEAR_ALT_HANDLE: guess: 0 = STOW, 1 = PULL; GEAR_ALT_BTN: 0 = released, 1 = pressed | Handle (PULL/STOW) plus its push-to-reset button |

## Right auxiliary console

### Magnetic Compass (p. 58)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Compass card | STANDBY_COMPASS_HEADING, STANDBY_COMPASS_PITCH, STANDBY_COMPASS_ROLL | read only | bar or gauge | 0 to 65535 along the scale | Heading plus tilt as pitch and roll outputs |

### Fuel Quantity Indicator (p. 58)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| AL fuel needle | FUEL_AL | read only | bar or gauge | 0 to 65535 along the scale | Fuel Quantity Indicator AL |
| FR fuel needle | FUEL_FR | read only | bar or gauge | 0 to 65535 along the scale | Fuel Quantity Indicator FR |
| Totalizer window | FUELTOTALIZER_100, FUELTOTALIZER_1K, FUELTOTALIZER_10K | read only | bar or gauge | 0 to 65535 along the scale | Counters for the 100, 1000 and 10000 lb digits |

### Pilot Fault List Display (PFLD) (p. 59)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Fault list window | — | — | not exported | — | No PFLD text output; HUD_DED_DATA_SW (the HUD DED/PFLD switch) belongs to the HUD Control Panel (p. 94), not to the PFLD |

### Caution Light Panel (p. 59)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| FLCS FAULT | LIGHT_FLCS_FAULT | read only | lamp | 0 = off, 1 = lit | FLCS FAULT Light (yellow) |
| ENGINE FAULT | LIGHT_ENGINE_FAULT | read only | lamp | 0 = off, 1 = lit | ENGINE FAULT Light (yellow) |
| AVIONICS FAULT | LIGHT_AVIONICS_FAULT | read only | lamp | 0 = off, 1 = lit | AVIONICS FAULT Light (yellow) |
| SEAT NOT ARMED | LIGHT_SEAT_NOT | read only | lamp | 0 = off, 1 = lit | SEAT NOT ARMED Light (yellow) |
| ELEC SYS | LIGHT_ELEC_SYS | read only | lamp | 0 = off, 1 = lit | ELEC SYS Light (yellow) |
| SEC | LIGHT_SEC | read only | lamp | 0 = off, 1 = lit | SEC Light (yellow) |
| EQUIP HOT | LIGHT_EQUIP_HOT | read only | lamp | 0 = off, 1 = lit | EQUIP HOT Light (yellow) |
| NWS FAIL | LIGHT_NWS_FAIL | read only | lamp | 0 = off, 1 = lit | NWS FAIL Light (yellow) |
| PROBE HEAT | LIGHT_PROBE_HEAT | read only | lamp | 0 = off, 1 = lit | PROBE HEAT Light (yellow) |
| FUEL/OIL HOT | LIGHT_FUEL_OIL_HOT | read only | lamp | 0 = off, 1 = lit | FUEL OIL HOT Light (yellow) |
| RADAR ALT | LIGHT_RADAR_ALT | read only | lamp | 0 = off, 1 = lit | RADAR ALT Light (yellow) |
| ANTI SKID | LIGHT_ANTI_SKID | read only | lamp | 0 = off, 1 = lit | ANTI SKID Light (yellow) |
| CADC | LIGHT_CADC | read only | lamp | 0 = off, 1 = lit | CADC Light (yellow) |
| INLET ICING | LIGHT_INLET_ICING | read only | lamp | 0 = off, 1 = lit | INLET ICING Light (yellow) |
| IFF | LIGHT_IFF | read only | lamp | 0 = off, 1 = lit | IFF Light (yellow) |
| HOOK | LIGHT_HOOK | read only | lamp | 0 = off, 1 = lit | HOOK Light (yellow) |
| STORES CONFIG | LIGHT_STORES_CONFIG | read only | lamp | 0 = off, 1 = lit | STORES CONFIG Light (yellow) |
| OVERHEAT | LIGHT_OVERHEAT | read only | lamp | 0 = off, 1 = lit | OVERHEAT Light (yellow) |
| NUCLEAR | LIGHT_NUCLEAR | read only | lamp | 0 = off, 1 = lit | NUCLEAR Light (yellow) |
| OBOGS | LIGHT_OBOGS | read only | lamp | 0 = off, 1 = lit | OBOGS Light (yellow) |
| ATF NOT ENGAGED | LIGHT_ATF_NOT | read only | lamp | 0 = off, 1 = lit | ATF NOT ENGAGED Light (yellow) |
| EEC | LIGHT_EEC | read only | lamp | 0 = off, 1 = lit | EEC Light (yellow) |
| CABIN PRESS | LIGHT_CABIN_PRESS | read only | lamp | 0 = off, 1 = lit | CABIN PRESS Light (yellow) |
| FWD FUEL LOW | LIGHT_FWD_FUEL_LOW | read only | lamp | 0 = off, 1 = lit | FWD FUEL LOW Light (yellow) |
| BUC | LIGHT_BUC | read only | lamp | 0 = off, 1 = lit | BUC Light (yellow) |
| AFT FUEL LOW | LIGHT_AFT_FUEL_LOW | read only | lamp | 0 = off, 1 = lit | AFT FUEL LOW Light (yellow) |

### Hydraulic Pressure Indicators (p. 61)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| HYD PRESS A gauge | SYSA_PRESSURE | read only | bar or gauge | 0 to 65535 along the scale | System A Pressure |
| HYD PRESS B gauge | SYSB_PRESSURE | read only | bar or gauge | 0 to 65535 along the scale | System B Pressure |

### EPU Fuel Quantity Indicator (p. 61)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| EPU fuel gauge | HYDRAZIN_VOLUME | read only | bar or gauge | 0 to 65535 along the scale | likely; Hydrazin Volume Indicator |

### Cabin Pressure Gauge (p. 61)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Cabin pressure gauge | COCKPIT_ALITITUDE | read only | bar or gauge | 0 to 65535 along the scale | Cabin Pressure Altimeter; the identifier is spelled ALITITUDE |

### Mechanical Clock (p. 61)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. "Day" hand | — | — | not exported | — | No day output in DCS-BIOS |
| 2. "Hour" hand | CLOCK_CURRTIME_H | read only | bar or gauge | 0 to 65535 along the scale | Current Time Hours |
| 3. "Minute" hand | CLOCK_CURRTIME_MS | read only | bar or gauge | 0 to 65535 along the scale | Current Time Minutes |
| 4. Wind / Control Knob | CLOCK_WIND, CLOCK_SET | read + command | CLOCK_WIND: step rocker (3200); CLOCK_SET: button | CLOCK_WIND: step up or down only, no absolute value; CLOCK_SET: 0 = released, 1 = pressed | likely; Turn is CLOCK_WIND; pull is CLOCK_SET (Clock Setting Knob) |

## Left console

### Manual Pitch Override Switch (p. 62)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| MANUAL PITCH override switch | MANUAL_PITCH_SW | read + command | selector (2) | guess: 0 = NORM, 1 = OVRD | Toggle in DCS-BIOS; PANELS says it is held in OVRD; DCS-BIOS description: MANUAL PITCH Override Switch, OVRD/NORM |

### ENG & JET START Control Panel (p. 63)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. JET FUEL RUN light | LIGHT_JFS_RUN | read only | lamp | 0 = off, 1 = lit | JFS RUN Light (green) |
| 2. JET FUEL JFS Switch | JFS_SW | read + command | selector (3) spring | 0 = START 1, 1 = OFF, 2 = START 2 | Spring-loaded; rest is the middle |
| 3. ENG CONT Switch | ENG_CONT_SW, ENG_CONT_SW_COVER | read + command | selector (2) | ENG_CONT_SW: guess: 0 = SEC, 1 = PRI; ENG_CONT_SW_COVER: guess: 0 = CLOSE, 1 = OPEN | Switch plus its cover (PANELS does not list the cover) |
| 4. AB RESET Switch | AB_RESET_SW | read + command | selector (3) spring | 0 = AB RESET, 1 = NORM, 2 = ENG DATA | Spring-loaded; rest is the middle |
| 5. MAX POWER Switch | MAX_PWR_SW | read + command | selector (2) | guess: 0 = OFF, 1 = MAX POWER | PANELS does not state the positions; DCS-BIOS description: MAX POWER Switch, MAX POWER/OFF |

### EPU Control Panel (p. 64)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. EPU Switch | EPU_SW, EPU_SW_COVER_OFF, EPU_SW_COVER_ON | read + command | EPU_SW: selector (3); EPU_SW_COVER_OFF, EPU_SW_COVER_ON: selector (2) | EPU_SW: 0 = ON, 1 = NORM, 2 = OFF; EPU_SW_COVER_OFF, EPU_SW_COVER_ON: guess: 0 = CLOSE, 1 = OPEN | Switch plus its two covers (PANELS does not list the covers) |
| 2. EPU Run Light | LIGHT_EPU | read only | lamp | 0 = off, 1 = lit | EPU Light (green) |
| 3. AIR Light | LIGHT_AIR | read only | lamp | 0 = off, 1 = lit | AIR Light (yellow) |
| 4. HYDRAZN Light | LIGHT_HYDRAZN | read only | lamp | 0 = off, 1 = lit | HYDRAZN Light (yellow) |

### ELEC Control Panel (p. 64)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. MAIN PWR Switch | MAIN_PWR_SW | read + command | selector (3) | 0 = MAIN PWR, 1 = BATT, 2 = OFF | MAIN PWR Switch |
| 2. ELEC CAUTION RESET Button | ELEC_CAUTION | read + command | button | 0 = released, 1 = pressed | ELEC CAUTION RESET Button - Push to reset |
| 3. FLCS PMG Light | LIGHT_FLCS_PMG | read only | lamp | 0 = off, 1 = lit | FLCS PMG Light (yellow) |
| 4. MAIN GEN Light | LIGHT_MAIN_GEN | read only | lamp | 0 = off, 1 = lit | MAIN GEN Light (yellow) |
| 5. STBY GEN Light | LIGHT_STBY_GEN | read only | lamp | 0 = off, 1 = lit | STBY GEN Light (yellow) |
| 6. EPU GEN Light | LIGHT_EPU_GEN | read only | lamp | 0 = off, 1 = lit | EPU GEN Light (yellow) |
| 7. EPU PMG Light | LIGHT_EPU_PMG | read only | lamp | 0 = off, 1 = lit | EPU PMG Light (yellow) |
| 8. ACFT BATT FAIL Light | LIGHT_ACFT_BATT_FAIL | read only | lamp | 0 = off, 1 = lit | ACFT BATT FAIL Light (yellow) |
| 9. ACFT BATT TO FLCS Light | LIGHT_TO_FLCS | read only | lamp | 0 = off, 1 = lit | TO FLCS Light (yellow) |
| 10. ACFT BATT FLCS RLY Light | LIGHT_FLCS_RLY | read only | lamp | 0 = off, 1 = lit | FLCS RLY Light (yellow) |

### AUDIO 1 Control Panel (p. 65)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. COMM 1 Power/Volume Knob | COMM1_PWR_KNB | read + command | knob | continuous, 0 to 65535 | COMM 1 Power Knob |
| 2. COMM 2 Power/Volume Knob | COMM2_PWR_KNB | read + command | knob | continuous, 0 to 65535 | COMM 2 Power Knob |
| 3. COMM 1 Mode Knob | COMM1_MODE_KNB | read + command | selector (3) | guess: 0 = OFF, 1 = SQL, 2 = GD | COMM 1 (UHF) Mode Knob |
| 4. COMM 2 Mode Knob | COMM2_MODE_KNB | read + command | selector (3) | guess: 0 = OFF, 1 = SQL, 2 = GD | COMM 2 (VHF) Mode Knob |
| 5. SECURE VOICE Volume Knob | SEC_VOICE_KNB | read + command | knob | continuous, 0 to 65535 | SECURE VOICE Knob |
| 6. MSL Volume Knob | MSL_KNB | read + command | knob | continuous, 0 to 65535 | MSL Tone Knob |
| 7. TF Volume Knob | TF_KNB | read + command | knob | continuous, 0 to 65535 | TF Tone Knob |
| 8. THREAT Volume Knob | THREAT_KNB | read + command | knob | continuous, 0 to 65535 | THREAT Tone Knob |

### AUDIO 2 Control Panel (p. 65)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 9. INTERCOM Volume Knob | INTERCOM_KNB | read + command | knob | continuous, 0 to 65535 | INTERCOM Knob |
| 10. TACAN Volume Knob | TACAN_KNB | read + command | knob | continuous, 0 to 65535 | TACAN Knob |
| 11. ILS Power/Volume Knob | ILS_PWR_KNB | read + command | knob | continuous, 0 to 65535 | ILS Power Knob |
| 12. HOT MIC CIPHER Switch (Microphone Switch) | HOT_MIC_SW | read + command | selector (3) | 0 = HOT MIC, 1 = OFF, 2 = CIPHER | HOT MIC CIPHER Switch |

### AVTR Control Panel (p. 66)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| AVTR panel controls | — | — | not exported | — | PANELS names no individual controls; DCS-BIOS has no AVTR category |

### FUEL Control Panel (p. 67)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. FUEL MASTER Switch | FUEL_MASTER_SW, FUEL_MASTER_CV | read + command | selector (2) | FUEL_MASTER_SW: guess: 0 = OFF, 1 = MASTER; FUEL_MASTER_CV: guess: 0 = CLOSE, 1 = OPEN | Switch plus its cover |
| 2. TANK INERTING Switch | TANK_INTERTING_SW | read + command | selector (2) | guess: 0 = OFF, 1 = TANK INERTING | The identifier is spelled INTERTING; DCS-BIOS description: TANK INERTING Switch, TANK INERTING /OFF |
| 3. ENG FEED Knob | ENGINE_FEED_KNB | read + command | selector (4) | 0 = OFF, 1 = NORM, 2 = AFT, 3 = FWD | Category External Lights in DCS-BIOS |
| 4. AIR REFUEL Switch | AIR_REFUEL_SW | read + command | selector (2) | guess: 0 = CLOSE, 1 = OPEN | AIR REFUEL Switch, OPEN/CLOSE |

### IFF Control Panel (p. 67)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. MASTER Knob | IFF_MASTER_KNB | read + command | selector (5) | 0 = OFF, 1 = STBY, 2 = LOW, 3 = NORM, 4 = EMER | IFF MASTER Knob |
| 2. M-4 CODE Switch | IFF_M4_CODE_SW | read + command | selector (3) | 0 = HOLD, 1 = A/B, 2 = ZERO | Spring-loaded in PANELS (rest A/B); a plain 3-position switch in DCS-BIOS; reverse order of PANELS |
| 3. C & I Knob | IFF_C_I_KNB | read + command | selector (2) | guess: 0 = UFC, 1 = BACK UP | IFF C & I Knob, UFC/BACKUP |
| 4. ENABLE Switch | IFF_ENABLE_SW | read + command | selector (3) | 0 = M1/M3, 1 = OFF, 2 = M3/MS | IFF ENABLE Switch; reverse order of PANELS |
| 5. MODE 1 & MODE 3 Thumbwheel Selectors | IFF_M1_SEL_1, IFF_M1_SEL_2, IFF_M3_SEL_1, IFF_M3_SEL_2, IFF_CODE_DRUM_DIGIT_1, IFF_CODE_DRUM_DIGIT_2, IFF_CODE_DRUM_DIGIT_3, IFF_CODE_DRUM_DIGIT_4 | read + command | IFF_M1_SEL_1, IFF_M1_SEL_2, IFF_M3_SEL_1, IFF_M3_SEL_2: selector (3) spring; IFF_CODE_DRUM_DIGIT_1, IFF_CODE_DRUM_DIGIT_2, IFF_CODE_DRUM_DIGIT_3, IFF_CODE_DRUM_DIGIT_4: bar or gauge | IFF_M1_SEL_1, IFF_M1_SEL_2, IFF_M3_SEL_1, IFF_M3_SEL_2: guess: 0 = DN, 1 = CENTER, 2 = UP; IFF_CODE_DRUM_DIGIT_1, IFF_CODE_DRUM_DIGIT_2, IFF_CODE_DRUM_DIGIT_3, IFF_CODE_DRUM_DIGIT_4: 0 to 65535 along the scale | Four spring-loaded selector levers (one per digit pair: Mode 1 digits 1 and 2, Mode 3 digits 1 and 2) plus four digit drums (IFF Code Digit 1 to 4) as output; read only: IFF_CODE_DRUM_DIGIT_1, IFF_CODE_DRUM_DIGIT_2, IFF_CODE_DRUM_DIGIT_3, IFF_CODE_DRUM_DIGIT_4 |
| 6. MODE 4 REPLY Switch | IFF_M4_REPLY_SW | read + command | selector (3) | 0 = OUT, 1 = A, 2 = B | IFF MODE 4 REPLY Switch |
| 7. MODE 4 MONITOR Switch | IFF_M4_MONITOR_SW | read + command | selector (2) | guess: 0 = OUT, 1 = AUDIO | IFF MODE 4 MONITOR Switch, OUT/AUDIO |

### EXT LIGHTING Control Panel (p. 69)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. POSITION FLASH / STEADY Switch | POS_FLASH_LIGHT_SW | read + command | selector (2) | guess: 0 = STEADY, 1 = FLASH | FLASH STEADY Light Switch, FLASH/STEADY |
| 2. POSITION WING / TAIL Switch | POS_WING_TAIL_LIGHT_SW | read + command | selector (3) | 0 = BRT, 1 = OFF, 2 = DIM | WING/TAIL Light Switch |
| 3. FUSELAGE Switch | POS_FUSELAGE_LIGHT_SW | read + command | selector (3) | 0 = BRT, 1 = OFF, 2 = DIM | FUSELAGE Light Switch |
| 4. ANTI-COLL Knob | ANTI_COLL_LIGHT_KNB | read + command | selector (8) | 0 = OFF, 1 = 1, 2 = 2, 3 = 3, 4 = 4, 5 = A, 6 = B, 7 = C | ANTI-COLL Knob |
| 5. FORM Knob | FORM_LIGHT_KNB | read + command | knob | continuous, 0 to 65535 | FORM Light Knob |
| 6. AERIAL REFUELING Knob | AIR_REFUEL_LIGHT_KNB | read + command | knob | continuous, 0 to 65535 | AERIAL REFUELING Light Knob |
| 7. MASTER Knob | MASTER_LIGHT_SW | read + command | selector (5) | 0 = OFF, 1 = ALL, 2 = A-C, 3 = FORM, 4 = NORM | PANELS names the positions OFF, COVERT ALL, COVERT A-C, COVERT FORM, NORM |

### FLT CONTROL Panel (p. 71)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. DIGITAL BACKUP Switch | DIGI_BAK_SW | read + command | selector (2) | guess: 0 = OFF, 1 = BACKUP | DIGITAL BACKUP Switch, OFF/BACKUP |
| 2. MANUAL TF FLY-UP Switch | MAN_TF_FLYUP_SW | read + command | selector (2) | guess: 0 = ENABLE, 1 = DISABLE | MANUAL TF FLYUP Switch, ENABLE/DISABLE |
| 3. ALT FLAPS Switch | ALT_FLAPS_SW | read + command | selector (2) | guess: 0 = NORM, 1 = EXTEND | ALT FLAPS Switch, NORM/EXTEND |
| 4. FLCS RUN / FAIL Indicator Lights | LIGHT_FL_RUN, LIGHT_FL_FAIL | read only | lamp | 0 = off, 1 = lit | RUN (green) and FAIL (red) lights |
| 5. LE FLAPS Switch | LE_FLAPS_SW | read + command | selector (2) | guess: 0 = AUTO, 1 = LOCK | LE FLAPS Switch, AUTO/LOCK |
| 6. FLCS RESET Switch | FLCS_RESET_SW | read + command | selector (2) | guess: 0 = OFF, 1 = RESET | FLCS RESET Switch, OFF/RESET |
| 7. FLCS BIT Switch | BIT_SW | read + command | selector (2) | guess: 0 = OFF, 1 = BIT | Toggle in DCS-BIOS; PANELS says it springs back to OFF; DCS-BIOS description: BIT Switch, OFF/BIT |

### MANUAL TRIM Panel (p. 72)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. ROLL TRIM Wheel & Indicator | ROLL_TRIM, ROLLTRIMIND | read + command | ROLL_TRIM: knob; ROLLTRIMIND: bar or gauge | ROLL_TRIM: continuous, 0 to 65535; ROLLTRIMIND: 0 to 65535 along the scale | Wheel plus Roll Trim Indicator as output; read only: ROLLTRIMIND |
| 2. YAW TRIM Knob | YAW_TRIM | read + command | knob | continuous, 0 to 65535 | YAW TRIM Knob |
| 3. PITCH TRIM Wheel & Indicator | PITCH_TRIM, PITCHTRIMIND | read + command | PITCH_TRIM: knob; PITCHTRIMIND: bar or gauge | PITCH_TRIM: continuous, 0 to 65535; PITCHTRIMIND: 0 to 65535 along the scale | Wheel plus Pitch Trim Indicator as output; read only: PITCHTRIMIND |
| 4. TRIM/AP DISC Switch | TRIM_AP_DISC_SW | read + command | selector (2) | guess: 0 = DISC, 1 = NORM | TRIM/AP DISC Switch, DISC/NORM |

### TEST Panel (p. 72)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. FIRE & OHEAT DETECT Test Button | FIRE_OHEAT_DETECT_BTN | read + command | button | 0 = released, 1 = pressed | Category Engine in DCS-BIOS |
| 2. OBOGS BIT Switch | OBOGS_SW | read + command | selector (2) | guess: 0 = OFF, 1 = BIT | Toggle in DCS-BIOS; PANELS says momentary; DCS-BIOS description: OBOGS BIT Switch, BIT/OFF |
| 3. MAL & IND LTS Test Button | MAL_IND_LTS_TEST | read + command | button | 0 = released, 1 = pressed | Category Interior Lights in DCS-BIOS |
| 4. PROBE HEAT Switch | PROBE_HEAT_SW | read + command | selector (3) spring | 0 = PROBE HEAT, 1 = OFF, 2 = TEST | Spring-loaded; PANELS lists it as a plain toggle |
| 5. EPU/GEN Switch | EPU_GEN_TEST_SW | read + command | selector (2) | guess: 0 = OFF, 1 = EPU/GEN | Toggle in DCS-BIOS; PANELS says TEST is momentary; category Electric System; DCS-BIOS description: EPU/GEN Test Switch, EPU/GEN /OFF |
| 6. FLCS PWR Lights | LIGHT_FLCS_PWR_A, LIGHT_FLCS_PWR_B, LIGHT_FLCS_PWR_C, LIGHT_FLCS_PWR_D | read only | lamp | 0 = off, 1 = lit | Lights A, B, C and D |
| 7. FLCS PWR TEST Switch | FLCS_PWR_TEST_SW | read + command | selector (3) spring | 0 = MAINT, 1 = NORM, 2 = TEST | Spring-loaded; PANELS lists it as a plain toggle; category Electric System; reverse order of PANELS |

### Canopy Switch and Canopy Handle (p. 73)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Canopy Switch | CANOPY_SW | read + command | selector (3) spring | 0 = OPEN, 1 = HOLD, 2 = CLOSE | Spring-loaded; PANELS: up, centre, down |
| 2. Canopy Lever | CANOPY_HANDLE, CANOPY_LOCK | read + command | CANOPY_HANDLE: selector (2); CANOPY_LOCK: bar or gauge | CANOPY_HANDLE: guess: 0 = LOCKED, 1 = UNLOCKED; CANOPY_LOCK: 0 to 65535 along the scale | likely; Handle plus Canopy Lock Position as output; read only: CANOPY_LOCK |

### Canopy Jettison T-Handle (p. 74)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| CANOPY JETTISON T-handle | CANOPY_JETT_THANDLE | read + command | selector (2) | guess: 0 = STOW, 1 = PULL | CANOPY JETTISON T-Handle, PULL/STOW |

### DEFOG Lever (p. 74)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| DEFOG lever | DEFOG_LEVER | read + command | selector (21) | guess: 0 = MIN, 1 to 19 = in between, 20 = MAX | Category ECS in DCS-BIOS; 21 steps |

### Manual Canopy Control Handcrank (p. 62)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Manual canopy handcrank | — | — | not exported | — | PANELS: only named in the figure |

### ANTI-G TEST Button (p. 62)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| ANTI-G TEST button | — | — | not exported | — | PANELS: only named in the figure |

### UHF Backup Control Panel (p. 260)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Preset Channel Card & Access Door | UHF_DOOR | read + command | selector (2) | guess: 0 = CLOSE, 1 = OPEN | UHF Access Door, OPEN/CLOSE |
| 2. TEST DISPLAY Button | UHF_TEST_BTN | read + command | button | 0 = released, 1 = pressed | UHF TEST DISPLAY Button |
| 3. CHAN Display | UHF_CHAN_DISP | read only | display | text of 2 characters | UHF CHAN Display |
| 4. CHAN Knob | UHF_CHAN_KNB | read + command | selector (20) | guess: 0 = preset 1, 1 = preset 2, ... 19 = preset 20 | Twenty presets |
| 5. Frequency Status/Display | UHF_FREQ_DISP | read only | display | text of 7 characters | UHF Manual Frequency Display |
| 6. STATUS Button | UHF_STATUS_BTN | read + command | button | 0 = released, 1 = pressed | UHF STATUS Button |
| 7. A-3-2 Knob | UHF_FREQ_100_KNB | read + command | selector (3) | guess: 0 = A, 1 = 3, 2 = 2 | likely; UHF Manual Frequency Knob 100 MHz; the A-10C ARC-164 has 0 = 2, 1 = 3, 2 = A |
| 8. Manual Frequency Knobs | UHF_FREQ_10_KNB, UHF_FREQ_1_KNB, UHF_FREQ_01_KNB, UHF_FREQ_0025_KNB | read + command | UHF_FREQ_10_KNB, UHF_FREQ_1_KNB, UHF_FREQ_01_KNB: selector (10); UHF_FREQ_0025_KNB: selector (4) | UHF_FREQ_10_KNB, UHF_FREQ_1_KNB, UHF_FREQ_01_KNB: guess: 0 to 9 = digit 0 to 9; UHF_FREQ_0025_KNB: guess: 0 = 00, 1 = 25, 2 = 50, 3 = 75 | likely; Four knobs for 10 MHz, 1 MHz, 0.1 MHz and 0.025 MHz, left to right order assumed; the A-10C ARC-164 has states 00, 25, 50, 75 |
| 9. Function Knob | UHF_FUNC_KNB | read + command | selector (4) | guess: 0 = OFF, 1 = MAIN, 2 = BOTH, 3 = ADF | UHF Function Knob |
| 10. Mode Knob | UHF_MODE_KNB | read + command | selector (3) | guess: 0 = MNL, 1 = PRESET, 2 = GRD | UHF Mode Knob |
| 11. TONE Button | UHF_TONE_BTN | read + command | button | 0 = released, 1 = pressed | UHF Tone Button |
| 12. VOL Knob | UHF_VOL_KNB | read + command | knob | continuous, 0 to 65535 | UHF VOL Knob |
| 13. SQUELCH Switch | UHF_SQUELCH_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | UHF SQUELCH Switch |

## Right console

### SNSR PWR Control Panel (p. 75)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. LEFT HDPT Switch | HDPT_SW_L | read + command | selector (2) | guess: 0 = OFF, 1 = ON | LEFT HDPT Switch, ON/OFF |
| 2. RIGHT HDPT Switch | HDPT_SW_R | read + command | selector (2) | guess: 0 = OFF, 1 = ON | RIGHT HDPT Switch, ON/OFF |
| 3. FCR Switch | FCR_PWR_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | FCR Switch, FCR/OFF |
| 4. RDR ALT Switch | RDR_ALT_PWR_SW | read + command | selector (3) | 0 = RDR ALT, 1 = STBY, 2 = OFF | RDR ALT Switch |

### Interior LIGHTING Control Panel (p. 76)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. PRIMARY CONSOLES Knob | PRI_CONSOLES_BRT_KNB | read + command | knob | continuous, 0 to 65535 | PRIMARY CONSOLES BRT Knob |
| 2. PRIMARY INST PNL Knob | PRI_INST_PNL_BRT_KNB | read + command | knob | continuous, 0 to 65535 | PRIMARY INST PNL BRT Knob |
| 3. PRIMARY DATA ENTRY DISPLAY Knob | PRI_DATA_DISPLAY_BRT_KNB | read + command | knob | continuous, 0 to 65535 | PRIMARY DATA ENTRY DISPLAY BRT Knob |
| 4. FLOOD CONSOLES Knob | FLOOD_CONSOLES_BRT_KNB | read + command | knob | continuous, 0 to 65535 | FLOOD CONSOLES BRT Knob |
| 5. FLOOD INST PNL Knob | FLOOD_INST_PNL_BRT_KNB | read + command | knob | continuous, 0 to 65535 | FLOOD INST PNL BRT Knob |
| 6. MAL & IND LTS Switch | MAL_IND_LTS_BRT_SW | read + command | selector (3) spring | 0 = BRT, 1 = Center, 2 = DIM | Spring-loaded with a centre rest in DCS-BIOS; category External Lights; PANELS lists only BRT and DIM |

### AIR COND Control Panel (p. 76)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. TEMP Knob | TEMP_KNB | read + command | knob | continuous, 0 to 65535 | Continuous in DCS-BIOS; PANELS lists labelled positions |
| 2. AIR SOURCE Knob | AIR_SOURCE_KNOB | read + command | selector (4) | 0 = OFF, 1 = NORM, 2 = DUMP, 3 = RAM | Category ECS; the older AIR_SOURCE_KNB is deprecated (see the DCS-BIOS-only part) |

### KY-58 Secure Voice Panel (p. 77)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| KY-58 panel controls | KY58_PWR_KNB, KY58_MODE_KNB, KY58_FILL_KNB, KY58_VOL_KNB | read + command | KY58_PWR_KNB: selector (3); KY58_MODE_KNB: selector (4); KY58_FILL_KNB: selector (8); KY58_VOL_KNB: knob | KY58_PWR_KNB: 0 = OFF, 1 = ON, 2 = TD; KY58_MODE_KNB: 0 = P, 1 = C, 2 = LD, 3 = RV; KY58_FILL_KNB: 0 = Z 1-5, 1 = 1, 2 = 2, 3 = 3, 4 = 4, 5 = 5, 6 = 6, 7 = Z ALL; KY58_VOL_KNB: continuous, 0 to 65535 | PANELS names no individual controls; DCS-BIOS has power, mode, fill and volume knobs |

### PLAIN/CIPHER Switch (p. 77)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| PLAIN/CIPHER switch | PLAIN_CIPHER_SW | read + command | selector (3) | 0 = CRAD 1, 1 = PLAIN, 2 = CRAD 2 | PANELS: PLAIN, CIPHER, labels CRAD 1 and CRAD 2 in the figure |

### OXYGEN Regulator Panel (p. 77)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. OXYGEN REGULATOR FLOW Indicator | FLOW_INDICATOR_LIGHT, FLOW_INDICATOR | read only | FLOW_INDICATOR_LIGHT: lamp; FLOW_INDICATOR: bar or gauge | FLOW_INDICATOR_LIGHT: 0 = off, 1 = lit; FLOW_INDICATOR: 0 to 65535 along the scale | Flow Indicator Light (on/off) and Flow Indicator Gauge (as a value) |
| 2. OXYGEN SUPPLY Indicator | OXYGEN_PRESSURE | read only | bar or gauge | 0 to 65535 along the scale | Oxygen Pressure |
| 3. EMERGENCY Lever | OXY_EMERG_LVR | read + command | selector (3) spring | 0 = EMERGENCY, 1 = NORMAL, 2 = TEST MASK | Spring-loaded; rest is NORMAL |
| 4. Diluter Lever | OXY_DILUTER_LVR | read + command | selector (2) | guess: 0 = NORM, 1 = 100% | Diluter Lever, 100 percent/NORM |
| 5. SUPPLY Lever | OXY_SUPPLY_LVR | read + command | selector (3) | 0 = PBG, 1 = ON, 2 = OFF | Supply Lever |

### ENGINE ANTI-ICE Switch (p. 78)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. ANTI-ICE ENGINE Switch | ENG_ANTI_ICE | read + command | selector (3) | 0 = ON, 1 = AUTO, 2 = OFF | Category Engine in DCS-BIOS |

### ANT SEL Panel (p. 78)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 2. ANT SEL IFF Switch | IFF_ANT_SEL_SW | read + command | selector (3) | 0 = LOWER, 1 = NORM, 2 = UPPER | Category Audio Panel in DCS-BIOS; reverse order of PANELS |
| 3. ANT SEL UHF Switch | UHF_ANT_SEL_SW | read + command | selector (3) | 0 = LOWER, 1 = NORM, 2 = UPPER | Category Audio Panel in DCS-BIOS; reverse order of PANELS |

### AVIONICS POWER Control Panel (p. 78)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. MMC Switch | MMC_PWR_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | MMC Switch, MMC/OFF |
| 2. ST STA Switch | ST_STA_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | ST STA Switch, ST STA/OFF |
| 3. MFD Switch | MFD_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | MFD Switch, MFD/OFF |
| 4. UFC Switch | UFC_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | UFC Switch, UFC/OFF |
| 5. MAP Switch | MAP_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | MAP Switch, MAP/OFF |
| 6. GPS Switch | GPS_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | GPS Switch, GPS/OFF |
| 7. DL Switch | DL_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | DL Switch, DL/OFF |
| 8. INS Knob | INS_KNB | read + command | selector (7) | 0 = OFF, 1 = STOR HDG, 2 = NORM, 3 = NAV, 4 = CAL, 5 = INFLT ALIGN, 6 = ATT | PANELS names the third position ALIGN NORM |
| 9. MIDS LVT Knob | MIDS_LVT_KNB | read + command | selector (3) | 0 = ZERO, 1 = OFF, 2 = ON | MIDS LVT Knob |

### VOICE MESSAGE Switch (p. 80)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| VOICE MESSAGE switch | VMS_INHIBIT_SW | read + command | selector (2) | guess: 0 = VOICE MESSAGE, 1 = INHIBIT | Voice Message Inhibit Switch, VOICE MESSAGE/INHIBIT. Inconsistent with the toggle rule above: here the first name of the DCS-BIOS description is taken as 0, while most other toggles (for example HOOK_SW, AIR_REFUEL_SW) take the first name as the higher value. Check both ways in DCS |

### ZEROIZE Switch (p. 80)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| ZEROIZE switch | ZEROIZE_SW, ZEROIZE_SW_COVER | read + command | ZEROIZE_SW: selector (3); ZEROIZE_SW_COVER: selector (2) | ZEROIZE_SW: 0 = OFP, 1 = OFF, 2 = DATA; ZEROIZE_SW_COVER: guess: 0 = CLOSE, 1 = OPEN | Switch plus its cover; category KY-58 |

### SEAT ADJ Switch (p. 80)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| SEAT ADJ switch | SEAT_ADJ, SEAT_HEIGHT | read + command | SEAT_ADJ: selector (3) spring; SEAT_HEIGHT: bar or gauge | SEAT_ADJ: 0 = UP, 1 = OFF, 2 = DOWN; SEAT_HEIGHT: 0 to 65535 along the scale | Spring-loaded switch; SEAT_HEIGHT (Seat Height as output) likely belongs here; read only: SEAT_HEIGHT |

### NUCLEAR CONSENT Switch (p. 80)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| NUCLEAR CONSENT switch | — | — | no function in DCS | — | PANELS: not implemented; only the NUCLEAR caution lamp exists |

### Other right console fittings (pp. 75, 127)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Utility Light | — | — | not exported | — |  |
| Arm Rest | — | — | not exported | — |  |
| DTU Receptacle | — | — | not exported | — |  |

## Ejection seat

### Ejection Seat Controls (pp. 81, 82)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Ejection Handle | SEAT_EJECT_HANDLE | read + command | selector (2) | guess: 0 = STOW, 1 = PULL | Ejection Handle, PULL/STOW |
| Ejection Seat Arming Lever | SEAT_EJECT_SAFE | read + command | selector (2) | guess: 0 = ARMED, 1 = LOCKED | The SEAT NOT ARMED caution lamp is LIGHT_SEAT_NOT; DCS-BIOS description: Ejection Safety Lever, ARMED/LOCKED |
| Emergency Manual Chute Lever | — | — | not exported | — | PANELS: function not stated |

## Display-related controls

### Head-Up Display (HUD) (p. 90)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Combining glass | — | — | export | — | Symbology picture; no HUD output in DCS-BIOS |

### HUD Control Panel (p. 94)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Scales Switch | HUD_SCALES_SW | read + command | selector (3) | 0 = VV/VAH, 1 = VAH, 2 = OFF | HUD Scales Switch |
| 2. Flightpath Marker Switch | HUD_FP_MARKER_SW | read + command | selector (3) | 0 = ATT/FPM, 1 = FPM, 2 = OFF | HUD Flightpath Marker Switch |
| 3. DED/PFLD Switch | HUD_DED_DATA_SW | read + command | selector (3) | 0 = DED, 1 = PFL, 2 = OFF | HUD DED/PFLD Data Switch; the only row for this id (the PFLD section has none) |
| 4. Depressible Reticle Switch | HUD_DEPRESS_RET_SW | read + command | selector (3) | 0 = STBY, 1 = PRI, 2 = OFF | HUD Depressible Reticle Switch |
| 5. Velocity Switch | HUD_SPEED_SW | read + command | selector (3) | 0 = CAS, 1 = TAS, 2 = GND SPD | HUD Velocity Switch |
| 6. Altitude Switch | HUD_ALT_SW | read + command | selector (3) | 0 = RADAR, 1 = BARO, 2 = AUTO | HUD Altitude Switch |
| 7. Brightness Control Switch | HUD_BRT_SW | read + command | selector (3) | 0 = DAY, 1 = AUTO BRT, 2 = NIGHT | HUD Brightness Control Switch |
| 8. Test Switch | HUD_TEST_SW | read + command | selector (3) | 0 = STEP, 1 = ON, 2 = OFF | HUD TEST Switch |

### Integrated Control Panel (ICP) (p. 99)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Override button COM 1 | ICP_COM1_BTN | read + command | button | 0 = released, 1 = pressed | ICP COM Override Button, COM1(UHF) |
| 1. Override button COM 2 | ICP_COM2_BTN | read + command | button | 0 = released, 1 = pressed | ICP COM Override Button, COM2(VHF) |
| 1. Override button IFF | ICP_IFF_BTN | read + command | button | 0 = released, 1 = pressed | ICP IFF Override Button, IFF |
| 1. Override button LIST | ICP_LIST_BTN | read + command | button | 0 = released, 1 = pressed | ICP LIST Override Button, LIST |
| 2. Master mode button A-A | ICP_AA_MODE_BTN | read + command | button | 0 = released, 1 = pressed | ICP Master Mode Button, A-A |
| 2. Master mode button A-G | ICP_AG_MODE_BTN | read + command | button | 0 = released, 1 = pressed | ICP Master Mode Button, A-G |
| 3. SYM Knob | ICP_HUD_BRT_KNB | read + command | knob | continuous, 0 to 65535 | ICP HUD Symbology Intensity Knob |
| 4. RET DEPR Knob | ICP_RETICLE_DEPRESS_KNB | read + command | knob | continuous, 0 to 65535 | ICP Reticle Depression Control Knob |
| 5. Keypad key 1 | ICP_BTN_1 | read + command | button | 0 = released, 1 = pressed | ICP Priority Function Button, 1(T-ILS) |
| 5. Keypad key 2 | ICP_BTN_2 | read + command | button | 0 = released, 1 = pressed | ICP Priority Function Button, 2/N(ALOW) |
| 5. Keypad key 3 | ICP_BTN_3 | read + command | button | 0 = released, 1 = pressed | ICP Priority Function Button, 3 |
| 5. Keypad key 4 | ICP_BTN_4 | read + command | button | 0 = released, 1 = pressed | ICP Priority Function Button, 4/W(STPT) |
| 5. Keypad key 5 | ICP_BTN_5 | read + command | button | 0 = released, 1 = pressed | ICP Priority Function Button, 5(CRUS) |
| 5. Keypad key 6 | ICP_BTN_6 | read + command | button | 0 = released, 1 = pressed | ICP Priority Function Button, 6/E(TIME) |
| 5. Keypad key 7 | ICP_BTN_7 | read + command | button | 0 = released, 1 = pressed | ICP Priority Function Button, 7(MARK) |
| 5. Keypad key 8 | ICP_BTN_8 | read + command | button | 0 = released, 1 = pressed | ICP Priority Function Button, 8/S(FIX) |
| 5. Keypad key 9 | ICP_BTN_9 | read + command | button | 0 = released, 1 = pressed | ICP Priority Function Button, 9(A-CAL) |
| 6. RCL Button | ICP_RCL_BTN | read + command | button | 0 = released, 1 = pressed | ICP Recall Button, RCL |
| 7. ENTR Button | ICP_ENTR_BTN | read + command | button | 0 = released, 1 = pressed | ICP Enter Button, ENTR |
| 8. BRT Knob | ICP_RASTER_BRT_KNB | read + command | knob | continuous, 0 to 65535 | ICP Raster Intensity Knob |
| 9. CONT Knob | ICP_RASTER_CONTR_KNB | read + command | knob | continuous, 0 to 65535 | ICP Raster Contrast Knob |
| 10. 0/M-SEL Button | ICP_BTN_0 | read + command | button | 0 = released, 1 = pressed | ICP Priority Function Button, 0(M-SEL) |
| 11. DED Increment/Decrement Rocker | ICP_DED_SW | read + command | selector (3) spring | guess: 0 = DN, 1 = CENTER, 2 = UP | ICP DED Increment/Decrement Switch |
| 12. Data Control Switch (DCS) | ICP_DATA_RTN_SEQ_SW, ICP_DATA_UP_DN_SW | read + command | selector (3) spring | ICP_DATA_RTN_SEQ_SW: guess: 0 = RTN, 1 = CENTER, 2 = SEQ; ICP_DATA_UP_DN_SW: guess: 0 = DN, 1 = CENTER, 2 = UP | Left-right axis is ICP_DATA_RTN_SEQ_SW; up-down axis is ICP_DATA_UP_DN_SW |
| 13. DRIFT C/O & WARN RESET Switch | ICP_DRIFT_SW | read + command | selector (3) spring | 0 = DRIFT C/O, 1 = NORM, 2 = WARN RESET | Spring-loaded; PANELS: spring from WARN RESET only |
| 14. TFR WX Button | ICP_WX_BTN | read + command | button | 0 = released, 1 = pressed | likely; DCS-BIOS calls it FLIR Polarity Button, Wx |
| 14. FLIR Increment/Decrement Rocker | ICP_FLIR_SW | read + command | selector (3) spring | guess: 0 = DN, 1 = CENTER, 2 = UP | ICP FLIR Increment/Decrement Switch |
| 14. FLIR GAIN/LVL/AUTO Switch | ICP_FLIR_GAIN_SW | read + command | selector (3) | 0 = GAIN, 1 = LVL, 2 = AUTO | ICP FLIR GAIN/LEVEL Switch |

### Data Entry Display (DED) (p. 101)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| DED window | DED_L1, DED_L2, DED_L3, DED_L4, DED_L5, DED_L1_FORMAT, DED_L2_FORMAT, DED_L3_FORMAT, DED_L4_FORMAT, DED_L5_FORMAT | read only | display | text of 24 characters | Five text lines of 24 characters plus a format string per line (i = inverse, b = big); the older DED_LINE_1 to DED_LINE_5 are in the DCS-BIOS-only part |

### Multi-Function Display (MFD) bezel (p. 122)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Screen | — | — | export | — | Two MFDs; no screen output in DCS-BIOS |
| 1. OSB 1 to 5 | MFD_L_1, MFD_L_2, MFD_L_3, MFD_L_4, MFD_L_5, MFD_R_1, MFD_R_2, MFD_R_3, MFD_R_4, MFD_R_5 | read + command | button | 0 = released, 1 = pressed | Left MFD (MFD_L_) and right MFD (MFD_R_) push buttons named by OSB number |
| 1. OSB 6 to 10 | MFD_L_6, MFD_L_7, MFD_L_8, MFD_L_9, MFD_L_10, MFD_R_6, MFD_R_7, MFD_R_8, MFD_R_9, MFD_R_10 | read + command | button | 0 = released, 1 = pressed | Left MFD (MFD_L_) and right MFD (MFD_R_) push buttons named by OSB number |
| 1. OSB 11 to 15 | MFD_L_11, MFD_L_12, MFD_L_13, MFD_L_14, MFD_L_15, MFD_R_11, MFD_R_12, MFD_R_13, MFD_R_14, MFD_R_15 | read + command | button | 0 = released, 1 = pressed | Left MFD (MFD_L_) and right MFD (MFD_R_) push buttons named by OSB number |
| 1. OSB 16 to 20 | MFD_L_16, MFD_L_17, MFD_L_18, MFD_L_19, MFD_L_20, MFD_R_16, MFD_R_17, MFD_R_18, MFD_R_19, MFD_R_20 | read + command | button | 0 = released, 1 = pressed | Left MFD (MFD_L_) and right MFD (MFD_R_) push buttons named by OSB number |
| 2. GAIN Rocker | MFD_L_GAIN_SW, MFD_R_GAIN_SW | read + command | selector (3) spring | guess: 0 = DN, 1 = CENTER, 2 = UP | Left and right MFD |
| 3. SYM Rocker | MFD_L_SYM_SW, MFD_R_SYM_SW | read + command | selector (3) spring | guess: 0 = DN, 1 = CENTER, 2 = UP | Left and right MFD |
| 4. BRT Rocker | MFD_L_BRT_SW, MFD_R_BRT_SW | read + command | selector (3) spring | guess: 0 = DN, 1 = CENTER, 2 = UP | Left and right MFD |
| 5. CON Rocker | MFD_L_CON_SW, MFD_R_CON_SW | read + command | selector (3) spring | guess: 0 = DN, 1 = CENTER, 2 = UP | Left and right MFD |

### MFD Format Selection Master Menu (p. 124)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. BLANK Format | MFD_L_1, MFD_R_1 | read + command | button | 0 = released, 1 = pressed | OSB 1 of either MFD, same ids as the MFD bezel OSB row |
| 2. HAD Format | MFD_L_2, MFD_R_2 | read + command | button | 0 = released, 1 = pressed | OSB 2 of either MFD, same ids as the MFD bezel OSB row |
| 3. RCCE Format | MFD_L_4, MFD_R_4 | read + command | button | 0 = released, 1 = pressed | OSB 4 of either MFD, same ids as the MFD bezel OSB row |
| 4. RESET MENU Page | MFD_L_5, MFD_R_5 | read + command | button | 0 = released, 1 = pressed | OSB 5 of either MFD, same ids as the MFD bezel OSB row |
| 5. FCR Format | MFD_L_20, MFD_R_20 | read + command | button | 0 = released, 1 = pressed | OSB 20 of either MFD, same ids as the MFD bezel OSB row |
| 6. TGP Format | MFD_L_19, MFD_R_19 | read + command | button | 0 = released, 1 = pressed | OSB 19 of either MFD, same ids as the MFD bezel OSB row |
| 7. WPN Format | MFD_L_18, MFD_R_18 | read + command | button | 0 = released, 1 = pressed | OSB 18 of either MFD, same ids as the MFD bezel OSB row |
| 8. TFR Format | MFD_L_17, MFD_R_17 | read + command | button | 0 = released, 1 = pressed | OSB 17 of either MFD, same ids as the MFD bezel OSB row |
| 9. FLIR Format | MFD_L_16, MFD_R_16 | read + command | button | 0 = released, 1 = pressed | OSB 16 of either MFD, same ids as the MFD bezel OSB row |
| 10. SMS Format | MFD_L_6, MFD_R_6 | read + command | button | 0 = released, 1 = pressed | OSB 6 of either MFD, same ids as the MFD bezel OSB row |
| 11. HSD Format | MFD_L_7, MFD_R_7 | read + command | button | 0 = released, 1 = pressed | OSB 7 of either MFD, same ids as the MFD bezel OSB row |
| 12. DTE Format | MFD_L_8, MFD_R_8 | read + command | button | 0 = released, 1 = pressed | OSB 8 of either MFD, same ids as the MFD bezel OSB row |
| 13. TEST Format | MFD_L_9, MFD_R_9 | read + command | button | 0 = released, 1 = pressed | OSB 9 of either MFD, same ids as the MFD bezel OSB row |
| 14. FLCS Format | MFD_L_10, MFD_R_10 | read + command | button | 0 = released, 1 = pressed | OSB 10 of either MFD, same ids as the MFD bezel OSB row |
| 15. Swap Button | MFD_L_15, MFD_R_15 | read + command | button | 0 = released, 1 = pressed | OSB 15 of either MFD, same ids as the MFD bezel OSB row |
| 16. Format Select Buttons | MFD_L_12, MFD_R_12, MFD_L_13, MFD_R_13, MFD_L_14, MFD_R_14 | read + command | button | 0 = released, 1 = pressed | OSB 12, 13 and 14 of either MFD, same ids as the MFD bezel OSB row |
| 17. Declutter Button | MFD_L_11, MFD_R_11 | read + command | button | 0 = released, 1 = pressed | OSB 11 of either MFD, same ids as the MFD bezel OSB row |

## Defensive systems

### Threat Warning Azimuth Indicator (p. 694)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| Azimuth scope | — | — | export | — | No scope output in DCS-BIOS |
| Brightness knob | RWR_INTENS_KNB | read + command | knob | continuous, 0 to 65535 | likely; RWR Intensity Knob |

### Threat Warning Prime Control Panel (p. 695)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. HANDOFF Button | RWR_HANDOFF_BTN, LIGHT_RWR_HANDOFF_H, LIGHT_RWR_HANDOFF_UP | read + command | RWR_HANDOFF_BTN: button; LIGHT_RWR_HANDOFF_H, LIGHT_RWR_HANDOFF_UP: lamp | RWR_HANDOFF_BTN: 0 = released, 1 = pressed; LIGHT_RWR_HANDOFF_H, LIGHT_RWR_HANDOFF_UP: 0 = off, 1 = lit | Button plus the two HANDOFF lights (H and UP); read only: LIGHT_RWR_HANDOFF_H, LIGHT_RWR_HANDOFF_UP |
| 2. MODE Button | RWR_MODE_BTN, LIGHT_RWR_MODE_OPEN, LIGHT_RWR_MODE_PRI | read + command | RWR_MODE_BTN: button; LIGHT_RWR_MODE_OPEN, LIGHT_RWR_MODE_PRI: lamp | RWR_MODE_BTN: 0 = released, 1 = pressed; LIGHT_RWR_MODE_OPEN, LIGHT_RWR_MODE_PRI: 0 = off, 1 = lit | Button plus the OPEN and PRIORITY lights; read only: LIGHT_RWR_MODE_OPEN, LIGHT_RWR_MODE_PRI |
| 3. LAUNCH Button | RWR_LAUNCH_BTN, LIGHT_RWR_MSL_LAUNCH | read + command | RWR_LAUNCH_BTN: button; LIGHT_RWR_MSL_LAUNCH: lamp | RWR_LAUNCH_BTN: 0 = released, 1 = pressed; LIGHT_RWR_MSL_LAUNCH: 0 = off, 1 = lit | Button plus the MISSILE LAUNCH light; read only: LIGHT_RWR_MSL_LAUNCH |
| 4. TGT SEP Button | RWR_T_BTN, LIGHT_RWR_TGTSEP_UP, LIGHT_RWR_TGTSEP_DN | read + command | RWR_T_BTN: button; LIGHT_RWR_TGTSEP_UP, LIGHT_RWR_TGTSEP_DN: lamp | RWR_T_BTN: 0 = released, 1 = pressed; LIGHT_RWR_TGTSEP_UP, LIGHT_RWR_TGTSEP_DN: 0 = off, 1 = lit | likely; DCS-BIOS calls the button T Button; lights are TGT SEP UP and DOWN; read only: LIGHT_RWR_TGTSEP_UP, LIGHT_RWR_TGTSEP_DN |
| 5. UNKNOWN Button | RWR_UNKNOWN_SHIP_BTN, LIGHT_RWR_SHIP_U, LIGHT_RWR_SHIP_UNK | read + command | RWR_UNKNOWN_SHIP_BTN: button; LIGHT_RWR_SHIP_U, LIGHT_RWR_SHIP_UNK: lamp | RWR_UNKNOWN_SHIP_BTN: 0 = released, 1 = pressed; LIGHT_RWR_SHIP_U, LIGHT_RWR_SHIP_UNK: 0 = off, 1 = lit | Button plus the U lights (SHIP U and SHIP UNKNOWN); read only: LIGHT_RWR_SHIP_U, LIGHT_RWR_SHIP_UNK |
| 6. SYS TEST Button | RWR_SYS_TEST_BTN, LIGHT_RWR_SYSTEST, LIGHT_RWR_SYSTEST_ON | read + command | RWR_SYS_TEST_BTN: button; LIGHT_RWR_SYSTEST, LIGHT_RWR_SYSTEST_ON: lamp | RWR_SYS_TEST_BTN: 0 = released, 1 = pressed; LIGHT_RWR_SYSTEST, LIGHT_RWR_SYSTEST_ON: 0 = off, 1 = lit | Button plus the SYSTEST and ON lights; read only: LIGHT_RWR_SYSTEST, LIGHT_RWR_SYSTEST_ON |

### Threat Warning Auxiliary Control Panel (p. 696)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. SEARCH Button | RWR_SEARCH_BTN, LIGHT_RWR_SEARCH | read + command | RWR_SEARCH_BTN: button; LIGHT_RWR_SEARCH: lamp | RWR_SEARCH_BTN: 0 = released, 1 = pressed; LIGHT_RWR_SEARCH: 0 = off, 1 = lit | Button plus the S light; read only: LIGHT_RWR_SEARCH |
| 2. ACT/PWR Button | RWR_ACT_PWR_BTN, LIGHT_RWR_ACT_POWER, LIGHT_RWR_ACTIVITY | read + command | RWR_ACT_PWR_BTN: button; LIGHT_RWR_ACT_POWER, LIGHT_RWR_ACTIVITY: lamp | RWR_ACT_PWR_BTN: 0 = released, 1 = pressed; LIGHT_RWR_ACT_POWER, LIGHT_RWR_ACTIVITY: 0 = off, 1 = lit | Button plus the POWER and ACTIVITY lights; read only: LIGHT_RWR_ACT_POWER, LIGHT_RWR_ACTIVITY |
| 3. ALTITUDE Button | RWR_ALT_BTN, LIGHT_RWR_ALT, LIGHT_RWR_ALT_LOW | read + command | RWR_ALT_BTN: button; LIGHT_RWR_ALT, LIGHT_RWR_ALT_LOW: lamp | RWR_ALT_BTN: 0 = released, 1 = pressed; LIGHT_RWR_ALT, LIGHT_RWR_ALT_LOW: 0 = off, 1 = lit | Button plus the ALT and LOW lights; read only: LIGHT_RWR_ALT, LIGHT_RWR_ALT_LOW |
| 4. POWER Button | RWR_PWR_BTN, LIGHT_RWR_POWER | read + command | RWR_PWR_BTN: button; LIGHT_RWR_POWER: lamp | RWR_PWR_BTN: guess: 0 = off, 1 = on; LIGHT_RWR_POWER: 0 = off, 1 = lit | Toggle in DCS-BIOS; plus the SYSTEM POWER light; read only: LIGHT_RWR_POWER |
| 5. DIM Knob | RWR_IND_DIM_KNB | read + command | knob | continuous, 0 to 65535 | RWR Indicator Control DIM Knob - Rotate to adjust brightness |

### CMDS Control Panel (p. 697)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. Status Display | LIGHT_CMDS_NO_GO, LIGHT_CMDS_GO, LIGHT_CMDS_DISP, LIGHT_CMDS_RDY | read only | lamp | 0 = off, 1 = lit | Four green lights: NO GO, GO, DISP and RDY |
| 2. Quantity Display | CMDS_CH_AMOUNT, CMDS_FL_AMOUNT, CMDS_O1_AMOUNT, CMDS_O2_AMOUNT | read only | display | text of 4 characters | Text of 4 characters per count; O1 and O2 are unused in the manual |
| 3. RWR Switch | CMDS_PWR_SOURCHE_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | CMDS RWR Source Switch; DCS-BIOS description: CMDS RWR Source Switch, ON/OFF |
| 4. O1 Switch | CMDS_01_EXP_CAT_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | Written with a zero (01) in the identifier; DCS-BIOS description: CMDS O1 Expendable Category Switch, ON/OFF |
| 4. O2 Switch | CMDS_02_EXP_CAT_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | Written with a zero (02) in the identifier; DCS-BIOS description: CMDS O2 Expendable Category Switch, ON/OFF |
| 4. CH Switch | CMDS_CH_EXP_CAT_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | CMDS CH Expendable Category Switch, ON/OFF |
| 4. FL Switch | CMDS_FL_EXP_CAT_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | CMDS FL Expendable Category Switch, ON/OFF |
| 5. JMR Switch | CMDS_JMR_SOURCHE_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | CMDS JMR Source Switch; DCS-BIOS description: CMDS JMR Source Switch, ON/OFF |
| 6. MWS Switch | CMDS_MWS_SOURCHE_SW | read + command | selector (2) | guess: 0 = OFF, 1 = ON | CMDS MWS Source Switch; DCS-BIOS description: CMDS MWS Source Switch, ON/OFF |
| 7. JETT Switch | CMDS_JETT_SW | read + command | selector (2) | guess: 0 = OFF, 1 = JETT | Jettison Switch, JETT/OFF |
| 8. PRGM Knob | CMDS_PROG_KNB | read + command | selector (5) | 0 = BIT, 1 = 1, 2 = 2, 3 = 3, 4 = 4 | CMDS PROGRAM Knob |
| 9. MODE Knob | CMDS_MODE_KNB | read + command | selector (6) | 0 = OFF, 1 = STBY, 2 = MAN, 3 = SEMI, 4 = AUTO, 5 = BYP | CMDS MODE Knob |

### ECM Control Panel (p. 706)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| 1. ECM Power Switch | ECM_PW_SW | read + command | selector (3) | guess: 0 = OFF, 1 = STBY, 2 = OPR | ECM Power Switch |
| 2. XMIT Switch | ECM_XMIT_SW | read + command | selector (3) | guess: 0 = XMIT 3, 1 = XMIT 2, 2 = XMIT 1 | ECM XMIT Switch |
| 3. DIM Knob | ECM_DIM_KNB | read + command | knob | continuous, 0 to 65535 | ECM DIM Rotary Knob |
| 4. RESET Button | ECM_RESET_BTN | read + command | button | 0 = released, 1 = pressed | ECM Reset Button |
| 5. BIT Button | ECM_BIT_BTN | read + command | button | 0 = released, 1 = pressed | ECM Bit Button |
| 6. ECM Module Control Button 1 | ECM_1_BTN, LIGHT_ECM_1_S, LIGHT_ECM_1_A, LIGHT_ECM_1_F, LIGHT_ECM_1_T | read + command | ECM_1_BTN: button; LIGHT_ECM_1_S, LIGHT_ECM_1_A, LIGHT_ECM_1_F, LIGHT_ECM_1_T: lamp | ECM_1_BTN: guess: 0 = out, 1 = in; LIGHT_ECM_1_S, LIGHT_ECM_1_A, LIGHT_ECM_1_F, LIGHT_ECM_1_T: 0 = off, 1 = lit | Latching button plus its S, A, F and T lights; read only: LIGHT_ECM_1_S, LIGHT_ECM_1_A, LIGHT_ECM_1_F, LIGHT_ECM_1_T |
| 6. ECM Module Control Button 2 | ECM_2_BTN, LIGHT_ECM_2_S, LIGHT_ECM_2_A, LIGHT_ECM_2_F, LIGHT_ECM_2_T | read + command | ECM_2_BTN: button; LIGHT_ECM_2_S, LIGHT_ECM_2_A, LIGHT_ECM_2_F, LIGHT_ECM_2_T: lamp | ECM_2_BTN: guess: 0 = out, 1 = in; LIGHT_ECM_2_S, LIGHT_ECM_2_A, LIGHT_ECM_2_F, LIGHT_ECM_2_T: 0 = off, 1 = lit | Latching button plus its S, A, F and T lights; read only: LIGHT_ECM_2_S, LIGHT_ECM_2_A, LIGHT_ECM_2_F, LIGHT_ECM_2_T |
| 6. ECM Module Control Button 3 | ECM_3_BTN, LIGHT_ECM_3_S, LIGHT_ECM_3_A, LIGHT_ECM_3_F, LIGHT_ECM_3_T | read + command | ECM_3_BTN: button; LIGHT_ECM_3_S, LIGHT_ECM_3_A, LIGHT_ECM_3_F, LIGHT_ECM_3_T: lamp | ECM_3_BTN: guess: 0 = out, 1 = in; LIGHT_ECM_3_S, LIGHT_ECM_3_A, LIGHT_ECM_3_F, LIGHT_ECM_3_T: 0 = off, 1 = lit | Latching button plus its S, A, F and T lights; read only: LIGHT_ECM_3_S, LIGHT_ECM_3_A, LIGHT_ECM_3_F, LIGHT_ECM_3_T |
| 6. ECM Module Control Button 4 | ECM_4_BTN, LIGHT_ECM_4_S, LIGHT_ECM_4_A, LIGHT_ECM_4_F, LIGHT_ECM_4_T | read + command | ECM_4_BTN: button; LIGHT_ECM_4_S, LIGHT_ECM_4_A, LIGHT_ECM_4_F, LIGHT_ECM_4_T: lamp | ECM_4_BTN: guess: 0 = out, 1 = in; LIGHT_ECM_4_S, LIGHT_ECM_4_A, LIGHT_ECM_4_F, LIGHT_ECM_4_T: 0 = off, 1 = lit | Latching button plus its S, A, F and T lights; read only: LIGHT_ECM_4_S, LIGHT_ECM_4_A, LIGHT_ECM_4_F, LIGHT_ECM_4_T |
| 6. ECM Module Control Button 5 | ECM_5_BTN, LIGHT_ECM_5_S, LIGHT_ECM_5_A, LIGHT_ECM_5_F, LIGHT_ECM_5_T | read + command | ECM_5_BTN: button; LIGHT_ECM_5_S, LIGHT_ECM_5_A, LIGHT_ECM_5_F, LIGHT_ECM_5_T: lamp | ECM_5_BTN: guess: 0 = out, 1 = in; LIGHT_ECM_5_S, LIGHT_ECM_5_A, LIGHT_ECM_5_F, LIGHT_ECM_5_T: 0 = off, 1 = lit | Latching button plus its S, A, F and T lights; read only: LIGHT_ECM_5_S, LIGHT_ECM_5_A, LIGHT_ECM_5_F, LIGHT_ECM_5_T |
| 6. ECM Module Control Button (unmarked) | ECM_6_BTN, LIGHT_ECM_S, LIGHT_ECM_A, LIGHT_ECM_F, LIGHT_ECM_T | read + command | ECM_6_BTN: button; LIGHT_ECM_S, LIGHT_ECM_A, LIGHT_ECM_F, LIGHT_ECM_T: lamp | ECM_6_BTN: guess: 0 = out, 1 = in; LIGHT_ECM_S, LIGHT_ECM_A, LIGHT_ECM_F, LIGHT_ECM_T: 0 = off, 1 = lit | likely; Sixth button; its lights are the ones without a number; read only: LIGHT_ECM_S, LIGHT_ECM_A, LIGHT_ECM_F, LIGHT_ECM_T |
| 6. ECM Module Control Button FRM | ECM_FRM_BTN, LIGHT_ECM_FRM_S, LIGHT_ECM_FRM_A, LIGHT_ECM_FRM_F, LIGHT_ECM_FRM_T | read + command | ECM_FRM_BTN: button; LIGHT_ECM_FRM_S, LIGHT_ECM_FRM_A, LIGHT_ECM_FRM_F, LIGHT_ECM_FRM_T: lamp | ECM_FRM_BTN: guess: 0 = out, 1 = in; LIGHT_ECM_FRM_S, LIGHT_ECM_FRM_A, LIGHT_ECM_FRM_F, LIGHT_ECM_FRM_T: 0 = off, 1 = lit | Latching button plus its S, A, F and T lights; read only: LIGHT_ECM_FRM_S, LIGHT_ECM_FRM_A, LIGHT_ECM_FRM_F, LIGHT_ECM_FRM_T |
| 6. ECM Module Control Button SPL | ECM_SPL_BTN, LIGHT_ECM_SPL_S, LIGHT_ECM_SPL_A, LIGHT_ECM_SPL_F, LIGHT_ECM_SPL_T | read + command | ECM_SPL_BTN: button; LIGHT_ECM_SPL_S, LIGHT_ECM_SPL_A, LIGHT_ECM_SPL_F, LIGHT_ECM_SPL_T: lamp | ECM_SPL_BTN: guess: 0 = out, 1 = in; LIGHT_ECM_SPL_S, LIGHT_ECM_SPL_A, LIGHT_ECM_SPL_F, LIGHT_ECM_SPL_T: 0 = off, 1 = lit | Latching button plus its S, A, F and T lights; read only: LIGHT_ECM_SPL_S, LIGHT_ECM_SPL_A, LIGHT_ECM_SPL_F, LIGHT_ECM_SPL_T |

### CHAFF/FLARE Dispense Button (p. 708)

| Control | DCS-BIOS identifier | Access | Build | Position order | Note |
| --- | --- | --- | --- | --- | --- |
| CHAFF/FLARE Dispense button | CMDS_DISPENSE_BTN | read + command | button | 0 = released, 1 = pressed | Category CMDS in DCS-BIOS |

## DCS-BIOS controls not in PANELS.md

These controls exist in DCS-BIOS but no row of PANELS.md describes them (the manual does not cover them, or they belong to the external model). Columns as above, with the DCS-BIOS identifier first; the description is the DCS-BIOS one. Every other identifier of the module is on a row above.

### ADI (DCS-BIOS only)

| DCS-BIOS identifier | Access | Build | Position order | Description | Note |
| --- | --- | --- | --- | --- | --- |
| ADI_GS_BAR | read only | bar or gauge | 0 to 65535 along the scale | ADI GS Bar | Related to the ADI; PANELS lists no glide slope bar |
| ADI_GS_FLAG | read only | bar or gauge | 0 to 65535 along the scale | ADI GS Flag | Related to the ADI; PANELS lists no glide slope flag |
| ADI_LOC_BAR | read only | bar or gauge | 0 to 65535 along the scale | ADI LOC Bar | Related to the ADI; PANELS lists no localizer bar |
| ADI_LOC_FLAG | read only | bar or gauge | 0 to 65535 along the scale | ADI LOC Flag | Related to the ADI; PANELS lists no localizer flag |

### Clock (DCS-BIOS only)

| DCS-BIOS identifier | Access | Build | Position order | Description | Note |
| --- | --- | --- | --- | --- | --- |
| CLOCK_ELAPSED | read + command | button | 0 = released, 1 = pressed | Clock Elapsed Time Knob | Related to the Mechanical Clock; PANELS lists no elapsed time function |
| CLOCK_ELAPSED_TIME_M | read only | bar or gauge | 0 to 65535 along the scale | Elapsed Time Minutes | Related to the Mechanical Clock; PANELS lists no elapsed time hands |
| CLOCK_ELAPSED_TIME_SEC | read only | bar or gauge | 0 to 65535 along the scale | Elapsed Time Seconds | Related to the Mechanical Clock; PANELS lists no elapsed time hands |

### Cockpit Mechanics (DCS-BIOS only)

| DCS-BIOS identifier | Access | Build | Position order | Description | Note |
| --- | --- | --- | --- | --- | --- |
| CANOPY_POS | read only | bar or gauge | 0 to 65535 along the scale | Canopy Position | Canopy position as output; related to the Canopy Switch |
| HIDE_STICK | read + command | selector (2) | guess: 0 = off, 1 = on | Hide Stick toggle | Hides the stick model |

### DED Output Data (Deprecated) (DCS-BIOS only)

| DCS-BIOS identifier | Access | Build | Position order | Description | Note |
| --- | --- | --- | --- | --- | --- |
| DED_LINE_1 | read only | display | text of 29 characters | DED Display Line 1 | Deprecated line output of the DED (29 characters); the new one is DED_L1 |
| DED_LINE_2 | read only | display | text of 29 characters | DED Display Line 2 | Deprecated line output of the DED (29 characters); the new one is DED_L2 |
| DED_LINE_3 | read only | display | text of 29 characters | DED Display Line 3 | Deprecated line output of the DED (29 characters); the new one is DED_L3 |
| DED_LINE_4 | read only | display | text of 29 characters | DED Display Line 4 | Deprecated line output of the DED (29 characters); the new one is DED_L4 |
| DED_LINE_5 | read only | display | text of 29 characters | DED Display Line 5 | Deprecated line output of the DED (29 characters); the new one is DED_L5 |

### ECS (DCS-BIOS only)

| DCS-BIOS identifier | Access | Build | Position order | Description | Note |
| --- | --- | --- | --- | --- | --- |
| AIR_SOURCE_KNB | read + command | selector (5) | guess: 0 = OFF, 1 = NORM, 2 = DUMP, 3 = RAM, 4 = unknown | AIR SOURCE Knob | Deprecated since 0.11.1: five positions for a four-position knob; use AIR_SOURCE_KNOB (AIR COND Control Panel). Not used by the dashboard |

### External Aircraft Model (DCS-BIOS only)

| DCS-BIOS identifier | Access | Build | Position order | Description | Note |
| --- | --- | --- | --- | --- | --- |
| EXT_FORMATION_LIGHTS | read only | none | 0 to 65535 | Formation Lights |  |
| EXT_POSITION_LIGHTS_WING | read only | none | 0 = off, 1 = on | Wing Position Lights (L-red; R-green) |  |
| EXT_POSITION_LIGHT_FUSELAGE | read only | none | 0 = off, 1 = on | Fuselage Position Lights (L-red; R-green;Back-white) |  |
| EXT_SPEED_BRAKE_LEFT | read only | none | 0 to 65535 | Left Speed Brake |  |
| EXT_SPEED_BRAKE_RIGHT | read only | none | 0 to 65535 | Right Speed Brake |  |
| EXT_STROBE_TAIL | read only | none | 0 = off, 1 = on | Tail Strobe Light |  |
| EXT_TAIL_LIGHT | read only | none | 0 to 65535 | Tail Lights |  |
| EXT_WOW_LEFT | read only | none | 0 = off, 1 = on | Weight ON Wheels Left Gear |  |
| EXT_WOW_NOSE | read only | none | 0 = off, 1 = on | Weight ON Wheels Nose Gear |  |
| EXT_WOW_RIGHT | read only | none | 0 = off, 1 = on | Weight ON Wheels Right Gear |  |

### Interior Lights Indicators (DCS-BIOS only)

| DCS-BIOS identifier | Access | Build | Position order | Description | Note |
| --- | --- | --- | --- | --- | --- |
| LIGHT_CONSLES | read only | bar or gauge | 0 to 65535 along the scale | Consoles Lightning (green) | Lighting state as output; related to the Interior LIGHTING Control Panel |
| LIGHT_CONSLES_FLOOD | read only | bar or gauge | 0 to 65535 along the scale | Consoles Flood Lightning (green) | Lighting state as output; related to the Interior LIGHTING Control Panel |
| LIGHT_INST_PNL | read only | bar or gauge | 0 to 65535 along the scale | Instrumen Panel Lightning (green) | Lighting state as output; related to the Interior LIGHTING Control Panel |
| LIGHT_INST_PNL_FLOOD | read only | bar or gauge | 0 to 65535 along the scale | Instrumen Panel Flood Lightning (green) | Lighting state as output; related to the Interior LIGHTING Control Panel |

### Radio Frequencies (DCS-BIOS only)

| DCS-BIOS identifier | Access | Build | Position order | Description | Note |
| --- | --- | --- | --- | --- | --- |
| UHF_RADIO | read + command | display | text of 7 characters | UHF RADIO | Frequency string, can be set by string; the UHF Backup Control Panel knobs are on its rows |
| VHF_RADIO | read + command | display | text of 7 characters | VHF RADIO | Frequency string, can be set by string; no VHF panel in PANELS |

### Warning, Caution and IndicatorLights (DCS-BIOS only)

| DCS-BIOS identifier | Access | Build | Position order | Description | Note |
| --- | --- | --- | --- | --- | --- |
| LIGHT_CAUTION_1 | read only | lamp | 0 = off, 1 = lit | 1. Caution - Light (yellow) | Unnamed caution light of the Caution Light Panel block in the module; no legend in PANELS |
| LIGHT_CAUTION_2 | read only | lamp | 0 = off, 1 = lit | 2. Caution - Light (yellow) | Unnamed caution light of the Caution Light Panel block in the module; no legend in PANELS |
| LIGHT_CAUTION_3 | read only | lamp | 0 = off, 1 = lit | 3. Caution - Light (yellow) | Unnamed caution light of the Caution Light Panel block in the module; no legend in PANELS |
| LIGHT_CAUTION_4 | read only | lamp | 0 = off, 1 = lit | 4. Caution - Light (yellow) | Unnamed caution light of the Caution Light Panel block in the module; no legend in PANELS |
| LIGHT_CAUTION_5 | read only | lamp | 0 = off, 1 = lit | 5. Caution - Light (yellow) | Unnamed caution light of the Caution Light Panel block in the module; no legend in PANELS |
| LIGHT_CAUTION_6 | read only | lamp | 0 = off, 1 = lit | 6. Caution - Light  (yellow) | Unnamed caution light of the Caution Light Panel block in the module; no legend in PANELS |
| LIGHT_EDGE | read only | lamp | 0 = off, 1 = lit | Edge - Light (red) | Red light in the glareshield edge group of the module; no legend in PANELS |
| LIGHT_ELEC | read only | lamp | 0 = off, 1 = lit | Elec - Light (red) | Red light listed with the ELEC Control Panel lights in the module; not named in PANELS |
| LIGHT_MARKER_BEACON | read only | lamp | 0 = off, 1 = lit | MARKER BEACON Light (green) | No panel for it in PANELS |

## Summary

Rows counted over all tables above the "DCS-BIOS controls not in PANELS.md" part. A row is one row of PANELS.md; the DCS-BIOS-only column counts the identifiers of the last part.

| Access | PANELS.md rows | DCS-BIOS-only controls |
| --- | --- | --- |
| read + command | 236 | 5 |
| read only | 107 | 35 |
| — | 55 | 0 |
| Total | 398 | 40 |

Of the 522 identifiers, 482 are on PANELS.md rows and 40 are in the DCS-BIOS-only part. 39 identifiers appear on more than one row: ADI_BANK (three rows: attitude sphere, upper and lower bank pointers, all ADI) and the 38 OSB identifiers MFD_L_n and MFD_R_n (two rows each: the MFD bezel OSB rows and the MFD Format Selection Master Menu rows, because the menu buttons are the same OSBs). Rows with several identifiers (button and lamp, left and right MFD) make the identifier count higher than the row count.

Build of all 522 identifiers (from the classification table):

| Build | Identifiers |
| --- | --- |
| lamp | 130 |
| button | 101 |
| bar or gauge | 71 |
| selector (2) | 59 |
| selector (3) | 37 |
| knob | 34 |
| display | 27 |
| selector (3) spring | 27 |
| none | 11 |
| selector (4) | 5 |
| selector (5) | 5 |
| step rocker (3200) | 5 |
| selector (10) | 3 |
| selector (8) | 2 |
| selector (2) NO READBACK | 1 |
| selector (20) | 1 |
| selector (21) | 1 |
| selector (6) | 1 |
| selector (7) | 1 |
| Total | 522 |

### NO READBACK (1)

- FUEL_QTY_SEL_T_KNB: FUEL QTY SEL Knob, TEST; no output is named FUEL_QTY_SEL_T_KNB, the state comes back as FUEL_QTY_SEL_T_KNB_INT and FUEL_QTY_SEL_T_KNB_STR. PANELS row: 1. FUEL QTY SEL Knob (FUEL QTY SEL Panel).

### Position orders that are guesses (phase 7)

Every identifier whose position order starts with `guess:` above, to be checked in DCS when the module is installed. The orders follow the rules in the column list at the top.

- Miscellaneous (MISC) Panel (p. 47)
  - 3. LASER ARM Switch: LASER_ARM_SW — 0 = OFF, 1 = LASER ARM
  - 6. ADV MODE Button: ADV_MODE_SW — 0 = off, 1 = on
- FUEL QTY SEL Panel (p. 54)
  - 1. FUEL QTY SEL Knob: FUEL_QTY_SEL_T_KNB — 0 = not TEST, 1 = TEST
  - 2. EXT FUEL TRANS Switch: EXT_FUEL_TRANS_SW — 0 = WING FIRST, 1 = NORM
- Landing Gear Panel (p. 55)
  - 2. HOOK Switch: HOOK_SW — 0 = DN, 1 = UP
  - 4. LG Handle: GEAR_HANDLE — 0 = DOWN, 1 = UP
  - 5. GND JETT ENABLE Switch: GND_JETT_ENABLE_SW — 0 = OFF, 1 = ENABLE
  - 6. BRAKES Channel Switch: BRAKE_CHAN_SW — 0 = CHAN 2, 1 = CHAN 1
  - 9. STORES CONFIG Switch: STORES_CONFIG_SW — 0 = CAT III, 1 = CAT I
- ALT GEAR Handle (p. 57)
  - ALT GEAR handle: GEAR_ALT_HANDLE — 0 = STOW, 1 = PULL
- Manual Pitch Override Switch (p. 62)
  - MANUAL PITCH override switch: MANUAL_PITCH_SW — 0 = NORM, 1 = OVRD
- ENG & JET START Control Panel (p. 63)
  - 3. ENG CONT Switch: ENG_CONT_SW — 0 = SEC, 1 = PRI
  - 3. ENG CONT Switch: ENG_CONT_SW_COVER — 0 = CLOSE, 1 = OPEN
  - 5. MAX POWER Switch: MAX_PWR_SW — 0 = OFF, 1 = MAX POWER
- EPU Control Panel (p. 64)
  - 1. EPU Switch: EPU_SW_COVER_OFF — 0 = CLOSE, 1 = OPEN
  - 1. EPU Switch: EPU_SW_COVER_ON — 0 = CLOSE, 1 = OPEN
- AUDIO 1 Control Panel (p. 65)
  - 3. COMM 1 Mode Knob: COMM1_MODE_KNB — 0 = OFF, 1 = SQL, 2 = GD
  - 4. COMM 2 Mode Knob: COMM2_MODE_KNB — 0 = OFF, 1 = SQL, 2 = GD
- FUEL Control Panel (p. 67)
  - 1. FUEL MASTER Switch: FUEL_MASTER_SW — 0 = OFF, 1 = MASTER
  - 1. FUEL MASTER Switch: FUEL_MASTER_CV — 0 = CLOSE, 1 = OPEN
  - 2. TANK INERTING Switch: TANK_INTERTING_SW — 0 = OFF, 1 = TANK INERTING
  - 4. AIR REFUEL Switch: AIR_REFUEL_SW — 0 = CLOSE, 1 = OPEN
- IFF Control Panel (p. 67)
  - 3. C & I Knob: IFF_C_I_KNB — 0 = UFC, 1 = BACK UP
  - 5. MODE 1 & MODE 3 Thumbwheel Selectors: IFF_M1_SEL_1 — 0 = DN, 1 = CENTER, 2 = UP
  - 5. MODE 1 & MODE 3 Thumbwheel Selectors: IFF_M1_SEL_2 — 0 = DN, 1 = CENTER, 2 = UP
  - 5. MODE 1 & MODE 3 Thumbwheel Selectors: IFF_M3_SEL_1 — 0 = DN, 1 = CENTER, 2 = UP
  - 5. MODE 1 & MODE 3 Thumbwheel Selectors: IFF_M3_SEL_2 — 0 = DN, 1 = CENTER, 2 = UP
  - 7. MODE 4 MONITOR Switch: IFF_M4_MONITOR_SW — 0 = OUT, 1 = AUDIO
- EXT LIGHTING Control Panel (p. 69)
  - 1. POSITION FLASH / STEADY Switch: POS_FLASH_LIGHT_SW — 0 = STEADY, 1 = FLASH
- FLT CONTROL Panel (p. 71)
  - 1. DIGITAL BACKUP Switch: DIGI_BAK_SW — 0 = OFF, 1 = BACKUP
  - 2. MANUAL TF FLY-UP Switch: MAN_TF_FLYUP_SW — 0 = ENABLE, 1 = DISABLE
  - 3. ALT FLAPS Switch: ALT_FLAPS_SW — 0 = NORM, 1 = EXTEND
  - 5. LE FLAPS Switch: LE_FLAPS_SW — 0 = AUTO, 1 = LOCK
  - 6. FLCS RESET Switch: FLCS_RESET_SW — 0 = OFF, 1 = RESET
  - 7. FLCS BIT Switch: BIT_SW — 0 = OFF, 1 = BIT
- MANUAL TRIM Panel (p. 72)
  - 4. TRIM/AP DISC Switch: TRIM_AP_DISC_SW — 0 = DISC, 1 = NORM
- TEST Panel (p. 72)
  - 2. OBOGS BIT Switch: OBOGS_SW — 0 = OFF, 1 = BIT
  - 5. EPU/GEN Switch: EPU_GEN_TEST_SW — 0 = OFF, 1 = EPU/GEN
- Canopy Switch and Canopy Handle (p. 73)
  - 2. Canopy Lever: CANOPY_HANDLE — 0 = LOCKED, 1 = UNLOCKED
- Canopy Jettison T-Handle (p. 74)
  - CANOPY JETTISON T-handle: CANOPY_JETT_THANDLE — 0 = STOW, 1 = PULL
- DEFOG Lever (p. 74)
  - DEFOG lever: DEFOG_LEVER — 0 = MIN, 1 to 19 = in between, 20 = MAX
- UHF Backup Control Panel (p. 260)
  - 1. Preset Channel Card & Access Door: UHF_DOOR — 0 = CLOSE, 1 = OPEN
  - 4. CHAN Knob: UHF_CHAN_KNB — 0 = preset 1, 1 = preset 2, ... 19 = preset 20
  - 7. A-3-2 Knob: UHF_FREQ_100_KNB — 0 = A, 1 = 3, 2 = 2
  - 8. Manual Frequency Knobs: UHF_FREQ_10_KNB — 0 to 9 = digit 0 to 9
  - 8. Manual Frequency Knobs: UHF_FREQ_1_KNB — 0 to 9 = digit 0 to 9
  - 8. Manual Frequency Knobs: UHF_FREQ_01_KNB — 0 to 9 = digit 0 to 9
  - 8. Manual Frequency Knobs: UHF_FREQ_0025_KNB — 0 = 00, 1 = 25, 2 = 50, 3 = 75
  - 9. Function Knob: UHF_FUNC_KNB — 0 = OFF, 1 = MAIN, 2 = BOTH, 3 = ADF
  - 10. Mode Knob: UHF_MODE_KNB — 0 = MNL, 1 = PRESET, 2 = GRD
  - 13. SQUELCH Switch: UHF_SQUELCH_SW — 0 = OFF, 1 = ON
- SNSR PWR Control Panel (p. 75)
  - 1. LEFT HDPT Switch: HDPT_SW_L — 0 = OFF, 1 = ON
  - 2. RIGHT HDPT Switch: HDPT_SW_R — 0 = OFF, 1 = ON
  - 3. FCR Switch: FCR_PWR_SW — 0 = OFF, 1 = ON
- OXYGEN Regulator Panel (p. 77)
  - 4. Diluter Lever: OXY_DILUTER_LVR — 0 = NORM, 1 = 100%
- AVIONICS POWER Control Panel (p. 78)
  - 1. MMC Switch: MMC_PWR_SW — 0 = OFF, 1 = ON
  - 2. ST STA Switch: ST_STA_SW — 0 = OFF, 1 = ON
  - 3. MFD Switch: MFD_SW — 0 = OFF, 1 = ON
  - 4. UFC Switch: UFC_SW — 0 = OFF, 1 = ON
  - 5. MAP Switch: MAP_SW — 0 = OFF, 1 = ON
  - 6. GPS Switch: GPS_SW — 0 = OFF, 1 = ON
  - 7. DL Switch: DL_SW — 0 = OFF, 1 = ON
- VOICE MESSAGE Switch (p. 80)
  - VOICE MESSAGE switch: VMS_INHIBIT_SW — 0 = VOICE MESSAGE, 1 = INHIBIT
- ZEROIZE Switch (p. 80)
  - ZEROIZE switch: ZEROIZE_SW_COVER — 0 = CLOSE, 1 = OPEN
- Ejection Seat Controls (pp. 81, 82)
  - Ejection Handle: SEAT_EJECT_HANDLE — 0 = STOW, 1 = PULL
  - Ejection Seat Arming Lever: SEAT_EJECT_SAFE — 0 = ARMED, 1 = LOCKED
- Integrated Control Panel (ICP) (p. 99)
  - 11. DED Increment/Decrement Rocker: ICP_DED_SW — 0 = DN, 1 = CENTER, 2 = UP
  - 12. Data Control Switch (DCS): ICP_DATA_RTN_SEQ_SW — 0 = RTN, 1 = CENTER, 2 = SEQ
  - 12. Data Control Switch (DCS): ICP_DATA_UP_DN_SW — 0 = DN, 1 = CENTER, 2 = UP
  - 14. FLIR Increment/Decrement Rocker: ICP_FLIR_SW — 0 = DN, 1 = CENTER, 2 = UP
- Multi-Function Display (MFD) bezel (p. 122)
  - 2. GAIN Rocker: MFD_L_GAIN_SW — 0 = DN, 1 = CENTER, 2 = UP
  - 2. GAIN Rocker: MFD_R_GAIN_SW — 0 = DN, 1 = CENTER, 2 = UP
  - 3. SYM Rocker: MFD_L_SYM_SW — 0 = DN, 1 = CENTER, 2 = UP
  - 3. SYM Rocker: MFD_R_SYM_SW — 0 = DN, 1 = CENTER, 2 = UP
  - 4. BRT Rocker: MFD_L_BRT_SW — 0 = DN, 1 = CENTER, 2 = UP
  - 4. BRT Rocker: MFD_R_BRT_SW — 0 = DN, 1 = CENTER, 2 = UP
  - 5. CON Rocker: MFD_L_CON_SW — 0 = DN, 1 = CENTER, 2 = UP
  - 5. CON Rocker: MFD_R_CON_SW — 0 = DN, 1 = CENTER, 2 = UP
- Threat Warning Auxiliary Control Panel (p. 696)
  - 4. POWER Button: RWR_PWR_BTN — 0 = off, 1 = on
- CMDS Control Panel (p. 697)
  - 3. RWR Switch: CMDS_PWR_SOURCHE_SW — 0 = OFF, 1 = ON
  - 4. O1 Switch: CMDS_01_EXP_CAT_SW — 0 = OFF, 1 = ON
  - 4. O2 Switch: CMDS_02_EXP_CAT_SW — 0 = OFF, 1 = ON
  - 4. CH Switch: CMDS_CH_EXP_CAT_SW — 0 = OFF, 1 = ON
  - 4. FL Switch: CMDS_FL_EXP_CAT_SW — 0 = OFF, 1 = ON
  - 5. JMR Switch: CMDS_JMR_SOURCHE_SW — 0 = OFF, 1 = ON
  - 6. MWS Switch: CMDS_MWS_SOURCHE_SW — 0 = OFF, 1 = ON
  - 7. JETT Switch: CMDS_JETT_SW — 0 = OFF, 1 = JETT
- ECM Control Panel (p. 706)
  - 1. ECM Power Switch: ECM_PW_SW — 0 = OFF, 1 = STBY, 2 = OPR
  - 2. XMIT Switch: ECM_XMIT_SW — 0 = XMIT 3, 1 = XMIT 2, 2 = XMIT 1
  - 6. ECM Module Control Button 1: ECM_1_BTN — 0 = out, 1 = in
  - 6. ECM Module Control Button 2: ECM_2_BTN — 0 = out, 1 = in
  - 6. ECM Module Control Button 3: ECM_3_BTN — 0 = out, 1 = in
  - 6. ECM Module Control Button 4: ECM_4_BTN — 0 = out, 1 = in
  - 6. ECM Module Control Button 5: ECM_5_BTN — 0 = out, 1 = in
  - 6. ECM Module Control Button (unmarked): ECM_6_BTN — 0 = out, 1 = in
  - 6. ECM Module Control Button FRM: ECM_FRM_BTN — 0 = out, 1 = in
  - 6. ECM Module Control Button SPL: ECM_SPL_BTN — 0 = out, 1 = in
- DCS-BIOS controls not in PANELS.md
  - HIDE_STICK — 0 = off, 1 = on
  - AIR_SOURCE_KNB (deprecated, not used; the AIR COND page uses AIR_SOURCE_KNOB, which has a known order) — 0 = OFF, 1 = NORM, 2 = DUMP, 3 = RAM, 4 = unknown

99 identifiers have a guessed position order.

### Gaps

Every row without a DCS-BIOS identifier in the sections above, grouped by its gap (55 rows).

#### keybind (15)

- Side Stick Controller (SSC): 1. Weapon Release Button
- Side Stick Controller (SSC): 2. Trim Switch (4-way)
- Side Stick Controller (SSC): 3. Trigger (2-position)
- Side Stick Controller (SSC): 4. Missile Step Button
- Side Stick Controller (SSC): 5. Target Management Switch (TMS) (4-way)
- Side Stick Controller (SSC): 6. Display Management Switch (DMS) (4-way)
- Side Stick Controller (SSC): 7. Countermeasures Management Switch (CMS) (4-way)
- Side Stick Controller (SSC): 8. Paddle Switch
- Side Stick Controller (SSC): 9. Expand / FOV Button
- Throttle: 1. UHF VHF Transmit Switch (4-way)
- Throttle: 2. MAN RNG / UNCAGE Knob
- Throttle: 3. DOG FIGHT Switch (3-position)
- Throttle: 4. ANT ELEV Knob
- Throttle: 5. RDR CURSOR / ENABLE Switch
- Throttle: 6. SPD BRK Switch (3-position, aft momentary)

#### export (3)

- Head-Up Display (HUD): Combining glass
- Multi-Function Display (MFD) bezel: Screen
- Threat Warning Azimuth Indicator: Azimuth scope

#### not exported (19)

- Throttle: Throttle Cutoff Release
- Electronic Horizontal Situation Indicator (EHSI): 1. Bearing pointer
- Electronic Horizontal Situation Indicator (EHSI): 5. Magnetic heading compass
- Electronic Horizontal Situation Indicator (EHSI): 6. Heading marker
- Electronic Horizontal Situation Indicator (EHSI): 7. Course pointer
- Electronic Horizontal Situation Indicator (EHSI): 8. To-From indicator
- Electronic Horizontal Situation Indicator (EHSI): 10. Course deviation indicator
- Electronic Horizontal Situation Indicator (EHSI): 11. New mode indicator
- Electronic Horizontal Situation Indicator (EHSI): 18. Warning display area
- Electronic Horizontal Situation Indicator (EHSI): 19. CDI flag
- Pilot Fault List Display (PFLD): Fault list window
- Mechanical Clock: 1. "Day" hand
- AVTR Control Panel: AVTR panel controls
- Manual Canopy Control Handcrank: Manual canopy handcrank
- ANTI-G TEST Button: ANTI-G TEST button
- Other right console fittings: Utility Light
- Other right console fittings: Arm Rest
- Other right console fittings: DTU Receptacle
- Ejection Seat Controls: Emergency Manual Chute Lever

#### no function in DCS (18)

- Standby Attitude Indicator (SAI): 4. Roll indicator scale
- Airspeed and Mach Indicator: 2. Indicated airspeed scale
- Altimeter: 1. Altitude scale
- Angle-of-Attack (AoA) Indicator: 1. AoA scale tape
- Angle-of-Attack (AoA) Indicator: 3. High AoA region marker
- Angle-of-Attack (AoA) Indicator: 4. Optimal AoA region marker
- Angle-of-Attack (AoA) Indicator: 5. Low AoA region marker
- Vertical Velocity Indicator (VVI): 1. Vertical velocity tape
- Vertical Velocity Indicator (VVI): 3. Positive region marker
- Vertical Velocity Indicator (VVI): 4. Negative region marker
- Attitude Director Indicator (ADI): 3. Pitch scale
- Attitude Director Indicator (ADI): 5. Glideslope deviation scale
- Attitude Director Indicator (ADI): 6. Aircraft symbol (waterline)
- Attitude Director Indicator (ADI): 9. Lower bank angle scale
- Electronic Horizontal Situation Indicator (EHSI): 2. Lubber lines
- Electronic Horizontal Situation Indicator (EHSI): 9. Course deviation scale
- Electronic Horizontal Situation Indicator (EHSI): 12. Aircraft symbol
- NUCLEAR CONSENT Switch: NUCLEAR CONSENT switch

### Cold start coverage

Every row of [STARTUP.md](STARTUP.md) looked up by Panel and Control in the sections above (a Control cell naming several controls counts as one row; "(whole panel)" is checked against all rows of that panel). Rows marked "(not in PANELS.md)" have no PANELS.md row to look up. The sequence has 117 steps.

- **62 fully possible from the dashboard via DCS-BIOS**: every control of the step has an identifier with `read + command` (the check, if any, is a lamp or gauge that is readable too).
- **36 only a check**: the step only reads a lamp, gauge or text; every control has a `read only` identifier.
- **6 need a keybind**: the step moves a HOTAS control or the throttle lever.
- **12 have no identifier**: ground crew or radio steps that are not cockpit controls, stick movement, the HMCS alignment, controls the manual does not name and the HUD picture.
- **1 names an OSB without its number**: the identifier family is known (MFD_L_1 … MFD_L_20 and MFD_R_1 … MFD_R_20), the key is not.
- Total 117.

The `read only` (check) rows are #2, #4, #5, #6, #7, #10, #11, #12, #13, #14, #15, #21, #22, #23, #24, #26, #27, #28, #30, #31, #32, #33, #34, #35, #36, #37, #50, #61, #65, #68, #77, #97, #102, #103, #104, #105. Of these #31, #50 and #77 need a note: #31 reads the fuel flow through three counter drums (FUELFLOWCOUNTER_100, _1K, _10K, `likely`), #50 reads the DED text lines (opening the TIME page is not stated) and #77 reads HYDRAZIN_VOLUME (`likely`).

#### Fully possible rows with a caveat

- STARTUP #25: Throttle / Throttle lever, advance from OFF to IDLE — THROTTLE_OFF_IDLE (`likely`, `read + command`); only the OFF to IDLE move, the rest of the lever travel is a keybind.
- STARTUP #70: FUEL QTY SEL Panel / 1. FUEL QTY SEL Knob, TEST — FUEL_QTY_SEL_T_KNB is NO READBACK (see above); the gauges and lamps checked in #70 to #76 are readable.
- STARTUP #49: AVIONICS POWER Control Panel / 7. DL Switch — DL_SW exists; the manual says the function is not implemented.
- STARTUP #79: MFD Format Selection Master Menu / 12. DTE Format — OSB 8 (MFD_L_8 or MFD_R_8); the master menu page itself is opened with a format select OSB (OSB 12 to 14).
- STARTUP #111: UHF Backup Control Panel (whole panel) — all 13 controls have identifiers; the A-3-2 knob (UHF_FREQ_100_KNB) and the four manual frequency knobs are `likely` matches, and several position orders are guesses.
- STARTUP #3, #8, #64, #91, #92, #101 and #106: switches that PANELS.md lists as spring-loaded or momentary; DCS-BIOS defines FLCS_PWR_TEST_SW as spring-loaded but BIT_SW, MANUAL_PITCH_SW and EPU_GEN_TEST_SW as plain toggles, so the spring-back of these three is not part of the DCS-BIOS definition (check in DCS).

#### Rows that need a keybind (6)

- STARTUP #60: Throttle lever to MIL and back to IDLE: only the OFF to IDLE move has an identifier (THROTTLE_OFF_IDLE)
- STARTUP #67: Throttle / 6. SPD BRK Switch: keybind
- STARTUP #86: Side Stick Controller / 2. Trim Switch (4-way): keybind (the trim wheel indicators ROLLTRIMIND and PITCHTRIMIND can be read)
- STARTUP #88: Side Stick Controller / 2. Trim Switch (4-way): keybind (the trim wheel indicators ROLLTRIMIND and PITCHTRIMIND can be read)
- STARTUP #100: Throttle lever to 10 percent above idle: no identifier for lever travel
- STARTUP #107: Throttle lever back to IDLE: no identifier for lever travel

#### Rows with an OSB but no number (1)

- STARTUP #80: Multi-Function Display (MFD) bezel / DTC upload OSB (number not stated) — `read + command`; which key is not stated (MFD_L_1 … MFD_L_20 / MFD_R_1 … MFD_R_20).

#### Rows without an identifier (12)

- STARTUP #16: Communications / Radio calls (not in PANELS.md): not a cockpit control
- STARTUP #18: Ground crew / Chocks (not in PANELS.md): not a cockpit control
- STARTUP #19: Ground crew / Ground crew position (not in PANELS.md): not a cockpit control
- STARTUP #63: Side Stick Controller (SSC) / Stick movement (not in PANELS.md): no DCS-BIOS control for stick movement (HIDE_STICK only hides the stick model)
- STARTUP #78: Avionics, MFDs and radios / Controls not named (not in PANELS.md): controls not named by the manual
- STARTUP #81: HMCS Control Panel / HMCS alignment (not in PANELS.md): no DCS-BIOS control for the alignment (HMCS_INT_KNB is only the brightness knob)
- STARTUP #83: Side Stick Controller (SSC) / Stick movement (not in PANELS.md): see #63
- STARTUP #90: Side Stick Controller (SSC) / Stick movement (not in PANELS.md): see #63
- STARTUP #93: Side Stick Controller (SSC) / Stick movement (not in PANELS.md): see #63
- STARTUP #94: Side Stick Controller (SSC) / Stick movement (not in PANELS.md): see #63
- STARTUP #114: Head-Up Display (HUD) / Combining glass: export (the HUD picture has no DCS-BIOS output)
- STARTUP #117: Ground crew / Chocks (not in PANELS.md): not a cockpit control
