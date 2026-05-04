# pi-central-hub

Centralized local repo for my **pi** skills and extensions.

It keeps:

- `extensions/` → pi extensions
- `skills/` → pi skills (`SKILL.md`)

## Contents

### Imported from `amosblomqvist/pi-config`

- Skills:
  - `pdf-reader`
  - `stop-slop`
- Extensions:
  - `youtube-search`
  - `filechanges`
  - `video-extract`
  - `subagents`
  - `ask-user-question.ts`
  - `web-fetch`

### Existing local resources

- Skills:
  - `project-checklist`
  - `debug-live-boundary` (from `panamini/skill-lib`)
  - `design-md-library` (from `panamini/skill-lib`)
- Extension:
  - `central-hub` (`/hub-note` command)

## Install (global)

```bash
pi install /Users/pana/pi-tooling
```

## Use

- Skills:
  - `/skill:project-checklist`
  - `/skill:debug-live-boundary`
  - `/skill:design-md-library`
  - `/skill:pdf-reader`
  - `/skill:stop-slop`
- Extensions:
  - Check command names in each extension’s source or README.
  - Added direct extension files:
    - `extensions/ask-user-question.ts`

## Notes

This package is local and centralized so you can keep one repo for all your custom pi workflow tools.
