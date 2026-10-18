# A-10C II – reference pictures

Which picture of the DCS A-10C II flight manual (see [RESEARCH.md](RESEARCH.md)) shows each panel of [PANELS.md](PANELS.md), and how usable it is for drawing the panel page. The pictures are not in the repo (copyright). Get one again from the manual with:

```
pdfimages -j -f <page> -l <page> DCS_A-10C_II_Flight_Manual_EN.pdf p<page>
```

The image number in the table is the number pdfimages gives it on that page (`p129-002.jpg` = page 129, image 2). The manual's figures are DCS cockpit renders (JPEG, about 256 ppi) with a separate overlay for the callout arrows; the overlay is not needed.

Quality: `good` (every label and part readable), `partial` (some labels hidden, for example behind a toggle lever, or cut off; listed in the next column), `poor` (too small or blurred to draw from), `none` (no picture). Screenshot needed: `yes` when the page cannot be drawn from the manual picture alone.
