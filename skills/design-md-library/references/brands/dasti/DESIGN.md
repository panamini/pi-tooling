# dasti Design System (2026 Elite)

> **Brand one-liner:** Editorial calm. Document as hero. Chrome disappears so the writing breathes.

dasti is an AI-assisted cover-letter and resume builder (internally "Neyssan"). Its design system is tuned for people staring at a blank page, trying to tell their career story clearly. Every decision biases the eye toward the document — the chrome recedes, the paper commands attention, and the accents are quiet enough to live with for hours.

---

## 1. Brand Voice & Visual Theme

### 1.1 What dasti is not

dasti is not cinematic. There are no hero videos, no gradients across giant product shots, no stacked marketing sections. Where Apple's system optimizes for product showcase, dasti's optimizes for **workspace** — a surface the user returns to every day to write, revise, and export documents that matter.

### 1.2 Core atmosphere

- **Editorial, not promotional.** Type choices borrow from print (Fraunces on the document, Geist on the chrome). Margins are generous. Headings don't shout.
- **Warm-neutral in light mode, OLED-true in dark.** Light canvas is a cool gallery (`#F7F7F9`). Dark canvas is pure `#000` — no near-black — so the paper (`#faf9f5`) genuinely floats.
- **Five accents, one voice.** The palette system offers Sauge (sage green, default), Ocre (burnt umber), Pierre (stone gray-blue), Bordeaux (muted wine), and Encre (deep teal-ink). All five share the same saturation and lightness discipline so swapping palettes never breaks the rest of the system.
- **Calm, trustworthy, premium, low-friction.** No celebratory animations. No emoji in UI. No confetti. The product is a tool for serious work; it acts like one.

### 1.3 THE defining rule — Chrome vs Document boundary

This is the single most important rule in the system. Two layers, two typefaces, two different visual languages:

| Layer | Where it shows | Typeface | Feel |
|-------|----------------|----------|------|
| **Chrome** | Nav, sidebar, dialogs, toolbars, forms, card titles, settings, empty states | **Geist Variable** sans | Modern, quiet, humane app UI |
| **Document** | Resume preview, exported PDFs, resume print route, `.cv-*` selectors in templates | **Fraunces** serif (via `--font-serif-display`) | Editorial, printed, authored |

If you're ever unsure which layer you're designing for: if the element lives inside the document paper (`.cv-document-paper`, `.proposal-paper`, `[data-paper]`), it's the document layer and may use Fraunces. **Everything else is chrome and must use Geist.**

### 1.4 Audience cues

- Knowledge workers mid-career. Often bilingual, job-searching internationally.
- Using dasti on a 14"+ laptop, at a desk, for 20–90 minutes at a time.
- Reads the document more than the chrome. The chrome must disappear.

---

## 2. Color System

All colors are exposed as CSS custom properties. Tokens fall into five groups: **accent palettes** (interchangeable), **surface stack**, **text stack**, **semantic triplets**, and **borders**.

### 2.1 Accent Palettes (5 interchangeable)

Each palette sets `--ac` (solid), `--am` (mid/hover), `--ap` (pale), `--as` (soft), `--fr` (focus ring), and `--op` (on-primary text). Palettes are applied by adding `.pal-sauge`, `.pal-ocre`, `.pal-pierre`, `.pal-bordeaux`, or `.pal-encre` to `<body>`. Default is Sauge.

**Sauge (default — sage green)**

| Token | Light | Dark |
|-------|-------|------|
| `--ac` | `hsl(155, 22%, 30%)` | `hsl(155, 28%, 62%)` |
| `--am` | `hsl(155, 24%, 44%)` | `hsl(155, 28%, 72%)` |
| `--ap` | `hsl(155, 22%, 92%)` | `hsl(155, 20%, 18%)` |
| `--as` | `hsl(155, 18%, 88%)` | `hsl(155, 18%, 22%)` |
| `--fr` | `hsl(155, 22%, 56%)` | `hsl(155, 28%, 78%)` |
| `--op` | `hsl(40, 20%, 99%)` | `hsl(80, 5%, 7%)` |

**Ocre (warm earth)**

| Token | Light | Dark |
|-------|-------|------|
| `--ac` | `hsl(34, 38%, 32%)` | `hsl(34, 26%, 58%)` |
| `--am` | `hsl(34, 34%, 42%)` | `hsl(34, 28%, 68%)` |
| `--ap` | `hsl(34, 30%, 92%)` | `hsl(34, 18%, 18%)` |
| `--fr` | `hsl(34, 32%, 54%)` | `hsl(34, 28%, 74%)` |

**Pierre (stone gray-blue)**

| Token | Light | Dark |
|-------|-------|------|
| `--ac` | `hsl(220, 14%, 30%)` | `hsl(220, 14%, 62%)` |
| `--am` | `hsl(220, 14%, 42%)` | `hsl(220, 14%, 72%)` |
| `--ap` | `hsl(220, 12%, 92%)` | `hsl(220, 8%, 18%)` |

**Bordeaux (muted wine)**

| Token | Light | Dark |
|-------|-------|------|
| `--ac` | `hsl(348, 22%, 30%)` | `hsl(348, 22%, 62%)` |
| `--am` | `hsl(348, 22%, 42%)` | `hsl(348, 22%, 72%)` |

