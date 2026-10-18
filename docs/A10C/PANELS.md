# A-10C II – cockpit panels

Inventory of the cockpit controls, taken from the DCS A-10C II flight manual (see [RESEARCH.md](RESEARCH.md)). Page numbers are the manual's pages. Written in our own words; no text or pictures are copied from the manual. DCS-BIOS identifiers are added in phase 3.

Control types: `toggle` (2 or 3 positions), `spring` (spring-loaded, returns to a rest position), `button` (push button), `guarded` (has a cover), `rotary` (selector with fixed positions), `knob` (continuous), `rocker`, `hat` (multi-way switch), `lever`, `handle`, `lamp`, `display`, `gauge` (needle, drum or flag).

## Control stick and throttles (HOTAS)

Functions depend on the selected sensor of interest (SOI). Columns used: TAD, TGP, HUD, A-A, MAV, HMCS, HMCS B/S (boresight), MSG. Long press means held about 1 second or more. A function written without an SOI applies to all of them.

### Control Stick (p. 106)

Where: Centre-mounted full-motion stick, right hand (figure on p. 108).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Master Mode Control Button (MMCB) | button | depress short: toggle HUD; depress long: enter A-A | none | Same in every SOI |
| 2. Data Management Switch (DMS) | hat | fwd short: TAD scale down; TGP zoom and focus up; HUD, A-A steerpoint increment; MAV boresight reticle up; HMCS brightness up; HMCS B/S text rotate CCW; MSG change shape. fwd long: TAD map quick toggle; MAV reticle up with gyro stab; MSG drop shape; others as short. aft short: TAD scale up; TGP zoom and focus down; HUD, A-A steerpoint decrement; MAV boresight reticle down; HMCS brightness down; HMCS B/S text rotate CW; MSG none. aft long: TAD select TAD centre option; others as short. left short: TAD CEN/DEP mode, centre on own; TGP, HMCS right MFCD video on HMD; HUD, A-A gunsight profile toggle; MAV boresight reticle left; HMCS B/S boresight roll CCW; MSG none. left long: HMD on/off (HMCS B/S stays roll CCW). right short: TAD cycle TAD centre option; TGP laser/IR pointer toggle; HUD, A-A gunsight profile toggle; MAV boresight reticle right; HMCS cycle HMCS profiles; HMCS B/S boresight roll CW; MSG none. right long: slave TGP to HMCS LOS (MAV: slave Maverick to HMCS; HMCS B/S stays roll CW) | none | Long press same as short unless listed |
| 3. Target Management Switch (TMS) | hat | fwd short: TAD hook symbol under cursor; TGP area/point/NR track; HUD TDC ground stabilise; A-A conical scan; MAV track; HMCS hook symbol under crosshair; HMCS B/S comp BS/sett occl pt. fwd long: make SPI (TAD, HMCS: make hooked object SPI; HMCS B/S: complete occl pt). aft short: TAD, HMCS un-hook symbol; TGP FLIR auto focus; HUD IFFCC wpns sol. SPI; A-A break lock; MAV ground stabilise; HMCS B/S remove occl pt. aft long: reset SPI to current steerpoint. left short: acknowledge W/C/N and message receipt. left long: SPI broadcast. right short: mark at TAD cursor (TAD), TGP LOS (TGP), TDC (HUD, A-A), Maverick LOS (MAV), HDC (HMCS). right long: make last markpoint SPI | none | Left, aft long and right long: same in all SOI |
| 4. Nosewheel Steering (NWS) Button | button | depress: on ground NWS engage/disengage; in air laser/IR pointer HOT fire and toggle fire; during AR disconnect/reset | STEERING ENGAGED lamp, see p. 134 | Same in every SOI |
| 5. Countermeasures Switch (CMS) | hat | fwd short: 1 flare; fwd long: next program; aft short: 1 chaff; aft long: previous program; left short: 6 flares; right short: 6 chaff; depress short: activate/deactivate selected program; depress long: activate/deactivate ECM | none | Same in every SOI |
| 6. Weapon Release Button | button | press | none | Function not stated on these pages |
| 7. Trim Switch | hat | pitch and roll stick neutral trim; direction mapping not stated | none | Manual calls it the trim hat |
| 8. Trigger | button | pull | none | Needs MASTER at ARM; PAC may be tied to first stage |

### Throttles (p. 111)

