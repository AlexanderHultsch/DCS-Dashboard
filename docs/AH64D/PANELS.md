# AH-64D – cockpit panels

Inventory of the cockpit controls, taken from the DCS AH-64D Flight Manual (see [RESEARCH.md](RESEARCH.md)). Page numbers are the manual's pages (printed page = PDF page). Written in our own words; no text or pictures are copied from the manual. DCS-BIOS identifiers are in [BIOS.md](BIOS.md).

Control types: `toggle` (2 or 3 positions), `spring` (spring-loaded, returns to a rest position), `button` (push button), `guarded` (has a cover), `rotary` (selector with fixed positions), `knob` (continuous), `rocker`, `hat` (multi-way switch), `lever`, `handle`, `lamp`, `display`, `gauge` (needle, drum or flag).

"N/I" means the manual marks the control as not implemented in DCS. Where the manual numbers the items of a figure, the rows use the same numbers; a number can appear on several rows when one item holds several switches or lamps.

## Pilot cockpit

The pilot sits in the rear seat. Panels that exist in both crew stations are described once here; the Where line gives the Copilot/Gunner (CP/G) page and any difference. The pilot instrument panel carries the Enhanced Upfront Display (EUFD) and the two Multi-Purpose Displays (MPD); those are described in the Displays area.

### Standby Magnetic Compass (p. 105)

Where: Pilot instrument panel, top (figure on p. 105). The CP/G instrument panel (p. 124) has no compass.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Standby magnetic compass | gauge | heading card; scale not stated | none | Heading backup when primary power or the navigation system fails; not precise in manoeuvres |

### Master Warning / Master Caution Lighted Pushbuttons (p. 106)

Where: Pilot instrument panel, top, next to the standby compass (figure on p. 106). The CP/G has the same pair on p. 124, acting on the CP/G station only; its text repeats the wrong MSTR WARN label on item 2.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. MSTR WARN Button | button | press | lit lamp in the button | Acknowledges the master warning: puts out the pilot lamp and stops the voice warning in both stations |
| 1. MSTR WARN light | lamp | flashing; unlit | warning lamp in the button | Flashes while a WARNING message is shown on the EUFD |
| 2. MSTR CAUT Button | button | press | lit lamp in the button | Acknowledges the master caution: puts out the pilot lamp and stops the caution tone in the pilot station. The manual's text labels this item MSTR WARN, a typo |
| 2. MSTR CAUT light | lamp | lit; unlit | caution lamp in the button | Lit while a CAUTION message is shown on the EUFD |

### Fire Detection / Extinguishing Panel (FIRE DET/EXTG) (p. 106)

Where: Pilot instrument panel, left side next to the left MPD (figure on p. 106). The CP/G has it on p. 124 and the manual says it works the same. The three fire buttons are common to both stations; the station that pressed a button is the only one that can disarm it.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. ENG 1 FIRE Button | guarded | cover closed; cover open and pressed (armed) | FIRE and RDY lights in the button | Arms the extinguisher for the left engine nacelle; also shuts engine 1 fuel flow and bleed air and acknowledges the master warning |
| 1. ENG 1 FIRE light | lamp | lit; unlit | yellow, legend FIRE | Lit while fire is detected in the left engine nacelle |
| 1. ENG 1 RDY light | lamp | lit; unlit | green, legend RDY | Lit once the button is pressed in either station |
| 2. APU FIRE Button | guarded | cover closed; cover open and pressed (armed) | FIRE and RDY lights in the button | Arms the extinguisher for the APU compartment; also shuts APU fuel flow and bleed air and acknowledges the master warning |
| 2. APU FIRE light | lamp | lit; unlit | yellow, legend FIRE | Lit while fire is detected in the APU compartment |
| 2. APU RDY light | lamp | lit; unlit | green, legend RDY | Lit once the button is pressed in either station |
| 3. ENG 2 FIRE Button | guarded | cover closed; cover open and pressed (armed) | FIRE and RDY lights in the button | Arms the extinguisher for the right engine nacelle; also shuts engine 2 fuel flow and bleed air and acknowledges the master warning |
| 3. ENG 2 FIRE light | lamp | lit; unlit | yellow, legend FIRE | Lit while fire is detected in the right engine nacelle |
| 3. ENG 2 RDY light | lamp | lit; unlit | green, legend RDY | Lit once the button is pressed; the manual's text names the ENG 1 button here, apparently a typo |
| 4. PRI Button | button | press | DISCH light in the button | Fires the primary bottle into the compartment selected with ENG 1, ENG 2 or APU |
| 4. PRI DISCH light | lamp | lit; unlit | legend DISCH | Lit while the primary bottle is armed; out after discharge or when the selection is cancelled |
| 5. TEST Switch | spring | TEST 1; centre; TEST 2 (order not stated) | none | Rest position centre. TEST 1 checks detection circuit 1; TEST 2 checks circuit 2 and also lights both DISCH lights. A good test lights all three FIRE lights and MSTR WARN in both stations, shows AFT DECK FIRE on the EUFD and plays the fire voice warnings in sequence |
| 6. RES Button | button | press | DISCH light in the button | Fires the reserve bottle into the compartment selected with ENG 1, ENG 2 or APU |
| 6. RES DISCH light | lamp | lit; unlit | legend DISCH | Lit while the reserve bottle is armed; out after discharge or when the selection is cancelled |

### Armament Panel (p. 108)

Where: Pilot instrument panel, lower left (figure on p. 108). The CP/G has it on p. 124, working the same. Both buttons are common to both stations: a press in one seat changes the state in the other.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. A/S Button | button | press toggles ARM and SAFE | ARM and SAFE lights | Works in the air, or on the ground only while Ground Override is on |
| 1. ARM light | lamp | lit; unlit | legend ARM | Weapons and the laser can fire |
| 1. SAFE light | lamp | lit; unlit | legend SAFE | Weapons and the laser are inhibited |
| 2. GND ORIDE Button | button | press toggles on and off | ON light | No effect in the air. On the ground, on allows ARM, actioning weapons, FCR transmission and arming chaff; switching it off sets A/S to SAFE, de-actions weapons, stops FCR transmission and sets chaff to SAFE |
| 2. ON light | lamp | lit; unlit | legend ON | Lit while Ground Override is on |

### Video Panel (p. 109)

Where: Pilot instrument panel, lower left, next to the Armament Panel (figure on p. 109). The CP/G instrument panel (p. 124) does not list a Video Panel.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. IHADSS BRT Knob (outer) | knob | continuous; range not stated | none | Brightness of the helmet display video; concentric with the contrast knob |
| 1. IHADSS CON Knob (inner) | knob | continuous; range not stated | none | Contrast of the helmet display video |
| 2. SYM BRT Knob | knob | continuous; range not stated | none | Brightness of the helmet symbology, separate from the video |
| 3. ACM Switch | toggle | on; off | none | N/I. On: FLIR level and gain automatic; off: the FLIR knobs are active |
| 4. FLIR LVL Knob (outer) | knob | continuous; range not stated | none | FLIR level for PNVS or TADS video; concentric with the gain knob |
| 4. FLIR GAIN Knob (inner) | knob | continuous; range not stated | none | FLIR gain for PNVS or TADS video |

### Canopy Jettison Handle (p. 109)

Where: Pilot instrument panel, left side (figure on p. 105). The CP/G has one on p. 124, and a third handle is outside for rescue crews. A stowage slot in each station holds the safety pin in flight.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Canopy Jettison Handle | handle | pin fitted (locked); pin removed, pull | none | N/I. Fires off the canopy side panels of both stations. Safety pin is stowed before flight |

### Master Zeroize Switch (p. 109)

Where: Pilot instrument panel, right side below the right MPD (figure on p. 105). The CP/G has it on p. 124, working the same.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Master Zeroize Switch | guarded | positions not stated | none | N/I. Erases all sensitive data on board |

