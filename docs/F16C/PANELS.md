# F-16C Viper – cockpit panels

Inventory of the cockpit controls, taken from the DCS F-16C Early Access Guide (see [RESEARCH.md](RESEARCH.md)). Page numbers are the manual's pages (printed page = PDF page). Written in our own words; no text or pictures are copied from the manual. DCS-BIOS identifiers are added in phase 3.

Control types: `toggle` (2 or 3 positions), `spring` (spring-loaded, returns to a rest position), `button` (push button), `guarded` (has a cover), `rotary` (selector with fixed positions), `knob` (continuous), `rocker`, `hat` (multi-way switch), `lever`, `handle`, `lamp`, `display`, `gauge` (needle, drum or flag).

"N/I" means the manual marks the control as not implemented in DCS. Where the manual numbers the items of a figure, the rows use the same numbers; a number can appear on several rows when one item holds several switches or lamps.

## Hands-on controls (HOTAS)

Functions depend on the sensor of interest (SOI). Columns used by the manual: HUD, HMCS, FCR (fire control radar), HSD, HAD (HARM attack display), TGP (targeting pod), WPN (weapon page, with AGM-65 or AGM-88 selected). Short press means under 0.5 s and long press over 0.5 s; the few exceptions need a full 1 s and are marked. A function written without an SOI applies to all of them. The manual says pp. 83 to 89 do not list every function; picture versions are in Appendix D (pp. 755 to 761).

### Side Stick Controller (SSC) (p. 83)

Where: Right-hand stick; pitch and roll come from the stick itself (figure on p. 83).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Weapon Release Button | button | press and hold | none | Fires an air-to-air missile or releases an air-to-ground store while held |
| 2. Trim Switch (4-way) | hat | aft: nose up; fwd: nose down; left: left wing down; right: right wing down | none | Same in every SOI |
| 3. Trigger (2-position) | button | first detent: laser designator / ranger fires (pod fitted and powered); second detent: gun (if selected and armed), or laser for 30 s in CCIP | none | Two-stage pull |
| 4. Missile Step Button | button | on the ground: press to switch nosewheel steering on, press again to switch off; in the air with AIR REFUEL switch OPEN: press to disconnect the boom; NAV: no action; A-A, MSL ORIDE, DGFT: short press next missile station of the type, long press cycle missile type; A-G: short press cycle CCIP, DTOS, CCRP (with AGM-65 or AGM-88 selected on SMS: next missile station), long press no action | AR/NWS lamp on the AR Status / NWS indicator (p. 45) | Depends on aircraft state and master mode |
| 5. Target Management Switch (TMS) (4-way) | hat | fwd short: HUD designate (DTOS / VIS); HMCS designate; FCR designate (ACM: bore); HSD designate / show range ring; HAD designate; TGP point track (on release); WPN track / force correlate. fwd long: HUD SOI to HMCS; FCR spotlight scan while held; HAD cycle HARM POS (1 s); TGP area track while held; others no action. left short: FCR scan interrogate; HAD DED to SEAD; TGP cycle TV / FLIR / FLIR polarity; WPN HARM table / MAV polarity; HUD, HMCS, HSD no action. left long: FCR NCTR / LOS interrogate; HAD start TDOA; others no action. right short: HUD rotate sighting point; FCR target step, ACM 30x20, or sighting point (A-G); HAD target step; TGP area track / IR pointer (2x); WPN HARM target step; HMCS, HSD no action. right long: FCR TWS toggle (1 s); TGP inertial track; others no action. aft short: HUD target reject; HMCS target reject / SOI to HUD; FCR target reject / ACM 10x60; HSD drop PDLT / hide ring; HAD target reject / DED to CNI; TGP slave mode / cursor zero; WPN target reject / MAV slave. aft long: HAD end TDOA; TGP declutter while held; others no action | none | A-G with HUD or FCR as SOI: right short steps through the available sighting points |
| 6. Display Management Switch (DMS) (4-way) | hat | fwd short: SOI to HUD (FCR, HSD, HAD, TGP, WPN; HUD and HMCS no action); left short: cycle left MFD format; right short: cycle right MFD format; aft short: HUD, HMCS SOI to MFD; FCR, HSD, HAD, TGP, WPN swap the SOI between the two MFDs; aft long: helmet display on / off; other long presses no action | none | Main way to set the SOI |
| 7. Countermeasures Management Switch (CMS) (4-way) | hat | fwd (all CMDS modes): dispense one manual program 1 to 4 as chosen on the PRGM knob; left (all modes): dispense manual program 6; right: MAN deactivate ECM, SEMI disable ECM, AUTO stop auto dispensing or interrupt the running program; aft: MAN switch ECM on (XMIT switch at 3), SEMI dispense one auto program and enable ECM (XMIT at 1 or 2), AUTO enable continuous auto dispensing | none | Same in every SOI; p. 708 adds that fwd does nothing while another program runs |
| 8. Paddle Switch | spring | press and hold | none | Autopilot off while held; on release it takes new pitch, roll or altitude references |
| 9. Expand / FOV Button | button | short: FCR, HSD, HAD cycle expand modes; TGP cycle FOV / XR zoom (2x); WPN cycle missile FOV or POS (AGM-65 seeker FOV; AGM-88 HAS: WIDE, CTR, LT, RT; POS: EOM, RUK, PB); HUD, HMCS no action. long: HSD zoom mode while held | none | The long press is listed for every SOI |

### Throttle (p. 86)

Where: Left hand, mounted above the left console; detents OFF, IDLE, MIL, MAX AB (figure on p. 86).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Throttle lever | lever | OFF; IDLE; MIL; MAX AB | none | OFF cuts ignition and fuel; IDLE for all starts; MIL to IDLE range sets thrust; forward of MIL runs the afterburner |
| Throttle Cutoff Release | lever | not stated | none | Named in the figure only |
| 1. UHF VHF Transmit Switch (4-way) | hat | fwd: transmit on the VHF radio (ARC-222); aft: transmit on the UHF radio (ARC-164); left (IFF OUT) short: toggle datalink information on the FCR, long: no action; right (IFF IN) short: cycle datalink filters on the FCR, long: send the selected steerpoint, SPI or SEAD target over the datalink | none | Fwd and aft are push-to-talk and also open the matching call radio menu (p. 263) |
| 2. MAN RNG / UNCAGE Knob | knob | rotate: TGP manual zoom; depress short: NAV with gear down declutter ILS bars and roll indicator, A-A / MSL / DGFT uncage the AIM-9 seeker (AIM-9 on SMS), A-G toggle laser spot track (TGP as SOI); depress long (over 1.0 s): A-G toggle gun strafe mode, other modes no action | none | Function depends on master mode and SOI |
| 3. DOG FIGHT Switch (3-position) | toggle | up (outboard): dogfight mode, FCR to ACM and standby; centre: back to the previous master mode; down (inboard): missile override, FCR to CRM and RWS | HUD master mode status shows DGFT, or MRM / SRM / HOB / MSL | Overrides every master mode except emergency jettison |
| 4. ANT ELEV Knob | knob | rotate; centre detent | none | Sets the FCR antenna elevation by hand |
| 5. RDR CURSOR / ENABLE Switch | hat | slew: HUD, HMCS move the TD box / mark cue; FCR, HSD, HAD move the MFD cursor (FCR in ACM: ACM slew); TGP slews the pod; WPN with AGM-65 slews the seeker; WPN with AGM-88 moves the HAS cursor. depress: A-A, MSL ORIDE, DGFT swap AIM-9 BORE / SLAVE while held; A-G with AGM-65 steps PRE, VIS, BORE; A-G with AGM-88 toggles HAS and POS | none | Multi-direction with a push |
| 6. SPD BRK Switch (3-position, aft momentary) | spring | fwd: retract; centre: hold position; aft: extend (springs back to centre) | speed brake position indicator on the landing gear panel (p. 57) | Right gear down and locked limits opening to 43 degrees; holding aft overrides it |

## Instrument panel

The panel runs left to right: MISC panel, left MFD, the centre column (ICP and DED at the top, then the flight instruments), right MFD and the engine instruments. HUD, ICP, DED, MFD and the threat warning panels have their own sections further down.

### AoA Indexer (p. 44)

Where: Left side of the HUD frame, at eye level (figure on p. 44).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Dimming Lever | lever | rotate down to dim | none | Dims all three lights |
| 2. High AoA light | lamp | lit; unlit | top symbol, red in the figure | Lit at 14 degrees or more |
| 3. Optimal AoA light | lamp | lit; unlit | middle circle, green in the figure | Lit from 11.1 to 13.9 degrees |
| 4. Low AoA light | lamp | lit; unlit | bottom symbol, yellow in the figure | Lit at 11 degrees or less |

### AR Status / NWS Indicator (p. 45)

Where: Right side of the HUD frame (figure on p. 45).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Dimming Lever | lever | rotate down to dim | none | Dims the three lights |
| 2. RDY light | lamp | lit; unlit | legend RDY | Refuelling door open and ready |
| 3. AR / NWS light | lamp | lit; unlit | legend AR NWS | In the air: boom latched; on the ground: nosewheel steering on |
| 4. DISC light | lamp | lit; unlit | legend DISC | Boom disconnected; returns to ready after 3 s |

### Left Eyebrow Lights (p. 45)

Where: Top left of the instrument panel, along the left eyebrow above the MISC panel (figure on p. 45).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. MASTER CAUTION button | button | press | lit lamp in the button, legend MASTER CAUTION | Lit by any caution light; press resets it |
| 2. TF-FAIL warning light | lamp | lit; unlit | legend TF-FAIL | No function in the Block 50 |
| 3. F-ACK button | button | press | none | Acknowledges and clears a fault on the PFLD |
| 4. IFF IDENT button | button | press | none | Ident reply to non-Mode 4 interrogations |

### Right Eyebrow Lights (p. 46)