Where: Left console, left hand; two levers, grip controls on both (figure on p. 111).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Left throttle lever | lever | full aft: OFF; past the hump: IDLE; forward: more thrust up to max | none | Hump starts auto-start once other startup steps are done |
| Right throttle lever | lever | full aft: OFF; past the hump: IDLE; forward: more thrust up to max | none | Left, right and linked up/down commands exist |
| 1. Mic Switch | hat | fwd: VHF AM transmit (audio rotary at VHF); aft: VHF FM transmit; up: no function; down: UHF transmit | none | Same in every SOI; up has no function in DCS |
| 2. Speed Brake | toggle | fwd: retract; center: hold position; aft: extend | none | Same in every SOI |
| 3. Boat Switch | toggle | fwd: TGP FLIR black hot (MAV: Maverick black hot); center: TGP CCD (MAV: Maverick force correlate mode); aft: TGP FLIR white hot (MAV: Maverick white hot) | none | MAV column differs, others use TGP |
| 4. China Hat | spring | fwd short: TGP toggle FOV; HUD change LSS FOV; A-A show Maverick video, SOI to Maverick; MAV uncage / consent to self-track; HMCS change FOV; HMCS B/S change TGP or LSS FOV; TAD, MSG none. fwd long: slave all to SPI. aft short: TAD reset cursor; TGP toggle LSS; HUD cage TDC to TVV; A-A, MAV re-cage / manual sequence; HMCS cage HDC to crosshairs; HMCS B/S, MSG none. aft long: slave TGP to current steerpoint | none | Long press same in every SOI |
| 5. Pinky Switch | toggle | fwd: position lights dim and steady, strobes off; center: all exterior lights off; aft: exterior lights per lighting panel | none | Marked invisible in the figure |
| 6. Left Throttle Button | button | press short: LAAP | none | Same in every SOI |
| 7. Slew Control | hat | slew: TAD cursor; TGP seeker head; HUD TDC; A-A seeker head; MAV seeker head; HMCS HDC; HMCS B/S boresight; MSG cursor. Z-axis: no function listed | none | Z-axis row is empty in the table |
| 8. Coolie Hat | hat | up short: SOI to HUD; up long: messages quick-look; down short: SOI to HMCS; down long: DSMS weapon status and profile pages quick-look; left short: cycle left MFCD page; left long: SOI to left MFCD; right short: cycle right MFCD page; right long: SOI to right MFCD | none | Main way to set SOI; same in every SOI |

## Left front dash

### Left Engine "T-Handle" Fire Extinguisher Discharge Select (p. 114)

Where: Below the HUD, left part of the front dash (item 1 in the figure on p. 113).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Left engine T-handle | handle | not pulled; pulled | fire lamp in the handle | Pull selects left engine as extinguisher target |
| Left engine fire lamp | lamp | lit; unlit | lit on left engine fire; legend FIRE ENG PULL | Discharge switch is on another panel |

### Radar Warning Receiver (RWR) Display (p. 115)

Where: Left front dash, upper right, below the gun and NWS lights and above the airspeed indicator.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Azimuth indicator | display | circular scope | emitter bearings; missile launch bearing | Details in the Defensive Systems chapter |

### Airspeed Indicator (p. 116)

Where: Left front dash, below the RWR display.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Current airspeed pointer | gauge | 0 to 550 kt, ticks every 10 kt | solid white pointer | Yellow mark at 200 kt: maximum flap and gear speed |
| Maximum speed pointer | gauge | follows altitude limit | striped black and white pointer | Maximum allowed speed for current altitude |
| Decimals drum | gauge | rotary drum | none | Reads decimals of the main dial |

### Standby Attitude Indicator (SAI) (p. 117)

Where: Left front dash, below the airspeed indicator, left of the UHF repeater.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Attitude display | gauge | pitch and roll; scale not stated | none | Independent backup to the ADI |
| OFF warning flag | gauge | shown; hidden | flag on left side | Shown when unpowered or caged |
| Cage knob (PULL TO CAGE) | knob | pull: cage; turn: adjust level pitch angle | none | Lower right of the gauge |

### UHF Frequency Repeater (p. 118)

Where: Left front dash, right of the SAI, above the angle of attack indicator.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| UHF preset frequency readout | display | not stated | frequency window, legend UHF | Repeats the AN/ARC-164 preset |

### Angle of Attack Indicator (p. 118)

