---
name: pi-review-loop
description: Run automated iterative review (N passes) to reduce missed regressions after edits or before shipping.
disable-model-invocation: true
---

# Pi Review Loop

Use when you want review automation:

- `/review-start` for implementation review loop.
- `/review-plan` to sanity-check plans vs current code.
- `review_loop()` for explicit control and iteration settings.