Where: Top right of the instrument panel, along the right eyebrow above the right MFD (figure on p. 46).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. ENG FIRE warning light | lamp | lit; unlit | legend ENG FIRE | Fire detected in the engine bay |
| 2. ENGINE warning light | lamp | lit; unlit | legend ENGINE | RPM under 60 %, or FTIT over 1,100 C for 2 s |
| 3. HYD / OIL PRESS warning lights | lamp | lit; unlit | split light, legends HYD and OIL PRESS | Oil under 10 PSI for 30 s, or hydraulic A or B under 1,000 PSI |
| 4. FLCS warning light | lamp | lit; unlit | legend FLCS | FLCS fault, failed BIT or locked leading-edge flaps |
| 5. DBU ON warning light | lamp | lit; unlit | legend DBU ON | Digital backup mode, automatic or selected |
| 6. TO / LDG CONFIG warning lights | lamp | lit; unlit | split light, legends TO and LDG CONFIG | Low and slow, gear or flaps not set; gear horn sounds with it |
| 7. CANOPY warning light | lamp | lit; unlit | legend CANOPY | Canopy not down and locked |
| 8. OXY LOW warning light | lamp | lit; unlit | legend OXY LOW | Backup oxygen under 5 PSI; also lit 10 s during an OBOGS BIT |

### Miscellaneous (MISC) Panel (p. 47)

Where: Left side of the instrument panel, left of the left MFD, below the left eyebrow (figure on p. 47).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. RF Switch | toggle | NORM; QUIET; SILENT | none | Limits emissions; details after the table |
| 2. ECM light | lamp | lit; unlit | legend ECM | Lit while the ECM pod is jamming |
| 3. LASER ARM Switch | toggle | LASER ARM; OFF | none | Allows the pod laser to fire when not masked |
| 4. ALT REL Button | button | press | red button in the figure | Backup for the SSC weapon release button |
| 5. MASTER ARM Switch | toggle | MASTER ARM; OFF; SIMULATE | HUD shows ARM, blank, SIM | OFF still allows emergency jettison; SIMULATE blocks release |
| 6. ADV MODE Button | button | press | none | Terrain following function, not used in the Block 50 |
| 7. Autopilot ROLL Switch | toggle | HDG SEL; ATT HOLD; STRG SEL | none | Roll mode; see Autopilot controls below |
| 7. Autopilot PITCH Switch | toggle | ALT HOLD; A/P OFF; ATT HOLD | none | Held in ALT HOLD or ATT HOLD by a solenoid; drops to A/P OFF on disengage |

RF switch effects (p. 48):
- FCR: QUIET stops RWS, VSR, TWS, the SAM scan and all A-G modes except fixed target track; SILENT stops all CRM sub-modes and all A-G modes; ACM works in both.
- AIFF: QUIET and SILENT stop replies and the IFF IDENT button when the IFF MASTER knob is at LOW or NORM; EMER still replies.
- TNDL: QUIET limits MIDS power to low; SILENT receives only.
- ECM pod: QUIET and SILENT revoke consent in MAN and SEMI (CMS aft restores it); in AUTO the pod is blocked.
- TACAN: QUIET and SILENT force receive only.
- Radar altimeter: SILENT stops it transmitting.

### Autopilot controls (pp. 129 to 132)

Where: No panel of its own; it uses the MISC panel switches above, the SSC paddle switch (p. 83), the EHSI heading set knob (p. 230) and the ICP steerpoint selection. Every control already has a row elsewhere; this lists what pp. 130 to 132 add.

- PITCH switch: ALT HOLD holds barometric altitude, ATT HOLD holds the current pitch, A/P OFF disengages.
- ROLL switch (works only with PITCH at ALT HOLD or ATT HOLD): HDG SEL turns to and holds the EHSI heading marker, ATT HOLD holds the current roll attitude, STRG SEL holds a direct course to the selected steerpoint.
- Paddle switch: autopilot interrupted while held; new references are taken on release; the PITCH switch stays where it is.
- Limits while engaged: pitch command +3.0 to -1.0 G, roll rate up to 20 degrees per second, bank up to 30 degrees.
- Automatic disengage (p. 132): AoA over 15 degrees, bank over 60 degrees, low speed warning, gear down and locked, autopilot failure, FLCS digital backup, ALT FLAPS at EXTEND below 400 knots, TRIM/AP DISC at DISC, AIR REFUEL switch at OPEN, manual pitch override at OVRD.

### Standby Attitude Indicator (SAI) (p. 49)

Where: Upper right of the centre column, right of the DED and above the fuel flow indicator (figure on p. 44).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Attitude sphere | gauge | pitch and roll; light blue upper half, dark brown lower half | none | Independent gyro |
| 2. Aircraft symbol (waterline) | display | fixed symbol | none | Height can be changed with the cage knob |
| 3. Roll indicator | gauge | pointer along the bank scale | none | Aligned with the index when level |
| 4. Roll indicator scale | gauge | index at 0; major ticks 30, 60, 90; minor ticks 10, 20 degrees | none | Bank angle reference |
| 5. Pitch trim scale | gauge | major ticks at 25 degrees; minor ticks every 5 degrees | none | Read against the knob arrow |
| 6. PULL TO CAGE Knob | knob | turn: adjust the symbol pitch; pull: cage to level; pull and turn counter-clockwise: lock caged | none | Caged flight: hold wings level and 4 degrees up |
| OFF warning flag | gauge | shown; hidden | red flag | Shown when caged or unpowered |

### Fuel Flow Indicator (p. 50)

Where: Right side of the centre column, below the SAI (figure on p. 44).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Fuel flow pointer | gauge | pounds per hour in 100 lb steps; range not stated | none | Engine fuel use |

### Engine Instruments (p. 50)

Where: Right of the right MFD (figure on p. 44).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Engine OIL pressure indicator | gauge | 0 to 100 PSI; major ticks 10, minor ticks 5 | none | Idle on the ground about 15, flight at MIL and above about 60 |
| 2. Engine NOZ POS indicator | gauge | percent; major ticks 20, minor ticks 10; end values not stated | none | Nozzle position |
| 3. Engine RPM indicator | gauge | 0 to 110 %; major ticks 5 %; minor ticks 5 % up to 60 % and 1 % above 65 % | none | From the engine alternator |
| 4. Engine FTIT indicator | gauge | 200 to 1,200 C; coarse ticks 100 C, finer ticks 50 C and 10 C by range | none | Average turbine inlet temperature |

### Airspeed and Mach Indicator (p. 51)

Where: Centre column, upper left, below the left MFD (figure on p. 44).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. VNE indicator | gauge | marker, 800 kt at sea level | none | Never-exceed speed |
| 2. Indicated airspeed scale | gauge | 80 to 850 kt; ticks 10 kt up to 400, 50 kt above | none | Outer scale |
| 3. Mach indicator window | display | 0.5 to 2.2 Mach | none | Read-out inside the dial |
| 4. Airspeed indicator | gauge | pointer on the outer scale | none | Pitot-static driven |
| 5. Airspeed reference index | gauge | movable marker | none | Pilot's reference speed |
| 6. SET INDEX Knob | knob | turn; stops not stated | none | Moves the reference index |

### Altimeter (p. 51)

Where: Centre column, upper right, right of the airspeed indicator (figure on p. 44).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Altitude scale | gauge | major ticks 100 ft, minor ticks 10 ft | none | One turn is 1,000 ft |
| 2. 1000-ft scale indicator | gauge | pointer on the outer scale | none | Shows altitude within the 1,000 ft |
| 3. PNEU flag | gauge | shown; hidden | flag | Shown in pneumatic mode, which is automatic after an electric fault |
| 4. Altitude indicator | display | counter, -1,000 to 80,000 ft in 100 ft steps | none | Barometric altitude |
| 5. Kollsman window | display | inches of mercury; range not stated | none | QNH setting |
| 6. Barometric Setting Knob | knob | turn; stops not stated | none | Sets the window value |
| 7. Altimeter Mode Switch | spring | ELEC; PNEU (held momentarily) | none | ELEC is the primary mode |

### Angle-of-Attack (AoA) Indicator (p. 52)

Where: Centre column, below the airspeed indicator (figure on p. 44).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. AoA scale tape | gauge | -5 to +32 degrees; major ticks 5, minor ticks 1 | none | Same data as the indexer |
| 2. Current AoA marker | gauge | marker on the tape | none | Present angle of attack |
| 3. High AoA region marker | display | 14 to 16.5 degrees | none | Matches the indexer top light |
| 4. Optimal AoA region marker | display | 11.1 to 13.9 degrees | none | On-speed band |
| 5. Low AoA region marker | display | 8.5 to 11 degrees | none | Matches the indexer bottom light |

### Vertical Velocity Indicator (VVI) (p. 52)

Where: Centre column, below the altimeter (figure on p. 44).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Vertical velocity tape | gauge | +/- 6,000 FPM; major ticks 500, minor ticks 100 | none | Source is the CADC |
| 2. Current vertical velocity marker | gauge | marker on the tape | none | Present climb or descent rate |
| 3. Positive region marker | display | light shading | none | Climb side |
| 4. Negative region marker | display | dark shading | none | Descent side |

### Attitude Director Indicator (ADI) (p. 53)

