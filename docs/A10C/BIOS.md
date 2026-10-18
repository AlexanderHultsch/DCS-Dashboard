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

## Left console

### Fuel System Control Panel (p. 158)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Main boost pump switch, left | FSCP_BOOST_MAIN_L | read + command | Boost Pumps Main Fuselage Left |
| 1. Main boost pump switch, right | FSCP_BOOST_MAIN_R | read + command | Boost Pumps Main Fuselage Right |
| 2. Wing boost pump switch, left | FSCP_BOOST_WING_L | read + command | Boost Pumps Left Wing |
| 2. Wing boost pump switch, right | FSCP_BOOST_WING_R | read + command | Boost Pumps Right Wing |
| 3. EXT TKS switch, WING | FSCP_EXT_TANKS_WING | read + command | External Wing Tanks Boost Pumps |
| 3. EXT TKS switch, FUS | FSCP_EXT_TANKS_FUS | read + command | External Fuselage Tanks Boost Pumps |
| 4. Crossfeed switch | FSCP_CROSSFEED | read + command | Crossfeed |
| 5. Tank gate switch (TK GATE) | FSCP_TK_GATE | read + command | Tank Gate |
| 7. Air refuel control lever (RCVR) | FSCP_RCVR_LEVER | read + command | Aerial Refueling Slipway Control Lever |
| 8. Fill disable button, wing left | FSCP_FD_WING_L | read + command | Fill Disable Wing Left; push button |
| 8. Fill disable button, wing right | FSCP_FD_WING_R | read + command | Fill Disable Wing Right; push button |
| 8. Fill disable button, main left | FSCP_FD_MAIN_L | read + command | Fill Disable Main Left; push button |
| 8. Fill disable button, main right | FSCP_FD_MAIN_R | read + command | Fill Disable Main Right; push button |
| 9. Receiver light dial (RCVR LT) | ALCP_RCVR_LTS | read + command | Refueling Lighting Dial; DCS-BIOS groups it with auxiliary lighting |
| 10. Line check button | FSCP_LINE_CHECK | read + command | Defined in DCS-BIOS although PANELS says no function |
| 11. Signal amplifier switch (SIG AMPL) | FSCP_AMPL | read + command | Defined in DCS-BIOS although PANELS says no function |

### Throttles Panel (p. 160)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. APU switch | ENGINE_APU_START | read + command | APU START |
| 2. Left throttle lever | ENG_THROTTLE_L | read only | Lever position only; no input |
| 2. Right throttle lever | ENG_THROTTLE_R | read only | Lever position only; no input |
| 3. Engine fuel flow switch, left | ENGINE_FUEL_FLOW_L | read + command | Fuel Flow L |
| 3. Engine fuel flow switch, right | ENGINE_FUEL_FLOW_R | read + command | Fuel Flow R |
| 4. Engine operate switch, left | ENGINE_OPER_L | read + command | ENG OPER L; spring-loaded, states 0 to 2 |
| 4. Engine operate switch, right | ENGINE_OPER_R | read + command | ENG OPER R; spring-loaded, states 0 to 2 |
| 5. Landing gear horn silence button (LDG WARN SILENCE) | GEAR_HORN_SILENCE | read + command | also in gear panel section |
| Throttle friction lever | ENGINE_THROTTLE_FRICTION | read + command | Friction Control |

### Flap lever, left of the throttles (p. 156)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| Flap lever | FLAPS_SWITCH | read + command | Flaps Setting DN - MVR - UP; reverse order of PANELS |

### LASTE Control Panel (p. 163)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. EAC switch | LASTE_EAC | read + command | EAC On/Off; electrically held switch |
| 2. Radar altimeter switch (RDR ALTM) | LASTE_RDR_ALTM | read + command | Radar Altimeter |
| 3. Autopilot select switch | LASTE_AP_MODE | read + command | AP MODE, 3 positions |
| 4. Autopilot engage/disengage button | LASTE_AP_TOGGLE | read + command | Autopilot Engage/Disengage |

### AN/ARC-186(V) Radio Control Panel (p. 167)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| TOD SND button | ARC210_TOD_SEND | read + command | Time of Day Send |
| TOD RCV button | ARC210_TOD_REC | read + command | Time of Day Receive |
| GPS button | ARC210_GPS | read + command | GPS |
| RT SELECT button | ARC210_TRANS_REC_SEL | read + command | Select Receiver - Transmitter |
| Line select button 1 (top) | ARC210_FSK_UP | read + command | likely; DCS-BIOS calls it Upper FSK |
| Line select button 2 | ARC210_FSK_MID | read + command | likely; DCS-BIOS calls it Middle FSK |
| Line select button 3 | ARC210_FSK_LOW | read + command | likely; DCS-BIOS calls it Lower FSK |
| Brightness up button | ARC210_BRIGHT_INC | read + command | Brightness Increase |
| Brightness down button | ARC210_BRIGHT_DEC | read + command | Brightness Decrease |
| Screen | ARC210_FREQUENCY, ARC210_FREQ_MHZ, ARC210_FREQ_KHZ | read only | Main frequency as text; other screen fields listed below |
| SQL knob | ARC210_SQUELCH | read + command | likely; Squelch ON/OFF as push button, not knob |
| MENU / TIME button | ARC210_MENU | read + command | Menu Pages |
| XMT/RCV / SEND button | ARC210_TRANS_REC_FUNC | read + command | Transmit / Receive Function Toggle |
| AM/FM button | ARC210_AMP_FREQ_MODUL | read + command | Amplitude / Frequency Modulation Select |
| OFFSET / RCV button | ARC210_OFF_FREQ | read + command | Offset Frequency |
| ENTER button | ARC210_ENTER | read + command | Enter |
| Unlabelled knob 1 (leftmost) | ARC210_100MHZ_SEL | read + command | likely; 100MHz Selector, left to right order assumed |
| Unlabelled knob 2 | ARC210_10MHZ_SEL | read + command | likely; 10MHz Selector, left to right order assumed |
| Unlabelled knob 3 | ARC210_1MHZ_SEL | read + command | likely; 1MHz Selector, left to right order assumed |
| Unlabelled knob 4 | ARC210_100KHZ_SEL | read + command | likely; 100KHz Selector, left to right order assumed |
| Unlabelled knob 5 (rightmost) | ARC210_25KHZ_SEL | read + command | likely; 25KHz Selector, states 00, 25, 50, 75 |
| Left mode dial | ARC210_MASTER | read + command | likely; Master Switch, 7 positions as in PANELS |
| CHANNEL knob | ARC210_CHN_KNB | read + command | Channel Selector Knob, variable step |
| Right mode dial | ARC210_SEC_SW | read + command | likely; Secondary Switch, 7 positions as in PANELS |
| (DCS-BIOS only) EXIT/SEND | ARC210_EXIT_SEND | read only | Screen text of 9 characters |
| (DCS-BIOS only) Transmit/Receive (XMIT/RECV) | ARC210_XMIT_RECV | read only | Screen text of 4 characters |
| (DCS-BIOS only) COMSEC submode (PT/CT/CT-TD) | ARC210_COMSEC_SUBMODE | read only | Screen text of 5 characters |
| (DCS-BIOS only) Active ECCM Channel | ARC210_ACTIVE_ECCM_CHANNEL | read only | Screen text of 2 characters |
| (DCS-BIOS only) SG Time | ARC210_SG_TIME | read only | Screen text of 5 characters |
| (DCS-BIOS only) Previous label | ARC210_PREV | read only | Screen text of 4 characters |
| (DCS-BIOS only) COMSEC menu mode (LOS/DAMA) | ARC210_COMSEC_MENU_MODE | read only | Screen text of 30 characters |
| (DCS-BIOS only) COMSEC mode | ARC210_COMSEC_MODE | read only | Screen text of 11 characters |
| (DCS-BIOS only) More | ARC210_MORE | read only | Screen text of 4 characters |
| (DCS-BIOS only) Load Time | ARC210_LOAD_TIME | read only | Screen text of 9 characters |
| (DCS-BIOS only) KY Submode | ARC210_KY_SUBMODE | read only | Screen text of 1 character |
| (DCS-BIOS only) EXIT/RECV | ARC210_EXIT_RECV | read only | Screen text of 9 characters |
| (DCS-BIOS only) Previous manual frequency | ARC210_PREV_MANUAL_FREQ | read only | Screen text of 7 characters |
| (DCS-BIOS only) Main frequency separator (.) | ARC210_FREQ_DOT_MARK | read only | Screen text of 1 character |
| (DCS-BIOS only) Modulation (AM/FM) | ARC210_MODULATION | read only | Screen text of 2 characters |
| (DCS-BIOS only) Selected RT | ARC210_SELECTED_RT | read only | Screen text of 3 characters |
| (DCS-BIOS only) EXIT/LOAD | ARC210_EXIT_LOAD | read only | Screen text of 9 characters |
| (DCS-BIOS only) Active Channel | ARC210_ACTIVE_CHANNEL | read only | Screen text of 2 characters |
| (DCS-BIOS only) Active Channel (WOD Page) | ARC210_VERIFY_WOD_ACTIVE_CHANNEL | read only | Screen text of 2 characters |
| (DCS-BIOS only) Active Channel (TR_PRSET Page) | ARC210_TR_PRSET_ACTIVE_CHANNEL | read only | Screen text of 2 characters |
| (DCS-BIOS only) ARC-210 Present | ARC210_PRESENT | read only | 1 when the ARC-210 is installed |

