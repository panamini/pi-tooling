# Ratios Reference

Source of truth for this skill: the Norma ratio bible and the Norma formats catalog (norma.science Formats Explorer). Values are approximate to three decimals unless marked exact.

## Contents

- 1. Levels
- 2. Status and confidence
- 3. Fundamental constants
- 4. Musical intervals
- 5. Lucas and Fibonacci integers
- 6. Poussin formats
- 7. Bosshard formats
- 8. Surface presets A:B:C
- 9. Position tokens
- 10. Angles
- 11. Collisions and caution

## 1. Levels

| Level | Controls | Example |
| --- | --- | --- |
| Format / frame | width/height of the whole frame | Poussin 1.236, 1.618, 1.707 |
| Surface | split of areas `A:B:C` | 3:4:5, 1:φ:φ² |
| Position | where a cut, line, or point sits | 1/3, 1/2, 1/φ |
| Angle | orientation or crossing | 30°, 36°, 45°, 60°, 90° |
| Type step | ratio between two type sizes | 5:4, 4:3, φ |
| Spacing | ratio between gaps | Fibonacci successors |

The same number can appear at several levels with different meanings. Always state the level.

## 2. Status and confidence

| Status | Meaning |
| --- | --- |
| `coded_currently` | already used by the product |
| `observed_external` | read from a capture, artwork, or analysis |
| `candidate_to_add` | good candidate for a future pack |
| `derived_known` | derived from a known constant |
| `ambiguous` | several readings possible |
| `speculative` | weak match, intuition only |
| `do_not_use_yet` | not validated |

| Confidence | Criterion |
| --- | --- |
| `exact` | mathematical equality |
| `strong` | very small deviation, clear formula |
| `approximate` | plausible, not tight |
| `speculative` | intuition only |
| `unknown` | no known match |

Never force a ratio to make a layout look justified. A `speculative` entry never becomes an automatic constraint.

## 3. Fundamental constants

| Constant | Value | Family | Typical use |
| --- | --: | --- | --- |
| 1 | 1.000 | identity | square, pivot |
| 1/4 · 1/3 · 1/2 · 2/3 · 3/4 | 0.250 · 0.333 · 0.500 · 0.667 · 0.750 | rational | positions |
| φ | 1.618 | golden | format, surface, growth |
| 1/φ | 0.618 | golden | position, vertical format |
| φ⁻² | 0.382 | golden | position |
| φ² | 2.618 | golden | expansion |
| √2 | 1.414 | root two | format (ISO A series), surface |
| 1/√2 | 0.707 | root two | position, format |
| √3 | 1.732 | root three | triangle, angle |
| 1/√3 | 0.577 | root three | position |
| √3/2 | 0.866 | equilateral | vertical format |
| √5 | 2.236 | root five | format |
| δ = 1 + √2 | 2.414 | silver | surface, format |
| 1/δ | 0.414 | silver | position |
| α = √6/2 | 1.225 | observed family | observed only |
| π, π/φ, π/φ², πφ | 3.142, 1.942, 1.200, 5.083 | circle, circle-gold | radii, observed only |

## 4. Musical intervals

Useful for type steps and surface splits. Ratios are exact.

| Interval | Ratio | Value |
| --- | --- | --: |
| minor second | 16:15 | 1.067 |
| major second | 9:8 | 1.125 |
| minor third | 6:5 | 1.200 |
| major third | 5:4 | 1.250 |
| perfect fourth | 4:3 | 1.333 |
| tritone (augmented fourth) | √2 | 1.414 |
| perfect fifth | 3:2 | 1.500 |
| minor sixth | 8:5 | 1.600 |
| major sixth | 5:3 | 1.667 |
| minor seventh | 16:9 | 1.778 |
| major seventh | 15:8 | 1.875 |
| octave | 2:1 | 2.000 |

## 5. Lucas and Fibonacci integers

- Fibonacci: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144.
- Lucas: 2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123.
- Ratios of consecutive terms of either sequence tend to φ; ratios two steps apart tend to φ².
- On an `n`-module grid where `n` is a term, the two previous terms give golden positions in integers:

| Modules | Positions | Values | Target |
| --: | --- | --- | --- |
| 13 | 5/13, 8/13 | 0.385, 0.615 | φ⁻², φ⁻¹ |
| 18 | 7/18, 11/18 | 0.389, 0.611 | φ⁻², φ⁻¹ |
| 21 | 8/21, 13/21 | 0.381, 0.619 | φ⁻², φ⁻¹ |
| 29 | 11/29, 18/29 | 0.379, 0.621 | φ⁻², φ⁻¹ |
| 34 | 13/34, 21/34 | 0.382, 0.618 | φ⁻², φ⁻¹ |

Smaller grids are coarser but easier to perceive; 18 adds the exact midpoint 9/18.

## 6. Poussin formats

Frame ratios width/height (`aspectRatioRules`, never surface presets). Norma IDs: horizontal `poussin-h-01` … `h-10`, vertical `poussin-v-01` … `v-07`.

