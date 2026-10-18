# A-10C II – DCS-BIOS mapping

Maps every control in [PANELS.md](PANELS.md) to its DCS-BIOS identifier. Source: the DCS-Skunkworks DCS-BIOS module `A-10C` (`Scripts/DCS-BIOS/lib/modules/aircraft_modules/A-10C.lua`, commit 11c6209 of 2026-10-08), which serves both the A-10C and the A-10C II (`A-10C_2`). The module has 749 controls.

Sections and control names follow PANELS.md. Columns:

- **DCS-BIOS identifier**: the name used to read and command the control; `—` if there is none.
- **Access**: `read + command` (an output and an input exist), `read only` (lamps, gauges, text: `defineIndicatorLight`, `defineFloat`, `defineString`, `define8BitFloat`, `defineBitFromDrawArgument`, `defineFloatFromDrawArgument`, `defineIntegerFromGetter`), or `—`.
- **Note**: the DCS-BIOS description or positions where they differ from PANELS.md, `likely` when the match is by meaning rather than by name, and for controls without an identifier the gap: `keybind` (needs a DCS key), `export` (needs the export script), `no function in DCS`, or `not exported`.

## Control stick and throttles (HOTAS)

### Control Stick (p. 106)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Master Mode Control Button (MMCB) | — | — | keybind |
| 2. Data Management Switch (DMS) | — | — | keybind |
| 3. Target Management Switch (TMS) | — | — | keybind |
| 4. Nosewheel Steering (NWS) Button | — | — | keybind |
| 5. Countermeasures Switch (CMS) | — | — | keybind |
| 6. Weapon Release Button | — | — | keybind |
| 7. Trim Switch | — | — | keybind |
| 8. Trigger | — | — | keybind |

### Throttles (p. 111)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Left throttle lever | ENG_THROTTLE_L | read only | Lever position only; no input |
| Right throttle lever | ENG_THROTTLE_R | read only | Lever position only; no input |
| 1. Mic Switch | — | — | keybind |
| 2. Speed Brake | — | — | keybind |
| 3. Boat Switch | — | — | keybind |
| 4. China Hat | — | — | keybind |
| 5. Pinky Switch | — | — | keybind |
| 6. Left Throttle Button | — | — | keybind |
| 7. Slew Control | — | — | keybind |
| 8. Coolie Hat | — | — | keybind |

## Left front dash

### Left Engine "T-Handle" Fire Extinguisher Discharge Select (p. 114)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Left engine T-handle | FIRE_LENG_PULL | read + command | Left Engine Fire T-Handle |
| Left engine fire lamp | L_ENG_FIRE | read only | Left Engine Fire Indicator (yellow) |

### Radar Warning Receiver (RWR) Display (p. 115)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Azimuth indicator | — | — | export |
| (DCS-BIOS only) Display Brightness | RWR_BRT | read + command | RWR display brightness knob |

### Airspeed Indicator (p. 116)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Current airspeed pointer | AIRSPEED_NEEDLE | read only | Airspeed Needle |
| Maximum speed pointer | AIRSPEED_MAX_IAS | read only | Airspeed Max IAS Dial |
| Decimals drum | AIRSPEED_DIAL | read only | likely; described as Airspeed Dial |

### Standby Attitude Indicator (SAI) (p. 117)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Attitude display | SAI_PITCH, SAI_BANK | read only | Pitch and bank as separate outputs |
| OFF warning flag | SAI_WARNING_FLAG | read only | SAI Warning Flag |
| Cage knob (PULL TO CAGE) | SAI_CAGE, SAI_PITCH_TRIM | read + command | Pull is SAI_CAGE; turn is SAI_PITCH_TRIM |
| (DCS-BIOS only) SAI Manual Pitch Adjustment | SAI_PITCH_ADJ | read only | Knob turn position as output |
| (DCS-BIOS only) SAI Knob Arrow | SAI_KNOB_ARROW | read only | Knob arrow position as output |