### AN/ARC-164 UHF Radio Control Panel (p. 168)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Preset channel selector | UHF_PRESET_SEL | read + command | UHF Preset Channel Selector, 20 steps |
| 2. Preset channel indicator window | UHF_PRESET | read only | UHF Preset Display |
| 3. Frequency status indicator window | UHF_FREQUENCY | read only | UHF Frequency Display |
| 4. 100 MHz selector | UHF_100MHZ_SEL | read + command | States 0 to 2: 2, 3, A |
| 5. 10 MHz selector | UHF_10MHZ_SEL | read + command | UHF 10MHz Selector |
| 6. 1 MHz selector | UHF_1MHZ_SEL | read + command | UHF 1MHz Selector |
| 7. 0.1 MHz selector | UHF_POINT1MHZ_SEL | read + command | UHF 0.1MHz Selector |
| 8. 0.025 MHz selector | UHF_POINT25_SEL | read + command | likely; described as 0.25MHz, steps 00, 25, 50, 75 |
| 9. Frequency mode dial | UHF_MODE | read + command | MNL / PRESET / GRD |
| 10. Function dial | UHF_FUNCTION | read + command | OFF / MAIN / BOTH / ADF |
| 11. Volume knob (VOL) | UHF_VOL | read + command | UHF Volume Control |
| 12. T-tone control (T TONE) | UHF_T_TONE | read + command | Defined in DCS-BIOS although PANELS says no function |
| 13. Squelch control | UHF_SQUELCH | read + command | Squelch Switch |
| 14. LOAD button under the preset cover | UHF_LOAD, UHF_COVER | read + command | Button plus its cover |
| TEST DISPLAY button | UHF_TEST | read + command | Display Test Button |
| STATUS button | UHF_STATUS | read + command | Status Button |

### AN/ARC-186(V) VHF FM Radio 2 Control Panel (p. 171)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Preset channel selector wheel | VHFFM_PRESET | read + command | Preset Channel Selector; step up or down only |
| 2. Preset channel indicator window | VHFFM_PRESET | read + command | likely; same control as the wheel, output also gives label |
| 3. Frequency selector knob 1 (leftmost) | VHFFM_FREQ1 | read + command | Frequency Selector 1; step up or down only |
| 3. Frequency selector knob 2 | VHFFM_FREQ2 | read + command | Frequency Selector 2; step up or down only |
| 3. Frequency selector knob 3 | VHFFM_FREQ3 | read + command | Frequency Selector 3; step up or down only |
| 3. Frequency selector knob 4 | VHFFM_FREQ4 | read + command | Frequency Selector 4; states 00, 25, 50, 75 |
| Frequency windows | VHF_FM_FREQUENCY_S | read only | VHF FM Frequency (String), 7 characters |
| 4. Load button | VHFFM_LOAD | read + command | Load Button |
| 5. Volume knob (VOL) | VHFFM_VOL | read + command | VHF FM Volume Control |
| 6. Frequency mode dial | VHFFM_MODE | read + command | OFF / TR / DF |
| 7. Frequency selection dial | VHFFM_FREQEMER | read + command | FM / AM / MAN / PRE |
| 8. Squelch switch | VHFFM_SQUELCH | read + command | Squelch, 3 positions |
| (DCS-BIOS only) Frequency Selector 1 Rotation | VHFFM_FREQ1_ROT | read only | Knob turn position as output |
| (DCS-BIOS only) Frequency Selector 2 Rotation | VHFFM_FREQ2_ROT | read only | Knob turn position as output |
| (DCS-BIOS only) Frequency Selector 3 Rotation | VHFFM_FREQ3_ROT | read only | Knob turn position as output |
| (DCS-BIOS only) Frequency Selector 4 Rotation | VHFFM_FREQ4_ROT | read only | Knob turn position as output |

### KY-58 Secure Voice Control Panel (p. 173)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Power switch | KY58_PWR | read + command | Power Switch; PANELS says panel has no function |
| 2. Mode dial | KY58_MODE | read + command | Mode Switch, 3 positions; PANELS says panel has no function |
| 3. Radio select dial | KY58_PLAIN | read + command | C/RAD Switch, 3 positions; PANELS says panel has no function |
| 7. Encryption code preset dial | KY58_1TO5 | read + command | likely; DCS-BIOS calls it Full Switch, 6 positions |
| 8. Delay switch | KY58_DELAY | read + command | Delay Switch; PANELS says panel has no function |
| 9. Zeroize switch | KY58_ZEROIZE, KY58_ZEROIZE_COVER | read + command | Switch plus its cover; PANELS says panel has no function |

### Emergency Brake System (p. 174)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| EMER BRAKE handle | EMER_BRAKE | read + command | Emergency Brake |
| Unnamed toggle above the handle | SEAT_ADJUST | read + command | likely; title cut off in figure, DCS-BIOS Seat Adjust, spring-loaded |

### Auxiliary Lighting Control Panel (p. 175)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Refuel status and indexer lights dial | ALCP_RSIL | read + command | Refuel Status Indexer Lights |
| 2. NVIS lights switch (NVIS LTS) | ALCP_NVIS_LTS | read + command | Defined in DCS-BIOS although PANELS says no function |
| 3. Signal lights lamp test button | LAMP_TEST_BTN | read + command | Signal Lights Test |
| 4. Weapon station dimmer dial (WPN STA STATUS LTS) | ALCP_WPNSTA | read + command | Weapon Station Lights (No Function) |
| 5. HARS/SAS override switch | ALCP_HARSSAS | read + command | HARS-SAS Override/Norm |
| 6. Fire detect bleed air leak test button | ALCP_FDBA_TEST | read + command | Fire Detect Bleed Air Test |

### Stability Augmentation System (SAS) Panel (p. 176)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Yaw trim control knob | SASP_YAW_TRIM | read + command | Yaw Trim |
| 2. Takeoff trim button (T/O TRIM) | SASP_TO_TRIM | read + command | T/O Trim Button |
| Takeoff trim light | TAKE_OFF_TRIM | read only | TAKEOFF TRIM Indicator Light (green) |
| 3. Pitch SAS engage switch, left | SASP_PITCH_SAS_L | read + command | Electrically held switch OFF - ENGAGE |
| 3. Pitch SAS engage switch, right | SASP_PITCH_SAS_R | read + command | Electrically held switch OFF - ENGAGE |
| 4. Yaw SAS engage switch, left | SASP_YAW_SAS_L | read + command | Electrically held switch OFF - ENGAGE |
| 4. Yaw SAS engage switch, right | SASP_YAW_SAS_R | read + command | Electrically held switch OFF - ENGAGE |
| 5. Monitor test switch | SASP_MONITOR_TEST | read + command | Defined in DCS-BIOS although PANELS says no function |

