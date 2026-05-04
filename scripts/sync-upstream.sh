#!/usr/bin/env bash
set -euo pipefail

# Sync selected skill/extension sources into this repo from their upstream repos,
# then optionally commit and update the locally installed git package.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"

trap 'rm -rf "$TMP_DIR"' EXIT

function usage() {
  cat <<'EOF'
Usage: scripts/sync-upstream.sh [--commit] [--push]

Flags:
  --commit   Commit any synced changes with a generated message.
  --push     Push after committing (implies --commit).
  --no-update Skip refreshing local git-installed package in ~/.pi/agent/git.

This script:
  1) Pulls latest from source repos (non-interactively, depth 1)
  2) Overwrites selected local folders in this repo:
     - debug-live-boundary
     - design-md-library
     - pdf-reader
     - stop-slop
     - youtube-search
     - filechanges
     - video-extract
     - subagents
     - ask-user-question.ts
     - visual-explainer
     - pi-web-access
     - pi-design-deck
     - pi-prompt-template-model
     - pi-annotate
     - pi-intercom
     - pi-review-loop
     - pi-skill-palette
     - pi-side-chat
     - pi-mcp-adapter
     - pi-messenger
  3) Optionally commits + pushes
  4) Refreshes installed package in Pi: `pi update git:github.com/panamini/pi-tooling`
EOF
}

function prune_extension_artifacts() {
  local dst_path="$1"
  local dir="$ROOT_DIR/$dst_path"

  [[ -d "$dir" ]] || return 0

  # Keep runtime lean: drop lockfiles, test/example artifacts, and demos not required
  # for Pi execution in this centralized package.
  rm -f "$dir/package-lock.json"

  find "$dir" \
    -type d \
    \( -name "__tests__" -o -name "test" -o -name "tests" -o -name "examples" \) \
    -prune -exec rm -rf {} +

  find "$dir" \
    -type f \
    \( -name "*.test.ts" -o -name "*.test.tsx" -o -name "*.test.mjs" -o -name "*.test.mts" -o -name "*.mp4" -o -name "*.webm" \) \
    -delete
}


COMMIT=0
PUSH=0
UPDATE=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --commit)
      COMMIT=1
      shift
      ;;
    --push)
      COMMIT=1
      PUSH=1
      shift
      ;;
    --no-update)
      UPDATE=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

declare -A SOURCES
SOURCES["https://github.com/panamini/skill-lib.git,debug-live-boundary,skills/debug-live-boundary"]=""
SOURCES["https://github.com/panamini/skill-lib.git,design-md-library,skills/design-md-library"]=""

SOURCES["https://github.com/amosblomqvist/pi-config.git,skills/pdf-reader,skills/pdf-reader"]=""
SOURCES["https://github.com/amosblomqvist/pi-config.git,skills/stop-slop,skills/stop-slop"]=""
SOURCES["https://github.com/amosblomqvist/pi-config.git,extensions/youtube-search,extensions/youtube-search"]=""
SOURCES["https://github.com/amosblomqvist/pi-config.git,extensions/filechanges,extensions/filechanges"]=""
SOURCES["https://github.com/amosblomqvist/pi-config.git,extensions/video-extract,extensions/video-extract"]=""
SOURCES["https://github.com/amosblomqvist/pi-config.git,extensions/subagents,extensions/subagents"]=""
SOURCES["https://github.com/amosblomqvist/pi-config.git,extensions/ask-user-question.ts,extensions/ask-user-question.ts"]=""

SOURCES["https://github.com/nicobailon/pi-web-access.git,.,extensions/pi-web-access"]=""
SOURCES["https://github.com/nicobailon/pi-design-deck.git,.,extensions/pi-design-deck"]=""
SOURCES["https://github.com/nicobailon/pi-prompt-template-model.git,.,extensions/pi-prompt-template-model"]=""
SOURCES["https://github.com/nicobailon/pi-annotate.git,.,extensions/pi-annotate"]=""
SOURCES["https://github.com/nicobailon/pi-intercom.git,.,extensions/pi-intercom"]=""
SOURCES["https://github.com/nicobailon/pi-review-loop.git,.,extensions/pi-review-loop"]=""
SOURCES["https://github.com/nicobailon/pi-skill-palette.git,.,extensions/pi-skill-palette"]=""
SOURCES["https://github.com/nicobailon/pi-side-chat.git,.,extensions/pi-side-chat"]=""
SOURCES["https://github.com/nicobailon/pi-mcp-adapter.git,.,extensions/pi-mcp-adapter"]=""
SOURCES["https://github.com/nicobailon/pi-messenger.git,.,extensions/pi-messenger"]=""

SOURCES["https://github.com/nicobailon/visual-explainer.git,plugins/visual-explainer,skills/visual-explainer"]=""

declare -A CACHE

sync_from_repo() {
  local repo="$1"
  local src_path="$2"
  local dst_path="$3"

  local dir_name
  dir_name="${repo##*/}"
  dir_name="${dir_name%.git}"

  local workdir="$TMP_DIR/$dir_name"

  if [[ -z "${CACHE[$repo]+x}" ]]; then
    if [[ -d "$workdir/.git" ]]; then
      echo "Updating cached clone: $repo"
      git -C "$workdir" fetch --depth 1
      git -C "$workdir" reset --hard origin/HEAD
    else
      echo "Cloning $repo"
      git clone --depth 1 "$repo" "$workdir"
    fi
    CACHE[$repo]="$workdir"
  fi

  workdir="${CACHE[$repo]}"
  local full_src="$workdir/$src_path"

  if [[ ! -e "$full_src" ]]; then
    echo "Skipped: source not found -> $src_path in $repo" >&2
    return 1
  fi

  mkdir -p "$(dirname "$ROOT_DIR/$dst_path")"
  rm -rf "$ROOT_DIR/$dst_path"
  cp -R "$full_src" "$ROOT_DIR/$dst_path"
  echo "Synced: $src_path -> $dst_path"
}

for key in "${!SOURCES[@]}"; do
  IFS=',' read -r repo src dst <<< "$key"
  sync_from_repo "$repo" "$src" "$dst"
  if [[ "$dst" == extensions/* ]]; then
    prune_extension_artifacts "$dst"
  fi
done

if [[ $COMMIT -eq 1 ]]; then
  cd "$ROOT_DIR"
  git add README.md package.json scripts/sync-upstream.sh extensions skills notes 2>/dev/null || true
  if git diff --cached --quiet; then
    echo "No changes to commit."
  else
    git commit -m "chore: sync upstream skill and extension sources"
  fi

  if [[ $PUSH -eq 1 ]]; then
    git push
  fi
fi

if [[ $UPDATE -eq 1 ]]; then
  if command -v pi >/dev/null 2>&1; then
    echo "Refreshing installed package in pi: git:github.com/panamini/pi-tooling"
    pi update git:github.com/panamini/pi-tooling
  else
    echo "pi CLI not found; skipping installed-package refresh."
  fi
fi