### UHF Frequency Repeater (p. 118)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| UHF preset frequency readout | UHF_PRESET, UHF_FREQUENCY | read only | likely; ARC-164 panel display values, no separate repeater |

### Angle of Attack Indicator (p. 118)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Angle of attack pointer | AOA_UNITS | read only | AOA Units |
| OFF warning flag | AOA_PWROFF | read only | AOA Poweroff Flag |

### Digital Clock (p. 119)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Time readout | CLOCK_HH, CLOCK_MM, CLOCK_SS, CLOCK_ETC | read only | Text fields; CLOCK_ETC gives ET or C mode letters |
| Digital second hand | CLOCK_SS | read only | likely; seconds as text, no ring segments |
| SEL button (1) | CLOCK_SET | read + command | likely; DCS-BIOS calls it Clock SET |
| CTRL button (2) | CLOCK_CTRL | read + command | Clock CTRL |

### Emergency Jettison Button (p. 120)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| EXT STORES JETT button | EXT_STORES_JETTISON | read + command | External Stores Jettison Button |

### Left Multifunction Color Display (MFCD) (p. 121)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Screen | — | — | export |
| OSB 1 to 5 | LMFD_01 … LMFD_05 | read + command | Push buttons named by OSB number |
| OSB 6 to 10 | LMFD_06 … LMFD_10 | read + command | Push buttons named by OSB number |
| OSB 11 to 15 | LMFD_11 … LMFD_15 | read + command | Push buttons named by OSB number |
| OSB 16 to 20 | LMFD_16 … LMFD_20 | read + command | Push buttons named by OSB number |
| ADJ rocker | LMFD_ADJ | read + command | States 0 to 2: down, center, up |
| DSP rocker | LMFD_DSP | read + command | Defined in DCS-BIOS although PANELS says no function |
| CON rocker | LMFD_CON | read + command | Defined in DCS-BIOS although PANELS says no function |
| BRT rocker | LMFD_BRT | read + command | States 0 to 2: down, center, up |
| SYM rocker | LMFD_SYM | read + command | Defined in DCS-BIOS although PANELS says no function |
| Day / night / off select | LMFD_PWR | read + command | PWR OFF - NT - DAY |

### Landing Gear and Flap Control Panel (p. 125)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Landing lights switch (LIGHTS LAND) | LANDING_LIGHTS | read + command | Positions TAXI / OFF / LAND |
| 2. Downlock solenoid override button | DOWNLOCK_OVERRIDE | read + command | Downlock Override Button |
| 3. Landing gear handle (LGD GEAR DOWN) | GEAR_LEVER | read + command | Gear Lever DOWN - UP |
| Gear handle lamp | HANDLE_GEAR_WARNING | read only | Handle Gear Warning Light (red) |
| 4. Anti-skid switch | ANTI_SKID_SWITCH | read + command | Electrically held switch |
| 5. L SAFE gear light | GEAR_L_SAFE | read only | Left Gear Safe (green) |
| 5. N SAFE gear light | GEAR_N_SAFE | read only | Nose Gear Safe (green) |
| 5. R SAFE gear light | GEAR_R_SAFE | read only | Right Gear Safe (green) |
| 6. Flap position indicator (FLAPS DEGREES) | FLAP_POS | read only | Flap Position Indicator |
| 7. TEMS DATA switch | ENGINE_TEMS_DATA | read + command | TEMS Data; PANELS says no function in DCS |
| (DCS-BIOS only) Landing Gear Horn Silence | GEAR_HORN_SILENCE | read + command | Push button |