### Identify Friend or Foe (IFF) Panel (p. 178)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Master mode dial | IFF_MASTER | read + command | OFF - STBY - LOW - NORM - EMER |
| 2. M-1 switch | IFF_TEST_M1 | read + command | Test M-1, states 0 to 2 |
| 3. M-2 switch | IFF_TEST_M2 | read + command | Test M-2, states 0 to 2 |
| 4. M-3/A switch | IFF_TEST_M3 | read + command | Test M-3, states 0 to 2 |
| 5. M-C switch | IFF_TEST_M4 | read + command | likely; fourth rocker, DCS-BIOS calls it Test M-4 |
| 6. Radiation test monitor switch (RAD TEST) | IFF_RADTEST | read + command | Defined in DCS-BIOS although PANELS says no function |
| 7. Identification of position switch (IDENT) | IFF_MIC_IDENT | read + command | Defined in DCS-BIOS although PANELS says no function |
| 8. Mode 1 code wheel, left | IFF_MODE1_WHEEL1 | read + command | Mode-1 Wheel 1 |
| 8. Mode 1 code wheel, right | IFF_MODE1_WHEEL2 | read + command | Mode-1 Wheel 2 |
| 9. Mode 3/A code wheel 1 (leftmost) | IFF_MODE3A_WHEEL1 | read + command | Mode-3A Wheel 1 |
| 9. Mode 3/A code wheel 2 | IFF_MODE3A_WHEEL2 | read + command | Mode-3A Wheel 2 |
| 9. Mode 3/A code wheel 3 | IFF_MODE3A_WHEEL3 | read + command | Mode-3A Wheel 3 |
| 9. Mode 3/A code wheel 4 | IFF_MODE3A_WHEEL4 | read + command | Mode-3A Wheel 4 |
| 10. Mode 4 switch | IFF_ON_OUT | read + command | likely; DCS-BIOS calls it IFF On/Out |
| 11. Audio light switch | IFF_OUT_AUDIO_LIGHT | read + command | LIGHT - OFF - AUDIO; reverse order of PANELS |
| 12. Code dial | IFF_CODE | read + command | Defined in DCS-BIOS although PANELS says no function |
| 13. Reply light | IFF_REPLY, IFF_REPLY_TEST, IFF_REPLY_DIM | read + command | Green lamp, push-to-test and DIM ring |
| 14. Test light | IFF_TEST, IFF_TEST_TEST, IFF_TEST_DIM | read + command | Green lamp, push-to-test and DIM ring |

### Emergency Flight Control Panel (p. 180)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Pitch/roll trim switch | EFCP_TRIM_OVERRIDE | read + command | EMER - NORM; reverse order of PANELS |
| 1. Emergency pitch and roll switch | EFCP_EMER_TRIM | read + command | Hat states 0 to 4: center, NOSE DN, RWD, NOSE UP, LWD |
| 2. Speed brake emergency retract switch (SPD BK EMER RETR) | EFCP_SPDBK_EMER_RETR | read + command | Speed Brake Emergency Retract |
| 3. Flap emergency retract switch (FLAP EMER RETR) | EFCP_FLAPS_EMER_RETR | read + command | Flaps Emergency Retract |
| 4. Aileron emergency disengage switch | EFCP_AILERON_EMER_DISENGAGE | read + command | LEFT - OFF - RIGHT |
| 5. Elevator emergency disengage switch | EFCP_ELEVATOR_EMER_DISENGAGE | read + command | LEFT - OFF - RIGHT |
| 6. MRFCS switch (FLT CONT) | EFCP_MRFCS | read + command | MAN REVERSION - NORM; reverse order of PANELS |
| L-AIL lamp | L_AILERON_EMER_DISENGAGE | read only | Left Aileron EMER DISENG Indicator (yellow) |
| R-AIL lamp | R_AILERON_EMER_DISENGAGE | read only | Right Aileron EMER DISENG Indicator (yellow) |
| L-ELEV lamp | L_ELEVATOR_EMER_DISENGAGE | read only | Left Elevator EMER DISENG Indicator (yellow) |
| R-ELEV lamp | R_ELEVATOR_EMER_DISENGAGE | read only | Right Elevator EMER DISENG Indicator (yellow) |

### Intercom Control Panel (p. 182)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Volume control knob (VOL) | INT_VOL | read + command | Intercom Volume |
| 2. HM switch | INT_HM | read + command | HM Switch; toggle in DCS-BIOS |
| 3. INT switch | INT_INT_UNMUTE, INT_INT_VOL | read + command | Un-Mute is in or out; Volume is the turn |
| 4. AIM switch | INT_AIM_UNMUTE, INT_AIM_VOL | read + command | Un-Mute is in or out; Volume is the turn |
| 5. FM switch | INT_FM_UNMUTE, INT_FM_VOL | read + command | Un-Mute is in or out; Volume is the turn |
| 6. VHF switch | INT_VHF_UNMUTE, INT_VHF_VOL | read + command | Un-Mute is in or out; Volume is the turn |
| 7. ILS switch | INT_ILS_UNMUTE, INT_ILS_VOL | read + command | Un-Mute is in or out; Volume is the turn |
| 8. UHF switch | INT_UHF_UNMUTE, INT_UHF_VOL | read + command | Un-Mute is in or out; Volume is the turn |
| 9. TCN switch | INT_TCN_UNMUTE, INT_TCN_VOL | read + command | Un-Mute is in or out; Volume is the turn |
| 10. Rotary selector dial | INT_MODE | read + command | INT / FM / VHF / HF / Blank |
| 11. IFF switch | INT_IFF_UNMUTE, INT_IFF_VOL | read + command | Un-Mute is in or out; Volume is the turn |
| 12. Call switch | INT_CALL | read + command | Defined in DCS-BIOS although PANELS says no function |

### Stall Warning Control Panel (p. 183)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| STALL volume dial | STALL_VOL | read + command | Stall Volume |
| PEAK PRFM volume dial | STALL_PEAK_VOL | read + command | Peak Volume |

### AN/ARC-186(V) VHF AM radio (DCS-BIOS only)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| (DCS-BIOS only) Preset Channel Selector | VHFAM_PRESET | read + command | Preset Channel Selector; step up or down only |
| (DCS-BIOS only) Mode | VHFAM_MODE | read + command | OFF / TR / DF |
| (DCS-BIOS only) Frequency Selection Dial | VHFAM_FREQEMER | read + command | FM / AM / MAN / PRE |
| (DCS-BIOS only) Volume Control | VHFAM_VOL | read + command | VHF AM Volume Control |
| (DCS-BIOS only) Load Button | VHFAM_LOAD | read + command | Load Button |
| (DCS-BIOS only) Squelch | VHFAM_SQUELCH | read + command | Squelch, 3 positions |
| (DCS-BIOS only) Frequency Selector 1 | VHFAM_FREQ1 | read + command | Frequency Selector 1; step up or down only |
| (DCS-BIOS only) Frequency Selector 2 | VHFAM_FREQ2 | read + command | Frequency Selector 2; step up or down only |
| (DCS-BIOS only) Frequency Selector 3 | VHFAM_FREQ3 | read + command | Frequency Selector 3; step up or down only |
| (DCS-BIOS only) Frequency Selector 4 | VHFAM_FREQ4 | read + command | Frequency Selector 4; states 00, 25, 50, 75 |
| (DCS-BIOS only) Frequency Selector 1 Rotation | VHFAM_FREQ1_ROT | read only | Knob turn position as output |
| (DCS-BIOS only) Frequency Selector 2 Rotation | VHFAM_FREQ2_ROT | read only | Knob turn position as output |
| (DCS-BIOS only) Frequency Selector 3 Rotation | VHFAM_FREQ3_ROT | read only | Knob turn position as output |
| (DCS-BIOS only) Frequency Selector 4 Rotation | VHFAM_FREQ4_ROT | read only | Knob turn position as output |
| (DCS-BIOS only) Frequency (String) | VHF_AM_FREQUENCY_S | read only | VHF AM Frequency (String), 7 characters |
| (DCS-BIOS only) VHF AM Present | VHFAM_PRESENT | read only | 1 when the VHF AM radio is installed, ARC-210 absent |

