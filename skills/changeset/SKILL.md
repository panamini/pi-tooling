---
name: changeset
description: Use for targeted repository change assessment, a scoped implementation plan, execution of an approved or explicitly requested change, verification of local changes, review of a diff or pull request, or preparation of a commit/PR. Applies to fixes, features, refactors, configuration, tests, docs, dependencies, and migrations. Enforces Git-safe scope control and evidence-backed completion. Do not use for open-ended architecture exploration, incident response, or code explanation with no proposed change.
disable-model-invocation: true
---

# Changeset

Control one atomic repository outcome from understanding through review and publication. Keep the change narrow, preserve user work, and make every completion claim traceable to fresh evidence.

Respond in the user's language. Keep status tokens, paths, commands, and identifiers unchanged.

## Load the right reference

- For `PLAN` or `IMPLEMENT`, read [references/change-contract.md](references/change-contract.md).
- Before any Git mutation or `PUBLISH`, read [references/git-safety.md](references/git-safety.md).
- For `VERIFY`, `REVIEW`, or any success claim, read [references/verification-and-review.md](references/verification-and-review.md).
- When changing or evaluating this skill, read [references/evaluation-cases.md](references/evaluation-cases.md).

Do not load every reference by default.

## Non-negotiable contract

1. Work on one independently reviewable outcome, not necessarily one file. Split unrelated outcomes into separate contracts.
2. Treat `ASSESS`, `PLAN`, `VERIFY`, and standalone `REVIEW` as read-only. Running non-destructive inspection and tests is allowed; editing is not.
3. Never commit, push, open a PR, mark a draft ready, or merge unless the user explicitly requests that action.
4. Never discard, overwrite, stash, reset, restore, clean, or rewrite user work automatically.
5. Never broaden scope for opportunistic refactors, formatting, dependency updates, or adjacent fixes.
6. Never claim success from intention, a prior run, a grep alone, or an uninspected exit code. Use fresh evidence from the final state.
7. Never invent repository wrappers or commands. Use prescribed tooling only when it exists and is available; otherwise use appropriate native tools.
8. Never use real secrets, production systems, shared databases, user data, or mutable local environment files merely to construct a test.
9. Mark facts as observed, inferred, or unverified. Do not present inference as repository truth.
10. Stop when the requested outcome is complete. Do not begin the next improvement.

## Resolve the operation

Choose the smallest operation that satisfies the request:

- `ASSESS`: The user wants targeted file/code-path analysis but has not selected a precise outcome.
- `PLAN`: The user wants a fiche, plan, scope, implementation brief, or review before editing.
- `IMPLEMENT`: The user explicitly asks to implement, fix, change, apply, or execute an approved contract.
- `VERIFY`: The user asks to prove, test, validate, or check an implementation without changing it.
- `REVIEW`: The user asks for code review of a diff, branch, commit range, or PR.
- `PUBLISH`: The user explicitly asks to stage, commit, push, open/update a PR, or mark it ready.

For combined requests, run the required operations in order. `PUBLISH` authorization never follows implicitly from `IMPLEMENT` authorization.

When wording is ambiguous, choose the read-only operation. An explicit “do not modify” instruction overrides implementation language.

## Resolve authorization without unnecessary ceremony

- A request for analysis, planning, verification, or review does not authorize edits.
- A clear request to implement authorizes a compact change contract and implementation in the same run when the outcome is unambiguous, reversible, and not high risk.
- Require a separate approval of the exact contract version when the user requests approval-first behavior, the change is high risk or irreversible, the behavior is materially ambiguous, or a product/design decision remains.
- A prior contract is executable only when the user approves or clearly references its exact latest version. Never execute an older version silently.
- Implementation authorization does not authorize commit, push, PR creation, deployment, migration execution, or merge.

## Repository preflight

Before making repository-specific claims:

