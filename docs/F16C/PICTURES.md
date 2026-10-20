# F-16C Viper – reference pictures

Which picture of the DCS F-16C Early Access Guide (see [RESEARCH.md](RESEARCH.md)) shows each panel of [PANELS.md](PANELS.md), and how usable it is for drawing the panel page. The pictures are not in the repo (copyright). Get one again from the manual with:

```
pdfimages -j -p -f <page> -l <page> "DCS F-16C Early Access Guide EN.pdf" p<page>
```

pdfimages names the files `p<page>-<page>-<number>`; the table drops the repeated page, so the image number is the number pdfimages gives it on that page (`p055-005.jpg` = page 55, image 5). The manual's figures are DCS cockpit renders (JPEG, about 220 ppi). Most are close-ups of one panel and only 100 to 700 px wide, because the page prints them small; only the cockpit overviews (pp. 44, 55, 58, 62, 75, 90) are 1152 px wide. Every figure has a separate low-resolution overlay for the callout arrows and number tags (stored as flat images, extracted as .ppm); the overlays are not needed. One figure (`p080-002`) is stored the same way and was converted to PNG. Where a panel is only part of an overview picture, or the picture is small and the callout numbers on the page help, the page is also rendered with `pdftoppm -r 150 -png -f <page> -l <page> "DCS F-16C Early Access Guide EN.pdf" page` (`page-055.png` = page 55); the table says so.

Quality: `good` (every label and part readable), `partial` (some labels hidden, for example behind a toggle lever, or cut off, or the picture is very small; listed in the next column), `poor` (too small or blurred to draw from), `none` (no picture). Screenshot needed: `yes` when the page cannot be drawn from the manual picture alone. "Hidden or unreadable" starting with `none` means nothing is hidden; text after the semicolon is a remark.

## Hands-on controls (HOTAS)

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| Side Stick Controller (SSC) | 83 | p083-006.jpg | 330 × 637 | partial | No switch legends on the grip (the callout numbers are only on the page); rear of the grip not shown; second view p083-002.jpg (234 × 252) shows the top | no |
| Throttle | 86 | p086-002.jpg | 813 × 500 | partial | Grip only, seen from above at an angle; some legends cut or turned away; throttle lever, OFF and IDLE detents and Cutoff Release not shown | yes |

## Instrument panel

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| AoA Indexer | 44 | p044-002.jpg | 154 × 294 | good | Small; dimming lever only a stub at the left; all three symbols shown lit; page-044.png has the callouts | no |
| AR Status / NWS Indicator | 45 | p045-013.jpg | 154 × 294 | good | Small; dimming lever at the right; RDY, AR NWS and DISC all shown lit | no |
| Left Eyebrow Lights | 45 | p045-002.jpg | 483 × 625 | good | Seen at about 35 degrees; two square buttons blank; part of the MISC panel and MFD edge in frame | no |
| Right Eyebrow Lights | 46 | p046-002.jpg | 440 × 461 | good | Seen at about 40 degrees; all ten legends shown lit and readable; fuel flow digits cut in at the left | no |
| Miscellaneous (MISC) Panel | 47 | p047-002.jpg | 302 × 828 | partial | RF NORM and LASER ARM ON legends partly under the lever tips; two eyebrow buttons cut in at the top left | no |
| Autopilot controls | — | — | — | — | Cross-reference, no panel of its own; the controls are drawn from the MISC panel (p. 47), SSC (p. 83), EHSI (p. 230) and ICP (p. 99) pictures | — |
| Standby Attitude Indicator (SAI) | 49 | p049-002.jpg | 329 × 314 | good | none; PULL TO CAGE legible; no OFF flag shown, bank scale unnumbered | no |
| Fuel Flow Indicator | 50 | p050-002.jpg | 330 × 253 | good | none; drum shows 6500 with the next digit half rolled | no |
| Engine Instruments | 50 | p050-005.jpg | 220 × 588 | good | none; OIL, NOZ POS, RPM and FTIT gauges all shown, OIL gauge touches the top edge | no |
| Airspeed and Mach Indicator | 51 | p051-002.jpg | 286 × 284 | partial | Inner Mach scale hidden behind a dark wedge; pointers cover some numerals; no Mach window shown | no |
| Altimeter | 51 | p051-017.jpg | 286 × 283 | good | none; PNEU flag and ELEC/PNEU lever legible, baro knob unlabelled | no |
| Angle-of-Attack (AoA) Indicator | 52 | p052-013.jpg | 110 × 229 | partial | Only 110 px wide; scale numbers 15 and 10, AOA and DEG readable, other ticks tiny; page-052.png has the callouts | no |
| Vertical Velocity Indicator (VVI) | 52 | p052-002.jpg | 110 × 209 | partial | Only 110 px wide; 0, .5, 1 and 1000 FPM readable, ticks tiny; page-052.png has the callouts | no |
| Attitude Director Indicator (ADI) | 53 | p053-002.jpg | 330 × 330 | good | none; OFF and AUX flags shown; a small white arrow and dot from the manual's overlay are baked in at the lower right | no |
| Electronic Horizontal Situation Indicator (EHSI) | 230 | p230-002.jpg | 550 × 550 | good | none; screen shows a NAV page; the two knobs and the M button unlabelled | no |
| FUEL QTY SEL Panel | 54 | p054-002.jpg | 220 × 436 | good | none; round plug at the top unlabelled | no |