## Right console

### Cockpit Canopy Switch and Canopy Ejection Handle (p. 186)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Canopy switch (CANOPY) | CANOPY_OPEN | read + command | Canopy Open Switch; states 0 to 2: down, stop, up |
| 2. Boarding ladder button | LADDER_EXTEND, LADDER_EXTEND_COVER | read + command | Button plus its cover |
| 3. Canopy jettison handle | CANOPY_JTSN | read + command | Canopy Jettison |
| (DCS-BIOS only) Canopy Jettison Unlock | CANOPY_JTSN_UNLOCK | read + command | Canopy Jettison Unlock |
| (DCS-BIOS only) Canopy Position | CANOPY_POS | read only | Canopy position as output |

### Electrical Power Panel (p. 187)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 3. APU GEN switch (APU GEN PWR) | EPP_APU_GEN_PWR | read + command | APU GEN PWR |
| 2. Inverter switch (INVERTER STBY) | EPP_INVERTER | read + command | Inverter TEST - OFF - STBY; spring-loaded, reverse order of PANELS |
| 5. EMER FLOOD switch | EPP_EMER_FLOOD | read + command | Emergency Flood Light |
| 4. AC GEN switch, left | EPP_AC_GEN_PWR_L | read + command | AC GEN PWR Left |
| 4. AC GEN switch, right | EPP_AC_GEN_PWR_R | read + command | AC GEN PWR Right |
| 1. Battery switch (BATTERY PWR) | EPP_BATTERY_PWR | read + command | Battery Power |

### Environment System Panel (p. 189)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 4. Oxygen flow indicator | OXY_FLOW, OXY_FLOW_G | read only | Flow Indicator on/off (white); OXY_FLOW_G gives it as gauge |
| 5. Oxygen supply pressure gauge | OXY_PRESS | read only | Oxygen Pressure Indicator |
| 3. Oxygen emergency lever | OXY_EMERGENCY | read + command | Oxygen Flow Emergency / Normal / Test; spring-loaded |
| 2. Oxygen dilution lever | OXY_DILUTER | read + command | Oxygen Normal/100% |
| 1. Oxygen supply lever | OXY_SUPPLY | read + command | Oxygen Supply On/Off |
| 6. Oxygen quantity gauge | OXY_VOLUME | read only | Oxygen Volume (0 to 5 liters) |
| 7. Oxygen indicator test button (OXY IND TEST) | ENVCP_OXY_TEST | read + command | Oxygen Indicator Test |
| 4. Windshield defog/deice switch | ENVCP_WINDSHIELD_DEFOG | read + command | Windshield Defog/Deice |
| 8. Canopy defog dial | ENVCP_CANOPY_DEFOG | read + command | Canopy Defog |
| 6. Windshield rain remove and wash switch | ENVCP_WRRW | read + command | Windshield Rain Removal/Wash, 3 positions; PANELS says no function |
| 5. Pitot heater switch | ENVCP_PITOT_HEAT | read + command | Pitot Heat |
| 7. Bleed air switch | ENVCP_BLEED_AIR | read + command | Bleed Air |
| 14. Cabin air pressure gauge | CABIN_PRESS_ALT | read only | Cabin Pressure Altitude |
| 9. TEMP/PRESS switch | ENVCP_TEMP_PRESS | read + command | Temperature/Pressure Control, 3 positions |
| 11. Main air supply switch | ENVCP_AIR_SUPPLY | read + command | Main Air Supply |
| 10. Flow level dial | ENVCP_FLOW_LEVEL | read + command | Flow Level |
| 13. Cabin air conditioner switch (CABIN AIR COND) | ENVCP_AC_OPER | read + command | Air Conditioner MAN / AUTO / COLD / HOT; PANELS lists three |
| 12. Temperature level dial | ENVCP_TEMP_LEVEL | read + command | Defined in DCS-BIOS although PANELS says no function |

### Lighting Control Panel (p. 191)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. POSITION switch | LCP_POSITION | read + command | Positions FLASH / OFF / STEADY |
| 3. FORMATION dial | LCP_FORMATION | read + command | Formation Lights |
| 2. ANTI-COLLISION switch | LCP_ANTICOLLISION | read + command | Electrically held switch |
| 5. ENG INST dial | LCP_ENG_INST | read + command | Engine Instrument Lights |
| 4. NOSE ILLUM switch | LCP_NOSE_ILLUM | read + command | Nose Illumination |
| 7. AUX INST dial | LCP_AUX_INST | read + command | Aux Instrument Lights |
| 8. SIGNAL LTS switch | LCP_SIGNAL_LIGHTS | read + command | Signal Lights |
| 6. FLT INST dial | LCP_FLIGHT_INST | read + command | Flight Instrument Lights |
| 9. ACCEL & COMP switch | LCP_ACCEL_COMP | read + command | Accelerometer and Compass Lights |
| 10. FLOOD dial | LCP_FLOOD | read + command | Flood Lights |
| 11. CONSOLE dial | LCP_CONSOLE | read + command | Console Lights |
| (DCS-BIOS only) Console Light Brightness | INT_CONSOLE_L_BRIGHT | read only | Brightness as output |
| (DCS-BIOS only) Engine Instrument Light Brightness | INT_ENG_INST_L_BRIGHT | read only | Brightness as output |
| (DCS-BIOS only) Flight Instruments Light Brightness | INT_FLT_INST_L_BRIGHT | read only | Brightness as output |
| (DCS-BIOS only) Auxiliary Instruments Light Brightness | INT_AUX_INST_L_BRIGHT | read only | Brightness as output |
| (DCS-BIOS only) Flood Light Brightness | INT_FLOOD_L_BRIGHT | read only | Brightness as output |
| (DCS-BIOS only) Caution Lights Brightness | INT_CAUTION_L_BRIGHT | read only | Brightness as output |