1. Locate the repository/workspace root and the actual target path.
2. Read applicable instructions from the root through the target directory, including agent instructions and relevant contribution/build/test documentation.
3. Detect the project tooling from real files and CI configuration. Check that proposed commands exist.
4. If Git is present, record branch, `HEAD`, status including untracked files, likely base ref, and changed paths.
5. Read the target files and only the call sites, tests, configuration, generated-source rules, or docs needed to understand the active path.
6. Identify the source of truth: current user request, issue/spec, tests, public contract, or observed behavior. Report conflicts instead of choosing silently.
7. Classify the risk and decide whether same-run implementation is allowed.

Do not turn preflight into a general repository audit.

## Atomic scope

Define one behavioral or operational outcome. Include every file genuinely required for that outcome, such as implementation, focused tests, schema, lockfile, or documentation. Do not force a coherent change into one file.

Separate scope into:

- **Allowed**: expected files or paths.
- **Conditional**: files permitted only if a named trigger is observed.
- **Forbidden**: tempting adjacent areas, generated files, legacy paths, or unrelated tests that must remain unchanged.

If the request contains independent outcomes, plan only the first or produce separate contracts; never merge them into one hidden refactor.

## Baseline and anti-stale gate

Every executable change contract must identify its version and baseline. Include repository root, branch, `HEAD`, worktree status, files actually read, stable anchors, and content fingerprints for target and context files when available.

A dirty target file is not automatically forbidden: it may be an intentional baseline if its current content and diff are captured explicitly. Unknown or changed in-scope work is not safe to overwrite.

Immediately before editing:

1. Re-read the approved contract and applicable repository instructions.
2. Recompute the baseline and relocate every stable anchor.
3. If `HEAD` moved, inspect the intervening paths. Unrelated drift may proceed only after revalidation is recorded.
4. If an observed file, relevant instruction, anchor, requirement, or in-scope diff changed materially, stop with `STALE_CONTRACT`.
5. If objective, behavior, allowed files, invariants, or required evidence must change, issue a new contract version and return to approval when required.

Do not silently “adapt” a stale contract. Mechanical choices explicitly left to implementation discretion do not require a new version.

## `ASSESS` workflow

Remain read-only and concise:

1. Identify the file type, role, and active path.
2. List only the context files needed next.
3. Separate certain, probable, and unverified claims.
4. Identify the main risks and smallest useful candidate outcome.
5. End with `TARGET_CLEAR`, `NEEDS_TARGET`, or `BLOCKED`.

Do not produce a full roadmap or pseudo-patch unless requested.

## `PLAN` workflow

Read the change-contract reference and produce a versioned Change Contract. It must contain:

- one atomic outcome and explicit non-goals;
- sources of truth, assumptions, invariants, and unresolved decisions;
- risk tier and authorization requirement;
- baseline and observed anchors;
- allowed, conditional, and forbidden files;
- required behavior plus bounded implementation discretion;
- an acceptance/evidence matrix;
- realistic failure modes and a non-destructive recovery strategy;
- proposed branch/PR framing when relevant.

Use `READY_FOR_APPROVAL`, `AUTHORIZED_TO_IMPLEMENT`, `NEEDS_DECISION`, or `BLOCKED`. An agent-generated plan is never self-approved; `AUTHORIZED_TO_IMPLEMENT` requires a direct implementation request or explicit approval.

## `IMPLEMENT` workflow

Read the change-contract and Git-safety references first.

1. Pass authorization, preflight, baseline, and anti-stale gates.
2. Prepare a safe branch/worktree strategy without moving or hiding unrelated user changes.
3. Capture before-state evidence only where it distinguishes the expected change or a regression.
4. Apply the smallest coherent patch within allowed and conditional scope.
5. Add or update focused tests when behavior changes and the repository supports them. Do not manufacture tests that only mirror the implementation.
6. Run narrow checks first, then the broader checks required by risk and blast radius.
7. Inspect the complete tracked and untracked diff, verify scope, and correct only in-contract failures.
8. Re-run affected evidence after every correction. Stop after repeated materially identical failure or when a fix would require new scope.
9. Perform the final evidence pass from the final state and report it.

Do not commit or publish unless separately authorized. End with `LOCAL_PASS`, `LOCAL_PASS_WITH_LIMITATIONS`, `LOCAL_FAIL`, or `STALE_CONTRACT`.

## `VERIFY` workflow