### Standby Attitude Indicator (p. 110)

Where: Pilot instrument panel, right side (figure on p. 110). The CP/G instrument panel (p. 124) does not list one. Backup for the pilot when primary power or the flight reference system fails.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Bank Angle Scale | gauge | white index at 0 degrees; large ticks at 30, 60, 90; small ticks at 10, 20 | none | Read together with the bank angle indicator |
| 2. Bank Angle Indicator | gauge | pointer on the bank scale | none | Lines up with the fixed index in level flight |
| 3. Attitude Sphere | gauge | plus and minus 85 degrees pitch; 360 degrees roll | white half: nose above the horizon; black half: nose below | Moves against the aircraft symbol |
| 4. Aircraft Symbol (Waterline) | gauge | fixed symbol | none | Its height can be adjusted with the PULL TO CAGE knob |
| 5. Pitch Scale | gauge | large ticks every 10 degrees; small ticks every 5 degrees | none | Relative to the aircraft symbol |
| 6. Slip Indicator (Ball) | gauge | left of centre; centred between the two marks; right of centre | none | Ball left: apply left pedal; ball right: apply right pedal |
| 7. Rate-of-Turn Indicator | gauge | lower bar moves left or right; one bar width is 1 to 1.2 degrees per second | none | Bar under an outer upper bar: standard rate, 3 degrees per second; midway between two: half standard rate |
| 8. PULL TO CAGE Knob | knob | pull out: cage; pull out and turn fully clockwise: locked caged; turn: move the aircraft symbol up or down | none | Caging levels the sphere whatever the real attitude and shows the OFF flag |
| OFF warning flag | gauge | shown; hidden | yellow flag | Shown when caged or when power is lost |

### Standby Airspeed Indicator (p. 111)

Where: Pilot instrument panel, right side, below the attitude indicator (figure on p. 105 and p. 111). The CP/G instrument panel (p. 124) does not list one. Driven by the right pitot probe.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Airspeed Indicator | gauge | pointer on the outer scale | none | Shows indicated airspeed |
| 2. Indicated Airspeed Scale | gauge | 0 to 250 kt; ticks every 50 kt; dots every 10 kt from 20 kt | none | Outer scale of the instrument |

### Standby Altimeter (p. 111)

Where: Pilot instrument panel, right side, below the attitude indicator (figure on p. 105 and p. 111). The CP/G instrument panel (p. 124) does not list one. Driven by the static pressure system.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. 1000-foot Altitude Scale | gauge | large ticks every 100 ft; small ticks every 50 ft | none | Outer scale for one 1,000 ft revolution |
| 2. 1000-ft Scale Indicator | gauge | pointer on the outer scale | none | Altitude within the current 1,000 ft |
| 3. Altitude Indicator | gauge | 0 to 20,000 ft in 1,000 ft steps | none | Barometric altitude |
| 4. "Kollsman" Window | display | in/Hg; range not stated | pressure setting | Meant for QNH settings, so the altitude is above mean sea level |
| 5. Barometric Setting Knob | knob | continuous; range not stated | pressure in the window | Sets the pressure shown in the Kollsman window |

### Check Overspeed Test / Generator Reset Panel (p. 111)

Where: Pilot instrument panel, lower area (figure on p. 105 and p. 111). The CP/G instrument panel (p. 124) does not list one. Meant for resetting a generator when the MPDs do not work after a power failure.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. CKT A Switch | spring | ENG 1; OFF; ENG 2 | none | N/I for the ENG 1 and ENG 2 positions. Rest position OFF. Tests overspeed circuit A of each engine |
| 2. CKT B Switch | spring | ENG 1; OFF; ENG 2 | none | N/I for the ENG 1 and ENG 2 positions. Rest position OFF. Tests overspeed circuit B of each engine |
| 3. GEN RST Switch | toggle | GEN 1; GEN 2; centre and spring action not stated | none | Resets generator 1 or generator 2 |

### Windshield Wiper Control Panel (p. 112)

Where: Pilot instrument panel, lower area (figure on p. 112). The CP/G has the same panel on its right console (p. 127), working the same.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. DEFOG Button | button | press | none | N/I. Blows warm cockpit air against the canopy side panels |
| 2. WINDSHIELD WIPER Knob | rotary | PARK; OFF; LO; HI (order as listed in the manual) | none | PARK is held and springs back to OFF; the wiper then rests at its park position. OFF stops it where it is |

### Parking Brake Handle (p. 112)

Where: Pilot instrument panel, lower area (figure on p. 105). The CP/G instrument panel (p. 124) does not list one; either crew member can release the brake with the pedals.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| PARK BRAKE Handle | handle | pushed in (forward); pulled out and locked | none | Set by pressing the pedals in either seat and then pulling the handle out. Pushed in means the brakes are free; pulled out does not prove the brakes are on. Pedal pressure from either seat snaps it back in |

### Keyboard Unit (KU) (p. 113)

Where: Pilot station, in front of the left console (overview figure on p. 104). The CP/G has its own unit on p. 125 that the manual says works the same. Each unit is used on its own, and data is taken only while a data prompt is shown on the KU display. Entry overwrites the characters under the cursor.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Display Prompt | display | prompt text ending in a colon | prompt area on the KU display | Appears when an MPD button with a data entry symbol is pressed |
| 2. Scratchpad Display | display | up to 22 characters shown | scratchpad line | Scroll arrows move the cursor when the entry is longer; invalid entries flash |
| 3. Arithmetic Buttons | button | multiply; divide; add; subtract | none | Work only while no prompt is shown. Enter a number, an operator, a second number, then ENTER for the result |
| 4. CLR Button | button | press | none | Clears the scratchpad; does not cancel a prompt |
| 5. Scroll Arrows | button | left; right | none | Move the cursor along the entry |
| 6. ENTER Button | button | press | none | Accepts the entry into the MPD prompt |
| 7. Display Brightness Knob | knob | continuous; range not stated | none | Brightness of the KU scratchpad display |
| 8. BKS Button | button | press | none | Deletes the character left of the cursor and shifts the rest |
| 9. SPC Button | button | press | none | Inserts a blank at the cursor |
| Letter, number and N / E / S / W keys | button | key layout not described in the text | none | The manual only says the four compass keys are boxed, for entering latitude and longitude; it numbers them in no callout |

### Tail Wheel / NVS Mode Panel (p. 115)

Where: Pilot left console (overview figure on p. 115). The CP/G has the same panel on p. 125 and the manual says it works the same; the default NVS sensor is the PNVS in the pilot seat and the TADS in the CP/G seat, unless the NVS select switch on the collective grip has swapped them.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. TAIL WHEEL Button | button | press toggles locked and unlocked (commanded state) | UNLOCK light | Requests locking or unlocking of the tail wheel |
| UNLOCK light | lamp | lit; unlit | legend UNLOCK (unnumbered in the manual) | Lit whenever the wheel is actually unlocked, whatever the commanded state |
| 2. NVS MODE Switch | toggle | FIXED; NORM; OFF (order as listed in the manual) | none | FIXED: sensor on, pointed at the fixed forward position (0 degrees azimuth, -4.9 degrees elevation). NORM: sensor on, following the crew member's helmet sight line. In both, the PNVS is un-stowed, and a TADS sensor goes to FLIR with wide field of view whatever the TEDAC switches say. OFF: sensor off and stowed; the TADS parks at the fixed forward position |

### Emergency Panel (p. 116)