Where: Left front dash, lower right, below the UHF repeater and right of the clock.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Angle of attack pointer | gauge | 0 to 30 units, 1 unit per tick | pointer from centre | Rests at 0 with no power |
| OFF warning flag | gauge | shown; hidden | red flag, right side | Shown when unpowered |

### Digital Clock (p. 119)

Where: Left front dash, lower left of the instrument column, left of the angle of attack indicator.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Time readout | display | HH:MM:SS, seconds on bottom | mode letters C (clock) and ET (elapsed time) | Default is clock mode |
| Digital second hand | display | rotates around the rim | segments on the periphery | Shows seconds |
| SEL button (1) | button | press | none | Switches between clock and elapsed time |
| CTRL button (2) | button | press | none | Elapsed time: 1st start, 2nd stop, 3rd reset; clock: no function |

### Emergency Jettison Button (p. 120)

Where: Top left of the front dash, above the left MFCD.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| EXT STORES JETT button | button | press; works with gear handle in any position | none | Drops stations 1 to 11 except TGP and ECM pod |

### Left Multifunction Color Display (MFCD) (p. 121)

Where: Left front dash, upper left, below the jettison button; bezel only, pages come later.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Screen | display | 5 x 5 in | MFCD pages | Powered through the CICU switch on the AHCP |
| OSB 1 to 5 | button | 5 buttons along the top; order within side not stated | legends on screen | Function depends on page |
| OSB 6 to 10 | button | 5 buttons along the right side; order within side not stated | legends on screen | Function depends on page |
| OSB 11 to 15 | button | 5 buttons along the bottom; order within side not stated | legends on screen | OSB 11 is declutter by default |
| OSB 16 to 20 | button | 5 buttons along the left side; order within side not stated | legends on screen | 20 OSBs in total |
| ADJ rocker | rocker | + / - | none | TAD manual map mode: zoom in and out |
| DSP rocker | rocker | + / - | none | Backlight brightness; no function in DCS |
| CON rocker | rocker | + / - | none | Video contrast; no function in DCS |
| BRT rocker | rocker | + / - | none | Display brightness |
| SYM rocker | rocker | - / + | none | Symbol brightness; no function in DCS |
| Day / night / off select | rotary | DAY; NT; OFF | none | Lower left of bezel; OFF cuts power to the MFCD |

### Landing Gear and Flap Control Panel (p. 125)

Where: Left front dash, lower left, below the left MFCD, left of the AHCP.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Landing lights switch (LIGHTS LAND) | toggle | LAND; OFF; TAXI | none | TAXI: taxi light only; LAND: landing and taxi |
| 2. Downlock solenoid override button | button | press | none | Lets handle go UP with weight on wheels |
| 3. Landing gear handle (LGD GEAR DOWN) | lever | UP; DOWN | red lamp in handle | UP needs no weight on wheels or override |
| Gear handle lamp | lamp | lit; unlit | red, in the handle | Lit in transit and until gear locks |
| 4. Anti-skid switch | toggle | OFF (bottom); other position not stated | none | Prevents wheel lock when braking |
| 5. L SAFE gear light | lamp | lit; unlit | green when left main down and locked | Unlit when up and locked |
| 5. N SAFE gear light | lamp | lit; unlit | green when nose gear down and locked | Unlit when up and locked |
| 5. R SAFE gear light | lamp | lit; unlit | green when right main down and locked | Unlit when up and locked |
| 6. Flap position indicator (FLAPS DEGREES) | gauge | 0 to 30 degrees; scale labels 0, 10, 20, 30 | pointer | Flaps UP 0, MVR 7, DN 20; set from throttle |
| 7. TEMS DATA switch | button | not stated | none | No function in DCS |

### Armament HUD Control Panel (AHCP) (p. 129)

Where: Left front dash, lower centre, below the left MFCD, right of the gear panel; positions listed top to bottom.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. MASTER | toggle | ARM; SAFE; TRAIN | none | ARM enables gun, jettison, trigger; TRAIN: blue DSMS |
| 2. GUN/PAC | toggle | ARM; SAFE; GUNARM | RDY status on HUD | ARM gun with PAC; GUNARM gun without PAC |
| 3. LASER | toggle | ARM; SAFE; TRAIN | L on TGP page when not SAFE | ARM combat power; TRAIN training energy |
| 4. TGP | toggle | ON; OFF | TGP OFF on standby page when off | ON powers pod, starts FLIR cooldown |
| 5. ALT SCE | toggle | BARO; DELTA; RADAR | none | Altitude source: baro, baro-radar difference, radar |
| 6. HUD MODE day/night | toggle | DAY; NIGHT | none | DAY green, NIGHT amber |
| 6. HUD MODE norm/standby | toggle | NORM; STBY | none | Normal or standby HUD mode |
| 7. CICU | toggle | ON; OFF | DTS load page on both MFCDs | Powers both MFCDs and their subsystems |
| 8. JTRS | toggle | ON; OFF | none | Powers the datalink |
| 9. IFFCC | toggle | ON; TEST; OFF | HUD; settings display in TEST | Powers IFFCC and HUD; HUD starts in GUNS |

