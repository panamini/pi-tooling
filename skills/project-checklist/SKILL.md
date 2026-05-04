---
name: project-checklist
description: Create and track a lightweight checklist for project onboarding, validation, and cleanup tasks.
---

# project-checklist

Use this skill when starting work in a project and you need a quick consistency pass.

## What to do

1. Read this skill with `/skill:project-checklist` before touching code.
2. Create a checklist file:

```bash
./scripts/checklist.sh .
```

3. Fill the list and keep it in the project root as `project-checklist.md`.

## Checklist template

- [ ] Confirm project root and dependencies are correct
- [ ] Run tests/lint/typecheck before changes
- [ ] Review README for setup or run instructions
- [ ] Validate file permissions and env requirements

## When to use

- New feature branches
- Before opening a review or PR
- Before long refactors