Where: Centre column, below the AoA indicator and VVI, above the EHSI (figure on p. 44).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Attitude sphere | gauge | pitch and roll; light blue upper half, dark brown lower half | none | Data from the INS |
| 2. Upper bank angle indicator | gauge | pointer against a fixed index | none | Aligned with the index when level |
| 3. Pitch scale | gauge | major ticks 10, minor ticks 5 degrees | none | Read against the aircraft symbol |
| 4. Glideslope deviation indicator | gauge | pointer along the scale | none | Centred means on the ILS glideslope |
| 5. Glideslope deviation scale | gauge | white dots 2.5 degrees apart | none | Outer dots are 5 degrees off |
| 6. Aircraft symbol (waterline) | display | fixed symbol | none | Height set by the pitch trim knob |
| 7. OFF warning flag | gauge | shown; hidden | flag | No attitude data from the INS |
| 8. AUX warning flag | gauge | shown; hidden | flag | Degraded INS data or no coarse alignment |
| 9. Lower bank angle scale | gauge | index at 0; major ticks 30, 60, 90; minor ticks 10, 20 degrees | none | Bottom of the case |
| 10. Lower bank angle indicator | gauge | pointer against a fixed index | none | Aligned with the index when level |
| 11. Slip indicator (ball) | gauge | ball between two marks | none | Centred is coordinated flight |
| 12. Rate-of-turn indicator | gauge | bar; one bar width is 1 to 1.2 degrees per second; aligned with the side bars is 3 degrees per second | none | Centred is no turn |
| 13. Pitch Trim Knob | knob | turn; each click 0.5 degrees | none | Offsets the aircraft symbol from the sphere |

### Electronic Horizontal Situation Indicator (EHSI) (p. 230)

Where: Bottom centre of the instrument panel, below the ADI (figure on p. 44; the EHSI is described in the navigation chapter).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Bearing pointer | gauge | arrow | none | To the steerpoint in NAV, to the TACAN station in TCN |
| 2. Lubber lines | display | marks every 45 degrees | none | Fixed to the aircraft |
| 3. Range indicator | display | nautical miles; fourth digit is 0.1 NM | none | Steerpoint in NAV, TACAN DME in TCN |
| 4. Course indicator | display | course value | numeric read-out | Set with the course knob |
| 5. Magnetic heading compass | gauge | numerals every 30 degrees; ticks 10 and 5 degrees | none | Turns around the aircraft symbol |
| 6. Heading marker | gauge | marker on the compass | none | Autopilot HDG SEL turns to it |
| 7. Course pointer | gauge | arrow | none | Desired course |
| 8. To-From indicator | gauge | to; from | none | Not shown in the figure |
| 9. Course deviation scale | gauge | inner dots 5 degrees, outer 10 (NAV, TCN); 1.25 and 2.5 degrees with localizer | none | Scale follows the mode |
| 10. Course deviation indicator | gauge | offset left or right | none | Centred means on course |
| 11. New mode indicator | display | mode name for 1 s after a change; ADJ HDG or BRT while a knob is pushed | text | In front of the aircraft symbol |
| 12. Aircraft symbol | display | fixed symbol | none | Centre of the display |
| 13. Heading Set Knob | knob | turn; push in ATT mode: adjust compass (ADJ HDG, reverts after 2 s) | text ADJ HDG | Lower left |
| 14. Course Set / Brightness Knob | knob | turn: course; push: brightness (BRT, reverts after 2 s) | text BRT | Lower right; with a localizer the course syncs to the T-ILS page |
| 15. Instrument Mode Selector | button | press: NAV, NAV/PLS, TCN, TCN/PLS, then NAV again | none | Button marked M at the bottom centre |
| 16. Selected instrument mode | display | NAV; NAV/PLS; TCN; TCN/PLS | text | Source for bearing, course and range |
| 17. Range flag | gauge | shown; hidden | flag | Shown when range is unavailable |
| 18. Warning display area | display | INU; ATT | text | INU unaligned, failed or off; ATT attitude mode |
| 19. CDI flag | gauge | shown; hidden | flag | Deviation unavailable; indicator centred and dashed |

### FUEL QTY SEL Panel (p. 54)

Where: Bottom of the centre column, right of the EHSI (figure on p. 44).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. FUEL QTY SEL Knob | rotary | TEST; NORM; RSVR; INT WING; EXT WING; EXT CTR | none | Chooses what the two fuel needles show; TEST sets both to 2000 lb and the totalizer to 6000 lb and lights FWD and AFT FUEL LOW |
| 2. EXT FUEL TRANS Switch | toggle | NORM; WING FIRST | none | NORM drains the centreline tank first, WING FIRST the wing tanks first |

## Left auxiliary console

The THREAT WARNING AUX and CMDS control panels also sit on this console; they are listed under Defensive systems.

### Landing Gear Panel (p. 55)

Where: Top of the left auxiliary console, with the CMDS panel below it (figure on p. 55). Items 1 to 12 are numbered as in the figure.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. EMER STORES JETTISON Button | button | press and hold for 1 s | none | Drops tanks, racks and free-fall stores on stations 3 to 7; air-to-air missiles stay; no arming needed |
| 2. HOOK Switch | toggle | UP; DN | HOOK caution light while the hook is not stowed | DN drops the hook; it cannot be fully retracted from the cockpit |
| 3. WHEELS Down Lights | lamp | lit; unlit | three green lights (nose, left main, right main) | Green means down and locked |
| 4. LG Handle | lever | up; down | red warning light in the handle | Light also comes on with the TO/LDG CONFIG warning |
| 5. GND JETT ENABLE Switch | toggle | ENABLE; OFF | none | Maintenance use; OFF blocks jettison and weapon release with weight on wheels |
| 6. BRAKES Channel Switch | toggle | CHAN 1; CHAN 2 | none | Normally CHAN 1 |
| 7. PARKING BRAKE / ANTI-SKID Switch | toggle | PARKING BRAKE; ANTI-SKID; OFF | none | Figure calls it PARKING BRAKE, text ANTI-SKID; parking brake releases when the throttle goes 1 inch past IDLE |
| 8. DN LOCK REL Button | button | press | yellow button in the figure | Frees the handle if the solenoid fails; overrides weight on wheels |
| 9. STORES CONFIG Switch | toggle | CAT I; CAT III | STORES CONFIG caution if wrong | Picks FLCS limits for the load |
| 10. HORN SILENCER Button | button | press | none | Silences gear and low speed tones |
| 11. LANDING TAXI LIGHTS Switch | toggle | LANDING; OFF; TAXI | none | Lights go off when the gear handle goes up |
| 12. SPEED BRAKE Position Indicator | display | CLOSED; nine dots (open at any angle); stripes (no power) | indicator window | Bottom left of the panel |

### HMCS Control Panel (p. 57)

Where: Left auxiliary console, below the CMDS panel (figure on p. 55).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| HMCS symbology brightness knob | knob | clockwise: brighter; OFF end position: symbology off | none | Brightness of the helmet display symbols |

### ALT GEAR Handle (p. 57)

Where: Left side of the left auxiliary console, lower left in the figure on p. 55.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| ALT GEAR handle | handle | not stated | none | Drops the gear if the hydraulics fail or the normal handle cannot |

## Right auxiliary console

Left to right in the figure on p. 58: magnetic compass at the top left, fuel quantity indicator and the hydraulic gauges at the top, PFLD and caution light panel on the left, EPU fuel, clock and cabin pressure on the right.

### Magnetic Compass (p. 58)

Where: Top left of the right auxiliary console (figure on p. 58).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Compass card | gauge | heading numerals in a window | none | Standby heading; not precise in manoeuvres |

### Fuel Quantity Indicator (p. 58)

Where: Top of the right auxiliary console (figure on p. 58).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| AL fuel needle | gauge | pounds in 100 lb steps; dial 0 to 40 (x 100) in the figure | red at the needle base when out of balance | Aft and left tanks; the FUEL QTY SEL knob changes the source |
| FR fuel needle | gauge | pounds in 100 lb steps; dial 0 to 40 (x 100) in the figure | red at the needle base when out of balance | Forward and right tanks |
| Totalizer window | display | pounds | numeric read-out | Total fuel; shows 6000 lb in the FUEL QTY SEL test |

### Pilot Fault List Display (PFLD) (p. 59)

Where: Right auxiliary console, left of centre, above the caution light panel (figure on p. 58).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Fault list window | display | WARNING level (in brackets); CAUTION level | text lines | Cleared with the F-ACK button; also repeated on the HUD by the DED/PFLD switch |

### Caution Light Panel (p. 59)

Where: Right auxiliary console, lower left (figure on p. 58). The lights form a grid of 8 rows and 4 columns; the notes give row and column (R1 C1 is top left). Six cells are blank in the figure: R6 C3, R7 C3, R7 C4, R8 C2, R8 C3, R8 C4.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| FLCS FAULT | lamp | lit; unlit | legend FLCS FAULT | R1 C1; dual FLCC fault, locked LEF or failed BIT |
| ENGINE FAULT | lamp | lit; unlit | legend ENGINE FAULT | R1 C2; clears when acknowledged |
| AVIONICS FAULT | lamp | lit; unlit | legend AVIONICS FAULT | R1 C3; avionics fault or lost bus link |
| SEAT NOT ARMED | lamp | lit; unlit | legend SEAT NOT ARMED | R1 C4; arming lever is up |
| ELEC SYS | lamp | lit; unlit | legend ELEC SYS | R2 C1; see the ELEC panel lights |
| SEC | lamp | lit; unlit | legend SEC | R2 C2; engine in secondary mode |
| EQUIP HOT | lamp | lit; unlit | legend EQUIP HOT | R2 C3; avionics bay cooling short; cuts FCR power |
| NWS FAIL | lamp | lit; unlit | legend NWS FAIL | R2 C4; nosewheel steering fault |
| PROBE HEAT | lamp | lit; unlit | legend PROBE HEAT | R3 C1; icing or heater fault; flashes after a good test |
| FUEL/OIL HOT | lamp | lit; unlit | legend FUEL/OIL HOT | R3 C2; fuel or oil too hot |
| RADAR ALT | lamp | lit; unlit | legend RADAR ALT | R3 C3; radar altimeter fault |
| ANTI SKID | lamp | lit; unlit | legend ANTI SKID | R3 C4; switch off or brake fault above 5 kt |
| CADC | lamp | lit; unlit | legend CADC | R4 C1; air data computer fault |
| INLET ICING | lamp | lit; unlit | legend INLET ICING | R4 C2; ice detected or detector failed |
| IFF | lamp | lit; unlit | legend IFF | R4 C3; Mode 4 interrogation cannot be answered |
| HOOK | lamp | lit; unlit | legend HOOK | R4 C4; hook not up and locked |
| STORES CONFIG | lamp | lit; unlit | legend STORES CONFIG | R5 C1; STORES CONFIG switch in the wrong place |
| OVERHEAT | lamp | lit; unlit | legend OVERHEAT | R5 C2; engine bay, wheel wells, ECS or EPU bay |
| NUCLEAR | lamp | lit; unlit | legend NUCLEAR | R5 C3; not implemented |
| OBOGS | lamp | lit; unlit | legend OBOGS | R5 C4; ECS air pressure under 10 PSI |
| ATF NOT ENGAGED | lamp | lit; unlit | legend ATF NOT ENGAGED | R6 C1; no function |
| EEC | lamp | lit; unlit | legend EEC | R6 C2; no function |
| CABIN PRESS | lamp | lit; unlit | legend CABIN PRESS | R6 C4; cabin altitude above 27,000 ft |
| FWD FUEL LOW | lamp | lit; unlit | legend FWD FUEL LOW | R7 C1; forward reservoir under 400 lb |
| BUC | lamp | lit; unlit | legend BUC | R7 C2; no function |
| AFT FUEL LOW | lamp | lit; unlit | legend AFT FUEL LOW | R8 C1; aft reservoir under 250 lb |