### Armament HUD Control Panel (AHCP) (p. 129)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. MASTER | AHCP_MASTER_ARM | read + command | TRAIN - SAFE - ARM |
| 2. GUN/PAC | AHCP_GUNPAC | read + command | GUNARM - SAFE - ARM |
| 3. LASER | AHCP_LASER_ARM | read + command | TRAIN - SAFE - ARM |
| 4. TGP | AHCP_TGP | read + command | TGP OFF - ON |
| 5. ALT SCE | AHCP_ALT_SCE | read + command | RADAR - DELTA - BARO |
| 6. HUD MODE day/night | AHCP_HUD_DAYNIGHT | read + command | NIGHT - DAY |
| 6. HUD MODE norm/standby | AHCP_HUD_MODE | read + command | STBY - NORM |
| 7. CICU | AHCP_CICU | read + command | CICU OFF - ON |
| 8. JTRS | AHCP_JTRS | read + command | JTRS OFF - ON |
| 9. IFFCC | AHCP_IFFCC | read + command | OFF - TEST - ON |

### Heading Attitude Reference (HARS) Fast Erect Button (p. 133)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| HARS FAST ERECT button | HARS_FAST_ERECT | read + command | HARS Fast Erect Button |

### Gun and Nose Wheel Steering (NWS) Lights (p. 134)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| GUN READY light | GUN_READY | read only | GUN READY Indicator (green) |
| STEERING ENGAGED light | NOSEWHEEL_STEERING | read only | likely; Nosewheel Steering Indicator (green) |

## Center front dash

### APU "T Handle" Fire Extinguisher Discharge Select (p. 136)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| APU T-handle | FIRE_APU_PULL | read + command | APU Fire T-Handle |
| APU fire lamp | APU_FIRE | read only | APU Fire Indicator (yellow) |

### Countermeasures Set Control (CMSC) (p. 136)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Upper arrow button | CMSC_JMR | read + command | likely; Select Jammer Program |
| Lower arrow button | CMSC_MWS | read + command | likely; Select MWS Programs (No Function) |
| JMR window | CMSC_TXT_JMR | read only | JMR Status Display, text of 8 characters |
| MWS window | CMSC_TXT_MWS | read only | MWS Status Display, text of 8 characters |
| CHAFF / FLARE window | CMSC_TXT_CHAFF_FLARE | read only | One text field for both counts, 8 characters |
| Left RWR-area lamp | CMSC_PRIO | read only | likely; Priority Status Indicator (green) |
| Right RWR-area lamp | CMSC_UNKN | read only | likely; Unknown Status Indicator (green) |
| RWR PRI button | CMSC_PRI | read + command | Toggle between 5 and 16 priority threats |
| RWR SEP button | CMSC_SEP | read + command | Separate RWR Symbols |
| RWR UNK button | CMSC_UNK | read + command | Display Unknown Threats |
| BRT knob | CMSC_BRT | read + command | Adjust Display Brightness |
| AUD knob | CMSC_RWR_VOL | read + command | likely; Adjust RWR Volume |
| ML lamp | CMSC_LAUNCH | read only | likely; Missile Launch Indicator (red) |

### Attitude Director Indicator (ADI) (p. 137)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Attitude sphere | ADI_PITCH, ADI_BANK | read only | Pitch and bank as separate outputs |
| 2. Miniature aircraft | ADI_PITCH_TRIM | read + command | likely; marker offset is the pitch trim position |
| 3. Bank scale | — | — | no function in DCS; fixed scale |
| 3. Bank pointer | ADI_BANK | read only | likely; pointer rides with the sphere |
| 4. Slip ball | ADI_SLIP | read only | ADI Slipball Position |
| 4. Turn indicator | ADI_TURN | read only | ADI Turn Needle |
| 5. Pitch trim knob | ADI_PITCH_TRIM | read + command | ADI Pitch Trim |
| 5. Pitch trim index | — | — | no function in DCS; fixed marker |
| 6. Course warning flag | ADI_CRSWARN_FLAG | read only | ADI Course Warning Flag |
| 7. Bank steering bar | ADI_STEER_BANK | read only | ADI Bank Steering Bar |
| 8. Pitch steering bar | ADI_STEER_PITCH | read only | ADI Pitch Steering Bar |
| 9. Glide slope warning flag | ADI_GSWARN_FLAG | read only | ADI Glide Slope Warning Flag |
| 10. Glide slope deviation scale | — | — | no function in DCS; fixed scale |
| 10. Glide slope indicator | ADI_GS | read only | ADI Glide Slope Indicator |
| 11. Attitude warning flag (OFF) | ADI_ATTWARN_FLAG | read only | ADI Attitude Warning Flag |

