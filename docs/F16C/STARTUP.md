# F-16C Viper – cold start sequence

Cold-start sequence taken from the Aircraft Start and Before Taxi parts of the Procedures chapter of the DCS F-16C Early Access Guide (pp. 133–142, see [RESEARCH.md](RESEARCH.md)), written in our own words. Page numbers are the manual's pages; controls are named as in [PANELS.md](PANELS.md), and a control missing there is flagged in its Control cell. Rows are numbered continuously through the file. The sequence ends with Before Taxi steps 1 to 6 (p. 142); steps 7 to 10 of that list belong to the Taxi stage and are not included.

## Before Engine Start (p. 135)

The manual starts with the walkaround done and the pilot strapped in, with oxygen hoses and communications leads connected (p. 134). It lists no switch sweep before the first step.

| # | Panel | Control | Action / position | Wait for / check |
| --- | --- | --- | --- | --- |
| 1 | ELEC Control Panel | 1. MAIN PWR Switch | BATT | Battery power is limited: do not leave the switch in BATT or MAIN PWR for more than 5 minutes without starting the engine or applying external power |
| 2 | ELEC Control Panel | 10. ACFT BATT FLCS RLY Light | Check | Lit |
| 3 | TEST Panel | 7. FLCS PWR TEST Switch | TEST and hold |  |
| 4 | ELEC Control Panel | 3. FLCS PMG Light | Check | Lit |
| 5 | ELEC Control Panel | 9. ACFT BATT TO FLCS Light | Check | Lit |
| 6 | ELEC Control Panel | 10. ACFT BATT FLCS RLY Light | Check | Out |
| 7 | TEST Panel | 6. FLCS PWR Lights | Check lights A, B, C and D | All four lit |
| 8 | TEST Panel | 7. FLCS PWR TEST Switch | Release |  |
| 9 | ELEC Control Panel | 1. MAIN PWR Switch | MAIN PWR |  |
| 10 | Right Eyebrow Lights | 2. ENGINE warning light | Check | Lit |
| 11 | Right Eyebrow Lights | 3. HYD / OIL PRESS warning lights | Check | Lit |
| 12 | Caution Light Panel | ELEC SYS | Check | Lit |
| 13 | Caution Light Panel | SEC | Check | Lit |
| 14 | ELEC Control Panel | 10. ACFT BATT FLCS RLY Light | Check | Lit |
| 15 | ELEC Control Panel | 6. EPU GEN Light; 7. EPU PMG Light | Check | Both out. If either is lit, the EPU activation criteria are met and the EPU would fire if ground crew pulled its safety pin: set MAIN PWR to OFF and abort (restart the mission) |
| 16 | Communications | Radio calls (not in PANELS.md) | Establish contact with ground crew and ATC as needed for engine start | Radio and frequency: not stated |
| 17 | Canopy Switch and Canopy Handle | 1. Canopy Switch | As desired | Control not named by the manual; position: not stated |
| 18 | Ground crew | Chocks (not in PANELS.md) | In place |  |
| 19 | Ground crew | Ground crew position (not in PANELS.md) | Confirm clear of the intake and other danger areas |  |

## Engine Start (p. 136)

| # | Panel | Control | Action / position | Wait for / check |
| --- | --- | --- | --- | --- |
| 20 | ENG & JET START Control Panel | 2. JET FUEL JFS Switch | START 2 | Engine RPM starts to rise |
| 21 | ENG & JET START Control Panel | 1. JET FUEL RUN light | Check | Lit within 30 s of the JFS start |
| 22 | ELEC Control Panel | 10. ACFT BATT FLCS RLY Light | Check | Out (the flight control relays are powered once either JFS start position is selected) |
| 23 | ELEC Control Panel | 9. ACFT BATT TO FLCS Light | Check | Lit |
| 24 | Caution Light Panel | SEC | Check | Out |
| 25 | Throttle | Throttle lever | Advance from OFF to IDLE | Only at 20 percent RPM or more; combustion within a few seconds, RPM and FTIT rise. On battery power only, just the RPM and FTIT gauges work until the standby generator is online |
| 26 | Right Eyebrow Lights | 2. ENGINE warning light | Check | Out at about 60 percent RPM, when the standby generator comes online |
| 27 | Caution Light Panel | SEAT NOT ARMED | Check | Lit (shows the standby generator feeds the emergency busses) |
| 28 | Landing Gear Panel | 3. WHEELS Down Lights | Check | Three green lit. Within 5 to 10 s the main generator takes over and the standby generator goes offline |
| 29 | ENG & JET START Control Panel | 2. JET FUEL JFS Switch | Confirm OFF; set it to OFF by hand if needed | Engine at idle speed |
| 30 | Right Eyebrow Lights | 3. HYD / OIL PRESS warning lights | Check | Out |
| 31 | Fuel Flow Indicator | Fuel flow pointer | Check | 700 to 1,700 PPH |
| 32 | Engine Instruments | 1. Engine OIL pressure indicator | Check | 15 PSI or more |
| 33 | Engine Instruments | 2. Engine NOZ POS indicator | Check | Above 94 percent |
| 34 | Engine Instruments | 3. Engine RPM indicator | Check | 62 to 80 percent |
| 35 | Engine Instruments | 4. Engine FTIT indicator | Check | 650 C or less |
| 36 | Hydraulic Pressure Indicators | HYD PRESS A gauge | Check | 2,850 to 3,250 PSI |
| 37 | Hydraulic Pressure Indicators | HYD PRESS B gauge | Check | 2,850 to 3,250 PSI |

