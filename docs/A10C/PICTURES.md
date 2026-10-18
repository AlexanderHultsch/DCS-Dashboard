# A-10C II – reference pictures

Which picture of the DCS A-10C II flight manual (see [RESEARCH.md](RESEARCH.md)) shows each panel of [PANELS.md](PANELS.md), and how usable it is for drawing the panel page. The pictures are not in the repo (copyright). Get one again from the manual with:

```
pdfimages -j -f <page> -l <page> DCS_A-10C_II_Flight_Manual_EN.pdf p<page>
```

The image number in the table is the number pdfimages gives it on that page (`p129-002.jpg` = page 129, image 2). The manual's figures are DCS cockpit renders (JPEG, about 256 ppi) with a separate overlay for the callout arrows; the overlay is not needed.

Quality: `good` (every label and part readable), `partial` (some labels hidden, for example behind a toggle lever, or cut off; listed in the next column), `poor` (too small or blurred to draw from), `none` (no picture). Screenshot needed: `yes` when the page cannot be drawn from the manual picture alone.

## Control stick and throttles (HOTAS)

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| Control Stick | 108 | p108-002.jpg | 1100 × 825 | partial | No hat labels; NWS barely visible; MMCB only on rear stick | no |
| Throttles | 111 | p111-002.jpg | 564 × 616 | partial | Pinky, slew, coolie hat black on black; levers not shown | no |

## Left front dash

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| Left Engine "T-Handle" Fire Extinguisher Discharge Select | 114 | p114-002.jpg | 587 × 440 | good | Handle lamp unlit; FIRE ENG PULL legend readable | no |
| Radar Warning Receiver (RWR) Display | 115 | p115-002.jpg | 587 × 440 | good | Scope dark, no emitter symbols; INT button and legend readable | no |
| Airspeed Indicator | 116 | p116-000.jpg | 517 × 507 | good | Zero label not shown; drum shows 40 | no |
| Standby Attitude Indicator (SAI) | 117 | p117-002.jpg | 587 × 440 | good | none; OFF flag shown, PULL TO CAGE legible | no |
| UHF Frequency Repeater | 118 | p118-002.jpg | 587 × 440 | good | Frequency window blank (unpowered) | no |
| Angle of Attack Indicator | 118 | p118-006.jpg | 587 × 440 | partial | OFF flag hidden (only dark window at right) | no |
| Digital Clock | 119 | p119-002.jpg | 587 × 440 | good | Display unpowered, digits dim; SEL and CTRL legible | no |
| Emergency Jettison Button | 120 | p120-000.jpg | 587 × 440 | good | none | no |
| Left Multifunction Color Display (MFCD) | 121 | p121-002.jpg | 587 × 440 | good | OSB numbers not printed; screen blank; rockers and DAY NT OFF legible | no |
| Landing Gear and Flap Control Panel | 126 | p126-002.jpg | 448 × 865 | partial | LGD GEAR DOWN legend and handle lamp hidden; 20 behind flap pointer | no |
| Armament HUD Control Panel (AHCP) | 129 | p129-002.jpg | 564 × 960 | partial | Lower position labels hidden behind levers (TRAIN, GUNARM, OFF, NIGHT, STBY) | no |
| Heading Attitude Reference (HARS) Fast Erect Button | 133 | p133-002.jpg | 587 × 440 | good | none | no |
| Gun and Nose Wheel Steering (NWS) Lights | 134 | p134-002.jpg | 588 × 170 | good | none; both lamps shown lit | no |

## Center front dash

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| APU "T Handle" Fire Extinguisher Discharge Select | 136 | p136-002.jpg | 588 × 166 | good | Handle lamp unlit; FIRE APU PULL legend readable | no |
| Countermeasures Set Control (CMSC) | 136 | p136-006.jpg | 588 × 235 | good | Windows dark, no characters; all legends, knobs, buttons readable | no |
| Attitude Director Indicator (ADI) | 137 | p137-002.jpg | 383 × 439 | good | Bank scale ticks unnumbered; knob unlabelled; all flags shown | no |
| Horizontal Situation Indicator (HSI) | 139 | p139-002.jpg | 498 × 442 | good | Range drum cut mid-digit; all legends readable | no |
| Navigation Mode Select Panel (NMSP) | 141 | p141-002.jpg | 585 × 232 | partial | ABLE label behind PTR lever; homing lamp legends dim | no |
| Target Identification Set Laser (TISL) control panel | 135 | p135-002.jpg | 215 × 825 | poor | Only a low-res strip of whole dash; ENTER label under knob, fourth button blank | no |