### Hydraulic Pressure Indicators (p. 61)

Where: Top of the right auxiliary console, below the fuel quantity indicator (figure on p. 58).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| HYD PRESS A gauge | gauge | 0 to 4,000 PSI; ticks 500 | none | Normal 2,850 to 3,250 PSI |
| HYD PRESS B gauge | gauge | 0 to 4,000 PSI; ticks 500 | none | Normal 2,850 to 3,250 PSI |

### EPU Fuel Quantity Indicator (p. 61)

Where: Right side of the right auxiliary console (figure on p. 58).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| EPU fuel gauge | gauge | percent of hydrazine; ticks 5 % | none | Full load runs the EPU about 10 to 15 minutes |

### Cabin Pressure Gauge (p. 61)

Where: Bottom of the right auxiliary console, below the clock (figure on p. 58).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Cabin pressure gauge | gauge | 0 to 50,000 ft; ticks 1,000 ft | none | Cockpit pressure as an altitude; 7 means 7,000 ft |

### Mechanical Clock (p. 61)

Where: Right side of the right auxiliary console, lower right (figure on p. 58).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. "Day" hand | gauge | one turn is 8 days | none | 8-day clock |
| 2. "Hour" hand | gauge | one turn is 12 hours; inner ring | none | Set to local time at mission start |
| 3. "Minute" hand | gauge | one turn is 60 minutes; outer ring | none | Outer ring |
| 4. Wind / Control Knob | knob | turn clockwise: wind; pull and turn either way: set the time | none | Clock is set to local time at mission start |

## Left console

Figure on p. 62. Top row, left to right: manual canopy handcrank, DEFOG lever, CANOPY JETTISON T-handle, FUEL, EPU and ENG & JET START panels, manual pitch override switch. Below them FLT CONTROL, TEST, IFF, MANUAL TRIM and ELEC panels, and along the bottom the ANTI-G TEST button, EXT LIGHTING, AVTR, ECM and AUDIO panels. The UHF backup panel is at the right. The ECM panel is listed under Defensive systems.

### Manual Pitch Override Switch (p. 62)

Where: Upper right of the left console, near the throttle (figure on p. 62); guards on each side of the switch.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| MANUAL PITCH override switch | spring | NORM (rest); OVRD (held) | none | Raises stabilator authority for deep stall recovery; SSC roll and yaw inputs are blocked while held |

### ENG & JET START Control Panel (p. 63)

Where: Top right of the left console (figure on p. 62). Items 1 to 5 are numbered as in the figure on p. 63.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. JET FUEL RUN light | lamp | lit; unlit | legend RUN | Lit within 30 s of JFS start when it reaches governed speed |
| 2. JET FUEL JFS Switch | toggle | START 1; OFF; START 2 | none | START 2 needed above 38 C, below -7 C or for restarts below 20,000 ft |
| 3. ENG CONT Switch | toggle | PRI; SEC | SEC caution light | SEC gives no afterburner and fixed nozzle; red cover in the figure |
| 4. AB RESET Switch | spring | AB RESET; NORM (rest); ENG DATA | none | AB RESET does nothing with this engine; ENG DATA records 8 s of engine data; N/I |
| 5. MAX POWER Switch | toggle | positions not stated | none | No function with the F110-GE-129 engine |

### EPU Control Panel (p. 64)

Where: Upper centre of the left console, next to the FUEL panel (figure on p. 62).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. EPU Switch | toggle | OFF; NORM; ON | none | NORM starts the EPU by itself when power or both hydraulics are lost |
| 2. EPU Run Light | lamp | lit; unlit | green light | EPU running and pump pressure above 2,000 PSI |
| 3. AIR Light | lamp | lit; unlit | legend AIR | EPU running on bleed air |
| 4. HYDRAZN Light | lamp | lit; unlit | legend HYDRAZN | EPU running on hydrazine |

### ELEC Control Panel (p. 64)

Where: Lower centre of the left console (figure on p. 62).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. MAIN PWR Switch | toggle | MAIN PWR; BATT; OFF | none | Chooses the electrical source |
| 2. ELEC CAUTION RESET Button | button | press | none | Clears MASTER CAUTION and ELEC SYS and resets both generators |
| 3. FLCS PMG Light | lamp | lit; unlit | legend FLCS PMG | FLCS branches without PMG power |
| 4. MAIN GEN Light | lamp | lit; unlit | legend MAIN GEN | No main or external power on the non-essential buses |
| 5. STBY GEN Light | lamp | lit; unlit | legend STBY GEN | Standby generator unavailable |
| 6. EPU GEN Light | lamp | lit; unlit | legend EPU GEN | EPU commanded on but emergency buses not powered |
| 7. EPU PMG Light | lamp | lit; unlit | legend EPU PMG | EPU PMG not feeding all FLCS branches |
| 8. ACFT BATT FAIL Light | lamp | lit; unlit | legend FAIL | Battery or charger failure |
| 9. ACFT BATT TO FLCS Light | lamp | lit; unlit | legend TO FLCS | FLCS branches on battery power |
| 10. ACFT BATT FLCS RLY Light | lamp | lit; unlit | legend FLCS RLY | Low or missing battery bus feed; reset on the FLT CONTROL panel |

### AUDIO 1 Control Panel (p. 65)

Where: Bottom right of the left console, upper of the two audio panels (figure on p. 65). Items 1 to 8 are numbered as in the figure.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. COMM 1 Power/Volume Knob | knob | turn; fully counter-clockwise: UHF radio off | none | UHF volume |
| 2. COMM 2 Power/Volume Knob | knob | turn; fully counter-clockwise: VHF radio off | none | VHF volume |
| 3. COMM 1 Mode Knob | rotary | OFF; SQL; GD | none | GD tunes the UHF to 243.0 MHz; no effect with C & I at BACK UP |
| 4. COMM 2 Mode Knob | rotary | OFF; SQL; GD | none | GD tunes the VHF to 121.5 MHz |
| 5. SECURE VOICE Volume Knob | knob | turn; stops not stated | none | No function in DCS |
| 6. MSL Volume Knob | knob | turn; stops not stated | none | Tone of the selected AIM-9 |
| 7. TF Volume Knob | knob | turn; stops not stated | none | No function in DCS |
| 8. THREAT Volume Knob | knob | turn; stops not stated | none | ALR-56M warning audio |

### AUDIO 2 Control Panel (p. 65)

Where: Bottom right of the left console, lower of the two audio panels (figure on p. 65). Items 9 to 12 continue the numbers of the AUDIO 1 figure.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 9. INTERCOM Volume Knob | knob | turn; stops not stated | none | Also affects gear and low speed tones and voice messages; the manual marks it N/I |
| 10. TACAN Volume Knob | knob | turn; stops not stated | none | Lets you hear the station identifier |
| 11. ILS Power/Volume Knob | knob | turn; fully counter-clockwise: OFF | none | OFF switches the ILS receiver off |
| 12. HOT MIC CIPHER Switch (Microphone Switch) | toggle | HOT MIC; OFF; CIPHER | none | N/I; the figure calls it Microphone Switch |

### AVTR Control Panel (p. 66)

Where: Bottom of the left console, between the EXT LIGHTING and ECM panels (figure on p. 62).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| AVTR panel controls | not stated | not stated | not stated | The manual only says the recorder films the HUD or HMCS plus the MFDs; N/I; no controls described |

### FUEL Control Panel (p. 67)

Where: Top of the left console, left of the EPU panel (figure on p. 62).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. FUEL MASTER Switch | guarded | MASTER; OFF | none | Main fuel shutoff to the engine; normally MASTER with the guard closed |
| 2. TANK INERTING Switch | toggle | TANK INERTING; OFF | none | Fills the tanks with halon after damage |
| 3. ENG FEED Knob | rotary | OFF; NORM; AFT; FWD | none | AFT and FWD shift the centre of gravity by running one pump |
| 4. AIR REFUEL Switch | toggle | OPEN; CLOSE | none | OPEN opens the door, depressurises external tanks and lights the AR floodlights |

### IFF Control Panel (p. 67)