## After Engine Start (pp. 137 to 140)

| # | Panel | Control | Action / position | Wait for / check |
| --- | --- | --- | --- | --- |
| 38 | TEST Panel | 4. PROBE HEAT Switch | HEAT | PROBE HEAT caution (Caution Light Panel) out. If it is lit, a probe heater or the monitoring system has failed |
| 39 | TEST Panel | 4. PROBE HEAT Switch | TEST | PROBE HEAT caution flashes 3 to 5 times a second; if not, the monitoring system is inoperative |
| 40 | TEST Panel | 4. PROBE HEAT Switch | OFF |  |
| 41 | TEST Panel | 1. FIRE & OHEAT DETECT Test Button | Press | ENG FIRE warning light comes on (checks the fire and overheat detection loops) |
| 42 | TEST Panel | 3. MAL & IND LTS Test Button | Press | All warning, caution and indicator lights on; a short gear horn, then the voice messages in priority order |
| 43 | AVIONICS POWER Control Panel | 1. MMC Switch | MMC (PANELS.md: ON) |  |
| 44 | AVIONICS POWER Control Panel | 2. ST STA Switch | ST STA (PANELS.md: ON) |  |
| 45 | AVIONICS POWER Control Panel | 3. MFD Switch | MFD (PANELS.md: ON) |  |
| 46 | AVIONICS POWER Control Panel | 4. UFC Switch | UFC (PANELS.md: ON) |  |
| 47 | AVIONICS POWER Control Panel | 6. GPS Switch | GPS (PANELS.md: ON) | The receiver needs a clear view of the sky; inside a hangar or shelter, GPS time and position may not arrive until the aircraft has taxied clear |
| 48 | AVIONICS POWER Control Panel | 8. INS Knob | Align; ALIGN NORM is the setting the auto-start leaves (p. 134) | The manual refers to its INS Alignment section; alignment time: not stated on these pages |
| 49 | AVIONICS POWER Control Panel | 7. DL Switch | DL (PANELS.md: ON) | Not implemented |
| 50 | Data Entry Display (DED) | DED window | Check the TIME page | "GPS SYSTEM" shown once the GPS timing signal is received. Opening the page: not stated here |
| 51 | AVIONICS POWER Control Panel | 9. MIDS LVT Knob | ON | Only after the GPS receiver is powered and its timing signal received |
| 52 | SNSR PWR Control Panel | 1. LEFT HDPT Switch | As required; power the hardpoint if an HTS pod is fitted |  |
| 53 | SNSR PWR Control Panel | 2. RIGHT HDPT Switch | As required; power the hardpoint if a targeting pod is fitted |  |
| 54 | SNSR PWR Control Panel | 3. FCR Switch | FCR (PANELS.md: ON) |  |
| 55 | SNSR PWR Control Panel | 4. RDR ALT Switch | RDR ALT |  |
| 56 | HUD Control Panel | (whole panel) | As desired | Settings: not stated |
| 57 | Integrated Control Panel (ICP) | 3. SYM Knob | Rotate up, as needed, to raise HUD brightness |  |
| 58 | IFF Control Panel | 3. C & I Knob | UFC |  |
| 59 | ENG & JET START Control Panel | 3. ENG CONT Switch | SEC (check may be left for the Before Takeoff check) | SEC caution lit; RPM settles, after a drop of up to 10 percent from the PRI value, and may sit up to 5 percent lower than in PRI |
| 60 | Throttle | Throttle lever | Snap to MIL, then snap to IDLE once RPM reaches 85 percent | Normal indications and smooth running |
| 61 | Engine Instruments | 2. Engine NOZ POS indicator | Check | 10 percent or less within 30 s of selecting SEC |
| 62 | ENG & JET START Control Panel | 3. ENG CONT Switch | PRI | SEC caution out; NOZ POS above 94 percent |
| 63 | Side Stick Controller (SSC) | Stick movement (not in PANELS.md) | Cycle the flight controls to full deflection of all surfaces before the FLCS BIT | Pedals are not mentioned by the manual |
| 64 | FLT CONTROL Panel | 7. FLCS BIT Switch | BIT | RUN light lit for about 45 s until the BIT ends; the switch returns to OFF by itself |
| 65 | FLT CONTROL Panel | 4. FLCS RUN / FAIL Indicator Lights | Check when the BIT ends | FAIL light not lit |
| 66 | ECM Control Panel | 1. ECM Power Switch | As required; STBY if an ECM pod is fitted |  |
| 67 | Throttle | 6. SPD BRK Switch (3-position, aft momentary) | Extend (aft), then retract (fwd) |  |
| 68 | Landing Gear Panel | 3. WHEELS Down Lights | Check | Three green lit |
| 69 | Standby Attitude Indicator (SAI) | 6. PULL TO CAGE Knob | Uncage and set | How to uncage and the value to set: not stated |
| 70 | FUEL QTY SEL Panel | 1. FUEL QTY SEL Knob | TEST | FR and AL needles at 2,000 lb (within 100); totalizer 6,000 lb (within 100); FWD FUEL LOW and AFT FUEL LOW cautions lit |
| 71 | FUEL QTY SEL Panel | 1. FUEL QTY SEL Knob | NORM | AL about 2,810 lb and FR about 3,250 lb, if fully fuelled with JP-8 |
| 72 | FUEL QTY SEL Panel | 1. FUEL QTY SEL Knob | RSVR | Each reservoir about 480 lb |
| 73 | FUEL QTY SEL Panel | 1. FUEL QTY SEL Knob | INT WING | Each wing about 550 lb |
| 74 | FUEL QTY SEL Panel | 1. FUEL QTY SEL Knob | EXT WING | Each external wing tank about 2,420 lb, if full |
| 75 | FUEL QTY SEL Panel | 1. FUEL QTY SEL Knob | EXT CTR | FR about 1,890 lb, if full; AL at 0 |
| 76 | FUEL QTY SEL Panel | 1. FUEL QTY SEL Knob | As desired | Setting: not stated |
| 77 | EPU Fuel Quantity Indicator | EPU fuel gauge | Check | 95 to 102 percent |
| 78 | Avionics, MFDs and radios | Controls not named (not in PANELS.md) | Configure as required | Settings: not stated |
| 79 | MFD Format Selection Master Menu | 12. DTE Format | Open the DTE format (the manual points to the DTE MFD format) | OSB for this step: not stated |
| 80 | Multi-Function Display (MFD) bezel | DTC upload OSB (not in PANELS.md; number not stated) | Upload the DTC | Upload method: not stated |
| 81 | HMCS Control Panel | HMCS alignment (not in PANELS.md) | Align, if an HMCS is installed | Steps are in the manual's HMCS alignment section, not covered here |
| 82 | FLT CONTROL Panel | 1. DIGITAL BACKUP Switch | BACKUP, after the FLCS BIT is complete | DBU ON warning light (Right Eyebrow Lights) lit |
| 83 | Side Stick Controller (SSC) | Stick movement (not in PANELS.md) | Operate the flight controls | All surfaces respond normally |
| 84 | FLT CONTROL Panel | 1. DIGITAL BACKUP Switch | OFF | DBU ON warning light out |
| 85 | MANUAL TRIM Panel | 4. TRIM/AP DISC Switch | DISC |  |
| 86 | Side Stick Controller (SSC) | 2. Trim Switch (4-way) | Activate in roll and in pitch | No control surface movement and no motion of the trim wheel indicators (the manual names the FLT CONTROL Panel; PANELS.md puts the wheels on the MANUAL TRIM Panel) |
| 87 | MANUAL TRIM Panel | 4. TRIM/AP DISC Switch | NORM |  |
| 88 | Side Stick Controller (SSC) | 2. Trim Switch (4-way) | Check, then centre | Control surfaces move and the trim wheel indicators move |
| 89 | MANUAL TRIM Panel | 2. YAW TRIM Knob | Check rudder trim, then centre |  |
| 90 | Side Stick Controller (SSC) | Stick movement (not in PANELS.md) | Full forward and hold | Note the horizontal tail deflection |
| 91 | Manual Pitch Override Switch | MANUAL PITCH override switch | OVRD and hold | Horizontal tail trailing edges deflect further downward |
| 92 | Manual Pitch Override Switch | MANUAL PITCH override switch | Release |  |
| 93 | Side Stick Controller (SSC) | Stick movement (not in PANELS.md) | Release the stick | Horizontal tail returns to its original position |
| 94 | Side Stick Controller (SSC) | Stick movement (not in PANELS.md) | Operate the flight controls | All surfaces respond normally; no FLCS lights lit |
| 95 | FUEL Control Panel | 4. AIR REFUEL Switch | OPEN, if air refuelling is required | RDY light lit and DISC light out (AR Status / NWS Indicator) |
| 96 | FUEL Control Panel | 4. AIR REFUEL Switch | CLOSE | RDY light out |
| 97 | ELEC Control Panel | 6. EPU GEN Light; 7. EPU PMG Light | Confirm both out |  |
| 98 | EPU Control Panel | 1. EPU Switch | Only if either light above is lit: OFF, then back to NORM | If either light stays lit, abort (restart the mission) |
| 99 | OXYGEN Regulator Panel | 4. Diluter Lever | 100% | Start of the EPU check (may be done during the Before Takeoff check) |
| 100 | Throttle | Throttle lever | Raise engine RPM 10 percent above normal idle |  |
| 101 | TEST Panel | 5. EPU/GEN Switch | EPU/GEN and hold (PANELS.md: TEST) |  |
| 102 | EPU Control Panel | 3. AIR Light | Check | Lit |
| 103 | EPU Control Panel | 2. EPU Run Light | Check | Lit for at least 5 s |
| 104 | ELEC Control Panel | 6. EPU GEN Light; 7. EPU PMG Light | Check | Both out, but either may come on briefly at the start of the test |
| 105 | TEST Panel | 6. FLCS PWR Lights | Check lights A, B, C and D | All four lit |
| 106 | TEST Panel | 5. EPU/GEN Switch | OFF |  |
| 107 | Throttle | Throttle lever | IDLE |  |
| 108 | OXYGEN Regulator Panel | 4. Diluter Lever | NORMAL (PANELS.md: NORM) |  |

