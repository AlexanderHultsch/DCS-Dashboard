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