Where: Left of centre on the left console (figure on p. 62). Items 1 to 7 are numbered as in the figure.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. MASTER Knob | rotary | OFF; STBY; LOW; NORM; EMER | none | N/I; works with C & I at either setting |
| 2. M-4 CODE Switch | spring | ZERO; A/B (rest); HOLD | none | N/I; ZERO erases Mode 4 codes |
| 3. C & I Knob | rotary | UFC; BACK UP | none | BACK UP moves IFF and UHF control to this panel and the UHF backup panel |
| 4. ENABLE Switch | toggle | M3/MS; OFF; M1/M3 | none | N/I; picks the code set used in BACK UP |
| 5. MODE 1 & MODE 3 Thumbwheel Selectors | rotary | four thumbwheels, two digits for Mode 1 and two for Mode 3; digit range not stated | digit windows | N/I; only Mode 3 codes ending in 00 can be set |
| 6. MODE 4 REPLY Switch | toggle | A; B; OUT | none | N/I; order read from the figure: B, A, OUT |
| 7. MODE 4 MONITOR Switch | toggle | AUDIO; OUT | none | N/I; tone on encrypted replies |

### EXT LIGHTING Control Panel (p. 69)

Where: Lower left of the left console, right of the ANTI-G TEST button (figure on p. 62). Items 1 to 7 are numbered as in the figure on p. 69.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. POSITION FLASH / STEADY Switch | toggle | FLASH; STEADY | none | Flash mode of the wing and tail position lights |
| 2. POSITION WING / TAIL Switch | toggle | BRT; OFF; DIM | none | OFF hands the wingtip lights to the FORM knob |
| 3. FUSELAGE Switch | toggle | BRT; OFF; DIM | none | Lights on the fuselage that wash the tail |
| 4. ANTI-COLL Knob | rotary | OFF; 1; 2; 3; 4; A; B; C | none | Seven flash patterns, shown on p. 69 |
| 5. FORM Knob | knob | OFF to BRT; end stops as marked | none | Formation lights; wingtips only when WING/TAIL is OFF |
| 6. AERIAL REFUELING Knob | knob | OFF to BRT; end stops as marked | none | Receptacle lights; active only with AR REFUEL at OPEN |
| 7. MASTER Knob | rotary | OFF; COVERT ALL; COVERT A-C; COVERT FORM; NORM | none | The manual's table (p. 70) calls the last position ALL; chooses which lights may be on |

### FLT CONTROL Panel (p. 71)

Where: Upper left of the left console (figure on p. 62). Items 1 to 7 are numbered as in the figure on p. 71.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. DIGITAL BACKUP Switch | toggle | BACKUP; OFF | DBU ON eyebrow light and HUD WARN | Selects the backup flight control software |
| 2. MANUAL TF FLY-UP Switch | toggle | DISABLE; ENABLE (labels read from the figure) | none | Terrain following; not used in the Block 50 |
| 3. ALT FLAPS Switch | toggle | EXTEND; NORM | none | EXTEND drops the trailing-edge flaps by hand |
| 4. FLCS RUN / FAIL Indicator Lights | lamp | RUN lit; FAIL lit; unlit | green RUN, red FAIL | RUN during a BIT; FAIL if it finds a fault |
| 5. LE FLAPS Switch | toggle | LOCK; AUTO | FLCS warning light when LOCK | N/I |
| 6. FLCS RESET Switch | toggle | RESET; OFF | none | Clears FLCS warning and caution lights if the faults are gone |
| 7. FLCS BIT Switch | spring | BIT; OFF | RUN and FAIL lights | Needs weight on wheels and under 28 kt; test runs about 45 s |

### MANUAL TRIM Panel (p. 72)

Where: Left of centre on the left console, below the FLT CONTROL panel (figure on p. 62).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. ROLL TRIM Wheel & Indicator | knob | L WING DN to R WING DN | dial | Roll trim; range not stated |
| 2. YAW TRIM Knob | knob | L to R; dots around the knob show the setting | dot scale | Yaw trim |
| 3. PITCH TRIM Wheel & Indicator | knob | NOSE UP to NOSE DN | dial | Pitch trim |
| 4. TRIM/AP DISC Switch | toggle | NORM; DISC | none | DISC makes this panel the only trim source and blocks the autopilot |

### TEST Panel (p. 72)

Where: Left edge of the left console (figure on p. 62). Items 1 to 7 are numbered as in the figure on p. 72.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. FIRE & OHEAT DETECT Test Button | button | press | ENG FIRE, OVERHEAT and MASTER CAUTION | Checks the detector circuits |
| 2. OBOGS BIT Switch | spring | OBOGS BIT (momentary); OFF | OXY LOW eyebrow light for 10 s | Lamp stays lit if a fault is found |
| 3. MAL & IND LTS Test Button | button | press | all warning, caution and indicator lights | Also plays the voice messages |
| 4. PROBE HEAT Switch | toggle | HEAT; OFF; TEST | PROBE HEAT caution flashes after a good test | HEAT and OFF matter on the ground only |
| 5. EPU/GEN Switch | spring | TEST (momentary); OFF | none | Ground test of EPU generator and PMG output without hydrazine |
| 6. FLCS PWR Lights | lamp | lit; unlit | four lights A, B, C, D | Lit per channel when the FLCS PWR switch is at TEST |
| 7. FLCS PWR TEST Switch | toggle | TEST; NORM; MAINT | none | MAINT is for ground crew |

### Canopy Switch and Canopy Handle (p. 73)

Where: Left cockpit wall above the left console; exact spot not stated (figure on p. 73). The CHAFF/FLARE button sits just aft of the canopy lever (p. 708).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Canopy Switch | spring | up; centre; down | none | Up raises the canopy (springs to centre at full travel); down lowers it and must be held |
| 2. Canopy Lever | lever | unlocked (open, pulled out); locked (closed, against the wall) | CANOPY eyebrow light when unlocked | Also limits throttle travel when unlocked |

### Canopy Jettison T-Handle (p. 74)

Where: Top of the left console, centre-left (figure on p. 62).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| CANOPY JETTISON T-handle | handle | pulled; not pulled | none | Backup if the canopy does not leave at ejection |

### DEFOG Lever (p. 74)

Where: Top of the left console, left of the T-handle (figure on p. 62).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| DEFOG lever | lever | MIN to MAX | none | MAX sends air forward; with TEMP at AUTO, full MAX gives 3 min of full warm |

### Manual Canopy Control Handcrank (p. 62)

Where: Upper left corner of the left console (figure on p. 62); named in the figure only.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Manual canopy handcrank | handle | not stated | none | Not described in the text |

### ANTI-G TEST Button (p. 62)

Where: Bottom left corner of the left console (figure on p. 62); named in the figure only.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| ANTI-G TEST button | button | press | none | Not described in the text |

### UHF Backup Control Panel (p. 260)

Where: Right side of the left console, beside the throttle (figure on p. 62; panel figure on p. 260). Items 1 to 13 are numbered as in the figure.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Preset Channel Card & Access Door | display | list of preset frequencies on the door | printed card | Lifting the door for programming is N/I |
| 2. TEST DISPLAY Button | button | press | lights all segments of both windows | Display check |
| 3. CHAN Display | display | preset number; blank in MNL | two digits | Shows the chosen preset |
| 4. CHAN Knob | knob | selects a preset; 20 presets | CHAN display | Presets are 1 to 20 per p. 251 |
| 5. Frequency Status/Display | display | manual frequency, 0.025 MHz steps from 225.000 to 399.975 | six digits | Shows the tuned frequency during STATUS |
| 6. STATUS Button | button | press and hold | frequency window | Shows the tuned preset frequency while pressed |
| 7. A-3-2 Knob | rotary | A; 3; 2 | none | 3 and 2 set the first digit in MNL; A is anti-jam, N/I |
| 8. Manual Frequency Knobs | knob | four knobs; turn | frequency window | Remaining four digits in MNL |
| 9. Function Knob | rotary | OFF; MAIN; BOTH; ADF | none | BOTH adds the 243.0 MHz guard receiver; ADF no function |
| 10. Mode Knob | rotary | MNL; PRESET; GRD | none | GRD tunes 243.0 MHz |
| 11. TONE Button | button | press | none | Transmits a tone; N/I |
| 12. VOL Knob | knob | turn; stops not stated | none | No function in DCS |
| 13. SQUELCH Switch | toggle | on; off (labels read from the figure) | none | Squelch on or off |

## Right console

Figure on p. 75. The HUD control panel and the DTU receptacle are listed in their own sections below; the HUD control panel is in the display area of this file.

### SNSR PWR Control Panel (p. 75)

Where: Lower left of the right console, below the HUD control panel (figure on p. 75). Items 1 to 4 are numbered as in the figure.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. LEFT HDPT Switch | toggle | ON; OFF | none | Powers the left chin pod, normally the HARM targeting system |
| 2. RIGHT HDPT Switch | toggle | ON; OFF | none | Powers the right chin pod, normally the targeting pod |
| 3. FCR Switch | toggle | ON; OFF | none | Powers the APG-68 radar |
| 4. RDR ALT Switch | toggle | RDR ALT; STBY; OFF | none | STBY is powered but silent |

### Interior LIGHTING Control Panel (p. 76)

Where: Upper centre-left of the right console (figure on p. 75). Items 1 to 6 are numbered as in the figure on p. 76.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. PRIMARY CONSOLES Knob | knob | turn; stops not stated | none | Panel backlight on the left aux, left and right consoles |
| 2. PRIMARY INST PNL Knob | knob | turn; stops not stated | none | Backlight on the instrument panel and right aux console |
| 3. PRIMARY DATA ENTRY DISPLAY Knob | knob | turn; stops not stated | none | Brightness of the DED and PFLD |
| 4. FLOOD CONSOLES Knob | knob | turn; HIGH INT detent | none | Flood light on the three consoles; past HIGH INT forces BRT lights |
| 5. FLOOD INST PNL Knob | knob | turn; stops not stated | none | Flood light on the instrument panel and right aux console |
| 6. MAL & IND LTS Switch | toggle | BRT; DIM | none | Also dims the CMDS counters; BRT is forced by FLOOD past HIGH INT, INST PNL fully counter-clockwise or loss of emergency DC |

### AIR COND Control Panel (p. 76)