**Encre (deep teal-ink)**

| Token | Light | Dark |
|-------|-------|------|
| `--ac` | `hsl(200, 18%, 24%)` | `hsl(200, 18%, 62%)` |
| `--am` | `hsl(200, 18%, 36%)` | `hsl(200, 18%, 72%)` |

### 2.2 Surface Stack

Four elevation tiers, used consistently across both modes. Each tier is what sits above the last — never inline hex, always the token.

| Role | Token | Light | Dark | Where |
|------|-------|-------|------|-------|
| App canvas (shell) | `--bg` | `#F7F7F9` | `#000000` (OLED) | Outermost body, beyond the content frame |
| Workspace | `--sf1` | `#F3F1EC` | `#111111` | Behind panels; sidebar background |
| Panel surface / muted (inputs) | `--sf2` | `#EDE9E1` | `#161616` | `.dasti-field` default, muted cards |
| Raised / elevated | `--sfr` | `#FFFFFF` | `#1E1E1E` | Toolbars, dialogs, standard cards, popovers |
| **Paper** (document) | `--paper` | `#faf9f5` | `#faf9f5` (same) | Resume / proposal document sheet — always light |

Semantic aliases (preferred in new code):

| Alias | Resolves to |
|-------|-------------|
| `--color-canvas` | `var(--bg)` |
| `--color-surface` | `var(--sf1)` |
| `--color-surface-muted` | `var(--sf2)` |
| `--color-surface-raised` | `var(--sfr)` |
| `--color-surface-paper` | `var(--paper)` |

### 2.3 Text Stack

Three roles only. Don't invent new shades — reach for these.

| Role | Token | Light | Dark |
|------|-------|-------|------|
| Primary | `--ti` → `--color-text` | `#1F1F1C` | `#F5F3EF` |
| Muted | `--tm2` → `--color-text-muted` | `#4B4B4B` | `#C9C5BE` |
| Subtle / tertiary | `--tg2` → `--color-text-subtle` | `#7A7A7A` | `#9B978F` |
| On-primary (text on accent bg) | `--op` | palette-dependent | palette-dependent |

### 2.4 Semantic Colors (success / danger / warning)

Each semantic color ships as a triplet: **solid** (`--ok`, `--er`, `--wa`), **soft** (`-b` background), **ink** (`-t` text on soft bg).

| Token | Light | Dark |
|-------|-------|------|
| `--color-success` | `hsl(152, 20%, 28%)` | `hsl(152, 22%, 56%)` |
| `--color-success-soft` | `hsl(152, 16%, 92%)` | `hsl(152, 13%, 13%)` |
| `--color-success-ink` | `hsl(152, 20%, 22%)` | `hsl(152, 22%, 70%)` |
| `--color-danger` | `hsl(4, 26%, 34%)` | `hsl(4, 24%, 56%)` |
| `--color-danger-soft` | `hsl(4, 22%, 92%)` | `hsl(4, 15%, 13%)` |
| `--color-danger-ink` | `hsl(4, 26%, 28%)` | `hsl(4, 24%, 70%)` |
| `--color-warning` | `hsl(34, 36%, 32%)` | `hsl(36, 26%, 58%)` |
| `--color-warning-soft` | `hsl(34, 30%, 92%)` | `hsl(36, 13%, 13%)` |
| `--color-warning-ink` | `hsl(34, 36%, 26%)` | `hsl(36, 26%, 72%)` |

Note: there is no `--color-border-error` token. Error state on inputs uses `var(--color-danger)` for the 2px border and `color-mix(in srgb, var(--color-danger-soft) 35%, var(--color-surface-muted))` for the background.

### 2.5 Borders

| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `--border-soft` | `rgba(0, 0, 0, 0.08)` | `rgba(255, 255, 255, 0.08)` | Card outer, soft dividers, frost bottom |
| `--border-field` | `rgba(0, 0, 0, 0.06)` | `rgba(255, 255, 255, 0.06)` | Field dividers, subtle separators |
| `--border-strong` | `rgba(0, 0, 0, 0.12)` | `rgba(255, 255, 255, 0.12)` | Hover border, prominent dividers |
| `--border-selected` | `color-mix(in srgb, var(--ac) 45%, transparent)` | same | Selected item borders |

---

## 3. Typography

### 3.1 Chrome fonts

```css
--font-body-family: "Geist Variable", "Source Sans 3", system-ui, sans-serif;
--font-heading-family: "Geist Variable", "Source Sans 3", system-ui, sans-serif;
--font-mono-family: "IBM Plex Mono", source-code-pro, Menlo, Monaco, Consolas, monospace;
```

Both body and heading resolve to Geist. That is intentional — the chrome uses a single typeface. Hierarchy is built from size, weight, and tracking, not from font changes.

### 3.2 Document font

```css
--font-serif-display: "Fraunces", "Iowan Old Style", "Palatino Linotype",
                      "Book Antiqua", Baskerville, "Times New Roman", serif;
```

Applied **only** inside document selectors — `.cv-section-heading`, `.cv-section-title-input`, `.proposal-paper` body text, resume print route. Never on chrome.

### 3.3 Type scale (√2 from 12px base)

