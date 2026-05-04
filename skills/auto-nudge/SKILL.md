---
name: auto-nudge
description: Lightweight workflow nudges for repeated tasks, large plans, and review checkpoints. Use when configuring or reasoning about Pi's proactive guidance.
disable-model-invocation: true
---

# Auto Nudge

Pi-tooling includes a quiet auto-nudge extension that can suggest better workflows without forcing them.

## Commands

```txt
/nudge status
/nudge on
/nudge off
```

## Current nudge patterns

- Repeated workflow language → suggests `/skill-draft`.
- Large/multi-step task language → suggests `blueprint` or crew planning.
- Shipping/review checkpoint language → suggests review-loop.

## Principle

Nudges should be rare, actionable, and dismissible. If a nudge becomes noisy, turn it off or narrow its trigger.