Where: Pilot left console (overview figure on p. 115). The CP/G has the same panel on p. 125 and the manual says it works the same. It gathers emergency actions that otherwise sit on MPD pages.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. GUARD Button | button | press toggles on and off | ON light | N/I. On: the UHF radio goes to 243.000 MHz, the old primary frequency moves to standby and the callsign shows GUARD. Pressing again swaps them back |
| 1. GUARD ON light | lamp | lit; unlit | legend ON | N/I with the button. Lit after the button was pressed in either seat |
| 2. XPNDR Button | button | press toggles on and off | ON light | N/I. On: transponder Mode 3/A code 7700 (in-flight emergency); a transponder in STBY goes to NORM and the EUFD shows 7700 EMER. Pressing again returns the transponder to NORM but the code stays and must be changed by hand |
| 2. XPNDR ON light | lamp | lit; unlit | legend ON | N/I with the button. Lit after the button was pressed in either seat |
| 3. ZEROIZE Switch | toggle | forward; other positions not stated | none | N/I. Forward erases communications encryption, modem settings and all TSD points in the navigation database |
| 4. EMERG HYD Button | button | press | ON light | N/I. Gives the utility hydraulic system a short burst of emergency pressure, enough for an immediate emergency landing |
| 4. EMERG HYD ON light | lamp | lit; unlit | legend ON | N/I with the button. Lit after the button was pressed in either seat |

### Power Quadrant Panel (p. 117)

Where: Pilot left console (overview figure on p. 115; panel pp. 117 to 118). Holds the rotor brake, battery, APU, engine start and engine power controls. The CP/G has only the ENG POWER levers (p. 126): they move together with the pilot levers through linkages, and the CP/G detent levers act through microswitches, so they need electrical power to get past the LOCK OUT or IDLE detents.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. RTR BRK Switch | toggle | OFF; BRK; LOCK (order as listed in the manual) | none | Commands the rotor brake on the main transmission accessory gearbox. OFF releases it. BRK: low pressure, slows the rotor sooner on shutdown in high wind or on a ship in rough sea. LOCK: high pressure, holds the rotor still, for starting in the same conditions. Inhibited electrically while either ENG POWER lever is past IDLE; in BRK or LOCK the levers cannot be moved past IDLE |
| 2. MSTR IGN Knob | rotary | OFF; BATT; EXT PWR (order as listed in the manual) | none | OFF: battery cut from the DC battery bus. BATT: battery on the bus, charging while the TRUs supply DC and taking over as emergency supply if they fail. EXT PWR: external AC and DC power can come in through the receptacle |
| 3. FRICT Lever | lever | range not stated | none | N/I. Sets how stiff the ENG POWER levers are to move |
| 4. APU Button | button | press | ON light | Starts the APU, and shuts it down, through the automatic sequences |
| 4. APU ON light | lamp | lit; unlit | legend ON | Lit once the APU has started and is running |
| 5. ENG START Switches | toggle | START; OFF; IGN ORIDE (order as listed; one switch per engine) | none | START is momentary: begins the automatic start (ignition enabled, fuel boost pump on, starter valve open) and the system processor closes the starter valve at 52 % NG. OFF is the normal position afterwards. IGN ORIDE opens the starter valve by hand and holds NG near 25 % until the switch goes back to OFF, with no boost pump and no ignition (motoring). A start can be aborted by going to IGN ORIDE and then OFF. The manual does not say whether IGN ORIDE is spring-loaded |
| 6. ENG POWER Levers | lever | LOCK OUT; FLY; IDLE; OFF (one lever per engine) | none | Set fuel flow and control mode via the power-available spindle. LOCK OUT: electronic control (DEC) cut out, throttle fully open, overspeed and TGT limiting disabled, so the pilot must manage the throttle by hand; for DEC failures only. FLY: DEC holds rotor speed at 101 % and shares load between the engines. IDLE: no rotor-speed regulation or load sharing; also resets the DEC out of LOCK OUT. OFF: fuel cut. A detent stops the lever going past FLY into LOCK OUT or below IDLE to OFF; a finger-lift lever on each lever releases it |

### Stores Jettison Panel (p. 119)

Where: Pilot left console (overview figure on p. 115). The CP/G has the same panel on p. 125 and the manual says it works the same. Only the seat that armed a station can disarm it; once any station is armed, either seat can press JETT.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. L OUTBD Button | button | press toggles armed and disarmed | ARM light | Selects the left outboard wing station for jettison |
| 1. L OUTBD ARM light | lamp | lit; unlit | legend ARM | Lit when the station will be jettisoned by JETT |
| 2. L INBD Button | button | press toggles armed and disarmed | ARM light | Selects the left inboard wing station for jettison |
| 2. L INBD ARM light | lamp | lit; unlit | legend ARM | Lit when the station will be jettisoned by JETT |
| 3. R INBD Button | button | press toggles armed and disarmed | ARM light | Selects the right inboard wing station for jettison |
| 3. R INBD ARM light | lamp | lit; unlit | legend ARM | Lit when the station will be jettisoned by JETT |
| 4. R OUTBD Button | button | press toggles armed and disarmed | ARM light | Selects the right outboard wing station for jettison |
| 4. R OUTBD ARM light | lamp | lit; unlit | legend ARM | Lit when the station will be jettisoned by JETT |
| 5. L TIP Button | button | press | none | No function. The figure labels it only "No function" |
| 6. JETT Button | button | press | none | Jettisons every station armed on this panel |
| 7. R TIP Button | button | press | none | No function. The figure labels it only "No function" |

### Exterior Lighting / Interior Lighting Panel (p. 119)

Where: Pilot left console (overview figure on p. 115; panel pp. 119 to 120). The CP/G has an Interior Lighting Panel on p. 126 with only the SIGNAL, PRIMARY, FLOOD and PRESS TO TEST controls, worded the same but numbered 1 to 4; it has no NAV, FORM, STBY INST or ANTI COLL controls. It is described in its own section in the Copilot/Gunner cockpit area. The manual's intro to that CP/G panel also says it controls exterior lighting, which does not fit its list of controls.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. NAV Switch | toggle | BRT; OFF; DIM (order as listed in the manual) | none | Brightness of the red and green navigation lights on the engine nacelles and the white one on the tail |
| 2. SIGNAL Knob | knob | continuous, with an RST (reset) detent; range not stated | none | Brightness of the cockpit signal lights at night level; no effect while the signal lights are in day level. RST puts them back to night level when the PRIMARY knob is not OFF and the FLOOD knob is below 50 % |
| 3. PRIMARY Knob | knob | continuous, with an OFF position; range not stated | none | Backlighting of the primary instruments. OFF returns the signal lights to day level |
| 4. FORM Knob | knob | continuous; range not stated | none | Brightness of the formation lights on the wing tips, tail boom and vertical stabiliser |
| 5. FLOOD Knob | knob | continuous; range not stated | none | Brightness of the interior flood lights. Turning it clockwise past 50 % returns the signal lights to day level |
| 6. STBY INST Knob | knob | continuous; range not stated | none | Brightness of the lighting for the standby instruments |
| 7. ANTI COLL Switch | toggle | WHT; OFF; RED (order as listed in the manual) | none | Mode of the anti-collision strobes on the engine nacelles: white or red alternating flash, or off |
| 8. PRESS TO TEST Button | button | press | all signal lights | Lights every signal light as a lamp check |

### Free Air Temperature Gauge (p. 120)

Where: Pilot left console, top (overview figure on p. 115). The CP/G pages (pp. 125 to 126) do not list one. The probe sticks out of the gauge through the fuselage into the outside air.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Temperature Indicator | gauge | pointer; reads in degrees Celsius | none | Outside air temperature as measured next to the pilot cockpit |
| 2. Temperature Scale | gauge | major ticks every 10 degrees; minor ticks every 2 degrees; end values not stated | none | Scale behind the pointer |

### Communications Panel (p. 121)