Where: Centre of the right console, right of the lighting panel (figure on p. 75). Items 1 and 2 are numbered as in the figure.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. TEMP Knob | rotary | labels in the figure: COOL, MAN, AUTO, WARM and an OFF mark; order not read | none | N/I |
| 2. AIR SOURCE Knob | rotary | OFF; NORM; DUMP; RAM | none | OFF and RAM stop pressurisation, G-suit, canopy seal and external fuel transfer |

### KY-58 Secure Voice Panel (p. 77)

Where: Right of centre on the right console, below the anti-ice switches (figure on p. 75).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| KY-58 panel controls | not stated | not stated | not stated | N/I; the manual lists no individual controls |

### PLAIN/CIPHER Switch (p. 77)

Where: Top of the right console, next to the NUCLEAR CONSENT switch (figure on p. 75).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| PLAIN/CIPHER switch | toggle | PLAIN; CIPHER; labels CRAD 1 and CRAD 2 in the figure | none | N/I; plain or encrypted radio |

### OXYGEN Regulator Panel (p. 77)

Where: Bottom centre of the right console, below the arm rest (figure on p. 75). Items 1 to 5 are numbered as in the figure on p. 77.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. OXYGEN REGULATOR FLOW Indicator | display | white; black | blinker | White means oxygen flowing |
| 2. OXYGEN SUPPLY Indicator | gauge | PSI; normal 10 to 55; scale ends not stated | none | Oxygen pressure |
| 3. EMERGENCY Lever | lever | EMERGENCY; NORMAL; TEST MASK | none | N/I; positive pressure mode |
| 4. Diluter Lever | lever | 100%; NORM | none | N/I; air and oxygen mix |
| 5. SUPPLY Lever | lever | PBG; ON; OFF | none | PBG adds pressure breathing above 4 G |

### ENGINE ANTI-ICE Switch (p. 78)

Where: Upper right of the right console (figure on p. 75). Item 1 is numbered as in the figure on p. 78.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. ANTI-ICE ENGINE Switch | toggle | ON; AUTO; OFF | INLET ICING caution | AUTO heats when the detector sees ice; OFF disables detector and heaters |

### ANT SEL Panel (p. 78)

Where: Upper right of the right console, right of the anti-ice switch (figure on p. 75). Items 2 and 3 continue the numbers of the figure on p. 78.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 2. ANT SEL IFF Switch | toggle | UPPER; NORM; LOWER | none | NORM picks the stronger antenna |
| 3. ANT SEL UHF Switch | toggle | UPPER; NORM; LOWER | none | NORM alternates both antennas |

### AVIONICS POWER Control Panel (p. 78)

Where: Lower right of the right console (figure on p. 75). Items 1 to 9 are numbered as in the figure on p. 78.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. MMC Switch | toggle | ON; OFF | none | Modular mission computer |
| 2. ST STA Switch | toggle | ON; OFF | none | Stores stations under the wings and on the centreline |
| 3. MFD Switch | toggle | ON; OFF | none | Both MFDs |
| 4. UFC Switch | toggle | ON; OFF | none | ICP and DED |
| 5. MAP Switch | toggle | ON; OFF | none | Not functional in the Block 50 |
| 6. GPS Switch | toggle | ON; OFF | none | Needs a clear view of the sky; mission date limits apply (p. 79) |
| 7. DL Switch | toggle | ON; OFF | none | Secure modem datalink; N/I |
| 8. INS Knob | rotary | OFF; STOR HDG; ALIGN NORM; NAV; CAL; IN FLT ALIGN; ATT | none | CAL no function; keep the aircraft still during ground alignment |
| 9. MIDS LVT Knob | rotary | ZERO; OFF; ON | none | ZERO wipes the terminal memory |

### VOICE MESSAGE Switch (p. 80)

Where: Lower left of the right console, below the SNSR PWR panel (figure on p. 75).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| VOICE MESSAGE switch | toggle | INHIBIT; normal position not stated | none | INHIBIT silences all voice messages |

### ZEROIZE Switch (p. 80)

Where: Bottom left of the right console (figure on p. 75).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| ZEROIZE switch | toggle | OFP; OFF; DATA | none | Red cover in the figure; erases secure voice and GPS keys and other data |

### SEAT ADJ Switch (p. 80)

Where: Top left of the right console, beside the seat (figure on p. 75).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| SEAT ADJ switch | spring | up; centre (rest); down | none | Hold to raise or lower the seat |

### NUCLEAR CONSENT Switch (p. 80)

Where: Top of the right console, below the seat adjust switch (figure on p. 75).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| NUCLEAR CONSENT switch | toggle | not stated | none | Not implemented |

### Other right console fittings (pp. 75, 127)

Where: Utility light at the top right, arm rest at the bottom centre, DTU receptacle at the right edge (figure on p. 75). Only the DTU has a text description (p. 127).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Utility Light | lamp | not stated | none | Named in the figure only |
| Arm Rest | not stated | not stated | none | Named in the figure only; no control |
| DTU Receptacle | not stated | cartridge in; out | none | Takes the data transfer cartridge for the DTE MFD page |

## Ejection seat

### Ejection Seat Controls (pp. 81, 82)

Where: On the seat; the ejection handle at the front of the seat below the instrument panel, the arming lever on the left side of the seat and the manual chute lever on the seat (figures on pp. 81 and 82).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Ejection Handle | handle | pulled; not pulled | none | Not modelled in DCS; Left Ctrl + E starts the sequence |
| Ejection Seat Arming Lever | lever | up: disarmed; aft and down, flush: armed | SEAT NOT ARMED caution when up | Caution light on the caution panel |
| Emergency Manual Chute Lever | lever | not stated | none | N/I |

## Display-related controls

### Head-Up Display (HUD) (p. 90)

Where: Top centre of the cockpit at eye level, above the instrument panel; the combining glass is 25 degrees across (figure on p. 90).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Combining glass | display | not stated | HUD symbology | Content depends on master mode, sensors and the HUD control panel |

Symbology elements named in the figure on p. 90, numbered as there (details in the manual):
- 1 great circle steering cue; 2 current G; 3 steerpoint diamond; 4 horizon line; 5 velocity and velocity scale; 6 master arm status; 7 Mach number; 8 maximum G; 9 master mode status; 10 fuel / home bingo / bullseye status; 11 attitude bars; 12 boresight cross; 13 flight path marker; 14 altitude and altitude scale; 15 radar altitude; 16 altitude low setting; 17 slant range; 18 time to go; 19 distance to steerpoint and steerpoint number; 20 roll indicator; 21 heading scale.
- Shown only in some states (pp. 93, 94): bank angle indicator and vertical velocity scale (NAV mode with the scales switch at VV/VAH), manual bombing reticle with its depression setting (primary or secondary pattern, set with the ICP RET DEPR knob).

### HUD Control Panel (p. 94)

Where: Right console, left part, above the SNSR PWR panel (figure on p. 75; panel figure on p. 94). Items 1 to 8 are numbered as in the figure.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Scales Switch | toggle | VV/VAH; VAH; OFF | none | VV/VAH adds the vertical velocity scale and bank indicator; OFF leaves only digital read-outs |
| 2. Flightpath Marker Switch | toggle | ATT/FPM; FPM; OFF | none | ATT/FPM also shows the attitude bars |
| 3. DED/PFLD Switch | toggle | DED DATA; PFL; OFF | repeater in the lower HUD | OFF brings back the roll indicator |
| 4. Depressible Reticle Switch | toggle | STBY; PRI; OFF | reticle and its depression setting | STBY removes all other HUD symbols |
| 5. Velocity Switch | toggle | CAS; TAS; GND SPD | letter C, T or G beside the scale | Falls back to CAS in dogfight or with gear down |
| 6. Altitude Switch | toggle | ALT RADAR; BARO; AUTO (labels read from the figure) | none | N/I |
| 7. Brightness Control Switch | toggle | DAY; AUTO BRT; NIGHT | none | AUTO BRT is N/I |
| 8. Test Switch | toggle | ON; OFF (labels read from the figure; legend TEST STEP) | none | N/I |

### Integrated Control Panel (ICP) (p. 99)