| Role | Size | Line-height | Token (size/line) |
|------|------|-------------|-------------------|
| Caption / overline | 12px | 16px | `--tx` / `--lx` |
| Body-sm / label | 14px | 20px | `--ts` / `--ls` |
| Body | 16px | 24px | `--tb` / `--lb` |
| Title | 20px | 30px | `--tm` / `--ll` |
| Large title | 26px | 40px (generous) | `--tl` / `--lx2` |
| Display | 32px | 40px | `--tx2` / `--lx2` |

### 3.4 Display tracking

```css
--tracking-display: -0.02em;   /* chrome titles */
--tracking-tight:   -0.01em;
--tracking-normal:  0;
--tracking-wide:    0.14em;    /* eyebrows, small-caps */
```

Apply `letter-spacing: var(--tracking-display)` to every chrome title ≥20px (modal titles, workspace headers, card titles, empty-state headlines, doc-card titles, brief-card titles). It's a small tightening that makes Geist feel more editorial.

### 3.5 Eyebrow utility

```css
.dasti-eyebrow {
  font-family: var(--font-body-family);
  font-size: 10px;
  line-height: 1;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-text-muted);
}
```

Use above titles to group or label sections. Mix tokens — `0.1em` tracking (not `0.14em wide`) because the small size needs extra air.

### 3.6 Typography role table

| Role | Family | Weight | Size | Line-h | Tracking | Layer |
|------|--------|--------|------|--------|----------|-------|
| UI body | Geist | 400 | 16px | 24px | normal | chrome |
| UI body emphasis | Geist | 600 | 16px | 24px | normal | chrome |
| UI title | Geist | 600 | 20px | 30px | -0.02em | chrome |
| UI display | Geist | 600 | 26–32px | 40px | -0.02em | chrome |
| UI label | Geist | 600 | 14px | 20px | normal | chrome |
| UI caption | Geist | 400 | 12px | 16px | normal | chrome |
| UI eyebrow | Geist | 600 | 10px | 1 | 0.1em upper | chrome |
| UI code / meta | IBM Plex Mono | 400 | 12–14px | matched | normal | chrome |
| Document heading | Fraunces | 600 | 20–28px | 1.15 | -0.01em | **document** |
| Document body | Fraunces | 400 | 11–12pt | 1.5 | normal | **document** |

---

## 4. Components

dasti's component set is the most exhaustive part of the system. Every component below uses only tokens from sections 2, 3, 5, 6, and 7 — never raw hex or magic numbers.

### 4.1 Buttons — `.dasti-button`

Base contract:

```css
.dasti-button {
  min-height: var(--control-md);            /* 40px */
  padding: 0 var(--space-4);                /* 0 16px */
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-control);     /* 12px */
  background: var(--color-surface-raised);
  color: var(--color-text);
  font-family: var(--font-body-family);
  font-size: var(--text-body-sm-size);      /* 14px */
  font-weight: 600;
  box-shadow: var(--shadow-sm);
  transition: background-color 120ms var(--ez),
              border-color 120ms var(--ez),
              box-shadow 120ms var(--ez),
              transform 120ms var(--ez);
  cursor: pointer;
}
.dasti-button:hover:not(:disabled) { transform: translateY(-1px); }
.dasti-button:disabled { opacity: 0.5; cursor: not-allowed; }
```

Variants (modifier classes):

| Modifier | Background | Text | Border | Shadow |
|----------|-----------|------|--------|--------|
| `--primary` | `var(--color-accent)` | `var(--color-on-accent)` | transparent | `--shadow-sm` |
| `--secondary` | `var(--color-surface-raised)` | `var(--color-text)` | `--color-border-strong` | `--shadow-sm` |
| `--accent` | `var(--color-accent-soft)` | `var(--color-text)` | transparent | none |
| `--ghost` | transparent | `var(--color-text-muted)` | transparent | none |
| `--danger` | `var(--color-danger-soft)` → `var(--color-danger)` on hover | `var(--color-danger-ink)` → `var(--color-on-accent)` | transparent | none |
| `--pill` | (same as base variant) | (same) | (same) | (same) — sets `border-radius: 999px` |

Sizes:

| Modifier | min-height | padding |
|----------|-----------|---------|
| `--sm` | 32px | 0 12px |
| (default) | 40px | 0 16px |
| `--lg` | 44px | 0 24px |

**Primary CTA rule:** on any given screen, only **one** `.dasti-button--primary` should exist. The proposal Generate button is the canonical primary. Everything else is `--secondary`, `--accent`, `--ghost`, or `--danger`.

### 4.2 Icon buttons — `.dasti-icon-button`

```css
.dasti-icon-button {
  width: 32px;
  height: 32px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-control);     /* 12px */
  background: var(--color-surface-raised);
  color: var(--color-text-muted);
  box-shadow: var(--shadow-sm);
  transition: background-color 120ms var(--ez),
              border-color 120ms var(--ez),
              color 120ms var(--ez);
}
.dasti-icon-button:hover {
  background: var(--color-surface-muted);
  border-color: var(--color-border-strong);
  color: var(--color-text);
}
```

Modifiers:
- `--bare` — no border, no background, no shadow. Pure glyph in a hit target.
- `--confirm` — red confirm state: `background: var(--color-danger-soft); color: var(--color-danger-ink);` → on hover, `background: var(--color-danger); color: var(--color-on-accent);`.

