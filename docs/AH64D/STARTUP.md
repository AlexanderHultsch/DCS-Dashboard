# AH-64D Apache – cold start sequence

Cold-start sequence taken from the Aircraft Start and Taxi & Before Takeoff parts of the Procedures chapter of the DCS AH-64D Flight Manual (pp. 255–266, see [RESEARCH.md](RESEARCH.md)), written in our own words. Page numbers are the manual's pages; controls are named as in [PANELS.md](PANELS.md), and a control missing there is flagged in its Control cell. Rows are numbered continuously through the file. Only the pilot's (rear seat) steps are included: the manual's separate CP/G (front seat) lists are left out, and where a step says "PLT & CPG" or "PLT / CPG" only the pilot's half is written. The sequence runs from the interior checks to the end of Before Takeoff (p. 266); the Hover Power Check that closes that list belongs to the next section of the manual and is not included.

## Interior Checks (pp. 255 to 256)

The manual starts with the walkaround done, the pilot strapped in, and the intercom cables and the helmet-tracking connectors plugged in (p. 255). These checks are done before any electrical power is applied and before the APU is started. This is the "Prior to Starting APU" part of the chapter.

| # | Panel | Control | Action / position | Wait for / check |
| --- | --- | --- | --- | --- |
| 1 | Canopy door | Canopy door (not in PANELS.md) | Open, or an intermediate position, as desired |  |
| 2 | Exterior Lighting / Interior Lighting Panel | 1. NAV Switch | Set as local procedures require | Position: not stated |
| 3 | Exterior Lighting / Interior Lighting Panel | 7. ANTI COLL Switch | OFF |  |
| 4 | Exterior Lighting / Interior Lighting Panel | 2. SIGNAL Knob; 3. PRIMARY Knob; 5. FLOOD Knob; 6. STBY INST Knob | As desired | The manual says only "interior lighting knobs"; which knobs is our reading |
| 5 | Power Quadrant Panel | 6. ENG POWER Levers | OFF (both levers) |  |
| 6 | Power Quadrant Panel | 5. ENG START Switches | OFF (both switches) |  |
| 7 | Power Quadrant Panel | 1. RTR BRK Switch | OFF |  |
| 8 | Tail Wheel / NVS Mode Panel | 2. NVS MODE Switch | OFF |  |
| 9 | Keyboard Unit (KU) | 7. Display Brightness Knob | As desired |  |
| 10 | Enhanced Up-Front Display (EUFD) | 5. Brightness Control Knob | As desired |  |
| 11 | Multi-Purpose Displays (MPD) | 3. BRT Knob; 4. Mode Knob | As desired | The manual does not say which MPD |
| 12 | Parking Brake Handle | PARK BRAKE Handle | Pulled out | Brakes set |
| 13 | Standby Attitude Indicator | 8. PULL TO CAGE Knob | Caged | Check |
| 14 | CMWS Control Panel | 2. Power/Test Knob | OFF | The manual calls it the PWR knob |
| 15 | CMWS Control Panel | 5. ARM/SAFE Switch | SAFE |  |
| 16 | CMWS Control Panel | 6. CMWS/NAV Switch | As appropriate | Position: not stated |
| 17 | CMWS Control Panel | 8. BYPASS/AUTO Switch | As appropriate | Position: not stated |
| 18 | CMWS Control Panel | 7. JETTISON Switch | Down, cover closed |  |
| 19 | Communications Panel | 1. FM1 Knob; 2. FM2 Knob; 3. HF Knob; 4. VHF Knob; 5. UHF Knob; 8. MASTER Knob | As desired | The manual says only "audio volume knobs"; which knobs is our reading |
| 20 | Communications Panel | 9. ICS Switch; 7. SENS Knob | As desired |  |
| 21 | Helmet Display Unit (HDU) | HDU (not in PANELS.md) | As desired | Settings: not stated |

## Battery Checks (p. 257)

The manual assumes the interior checks above are complete.

