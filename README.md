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

### Imported from `nicobailon`

- `visual-explainer` (skill + prompt commands)
- `pi-web-access` (replaces basic web-fetch use-case)
- `pi-design-deck`
- `pi-prompt-template-model`
- `pi-annotate`
- `pi-intercom`
- `pi-review-loop`
- `pi-skill-palette`
- `pi-side-chat`
- `pi-mcp-adapter`
- `pi-messenger`

### Existing local resources

- Skills:
  - `project-checklist`
  - `debug-live-boundary` (from `panamini/skill-lib`)
  - `design-md-library` (from `panamini/skill-lib`)
- Extensions:
  - `central-hub` (`/hub-note` command)
  - `auto-workflow-router` (plain-language routing + skill hinting)
  - `pi-tooling-reminder`

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
  - `/skill:web-access`
  - `/skill:pi-design-deck`
  - `/skill:prompt-template-model`
  - `/skill:pi-annotate`
  - `/skill:pi-intercom`
  - `/skill:pi-review-loop`
  - `/skill:pi-skill-palette`
  - `/skill:pi-side-chat`
  - `/skill:pi-mcp-adapter`
  - `/skill:pi-messenger`

- Extensions:
  - Check command names in each extension’s source or README.
  - Added direct extension files:
    - `extensions/ask-user-question.ts`
    - `extensions/central-hub.ts`

For visual-explainer, prompt commands are available under `/commands`:
- `/generate-web-diagram`
- `/generate-visual-plan`
- `/generate-slides`
- `/diff-review`
- `/plan-review`
- `/project-recap`
- `/fact-check`
- `/share-page`

Use:

```bash
/sync-pi-tooling
```

to show the current refresh commands in Pi.

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
  - nicobailon/pi-web-access
  - nicobailon/pi-design-deck
  - nicobailon/pi-prompt-template-model
  - nicobailon/pi-annotate
  - nicobailon/pi-intercom
  - nicobailon/pi-review-loop
  - nicobailon/pi-skill-palette
  - nicobailon/pi-side-chat
  - nicobailon/pi-mcp-adapter
  - nicobailon/pi-messenger
- Commits + pushes the updates (`--commit`, `--push`)
- Runs `pi update git:github.com/panamini/pi-tooling` so installed Pi package updates immediately

### Day-to-day updates on any machine

```bash
pi update git:github.com/panamini/pi-tooling
```

If you are disconnected, your already-installed copy under `~/.pi/agent/git/...` keeps working.
When you reconnect, rerun the update command.

## Reminder behavior

This repo includes a Pi extension that shows a reminder when Pi starts (throttled to once every 12h):
- Command reminder: `/sync-pi-tooling`
- Default reminder text:
  - `cd /Users/pana/pi-tooling && ./scripts/sync-upstream.sh --commit --push`
  - `pi update git:github.com/panamini/pi-tooling`

## Notes

This repo is now a single source of truth: local edits + GitHub sync + Pi git package install.

### Token policy

To keep runtime prompt overhead low, newly added mini skills are marked
`disable-model-invocation: true`:
- They are discoverable via `/skill:<name>`
- They are not injected into every turn by default
- You get on-demand execution without permanent token spend.

## Auto-routing behavior

This repo also includes an auto-routing extension:
- `extensions/auto-workflow-router.ts`

It adds a lightweight, per-turn hint so natural-language tasks are mapped to the right skill/extension automatically.

For Neyssan app work and other complex flows, it biases toward richer orchestration (scout → planner → worker → reviewer-style flow) when it detects multi-step or high-risk work.
