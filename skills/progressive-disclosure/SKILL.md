---
name: progressive-disclosure
description: Design Pi workflows that start simple and reveal advanced controls only when needed. Use when improving UX, routing hints, palettes, deck flows, or agent command discoverability.
disable-model-invocation: true
---

# Progressive Disclosure

Use this when a workflow risks overwhelming the user with too many tools, commands, or options.

## Pattern

1. Start with one recommended action.
2. Offer 2-3 alternatives only if useful.
3. Reveal advanced configuration after the user asks or the simple path fails.
4. Keep escape hatches visible (`off`, `cancel`, `status`, `more`).

## Pi examples

- Skill palette: command picker instead of memorizing skill names.
- Web curator: simple search first, deeper source selection in UI.
- Design deck: visual options first, generated-more only on request.
- Auto-nudge: quiet one-line suggestions instead of forced workflows.

## Copy template

```txt
Recommended: <one action>.
Why: <short reason>.
More options: <option A>, <option B>, <option C>.
```