### Horizontal Situation Indicator (HSI) (p. 139)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Power OFF flag | HSI_PWROFF_FLAG | read only | HSI Poweroff Flag |
| 2. Compass card | HSI_HDG | read only | HSI Heading |
| 3. Aircraft symbol | — | — | no function in DCS; fixed symbol |
| 4. Lubber line | — | — | no function in DCS; fixed line |
| 5. Range indicator | HSI_RC_A … HSI_RC_D, HSI_RANGE_FLAG | read only | Four digit counters; HSI_RANGE_FLAG is the unpowered flag |
| 6. Bearing pointer 2 | HSI_BEARING2 | read only | HSI Bearing Pointer 2 |
| 7. Bearing pointer 1 | HSI_BEARING1 | read only | HSI Bearing Pointer 1 |
| 8. Heading set knob | HSI_HDG_KNOB | read + command | Heading Select Knob |
| 9. Heading marker | HSI_HDG_BUG | read only | HSI Heading Bug |
| 10. Bearing validity flag | HSI_BEARING_FLAG | read only | HSI Bearing Flag |
| 11. Course set knob | HSI_CRS_KNOB | read + command | Course Select Knob |
| 12. Course selector window | HSI_CC_A, HSI_CC_B | read only | Course Counter A and B as separate outputs |
| 13. Course arrow | HSI_CRS | read only | HSI Course |
| 14. Course deviation indicator (CDI) | HSI_DEVIATION | read only | HSI Deviation |
| 15. To-From indicator | HSI_TOFROM1, HSI_TOFROM2 | read only | HSI TO/FROM 1 and 2 as separate outputs |

### Navigation Mode Select Panel (NMSP) (p. 140)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. HARS button | NMSP_HARS_BTN, NMSP_HARS_LED | read + command | Button plus green triangle LED |
| 10. PTR switch | NMSP_ABLE_STOW | read + command | Able/Stow Localizer Bars |
| 2. EGI button | NMSP_EGI_BTN, NMSP_EGI_LED | read + command | Button plus green triangle LED |
| 3. TISL button | NMSP_TISL_BTN, NMSP_TISL_LED | read + command | Button plus LED; DCS-BIOS marks the button No Function |
| 4. STR PT button | NMSP_STEERPT_BTN, NMSP_STEERPT_LED | read + command | likely; DCS-BIOS calls it STEERPT |
| 5. ANCHR button | NMSP_ANCHR_BTN, NMSP_ANCHR_LED | read + command | Button plus green triangle LED |
| 6. TCN button | NMSP_TCN_BTN, NMSP_TCN_LED | read + command | Button plus green triangle LED |
| 7. ILS button | NMSP_ILS_BTN, NMSP_ILS_LED | read + command | Button plus green triangle LED |
| 8. UHF homing light | NMSP_UHF_LED | read only | UHF LED (green) |
| 9. FM homing light | NMSP_FM_LED | read only | FM LED (green) |

