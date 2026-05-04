---
name: design-md-library
description: Use this skill when Codex needs brand-inspired UI direction or wants to build, restyle, or critique an interface to match the visual language of one of the bundled design reference packs such as Stripe, Notion, Linear, Apple, Vercel, Figma, or other included brands. It is for style reference and interface generation guidance, not official vendor design systems.
---

# Design MD Library

## Overview

Use this skill to translate a requested brand or product aesthetic into concrete UI direction using the bundled `design-md` reference packs.

Treat each pack as an unofficial style reference. Reuse the visual language, not the brand assets or any claim of official compliance.

## Workflow

1. Identify the requested brand, product, or closest visual match.
2. Open only the relevant pack under `references/brands/<brand>/`.
3. Read `DESIGN.md` first for the design language.
4. Consult `preview.html`, `preview-dark.html`, or `README.md` only if you need a faster visual check or extra context.
5. Translate the reference into the target project's component system, layout, typography, color variables, and motion without copying marketing copy or claiming brand affiliation.

## Pack Selection

Use `references/catalog.md` to find the available brand folders.

Folder names are the routing key. Match user requests directly to the folder name when possible:

- `"make it look like Stripe"` -> `references/brands/stripe/`
- `"use a Notion-like UI"` -> `references/brands/notion/`
- `"give this page Linear energy"` -> `references/brands/linear.app/`
- `"make it feel like xAI"` -> `references/brands/x.ai/`

If the user names a brand that is not present, choose the closest pack by product category and explain that you are using it as the nearest stylistic match.

## How to Apply a Pack

Extract the smallest set of decisions needed for the task:

- palette and contrast strategy
- typography and hierarchy
- spacing density
- border radius and stroke treatment
- shadows, gradients, and surface treatment
- CTA style
- card, nav, and form patterns
- motion tone

Then adapt those decisions to the existing codebase. Preserve the host product's information architecture, accessibility requirements, and component APIs unless the user explicitly asks for structural changes.

## Constraints

- Treat the bundled packs as informative references, not authoritative design systems.
- Do not present the output as official brand work.
- Do not copy logos, trademarks, or proprietary illustrations unless the user separately provides rights-cleared assets.
- Prefer reading a single `DESIGN.md` over loading multiple packs.
- Only compare multiple packs when the user asks for exploration, ranking, or a blended direction.

## Resources

- Catalog of included packs: `references/catalog.md`
- Brand packs: `references/brands/<brand>/DESIGN.md`
- Optional visual previews: `references/brands/<brand>/preview.html` and `references/brands/<brand>/preview-dark.html`
