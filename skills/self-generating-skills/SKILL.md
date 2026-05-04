---
name: self-generating-skills
description: Turn repeated workflows into reusable Pi skills. Use when a task should become a SKILL.md or when the user asks to create, draft, or install a new skill.
disable-model-invocation: true
---

# Self-Generating Skills

Use this when a workflow is repeated or the user asks to turn behavior into a reusable skill.

## Fast path

Run:

```txt
/skill-draft <skill-name> <short description>
```

This creates `skills/<skill-name>/SKILL.md` in the current project.

## Authoring checklist

A good generated skill should include:

- A tight `description` that says exactly when to use it.
- Clear triggers and non-triggers.
- A short workflow with verification steps.
- Any required tools, files, or commands.
- Safety notes for destructive actions.

## Update loop

After the skill is used successfully 2-3 times:

1. Fold learned edge cases into `SKILL.md`.
2. Remove one-off context that should not generalize.
3. Run `/skill-curator` to check overlap with existing skills.
