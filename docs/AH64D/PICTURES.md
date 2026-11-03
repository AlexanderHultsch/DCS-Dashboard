# AH-64D – reference pictures

Which picture shows each panel of [PANELS.md](PANELS.md), and how usable it was for drawing the panel page. The AH-64D pages were drawn from the owner's cockpit photos (straight-on photos of each panel, kept outside the repo and not listed by file name) and from the figures of the DCS AH-64D Flight Manual (see [RESEARCH.md](RESEARCH.md)). The pictures are not in the repo: the manual figures are copyrighted and the photos are personal. The manual figures are on the pages given in the table (printed page = PDF page). Get one again from the manual, a PDF in the DCS install under `Mods/aircraft/AH-64D/Doc/`, with:

```
pdfimages -j -p -f <page> -l <page> "<manual>.pdf" p<page>
```

pdfimages names the files `p<page>-<page>-<number>`; the number is the one pdfimages gives the image on that page. This file does not list image numbers or sizes: the figures were not looked at again for it. Where the callout numbers on the page help, render the page with `pdftoppm -r 150 -png -f <page> -l <page> "<manual>.pdf" page`.

**The quality column of this file is derived from the build history, not from looking at the pictures again.** The photos are not available to these notes. The old COCKPIT specs and the specs say, page by page, what the photos showed, which part had no photo and which value was read from a photo; where they say nothing the row says `not rated`. That is why almost every row says so.

Source picture: `owner photo` (with the dashboard page that was built from it) and, where the specs name it, the manual figure; `manual figure p. N` where no photo was used. Quality: `good` (the history says the photo showed everything), `partial` (the history records something hidden or missing), `not rated` (the history says nothing). Hidden or unreadable: what the history records, else `not recorded`; a remark after the semicolon is not a defect of the picture. Screenshot needed: `yes` where a part had no picture, or where the history says a value taken from a picture, or a lamp colour, must be checked in DCS; `no` where the page is built and tested, or the panel is not drawn on the dashboard.

## Pilot cockpit

| Panel | Manual page | Source picture | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- |
| Standby Magnetic Compass | 105 | manual figure p. 105 | not rated | not recorded; not drawn on the dashboard (instrument) | no |
| Master Warning / Master Caution Lighted Pushbuttons | 106 | manual figure p. 106 (CP/G p. 124) | not rated | not recorded; the two lamps are in the lamp row of every page, not a panel page; the manual text labels item 2 MSTR WARN, a typo | no |
| Fire Detection / Extinguishing Panel (FIRE DET/EXTG) | 106 | owner photo (FIRE DET/EXTG page), manual figure p. 106 | not rated | not recorded; the manual does not give the colours of the DISCH lights, check them in DCS | yes |
| Armament Panel | 108 | owner photo (ARMAMENT page), manual figure p. 108 | not rated | not recorded; the lamp colours ARM, SAFE and GND ORIDE are not confirmed, check them in DCS | yes |
| Video Panel | 109 | owner photo (ARMAMENT page), manual figure p. 109 | not rated | not recorded | no |
| Canopy Jettison Handle | 109 | manual figure p. 109 | not rated | not recorded; not on the dashboard (no DCS-BIOS identifier) | no |
| Master Zeroize Switch | 109 | manual figure p. 109 (no owner photo) | partial | no photo: the page draws MASTER ZEROIZE as a plain placard | yes |
| Standby Attitude Indicator | 110 | manual figure p. 110 | not rated | not recorded; not drawn on the dashboard (instrument) | no |
| Standby Airspeed Indicator | 111 | manual figure p. 111 | not rated | not recorded; not drawn on the dashboard (instrument) | no |
| Standby Altimeter | 111 | owner photo (CENTER page), manual figure p. 111 | not rated | not recorded; only the barometric setting knob is on the dashboard, as ALT SET | no |
| Check Overspeed Test / Generator Reset Panel | 111 | owner photo (CENTER page), manual figure p. 111 | not rated | not recorded; the page deliberately does not follow the arrangement of the photo | no |
| Windshield Wiper Control Panel | 112 | owner photo (CENTER page and CP/G WIPER / DEFOG page), manual figure p. 112 (CP/G p. 127) | not rated | not recorded; the page prints the position labels as flat text in a fan, not turned along the dial as on the photo | no |
| Parking Brake Handle | 112 | owner photo (CENTER page), manual figure p. 112 | not rated | not recorded; the name is printed on two lines (PARK, BRAKE) | no |
| Keyboard Unit (KU) | 113 | owner photo (KU tab), manual figure p. 113 | not rated | not recorded; the Display Prompt has no DCS-BIOS entry | no |
| Tail Wheel / NVS Mode Panel | 115 | owner photo (TAIL WHEEL / NVS page), manual figure p. 115 | not rated | not recorded | no |
| Emergency Panel | 116 | owner photo (EMERGENCY page), manual figure p. 116 | not rated | not recorded | no |
| Power Quadrant Panel | 117 | owner photo (POWER page), manual figure p. 117 | not rated | not recorded; the FRICT slider direction was taken from the photo and is not checked in DCS | yes |
| Stores Jettison Panel | 119 | owner photo (STORES JETT page), manual figure p. 119 | not rated | not recorded; the figure labels L TIP and R TIP only 'No function' | no |
| Exterior Lighting / Interior Lighting Panel | 119 | owner photo (EXT / INTR LT page), manual figure p. 119 | not rated | not recorded; the end of the SIGNAL knob sweep was taken from the photo and is not checked in DCS | yes |
| Free Air Temperature Gauge | 120 | manual figure p. 120 | not rated | not recorded; not drawn on the dashboard (instrument) | no |
| Communications Panel | 121 | owner photo (COMM page and CP/G COMM page), manual figure p. 121 (CP/G p. 127) | not rated | not recorded; the figure labels the ATA knob 'No function'; the page does not follow the photo for the ICS and PTT labels | no |
| CMWS Control Panel | 630 | owner photo (CMWS page), manual figure p. 630 (indicator display p. 631) | not rated | not recorded | no |
| Items named only in the pilot overview figure | 104, 394 | manual figure p. 104 | not rated | labels only: the manual gives these items no description in the cockpit chapter; not drawn | no |

