# Recipes Reference

## Contents

- 1. CSS tokens
- 2. Guides overlay (web)
- 3. SwiftUI tokens
- 4. Verification
- 5. Documentation template
- 6. Anti-patterns

## 1. CSS tokens

```css
:root {
  /* type scale (px or pt equivalents) */
  --t-micro: 13px; --t-ui: 15px; --t-read: 17px; --t-fact: 22px;
  --t-large: 28px; --t-hook: 35px; --t-display: 59px; --t-hero: 74px;
  /* spacing: Fibonacci */
  --s-2: 2px; --s-3: 3px; --s-5: 5px; --s-8: 8px; --s-13: 13px; --s-21: 21px; --s-34: 34px;
}
/* module grid inside a frame: 18 vertical modules of the frame height */
.frame { container-type: size; position: relative; }
.frame > * { --module: calc(100cqh / 18); --margin-x: calc(100cqw / 18); }
.clock { position: absolute; top: calc(var(--module) * 11); left: var(--margin-x); right: var(--margin-x); }
```

Use container query units for components; use `dvh` only for full-viewport layouts.

## 2. Guides overlay (web)

```css
.guides { position: absolute; inset: 0; pointer-events: none; display: none; }
.show-guides .guides { display: block; }
.guides .line { position: absolute; left: 0; right: 0; border-top: 1px solid rgb(120 205 255 / .6); }
```

Render one `.line` per position token with a label `k/n · role`. Ship the toggle in review builds only.

## 3. SwiftUI tokens

```swift
enum HarmonicGrid {
    static let modules: CGFloat = 18
    static func y(_ module: CGFloat, in height: CGFloat) -> CGFloat {
        (height * module / modules).rounded()
    }
    static func marginX(in width: CGFloat) -> CGFloat {
        max(16, (width / modules).rounded())
    }
}

enum HarmonicSpacing {
    static let micro: [CGFloat] = [2, 3, 5]
    static let macro: [CGFloat] = [8, 13, 21, 34]
}

struct HarmonicType {
    @ScaledMetric(relativeTo: .largeTitle) var hero: CGFloat = 74
    @ScaledMetric(relativeTo: .title) var display: CGFloat = 59
    @ScaledMetric(relativeTo: .title2) var fact: CGFloat = 22
    @ScaledMetric(relativeTo: .body) var reading: CGFloat = 17
    @ScaledMetric(relativeTo: .subheadline) var ui: CGFloat = 15
    @ScaledMetric(relativeTo: .footnote) var micro: CGFloat = 13
}
```

Place with `GeometryReader` or a custom `Layout`; keep safe areas and the largest Dynamic Type size inside the rules (fall back to a compact layout before text crosses a content boundary such as a horizon).

## 4. Verification

1. Capture the rendered screen at fixed fixtures (time, data, locale).
2. Overlay guides and measure each token's rendered position and each type pair's rendered ratio.
3. Fill a deviation table: token · target · measured · deviation % · status.
4. Run legibility gates: text contrast from rendered pixels (WCAG 2.2 AA 4.5:1, 3:1 for large text and essential non-text marks), largest accessibility text size without truncation or overlap, hit targets, safe areas.
5. A harmonic token that fails a legibility gate is changed, not the gate.

## 5. Documentation template

```markdown
## Harmonic system — <product / screen>

| Token | Value | Level | Reading | Status · confidence | Role |
| --- | --- | --- | --- | --- | --- |
| clock-top | 11/18 | position | ≈ φ⁻¹ (0.611 vs 0.618) | coded_currently · strong | normal clock block |

### Relations
- 7/18 ↔ 11/18 ≈ golden pair (Lucas 4, 7, 11, 18)

### Deliberate exceptions
- 11 pt used only for rail labels (platform minimum, not a harmonic step)

### Verification
- capture fixtures, deviation table, legibility gates
```

## 6. Anti-patterns

- Forcing a ratio after the fact to justify a layout.
- Mixing more than two families on one screen.
- Letting a harmonic position put text over essential imagery.
- Ignoring Dynamic Type: a perfect grid at default size that breaks at the largest size is not a system.
- Sub-pixel tokens: always round to whole points or device pixels and report the rendered value.
- Golden-ratio mysticism in product copy or design rationale.