## Right dash

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| Fire Extinguisher Discharge | 144 | p144-002.jpg | 586 × 147 | good | none | no |
| Right Multifunction Color Display (MFCD) | 144 | p144-006.jpg | 587 × 440 | good | OSB numbers dim; screen blank; DAY NT OFF and rockers legible | no |
| Fuel Quantity and Hydraulic Indicator Panel | 146 | p146-002.jpg | 258 × 440 | partial | HYD dial numerals tiny; fuel gauge, selector, TEST IND legible | no |
| RIGHT Engine "T Handle" Fire Extinguisher Discharge Select | 147 | p147-002.jpg | 587 × 120 | good | Handle lamp unlit; FIRE R ENG PULL legend readable | no |
| Marker and Canopy Lights | 148 | p148-002.jpg | 587 × 110 | good | none; both lamps shown lit | no |
| Vertical Velocity Indicator (VVI) | 148 | p148-006.jpg | 587 × 440 | good | Pointer covers part of the 0 label | no |
| Altimeter | 149 | p149-002.jpg | 587 × 440 | partial | Counter digits partly masked by black patches; set knob unlabelled | no |
| Engine Monitoring Instruments (EMI) | 150 | p150-002.jpg | 587 × 440 | partial | Fuel flow multiplier cut; some numerals under pointer hubs | no |

## Above the dash

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| Heads Up Display Area Above Dash | 152 | p152-002.jpg | 1100 × 825 | good | Overview; HUD glass empty; bottom UFC legends cut by T-handles | no |
| Standby Compass | 153 | p153-002.jpg | 587 × 440 | good | Card shows only 3, N, 33; rest of card scrolls | no |
| Air Refuel Status Lights | 154 | p154-002.jpg | 587 × 287 | good | none; all three legends shown lit | no |
| Accelerometer (G-meter) | 154 | p154-006.jpg | 587 × 440 | good | none; PUSH TO SET button and ACCELERATION LIMITS legible | no |
| Angle of Attack Indexer | 155 | p155-002.jpg | 586 × 260 | good | none; all three symbols shown lit | no |

## Left console

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| Fuel System Control Panel | 158 | p158-002.jpg | 737 × 960 | good | none; pump-on positions unlabelled, lever lamps unlit | no |
| Throttles Panel | 161 | p161-002.jpg | 583 × 960 | partial | Right lever not shown; friction DECR end cut; left lever grip hides slot | no |
| Flap lever, left of the throttles | 508 | p508-002.jpg | 639 × 853 | poor | Overview; lever about 40 px, partly under throttle grip; UP, MVR, DN tiny | yes |
| LASTE Control Panel | 165 | p165-002.jpg | 589 × 202 | good | none | no |
| AN/ARC-186(V) Radio Control Panel | 167 | p167-002.jpg | 713 × 602 | partial | Shadow over screen and left knobs; TR G and OFF partly hidden; knobs unlabelled | no |
| AN/ARC-164 UHF Radio Control Panel | 168 | p168-002.jpg | 587 × 440 | partial | LOAD button hidden under open preset card; display blank | no |
| AN/ARC-186(V) VHF FM Radio 2 Control Panel | 171 | p171-002.jpg | 499 × 287 | good | Dial pointers smudged; preset window shows 1; all legends readable | no |
| KY-58 Secure Voice Control Panel | 173 | p173-002.jpg | 586 × 334 | good | DELAY partly under toggle; legends on guard and dials readable | no |
| Emergency Brake System | 174 | p174-002.jpg | 587 × 440 | partial | Toggle title cut at top edge; handle seen at an angle | no |
| Auxiliary Lighting Control Panel | 175 | p175-002.jpg | 474 × 441 | good | N of NORM hidden by toggle lever | no |
| Stability Augmentation System (SAS) Panel | 177 | p177-002.jpg | 587 × 394 | good | TAKEOFF TRIM window blank, legend not legible | no |
| Identify Friend or Foe (IFF) Panel | 179 | p179-002.jpg | 953 × 960 | good | STBY and MODE 4 OUT partly under levers; all code wheels shown | no |
| Emergency Flight Control Panel | 180 | p180-002.jpg | 587 × 440 | good | Four lamps unlit, unlabelled; all switch legends readable | no |
| Intercom Control Panel | 182 | p182-002.jpg | 1010 × 735 | good | Two unlabelled dark knobs; INT legend only at side | no |
| Stall Warning Control Panel | 183 | p183-002.jpg | 586 × 158 | good | none | no |