Where: Pilot right console (overview figure on p. 121; panel pp. 121 to 122). The CP/G has the same panel on its right console (p. 127) and the manual says it works the same. Sets the volume of the intercom, radios and other audio in the crew member's headset. Volume knobs turn clockwise for more; where a row says pull out, pulling the knob mutes that source.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. FM1 Knob | knob | rotate clockwise for more volume; pull out to mute | none | Volume of the FM1 radio |
| 2. FM2 Knob | knob | rotate clockwise for more volume; pull out to mute | none | Volume of the FM2 radio |
| 3. HF Knob | knob | rotate clockwise for more volume; pull out to mute | none | Volume of the HF radio |
| 4. VHF Knob | knob | rotate clockwise for more volume; pull out to mute | none | Volume of the VHF radio |
| 5. UHF Knob | knob | rotate clockwise for more volume; pull out to mute | none | Volume of the UHF radio |
| 6. SQL Switches | spring | forward; aft (momentary; rest position not stated) | none | Each press toggles squelch for the matching radio. The text does not say how many switches there are or which radio each one belongs to |
| 7. SENS Knob | knob | rotate clockwise for higher sensitivity; range not stated | none | Voice-activation sensitivity for the VOX position of the ICS switch; higher means a lower voice threshold |
| 8. MASTER Knob | knob | continuous; range not stated | none | Overall volume of everything in the helmet |
| 9. ICS Switch | toggle | PTT; VOX; HOT MIC (order as listed in the manual) | none | Microphone mode on the intercom. PTT: open only with the cyclic push-to-talk or the floor button. VOX: open above the SENS threshold, or with the push-to-talk. HOT MIC: always open |
| 10. IDENT Button | button | press | none | N/I. Momentary identification of own position for a non-Mode 4 transponder interrogation |
| 11. IFF Knob | knob | rotate clockwise for more volume; range not stated | none | N/I. Volume of the IFF interrogation audio |
| 12. RLWR Knob | knob | rotate clockwise for more volume; range not stated | none | Volume of the voice warnings from the APR-39/AVR-2 radar and laser warning receiver, and from the radar frequency interferometer when the mast-mounted FCR is fitted and the interferometer works |
| 13. ATA Knob | knob | not stated | none | No function. The figure labels it "No function"; the text names it ATA |
| 14. VCR Knob | knob | rotate clockwise for more volume; pull out to mute | none | N/I. Volume of the VCR audio during video playback |
| 15. ADF Knob | knob | rotate clockwise for more volume; pull out to mute | none | Volume of the audio from the ARN-149 automatic direction finder |

### CMWS Control Panel (p. 630)

Where: Pilot cockpit only (named in the overview figure on p. 104; described in the Aircraft Survivability Equipment chapter, figure and items 1 to 5 on p. 630, items 6 to 13 on p. 631). The CP/G station has no such panel, so only the pilot can arm the flare dispensers; either crew member can dispense flares with the cyclic FLARE button. The panel controls the AN/AAR-57 Common Missile Warning System. The manual's figure labels item 3 "No function" while its text calls it the AUDIO knob. Items 9 to 13 are the indicator display shown in a second figure.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Control Indicator Display | display | see items 9 to 13 | flare and chaff counts, threat direction arrows, status lamps | Shows the countermeasure stock, where a detected missile threat is, and the system status |
| 2. Power/Test Knob | rotary | OFF; ON; TEST (order as listed in the manual) | none | OFF: system unpowered. ON: system powered, and a built-in test runs by itself once it has initialised. TEST: starts a built-in test by hand. Whether TEST springs back is not stated |
| 3. AUDIO Knob | knob | not stated | none | No function |
| 4. LAMP Knob | knob | continuous; range not stated | none | Brightness of the Control Indicator Display |
| 5. ARM/SAFE Switch | toggle | SAFE; ARM (order as listed in the manual) | none | ARM allows automatic dispensing when a missile is detected and manual dispensing from either seat. SAFE inhibits flare dispensing. With weight on wheels dispensing is inhibited in either position |
| 6. CMWS/NAV Switch | toggle | CMWS; NAV (order as listed in the manual) | none | Chooses what the ADF audio channel carries in both seats. CMWS: the missile alert audio, and the ADF radio cannot be heard. NAV: the ADF receiver audio, and the missile alert audio cannot be heard. The ADF volume knob on the Communications Panel sets the level of either |
| 7. JETTISON Switch | guarded | positions not stated | none | Dumps every flare from the tail dispensers in an emergency. Works without the system being armed |
| 8. BYPASS/AUTO Switch | toggle | BYPASS; AUTO (order as listed in the manual) | none | BYPASS: the system's automatic dispensing is ignored, flare programs run only when the FLARE button on either cyclic is pressed. AUTO: programs can also start by themselves on a detected missile. The alert audio is given in both positions |
| 9. Flare Inventory | display | count up to 60 | flare count digits | Cartridges left. When none are left the display alternates between 0 and OUT |
| 10. Chaff Inventory | display | count up to 30 | chaff count digits | Cartridges left. When none are left the display alternates between 0 and OUT; the manual's text says "flare inventory" here, apparently a typo |
| 11. Quadrant Arrows | lamp | lit; unlit | direction arrows | Lit arrows show the direction of a detected missile threat |
| 12. Dispense Indicator | lamp | lit; unlit | dispense lamp | Lit while a flare or chaff dispensing is under way |
| 13. Ready Indicator | lamp | lit; unlit | ready lamp | Lit when flares can be dispensed: ARM/SAFE switch on ARM and the aircraft not on its wheels |

### Items named only in the pilot overview figure (pp. 104 and 394)

Where: Pilot cockpit overview figure on p. 104. The manual gives these three items no panel description in the cockpit chapter; the rows hold what other chapters say about them. The same figure also labels an M4 rifle and the HDU storage holster on the right console (see the Console fittings entry in the Copilot/Gunner area), which are stowage only.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Boresight Reticle Unit (BRU) | display | bullseye pattern shown while the helmet boresight is active | bullseye | Sits on top of the instrument panel (p. 394). It is switched on by choosing IHADSS on the BORESIGHT sub-page of the WPN page. Its brightness follows the PRIMARY lighting knob on the lighting panel of the same station. The crew member lines the helmet line-of-sight reticle up with the bullseye |
| Data Transfer Unit (DTU) receptacle | not stated | holds up to four data cartridges | card names on the DMS DTU sub-page | Pilot crewstation only, named as "DTU" in the figure. Loads mission data from, and saves data to, removable Data Transfer Cartridges; the DMS page DTU sub-page shows which cartridges are available |
| Anti-Torque Pedals | not stated | not described | none | Named in the figure. Pressing a pedal downwards brakes the matching main wheel, in either seat; see also the Parking Brake Handle entry |

## Copilot/Gunner cockpit

The Copilot/Gunner (CP/G) sits in the front seat. Panels that exist in both crew stations are described once in the Pilot cockpit area; the Where line of each of them gives the CP/G page and any difference. This area holds only what exists in the CP/G station alone: a lighting panel with its own numbering, the Processor Select Panel, some console fittings the manual only names in a figure, and the TADS Electronic Display And Control (TEDAC) with its display unit and two fixed handgrips. The CP/G Enhanced Upfront Display and Multi-Purpose Displays (p. 124) are in the Displays area, and the CP/G cyclic and collective grips are in the area "Hand controls (cyclic and collective grips)".

### Interior Lighting Panel (p. 126)

Where: CP/G left console (overview figure on p. 125; panel on p. 126). A smaller version of the pilot's Exterior Lighting / Interior Lighting Panel: the same four controls with the same effects, but numbered 1 to 4 here, and without the NAV, FORM, STBY INST and ANTI COLL controls. The manual's intro to this panel also says it controls exterior lighting, which none of its listed controls do.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. SIGNAL Knob | knob | continuous, with an RST (reset) detent; range not stated | none | Brightness of the cockpit signal lights at night level; no effect while they are at day level. RST brings night level back when PRIMARY is not OFF and FLOOD is below 50 % |
| 2. PRIMARY Knob | knob | continuous, with an OFF position; range not stated | none | Backlighting of the primary instruments. Turning it to OFF puts the signal lights back to day level |
| 3. FLOOD Knob | knob | continuous; range not stated | none | Brightness of the interior flood lights. Turning it clockwise past 50 % puts the signal lights back to day level |
| 4. PRESS TO TEST Button | button | press | all signal lights | Lights every signal light as a lamp check |

