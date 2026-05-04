---
name: personality-skins
description: Switch Pi behavior profiles such as builder, reviewer, researcher, minimal, and planner. Use when the user asks for persona packs, skins, tone presets, or workflow defaults.
disable-model-invocation: true
---

# Personality Skins

Personality skins bundle tone and workflow preferences. They are lighter than themes: themes change visuals; skins change behavior.

## Commands

```txt
/skin list
/skin status
/skin builder
/skin reviewer
/skin researcher
/skin minimal
/skin planner
/skin off
```

## Built-in skins

- `builder` — practical implementation mode.
- `reviewer` — adversarial review mode.
- `researcher` — evidence-first mode.
- `minimal` — low-chatter mode.
- `planner` — blueprint-style planning mode.

## Notes

The active skin is saved in `.pi/active-skin.json` for the current project and injected into the next turn's system prompt.