## Before Taxi (p. 142)

| # | Panel | Control | Action / position | Wait for / check |
| --- | --- | --- | --- | --- |
| 109 | Canopy Switch and Canopy Handle | 1. Canopy Switch | Close (PANELS.md: down, held until closed) |  |
| 110 | Canopy Switch and Canopy Handle | 2. Canopy Lever | Lock (PANELS.md: locked, closed against the wall) | CANOPY warning light (Right Eyebrow Lights) out, per PANELS.md |
| 111 | UHF Backup Control Panel | (whole panel) | Set and check as required | Settings: not stated |
| 112 | Altimeter | 6. Barometric Setting Knob | Set the altimeter |  |
| 113 | Altimeter | 7. Altimeter Mode Switch | Read the altimeter in ELEC and in PNEU (PANELS.md: ELEC; PNEU held) | Each within 75 ft of a known elevation and within 75 ft of each other |
| 114 | Head-Up Display (HUD) | Combining glass | Check the altitude shown | Matches the altimeter |
| 115 | EXT LIGHTING Control Panel | (whole panel) | As required | Settings: not stated |
| 116 | AVIONICS POWER Control Panel | 8. INS Knob | NAV | For a complete alignment before taxi: "RDY" flashing on the INS DED page and/or "ALIGN" flashing at the lower left of the HUD. Opening the INS DED page: not stated |
| 117 | Ground crew | Chocks (not in PANELS.md) | Remove |  |

## Automatic start

Page 134 says the F-16C can also be started by an auto-start sequence: Left Windows + Home starts it and Left Windows + End stops it. When it finishes, the INS knob is at ALIGN NORM and must be moved to NAV before taxi. The IFF MASTER knob is at STBY, the ALR-56M radar warning receiver is powered off, the CMDS MODE knob is at OFF and the ECM power switch is at OFF (the pod needs a 3-minute warm-up before use).