## Left auxiliary console

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| Landing Gear Panel | 55 | p055-005.jpg | 468 × 541 | partial | Hook switch cut at the top right edge; LG handle UP and DN legends under the grip; speed brake indicator cut at the left edge (two clean views on p. 57: p057-005.jpg and p057-008.jpg, 91 × 153 each) | no |
| HMCS Control Panel | 57 | p057-002.jpg | 418 × 123 | good | none | no |
| ALT GEAR Handle | 57 | p057-011.jpg | 132 × 216 | partial | Handle and its recess only, no placard or legend; small; location in the overview p055-002.jpg; page-055.png and page-057.png added | no |

## Right auxiliary console

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| Magnetic Compass | 58 | p058-005.jpg | 220 × 209 | good | Card shows only E, 6 and 3; the rest of the card scrolls | no |
| Fuel Quantity Indicator | 58 | p058-002.jpg | 220 × 226 | partial | Needle hubs cover part of the scale and the AL and FR letters; totalizer drum digits half rolled | no |
| Pilot Fault List Display (PFLD) | 59 | p059-005.jpg | 439 × 174 | good | none; shows one sample fault message | no |
| Caution Light Panel | 59 | p059-002.jpg | 485 × 372 | good | none; all 26 legends readable, the six blank cells drawn as a dash line | no |
| Hydraulic Pressure Indicators | 61 | p061-002.jpg | 220 × 321 | good | Needles cover the HYD legends of both gauges; plus sign and B legend at the right readable | no |
| EPU Fuel Quantity Indicator | 61 | p061-005.jpg | 220 × 226 | good | Pointer covers the 100 numeral | no |
| Cabin Pressure Gauge | 61 | p061-008.jpg | 220 × 224 | good | Pointer covers part of the PRESS ALT legend | no |
| Mechanical Clock | 61 | p061-011.jpg | 220 × 235 | good | Two round knobs unlabelled; day hand not distinguishable | no |