### Caution Light Panel (p. 195)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| ENG START CYCLE | CL_A1 | read only | ENG START CYCLE Light (green) |
| L-HYD PRESS | CL_A2 | read only | L-HYD PRESS Light (green) |
| R-HYD PRESS | CL_A3 | read only | R-HYD PRESS Light (green) |
| GUN UNSAFE | CL_A4 | read only | GUN UNSAFE Light (green) |
| ANTI-SKID | CL_B1 | read only | ANTI-SKID Light (green); PANELS says no function |
| L-HYD RES | CL_B2 | read only | L-HYD RES Light (green) |
| R-HYD RES | CL_B3 | read only | R-HYD RES Light (green) |
| OXY LOW | CL_B4 | read only | OXY LOW Light (green) |
| ELEV DISENG | CL_C1 | read only | ELEV DISENG Light (green) |
| Blank lamp (dash legend) | CL_C2 | read only | likely; matched by position, DCS-BIOS calls it VOID1 |
| SEAT NOT ARMED | CL_C3 | read only | SEAT NOT ARMED Light (green); PANELS says no function |
| BLEED AIR LEAK | CL_C4 | read only | BLEED AIR LEAK Light (green) |
| AIL DISENG | CL_D1 | read only | AIL DISENG Light (green) |
| L-AIL TAB | CL_D2 | read only | L-AIL TAB Light (green) |
| R-AIL TAB | CL_D3 | read only | R-AIL TAB Light (green) |
| SERVICE AIR HOT | CL_D4 | read only | SERVICE AIR HOT Light (green); PANELS says no function |
| PITCH SAS | CL_E1 | read only | PITCH SAS Light (green) |
| L-ENG HOT | CL_E2 | read only | L-ENG HOT Light (green) |
| R-ENG HOT | CL_E3 | read only | R-ENG HOT Light (green) |
| WINDSHIELD HOT | CL_E4 | read only | WINDSHIELD HOT Light (green); PANELS says no function |
| YAW SAS | CL_F1 | read only | YAW SAS Light (green) |
| L-ENG OIL PRESS | CL_F2 | read only | L-ENG OIL PRESS Light (green) |
| R-ENG OIL PRESS | CL_F3 | read only | R-ENG OIL PRESS Light (green) |
| CICU | CL_F4 | read only | CICU Light (green) |
| GCAS | CL_G1 | read only | GCAS Light (green) |
| L-MAIN PUMP | CL_G2 | read only | L-MAIN PUMP Light (green) |
| R-MAIN PUMP | CL_G3 | read only | R-MAIN PUMP Light (green) |
| Blank lamp (dash legend) | CL_G4 | read only | likely; matched by position, DCS-BIOS calls it VOID2 |
| LASTE | CL_H1 | read only | LASTE Light (green) |
| L-WING PUMP | CL_H2 | read only | L-WING PUMP Light (green) |
| R-WING PUMP | CL_H3 | read only | R-WING PUMP Light (green) |
| HARS | CL_H4 | read only | HARS Light (green) |
| IFF MODE-4 | CL_I1 | read only | IFF MODE-4 Light (green); PANELS says no function |
| L-MAIN FUEL LOW | CL_I2 | read only | L-MAIN FUEL LOW Light (green) |
| R-MAIN FUEL LOW | CL_I3 | read only | R-MAIN FUEL LOW Light (green) |
| L-R TKS UNEQUAL | CL_I4 | read only | L-R TKS UNEQUAL Light (green) |
| EAC | CL_J1 | read only | EAC Light (green) |
| L-FUEL PRESS | CL_J2 | read only | L-FUEL PRESS Light (green) |
| R-FUEL PRESS | CL_J3 | read only | R-FUEL PRESS Light (green) |
| NAV | CL_J4 | read only | NAV Light (green) |
| STALL SYS | CL_K1 | read only | STALL SYS Light (green) |
| L-CONV | CL_K2 | read only | L-CONV Light (green) |
| R-CONV | CL_K3 | read only | R-CONV Light (green) |
| CADC | CL_K4 | read only | CADC Light (green) |
| APU GEN | CL_L1 | read only | APU GEN Light (green) |
| L-GEN | CL_L2 | read only | L-GEN Light (green) |
| R-GEN | CL_L3 | read only | R-GEN Light (green) |
| INST INV | CL_L4 | read only | INST INV Light (green) |
| INU AIR HOT | — | — | not exported |

### TACAN Operation and Control Panel (p. 198)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 3. Channel display window | TACAN_CHANNEL | read only | TACAN Channel, text of 4 characters |
| 5. Volume knob (VOL) | TACAN_VOL | read + command | TACAN Signal Volume |
| 2. Channel selector, left | TACAN_10 | read + command | Left Channel Selector; step up or down only |
| 2. Channel selector, middle | TACAN_1, TACAN_XY | read + command | likely; DCS-BIOS calls it Right selector; X/Y is TACAN_XY |
| 4. Test button | TACAN_TEST_BTN | read + command | TACAN Test Button |
| Test lamp | TACAN_TEST | read only | TACAN Test Indicator Light; DCS-BIOS says green |
| 1. Mode dial | TACAN_MODE | read + command | TACAN Mode Dial, 5 positions |

### ILS Control Panel and ILS Operation (p. 199)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Power control knob, outer part | ILS_PWR | read + command | ILS Power |
| 1. Power control knob, base | ILS_MHZ | read + command | ILS Frequency MHz, states 108 to 111 |
| 3. ILS setting window | ILS_FREQUENCY_S | read only | ILS Frequency (String), 6 characters |
| 2. Volume knob, outer part (VOL) | ILS_VOL | read + command | ILS Volume |
| 2. Volume knob, base | ILS_KHZ | read + command | ILS Frequency KHz, 10 states from 10 to 95 |

### Heading and Attitude Reference Systems (HARS) Control Panel (p. 200)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. SYN-IND annunciator | HARS_SYNC | read only | HARS Sync |
| 2. Mode switch | HARS_SLAVE_DG | read + command | HARS SLAVE-DG Mode |
| 3. LAT correction dial | HARS_LATITUDE | read + command | HARS Latitude Dial |
| 6. Sync control (PUSH TO SYNC, HDG) | HARS_PTS, HARS_HDG | read + command | Push is HARS_PTS; turn is HARS_HDG |
| 5. Magnetic variation switch (MAG VAR) | HARS_MAGVAR | read + command | HARS MAG VAR, 3 positions |
| 4. Hemisphere selector switch | HARS_NS | read + command | HARS N/S toggle switch |

### Helmet Mounted Cueing System (HMCS) Control Panel (p. 201)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| HMCS power switch | A102_HMCS_PW | read + command | Scorpion HMCS Power BAT/OFF/ON; reverse order of PANELS |
| HVI UNSAFE legend | — | — | not exported |
| REPLACE BATTERY legend | — | — | not exported |

### Auxiliary Avionics Panel (AAP) (p. 203)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. CDU power switch | AAP_CDUPWR | read + command | CDU Power |
| 2. EGI power switch | AAP_EGIPWR | read + command | EGI Power |
| 4. STEER PT dial | AAP_STEERPT | read + command | STEERPT FLTPLAN - MARK - MISSION |
| 3. PAGE dial | AAP_PAGE | read + command | PAGE OTHER - POSITION - STEER - WAYPT |
| 5. STEER switch | AAP_STEER | read + command | Toggle Steerpoint; spring-loaded |

## Keypads and displays


### Control Display Unit (CDU) (p. 205)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Display window | CDU_LINE0 … CDU_LINE9 | read only | Export hook parses the CDU indication into 10 strings of 24 characters |
| Scratchpad | CDU_LINE9 | read only | Line 10 string; scratchpad text sits at its left |
| 2. Line select keys, left (LSK) | CDU_LSK_3L, CDU_LSK_5L, CDU_LSK_7L, CDU_LSK_9L | read + command | Only rows 3, 5, 7, 9 exist; 3L, 5L, 7L, 9L |
| 2. Line select keys, right (LSK) | CDU_LSK_3R, CDU_LSK_5R, CDU_LSK_7R, CDU_LSK_9R | read + command | Only rows 3, 5, 7, 9 exist; 3R, 5R, 7R, 9R |
| LSK marker symbols | CDU_LINE0 … CDU_LINE9 | read only | likely; arrows are remapped characters in the line text |
| 13.1. SYS key | CDU_SYS | read + command | Push button SYS |
| 13.2. NAV key | CDU_NAV | read + command | Push button NAV |
| 13.3. WP key | CDU_WP | read + command | Push button WP |
| 13.4. OSET key | CDU_OSET | read + command | Push button OSET |
| 13.5. FPM key | CDU_FPM | read + command | Push button FPM |
| 13.6. PREV key | CDU_PREV | read + command | Push button PREV |
| 4. Alphanumeric keys | CDU_0 … CDU_9, CDU_A … CDU_Z, CDU_POINT, CDU_SLASH | read + command | Digits, letters, decimal point and slash; push buttons |
| 3. DIM/BRT rocker | CDU_BRT | read + command | CDU Display Brightness Adjustment; states 0 to 2: down, center, up |
| 5. ± rocker | CDU_DATA | read + command | +/- Rocker; states 0 to 2: down, center, up |
| 12. Page rocker (P/G) | CDU_PG | read + command | PG Rocker; states 0 to 2: down, center, up |
| 9. Blank rocker | CDU_SCROLL | read + command | Scroll Waypoint Names (Blank Rocker); states 0 to 2 |
| 6. FA key (Fault Acknowledge) | CDU_FA | read + command | Push button FA |
| 7. CLR key | CDU_CLR | read + command | Push button CLR |
| 10. BCK key | CDU_BCK | read + command | Push button BCK |
| 8. SPC key | CDU_SPC | read + command | Push button SPC |
| 11. MK key | CDU_MK | read + command | Push button MK |
| Two unlabelled square keys | CDU_NA1, CDU_NA2 | read + command | likely; described as No Function 1 and 2 |

