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
