---
name: ingest-wiki
description: "Twoweeks wiki memory bridge workflow: choose ingest / lint / direct-update / save-output mode, read the neutral read-order, and mutate only through twoweeks rules."
disable-model-invocation: true
origin: twoweeks-wiki
---

# ingest-wiki

Use this when the user asks to mutate the twoweeks memory plane (`wiki/*`) from project context.

## 1) Mode selection

- `ingest`: process staged files in `rawinput/`
- `lint`: health check / audit / consistency review
- `direct-update`: explicit page edits without raw ingest
- `save-output`: save a current analysis to `wiki/outputs/`

## 2) Read sequence (required)

1. `WIKI_SCHEMA.md` if present
2. `AGENTS.md` and/or `CLAUDE.md`
3. `wiki/hot.md` if present
4. `wiki/index.md`
5. targeted durable pages via `index.md` / retrieval map
6. recent `wiki/log.md` entries only when needed

If `wiki/hot.md` is missing, stale, or unavailable, fall back to:
- `WIKI_SCHEMA.md`
- `CLAUDE.md`
- `wiki/overview.md`
- `wiki/index.md`

## 3) Core constraints

- `wiki/hot.md` is cache only, not canonical truth.
- Durable current pages (`status: current`) win over cache.
- Never treat the cache as the source of truth.
- Never duplicate the full write contract.
- For write operations, keep changes minimal and surgical.

## 4) Mutating memory pages (required updates)

When a write is performed:
- update `wiki/index.md` and `wiki/log.md`
- update `wiki/hot.md` when active context changed or retrieval routing changed
- preserve existing frontmatter and page conventions from `wiki`

## 5) Ingest workflow

For `ingest` mode:
1. Scan `wiki/rawinput/`.
2. If empty (except `README.md`), stop and report no staging.
3. Read full files, dedupe, and resolve target durable pages.
4. Update/create source and target pages.
5. Move staged files to `wiki/raw/` or `wiki/raw/assets/` according to type.
6. Update `index.md`, `log.md`, `hot.md` per contract.

## 6) Do not

- Do not add embeddings/RAG/vector DBs.
- Do not redesign product flows.
- Do not edit `wiki/raw/` files as mutable source.
- Do not read the whole wiki unless the request explicitly requires it.