| # | Panel | Control | Action / position | Wait for / check |
| --- | --- | --- | --- | --- |
| 22 | Power Quadrant Panel | 2. MSTR IGN Knob | BATT; EXT PWR if external power is to be used |  |
| 23 | Tail Wheel / NVS Mode Panel | 1. TAIL WHEEL Button; UNLOCK light | Check that the wheel is locked | UNLOCK light out |
| 24 | Communications Panel | 9. ICS Switch | Check the intercom with the other crew station | Control not named by the manual; the exchange is with the CP/G |
| 25 | Exterior Lighting / Interior Lighting Panel | 8. PRESS TO TEST Button | Press and hold | All signal lights lit |
| 26 | Master Warning / Master Caution Lighted Pushbuttons | 1. MSTR WARN light; 2. MSTR CAUT light | Check | No unexpected malfunction indication |
| 27 | Enhanced Up-Front Display (EUFD) | 2. Warning Message Area; 3. Caution Message Area | Check | No unexpected malfunction message |
| 28 | Fire Detection / Extinguishing Panel (FIRE DET/EXTG) | 5. TEST Switch | TEST 1 and hold | Pilot and CP/G both check the items below |
| 29 | Master Warning / Master Caution Lighted Pushbuttons | 1. MSTR WARN light | Check | Flashing |
| 30 | Fire Detection / Extinguishing Panel (FIRE DET/EXTG) | 1. ENG 1 FIRE light; 2. APU FIRE light; 3. ENG 2 FIRE light | Check | All three lit |
| 31 | Enhanced Up-Front Display (EUFD) | 2. Warning Message Area | Check | AFT DECK FIRE message shown |
| 32 | Audio | Voice warnings (not in PANELS.md) | Listen | ENG 1 FIRE, APU FIRE, ENG 2 FIRE and AFT DECK FIRE heard one after the other |
| 33 | Fire Detection / Extinguishing Panel (FIRE DET/EXTG) | 5. TEST Switch | TEST 2 and hold | The manual has the CP/G hold this one while both crew check; the pilot only checks. Whether TEST 1 is released first: not stated |
| 34 | Master Warning / Master Caution Lighted Pushbuttons | 1. MSTR WARN light | Check | Flashing |
| 35 | Fire Detection / Extinguishing Panel (FIRE DET/EXTG) | 1. ENG 1 FIRE light; 2. APU FIRE light; 3. ENG 2 FIRE light | Check | All three lit |
| 36 | Fire Detection / Extinguishing Panel (FIRE DET/EXTG) | 4. PRI DISCH light; 6. RES DISCH light | Check | Both lit |
| 37 | Enhanced Up-Front Display (EUFD) | 2. Warning Message Area | Check | AFT DECK FIRE message shown |
| 38 | Audio | Voice warnings (not in PANELS.md) | Listen | The same four voice warnings as in the TEST 1 check |

## APU Start (p. 258)

The manual assumes the battery checks are complete. The start is fully automatic: no further crew action is needed once the button is pressed.

| # | Panel | Control | Action / position | Wait for / check |
| --- | --- | --- | --- | --- |
| 39 | Power Quadrant Panel | 4. APU Button | Press and release | Automatic start sequence runs |
| 40 | Enhanced Up-Front Display (EUFD) | 4. Advisory Message Area | Check | APU ON message shown (PANELS.md also lists an APU ON light on the button) |
| 41 | Power Quadrant Panel | 2. MSTR IGN Knob | BATT, only if external power was used before the APU start |  |

## After Starting APU (p. 258)

The manual assumes the APU is running and the MPDs have finished initialising.

| # | Panel | Control | Action / position | Wait for / check |
| --- | --- | --- | --- | --- |
| 42 | Canopy door | Canopy door (not in PANELS.md) | Close |  |
| 43 | Multi-Purpose Displays (MPD) | DTU page, MASTER LOAD option (page function, not in PANELS.md; button not stated) | Select | Uploads the DTC mission data into the aircraft systems. Opening the DTU page: not stated here |

## Initialize Aircraft Systems (pp. 258 to 262)

After the master load the remaining options are set in each seat (the "DMS sweep"). The manual says the order is up to the crew, but settings common to both seats must be agreed with the other crew member, so the crew should work in step. The manual gives an example sweep (pp. 259 to 262); it is written here as one row per page or sub-page, with the options set on it in the Action cell (VAB = Variable Action Button, with its position on the bezel). The manual's example does not say which MPD is used. Options the manual marks as common to both seats are tagged (common). Parts of the example that are for the CP/G (WPN page UTIL / TADS / LASER, TDU controls, Sight Select) are left out.

