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