| Value | Reading | Confidence |
| --: | --- | --- |
| 0.353 | 1/(2√2) | strong |
| 0.618 | 1/φ | strong |
| 0.707 | 1/√2 | strong |
| 0.764 | 2/φ² | strong |
| 0.796 | √(2/π) = 0.798 | approximate |
| 0.809 | φ/2 | strong |
| 0.828 | 2/(1+√2) | strong |
| 1 | square | exact |
| 1.236 | 2/φ | strong |
| 1.309 | φ²/2 | strong |
| 1.325 | no canonical match | unknown |
| 1.353 | 1 + 1/(2√2) | strong |
| 1.382 | 1 + φ⁻² | strong |
| 1.414 | √2 | strong |
| 1.5 | 3:2 | exact |
| 1.618 | φ | strong |
| 1.707 | 1 + 1/√2 | strong |
| 2 | 2:1 | exact |

Reciprocal pairs: 0.618 ↔ 1.618, 0.707 ↔ 1.414, 0.764 ↔ 1.309, 0.809 ↔ 1.236. Observed corpus density: verticals mostly 0.70–0.87, horizontals mostly 1.236–1.707.

## 7. Bosshard formats

The 24 regular rectangles of the Bosshard plate (Norma IDs `bosshard-01` … `bosshard-24`, native portrait, ratio long:short). Readings marked `—` are plate values with no canonical reading asserted.

| # | Ratio | Reading | # | Ratio | Reading |
| --: | --: | --- | --: | --: | --- |
| 1 | 1 | square | 13 | 1.618 | φ |
| 2 | 1.118 | √5/2 | 14 | 1.667 | 5:3 |
| 3 | 1.155 | 2/√3 | 15 | 1.732 | √3 |
| 4 | 1.207 | (1+√2)/2 | 16 | 2 | double square |
| 5 | 1.236 | 2/φ | 17 | 2.236 | √5 |
| 6 | 1.25 | 5:4 | 18 | 2.309 | 4/√3 |
| 7 | 1.333 | 4:3 | 19 | 2.414 | 1 + √2 (silver) |
| 8 | 1.376 | ≈ tan 54° (pentagon), approximate | 20 | 2.449 | √6 |
| 9 | 1.414 | √2 | 21 | 2.5 | 5:2 |
| 10 | 1.454 | — | 22 | 2.646 | √7 |
| 11 | 1.5 | 3:2 | 23 | 2.828 | 2√2 |
| 12 | 1.539 | — | 24 | 3 | triple square |

## 8. Surface presets A:B:C

Convert with `A% = A / (A+B+C)`. Families present in Norma: balanced (1:1:1, 2:3:3, 3:4:4, 4:5:6), arithmetic (1:2:3, 2:3:4, 3:4:5, 4:5:6), Fibonacci (2:3:5, 3:5:8, 5:8:13, 8:13:21), golden (1:φ:φ², φ:φ²:φ³, 1:φ²:φ³), golden squared (1:φ²:φ⁴, φ²:φ³:φ⁴, 1:(1+φ):(1+φ)²), root two (1:√2:2, 1:2:2√2, √2:2:2√2), silver (1:δ:δ², δ:δ²:δ³, 1:2:δ²), geometric (1:2:4, 1:3:9, 2:4:8, 3:6:9), musical (2:3:4, 3:4:5, 4:5:6, 8:9:12), experimental (1:4:7, 2:5:11, 5:7:12, 7:11:18). Not all are harmonic in a strict sense; some are arithmetic or art-directional.

## 9. Position tokens

| Token | Value | Family |
| --- | --: | --- |
| quarter | 0.250 | rational |
| third | 0.333 | rational |
| phi-left | 0.382 | golden (φ⁻²) |
| silver-left | 0.414 | silver (1/δ) |
| half | 0.500 | midpoint |
| sqrt3 | 0.577 | root three (1/√3) |
| phi | 0.618 | golden (1/φ) |
| two-thirds | 0.667 | rational |
| sqrt2 | 0.707 | root two (1/√2) |
| three-quarters | 0.750 | rational |

A token can be cartesian (fraction of an axis) or perimetric (fraction of the frame's perimeter). Keep the context.

## 10. Angles

Common harmonic angles: 30°, 36° and 72° (pentagon, golden), 45°, 54°, 60° (equilateral), 90°. The diagonal of a φ rectangle makes ≈ 31.7° with the long side; of a √2 rectangle ≈ 35.3°; of a 3:2 rectangle ≈ 33.7°.

## 11. Collisions and caution

- Close constants collide: 1.25 (5:4) vs 1.236 (2/φ) vs 1.225 (√6/2); 1.333 (4:3) vs 1.309 (φ²/2); 1.6 (8:5) vs 1.618 (φ) vs 1.667 (5:3). State the deviation and keep the simplest reading that the construction supports.
- Rounding to screen points can move a value across a collision; report the rendered ratio, not the intended one.
- Perception studies do not support a universal preference for φ. Use ratios for coherence and repeatability, not as proof of beauty.