| # | Panel | Control | Action / position | Wait for / check |
| --- | --- | --- | --- | --- |
| 44 | Multi-Purpose Displays (MPD) | 7. M Button (VAB B1) | Press | Menu page shown |
| 45 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons L1 to L6 (left column): L3, ASE (page function, not in PANELS.md) | Select the ASE page; set AUTOPAGE (R1) as desired |  |
| 46 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons T1 to T6 (top row): T6, UTIL on the ASE page (page function, not in PANELS.md) | Select the UTIL sub-page; press RLWR power (R4) (common); set RLWR VOICE (R5) (common); set chaff MODE (L1) (common); set the chaff program with L2 to L5 (common) | Values: not stated |
| 47 | Multi-Purpose Displays (MPD) | 6. Fixed Action Button TSD | Press | TSD page shown |
| 48 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons T1 to T6 (top row): T3, SHOW on the TSD page (page function, not in PANELS.md) | Select SHOW and set the NAV options; with PHASE (B2) on ATK set the ATK options, then THRT SHOW (T5) and COORD SHOW (T6) options; put PHASE (B2) back to NAV and set the NAV COORD SHOW options; deselect SHOW | Option values: not stated |
| 49 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons T1 to T6 (top row): T6, UTIL on the TSD page (page function, not in PANELS.md) | Select the UTIL sub-page; set TIME (R2) to Zulu or local (common); update the local time with SYSTEM TIME> (R3) if needed (common); deselect UTIL | Entering the time uses the KU; steps: not stated |
| 50 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons R1 to R6 (right column): R1 and R2, map scale (page function, not in PANELS.md) | Set the scale as desired (common); set CTR (R3) as desired (common) |  |
| 51 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons B1 to B6 (bottom row): B5, RTE on the TSD page (page function, not in PANELS.md) | Select RTE; pick the route with RTM (B6) (common); set DIR (L5) to the wanted point if needed (common); deselect RTE |  |
| 52 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons B1 to B6 (bottom row): B4, MAP on the TSD page (page function, not in PANELS.md) | Select MAP; set TYPE (L2), COLOR BAND (L4), GRID (T5) and ORIENT (R5) as desired; deselect MAP |  |
| 53 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons L1 to L6 (left column): L1, INST on the TSD page (page function, not in PANELS.md) | Select only if the ADF will be used for navigation; then UTIL (T6), turn the ADF on with B6 if needed (common), configure it (common), deselect UTIL and INST | ADF settings: not stated |
| 54 | Multi-Purpose Displays (MPD) | 6. Fixed Action Button WPN | Press | WPN page shown |
| 55 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons L1 to L6 (left column): L6, GRAYSCALE on the WPN page (page function, not in PANELS.md) | Select | Grayscale test picture shown |
| 56 | Video Panel | 1. IHADSS BRT Knob (outer); 1. IHADSS CON Knob (inner) | Adjust for the best helmet display video | Values: not stated |
| 57 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons L1 to L6 (left column): L6, GRAYSCALE on the WPN page (page function, not in PANELS.md) | Deselect |  |
| 58 | Video Panel | 2. SYM BRT Knob | As desired |  |
| 59 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons B1 to B6 (bottom row): B5, BORESIGHT on the WPN page (page function, not in PANELS.md) | Select and do the IHADSS boresight procedure, then deselect BORESIGHT | The procedure is in a separate section of the manual, not covered here |
| 60 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons B1 to B6 (bottom row): B2, GUN on the WPN page (page function, not in PANELS.md) | Select GUN; choose the burst limit with L1 to L5; choose the MODE (R2) | Values: not stated |
| 61 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons B1 to B6 (bottom row): B3, MSL on the WPN page (page function, not in PANELS.md) | Select MSL; CODE (T4); with SET (T2) set the LRFD code, then the LST code (common); open CHAN (T1) and make sure one of channels 1 to 4 matches the LRFD code (common), then deselect CHAN; PRI (L1) = channel matching the LRFD (common); ALT (L2) = channel matching the LST, or as appropriate (common) | Code values: not stated |
| 62 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons B1 to B6 (bottom row): B5, RKT on the WPN page (page function, not in PANELS.md) | Select RKT; choose INVENTORY (L1 to L5) and QTY (R1); deselect RKT |  |
| 63 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons R1 to R6 (right column): R6, ACQ on the WPN page (page function, not in PANELS.md) | Set as desired | The CP/G must pick SLAVE for the cueing to appear in the helmet flight symbology |
| 64 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons B1 to B6 (bottom row): B6, MANRNG> on the WPN page (page function, not in PANELS.md) | Set the manual range, or enter A for automatic ranging | Data entry on the KU |
| 65 | Multi-Purpose Displays (MPD) | 6. Fixed Action Button FCR | Press | FCR page shown |
| 66 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons T1 to T6 (top row): T1, C SCP on the FCR page (page function, not in PANELS.md) | Select as desired |  |
| 67 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons T1 to T6 (top row): T6, UTIL on the FCR page (page function, not in PANELS.md) | Select the UTIL sub-page; set MMA (R6) to NORM to bring up the FCR (common); pick the priority SCHEME (R4) (common) | MMA state: not shown by the manual |
| 68 | Multi-Purpose Displays (MPD) | 6. Fixed Action Button A/C | Press | A/C page shown |
| 69 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons T1 to T6 (top row): T2, FLT on the A/C page (page function, not in PANELS.md) | Select FLT; open SET (B6); set HI> (T1) and LO> (T3) (common); set UNIT (T4); set the airfield elevation with ALT> (T5), or the altimeter setting with PRES> (T6), whichever is known (common); set UNIT (B2); close SET (B6) | Values: not stated |
| 70 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons T1 to T6 (top row): T3, FUEL on the A/C page (page function, not in PANELS.md) | Select FUEL; open CHECK (B6); pick MINUTES with R2 to R4 (common); close CHECK |  |
| 71 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons T1 to T6 (top row): T4, PERF on the A/C page (page function, not in PANELS.md) | Select PERF; for the MAX mode (B3) and then the PLAN mode (B4) set PA> (L1), FAT> (L2) and GWT> (L3) (common); then pick the CUR mode (B2) | Values: not stated |
| 72 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons T1 to T6 (top row): T6, UTIL on the A/C page (page function, not in PANELS.md) | Select the UTIL sub-page; set the anti-ice SYSTEM (R1) (common); if SYSTEM is MANUAL, set the anti-ice options with R3 to R6 (common) |  |
| 73 | Multi-Purpose Displays (MPD) | 6. Fixed Action Button COM | Press | COM page shown |
| 74 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons L1 to L6 (left column): L1 to L5, radio presets on the COM page (page function, not in PANELS.md) | Pick the radio (T1 to T5), choose the TUNE option (B2), set TUNE Radio to SC (B6); select and tune the presets with L1 to L5 and R1 to R5 (common) | Frequencies: not stated |
| 75 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons T1 to T6 (top row): T3, XPNDR on the COM page (page function, not in PANELS.md) | Select XPNDR; pick the MODE (L1 to L6); set MODE 1> (R1), MODE 2> (R2), MODE 3> (R3) and MODE 4 (R4); pick REPLY (B4) (all common) | Codes: not stated |
| 76 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons T1 to T6 (top row): T4, UHF on the COM page (page function, not in PANELS.md) | Select UHF; set GUARD RECEIVER (L6) as desired (common) |  |
| 77 | Multi-Purpose Displays (MPD) | 1. Variable Action Buttons T1 to T6 (top row): T5, FM on the COM page (page function, not in PANELS.md) | Select FM; open SET (B5); set POWER (L5) as appropriate (common) |  |
| 78 | CMWS Control Panel | 2. Power/Test Knob | ON | The manual calls it the Power/Set knob; a built-in test runs by itself after it initialises (PANELS.md) |

