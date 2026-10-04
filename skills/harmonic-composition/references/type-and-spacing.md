# Type and Spacing Reference

## Contents

- 1. Building a scale
- 2. Modular and double-stranded scales
- 3. Platform text styles
- 4. Relations worth checking
- 5. Baseline and line height
- 6. Figures, tracking, and optical details
- 7. Spacing sets
- 8. Worked scale: SOLAR HUD

## 1. Building a scale

1. Start from the reading size the content needs on the target device (iPhone body 17 pt, web 16–18 px).
2. Pick the step ratio from the governing family (5:4 calm, 4:3 firm, φ dramatic).
3. Generate up and down, round to whole points, then delete sizes the product does not need. Five to nine sizes is enough.
4. Keep adjacent sizes at least about 1.12 apart; closer steps read as mistakes rather than hierarchy.
5. Map each size to a platform text style so accessibility scaling still works.

## 2. Modular and double-stranded scales

- **Single strand:** `size(n) = base × ratio^n`.
- **Double strand:** two bases with the same ratio, interleaved. Example with φ on 13 and 17: 13, 17, 21, 27.5, 34, 44.5, 55, 72. It keeps two meaningful anchors (micro and body) inside one family.
- **Classical scale (Bringhurst):** 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 21, 24, 36, 48, 60, 72. Useful as a sanity check: good screen scales often land near it.

## 3. Platform text styles

Apple (iOS, default size): largeTitle 34, title 28, title2 22, title3 20, headline 17 semibold, body 17, callout 16, subheadline 15, footnote 13, caption 12, caption2 11. Use them with weights applied after the style so Dynamic Type keeps scaling.

Material 3: display 57/45/36, headline 32/28/24, title 22/16/14, body 16/14/12, label 14/12/11.

Several built-in steps are already near harmonic: 17:13 ≈ φ²/2, 22:17 ≈ 1.29, 28:22 ≈ 1.27, 34:17 = 2:1.

## 4. Relations worth checking

| Pair | Ratio | Nearest reading |
| --- | --: | --- |
| 17 : 13 | 1.308 | φ²/2 = 1.309 (closer than 4:3) |
| 22 : 17 | 1.294 | φ²/2, approximate |
| 28 : 17 | 1.647 | φ, approximate |
| 35 : 28 | 1.250 | 5:4, exact |
| 59 : 22 | 2.682 | φ², approximate |
| 74 : 59 | 1.254 | 5:4, strong |
| 74 : 28 | 2.643 | φ², approximate |
| 34 : 17 | 2.000 | octave, exact |

Report the deviation `|actual − target| / target`. Under 1 % is strong; 1–3 % approximate; above 3 % do not claim the relation.

## 5. Baseline and line height

- Use a 4 pt baseline on screens; line heights are multiples of it where the platform allows.
- Body line height about 1.3–1.5 × size; display sizes 1.0–1.2 ×.
- Gutters and paragraph gaps equal one or more line intervals, as in Müller-Brockmann's grid.

## 6. Figures, tracking, and optical details

- Tabular figures for any changing number (clocks, timers, tables): `font-variant-numeric: tabular-nums` or SwiftUI `.monospacedDigit()`.
- Let SF Pro and other system fonts handle their own tracking; add positive tracking only to all-caps labels, slight negative tracking only to very large display sizes.
- Avoid light weights below 20 pt.
- Typographic correctness counts as harmony: true minus sign (−, U+2212), real apostrophe (’), and in French a no-break space between number and unit (« 11 min », « 2 h 42 ») and inside guillemets.
- Optical corrections (overshoot, colon alignment, visual centring) may break the numeric grid by a point; document them as deliberate exceptions.

## 7. Spacing sets

- **Fibonacci:** 2, 3, 5, 8, 13, 21, 34, 55 — coherent with golden positions and Lucas grids.
- **Rational:** 4, 8, 12, 16, 24, 32, 48, 64 — coherent with 8 pt systems and 4:3 or 3:2 grids.
- Pick one set per product. Use the micro end (2–5) inside components, the macro end (13–34) between groups.

## 8. Worked scale: SOLAR HUD

| Size | Role |
| --: | --- |
| 11 | exception only |
| 13 | micro labels |
| 15 | compact UI |
| 17 | reading |
| 22 | fact, larger value |
| 28 | large value |
| 35 | article, large hook |
| 59 | secondary display |
| 74 | hero clock |

Philosophy: 18 divisions govern position; 5:4 and 4:3 (read precisely as φ²/2 for 17:13) govern strong typographic relations; 13/15/17 govern daily legibility; 11 is an exception; 2/3/4/5 govern micro-spacing. One harmonic idea does not have to rule every level.