Always pair with an accessible `aria-label` and (ideally) a tooltip.

### 4.3 Inputs — THE SUBTLE-FILL PATTERN (dasti hallmark)

**This is the most distinctive pattern in the entire system.** dasti inputs never show a focus glow. The border quietly changes from transparent to `--color-text` on focus. Background and shadow never change.

```css
.dasti-field, .dasti-select, .inputElement, .jobField {
  background: var(--color-surface-muted);   /* sf2 */
  border: 2px solid transparent;
  border-radius: var(--radius-control);     /* 12px */
  padding: 0 var(--space-3);                /* 0 12px */
  min-height: var(--control-md);            /* 40px */
  font-family: var(--font-body-family);
  font-size: var(--text-body-size);         /* 16px */
  color: var(--color-text);
  box-shadow: none;
  transition: border-color 120ms var(--ez);
}
.dasti-field:focus, .dasti-select:focus {
  outline: none;
  border-color: var(--color-text);          /* the one change */
  box-shadow: none;                         /* NO glow */
}
.dasti-field[aria-invalid="true"], .dasti-field.is-error {
  border-color: var(--color-danger);
  background: color-mix(in srgb, var(--color-danger-soft) 35%, var(--color-surface-muted));
}
.dasti-field:disabled { opacity: 0.5; cursor: not-allowed; }
```

Rules:
- Border is always 2px — even at rest (transparent). Never jump from 1px to 2px.
- Never add `box-shadow` on focus (no glow, no ring).
- Placeholder uses `color: var(--color-text-subtle)`.
- Error background uses the `color-mix` above; don't hardcode a tint.

### 4.4 Pills & Badges — `.dasti-pill`

```css
.dasti-pill {
  height: 28px;
  padding: 0 var(--space-2);                /* 0 8px */
  border: 1px solid var(--color-border);
  border-radius: var(--radius-pill);        /* 999px */
  background: var(--color-surface);
  color: var(--color-text-muted);
  font-size: var(--text-caption-size);      /* 12px */
  font-weight: 600;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
}
```

Variants share the pattern: soft bg + ink text + transparent border.

| Modifier | Background | Text |
|----------|-----------|------|
| `--accent` | `var(--color-accent-soft)` | `var(--color-text)` |
| `--success` | `var(--color-success-soft)` | `var(--color-success-ink)` |
| `--warning` | `var(--color-warning-soft)` | `var(--color-warning-ink)` |
| `--danger` | `var(--color-danger-soft)` | `var(--color-danger-ink)` |

### 4.5 Tone Badges (proposal-specific)

Used inside `.dasti-proposal-tone-badge` to label a proposal's voice. Three flavors, each a semantic pair:

| Tone | Background | Text |
|------|-----------|------|
| **Warm** | `var(--color-warning-soft)` | `var(--color-warning-ink)` |
| **Formal** | `var(--color-accent-soft)` (or Pierre accent soft) | `var(--color-text)` |
| **Natural** | `var(--color-surface-muted)` | `var(--color-text-muted)` |

Compact modifier reduces padding to `2px 6px` and caps size at 12px.

### 4.6 Cards — `.dasti-card`

```css
.dasti-card {
  padding: var(--space-4);                  /* 16px */
  border-radius: var(--radius-card);        /* 16px */
  border: 1px solid var(--color-border);
  background: var(--color-surface-raised);
  box-shadow: var(--shadow-sm);
  transition: background-color 120ms var(--ez),
              border-color 120ms var(--ez),
              box-shadow 120ms var(--ez),
              transform 120ms var(--ez);
}
.dasti-card--muted      { background: var(--color-surface); }
.dasti-card--elevated   { box-shadow: var(--shadow-md); }
.dasti-card--interactive:hover {
  border-color: var(--color-border-strong);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}
.dasti-card--sm { padding: var(--space-3); }
.dasti-card--lg { padding: var(--space-5); }
```

**Anti-pattern:** never stack `.dasti-card` inside another `.dasti-card` inside another. The system only supports **two** surface tiers visible at once. If you need nesting, use dividers (`border-bottom: 1px solid var(--border-field)`), not cards.

### 4.7 Sidebar Nav Items — `.sb-nav-item`

```css
.sb-nav-item {
  min-height: 36px;
  padding: 0 8px;
  border-radius: var(--radius-control);     /* 12px */
  background: transparent;
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  transition: background 150ms ease-out, color 150ms ease-out;
}
.sb-nav-item:hover {
  background: var(--sidebar-hover-bg);      /* sf2 light / gradient dark */
  color: var(--color-text);
}
.sb-nav-item--active {
  background: var(--sidebar-active-bg);
  color: var(--color-text);
  box-shadow: inset 2px 0 0 var(--ac);      /* THE left accent stripe */
}
```

Rules:
- Active item is recognized by the **2px left inset stripe**, not by a filled background alone. The raised bg is softer than a pure accent fill would be.
- No outer border.
- No drop shadow.
- Section labels above nav items use the eyebrow utility: 10px / 600 / 0.1em / uppercase / `color-text-subtle`.
- Count badges on nav items right-align as a pill: `.sb-count-badge` — 11px, `sf2` bg, `tm2` text, 999 radius, `1px 6px` padding.