## Engine Start (p. 263)

The manual assumes the APU is running and the aircraft systems are set up. Engine 1 is started first, then engine 2. The APU must keep running until both ENG POWER levers are at FLY and NR has settled at 101 %; otherwise the AC generators drop off line and the primary electrical power is lost.

| # | Panel | Control | Action / position | Wait for / check |
| --- | --- | --- | --- | --- |
| 79 | Tail Wheel / NVS Mode Panel | 2. NVS MODE Switch | As desired | Position: not stated |
| 80 | Standby Attitude Indicator | 8. PULL TO CAGE Knob | Uncage | OFF flag out |
| 81 | Ground crew | Area around the helicopter (not in PANELS.md) | Confirm clear | Not a switch; confirm with the ground crew |
| 82 | Power Quadrant Panel | 1. RTR BRK Switch | OFF; LOCK for a rotor lock start | The start itself is the same in both cases |
| 83 | Exterior Lighting / Interior Lighting Panel | 7. ANTI COLL Switch | WHT by day, RED by night |  |
| 84 | Power Quadrant Panel | 5. ENG START Switches | Engine 1 switch to START | ENG 1 START advisory on the EUFD and the START box on the ENG page. Abort (that engine's ENG POWER lever to OFF) if TGT looks set to pass 851 C before NG reaches the 63 % idle, if there is no rise of TGT, NP or engine oil pressure 45 s after the lever goes to IDLE, or if the ENG START advisory disappears before NG reaches 52 % |
| 85 | Power Quadrant Panel | 6. ENG POWER Levers | Engine 1 lever to IDLE | At the first sign of NG rising and only with TGT below 80 C |
| 86 | Enhanced Up-Front Display (EUFD) | 4. Advisory Message Area | Monitor the engine 1 start | Together with engine TGT, NG and oil pressure on the ENG page (next row) |
| 87 | Multi-Purpose Displays (MPD) | ENG page: TGT, NG and ENG OIL PSI (page function, not in PANELS.md) | Monitor the engine 1 start | Start proceeds normally; abort conditions in the ENG START row above |
| 88 | Power Quadrant Panel | 5. ENG START Switches | Engine 2 switch to START, once the engine 1 start is complete | ENG 2 START advisory on the EUFD and the START box on the ENG page; the same abort conditions apply |
| 89 | Power Quadrant Panel | 6. ENG POWER Levers | Engine 2 lever to IDLE | At the first sign of NG rising and only with TGT below 80 C |
| 90 | Enhanced Up-Front Display (EUFD) | 4. Advisory Message Area | Monitor the engine 2 start | Together with engine TGT, NG and oil pressure on the ENG page (next row) |
| 91 | Multi-Purpose Displays (MPD) | ENG page: TGT, NG and ENG OIL PSI (page function, not in PANELS.md) | Monitor the engine 2 start | Start proceeds normally |
| 92 | Power Quadrant Panel | 1. RTR BRK Switch | OFF |  |
| 93 | Multi-Purpose Displays (MPD) | ENG page, ENG Systems sub-page (page function, not in PANELS.md; button not stated) | Check engine oil pressure of both engines before the levers go to FLY | Below 70 PSI on both; in cold weather also NGB TEMP above 20 C |
| 94 | Power Quadrant Panel | 6. ENG POWER Levers | Both levers smoothly to FLY | TORQUE % of both engines rises together |
| 95 | Multi-Purpose Displays (MPD) | ENG page: NP and NR (page function, not in PANELS.md) | Check | Both at 101 % |
| 96 | Master Warning / Master Caution Lighted Pushbuttons | 1. MSTR WARN light; 2. MSTR CAUT light | Monitor | No malfunction indication; check the EUFD messages as well |
| 97 | Power Quadrant Panel | 4. APU Button | Press and release | Starts the APU shutdown sequence |

## Before Taxi (p. 264)

The manual assumes the engine start is complete.

| # | Panel | Control | Action / position | Wait for / check |
| --- | --- | --- | --- | --- |
| 98 | Ground crew | Chocks (not in PANELS.md) | Confirm removed with the ground crew |  |
| 99 | Multi-Purpose Displays (MPD) | UTIL page, bleed air option (page function, not in PANELS.md; button not stated) | On |  |
| 100 | Multi-Purpose Displays (MPD) | UTIL page, anti-ice options (page function, not in PANELS.md; button not stated) | As required |  |
| 101 | Exterior Lighting / Interior Lighting Panel | 1. NAV Switch | Check it is set as local procedures require | Position: not stated |
| 102 | Exterior Lighting / Interior Lighting Panel | 7. ANTI COLL Switch | Check: WHT by day, RED by night |  |
| 103 | Exterior Lighting / Interior Lighting Panel | 4. FORM Knob | Set as appropriate |  |
| 104 | Collective Flight Grip | 3. Searchlight Switch; 4. Searchlight Position Switch | As required |  |
| 105 | Parking Brake Handle | PARK BRAKE Handle | Release by pressing the wheel brakes | Handle pushed in |

## Ground Taxi (pp. 265 to 266)

The manual describes a usual way of ground taxiing (the night aids are the NVS mode and the searchlight); the flight controls themselves are not panels in PANELS.md and are flagged. Taxi stays on the ground; hover and takeoff are not part of this list.

| # | Panel | Control | Action / position | Wait for / check |
| --- | --- | --- | --- | --- |
| 106 | Cyclic Grip | 3. Symbology Select Switch | CT (forward) | Transition symbology mode |
| 107 | Cyclic Grip | 1. Force Trim/Hold Mode Switch | R (forward), press and hold |  |
| 108 | Flight controls | Collective lever (not in PANELS.md) | With the cyclic neutral, raise to 27 to 30 % | 30 to 35 % may be needed at high gross weight or high density altitude |
| 109 | Flight controls | Cyclic, pedals (not in PANELS.md) | Forward cyclic to start moving; pedals for heading and sideways cyclic to keep the fuselage level | Area clear of personnel and equipment before the tail wheel is unlocked. The horizon line of the helmet flight symbology serves as the level reference, not the slip ball. The trim may stay held or be released and pressed as needed |
| 110 | Collective Flight Grip | 8. Tail Wheel Lock/Unlock Button | Press to unlock before the first turn (either crew member may) | Whoever flies usually does this |
| 111 | Tail Wheel / NVS Mode Panel | 1. TAIL WHEEL Button; UNLOCK light | Check the wheel is unlocked | UNLOCK light lit |
| 112 | Flight controls | Cyclic, pedals (not in PANELS.md) | Turn: pedal toward the turn with cyclic in the same direction; use alternating pressure and counter-pressure on the pedals for a steady turn |  |
| 113 | Collective Flight Grip | 8. Tail Wheel Lock/Unlock Button | Press to lock before stopping or lifting off | UNLOCK light out. The TAIL WHEEL LOCK SEL and UNLK SEL advisories on the EUFD show only the commanded state; only the light shows the physical state |
| 114 | Tail Wheel / NVS Mode Panel | 1. TAIL WHEEL Button; UNLOCK light | Check the wheel is locked | UNLOCK light out |
| 115 | Flight controls | Cyclic, collective, wheel brakes (not in PANELS.md) | Aft cyclic to slow down; when stopped, centre the cyclic before lowering the collective; the wheel brakes may help |  |
| 116 | Items named only in the pilot overview figure | Anti-Torque Pedals | Press the toe brakes lightly in each crew station | Brakes work |
| 117 | Multi-Purpose Displays (MPD) | ENG page (page function, not in PANELS.md; button not stated) | Check | NP and NR at 101 %, all indications green |
| 118 | Multi-Purpose Displays (MPD) | FLT page (page function, not in PANELS.md; button not stated) | Check; update the altimeter setting if needed |  |
| 119 | Standby Altimeter | 5. Barometric Setting Knob | Check the standby instruments; update the altimeter setting if needed |  |

## Before Takeoff (p. 266)

The manual assumes the helicopter is at the departure point before lifting to a hover or taking off. The list has switch checks, so it is included. Its last step, the Hover Power Check, belongs to the next section of the manual and is not included.

| # | Panel | Control | Action / position | Wait for / check |
| --- | --- | --- | --- | --- |
| 120 | Armament Panel | 1. SAFE light | Check | Lit |
| 121 | Armament Panel | 2. GND ORIDE Button; 2. ON light | Check the button is off | ON light out |
| 122 | Weapons | Weapons-actioned check on the HMD high action display (not in PANELS.md) | Verify no weapon is actioned | Display text |
| 123 | Tail Wheel / NVS Mode Panel | 1. TAIL WHEEL Button; UNLOCK light | Check the wheel is locked | UNLOCK light out |
| 124 | Parking Brake Handle | PARK BRAKE Handle | As desired; released unless on uneven or sloping ground |  |
| 125 | Power Quadrant Panel | 6. ENG POWER Levers | Check both at FLY |  |
| 126 | Multi-Purpose Displays (MPD) | FUEL page options (page function, not in PANELS.md; button not stated) | Check the options | XFER AUTO, BOOST OFF, XFEED NORM |
| 127 | Enhanced Up-Front Display (EUFD) | 10. Information Display Area | Check the fuel quantity | Enough for the mission. The manual names no display; PANELS.md puts total fuel in this area |
| 128 | Enhanced Up-Front Display (EUFD) | 2. Warning Message Area; 3. Caution Message Area | Check | No warning or caution message |
| 129 | Multi-Purpose Displays (MPD) | ENG page and FLT page (page function, not in PANELS.md; button not stated) | Check engine and flight instruments | NP and NR at 101 %, all indications green |
| 130 | Multi-Purpose Displays (MPD) | FLT page, SET sub-page (page function, not in PANELS.md; button not stated) | Update the altimeter setting as required |  |
| 131 | Standby Altimeter | 5. Barometric Setting Knob | Update the altimeter setting as required |  |
| 132 | Multi-Purpose Displays (MPD) | ASE page (page function, not in PANELS.md; button not stated) | As required |  |
| 133 | Multi-Purpose Displays (MPD) | XPNDR page on the COM page (page function, not in PANELS.md; button not stated) | Set the transponder to NORM | The right modes enabled and the codes for the mission set |
| 134 | Enhanced Up-Front Display (EUFD) | 11. Radio Status Area | Check the radios as appropriate | Frequencies as planned |
| 135 | Multi-Purpose Displays (MPD) | TSD page (page function, not in PANELS.md; button not stated) | Check the navigation | The wanted route or direct destination selected |

## Notes

### Steps whose control is missing from PANELS.md

- Canopy door (rows 1 and 42): PANELS.md has no canopy door control, only the jettison handle. BIOS.md lists the canopy under the DCS-BIOS-only controls.
- Helmet Display Unit (row 21): no HDU controls in PANELS.md; the manual gives no setting.
- Voice warnings (rows 32 and 38) and the ground crew items (rows 81 and 98): not controls.
- MPD page functions, flagged in the Control cell with the bezel button where the manual gives one: DTU MASTER LOAD (row 43), the whole sweep (rows 44 to 77, only the Fixed Action Buttons and the M button are controls in PANELS.md), the ENG, FLT, UTIL, FUEL, ASE, XPNDR and TSD pages in rows 87 to 135. The manual gives no bezel button for these later rows; the Menu page and the page names are display content in PANELS.md.
- Flight controls: collective lever, cyclic, pedals and wheel brakes (rows 108, 109, 112 and 115). Only the switches on the grips and the Anti-Torque Pedals entry (row 116) are in PANELS.md.
- HMD high action display, for the check that no weapon is actioned (row 122).

### Steps that depend on display text

The check in these rows is text or a number on a display, not a switch position or a lamp: the EUFD messages in rows 27, 31, 37, 40, 86, 90, 127, 128 and 134; the engine start indications (START box, TGT, NG, oil pressure) in rows 86 to 91; the ENG Systems sub-page values in row 93; the NP, NR and torque values in rows 94, 95, 117, 118 and 129; the MPD page contents in rows 43 to 77, 99, 100, 126, 130, 132, 133 and 135; and the weapons-actioned check in row 122. BIOS.md says the EUFD lines come as DCS-BIOS strings, while the MPD text arrives only through the export script, so the dashboard has to read and parse that text; the sweep rows set options whose state is shown only as button labels.

### Left open by the manual

- Which MPD is used for the sweep and the later page steps, and which bezel buttons open the DTU, ENG, FLT, UTIL, FUEL and other pages outside the sweep example (rows 43, 87 to 135).
- Which interior lighting knobs (row 4) and which audio volume knobs (row 19) the interior check means; the lists in those rows are our reading.
- Settings the manual leaves to the crew: NAV switch, CMWS/NAV and BYPASS/AUTO positions, brightness knobs, HDU, and every sweep value (frequencies, codes, route, scale).
- Whether the TEST switch goes back to the centre between the TEST 1 and the TEST 2 check (rows 28 and 33), and that the TEST 2 hold is given to the CP/G in the manual.
- The sweep is an example: the order is up to the crew, and settings marked common must be agreed with the CP/G. The IHADSS boresight procedure (row 59) is in another section.
- The manual gives no wait time for the APU start, for the engine starts after the first sign of NG, or for the MPDs to finish initialising (row 43).
- The rotor lock start (row 82) is mentioned only as a different RTR BRK position; its own procedure is not in this chapter.
- Ground Taxi gives no brake or speed limits beyond the collective setting; the hover and the Hover Power Check that follow Before Takeoff are in the next section and not included.