## Copilot/Gunner cockpit

| Panel | Manual page | Source picture | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- |
| Interior Lighting Panel | 126 | owner photo (INTR LT page), manual figure p. 126 | not rated | not recorded | no |
| Processor Select Panel | 127 | manual figure p. 127 | not rated | not recorded; the whole panel is N/I, not on the dashboard | no |
| Console fittings named only in the overview figures | 125, 127 | manual figure pp. 125 and 127 | not rated | labels only in the figures, no description; not drawn | no |
| TEDAC Display Unit (TDU) | 129 | owner photo (MPD tab, TEDAC), manual figure p. 129 | not rated | not recorded; the TDU screen is not drawn | no |
| TEDAC Left Handgrip (LHG) | 131 | manual figure p. 131 | not rated | not recorded; items 10, 13 and 14 sit on the opposite side of the grip; the figure labels the Cage Button 'No function' | no |
| TEDAC Right Handgrip (RHG) | 134 | manual figure p. 134 | not rated | not recorded; items 10, 13 and 14 sit on the opposite side of the grip; the figure labels the HDD Button 'No function' | no |

## Hand controls (cyclic and collective grips)

| Panel | Manual page | Source picture | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- |
| Cyclic Grip | 136 | manual figure p. 136 | not rated | not recorded; the figure labels the Cage Button 'No function' | no |
| Collective Flight Grip | 138 | manual figure p. 138 | not rated | not recorded | no |
| Collective Mission Grip | 140 | manual figure p. 140 | not rated | not recorded | no |

## Displays (EUFD, MPD)

| Panel | Manual page | Source picture | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- |
| Enhanced Up-Front Display (EUFD) | 155 | owner photo (EUFD page), manual figure p. 155 (overview p. 105) | not rated | not recorded; the page puts the controls in a row below the glass, not around it as on the photo | no |
| Multi-Purpose Displays (MPD) | 164 | owner photo (MPD tab), manual figure p. 164 | not rated | not recorded; the MPD screen, the Menu page and the button label styles are not drawn | no |

## Summary

34 panels (every `###` section of PANELS.md): 0 good, 1 partial, 33 not rated. 19 were drawn from an owner photo (one of them, the standby altimeter, only for its setting knob), 15 from the manual figure only or are not drawn.

### Screenshots needed

- Fire Detection / Extinguishing Panel (FIRE DET/EXTG): the manual does not give the colours of the DISCH lights, check them in DCS
- Armament Panel: the lamp colours ARM, SAFE and GND ORIDE are not confirmed, check them in DCS
- Master Zeroize Switch: no photo: the page draws MASTER ZEROIZE as a plain placard
- Power Quadrant Panel: the FRICT slider direction was taken from the photo and is not checked in DCS
- Exterior Lighting / Interior Lighting Panel: the end of the SIGNAL knob sweep was taken from the photo and is not checked in DCS