## Left console

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| Manual Pitch Override Switch | 62 | p062-005.jpg | 160 × 139 | good | none; both guards shown | no |
| ENG & JET START Control Panel | 63 | p063-002.jpg | 228 × 552 | partial | MAX POWER ON legend and ENG CONT PRI under the lever tips (only the F of OFF shows); RUN lamp unlit | no |
| EPU Control Panel | 64 | p064-002.jpg | 350 × 158 | good | none; guard raised, OFF, ON and NORM legible, HYDRAZN AIR lamp text turned 90 degrees | no |
| ELEC Control Panel | 64 | p064-013.jpg | 330 × 440 | good | Start of the MAIN PWR legend under the lever; all lamps shown lit | no |
| AUDIO 1 Control Panel | 65 | p065-002.jpg | 440 × 341 | good | none; one picture shows both audio panels, AUDIO 1 is the upper one | no |
| AUDIO 2 Control Panel | 65 | p065-002.jpg | 440 × 341 | good | none; the lower panel of the same picture | no |
| AVTR Control Panel | 66 | p066-002.jpg | 483 × 191 | good | none | no |
| FUEL Control Panel | 67 | p067-002.jpg | 445 × 177 | partial | MASTER legend partly under the red guard; guard shown raised | no |
| IFF Control Panel | 67 | p067-013.jpg | 447 × 285 | partial | M-4 CODE ZERO and monitor AUD legends partly under the lever tips; code wheels show 0040 | no |
| EXT LIGHTING Control Panel | 69 | p069-085.jpg | 484 × 284 | good | Knob pointers cover parts of the scales; the large night picture p069-002.jpg shows the aircraft lights, not the panel | no |
| FLT CONTROL Panel | 71 | p071-002.jpg | 440 × 350 | partial | MANUAL TF FLY-UP and ENABLE legends partly under the lever | no |
| MANUAL TRIM Panel | 72 | p072-002.jpg | 440 × 321 | partial | TRIM/AP DISC switch name under the lever tip | no |
| TEST Panel | 72 | p072-013.jpg | 237 × 323 | partial | FLCS PWR TEST label under the lever (only EST shows); small | no |
| Canopy Switch and Canopy Handle | 73 | p073-002.jpg | 438 × 307 | poor | Oblique view of the yellow handle and a small silver switch; no legends or positions shown; page-073.png has the callouts | yes |
| Canopy Jettison T-Handle | 74 | p074-002.jpg | 330 × 211 | good | none | no |
| DEFOG Lever | 74 | p074-005.jpg | 330 × 126 | good | none; MIN, DEFOG, MAX legible | no |
| Manual Canopy Control Handcrank | 62 | p062-002.jpg | 1152 × 608 | poor | Overview only; the crank is about 80 px wide at the top left edge, partly cut; page-062.png has the callouts | yes |
| ANTI-G TEST Button | 62 | p062-002.jpg | 1152 × 608 | poor | Overview only; round button about 30 px wide at the bottom left, legend turned sideways; page-062.png has the callouts | yes |
| UHF Backup Control Panel | 260 | p260-002.jpg | 439 × 374 | good | Somewhat soft; preset card shown, frequency window lit | no |

## Right console

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| SNSR PWR Control Panel | 75 | p075-002.jpg | 440 × 134 | partial | RDR ALT STBY legend under the lever (only TBY shows); ON positions not printed; cut at the left edge | no |
| Interior LIGHTING Control Panel | 76 | p076-002.jpg | 440 × 352 | good | Knob pointers cover parts of the BRT legends | no |
| AIR COND Control Panel | 76 | p076-017.jpg | 440 × 176 | good | none | no |
| KY-58 Secure Voice Panel | 77 | p077-005.jpg | 440 × 319 | partial | Top edge hidden under the seat hardware; some knob legends cut | no |
| PLAIN/CIPHER Switch | 77 | p077-002.jpg | 110 × 138 | partial | Only 110 px wide; CRAD 1, CRAD 2 and PLAIN shown, no CIPHER legend; page-077.png added | no |
| OXYGEN Regulator Panel | 77 | p077-008.jpg | 440 × 235 | good | none; supply gauge numerals small | no |
| ENGINE ANTI-ICE Switch | 78 | p078-002.jpg | 439 × 127 | partial | ENG and ON legends under the lever; shares the picture with the ANT SEL panel | no |
| ANT SEL Panel | 78 | p078-002.jpg | 439 × 127 | partial | UPPER, IFF and UHF legends partly under the lever tips | no |
| AVIONICS POWER Control Panel | 78 | p078-011.jpg | 440 × 288 | partial | Top row legends (MMC, ST STA and others) partly under the toggle tips; rest readable | no |
| VOICE MESSAGE Switch | 80 | p080-002.png | 92 × 144 | good | Small; page-080.png added | no |
| ZEROIZE Switch | 80 | p080-005.jpg | 146 × 150 | good | none; guard shown raised, OFP, OFF and DATA legible | no |
| SEAT ADJ Switch | 80 | p080-008.jpg | 596 × 402 | partial | Oblique view; legend very dark and barely legible; lever shown in the centre position | no |
| NUCLEAR CONSENT Switch | 80 | p080-008.jpg | 596 × 402 | partial | Oblique view; ARM/REL, OFF and REL ONLY legible; guard shown raised | no |
| Other right console fittings | 75 | p075-013.jpg | 1152 × 591 | poor | Overview only; utility light, arm rest and DTU receptacle are small and unlabelled in the picture; p127-002.jpg is the MFD DTE page, not the receptacle; page-075.png has the callouts | yes |