### Up Front Controller (UFC) (p. 303)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 1. Mark (MK) button | UFC_MK | read + command | Push button MK |
| 2. Clear (CLR) button | UFC_CLR | read + command | Push button CLR |
| 3. Time Hack (HACK) button | UFC_HACK | read + command | Push button HACK |
| 4. Space (SPC) button | UFC_SPC | read + command | Push button SPC |
| 5. Altitude Alert (ALT ALRT) button | UFC_ALT_ALRT | read + command | Push button ALT ALRT |
| 6. Enter (ENT) button | UFC_ENT | read + command | Push button ENT |
| 7. Letter (LTR) mode button | UFC_LTR | read + command | Push button LTR |
| 8. Function (FUNC) mode button | UFC_FUNC | read + command | Push button FUNC |
| Key 1 | UFC_1 | read + command | Push button 1 |
| Key 2 | UFC_2 | read + command | Push button 2 |
| Key 3 | UFC_3 | read + command | Push button 3 |
| Key 4 | UFC_4 | read + command | Push button 4 |
| Key 5 | UFC_5 | read + command | Push button 5 |
| Key 6 | UFC_6 | read + command | Push button 6 |
| Key 7 | UFC_7 | read + command | Push button 7 |
| Key 8 | UFC_8 | read + command | Push button 8 |
| Key 9 | UFC_9 | read + command | Push button 9 |
| Key 0 | UFC_10 | read + command | likely; DCS-BIOS names the 0 key UFC_10 |
| 9. DATA rocker (PG) | UFC_DATA | read + command | DATA Up/Down; states 0 to 2: down, center, up |
| 10. SEL rocker | UFC_SEL | read + command | SEL Up/Down; states 0 to 2: down, center, up |
| 11. STEER rocker | UFC_STEER | read + command | STEER Up/Down; states 0 to 2: down, center, up |
| 12. INTEN rocker | UFC_INTEN | read + command | INTEN Incr/Decr; states 0 to 2, direction not documented |
| 13. DEPR rocker | UFC_DEPR | read + command | DEPR Up/Down; states 0 to 2: down, center, up |
| 14. MASTER CAUTION | MASTER_CAUTION, UFC_MASTER_CAUTION | read + command | Lamp is MASTER_CAUTION (read only); UFC_MASTER_CAUTION resets |
| FWD button | — | — | function not stated; maybe an A-10C II button below |
| MID button | — | — | function not stated; maybe an A-10C II button below |
| AFT button | — | — | function not stated; maybe an A-10C II button below |
| Three unlabelled buttons | — | — | function not stated; maybe an A-10C II button below |
| (DCS-BIOS only) COM1 button | UFC_COM1 | read + command | Control VHF UHF Radio (A-10C II) |
| (DCS-BIOS only) COM SEC button | UFC_COM_SEC | read + command | COM SEC (A-10C II) |
| (DCS-BIOS only) IFF button | UFC_IFF | read + command | IFF (A-10C II) |
| (DCS-BIOS only) COM2 button | UFC_COM2 | read + command | Toggle ARC-210 RT2 Status (A-10C II) |
| (DCS-BIOS only) ECCM button | UFC_ECCM | read + command | ECCM (A-10C II) |
| (DCS-BIOS only) IDM button | UFC_IDM | read + command | IDM (A-10C II) |

### MFCD pages overview (p. 309)

- MFCD page content (DTS, DP, STAT, DSMS, TAD, TGP, MAV, MSG, CDU repeater): no DCS-BIOS output (gap: export).
- Page selection works through the OSBs: LMFD_01 … LMFD_20 and RMFD_01 … RMFD_20, see the MFCD sections.
- The CDU screen text is exported on its own as CDU_LINE0 … CDU_LINE9, see the CDU section.

## Defensive systems


### Countermeasure Signal Processor (CMSP) Panel (p. 491)

| Control | DCS-BIOS identifier | Access | Note |
| --- | --- | --- | --- |
| 3. Display, upper line | CMSP1 | read only | CMSP Display Line 1; text of 19 characters, 4 segments |
| 3. Display, lower line | CMSP2 | read only | CMSP Display Line 2; text of 19 characters, 4 segments |
| 4. SET button, segment 1 (left) | CMSP_ARW1 | read + command | SET Button 1 |
| 4. SET button, segment 2 | CMSP_ARW2 | read + command | SET Button 2 |
| 4. SET button, segment 3 | CMSP_ARW3 | read + command | SET Button 3 |
| 4. SET button, segment 4 (right) | CMSP_ARW4 | read + command | SET Button 4 |
| 5. NXT switch | CMSP_UPDN | read + command | Cycle Program or Value Up/Down; states 0 to 2: down, center, up |
| 6. RTN button | CMSP_RTN | read + command | RTN |
| 7. JTSN switch | CMSP_JTSN | read + command | JTSN / OFF |
| 8. BRT knob | CMSP_BRT | read + command | Brightness |
| 2. System switch, MWS | CMSP_MWS | read + command | OFF - ON - (MENU); reverse order of PANELS |
| 2. System switch, JMR | CMSP_JMR | read + command | OFF - ON - (MENU); reverse order of PANELS |
| 2. System switch, RWR | CMSP_RWR | read + command | OFF - ON - (MENU); reverse order of PANELS |
| 2. System switch, DISP | CMSP_DISP | read + command | OFF - ON - (MENU); reverse order of PANELS |
| 1. Mode select dial | CMSP_MODE | read + command | CMSP Mode Select; five states 0 to 4, order not documented |

### CMSC operation (p. 497)

- Every CMSC control, window and lamp is mapped in the CMSC section of the Center front dash; this section adds no control.
- Window text is read from CMSC_TXT_JMR, CMSC_TXT_MWS and CMSC_TXT_CHAFF_FLARE; program choice and start with the stick CMS switch is a keybind.

### ALR-69(V) Radar Warning Receiver (RWR) (p. 500)

- Scope picture, symbols and the INT button: no DCS-BIOS output (gap: export).
- Related controls: RWR_BRT (scope brightness), CMSP_RWR (power and test), CMSC_RWR_VOL, CMSC_PRI, CMSC_SEP, CMSC_UNK, CMSC_LAUNCH.

### HMCS HOTAS Controls (p. 482)

- DMS and TMS functions with the HMCS: keybind; DCS-BIOS has no control for them (see Control Stick and Throttles).
- HMCS power is A102_HMCS_PW, see the HMCS Control Panel on the right console.

## DCS-BIOS controls not in PANELS.md

These controls exist in DCS-BIOS but no panel of PANELS.md describes them (the manual does not cover them, or they belong to the external model). Columns as above, with the DCS-BIOS identifier first; the description is the DCS-BIOS one.

### Antenna Panel (DCS-BIOS only)

| DCS-BIOS identifier | Access | Description | Note |
| --- | --- | --- | --- |
| ANT_IFF | read + command | IFF Antenna Switch |  |
| ANT_UHF | read + command | UHF Antenna Switch |  |
| ANT_EGIHQTOD | read + command | EGI HQ TOD Switch |  |

### Circuit Breaker Panel (DCS-BIOS only)

