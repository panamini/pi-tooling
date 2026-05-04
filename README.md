# pi-central-hub

Centralized repo for my **Pi** skills and extensions.

It keeps:

- `extensions/` → Pi extensions
- `skills/` → Pi skills (`SKILL.md`)

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

### Imported from `nicobailon/visual-explainer`

- Skill:
  - `visual-explainer` (plus prompt commands)

### Existing local resources

- Skills:
  - `project-checklist`
  - `debug-live-boundary` (from `panamini/skill-lib`)
  - `design-md-library` (from `panamini/skill-lib`)
- Extension:
  - `central-hub` (`/hub-note` command)

## Install (recommended)

```bash
pi install git:github.com/panamini/pi-tooling
```

You can still keep a local checkout (`/Users/pana/pi-tooling`) for editing and commits.

## Use

- Preview diff-style update demo:
  - `notes/visual-explainer-diff-update-flow.html`

- Skills:
  - `/skill:project-checklist`
  - `/skill:debug-live-boundary`
  - `/skill:design-md-library`
  - `/skill:pdf-reader`
  - `/skill:stop-slop`
  - `/skill:visual-explainer`

- Extensions:
  - Check command names in each extension’s source or README.
  - Added direct extension file:
    - `extensions/ask-user-question.ts`

For visual-explainer, prompt templates are also available under `/commands`:
- `/generate-web-diagram`
- `/generate-visual-plan`
- `/generate-slides`
- `/diff-review`
- `/plan-review`
- `/project-recap`
- `/fact-check`
- `/share-page`

## Update workflow (offline-safe + auto-update when online)

### One command to pull latest from source repos and sync this package

```bash
cd /Users/pana/pi-tooling
./scripts/sync-upstream.sh --commit --push
```

What it does:
- Re-syncs selected skill/extension folders from their upstream repos:
  - panamini/skill-lib
  - amosblomqvist/pi-config
  - nicobailon/visual-explainer
- Commits + pushes the updates (`--commit`, `--push`)
- Runs `pi update git:github.com/panamini/pi-tooling` so installed Pi package updates immediately

### Day-to-day updates on any machine

```bash
pi update git:github.com/panamini/pi-tooling
```

If you are disconnected, your already-installed copy under `~/.pi/agent/git/...` keeps working.
When you reconnect, rerun the update command.

## Notes

This repo is now a single source of truth: local edits + GitHub sync + Pi git package install.