### 4.8 Frost Panels — `.dasti-frost`

Used for modal headers, floating toolbars, and sticky headers over document content.

```css
.dasti-frost {
  background: var(--frost-bg);
  backdrop-filter: saturate(var(--frost-saturate)) blur(var(--frost-blur));
  -webkit-backdrop-filter: saturate(var(--frost-saturate)) blur(var(--frost-blur));
  border-bottom: 1px solid var(--color-border);
}
```

Tokens:

| Token | Light | Dark |
|-------|-------|------|
| `--frost-bg` | `hsla(38, 22%, 96%, 0.88)` | `hsla(0, 0%, 12%, 0.82)` |
| `--frost-surface` | `hsla(38, 22%, 96%, 0.74)` | `hsla(0, 0%, 12%, 0.7)` |
| `--frost-blur` | `18px` | `18px` |
| `--frost-saturate` | `140%` | `130%` |

Rules:
- Always pair frost with a backdrop-filter fallback (`-webkit-`).
- Don't nest frost inside frost — one layer only, at the top.
- Use frost only where content scrolls behind it.

### 4.9 Document Paper (resume & proposal sheets)

The paper is the hero of the system. Chrome retreats; the paper advances.

```css
.cv-document-paper, .proposal-paper, [data-paper] {
  --document-sheet-inline-size: 560px;
  --document-sheet-ratio: 1 / 1.41421356;   /* A4 */
  width: var(--document-sheet-inline-size);
  aspect-ratio: var(--document-sheet-ratio);
  background: var(--paper);                 /* #faf9f5 — both modes */
  border-radius: 4px;                       /* --document-paper-radius */
  box-shadow: var(--document-paper-shadow);
  font-family: var(--font-serif-display);   /* Fraunces */
  color: var(--color-text);
}
```

Paper shadow (dark-mode hero — this is what sells the floating paper):

```css
--document-paper-shadow: 0 4px 24px rgba(0, 0, 0, 0.40),
                         0 1px 2px rgba(0, 0, 0, 0.80);
```

Stage around the paper:

```css
.cv-preview-stage, .proposal-output-stage {
  padding: 32px;                            /* minimum breathing room */
  border-radius: 10px;                      /* --document-stage-radius */
  background: var(--color-surface);
}
```

### 4.10 Surface Panels — `.dasti-panel` / `.dasti-surface-panel`

Larger containers for grouped content (settings sections, compose columns, preview wrappers):

```css
.dasti-panel {
  border-radius: var(--radius-surface);     /* 20px */
  border: 1px solid var(--color-border);
  background: var(--gradient-surface);
  box-shadow: var(--shadow-sm);
  padding: var(--space-5);                  /* 24px */
  display: grid;
  gap: var(--space-4);
}
```

### 4.11 Dialog / Modal

```css
.dasti-dialog {
  border-radius: var(--radius-surface);     /* 20px */
  background: var(--color-surface-raised);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}
.dasti-dialog-header {
  background: var(--frost-bg);
  backdrop-filter: saturate(var(--frost-saturate)) blur(var(--frost-blur));
  border-bottom: 1px solid var(--color-border);
  padding: var(--space-4) var(--space-5);
  position: sticky;
  top: 0;
}
.dasti-dialog-title {
  font-family: var(--font-body-family);
  font-weight: 600;
  font-size: var(--text-title-size);        /* 20px */
  letter-spacing: var(--tracking-display);
}
```

### 4.12 Import Warning Banner

Surfaces automatic parser signals (e.g. `cv-import-signals.ts`).

```css
.dasti-import-warning {
  background: var(--color-warning-soft);
  border: 1px solid color-mix(in srgb, var(--color-warning) 35%, transparent);
  border-radius: var(--radius-control);     /* 12px */
  padding: 10px 14px;
  color: var(--color-warning-ink);
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 10px;
}
```

---

## 5. Layout & Spacing

### 5.1 Spacing scale

dasti uses a canonical 4·8·12·16·24·32·40·64·80 scale. Always use tokens — never inline pixels.

| Token | Value | Alias |
|-------|-------|-------|
| `--s1` | 4px | `--space-1` |
| `--s2` | 8px | `--space-2` |
| `--s3` | 12px | `--space-3` |
| `--s4` | 16px | `--space-4` |
| `--s5` | 24px | `--space-5` |
| `--s6` | 32px | `--space-6` |
| `--s7` | 40px | `--space-7` |
| `--s8` | 64px | `--space-8` |
| `--s9` | 80px | `--space-9` |

### 5.2 Control heights

| Token | Value | Use |
|-------|-------|-----|
| `--hs` / `--control-sm` | 32px | Small buttons, icon buttons, pills |
| `--hm` / `--control-md` | 40px | Default button, input, tab bar |
| `--hb` / `--control-lg` | 44px | Large CTA |
| `--hdr` / `--header-height` | 54px | App header |

Sidebar-specific:

| Token | Value |
|-------|-------|
| `--app-sidebar-item-height` | 36px (expanded) |
| `--app-sidebar-item-height-compact` | 34px |
| `--app-sidebar-action-height` | 30px |

### 5.3 Radii

