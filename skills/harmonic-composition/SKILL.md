---
name: harmonic-composition
description: Compose interfaces, pages, HUDs, and frames with harmonic proportions — formats, modular and Lucas/Fibonacci grids, position tokens, type scales, and spacing derived from φ, root rectangles, musical intervals, Poussin and Bosshard formats, and classical page canons. Use for frontend or native UI layout (HTML/CSS, SwiftUI, UIKit), typographic scales, grid systems, poster or editorial formats, auditing an existing layout's proportions, or documenting why a layout is built the way it is. Do not use for pure color or brand-voice work, for imposing a ratio against legibility or platform rules, or for numerology claims about beauty.
---

# Harmonic Composition

Build layouts whose proportions are chosen, named, and verifiable — never decorative numerology. A harmonic system is a small set of related ratios that governs frame, position, type, and spacing, so every measurement has a reason and the whole reads as one instrument.

Respond in the user's language. Keep ratio names, tokens, and code identifiers unchanged.

## Load only the reference needed

- Ratio families, constants, Poussin and Bosshard formats, surface presets, positions, angles, statuses: [references/ratios.md](references/ratios.md)
- Grids and canons (Müller-Brockmann, Van de Graaf/Tschichold, root rectangles, dynamic symmetry, Modulor, Lucas/Fibonacci integer grids, screen grids): [references/grids-and-canons.md](references/grids-and-canons.md)
- Type scales and spacing (modular scales, double-stranded scales, platform text styles, baseline, figures): [references/type-and-spacing.md](references/type-and-spacing.md)
- Implementation and verification (CSS, SwiftUI, guides overlay, tolerance checks, worked SOLAR example): [references/recipes.md](references/recipes.md)

Do not load every reference by default.

## Principles

1. **Legibility and platform rules win.** Safe areas, minimum hit targets (44 pt on iOS, 48 dp on Android), Dynamic Type, contrast, and readable line lengths are constraints, not inputs to negotiate with a ratio.
2. **One governing family, at most one secondary.** For example golden (positions) plus 5:4 (strong type steps). Mixing many families produces noise that only looks systematic.
3. **Separate levels.** A number means different things as a frame ratio, a surface split, a position, an angle, or a type step. Always state the level.
4. **Name the status and confidence of every ratio.** `exact`, `strong`, `approximate`, `speculative`. A `speculative` reading never becomes a constraint. Never force a ratio to make a layout look justified.
5. **Integers carry ratios.** Prefer module counts whose integer positions approximate the target (Lucas 4·7·11·18, Fibonacci 5·8·13·21) over fractional coordinates.
6. **Content decides placement.** A harmonic line that puts text over the essential image is wrong even if exact. Example: in SOLAR, the horizon sits near the middle so every HUD word rests on the sea and never covers the sky.
7. **Verify on the rendered artifact.** Overlay guides, measure positions and ratios against the target with a stated tolerance, then check legibility at the largest text size.

## Workflow

1. **Frame:** identify the real frame (device viewport and safe areas, card, poster format). Record its ratio and orientation.
2. **Family:** choose the governing family from the content's character (calm and classical → 3:2, √2, golden; dense and rational → 4:3, 5:4 modules; instrument or scientific → golden positions on an integer grid).
3. **Positions:** pick a module count and the few position tokens the layout needs (for example 2, 4, 7, 11 of 18). Assign each token a role.
4. **Type:** derive a short scale (5–9 sizes) from the body size with the family's ratios; map it to platform text styles so accessibility scaling keeps working.
5. **Spacing:** choose one spacing set (Fibonacci 2·3·5·8·13·21·34 or 4/8 multiples) and use it for every gap.
6. **Verify:** guides overlay, ratio deviation table, legibility gates (contrast, largest text size, safe areas, hit targets).
7. **Document:** list every token with its value, level, ratio reading, status, and confidence, so the system survives later edits.

## Output

When proposing or auditing a system, give:

- a token table: token · value · level · ratio reading · status/confidence · role;
- the relations that justify the system (for example `7/18 ≈ φ⁻²`, `74:59 ≈ 5:4`), with deviations;
- what is deliberately not harmonic and why (platform minimums, safe areas, optical corrections);
- implementation tokens for the target stack and a verification method.

Stop at the system the user asked for; do not redesign unrelated screens.