### Processor Select Panel (p. 127)

Where: CP/G right console (overview figure on p. 127), listed beside the Communications Panel. Not on the pilot consoles. The whole panel is N/I. It decides which of the two system processors (SP) is in charge of the aircraft functions.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. SP1 light | lamp | lit; unlit | legend SP1 | N/I. Shows that system processor 1 is the primary one. The manual names one pair of lights, "SP1/SP2 Lights" |
| 1. SP2 light | lamp | lit; unlit | legend SP2 | N/I. Shows that system processor 2 is the primary one |
| 2. PROCESSOR SELECT Switch | toggle | SP1; AUTO; SP2 (order as listed in the manual) | none | N/I. SP1 or SP2 forces that processor to be primary. AUTO lets the aircraft functions switch to the other processor when the primary one fails. The text does not describe the switch shape or any spring action |

### Console fittings named only in the overview figures (pp. 125 and 127)

Where: CP/G left console (figure on p. 125) and CP/G right console (figure on p. 127). The manual puts these labels in the figures without any description or control list, so only the names are recorded.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| Utility Light | lamp | not described | not described | Left console, CP/G only in the figures. The manual's lighting overview says each crew member has a dimmable utility light that can be aimed around the cockpit like a flashlight; no control is shown for it |
| Canopy Jettison Handle Pin | not stated | not described | none | Left console. Label only; see the Canopy Jettison Handle entry in the pilot area |
| First Aid Kit | not stated | not described | none | Left console. Label only |
| HDU Storage Holster | not stated | not described | none | Right console. Label only; the pilot right console figure shows one too |

### TEDAC Display Unit (TDU) (p. 129)

Where: CP/G station only. The TEDAC (overview figures on pp. 123 and 128; bezel controls on pp. 129 to 130) replaces the older optical relay tube and shows the high-resolution video of the modernised TADS. The TDU has no Variable Action Buttons, so FCR page options on it are reachable only with the MPD cursor. When the CP/G NVS Mode switch is NORM or FIXED, the TDU repeats the CP/G helmet display unit (HDU: flight symbology plus NVS sensor video) and the four top buttons (TAD, FCR, PNV, G/S) are inhibited. Callouts 1 to 18 follow the manual's figure.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| TDU screen | display | grayscale with the Display Knob at DAY; greenscale at NT | TADS or PNVS sensor video, symbology, or the FCR page | Unnumbered. Shows the picture chosen with the four top buttons |
| 1. TAD Button | button | press | none | Shows weapon symbology of the HMD when the CP/G sight is HMD; shows TADS weapon symbology with TADS video when the sight is TADS |
| 2. FCR Button | button | press | none | Shows the FCR page. Its functions, except opening the UTIL sub-page, work on the TDU but only with the MPD cursor. The cursor gets there only by the bump method: push it to the inboard edge of either MPD, release, then push inboard again; this works only while the FCR page is up |
| 3. PNV Button | button | press | none | Shows the pilot's HMD flight symbology and NVS video on the TDU. With the CP/G sight on TADS or FCR, the CP/G HDU shows the same pilot picture |
| 4. G/S Button | button | press | none | Shows a grayscale test pattern for setting TDU brightness and contrast |
| 5. TDU Display Knob | rotary | DAY; NT; OFF (order as listed in the manual) | none | DAY: screen on, day brightness scale. NT: screen on, night brightness scale. OFF: only the screen goes dark; every TEDAC function and bezel button keeps working |
| 6. FLIR LEV Knob | knob | continuous; range not stated | none | Relative brightness of the thermal picture from the PNVS or TADS FLIR |
| 7. FLIR GAIN Knob | knob | continuous; range not stated | none | Relative gain of the thermal picture from the PNVS or TADS FLIR |
| 8. SYM Rocker Switch | rocker | two directions; which one raises is not stated | none | Symbology brightness: of the CP/G HDU when the sight is HMD, of the TDU when the sight is TADS or FCR. A short press steps, a held press changes continuously |
| 9. BRT Rocker Switch | rocker | two directions; which one raises is not stated | none | Overall brightness: of the CP/G HDU when the sight is HMD, of the TDU when the sight is TADS or FCR. A short press steps, a held press changes continuously |
| 10. CON Rocker Switch | rocker | two directions; which one raises is not stated | none | Contrast: of the CP/G HDU when the sight is HMD, of the TDU when the sight is TADS or FCR. A short press steps, a held press changes continuously |
| 11. Asterisk Button | button | press | none | Puts brightness and contrast back to their defaults, on the CP/G HDU with the HMD sight or on the TDU with the TADS or FCR sight |
| 12. R/F Rocker Switch | rocker | up: longer focus range; down: shorter focus range | none | Range focus of the selected TADS sensor. A short press steps, a held press changes continuously |
| 13. EL Rocker Switch | rocker | not stated | none | N/I |
| 14. AZ Rocker Switch | rocker | not stated | none | N/I |
| 15. AZ/EL Button | button | press | none | N/I |
| 16. ACM Button | button | press | none | N/I |
| 17. FREEZE Button | button | press | none | Holds the current frame on the TDU only; the video keeps updating on the other displays in both stations |
| 18. FILTER Button | button | press | none | N/I |

### TEDAC Left Handgrip (LHG) (p. 131)

Where: CP/G station, the fixed handgrip on the left of the TEDAC (overview figure on p. 128; controls on pp. 131 to 133). The grips repeat many cyclic and collective functions so the CP/G can work without touching the pilot's flight controls. Items 10, 13 and 14 sit on the opposite side of the grip from the others. Weapons actioned with the LHG Weapon Action Switch can be fired only with the LHG Weapon Trigger. Weapons cannot be actioned while the aircraft is on the ground unless GND ORIDE is on at the Armament Panel.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Image Auto Track/Offset Switch | spring | IAT (forward); OFS (aft); rest position not stated | none | IAT: starts an auto-track on the target under the TADS line-of-sight reticle as the primary track; if the reticle is already inside the primary track gates, it moves the track aim point to the reticle centre. OFS short press (under 0.5 s): with the reticle outside the gates, sends it back to the primary track; inside the gates, drops the primary track. OFS long press (over 0.5 s): drops the primary and all secondary tracks wherever the reticle is |
| 2. TADS Field-Of-View Switch | hat | W (wide, right); M (medium, aft); N (narrow, left); Z (zoom, forward) | none | Magnification of the TADS FLIR and DTV cameras. Z is a 2:1 electronic magnification. For the DTV, M gives its wide field of view. A TADS sensor used as NVS sensor is forced to FLIR with wide field of view |
| 3. Video Record Button | button | press | none | N/I |
| 4. TADS Sensor Select Switch | toggle | FLIR (forward); TV (centre); DVO (aft) | none | FLIR: thermal camera video. TV: DTV camera video. DVO: no function. Forced to FLIR while the CP/G NVS Mode switch is NORM or FIXED |
| 5. Weapon Action Switch (WAS) | hat | GUN (forward); RKT (left); MSL (right); ATA (aft) | none | Selects a weapon; selecting it again de-selects it. GUN: area weapon system, gun slaved to the sight's solution. RKT: rockets, pylon articulation, rocket steering cursor; if the CP/G actions rockets here and the pilot does too, the crew is in COOP rocket mode; if the CP/G used the cyclic switch instead, the rockets go to whoever actioned last. MSL: Hellfire missiles, pylon articulation, missile launch symbology. ATA: no function. Neither seat has priority: the last actioning wins |
| 6. Store/Update Switch | spring | STORE (forward); UPDT (aft) | none | STORE, momentary: with the TADS sight stores a target point along the line of sight at the current range; with the FCR sight stores a target point at the next-to-shoot target; with the TSD Point sub-page open it stores a waypoint or target point, with HMD or TADS. UPDT (navigation position update): N/I |
| 7. FCR Mode Switch | hat | GTM (forward); RMAP (right); ATM (aft); TPM (left) | none | Works with the FCR as sight while it is not scanning. GTM: ground targeting. RMAP: radar map; selecting it again toggles the terrain video underlay on the FCR page. ATM: air targeting. TPM: terrain profile, for low-level flight in poor visibility |
| 8. Cursor Controller/Enter (CURSOR) | hat | pushed in any direction to move the cursor; pressed in to select | none | Moves the MPD cursor so bezel options or points on a display can be picked without the bezel buttons. Pressing it selects the item under the cursor |
| 9. Cursor Display Select (L/R) Button | button | press | none | Jumps the MPD cursor to the centre of the other MPD |
| 10. Weapon Trigger | button | first detent; second detent | none | Fires the actioned weapon when the A/S button on the Armament Panel is ARM. First detent: fires if no performance or safety inhibit exists. Second detent: fires if no safety inhibit exists. On the opposite side of the grip |
| 11. FCR Scan Switch | spring | S-SCAN (forward); C-SCAN (aft) | none | With the FCR sight, a momentary press starts a scanburst; during any running scanburst a momentary press to either side ends it. S-SCAN: one burst of several scans, their number set by the scan size. C-SCAN: continuous scanning until ended or another sight is chosen. The FCR cannot transmit on the ground unless GND ORIDE is on |
| 12. Cued Search (CUED) Button | button | press | none | N/I |
| 13. Linear Motion Compensation (LMC) Button | button | press | none | Toggles LMC of the TADS. On the opposite side of the grip |
| 14. Cage Button | button | press | none | No function. The figure labels it "No function"; the text names it Cage Button. On the opposite side of the grip |