### Heading Attitude Reference (HARS) Fast Erect Button (p. 133)

Where: Bottom of the left front dash, below the AHCP.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| HARS FAST ERECT button | button | press | clears OFF flag on ADI | Re-cages HARS gyro; use in straight and level flight |

### Gun and Nose Wheel Steering (NWS) Lights (p. 134)

Where: Top of the left front dash, above the RWR display at eye level.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| GUN READY light | lamp | lit; unlit | green legend GUN READY | Lit when gun is armed and ready |
| STEERING ENGAGED light | lamp | lit; unlit | green legend STEERING ENGAGED | Lit when nosewheel steering is on |

## Center front dash

### APU "T Handle" Fire Extinguisher Discharge Select (p. 136)

Where: Below the HUD, centre of the dash, above the CMSC (item 1 in the figure on p. 135).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| APU T-handle | handle | not pulled; pulled | fire lamp in the handle | Pull selects APU as extinguisher target |
| APU fire lamp | lamp | lit; unlit | lit on APU fire; legend FIRE APU PULL | Discharge switch is on the right dash (p. 144) |

### Countermeasures Set Control (CMSC) (p. 136)

Where: Centre of the front dash, below the APU T-handle, above the ADI (item 2 on p. 135); physical panel only, operation comes later.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Upper arrow button | button | press; label is an arrow, name not stated | none | Left edge, beside the JMR window |
| Lower arrow button | button | press; label is an arrow, name not stated | none | Left edge, beside the MWS window |
| JMR window | display | strip of about 4 cells | green segment characters | Legend JMR; manual text says ECM status, mapping not stated |
| MWS window | display | strip of about 4 cells | green segment characters | Legend MWS; missile warning status |
| CHAFF / FLARE window | display | one strip under both legends, about 4 cells | green segment characters | Legends CHAFF and FLARE; split of cells not stated |
| Left RWR-area lamp | lamp | lit; unlit | small square, no legend | Under CHAFF; meaning not stated |
| Right RWR-area lamp | lamp | lit; unlit | small square, no legend | Under FLARE; meaning not stated |
| RWR PRI button | button | press | none | Under legend RWR; function later |
| RWR SEP button | button | press | none | Under legend RWR; function later |
| RWR UNK button | button | press | none | Under legend RWR; function later |
| BRT knob | knob | turn; stops not stated | none | Lower left; label BRT |
| AUD knob | knob | turn; stops not stated | none | Lower left, right of BRT; label AUD |
| ML lamp | lamp | lit; unlit | small square, legend ML | Next to AUD knob; meaning not stated |

### Attitude Director Indicator (ADI) (p. 137)

Where: Centre of the front dash, below the CMSC, above the HSI (item 3 on p. 135).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Attitude sphere | gauge | pitch and roll; light upper half, dark lower half; dashed horizon line | pitch angle marks | Pitch mark spacing not stated |
| 2. Miniature aircraft | display | winged W-shaped marker at centre | none | Shows pitch and roll against the sphere |
| 3. Bank scale | gauge | ticks at 10, 20, 30, 60, 90 degrees | none | Around the lower half of the casing |
| 3. Bank pointer | gauge | white triangle moves along the bank scale | none | Rides with the sphere |
| 4. Slip ball | gauge | ball in liquid tube; centred = no slip | none | Under the sphere |
| 4. Turn indicator | gauge | yaw rate; scale not stated | none | Just below the slip ball |
| 5. Pitch trim knob | knob | turn to offset the aircraft symbol from the horizon | none | Lower right of the gauge |
| 5. Pitch trim index | display | small triangle at zero pitch setting | none | Next to the knob |
| 6. Course warning flag | gauge | shown; hidden | red flag at top | Shown in ILS or TACAN mode without signal |
| 7. Bank steering bar | gauge | vertical bar, left or right of centre | none | Centred means on desired bearing; also TISL, FM homing |
| 8. Pitch steering bar | gauge | horizontal bar, above or below centre | none | Glide slope, FM station signal strength, TISL target |
| 9. Glide slope warning flag | gauge | shown; hidden | red flag at left | Shown when no glide slope signal |
| 10. Glide slope deviation scale | gauge | centre line with 2 dots above and 2 below | none | Left side |
| 10. Glide slope indicator | gauge | white chevron moves up and down the scale | none | Text: chevron below centre means too high |
| 11. Attitude warning flag (OFF) | gauge | shown; hidden | OFF flag, lower left | Shown without power and while HARS fast erect is held |

