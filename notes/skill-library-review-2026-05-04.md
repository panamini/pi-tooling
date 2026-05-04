# Skill Library Review (Blueprint + ECC skill corpus)

Date: 2026-05-04

## Scope reviewed
- `https://github.com/owainlewis/blueprint`
- Local Codex skills:
  - `/Users/pana/.codex/skills/debug-red-first/SKILL.md`
  - `/Users/pana/.codex/skills/tdd-workflow/SKILL.md`
- Local Everything-Claudecode checkout (`.../neyssan/everything-claude-code`): scanned SKILL files (especially `skills/blueprint`, `skills/verification-loop`, `skills/tdd-workflow`, `skills/codebase-onboarding`, etc.)
- Existing Pi tooling hub skills in `/Users/pana/pi-tooling`

## Current Pi coverage (already have)
- `project-checklist` – onboarding checklist
- `pi-review-loop` – iterative post-edit review passes
- `debug-live-boundary` – production-vs-local behavior mismatch debugging
- `visual-explainer` – high-signal visual explanation/review outputs
- `web-access`, `pi-design-deck`, `pi-messenger`, etc. (supportive but not core code-review workflow)

## Blueprint overlap/fit
Blueprint (10 skills): `build, commit, compress, coverage, debug, plan, refactor, review, spec, tdd`.

### Already covered vs duplicate
- `review` → **partially covered** by `pi-review-loop` (same intent, but Blueprint is spec- and diff-style review workflow, less code tool-dependent)
- `coverage` → **partially covered** functionally by `pi-review-loop` (iterative checks), but Blueprint is cleaner target-driven guidance for gaps
- `tdd` → **same family** as Codex `tdd-workflow`; both are heavier than day-to-day unless you do strict TDD
- `debug` → **overlaps** with `debug-live-boundary` but Blueprint is broader, less UI-specific
- `plan/spec/commit/build/refactor/compress` → **not in current Pi skill set**, good gap fillers

## Codex / ECC findings by utility
- `debug-red-first` (Codex): highest signal for unstable UI/state bugs; very practical and stronger than generic debug guidance
- `tdd-workflow` (Codex): strict RED-first with 80%+ coverage goal; often heavier but good for behavior-sensitive areas
- `verification-loop` (ECC): practical end-of-change quality gate (build/type/lint/tests/security/diff). Strong companion to `pi-review-loop`
- `codebase-onboarding` (Codex): better than running a full checklist for first-open projects
- `git-workflow` (Codex): workflow quality (branching/commit conventions), good for consistency
- `blueprint` (ECC): useful only for larger multi-PR work; usually overkill for small one-shot tasks

## Most critical additions for day-to-day
1. **`verification-loop`** (ECC/neyssan copy) — strongest immediate quality gate replacement for “is this safe to ship?”
2. **`debug-red-first`** (Codex) — best for real-world bug symptoms when tests are green but behavior is wrong
3. **`tdd-workflow`** (Codex) *or* **`blueprint:tdd`** (choose one): strict RED-first discipline for new or risky changes
4. **`codebase-onboarding`** (Codex) for first-pass project understanding, instead of ad-hoc checklist runs
5. **`blueprint:spec` + `blueprint:plan`** for larger scoped work that normally needs explicit decisions before implementation

## Recommended “best review stack” to add next
- Primary: `verification-loop` + `debug-red-first`
- Secondary: one TDD skill (`tdd-workflow` preferred since you already have it locally) + `blueprint:review`
- Keep existing: `pi-review-loop` (strong iterative verifier), `project-checklist` (quick onboarding)

## Actioning plan (minimal overhead)
- Add lightweight `SKILL.md` wrappers in `pi-tooling` for the 3–5 above (disable-model-invocation: true), no extension overhead
- Avoid importing full heavy docs bundles or locales unless needed
- Route `user asks review/check/quality` heuristically to: `verification-loop` for end-state checks, `blueprint:review` for code/spec risk review, `debug-red-first` when symptom-level debugging is needed

---

## Supplemental pass (2026-05-04): full SKILL.md index sweep of your requested sources
- I ran a full SKILL.md inventory over:
  - `/Users/pana/.codex/skills`
  - `/Volumes/video/kay/app/pouraurelien/save/implementation_UI/neyssan/everything-claude-code` (`/skills`, plus locale docs)
- I did **not** need per-file manual permission prompts; I used full-tree metadata scans, so this is a broader and more complete comparison than prior ad-hoc reads.
- I also verified `/Volumes/video/claude-code/Claude-code-leaks-main/src` has **no SKILL.md files**.

### Findings from the sweep
- **Most critical day-to-day overlap candidates are still the same 4**:
  - `verification-loop`
  - `debug-red-first`
  - `tdd-workflow`
  - `codebase-onboarding`
- Additional high-signal but lower-priority, context-specific additions:
  - `security-review` (when touching auth/input/secret/payment/sensitive code)
  - `plankton-code-quality` (if you want auto quality-enforcement hooks; may be intrusive)
  - `repo-scan` (best for large unfamiliar repos when you need dependency/classification style audits)

### About your question: “already have /skill planificator?”
- In current `/Users/pana/pi-tooling`, there is **no** dedicated `/skill:planificator`.
- Closest equivalents:
  - `blueprint` (in Codex/ECC) → explicit planning/funnel/plan artifacts for large, multi-step work.
  - `project-checklist` + `verification-loop`/`debug-red-first` for lightweight day-to-day flow.
- So yes, your current plan ability exists in **blueprint-style decomposition** terms, but not as a literal `planificator` named skill in Pi.

### Recommendation
- Keep the four critical skills already added first.
- Add `security-review` as the next single import if your work includes user-facing or sensitive data paths.
- Add `blueprint` only when you need heavy planning orchestration across >1 PR or a true multi-session strategy.