### TEDAC Right Handgrip (RHG) (p. 134)

Where: CP/G station, the fixed handgrip on the right of the TEDAC (overview figure on p. 128; controls on pp. 134 to 135). Items 10, 13 and 14 sit on the opposite side of the grip from the others.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. FCR Scan Size Switch | hat | W (wide, right); M (medium, aft); N (narrow, left); Z (zoom, forward) | none | Sets the FCR scan width in azimuth while the FCR sight is not scanning. In GTM or RMAP: W 90, M 45, N 30, Z 15 degrees. In ATM: W 360, M 180, N 90, Z 45 degrees |
| 2. C-SCOPE Button | button | press | none | Turns the FCR C-Scope symbol overlays in the CP/G station on and off |
| 3. FLIR Polarity Button | button | press | none | Switches the FLIR picture between white-hot and black-hot |
| 4. Laser Tracker (LT) Switch | toggle | A (automatic, forward); O (off, centre); M (manual, aft) | none | Laser spot tracker of the TADS. A and M enable it and stop the LRFD from firing; O disables it and lets the LRFD fire. Nothing in the cockpit shows manual mode, so check the switch itself |
| 5. Sight Select Switch | hat | HMD (forward); FCR (left); TADS (right); LINK (aft) | none | Chooses the CP/G sight. HMD: helmet sight; the CP/G HDU shows HMD flight symbology. FCR: radar sight; opens the FCR page on the left MPD if not shown; the last seat to select the FCR keeps it. TADS: blocked while either crew member uses the TADS as NVS sensor. LINK: with the FCR sight, slaves the TADS to the next-to-shoot target; with the TADS sight, slaves the FCR centreline to the TADS azimuth |
| 6. Image Auto Track Polarity Switch | toggle | not stated | none | N/I |
| 7. Sight Slave Button | button | press | none | Slaves and de-slaves the CP/G sight to the selected acquisition source |
| 8. Sight Manual Tracker | hat | directions not described | none | Also called the thumb force controller. Moves the TADS or FCR sight by hand while it is de-slaved |
| 9. Display Zoom Button | button | press | none | Turns the FCR ZOOM format on and off, with the FCR as sight |
| 10. LRFD Trigger | button | first detent; second detent | none | Fires the laser rangefinder/designator when the A/S button is ARM and the LRFD is powered (VAB L6, WPN Utility sub-page). First detent: one short ranging pulse; release before the next. Second detent: continuous designation pulse while held. On the opposite side of the grip |
| 11. MTT Track Promote Switch | toggle | - (forward); + (aft); spring action not stated | none | For the multi-target track mode of image auto-track. -: makes the previous secondary track the primary one. +: makes the next one primary. The TADS reticle moves to the new primary track's aim point |
| 12. Cursor Enter Button | button | press | none | Selects the item under the cursor; an alternative to pressing the cursor controller |
| 13. Heads-Down Display (HDD) Button | button | press | none | No function. The figure labels it "No function"; the text names it HDD Button. On the opposite side of the grip |
| 14. Missile Advance Button | button | press | none | Steps to the next Hellfire missile; works only when the missile mode on the WPN page MSL format is MAN. On the opposite side of the grip |

## Hand controls (cyclic and collective grips)

Source: the manual's "Cyclic & Collective Hand Controls" section (pp. 136 to 141). The grips let either crew member work sensors, weapons, radios and defensive systems without taking a hand off the flight controls. The manual says the pilot and CP/G grips are identical in form and function, with two exceptions that are noted in the rows: the BUCS trigger on the Collective Flight Grip does nothing in the pilot seat, and the pilot cannot pick the TADS with the Sight Select switch on the Collective Mission Grip. The TEDAC handgrips are not here; they are in the Copilot/Gunner area. Numbers follow the manual's figures. Switch positions are given as the manual names them, with the physical direction in brackets where it states one.

### Cyclic Grip (p. 136)

Where: Pilot and CP/G cyclic; the manual describes them as identical, so both stations have the full set with the same numbering (pp. 136 to 138). The CP/G additionally has the TEDAC handgrips, which repeat several of these functions.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Force Trim/Hold Mode Switch | hat | R (release, forward); AT (attitude hold, left); AL (altitude hold, right); D (disengage, aft) | none | Runs the force trim and hold modes of the flight management computer. R must be held: while it is held forward the magnetic brakes on cyclic and pedals are free and Heading Hold and Attitude Hold drop out; on letting go the brakes grab again, a new trim reference is taken from the current cyclic and pedal positions and any hold mode whose conditions are met comes back. AT toggles Attitude Hold. AL toggles Altitude Hold. D switches off both Attitude Hold and Altitude Hold |
| 2. Weapon Action Switch (WAS) | hat | G (gun, forward); R (rocket, left); M (missile, right); A (air-to-air, aft) | none | Selects a weapon for use; selecting the same one again de-selects it. G: area weapon system, gun slaved to the solution of the station's sight. R: rocket sub-system, pylon articulation, rocket steering cursor. M: Hellfire missile system, pylon articulation, missile launch symbology. A: no function. If the CP/G actions with this cyclic switch, only the trigger on this cyclic fires for the CP/G. Neither seat has priority: the last actioning wins. For rockets, a CP/G action made on the TEDAC left handgrip together with a pilot action puts the crew in cooperative rocket mode; made on the cyclic, the rockets go to whoever actioned last |
| 3. Symbology Select Switch | hat | CT (cruise/transition, forward); HB (hover/bob-up, aft); depress (FLT page) | none | Picks the helmet display symbology mode for both crew members at once. CT: Transition mode; each further press alternates Cruise and Transition. HB: Hover mode; each further press alternates Bob-Up and Hover, and every entry into Bob-Up drops a new Bob-Up box and takes the current heading as the command heading. Depress: shows the FLT page on this station's left MPD (no effect if it is already there; if it is on the right MPD the two pages swap). If no button is pressed on the FLT page for 10 minutes the depress returns the left MPD to its previous page; after that the return no longer works |
| 4. PTT/RTS Switch | hat | RADIO (left); ICS (right); RTS (depress) | none | RADIO: transmits on the radio marked by the RTS indicator on the EUFD. ICS: transmits on the intercom to the other seat and to the ground crew. RTS: steps the RTS indicator to the next radio; after the HF radio at the bottom of the list it wraps to the VHF radio at the top |
| 5. Chaff Dispense (C) Button | button | press | none | Dispenses one chaff program when the chaff mode is PROGRAM, or one cartridge when it is MANUAL |
| 6. Flare Dispense (FLARE) Button | button | press | none | Dispenses one flare program |
| 7. Weapon Trigger | guarded | first detent; second detent | none | Fires the weapon actioned in this station. First detent: fires if no performance and no safety inhibit applies. Second detent: fires if no safety inhibit applies |
| 8. Cage Button | button | press | none | No function. The figure labels it "No function"; the text names it Cage Button |
| 9. FMC Release Button | button | press | none | Switches off the pitch, roll, yaw and collective channels of the flight management computer. They can be switched on again from the Utility page |