### Horizontal Situation Indicator (HSI) (p. 139)

Where: Centre of the front dash, below the ADI, above the NMSP (item 4 on p. 135).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Power OFF flag | gauge | shown; hidden | red OFF flag, right side | Shown without power |
| 2. Compass card | gauge | rotating, 360 degrees | none | Top of card is magnetic heading |
| 3. Aircraft symbol | display | fixed symbol at centre | none | Reference for all HSI readings |
| 4. Lubber line | display | fixed line from symbol to top | none | Marks current heading on the card |
| 5. Range indicator | display | 3-digit drum, nautical miles | striped white and orange flag over digits when unpowered | Slant range to steerpoint or TACAN; upper left, legend MILES |
| 6. Bearing pointer 2 | gauge | arrow head to current steerpoint; tail opposite | none | Tail is the reciprocal bearing |
| 7. Bearing pointer 1 | gauge | long thin arrow; head to TACAN or UHF ADF bearing | none | ADF wins over TACAN; fallback text unclear |
| 8. Heading set knob | knob | turn; stops not stated | none | Lower left; moves the heading marker |
| 9. Heading marker | gauge | two thick marks on the outside of the card | none | Turns with the card once set |
| 10. Bearing validity flag | gauge | shown; hidden | none | Shown when far off course |
| 11. Course set knob | knob | turn; stops not stated | none | Lower right; sets course window and arrows |
| 12. Course selector window | display | course in degrees | numeric window, upper right, legend COURSE | Digit count not stated |
| 13. Course arrow | gauge | two lines on the card: course and reciprocal | none | Set with the course knob |
| 14. Course deviation indicator (CDI) | gauge | line through centre; offset left or right | none | Through the symbol means on course |
| 15. To-From indicator | gauge | two triangles along the course line | none | Shows to or from the station or steerpoint |

### Navigation Mode Select Panel (NMSP) (p. 140)

Where: Centre of the front dash, directly below the HSI (item 5 on p. 135); numbers below follow the figure on p. 141.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. HARS button | button | press | green triangle when active | HARS drives HSI, ADI, HUD; default at cold start |
| 10. PTR switch | toggle | ABLE; STOW (ABLE label on the left in the figure) | none | STOW hides steering bars and course flag, unless TISL or FM homing |
| 2. EGI button | button | press | green triangle when active | CDU-driven data; needed for velocity vector; excludes HARS |
| 3. TISL button | button | press | green triangle when active | Laser spot tracker drives ADI steering bars |
| 4. STR PT button | button | press | green triangle when active | Sets HSI CDI to the steerpoint |
| 5. ANCHR button | button | press | green triangle when active | Uses the CDU anchor point |
| 6. TCN button | button | press | green triangle when active | Uses the selected TACAN station |
| 7. ILS button | button | press | green triangle when active | Glide slope on ADI, localizer on HSI |
| 8. UHF homing light | lamp | lit; unlit | amber; legend HOMING group | Lit with UHF panel in ADF mode; upper of the two |
| 9. FM homing light | lamp | lit; unlit | amber; legend HOMING group | Lit with VHF/FM panel in homing mode; lower |

### Target Identification Set Laser (TISL) control panel (p. 136)