### Target Identification Set Laser (TISL) control panel (p. 136)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| MODE select | TISL_MODE | read + command | TISL Mode, 5 positions |
| SLANT RNG MILES switch | TISL_SLANT_RANGE | read + command | UNDER 5 - 5 - 10; reverse order of PANELS |
| ALT ABV TST window | TISL_ALT_10000, TISL_ALT_1000 | read + command | Digit drums for the 10000 ft and 1000 ft digits |
| ENTER button | TISL_ENTER, TISL_ENTER_L | read + command | Button plus its light |
| + button | TISL_OVERTEMP, TISL_OVERTEMP_L | read + command | likely; second of four, DCS-BIOS calls it OVER TEMP |
| BITE button | TISL_BITE, TISL_BITE_L | read + command | Button plus its light |
| Fourth button | TISL_TRACK, TISL_TRACK_L | read + command | likely; fourth of four, DCS-BIOS calls it TRACK |
| CODE SELECT | TISL_CODE1 … TISL_CODE4 | read + command | Four code wheels, 20 steps each in half digits |
| TISL / BOTH / AUX switch | TISL_AUX | read + command | TISL AUX Switch, 3 positions |

## Right dash

### Fire Extinguisher Discharge (p. 144)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| FIRE EXTING DISCH switch | FIRE_EXT_DISCH | read + command | Positions Left / Off / Right |

### Right Multifunction Color Display (MFCD) (p. 144)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Screen | — | — | export |
| OSB 1 to 5 | RMFD_01 … RMFD_05 | read + command | Push buttons named by OSB number |
| OSB 6 to 10 | RMFD_06 … RMFD_10 | read + command | Push buttons named by OSB number |
| OSB 11 to 15 | RMFD_11 … RMFD_15 | read + command | Push buttons named by OSB number |
| OSB 16 to 20 | RMFD_16 … RMFD_20 | read + command | Push buttons named by OSB number |
| ADJ rocker | RMFD_ADJ | read + command | States 0 to 2: down, center, up |
| DSP rocker | RMFD_DSP | read + command | Defined in DCS-BIOS although PANELS says no function |
| CON rocker | RMFD_CON | read + command | Defined in DCS-BIOS although PANELS says no function |
| BRT rocker | RMFD_BRT | read + command | States 0 to 2: down, center, up |
| SYM rocker | RMFD_SYM | read + command | Defined in DCS-BIOS although PANELS says no function |
| Day / night / off select | RMFD_PWR | read + command | PWR OFF - NT - DAY |

### Fuel Quantity and Hydraulic Indicator Panel (p. 146)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 2. Fuel quantity gauge, left pointer | FUEL_QTY_L | read only | Fuel Qty Left |
| 2. Fuel quantity gauge, right pointer | FUEL_QTY_R | read only | Fuel Qty Right |
| 2. Total fuel readout | FUEL_QTY_10000, FUEL_QTY_1000, FUEL_QTY_100 | read only | Counters for the 10000, 1000 and 100 lb digits |
| 3. Fuel display selector | FQIS_SELECT | read + command | Fuel Display Selector, 5 positions |
| Test button | FQIS_TEST | read + command | Fuel Gauge Test |
| 4. Hydraulic pressure gauge, left (HYD SYS L) | L_HYD_PRESS | read only | Left Hydraulic Pressure |
| 4. Hydraulic pressure gauge, right (HYD SYS R) | R_HYD_PRESS | read only | Right Hydraulic Pressure |

### RIGHT Engine "T Handle" Fire Extinguisher Discharge Select (p. 147)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Right engine T-handle | FIRE_RENG_PULL | read + command | Right Engine Fire T-Handle |
| Right engine fire lamp | R_ENG_FIRE | read only | Right Engine Fire Indicator (yellow) |

### Marker and Canopy Lights (p. 148)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| MARKER BEACON light | MARKER_BEACON | read only | MARKER BEACON Indicator (green) |
| CANOPY UNLOCKED light | CANOPY_UNLOCKED | read only | CANOPY UNLOCKED Indicator (green) |

### Vertical Velocity Indicator (VVI) (p. 148)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Climb rate pointer | VVI | read only | Vertical Velocity Indicator |