### Collective Flight Grip (p. 138)

Where: Pilot and CP/G collective, same controls in both stations (pp. 138 to 139), with one exception: the BUCS trigger (item 9) is named "CPG only" and does nothing in the pilot seat.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Emergency Jettison (JETT) Button | guarded | press | none | Jettisons all weapon stations from the wing pylons |
| 2. Boresight/Polarity Switch | toggle | B/S; PLRT (order not stated) | none | Polarity of the FLIR picture from the NVS sensor of this station. B/S: no function. PLRT: toggles the FLIR picture between white-hot and black-hot |
| 3. Searchlight Switch | toggle | ON (forward); OFF (centre); STOW (aft) | none | Controls the fuselage search/landing light. ON: light on. OFF: light off. STOW: commands the light to retract; the switch springs from STOW back to OFF |
| 4. Searchlight Position Switch | hat | EXT (extend, forward); L (left); R (right); RET (retract, aft) | none | Aims the light. EXT: tilts the bulb forward and up. L: turns it left, counter-clockwise. R: turns it right, clockwise. RET: tilts it down and back. Position control is blocked for 1 minute after STOW |
| 5. NVS Select Switch | toggle | TADS (forward); PNVS (aft) | none | Chooses the night vision sensor of this station; the field-of-regard box in the helmet symbology changes to the slew limits of the chosen sensor. Neither seat has priority: either switch can give either sensor to either seat |
| 6. Stabilator Control Switch | hat | ND (nose-down, forward); NU (nose-up, aft); RESET (depress) | none | Moves the horizontal stabilator by hand. ND: trailing edge down, nose pitches down. NU: trailing edge up, nose pitches up. Either direction changes an automatic stabilator to manual mode. RESET: back to automatic mode |
| 7. Engine Chop (CHOP) Button | guarded | press toggles on and off | none | N/I. Engages the engine chop circuit, which takes engine power to idle; a second press clears it and restores normal power |
| 8. Tail Wheel Lock/Unlock Button | button | press | none | Toggles the commanded state of the tail wheel lock between locked and unlocked |
| 9. BUCS Trigger (CPG only) | button | press | none | N/I. Lets the CP/G take over the pilot's flight controls when the back-up control system is on. Does nothing in the pilot seat |

### Collective Mission Grip (p. 140)

Where: Pilot and CP/G collective, same controls and numbering in both stations (pp. 140 to 141), with one exception: the TADS position of the Sight Select Switch (item 4) does nothing in the pilot seat. The manual's figure labels item 9 the Alternate Cursor Enter Trigger.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. FCR Mode Switch | hat | GTM (forward); RMAP (right); ATM (aft); TPM (left) | none | Chooses the radar mode while the FCR is the station's sight and is not scanning. GTM: ground targeting, finds and classifies ground vehicles and low flyers. RMAP: radar map; picking it again toggles the terrain video underlay on the FCR page. ATM: air targeting, for helicopters and fixed-wing aircraft. TPM: terrain profile, for low flying in poor visibility |
| 2. FCR Scan Size Switch | hat | W (wide, right); M (medium, aft); N (narrow, left); Z (zoom, forward) | none | Sets the azimuth scan width while the FCR is the sight and not scanning. In GTM or RMAP: W 90, M 45, N 30, Z 15 degrees. In ATM: W 360, M 180, N 90, Z 45 degrees |
| 3. Cursor Controller/Enter (CURSOR) | hat | pushed in any direction to move the cursor; pressed in to select | none | Moves the MPD cursor so bezel options or display points can be picked without the bezel buttons. Pressing it selects the highlighted item |
| 4. Sight Select Switch | hat | HMD (forward); FCR (left); TADS (right); LINK (aft) | none | Chooses the sight of this station. HMD: helmet sight, helmet display shows HMD flight symbology. FCR: radar sight; opens the FCR page on the left MPD if it is not shown; the last seat to choose the FCR holds it. For a CP/G whose NVS Mode switch is OFF, the helmet display then shows TADS weapon symbology and video, unless the pilot uses the TADS as NVS sensor, in which case it shows HMD flight symbology. TADS: CP/G only, blocked while either crew member uses the TADS as NVS sensor; does nothing for the pilot. LINK: with the FCR as sight, slaves the TADS to the next-to-shoot target; with the CP/G TADS as sight, slaves the FCR centreline to the TADS azimuth |
| 5. Cursor Display Select Button | button | press | none | Jumps the MPD cursor to the centre of the other MPD |
| 6. FCR Scan Switch | spring | S-SCAN (forward); C-SCAN (aft); rest position not stated | none | With the FCR as sight, a momentary push to either side starts a scanburst; during a running single or continuous scanburst a momentary push to either side ends it. S-SCAN: one burst of several scans, the number depends on the scan size. C-SCAN: scans continuously until ended or another sight is chosen. The FCR cannot transmit with weight on wheels unless GND ORIDE is on at the Armament Panel |
| 7. Cued Search (CUED) Button | button | press | none | N/I |
| 8. Missile Advance Button | button | press | none | Steps to the next Hellfire missile; works only when the missile mode on the WPN page MSL format is MAN |
| 9. Alternate Cursor Enter Trigger | button | press | none | Selects the highlighted item under the cursor, as an alternative to pressing in the cursor controller |

## Displays (EUFD, MPD)

This area covers the display units and the controls on their bezels: the Enhanced Up-Front Display (EUFD) and the Multi-Purpose Displays (MPD). The TADS Electronic Display And Control (TEDAC) display unit is already described in the Copilot/Gunner area. What the MPD pages show (ENG, FLT, FUEL, PERF, UTIL, TSD, VID, DMS and the others) is display content, not controls, and is not described here; the same goes for the individual warning, caution and advisory texts on pp. 158 to 163, of which only the three message areas are listed. Controls come first in each table, display rows after them.

### Enhanced Up-Front Display (EUFD) (p. 155)