| Token | Value | Where |
|-------|-------|-------|
| `--radius-1` / `--radius-inline` | 8px | Tight chips, inline tags |
| `--radius-2` / `--radius-control` | 12px | Buttons, inputs, cards (control size) |
| `--radius-3` / `--radius-card` | 16px | Cards, grouped surfaces |
| `--radius-4` / `--radius-surface` | 20px | Panels, dialogs, large containers |
| `--radius-pill` | 999px | Pills, count badges |

Document exceptions (intentional):

| Token | Value | Where |
|-------|-------|-------|
| `--document-paper-radius` | 4px | Paper corners (near-sharp, print-like) |
| `--document-stage-radius` | 10px | Stage around paper |

### 5.4 Container padding

| Token | Value | Use |
|-------|-------|-----|
| `--container-pad-sm` | 16px | Mobile, compact surfaces |
| `--container-pad-md` | 24px | Default workspace padding |
| `--container-pad-lg` | 32px | Document stages, hero sections |

### 5.5 Flow spacing (em-based)

```css
--flow-1: 0.375em;
--flow-2: 0.5em;
--flow-3: 0.75em;
--flow-4: 1em;
--flow-5: 1.5em;
```

Use these inside document bodies (Fraunces), where rhythm should scale with font-size.

### 5.6 Split layouts

The signature dasti layout is a two-pane editor + preview.

| Breakpoint | Editor | Preview | Behavior |
|-----------|--------|---------|----------|
| ≥1280px | 56% | 44% | Side-by-side, both visible |
| 1024–1279px | 100% | hidden (preview button) | Stacked |
| <1024px | 100% | full-screen toggle | Mobile |

At ≥1280px, `--document-sheet-inline-size` must render at ≥360px inside the preview pane.

### 5.7 Z-index scale

| Token | Value | Role |
|-------|-------|------|
| `--z-base` | 0 | Default |
| `--z-sticky` | 100 | Sticky headers, topbar |
| `--z-popover` | 400 | Popovers, dropdowns |
| `--z-modal` | 800 | Modals, dialogs |
| `--z-toast` | 900 | Toast notifications |
| `--z-tooltip` | 1000 | Tooltips (topmost) |

---

## 6. Depth, Elevation, Frost

### 6.1 Shadow tiers (light mode — layered hsla warm)

```css
--sha: 0 1px 2px hsla(30, 20%, 8%, 0.04),
       0 5px 12px hsla(30, 20%, 8%, 0.036);            /* shadow-sm */

--shb: 0 2px 5px hsla(30, 20%, 8%, 0.052),
       0 8px 20px hsla(30, 20%, 8%, 0.06);             /* shadow-md */

--shc: 0 6px 16px hsla(30, 20%, 8%, 0.068),
       0 22px 46px hsla(30, 20%, 8%, 0.10);            /* shadow-lg */

--shadow-frost: 0 8px 20px -18px hsla(30, 20%, 8%, 0.26),
                0 2px 5px -4px hsla(30, 20%, 8%, 0.09);
```

### 6.2 Shadow tiers (dark mode — rgba black, heavier to hold the paper)

```css
--sha: 0 4px 24px rgba(0, 0, 0, 0.40),
       0 1px 2px rgba(0, 0, 0, 0.80);

--shb: 0 6px 32px rgba(0, 0, 0, 0.48),
       0 2px 4px rgba(0, 0, 0, 0.72);

--shc: 0 12px 48px rgba(0, 0, 0, 0.56),
       0 4px 8px rgba(0, 0, 0, 0.64);

--shadow-frost: 0 14px 34px hsla(0, 0%, 0%, 0.32);
```

**Dark-mode rule:** on raised surfaces (cards, panels), replace soft drop shadows with an **inset highlight**:

```css
.dark .dasti-card {
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.06);
}
```

This keeps the OLED canvas truly black while still separating surface from canvas.

### 6.3 Frost

Already defined in 4.8. Two rules worth restating here:

1. Frost is a **layer type**, not a decoration. Use it only where content is expected to scroll behind.
2. Dark-mode saturate is **130%**, not 140%. Dark environments amplify saturation — pulling it back prevents frost from looking neon.

### 6.4 Focus ring

```css
--focus-ring: 3px;
--focus-shadow-soft: 0 0 0 2px color-mix(in srgb, var(--fr) 58%, transparent);
```

The soft shadow ring is used on:
- Icon buttons (`:focus-visible` → inset border)
- Buttons (`:focus-visible` → outline with accent)
- Selectable cards
- Radio / checkbox primitives

**Exception — subtle-fill inputs do NOT use the soft ring.** They swap border from `transparent` → `--color-text` (see 4.3). The ring would compete with the border. This is the deliberate signature.

---

## 7. Motion

### 7.1 Easing

```css
--ez:  cubic-bezier(0.25, 0.1, 0.25, 1);      /* standard */
--ezb: cubic-bezier(0.34, 1.56, 0.64, 1);     /* bounce (sparingly) */

/* Proposal composer (enter/exit pairs) */
--proposal-motion-ease-enter: cubic-bezier(0.22, 1, 0.36, 1);
--proposal-motion-ease-exit:  cubic-bezier(0.4, 0, 0.2, 1);
```

### 7.2 Durations