Where: Top centre of the instrument panel, below the HUD and left of the DED (figures on pp. 44 and 99). Items 1 to 14 are numbered as in the figure on p. 99; groups of buttons use one row per button.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Override button COM 1 | button | press: UHF DED page; press again: previous page | legend COM 1 | Works from any DED page |
| 1. Override button COM 2 | button | press: VHF DED page; press again: previous page | legend COM 2 | Works from any DED page |
| 1. Override button IFF | button | press: IFF DED page; press again: previous page | legend IFF | The IFF page is not implemented |
| 1. Override button LIST | button | press: LIST DED page; press again: previous page | legend LIST | Lists the less used DED pages |
| 2. Master mode button A-A | button | press: air-to-air; press again in A-A: back to NAV | legend A-A | Top right |
| 2. Master mode button A-G | button | press: air-to-ground; press again in A-G: back to NAV | legend A-G | Top right |
| 3. SYM Knob | knob | up: brighter; down: dimmer; OFF mark in the figure | none | HUD symbology brightness; left edge |
| 4. RET DEPR Knob | knob | turn; 0 to 260 mils | none | Moves the manual bombing reticle in MAN mode; right edge |
| 5. Keypad key 1 | button | digit 1; on the CNI page opens T-ILS | legend T-ILS | Priority function keypad, top left |
| 5. Keypad key 2 | button | digit 2; on the CNI page opens ALOW | legends ALOW, N | N is a small letter in the figure |
| 5. Keypad key 3 | button | digit 3 | no function legend | No priority function |
| 5. Keypad key 4 | button | digit 4; on the CNI page opens STPT | legends STPT, W | W is a small letter in the figure |
| 5. Keypad key 5 | button | digit 5; on the CNI page opens CRUS | legend CRUS | |
| 5. Keypad key 6 | button | digit 6; on the CNI page opens TIME | legends TIME, E | E is a small letter in the figure |
| 5. Keypad key 7 | button | digit 7; on the CNI page opens MARK | legend MARK | |
| 5. Keypad key 8 | button | digit 8; on the CNI page opens FIX | legends FIX, S | S is a small letter in the figure |
| 5. Keypad key 9 | button | digit 9; on the CNI page opens A-CAL | legend A-CAL | |
| 6. RCL Button | button | press: erase the last digit; press again: drop the entry and restore the old value | legend RCL | Like backspace, then cancel |
| 7. ENTR Button | button | press | legend ENTR | Accepts the entry in the highlighted field |
| 8. BRT Knob | knob | turn; stops not stated | none | HUD raster brightness; no function in the Block 50 |
| 9. CONT Knob | knob | turn; stops not stated | none | HUD raster contrast; no function in the Block 50 |
| 10. 0/M-SEL Button | button | press: digit 0, a negative value, or cycle a page's modes | legend M-SEL | Also opens the MISC list from the LIST page |
| 11. DED Increment/Decrement Rocker | rocker | up; down | none | Changes the field marked with arrows; lower left |
| 12. Data Control Switch (DCS) | hat | RTN (left); SEQ (right); up; down | none | RTN returns the DED to CNI; SEQ cycles sub-pages; up and down move the asterisks or the arrow symbol |
| 13. DRIFT C/O & WARN RESET Switch | toggle | DRIFT C/O; NORM; WARN RESET | none | Spring-loaded to NORM from WARN RESET; DRIFT C/O cages the FPM and attitude bars; WARN RESET clears HUD warnings and sets max G to 1.0 |
| 14. TFR WX Button | button | press | none | No function in the Block 50 |
| 14. FLIR Increment/Decrement Rocker | rocker | up; down | none | No function in the Block 50 |
| 14. FLIR GAIN/LVL/AUTO Switch | toggle | GAIN; LVL; AUTO (labels read from the figure) | none | No function in the Block 50 |

### Data Entry Display (DED) (p. 101)

Where: Top of the centre column, right of the ICP and above the SAI (figure on p. 44).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| DED window | display | text; line count and width not stated on pp. 101 to 105 | LED text with asterisks around the active field | CNI is the home page; DCS to RTN returns to it and drops unaccepted entries |