Remain read-only. Read the verification reference and evaluate the exact artifact supplied: current worktree, patch, commit, branch, or PR.

- Map each acceptance criterion to structural, static, behavioral, negative, or manual evidence.
- Inspect command output and observable outcomes; a zero exit code alone may be insufficient.
- Treat `NOT_RUN`, unavailable tooling, skipped checks, and stale output as limitations, never as passes.
- Distinguish introduced failures from reproducible baseline failures when evidence permits.
- Verify the latest content or exact commit SHA. Cross-machine verification must identify the same artifact.

End with `VERIFIED`, `VERIFIED_WITH_LIMITATIONS`, `VERIFICATION_FAILED`, or `STALE_CONTRACT`.

## `REVIEW` workflow

Remain read-only unless the user also authorized implementation of review findings.

1. Establish the correct base and review the full introduced diff, including staged, unstaged, and relevant untracked files.
2. First review contract/spec compliance and out-of-scope changes.
3. Then review correctness, edge cases, security, data safety, concurrency, performance, compatibility, operations, and test quality as relevant.
4. Report findings first, ordered by severity. Every finding needs a location, failure scenario, evidence, and a bounded recommendation.
5. Avoid generic praise, style-only noise, and pre-existing issues outside the requested diff.
6. Prefer a fresh read-only reviewer/subagent when the harness supports one. Otherwise label the result `SELF_REVIEW`.
7. Any code change after review invalidates that review for the changed diff and requires fresh affected verification and review.

Use GitHub-compatible review outcomes: `APPROVE`, `COMMENT`, or `REQUEST_CHANGES`.

## `PUBLISH` workflow

Read the Git-safety and verification references first. Publication always requires explicit user authorization.

1. Confirm the intended base branch and exact change set.
2. Require fresh final-state evidence. Do not call a change merge-ready from local checks alone.
3. Stage only agent-owned, allowed hunks or files; never use blanket staging.
4. Inspect the staged diff and staged file list before committing.
5. Follow repository conventions for commit messages, signing, hooks, and PR templates. Never bypass hooks or signing silently.
6. Push without force unless the user explicitly authorizes a justified history rewrite.
7. Create or update a PR/MR with objective, scope, evidence, risks, rollback, limitations, and the Change Contract ID/version.
8. A ready-for-review PR requires required local evidence and no blocking review finding. With explicit permission, a draft may be opened to expose a blocker or await CI, but it must be labeled as limited.
9. Report remote checks and approvals only for the latest commit SHA. Never merge unless explicitly requested and all applicable repository gates pass.

Use `PR_CREATED_DRAFT`, `PR_CREATED_READY`, `PR_BLOCKED`, `MERGE_READY`, or `MERGE_BLOCKED`.

## Evidence rules

- Use the repository's real commands and narrowest relevant checks first.
- A grep proves presence or absence, not runtime behavior.
- A snapshot proves output shape, not necessarily semantics.
- A unit test proves only its covered behavior; name uncovered risks.
- For a bug fix, prefer a regression test that fails on the baseline and passes on the final state when practical.
- For configuration/provider changes, verify the changed outcome, not merely request success.
- For generated artifacts, verify the source-to-generated workflow and do not hand-edit generated output unless repository policy requires it.
- Record commands, exit status, relevant output, and limitations. Do not paste irrelevant logs.
- Run final evidence after the final edit; earlier passing results are stale.

## Adaptive reporting

Do not repeat unchanged material across phases. Reference the Change Contract ID/version and report deltas.

- `ASSESS`: role, active path, context, certainty, risks, candidate outcome, status.
- `PLAN`: full Change Contract.
- `IMPLEMENT`: authorization/baseline result, branch/worktree, files changed, commands and results, evidence matrix, diff summary, limitations, status.
- `VERIFY`: artifact identity, criteria-by-criteria evidence, failures/limitations, status.
- `REVIEW`: findings first, open questions, test gaps, review outcome, review identity.
- `PUBLISH`: commit/branch/base, staged paths, push/PR result, latest SHA, local/remote gates, status.

When blocked, state the smallest concrete decision or missing artifact needed. Do not invent certainty or continue out of scope.