Where: Pilot instrument panel (figure on p. 105), and the same unit in the CP/G station (p. 124); each crew member has their own. Unlike the MPDs, the EUFD keeps working on battery power. It is an LED display with controls on either side of it, and it is divided into three areas: warnings/cautions/advisories, radio status and information. The stopwatch of one station does not affect the other. Pages 158 to 163 list the warning, caution and advisory texts with their conditions; those are display content and are not recorded here.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Warning/Caution/Advisory (WCA) Scroll Rocker | rocker | up; down | none | Scrolls the message columns, needed when any column holds 8 or more messages (a double arrowhead symbol on the display says so). While the preset list is shown it scrolls the preset list instead |
| 5. Brightness Control Knob | knob | continuous; range not stated | none | Brightness of the EUFD |
| 6. Preset Button | button | press toggles | preset list at the right side of the display | Shows or hides the list of presets for the selected radio. Used together with the RTS rocker, the WCA rocker and the Enter button |
| 7. Enter Button | button | press | none | Puts the preset chosen in the list into the primary slot of the selected radio and tunes it. Only single-channel frequencies can be tuned this way, not frequency-hopping nets |
| 8. Datalink (DL) Transmit Select Rocker | rocker | direction names not stated | datalink transmit select indicators | Chooses the radio used for datalink transmission |
| 9. Radio Transmit Select (RTS) Rocker | rocker | up; down | RTS indicator | Moves the RTS indicator to the previous or next radio. Pressing down at the bottom of the list (HF) wraps to the top (VHF); pressing up at the top wraps to the bottom |
| 12. Stopwatch Button | button | press; hold 2 seconds | stopwatch above the time | Press: starts and stops the stopwatch; a square symbol beside it marks it as paused. Hold for 2 seconds: resets it and removes it from the display |
| 13. Swap Button | button | press | none | Exchanges frequency, encryption mode and network settings of the selected radio with its standby values |
| 2. Warning Message Area | display | left column; 8 or more messages need scrolling | warnings | Emergencies that could kill the crew or lose the aircraft (examples: engine fire, engine flameout, total hydraulic loss). Comes with the flashing MSTR WARN lamp and a voice message |
| 3. Caution Message Area | display | centre column; 8 or more messages need scrolling | cautions | Less critical but hazardous faults (examples: low oil or transmission pressure, overtemperature, electrical failures, low fuel). Comes with the MSTR CAUT lamp and a tone |
| 4. Advisory Message Area | display | right column; 8 or more messages need scrolling | advisories | Non-critical states and received datalink traffic (examples: tail wheel lock state with weight on wheels, automatic fuel check done, unlatched canopy door). Some come with their own tones |
| 10. Information Display Area | display | one line | fuel, transponder, time | Fields in order: total fuel in lb; transponder Mode S enabled status; Mode 3/A code; Mode 4 code (A or B); transponder status (STBY, NORM or EMER); time, local or Zulu. The Mode S, 3/A and 4 fields are blank when that mode is off. A running stopwatch is shown above the clock time |
| 11. Radio Status Area | display | 6 rows in the centre, five radios | radio status | Per radio: primary frequency, primary callsign (5 characters; MAN for a hand-tuned frequency; GUARD for a guard frequency), primary datalink network, standby frequency, standby callsign, radio monitor dots (left column: monitored in this station, right column: in the other station; a dot goes blank when the matching volume knob on the Communications Panel is pulled out), squelch asterisk. The VHF radio is at the top of the list and HF at the bottom; the order between them is not stated |
| 11. Radio Status Area - sixth line | display | extra line for the HF radio | HF transmit data | N/I. When the RTS indicator of this station is on the HF radio, the sixth line shows more about HF transmission |
| 11. Radio Status Area - GUARD receiver, power and standby network fields | display | not stated | G; power settings; standby network | G: the separate guard receiver of the ARC-164 radio monitors 243.0 MHz. Also shown: the HF power setting (ARC-220), the IFM amplifier power setting of the FM1 radio (ARC-201D) and the standby datalink network |
| 11. Radio Status Area - transmit select indicators | display | four states for voice, three for data | RTS and datalink icons | The icons show which station's transmissions are routed to a radio: this station, the other station, both, or (voice only) neither. The manual's figure carries the symbols; the text does not describe their shape |

### Multi-Purpose Displays (MPD) (p. 164)

Where: Pilot instrument panel, one left and one right MPD (figure on p. 105; bezel figure on p. 164). The CP/G has two identical MPDs on its instrument panel (p. 124). The two MPDs of a station are identical and each crew member uses theirs independently. The screens are colour LCDs, 6 by 6 inches. With external power, weight on wheels and both power levers OFF, the MPDs go to a screensaver after 5 minutes without a button press, and a press on either MPD wakes them. Numbers 1 to 7 follow the manual's bezel figure. Bezel controls come first, then the page-structure rows.

| Control | Type | Positions / range | Lamps / display | Notes |
| --- | --- | --- | --- | --- |
| 1. Variable Action Buttons T1 to T6 (top row) | button | six buttons, T1 far left to T6 far right | label text beside each button | Pick the option shown next to the button. The labels change with the page |
| 1. Variable Action Buttons L1 to L6 (left column) | button | six buttons, L1 top to L6 bottom | label text beside each button | Same behaviour as the top row |
| 1. Variable Action Buttons R1 to R6 (right column) | button | six buttons, R1 top to R6 bottom | label text beside each button | Same behaviour as the top row |
| 1. Variable Action Buttons B1 to B6 (bottom row) | button | six buttons, B1 far left to B6 far right | label text beside each button | Same behaviour as the top row. B1 is also the M button (item 7). The manual's text ends this row at "L6", a typo for B6 |
| 2. VID Knob | knob | continuous; range not stated | none | Brightness of the video or map underlay, apart from the main symbology |
| 3. BRT Knob | knob | continuous; range not stated | none | Overall brightness of the display inside the level set with the Mode knob |
| 4. Mode Knob | rotary | DAY; NT; MONO (order as listed in the manual) | none | DAY: day brightness. NT: night brightness. MONO: night brightness with a single-colour scheme for night vision goggles |
| 5. Asterisk (*) Button | button | press | none | N/I |
| 6. Fixed Action Button FCR | button | press | none | Shows the Fire Control Radar page. The figure labels a group of fixed action buttons at each side of the bezel; which of the six sit in which group is not stated |
| 6. Fixed Action Button WPN | button | press | none | Shows the Weapon page |
| 6. Fixed Action Button TSD | button | press | none | Shows the Tactical Situation Display page |
| 6. Fixed Action Button VID | button | press | none | Shows the Video page |
| 6. Fixed Action Button COM | button | press | none | Shows the Communications page |
| 6. Fixed Action Button A/C | button | press | none | Shows the Flight page in the air, or the Engine page on the ground with weight on wheels |
| 7. M Button (VAB B1) | button | press | page title above the button | Shows the Menu page from any other page. From the Menu page it opens the DMS page |
| MPD screen | display | 6 by 6 inch colour LCD | page contents | Unnumbered. The page shown is named by the text above the M button: boxed means a top-level page, un-boxed means a sub-page was opened from it (a second sub-page level gets its own box and the first level is boxed in a dimmer green). A right-facing arrow above a button label marks a sub-page option; format options for the same page have no arrow |
| Menu page | display | pages listed below | buttons that open top-level pages | Opens any top-level page, grouped in three categories. AIRCRAFT: ENG (engine and drive train), FLT (flight instruments), FUEL, PERF (performance data), UTIL (utility systems). COMMUNICATIONS: DL (datalink), XPNDR (transponder), UHF, FM (FM1 and FM2), HF, COM (presets and network management). MISSION: ASE (survivability equipment), TSD (tactical situation display), WPN (weapons), FCR (fire control radar). Also on the Menu page: DMS, VIDEO, VCR and Favorites (*). VCR and Favorites are not implemented. The button positions on the Menu page are not stated. The COM page lists the DL, XPNDR, UHF, FM and HF pages as buttons that the manual marks N/I |
| Variable Action Button label styles | display | page, momentary, maintained, on/off, two-state, grouped, multi-state, paging, search, data entry, disabled, missing/invalid | button label shapes | Unnumbered. The shape of a label tells what the button does: page button (arrow, boxed when open), momentary (inverse video while running), maintained (keeps its state across pages), on/off (filled circle means powered), two-state, grouped (pick one of a list), multi-state (expanding list that collapses on a pick), paging and search (step through pages or lists), data entry (a > symbol makes the Keyboard Unit take the entry), disabled ("barriered": a green line beside the label), missing or invalid data (white label with a question mark). The symbols themselves are in the manual's figure |