### Altimeter (p. 149)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Altitude pointer | ALT_100FT | read only | 100 ft Pointer |
| Altitude counter | ALT_10000FT_CNT, ALT_1000FT_CNT, ALT_100FT_CNT | read only | Counters for the 10000, 1000 and 100 ft digits |
| Pressure setting window | ALT_PRESSURE0 … ALT_PRESSURE3 | read only | Barometric Pressure Digit 0 to 3 |
| 1. Pressure set knob | ALT_SET_PRESSURE | read + command | Set Pressure |
| 2. ELECT/PNEU switch | ALT_ELECT_PNEU | read + command | Spring-loaded, states 0 to 2; PANELS lists only ELECT and PNEU |
| (DCS-BIOS only) PNEU Flag | ALT_PNEU_FLAG | read only | PNEU Flag as output |

### Engine Monitoring Instruments (EMI) (p. 150)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Left oil pressure | L_OIL_PRESS | read only | Left Oil Pressure |
| 1. Right oil pressure | R_OIL_PRESS | read only | Right Oil Pressure |
| 2. Left core speed | L_ENG_CORE, L_ENG_CORE_T | read only | likely; Tenth output is the small inset pointer |
| 2. Right core speed | R_ENG_CORE, R_ENG_CORE_T | read only | likely; Tenth output is the small inset pointer |
| 3. Left fan speed | L_ENG_FAN | read only | Left Engine Fan Speed |
| 3. Right fan speed | R_ENG_FAN | read only | Right Engine Fan Speed |
| 4. Left ITT | L_ENG_TEMP, L_ENG_TEMP_T | read only | likely; Tenth output is the small inset pointer |
| 4. Right ITT | R_ENG_TEMP, R_ENG_TEMP_T | read only | likely; Tenth output is the small inset pointer |
| 5. Left fuel flow | L_ENG_FUEL_FLOW | read only | Left Engine Fuel Flow |
| 5. Right fuel flow | R_ENG_FUEL_FLOW | read only | Right Engine Fuel Flow |
| 7. APU RPM | APU_RPM | read only | APU RPM Gauge |
| 6. APU EGT | APU_TEMP | read only | likely; described as APU Temperature Gauge |
| (DCS-BIOS only) Left ITT OFF flag | L_ENG_TEMP_OFF | read only | Left Engine Temperature Off |
| (DCS-BIOS only) Right ITT OFF flag | R_ENG_TEMP_OFF | read only | Right Engine Temperature Off |

## Above the dash

### Heads Up Display Area Above Dash (p. 152)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 3. Heads-Up Display (HUD) | — | — | export |
| 4. Up-Front Controller (UFC) | — | — | mapped in the UFC section |

### Standby Compass (p. 153)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Compass card | COMPASS_HDG, COMPASS_PITCH, COMPASS_BANK | read only | Heading plus tilt as pitch and bank outputs |

### Air Refuel Status Lights (p. 153)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| READY light | AIR_REFUEL_READY | read only | Air Refuel READY Light (green) |
| LATCHED light | AIR_REFUEL_LATCHED | read only | Air Refuel LATCHED Light (green) |
| DISCONNECT light | AIR_REFUEL_DISCONNECT | read only | Air Refuel DISCONNECT Light (green) |

### Accelerometer (G-meter) (p. 154)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| G pointer | ACCEL_G | read only | G Load |
| PUSH TO SET button | ACCEL_PTS | read + command | Accelerometer Button |
| (DCS-BIOS only) Accelerometer Min Pointer | ACCEL_MIN | read only | Minimum G pointer as output |
| (DCS-BIOS only) Accelerometer Max Pointer | ACCEL_MAX | read only | Maximum G pointer as output |

### Angle of Attack Indexer (p. 155)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Low-speed symbol | AOA_INDEXER_HIGH | read only | likely; named by AoA, high AoA is low speed |
| On-speed symbol | AOA_INDEXER_NORMAL | read only | AOA Indexer Normal (green) |
| High-speed symbol | AOA_INDEXER_LOW | read only | likely; named by AoA, low AoA is high speed |