Where: Bottom of the centre front dash, below the NMSP (item 6 on p. 135); named on p. 136 with no text description, so everything here is read from the figure on p. 135, labels low resolution.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| MODE select | rotary | OFF; CAGE; DIVE; LVL BAR; LVL WIDE | none | OFF at the top, then clockwise |
| SLANT RNG MILES switch | toggle | OVER 10; 10 / 5; UNDER 5 | none | 3 positions; to the right of MODE |
| ALT ABV TST window | display | two drum digits | legend FT X 1000 | Altitude above target readout; meaning inferred from legend |
| ENTER button | button | press | none | Label partly legible; first of four |
| + button | button | press | none | Second of four |
| BITE button | button | press | none | Third of four |
| Fourth button | button | press | none | No label visible |
| CODE SELECT | rotary | four digit wheels; digit range not stated | digits shown | Laser code; above the lower switch |
| TISL / BOTH / AUX switch | toggle | TISL; BOTH; AUX | none | Lower right of the panel; switch has no name |

## Right dash

### Fire Extinguisher Discharge (p. 144)

Where: Top of the right front dash, above the right MFCD (item 1 on p. 143).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| FIRE EXTING DISCH switch | toggle | left; centre; right | none | Spring return not stated |

### Right Multifunction Color Display (MFCD) (p. 144)

Where: Right front dash, centre, below the discharge switch (item 2 on p. 143). Same bezel as the left MFCD (p. 121).

### Fuel Quantity and Hydraulic Indicator Panel (p. 146)

Where: Lower right of the right front dash, right of the engine instruments (item 3 on p. 143).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 2. Fuel quantity gauge, left pointer | gauge | 0 to 6 thousand lb, legend FUEL LBS X1000 | none | Left fuel system; source set by selector |
| 2. Fuel quantity gauge, right pointer | gauge | 0 to 6 thousand lb, legend FUEL LBS X1000 | none | Right fuel system |
| 2. Total fuel readout | display | 5-digit counter, pounds | legend TOTAL LBS | Top of the dial; not affected by the selector |
| 3. Fuel display selector | rotary | INT (total internal per side); MAIN (main tank per side); WING (wing tank per side); EXT WING (left and right external tanks); EXT CTR (left pointer centreline external, right pointer 0) | none | Sets what the two pointers show |
| Test button | button | press and hold | none | Pointers go to 3, readout 6,000 while held |
| 4. Hydraulic pressure gauge, left (HYD SYS L) | gauge | dial marked x1000, psi; end of scale not legible | none | Top left; normal 2,800 to 3,350, max above 3,350 |
| 4. Hydraulic pressure gauge, right (HYD SYS R) | gauge | dial marked x1000, psi; end of scale not legible | none | Top right; text also says normal is above 1000 |

### RIGHT Engine "T Handle" Fire Extinguisher Discharge Select (p. 147)

Where: Below the HUD, right part of the front dash, top of the right dash (item 4 on p. 143).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Right engine T-handle | handle | not pulled; pulled | fire lamp in the handle | Pull selects right engine as extinguisher target |
| Right engine fire lamp | lamp | lit; unlit | lit on right engine fire; legend FIRE R ENG PULL | Discharge switch is on p. 144 |

### Marker and Canopy Lights (p. 148)

Where: Right dash, above the VVI (item 5 on p. 143).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| MARKER BEACON light | lamp | lit; unlit | legend MARKER BEACON, green in figure | Lit over a marker beacon in ILS mode |
| CANOPY UNLOCKED light | lamp | lit; unlit | legend CANOPY UNLOCKED, green in figure | Lit with canopy open |

### Vertical Velocity Indicator (VVI) (p. 148)

Where: Right dash, left column, below the marker lights, above the altimeter (item 6 on p. 143).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Climb rate pointer | gauge | 0 centred left; up and down to 6 (x1000 ft per min); labels .5, 1, 2, 4, 6 | legends CLIMB, UP, DOWN | Scale ticks every 100 ft; pointer rests at 0 in figure |

### Altimeter (p. 149)

Where: Right dash, left column, below the VVI, above the engine instruments (item 7 on p. 143).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Altitude pointer | gauge | numerals 0 to 9 around the dial; 100-foot scale | legend ALT | Text says 200-foot markers; tick value not stated |
| Altitude counter | display | 1,000 and 100 ft digits, last two always 00 | striped box on first digit in figure | Legends 1000 FT and 100 FT |
| Pressure setting window | display | 4 digits; units not stated | none | Lower right of the counter |
| 1. Pressure set knob | knob | turn clockwise or counter-clockwise | none | Lower left; sets the pressure window |
| 2. ELECT/PNEU switch | toggle | ELECT; PNEU (PNEU on top in figure) | none | Lower right; use PNEU after a CADC failure |

### Engine Monitoring Instruments (EMI) (p. 150)