```css
--duration-fast:   120ms;     /* hover, border swap, subtle-fill focus */
--duration-normal: 180ms;     /* default */
--duration-panel:  250ms;     /* panel open/close */
--duration-slow:   240ms;     /* preview resize */
```

### 7.3 Proposal toolbar motion

```
Enter: 320ms, shift -10px, scale 0.96, saturate 0.94, blur 6px → 0
Exit:  160ms, shift  -8px, scale 0.97, saturate 0.95, blur 5px
```

### 7.4 Brief (length slider) choreography

```
Swap:   160ms
Settle: 260ms
Enter:  260ms (shift 10px, scale 0.97, saturate 0.95, blur 6px)
Exit:   160ms (shift 8px)
```

### 7.5 Submit button

- Surface reveal: 380ms, `cubic-bezier(0.2, 0.8, 0.2, 1)`
- State change: 220ms
- Spinner loop: 1450ms per rotation
- Stroke draw: 1080ms

### 7.6 Default transition property set

For interactive surfaces, transition exactly these four properties — no more:

```css
transition: background-color 120ms var(--ez),
            border-color 120ms var(--ez),
            box-shadow 120ms var(--ez),
            transform 120ms var(--ez);
```

Do not transition `all`. Do not transition `color` unless the element explicitly needs it (some pills do). Never transition `width` or `height` in flowing content.

---

## 8. Do's & Don'ts

**DO**

- Treat the document as the visual hero. Whitespace around the paper is as important as the paper itself.
- Use soft frost for overlays. Blur 18px + saturate 140%/130%.
- Signal active sidebar items with the **2px left inset stripe**, not a filled background.
- Use Geist for chrome and Fraunces for document body — and nothing else.
- Use the subtle-fill input pattern (2px transparent → 2px text on focus, no glow).
- Ship with `#faf9f5` paper in both modes — it's the one warm surface that persists across light and dark.
- Tighten chrome titles with `letter-spacing: -0.02em`.
- Default to the Sauge palette unless the user explicitly switches.

**DON'T**

- Don't stack cards inside cards inside cards. Max two visible surface tiers.
- Don't use heavy drop shadows in dark mode. Replace with `inset 0 0 0 1px rgba(255,255,255,0.06)`.
- Don't use Fraunces in chrome. It belongs to the document.
- Don't add a focus glow ring to subtle-fill inputs — the border swap *is* the focus signal.
- Don't use pure white (`#FFFFFF`) for a background. Use `--sfr` (light: `#FFFFFF`, dark: `#1E1E1E`) as surface-raised, or `--paper` (`#faf9f5`) for document surfaces. The canvas itself is `#F7F7F9` or `#000`.
- Don't promote more than one primary button per screen.
- Don't animate `all` or `width`/`height`. Stick to the 4-property set in 7.6.
- Don't hardcode hex values in components. Always use the semantic token.
- Don't use emoji in UI chrome. Icons only.

---

## 9. Responsive

| Breakpoint | Behavior |
|-----------|----------|
| ≥1280px | Split editor/preview, sidebar expanded, all chrome visible |
| 1024–1279px | Sidebar expanded; preview collapses behind a "Preview" button |
| 768–1023px | Sidebar collapses to icon strip; preview hidden by default |
| <768px | Sidebar becomes a sheet/drawer; full-width content; touch targets ≥40px |

Always keep:
- Tap targets ≥40px square on touch.
- Readable paper at ≥320px inline size.
- Subtle-fill inputs at min-height 40px even on mobile.
- Topbar height fixed at 54px.

---

## 10. Light ↔ Dark Translation

Full token translation table. If a token isn't listed, it does not change between modes.

| Token | Light | Dark |
|-------|-------|------|
| `--bg` (canvas) | `#F7F7F9` (cool gallery) | `#000000` (OLED) |
| `--sf1` | `#F3F1EC` | `#111111` |
| `--sf2` | `#EDE9E1` | `#161616` |
| `--sfr` | `#FFFFFF` | `#1E1E1E` |
| `--paper` | `#faf9f5` | `#faf9f5` (unchanged) |
| `--ti` / `--color-text` | `#1F1F1C` | `#F5F3EF` |
| `--tm2` / `--color-text-muted` | `#4B4B4B` | `#C9C5BE` |
| `--tg2` / `--color-text-subtle` | `#7A7A7A` | `#9B978F` |
| `--border-soft` | `rgba(0,0,0,0.08)` | `rgba(255,255,255,0.08)` |
| `--border-field` | `rgba(0,0,0,0.06)` | `rgba(255,255,255,0.06)` |
| `--border-strong` | `rgba(0,0,0,0.12)` | `rgba(255,255,255,0.12)` |
| Accent `--ac` (Sauge) | `hsl(155,22%,30%)` | `hsl(155,28%,62%)` |
| `--fr` (focus) | `hsl(155,22%,56%)` | `hsl(155,28%,78%)` |
| `--op` (on-accent) | `hsl(40,20%,99%)` | `hsl(80,5%,7%)` |
| `--frost-bg` | `hsla(38,22%,96%,0.88)` | `hsla(0,0%,12%,0.82)` |
| `--frost-saturate` | `140%` | `130%` |
| `--sha` | layered hsla warm (low alpha) | rgba black (high alpha) |
| Raised card shadow strategy | `--shadow-sm` drop shadow | `inset 0 0 0 1px rgba(255,255,255,0.06)` |