## Ejection seat

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| Ejection Seat Controls | 81 | p081-002.jpg | 738 × 379 | partial | Handle seen from the front at an angle, no legend on it; arming lever in p081-007.jpg (440 × 611) and manual chute lever in p082-002.jpg (477 × 291), both legible with their placards; PEDAL ADJ knob visible but not described | no |

## Display-related controls

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| Head-Up Display (HUD) | 90 | p090-002.jpg | 1152 × 665 | good | Overview; glass with symbology and both frame posts, no mounted legends; a clearer de-cluttered view is p094-021.jpg (528 × 442) | no |
| HUD Control Panel | 94 | p094-002.jpg | 439 × 196 | partial | Lever tips cover part of the lower-position legends (VV/VAH, ATT/FPM, ALT RADAR AUTO, TEST STEP OFF) | no |
| Integrated Control Panel (ICP) | 99 | p099-002.jpg | 660 × 480 | good | none; all keys, wheels and the DRIFT C/O and FLIR switches legible | no |
| Data Entry Display (DED) | 101 | p101-000.jpg | 1203 × 1069 | partial | A diagram of DED pages on black, not a picture of the frame; the frame is seen only small in the overview p044-013.jpg and in p090-002.jpg; page-101.png and page-044.png added | no |
| Multi-Function Display (MFD) bezel | 122 | p122-002.jpg | 660 × 660 | good | OSB numbers not printed; screen shows the menu page; GAIN, SYM, BRT and CON legends legible | no |
| MFD Format Selection Master Menu | 124 | p124-002.jpg | 660 × 660 | good | none; all legends of the numbered items shown, FCR highlighted | no |

## Defensive systems

| Panel | Manual page | Image | Size px | Quality | Hidden or unreadable | Screenshot needed |
| --- | --- | --- | --- | --- | --- | --- |
| Threat Warning Azimuth Indicator | 694 | p694-004.jpg | 374 × 371 | good | none; scope shows sample symbols; no brightness knob in the picture | no |
| Threat Warning Prime Control Panel | 695 | p695-002.jpg | 385 × 433 | good | Cropped to the six buttons, no bezel; all legends lit | no |
| Threat Warning Auxiliary Control Panel | 696 | p696-002.jpg | 189 × 338 | good | none; small | no |
| CMDS Control Panel | 697 | p697-011.jpg | 485 × 310 | good | A few ON and OFF legends touched by the lever tips; display shows 60 60 | no |
| ECM Control Panel | 706 | p706-002.jpg | 408 × 181 | partial | DIM lever hides the OPR and STBY legends; the second button of the second row blank | no |
| CHAFF/FLARE Dispense Button | 708 | p708-032.jpg | 326 × 192 | poor | Dark oblique view of the wall near the throttle; button not recognisable; page-708.png has the callouts | yes |

## Summary

75 sections, 74 panels (the autopilot controls are a cross-reference without a picture of their own): 42 good, 27 partial, 5 poor, 0 none.

### Screenshots needed

- Throttle: only the grip seen from above; the lever, detents and Cutoff Release are not shown
- Canopy Switch and Canopy Handle: oblique view, no legends, switch small
- Manual Canopy Control Handcrank: only about 80 px in the left console overview
- ANTI-G TEST Button: only about 30 px in the left console overview
- Other right console fittings (utility light, arm rest, DTU receptacle): only small in the right console overview
- CHAFF/FLARE Dispense Button: dark oblique view, button not recognisable