DED pages (page numbers are the manual's; the pages themselves are not inventoried here):
- Always reachable: CNI home page p. 103 (fields 1 to 13); UHF via COM 1 pp. 104 and 253; VHF via COM 2 pp. 104 and 255; IFF via IFF p. 105, not implemented; LIST p. 105 and p. 117.
- Priority pages from the CNI page (p. 106): 1 T-ILS pp. 236 (TACAN) and 242 (ILS); 2 ALOW p. 107; 4 STPT p. 207; 5 CRUS with sub-pages TOS p. 108, RNG p. 110, HOME p. 112, EDR p. 114; 6 TIME p. 116; 7 MARK p. 219; 8 FIX p. 192; 9 A-CAL pp. 186 (AUTO ACAL) and 198 (MAN ACAL).
- LIST pages (p. 117): 1 DEST pp. 209 to 211 (UTM DEST, DEST DIR, DEST OA1 and OA2); 2 BNGO p. 118; 3 VIP pp. 353 and 354; 4 NAV pp. 181 and 182 (NAV STATUS, NAV COMMANDS); 5 MAN p. 119; 6 INS pp. 170 and 172; 7 CMDS pp. 700 to 702; 8 MODE p. 120; 9 VRP pp. 347 and 348; R INTG not implemented; E DLNK pp. 458 to 461 (NET STATUS, TNDL, TNDL STN); 0 MISC p. 121.
- MISC pages (p. 121): 2 MAGV p. 173; 5 LASR p. 503; 8 BULL p. 357; R HMCS pp. 553 and 554; E HTS p. 538; 0 HARM p. 658; CORR, OFP, INSM, GPS and DRNG are not implemented.

### Multi-Function Display (MFD) bezel (p. 122)

Where: Two identical MFDs on the instrument panel, one left and one right of the centre column (figure on p. 122). Both bezels carry the same controls; MFD power is on the AVIONICS POWER panel.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Screen | display | 4 x 4 in colour LCD | formats and pages | Video and text from the sensors and systems |
| 1. OSB 1 to 5 | button | top row, 1 at the far left to 5 at the far right | legends on screen | Function depends on the format; highlighted legend means active |
| 1. OSB 6 to 10 | button | right column, 6 at the top to 10 at the bottom | legends on screen | |
| 1. OSB 11 to 15 | button | bottom row, 11 at the far right to 15 at the far left | legends on screen | 12 to 14 are the format select buttons, 15 is SWAP |
| 1. OSB 16 to 20 | button | left column, 16 at the bottom to 20 at the top | legends on screen | |
| 2. GAIN Rocker | rocker | up; down; hold to run to the limit | none | Sensor video intensity; FCR map or MTI gain; TGP FLIR gain in manual gain; top left corner |
| 3. SYM Rocker | rocker | up; down; hold to run to the limit | none | Symbology intensity; top right corner |
| 4. BRT Rocker | rocker | up; down; hold to run to the limit | none | Overall brightness; bottom left corner |
| 5. CON Rocker | rocker | up; down; hold to run to the limit | none | Overall contrast; bottom right corner |

### MFD Format Selection Master Menu (p. 124)

Where: A page shown on either MFD; it is reached by pressing an already highlighted format select button (OSB 12 to 14, see p. 126), and its legends sit on the same OSBs (figure on p. 124). Items 1 to 17 are numbered as in the figure.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. BLANK Format | button | OSB 1 | legend BLANK | Gives a format select button no format; it drops out of the DMS cycle |
| 2. HAD Format | button | OSB 2 | legend HAD | HARM attack display |
| 3. RCCE Format | button | OSB 4 | legend RCCE | Reconnaissance; not functional |
| 4. RESET MENU Page | button | OSB 5 | legend RESET MENU | Reset symbology, brightness and contrast; N/I |
| 5. FCR Format | button | OSB 20 | legend FCR | Fire control radar |
| 6. TGP Format | button | OSB 19 | legend TGP | Targeting pod |
| 7. WPN Format | button | OSB 18 | legend WPN | Missile video and control |
| 8. TFR Format | button | OSB 17 | legend TFR | Not functional |
| 9. FLIR Format | button | OSB 16 | legend FLIR | Not functional |
| 10. SMS Format | button | OSB 6 | legend SMS | Stores management |
| 11. HSD Format | button | OSB 7 | legend HSD | Horizontal situation display |
| 12. DTE Format | button | OSB 8 | legend DTE | Data transfer from the cartridge |
| 13. TEST Format | button | OSB 9 | legend TEST | N/I |
| 14. FLCS Format | button | OSB 10 | legend FLCS | N/I |
| 15. Swap Button | button | OSB 15 | legend SWAP | Swaps formats and their button assignments between the two MFDs |
| 16. Format Select Buttons | button | three buttons, OSB 12, 13, 14 (see notes at the end of the section) | format names on screen | Pick the format shown; a second press of a highlighted one opens this page |
| 17. Declutter Button | button | OSB 11 | legend DCLT | N/I; hides OSB legends but keeps their commands |

Reassigning formats (p. 126):
- Each of the seven master modes (NAV, A-A, A-G, MSL override, dogfight, selective jettison, emergency jettison) starts with its own format layout, and the pilot can change it per mode.
- Press a highlighted format select OSB to open this page (press once to highlight, again to open; an empty BLANK button also needs the highlight step), then press the OSB next to the wanted format.
- One format can sit on only one select button of either MFD at a time, except BLANK; assigning a format already used elsewhere moves it and puts BLANK on the old button.
- The manual disagrees with itself: p. 124 text names OSB 13 to 15 as the format select buttons, p. 126 names OSB 12 to 14, and the figures show SWAP at OSB 15 and DCLT at OSB 11.

## Defensive systems

### Threat Warning Azimuth Indicator (p. 694)

Where: Upper left portion of the instrument panel (p. 694; figure on p. 44); the prime control panel is to its left.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Azimuth scope | display | circular, own aircraft at the centre; 360 degrees | threat symbols; centre S and L marks | More lethal threats sit nearer the centre; solid circle separates tracking from missile guidance |
| Brightness knob | knob | turn; stops not stated | none | Top left corner of the display |

Symbol rules (p. 694):
- Search or acquisition radar: symbol at the outside of the scope.
- Tracking radar: symbol just outside the solid circle, boxed.
- Missile guidance: symbol inside the solid circle with a flashing circle.
- Airborne radar: chevron over the symbol.
- Diamond: marks the top priority threat when handoff is floating; handoff off removes it, and removes the RWR diamond and direction marks in the HMCS.
- Up to 16 threats show in OPEN mode and 5 in PRIORITY mode (p. 695). The full symbol list is Appendix B (pp. 749 to 752).

### Threat Warning Prime Control Panel (p. 695)

Where: Instrument panel, upper left, left of the azimuth indicator (figure on p. 695). Items 1 to 6 are numbered as in the figure; each button is lit by legends in its upper and lower halves.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. HANDOFF Button | button | short press: floating / off; hold over 1 s: transient, cycles the diamond through threats; release: latched | HANDOFF diamond | Diamond is dark when handoff is off |
| 2. MODE Button | button | press: OPEN / PRIORITY | OPEN (lower), PRIORITY (upper) | OPEN shows 16 threats, PRIORITY shows 5 |
| 3. LAUNCH Button | button | press | MISSILE LAUNCH flashes | Flashes when a radar is in missile guidance mode; press function not stated |
| 4. TGT SEP Button | button | press | TGT SEP | Spreads overlapping symbols outward for 5 s |
| 5. UNKNOWN Button | button | press: enable / disable unknown radars | U lit; U flashes when disabled and unknown radars exist | Shows unidentified radars with a U symbol |
| 6. SYS TEST Button | button | press and hold 1 s; press again to abort | ON | Test lights all buttons on both threat warning panels, shows diagnostics and plays tones |

### Threat Warning Auxiliary Control Panel (p. 696)

Where: Left auxiliary console, left of the CMDS panel (figure on p. 696). Items 1 to 5 are numbered as in the figure.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. SEARCH Button | button | press: enable / disable search radars | S lit; S flashes when disabled and such radars exist | Shows an S at the scope centre when enabled |
| 2. ACT/PWR Button | button | press function not stated | POWER (lower) lit when powered; ACTIVITY (upper) lit on a tracking or guidance radar | Mostly an indicator |
| 3. ALTITUDE Button | button | press: high / low altitude threat table | ALT (lower); LOW (upper) in low mode | Low mode shows an L at the scope centre |
| 4. POWER Button | button | press: ALR-56M on / off | SYSTEM POWER | Powers the receiver |
| 5. DIM Knob | knob | turn clockwise: brighter | none | Dims the lights of both threat warning panels |

### CMDS Control Panel (p. 697)

Where: Left auxiliary console, below the landing gear panel and right of the threat warning aux panel (figure on p. 55; panel figure on p. 697). Items 1 to 9 are numbered as in the figure; item 4 holds four switches.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Status Display | display | NO GO; GO; DISPENSE RDY | green text | DISPENSE RDY in SEMI means consent is wanted, with a Counter voice message |
| 2. Quantity Display | display | two counts (CH and FL) in the figure; O1 and O2 unused | green digits; LO beside a low type | Also shows failure messages |
| 3. RWR Switch | toggle | ON; OFF | none | Lets SEMI and AUTO use RWR threat data |
| 4. O1 Switch | toggle | ON; OFF | none | No function in DCS |
| 4. O2 Switch | toggle | ON; OFF | none | No function in DCS |
| 4. CH Switch | toggle | ON; OFF | chaff count shown above it | Enables chaff dispensing |
| 4. FL Switch | toggle | ON; OFF | flare count shown above it | Enables flare dispensing |
| 5. JMR Switch | toggle | ON; OFF | none | No function in DCS |
| 6. MWS Switch | toggle | ON; OFF | none | No function in DCS |
| 7. JETT Switch | toggle | JETT (forward); OFF | none | Dumps all chaff and flares in any MODE position |
| 8. PRGM Knob | rotary | BIT; 1; 2; 3; 4 | none | Picks the manual program for CMS forward; BIT is N/I |
| 9. MODE Knob | rotary | OFF; STBY; MAN; SEMI; AUTO; BYP | status display | OFF no power; STBY edits only; MAN manual programs; SEMI auto program on consent; AUTO auto programs; BYP one chaff and one flare per CMS forward |

CMDS notes (pp. 698 to 701):
- Manual programs 1 to 4 follow the PRGM knob (CMS forward), program 5 is the CHAFF/FLARE button (p. 708), program 6 is CMS left.
- MAN: ECM noise jamming on with CMS aft (XMIT at 3), off with CMS right.
- SEMI: CMS aft sends one auto program and enables deception jamming (XMIT at 1 or 2); CMS right disables the ECM pod; auto programs are blocked when chaff is LO.
- AUTO: consent is on each time the knob enters AUTO; CMS aft grants it, CMS right revokes it and interrupts running programs.
- Edits to bingo counts and program timing are made on the CMDS DED pages (pp. 700 to 702) with the knob at STBY.

### ECM Control Panel (p. 706)

Where: Bottom of the left console, between the AVTR and AUDIO panels (figure on p. 62; panel figure on p. 706). Items 1 to 6 are numbered as in the figure; item 6 is eight buttons.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. ECM Power Switch | toggle | OPR; STBY; OFF | none | STBY warms the pod for about 3 min |
| 2. XMIT Switch | toggle | 1 (deception, avionics priority); 2 (deception, ECM priority); 3 (noise, ECM priority) | none | 1 and 2 need CMDS at SEMI or AUTO; 3 needs MAN |
| 3. DIM Knob | knob | turn; stops not stated | none | Dims the lights on the band buttons |
| 4. RESET Button | button | press | none | No function in DCS |
| 5. BIT Button | button | press | none | N/I |
| 6. ECM Module Control Button 1 | button | latched in; latched out | S, A, F, T status lights | Band 1 module on or off |
| 6. ECM Module Control Button 2 | button | latched in; latched out | S, A, F, T status lights | Band 2 module |
| 6. ECM Module Control Button 3 | button | latched in; latched out | S, A, F, T status lights | Band 3 module |
| 6. ECM Module Control Button 4 | button | latched in; latched out | S, A, F, T status lights | Band 4 module |
| 6. ECM Module Control Button 5 | button | latched in; latched out | S, A, F, T status lights | Band 5 module |
| 6. ECM Module Control Button (unmarked) | button | latched in; latched out | S, A, F, T status lights | Spare module slot |
| 6. ECM Module Control Button FRM | button | latched in; latched out | S, A, F, T status lights | No function in DCS |
| 6. ECM Module Control Button SPL | button | latched in; latched out | S, A, F, T status lights | No function in DCS |

Status lights on each module button (p. 707): S standby, A active, F failed, T transmitting. All pods and modules act the same in DCS.

### CHAFF/FLARE Dispense Button (p. 708)

Where: Left cockpit wall, outboard of and above the throttle, just aft of the canopy locking lever (figure on p. 708).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| CHAFF/FLARE Dispense button | button | press | none | Dispenses manual program 5 in MAN, SEMI and AUTO; independent of the CMS |

## Summary

Panel sections and control rows per area. A row is one control, lamp, gauge or display; the HOTAS rows hold all functions of a switch in one cell.

| Area | Panel sections | Control rows |
| --- | --- | --- |
| Hands-on controls (HOTAS) | 2 | 17 |
| Instrument panel | 16 | 96 |
| Left auxiliary console | 3 | 14 |
| Right auxiliary console | 8 | 39 |
| Left console | 19 | 88 |
| Right console | 14 | 38 |
| Ejection seat | 1 | 3 |
| Display-related controls | 6 | 64 |
| Defensive systems | 6 | 39 |
| Total | 75 | 398 |

Notes on the counts:
- The instrument panel count includes one section without rows, the Autopilot controls cross-reference (pp. 129 to 132); it only lists what the manual says about controls already in other rows.
- The HUD control panel sits on the right console in the cockpit, but is counted under display-related controls; the CMDS and THREAT WARNING AUX panels sit on the left auxiliary console and the ECM panel on the left console, but all three are counted under defensive systems.
- Three sections group several small items: Ejection Seat Controls (3 rows), Other right console fittings (3 rows) and the ICP (28 rows for the 14 numbered items, because buttons and keys are split into one row each).
- Not inventoried by design: the DED pages (only listed with page numbers), the MFD formats, the HUD symbology details and the ICP-driven start-up and navigation procedures.

Controls whose positions or function the manual does not state, for phase 3 (matching with DCS-BIOS) and phase 7 (check in DCS):

Named in a figure or text with no description of function or positions:
- Throttle Cutoff Release (p. 86): function and positions.
- ALT GEAR handle (p. 57): positions and travel.
- Manual canopy handcrank, ANTI-G TEST button (both only named in the figure on p. 62).
- AVTR control panel (p. 66) and KY-58 panel (p. 77): no individual controls described.
- NUCLEAR CONSENT switch (p. 80, not implemented) and MAX POWER switch (p. 63): positions not stated.
- Utility light, arm rest, DTU receptacle (p. 75): no description beyond the name; the DTU is described only as a cartridge slot (p. 127).
- A PEDAL ADJ knob is visible in the figure on p. 81 but is not named in the text.
- LAUNCH button (p. 695) and ACT/PWR button (p. 696): what a press does is not stated.

Knob end stops, ranges and steps not stated (phase 7):
- SET INDEX, barometric setting, heading set and course set knobs (end stops, steps per turn).
- AUDIO 1 and AUDIO 2 volume knobs, UHF backup VOL knob.
- Interior LIGHTING knobs (only the HIGH INT detent on FLOOD CONSOLES is named).
- ECM DIM, threat warning DIM, azimuth indicator brightness, HMCS brightness, ICP SYM, BRT and CONT knobs.
- FORM and AERIAL REFUELING knob end stops.
- Manual trim wheels and the yaw trim knob: range and clicks.
- Scale ends: NOZ POS gauge, fuel flow indicator, Kollsman window, oxygen supply gauge, SAI and ADI bank pointer limits.
- AIR COND TEMP knob: positions are only readable as labels in the figure (N/I).
- ICP RET DEPR direction, DED increment/decrement rocker direction and the up/down use of the DCS.

Switch directions and return behaviour not stated in the text (read from figures or inferred; check in DCS):
- Which direction is ON for the AVIONICS POWER, SNSR PWR, CMDS, anti-ice, ANT SEL and most other 2-position toggles.
- Which toggles spring back: FLCS RESET, EPU/GEN test, ICP DRIFT C/O switch (spring from WARN RESET only), altimeter mode switch (held), CMDS JETT.
- Positions read from the figures only: FLT CONTROL MANUAL TF FLY-UP, HUD control panel altitude and test switches, ICP FLIR GAIN/LVL/AUTO switch, UHF backup SQUELCH switch, ZEROIZE (OFP, OFF, DATA), VOICE MESSAGE normal position, PLAIN/CIPHER labels, IFF MODE 4 REPLY order, EXT LIGHTING MASTER order.

Contradictions inside the manual:
- p. 56 text calls the switch next to the brakes channel switch ANTI-SKID, its figure label says PARKING BRAKE.
- pp. 124 and 126 disagree on which OSBs are the format select buttons (13 to 15 versus 12 to 14); the figure on p. 124 puts SWAP at OSB 15 and DCLT at OSB 11.