| DCS-BIOS identifier | Access | Description | Note |
| --- | --- | --- | --- |
| CBP_AILERON_DISC_L | read + command | AILERON DISC L Circuit Breaker |  |
| CBP_AILERON_DISC_R | read + command | AILERON DISC R Circuit Breaker |  |
| CBP_SPS_RUDDER_AUTH_LIM | read + command | SPS RUDDER AUTH LIM Circuit Breaker |  |
| CBP_ELEVATOR_DISC_L | read + command | ELEVATOR DISC L Circuit Breaker |  |
| CBP_ELEVATOR_DISC_R | read + command | ELEVATOR DISC R Circuit Breaker |  |
| CBP_AILERON_TAB_L | read + command | AILERON TAB L Circuit Breaker |  |
| CBP_AILERON_TAB_R | read + command | AILERON TAB R Circuit Breaker |  |
| CBP_EMER_FLAP | read + command | EMER FLAP Circuit Breaker |  |
| CBP_EMER_TRIM | read + command | EMER TRIM Circuit Breaker |  |
| CBP_GEAR | read + command | GEAR Circuit Breaker |  |
| CBP_ENG_START_L | read + command | ENG START L Circuit Breaker |  |
| CBP_ENG_START_R | read + command | ENG START R Circuit Breaker |  |
| CBP_APU_CONT | read + command | APU CONT Circuit Breaker |  |
| CBP_ENG_IGNITOR_1 | read + command | ENG IGNITOR 1 Circuit Breaker |  |
| CBP_ENG_IGNITOR_2 | read + command | ENG IGNITOR 2 Circuit Breaker |  |
| CBP_FUEL_SHUTOFF_L | read + command | FUEL SHUTOFF L Circuit Breaker |  |
| CBP_FUEL_SHUTOFF_R | read + command | FUEL SHUTOFF R Circuit Breaker |  |
| CBP_DC_FUEL_PUMP | read + command | DC FUEL PUMP Circuit Breaker |  |
| CBP_BLEED_AIR_CONT_L | read + command | BLEED AIR CONT L Circuit Breaker |  |
| CBP_BLEED_AIR_CONT_R | read + command | BLEED AIR CONT R Circuit Breaker |  |
| CBP_EXT_STORES_JETT_1 | read + command | EXT STORES JETT 1 Circuit Breaker |  |
| CBP_EXT_STORES_JETT_2 | read + command | EXT STORES JETT 2 Circuit Breaker |  |
| CBP_STBY_ATT_IND | read + command | STBY ATT IND Circuit Breaker |  |
| CBP_MASTER_CAUTION | read + command | MASTER CAUTION Circuit Breaker |  |
| CBP_PITOT_HEAT_AC | read + command | PITOT HEAT AC Circuit Breaker |  |
| CBP_IFF | read + command | IFF Circuit Breaker |  |
| CBP_UHF | read + command | UHF Circuit Breaker |  |
| CBP_INTERCOM | read + command | INTERCOM Circuit Breaker |  |
| CBP_GEN_CONT_L | read + command | GEN CONT L Circuit Breaker |  |
| CBP_GEN_CONT_R | read + command | GEN CONT R Circuit Breaker |  |
| CBP_CONVERTER_L | read + command | CONVERTER L Circuit Breaker |  |
| CBP_AUX_ESS_BUS_0A | read + command | AUX ESS BUS 0A Circuit Breaker |  |
| CBP_AUX_ESS_BUS_0B | read + command | AUX ESS BUS 0B Circuit Breaker |  |
| CBP_AUX_ESS_BUS_0C | read + command | AUX ESS BUS 0C Circuit Breaker |  |
| CBP_BAT_BUS_TRANS | read + command | BAT BUS TRANS Circuit Breaker |  |
| CBP_INVERTER_PWR | read + command | INVERTER PWR Circuit Breaker |  |
| CBP_INVERTER_CONT | read + command | INVERTER CONT Circuit Breaker |  |
| CBP_AUX_ESS_BUS_TIE | read + command | AUX ESS BUS TIE Circuit Breaker |  |

### DVADR (DCS-BIOS only)

| DCS-BIOS identifier | Access | Description | Note |
| --- | --- | --- | --- |
| DVADR_FUNCTION | read + command | Function Control Toggle Switch |  |
| DVADR_VIDEO | read + command | Video Selector Toggle Switch |  |
| DVADR_EOT | read only | DVADR End of Tape Indicator Light (yellow) |  |
| DVADR_REC_REMOTE | read only | DVADR Record (On) Remote Panel Indicator Light (green) |  |
| DVADR_EOT_REMOTE | read only | DVADR End of Tape Remote Panel Indicator Light |  |
| DVADR_REC | read only | DVADR Record (On) Indicator Light (green) |  |

### External Aircraft Model (DCS-BIOS only)

| DCS-BIOS identifier | Access | Description | Note |
| --- | --- | --- | --- |
| EXT_SPEED_BRAKE_RIGHT | read only | Right Speed Brake |  |
| EXT_SPEED_BRAKE_LEFT | read only | Left Speed Brake |  |
| EXT_FORMATION_LIGHTS | read only | Formation Lights (light green) |  |
| EXT_POSITION_LIGHT_LEFT | read only | Left Position Light (red) |  |
| EXT_POSITION_LIGHT_RIGHT | read only | Right Position Light (green) |  |
| EXT_STROBE_TAIL | read only | Tail Strobe Light (white) |  |
| EXT_STROBE_LEFT | read only | Left Strobe Light (white) |  |
| EXT_STROBE_RIGHT | read only | Right Strobe Light (white) |  |
| EXT_WOW_NOSE | read only | Weight ON Wheels Nose Gear |  |
| EXT_WOW_RIGHT | read only | Weight ON Wheels Right Gear |  |
| EXT_WOW_LEFT | read only | Weight ON Wheels Left Gear |  |
| EXT_BOTTOM_LIGHT | read only | Middle Bottom Light (white) |  |
| EXT_TOP_LIGHT | read only | Top Light (white) |  |
| EXT_TAIL_LIGHT | read only | Tail Light (white) |  |
| EXT_L_RUDDER_LIGHT | read only | Left Rudder Light (white) |  |
| EXT_R_RUDDER_LIGHT | read only | Right Rudder Light (white) |  |

### Misc (DCS-BIOS only)

| DCS-BIOS identifier | Access | Description | Note |
| --- | --- | --- | --- |
| GND_SAFE_OVERRIDE_COVER | read + command | Ground Safety Override Switch Cover |  |
| GND_SAFE_OVERRIDE | read + command | Ground Safety Override |  |
| AUX_GEAR | read + command | Auxiliary Landing Gear Handle |  |
| AUX_GEAR_LOCK | read + command | Auxiliary Landing Gear Handle Lock Button |  |
| SEAT_ARM | read + command | Seat Arm Handle (0 = ARM, 1 = DISARM) |  |
| SUIT_TEST | read + command | Anti-G Suit Valve Test Button |  |
| CANOPY_DISENGAGE | read + command | Canopy actuator disengage lever |  |
| MIRROR_TOGGLE | read + command | Toggle Mirrors |  |
| STICK_HIDE | read + command | Hide Stick toggle |  |

## Summary

Rows counted over all tables above the "DCS-BIOS controls not in PANELS.md" section; rows whose Control starts with "(DCS-BIOS only)" are counted in their own column.

| Access | PANELS.md rows | DCS-BIOS-only rows |
| --- | --- | --- |
| read + command | 323 | 19 |
| read only | 154 | 45 |
| — | 33 | 0 |
| Total | 510 | 64 |

The "DCS-BIOS controls not in PANELS.md" section adds 72 rows (52 read + command, 20 read only), so 136 DCS-BIOS-only rows in all.

### Gaps

Every row without a DCS-BIOS identifier in the sections above, grouped by its gap (33 rows).

#### keybind (16)

