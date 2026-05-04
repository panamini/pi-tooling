---
name: skill-curator
description: Inspect and maintain the local Pi skill library. Use when reviewing duplicate, stale, tiny, missing-description, or overlapping skills.
disable-model-invocation: true
---

# Skill Curator

Use this to maintain a Pi skill library without immediately deleting anything.

## Run curator report

```txt
/skill-curator
```

This scans local `skills/` and extension-bundled `SKILL.md` files, then writes:

```txt
.pi/SKILL_CURATOR_REPORT.md
```

## Review process

1. Read the generated report.
2. Check duplicate-name groups first.
3. Add missing descriptions to frontmatter.
4. Expand tiny skills or merge them into broader workflow skills.
5. Re-test stale skills before routing users to them.

## Safety rule

Do not delete skills automatically. Archive or remove only after user approval.