Switching modes is done by toggling `.dark` on `<html>`. All tokens flip in one transaction.

**Critical dark-mode rule:** OLED canvas is **pure `#000`**. Anything in the `#0D–#18` range is wrong. Surface tiers step up to `#111 → #161616 → #1E1E1E`. This creates a genuine floating-paper effect.

---

## 11. Agent Prompt Guide

Use these recipes when generating dasti-flavored UI with an LLM. Each emphasizes semantic tokens and the chrome/document boundary.

### 11.1 Recipes

**New page (chrome)**
> Generate a dasti page. Use `var(--color-canvas)` as body background. Sidebar: `sb-nav-item` pattern, active item gets `box-shadow: inset 2px 0 0 var(--ac)`. Topbar: 54px, frost bg, breadcrumb uses body + `letter-spacing: var(--tracking-display)`. Main content: grid with `gap: var(--space-5)`. All typography Geist — never Fraunces in chrome.

**New card**
> Create a `.dasti-card` with 16px radius, 16px padding, `var(--color-surface-raised)` bg, 1px `var(--color-border)` border, `var(--sha)` shadow. Title uses Geist 20px/600 with `-0.02em` tracking. Body uses Geist 14px/400 in `var(--color-text-muted)`. On hover: lift -1px, `var(--shb)` shadow, `var(--color-border-strong)` border. No nested cards.

**New modal**
> Build a dialog: 20px radius, `var(--color-surface-raised)` body, `var(--shc)` shadow. Header uses frost (`var(--frost-bg)` + `backdrop-filter: saturate(140%) blur(18px)`), sticky top, 1px bottom `var(--color-border)`. Title is 20px Geist 600 with `-0.02em` tracking. Body padding 24px. Footer buttons: one `.dasti-button--primary`, others `--ghost`.

**New form**
> All inputs use the subtle-fill pattern: `background: var(--color-surface-muted)`, `border: 2px solid transparent`, 12px radius, min-height 40px. On focus, swap border to `var(--color-text)` — no box-shadow. Error state: `border-color: var(--color-danger)`, bg `color-mix(in srgb, var(--color-danger-soft) 35%, var(--color-surface-muted))`. Labels use 14px/600 Geist above the field. No focus glow rings anywhere.

**New empty state**
> Centered block with 24px gap. Headline: Geist 20px/600, `-0.02em` tracking, `var(--color-text)`. Body sentence: Geist 14px/400, `var(--color-text-muted)`, max-width 44ch. One `.dasti-button--primary` as the single CTA; optional `.dasti-button--ghost` secondary below.

**New document surface (resume / proposal)**
> Wrap the content in `.dasti-preview-stage` with 32px padding and `var(--color-surface)` bg. Inside, the paper: `width: 560px; aspect-ratio: 1/1.41421356; background: var(--paper); border-radius: 4px; box-shadow: var(--document-paper-shadow); font-family: var(--font-serif-display)`. Fraunces is ONLY allowed inside this paper element.

### 11.2 Sample prompts (copy-paste ready)

> Design a dasti `/letters` library page. Grid of cover-letter cards (`.dasti-card--interactive`), 3 cols on wide, 1 col on mobile. Each card shows: tone badge (color-coded), company + role title (Geist 16px/600), 2-line snippet (Geist 14px/400 muted, skip "Dear Hiring Manager"), date (12px subtle). Top toolbar: search input (subtle-fill), sort dropdown (subtle-fill), `+ New letter` primary button right-aligned.

> Generate a dasti proposal composer screen. Left rail: job description source panel, subtle-fill textarea, 14px body, 68ch max. Center: floating toolbar (frost, 12px radius, `var(--shb)` shadow) above the paper. Right: proposal document paper (560×A4, Fraunces, `#faf9f5`, 4px radius, paper shadow, 32px stage padding). Primary Generate button in the toolbar is the only filled CTA.

> Create a dasti settings surface with three sections: Account, Appearance, Export defaults. Each section uses `.dasti-panel` (20px radius, gradient surface, 24px padding). Section headings: eyebrow utility (10px/600/0.1em/uppercase) above a 20px Geist title. Palette picker shows all 5 accents as 36×36 circles with selected-ring `box-shadow: 0 0 0 2px var(--color-border-strong)`.

### 11.3 Golden rules for prompts

1. **Never mention raw hex** when a semantic token exists. Write `var(--color-accent)`, not `#5d8a70`.
2. **State the layer explicitly** ("this is chrome" / "this is inside the document paper") so the model picks the correct typeface.
3. **Use the 4-property transition** (`background-color, border-color, box-shadow, transform @ 120ms var(--ez)`). Don't invent new curves.
4. **Limit to one primary button** per screen.
5. **Remind about the inset stripe** for active nav items — models default to filled backgrounds and that breaks the system.
6. **Explicitly ban focus glow on subtle-fill inputs** — it's the easiest rule to lose in generation.
7. **Default to Sauge** unless told otherwise. Every palette variant must still respect the same structural tokens.

---

*End of DESIGN.md. The accompanying `preview.html` and `preview-dark.html` are the living visual catalogs for this system.*