Where: Lower right of the front dash, below the altimeter and right MFCD, left of the fuel panel (item 8 on p. 143); 12 gauges in two blocks, left engine in the left column of each block.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Left oil pressure | gauge | psi, labels 20 to 100; normal idle 55 to 85 | green, yellow, red arcs | Bottom row, left block; min 40, max 95 |
| 1. Right oil pressure | gauge | psi, labels 20 to 100; normal idle 55 to 85 | green, yellow, red arcs | Bottom row, left block; min 40, max 95 |
| 2. Left core speed | gauge | percent rpm, labels 10 to 100; normal 56 to 98 | green, yellow, red arcs; small inset pointer | Middle row, left block; do not exceed 102 |
| 2. Right core speed | gauge | percent rpm, labels 10 to 100; normal 56 to 98 | green, yellow, red arcs; small inset pointer | Middle row, left block; 100 to 102 max 3 s |
| 3. Left fan speed | gauge | percent rpm, labels 25 to 100 | green, yellow, red arcs | Top row, right block; about 82 at takeoff |
| 3. Right fan speed | gauge | percent rpm, labels 25 to 100 | green, yellow, red arcs | Top row, right block; about 82 at takeoff |
| 4. Left ITT | gauge | degrees C x100, labels 1 to 10; normal 275 to 865 | green arc, red mark; small inset pointer | Top row, left block; 900 briefly at start |
| 4. Right ITT | gauge | degrees C x100, labels 1 to 10; normal 275 to 865 | green arc, red mark; small inset pointer | Top row, left block; stable above 865 is a fault |
| 5. Left fuel flow | gauge | pounds per hour, labels 5 to 50; multiplier not legible | green arc, red mark | Middle row, right block; normal 1500 to 4100 |
| 5. Right fuel flow | gauge | pounds per hour, labels 5 to 50; multiplier not legible | green arc, red mark | Middle row, right block; normal 1500 to 4100 |
| 7. APU RPM | gauge | percent rpm, labels 20 to 120 | none | Bottom row, right block, left gauge; normal 100, max 110 |
| 6. APU EGT | gauge | degrees C x100, labels 1 to 10; normal 200 to 715 | green arc, yellow and red marks | Bottom row, right block, right gauge; 760 max for 2 s at start |

## Above the dash

### Heads Up Display Area Above Dash (p. 152)

Where: Above the front dash between the canopy bows; the UFC sits under the HUD; three T-handles run along the dash top (figure on p. 152).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 3. Heads-Up Display (HUD) | display | not stated | HUD symbology | Covered in other chapters |
| 4. Up-Front Controller (UFC) | button | not stated | not stated | Panel under the HUD; covered in another chunk |

Items 1, 2, 5 and 6 of the figure (standby compass, aerial refuelling lights, G-meter, AoA indexer) follow as their own sections.

### Standby Compass (p. 153)

Where: Hangs from the right canopy bow (item 1 on p. 152).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Compass card | gauge | heading numerals in a window beside a fixed index line | none | Liquid-filled magnetic type; tilts, loses accuracy in bank |

### Air Refuel Status Lights (p. 153)

Where: Right canopy bow area, below the standby compass (item 2 on p. 152).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| READY light | lamp | lit; unlit | legend READY, green in figure | On when the slipway door is open |
| LATCHED light | lamp | lit; unlit | legend LATCHED, green in figure | On when the nozzle is locked in; READY goes off |
| DISCONNECT light | lamp | lit; unlit | legend DISCONNECT, green in figure | On after the nozzle comes out; off when door closes |

### Accelerometer (G-meter) (p. 154)

Where: Left canopy bow (item 5 on p. 152).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| G pointer | gauge | labels -4, -2, 0, 2, 4, 6, 8, 10 | legend ACCELERATION LIMITS | Shows current load, positive or negative |
| PUSH TO SET button | button | press | none | Lower left of the dial; in figure only, function not stated |

### Angle of Attack Indexer (p. 155)

Where: Left front canopy rail, beneath the G-meter (item 6 on p. 152).

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Low-speed symbol | lamp | lit; unlit | V shape, top in figure | Colours per symbol not stated; text names green and yellow |
| On-speed symbol | lamp | lit; unlit | circle, middle in figure | With a chevron: slightly slow or fast |
| High-speed symbol | lamp | lit; unlit | inverted V, bottom in figure | Works only with nose gear down |