- Control Stick: 1. Master Mode Control Button (MMCB)
- Control Stick: 2. Data Management Switch (DMS)
- Control Stick: 3. Target Management Switch (TMS)
- Control Stick: 4. Nosewheel Steering (NWS) Button
- Control Stick: 5. Countermeasures Switch (CMS)
- Control Stick: 6. Weapon Release Button
- Control Stick: 7. Trim Switch
- Control Stick: 8. Trigger
- Throttles: 1. Mic Switch
- Throttles: 2. Speed Brake
- Throttles: 3. Boat Switch
- Throttles: 4. China Hat
- Throttles: 5. Pinky Switch
- Throttles: 6. Left Throttle Button
- Throttles: 7. Slew Control
- Throttles: 8. Coolie Hat

#### export (4)

- Radar Warning Receiver (RWR) Display: Azimuth indicator
- Left Multifunction Color Display (MFCD): Screen
- Right Multifunction Color Display (MFCD): Screen
- Heads Up Display Area Above Dash: 3. Heads-Up Display (HUD)

#### not exported (3)

- Caution Light Panel: INU AIR HOT
- Helmet Mounted Cueing System (HMCS) Control Panel: HVI UNSAFE legend
- Helmet Mounted Cueing System (HMCS) Control Panel: REPLACE BATTERY legend

#### no function in DCS (5)

- Attitude Director Indicator (ADI): 3. Bank scale
- Attitude Director Indicator (ADI): 5. Pitch trim index
- Attitude Director Indicator (ADI): 10. Glide slope deviation scale
- Horizontal Situation Indicator (HSI): 3. Aircraft symbol
- Horizontal Situation Indicator (HSI): 4. Lubber line

#### other (5)

- Heads Up Display Area Above Dash: 4. Up-Front Controller (UFC) — "mapped in the UFC section"
- Up Front Controller (UFC): FWD button — "function not stated; maybe an A-10C II button below"
- Up Front Controller (UFC): MID button — "function not stated; maybe an A-10C II button below"
- Up Front Controller (UFC): AFT button — "function not stated; maybe an A-10C II button below"
- Up Front Controller (UFC): Three unlabelled buttons — "function not stated; maybe an A-10C II button below"

### Cold start coverage

Every row of [STARTUP.md](STARTUP.md) looked up by Panel and Control in the sections above (a Control cell naming several controls counts as one row; the CDU is the Control Display Unit (CDU) section; Lighting Control Panel "(whole panel)" is checked against its 11 numbered controls). Rows marked "(not in PANELS.md)" are matched against the section "DCS-BIOS controls not in PANELS.md" and the radio panel.

164 rows: 132 use only controls with an identifier and `read + command` (129 by name, 3 by `likely` match for a control not in PANELS.md); 8 use a `read only` control (checks: fine); 13 name an MFCD OSB or CDU line select key without its number, so only the identifier family is known; 11 have no identifier.

The `read only` rows are #15, #16, #43, #75, #77, #102, #104, #105. Of these, #15, #16, #102 and #105 move a throttle lever (lever position only, no input) and #77 sets the clock (the buttons are CLOCK_SET and CLOCK_CTRL on the Digital Clock); the others are lamp, gauge or readout checks.

#### Rows matched to a control not in PANELS.md

- STARTUP #4: Ejection Seat Arm / Ejection seat arm lever (not in PANELS.md) — SEAT_ARM, Seat Arm Handle (`likely`, `read + command`; 0 = ARM, 1 = DISARM)
- STARTUP #44: Front dash / Auxiliary landing gear extension handle (not in PANELS.md) — AUX_GEAR, Auxiliary Landing Gear Handle (`likely`, `read + command`; AUX_GEAR_LOCK is its lock button)
- STARTUP #88: AN/ARC-186(V) Radio Control Panel / Radio 1 frequency controls (not in PANELS.md) — ARC210_100MHZ_SEL, ARC210_10MHZ_SEL, ARC210_1MHZ_SEL, ARC210_100KHZ_SEL, ARC210_25KHZ_SEL, the five unlabelled knobs of the AN/ARC-186(V) Radio Control Panel (`likely`, `read + command`; which knob is which is not stated)

#### Rows with an OSB or line select key but no number (13)

- STARTUP #127: MFCD / OSB LOAD ALL (number not stated) — `read + command`; which key is not stated (LMFD_01 … LMFD_20 / RMFD_01 … RMFD_20)
- STARTUP #131: CDU / Line select key beside FPBUILD (side and line not stated) — `read + command`; which key is not stated (CDU_LSK_3L, CDU_LSK_5L, CDU_LSK_7L, CDU_LSK_9L / CDU_LSK_3R, CDU_LSK_5R, CDU_LSK_7R, CDU_LSK_9R)
- STARTUP #132: MFCD / OSB TAD (number not stated) — `read + command`; which key is not stated (LMFD_01 … LMFD_20 / RMFD_01 … RMFD_20)
- STARTUP #133: MFCD / OSB NET (number not stated) — `read + command`; which key is not stated (LMFD_01 … LMFD_20 / RMFD_01 … RMFD_20)
- STARTUP #134: MFCD / OSB at Ownship ID (number not stated) — `read + command`; which key is not stated (LMFD_01 … LMFD_20 / RMFD_01 … RMFD_20)
- STARTUP #135: MFCD / OSB at Group ID (number not stated) — `read + command`; which key is not stated (LMFD_01 … LMFD_20 / RMFD_01 … RMFD_20)
- STARTUP #137: MFCD / OSB TGP (number not stated) — `read + command`; which key is not stated (LMFD_01 … LMFD_20 / RMFD_01 … RMFD_20)
- STARTUP #139: MFCD / OSB STAT (number not stated) — `read + command`; which key is not stated (LMFD_01 … LMFD_20 / RMFD_01 … RMFD_20)
- STARTUP #140: MFCD / STAT page 2 scroll OSBs (numbers not stated) — `read + command`; which key is not stated (LMFD_01 … LMFD_20 / RMFD_01 … RMFD_20)
- STARTUP #141: MFCD / OSB SLEW rate (number not stated) — `read + command`; which key is not stated (LMFD_01 … LMFD_20 / RMFD_01 … RMFD_20)
- STARTUP #142: MFCD / OSB DSMS (number not stated) — `read + command`; which key is not stated (LMFD_01 … LMFD_20 / RMFD_01 … RMFD_20)
- STARTUP #143: MFCD / Profile data fields (OSBs not stated) — `read + command`; which key is not stated (LMFD_01 … LMFD_20 / RMFD_01 … RMFD_20)
- STARTUP #151: CDU / Alignment page GROUND/NAV line select key (line not stated) — `read + command`; which key is not stated (CDU_LSK_3L, CDU_LSK_5L, CDU_LSK_7L, CDU_LSK_9L / CDU_LSK_3R, CDU_LSK_5R, CDU_LSK_7R, CDU_LSK_9R)

#### Rows without an identifier (11)

- STARTUP #14: Throttles / 5. Pinky Switch — keybind
- STARTUP #18: Throttles / 2. Speed Brake — keybind
- STARTUP #103: Control Stick / Stick movement (not in PANELS.md) — not in PANELS.md; no DCS-BIOS control for stick movement (STICK_HIDE only hides the stick model)
- STARTUP #108: Throttles / 2. Speed Brake — keybind
- STARTUP #110: Throttles / 2. Speed Brake — keybind
- STARTUP #111: Control Stick / Stick movement (not in PANELS.md) — not in PANELS.md; no DCS-BIOS control for stick movement (STICK_HIDE only hides the stick model)
- STARTUP #112: Throttles / 2. Speed Brake — keybind
- STARTUP #115: Control Stick / 7. Trim Switch — keybind
- STARTUP #122: Heads Up Display Area Above Dash / 3. Heads-Up Display (HUD) — export
- STARTUP #136: MFCD / TAD datalink symbol (hook control not stated) — export; hook control not stated, and the MFCD screen has no DCS-BIOS output
- STARTUP #162: Control Stick / Paddle switch (not in PANELS.md) — not in PANELS.md; no DCS-BIOS control found for the paddle switch
