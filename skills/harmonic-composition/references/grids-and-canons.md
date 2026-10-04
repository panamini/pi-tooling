# Grids and Canons Reference

## Contents

- 1. Modular grid (Müller-Brockmann)
- 2. Page canons (Van de Graaf, Villard, Tschichold, Rosarivo)
- 3. Root rectangles and dynamic symmetry
- 4. Rabatment and armatures
- 5. Modulor
- 6. Integer golden grids (Lucas, Fibonacci)
- 7. Screen grids and platform constraints
- 8. Choosing a grid

## 1. Modular grid (Müller-Brockmann)

From *Grid Systems in Graphic Design* (1981):

- The text type size and leading come first; the grid derives from them.
- Columns and rows form fields; the gutter between fields equals one or more line intervals, so every field starts and ends on a baseline.
- Field heights are whole numbers of lines. Typical counts: 4, 8, 20, or 32 fields per page.
- Images, captions, and headings snap to field edges. Hierarchy comes from size and position, not ornament.
- Asymmetric, flush-left, ragged-right text is the default reading form.

On screens, use the line interval (for example a 4 pt baseline with 8 pt multiples) as the vertical unit, and let column count adapt to width.

## 2. Page canons (Van de Graaf, Villard, Tschichold, Rosarivo)

- **Van de Graaf canon:** on a 2:3 page, the diagonals of the page and of the spread construct a text block whose height equals the page width. Margins divide the page into ninths: inner 1/9, top 1/9, outer 2/9, bottom 2/9 (ratio 2:3:4:6 for inner:top:outer:bottom).
- **Villard diagram:** a geometric construction that divides a segment into any number of equal parts without measuring.
- **Tschichold (*The Form of the Book*):** documented these medieval canons and favoured 2:3 pages with the 2:3:4:6 margins; he warned against arbitrary formats.
- **Rosarivo:** the same ninths reached by dividing the page into 9 × 9.
- Use for editorial pages, long reading, and print-like screens; adapt margins to safe areas on devices.

## 3. Root rectangles and dynamic symmetry

- **√2:** halving the long side yields two rectangles of the same ratio (ISO 216 A series). Good for systems that must scale by halves.
- **√3, √5:** built by successive diagonals from a square; √5 contains two golden rectangles and a square.
- **φ:** a square plus its golden extension; removing the square leaves another φ rectangle.
- **Dynamic symmetry (Jay Hambidge):** the diagonal of a rectangle and the perpendicular to it from a corner (its reciprocal) divide the frame into similar rectangles. Intersections of diagonals and reciprocals are strong placement points.

## 4. Rabatment and armatures

- **Rabatment:** fold the short side onto the long side to inscribe a square at each end; the square's inner edge is a natural division line.
- **Harmonic armature of the rectangle:** both diagonals, the four reciprocals, the midlines, and the rabatment lines. Their intersections give a small, reusable set of anchors.
- Norma keeps armatures (geometry generators) separate from ratio packs and frame formats; keep that separation when documenting a layout.

## 5. Modulor

Le Corbusier's Modulor uses two φ series based on human height (red: … 27, 43, 70, 113, 183, 296 cm; blue: … 86, 140, 226, 366 cm). Treat it as historical proportional vocabulary, not a universal law.

## 6. Integer golden grids (Lucas, Fibonacci)

- Choose a module count that belongs to the Lucas (4, 7, 11, 18, 29) or Fibonacci (5, 8, 13, 21, 34) sequence. The two previous terms then sit near φ⁻² and φ⁻¹ of the frame.
- Example — SOLAR HUD, 18 modules of the viewport height: 2/18 secondary line, 4/18 instrument, 7/18 accessibility composition (≈ φ⁻²), 9/18 reduced clock (midpoint), 11/18 normal clock (≈ φ⁻¹), 17/18 footer line. Steps 2 → 4 → 7 → 11 grow by +2, +3, +4.
- Use the same count horizontally when it helps: margin at 1/18 of the width, columns at 7/18 and 11/18.
- Keep content rules above the grid: in SOLAR the horizon sits near the centre so the clock block at 11/18 lands on the sea and never covers the sky.

## 7. Screen grids and platform constraints

- **Units:** 8 pt spacing with a 4 pt baseline is the common screen convention; round every computed value to whole points and check device pixels.
- **Apple:** respect safe areas and layout margins (16–20 pt on iPhone), 44 × 44 pt minimum hit targets, Dynamic Type reflow, concentric corner radii on iOS 26 (inner radius = outer radius − inset).
- **Android / Material 3:** 8 dp grid, 48 × 48 dp targets, window size classes.
- **Web:** use container queries or viewport units for module sizes; never let a harmonic token create horizontal scrolling at 320–400 px width.

## 8. Choosing a grid

| Content | Grid |
| --- | --- |
| Reading, editorial | Van de Graaf ninths, 2:3 or √2 pages, baseline grid |
| Data, dashboards | rational modular grid (4:3, 5:4 fields), 8 pt spacing |
| Instrument, HUD, scientific | integer golden grid (Lucas or Fibonacci count) with one rational midpoint |
| Posters, covers | root or golden armature, rabatment lines |
| Responsive web | fluid columns plus a fixed vertical rhythm; harmonic positions only for hero sections |

