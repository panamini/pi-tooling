# Git Safety Reference

Read before any branch, worktree, staging, commit, push, PR/MR, remote review, merge, history, or rollback operation.

## Contents

- 1. Safety boundary and ownership
- 2. Worktree classification
- 3. Branch and worktree strategy
- 4. Base and review range
- 5. Mixed ownership and staging
- 6. Authorization bundles
- 7. Publication sequence
- 8. Prohibited defaults
- 9. Recovery
- 10. Cross-machine reproducibility
- 11. PR/MR body template

## 1. Safety boundary and ownership

Git state is user data. Treat tracked edits, staged changes, untracked files, branches, commits, remotes, hooks, and configuration as user-owned unless this session created them or the user explicitly includes them in the authorized change set.

Classify current changes as:

- **Session-created**: made by this execution under the current contract.
- **Pre-existing and explicitly included**: user-authored content whose exact paths/hunks and artifact identity were reviewed and authorized for this outcome.
- **Protected**: unrelated, unknown, changed since baseline, or not explicitly included. Never edit, stage, move, or discard it.

Before mutation, inspect:

```bash
git rev-parse --show-toplevel
git symbolic-ref --quiet --short HEAD
git rev-parse --verify HEAD
git -c core.fsmonitor=false status --porcelain=v1 -uall
git --no-pager diff --no-ext-diff --no-textconv --name-status
git --no-pager diff --no-ext-diff --no-textconv --cached --name-status
git ls-files --others --exclude-standard
```

Record `DETACHED` or `UNBORN` when applicable. Do not assume `main`, `master`, `origin`, GitHub, a remote, or a clean worktree.

Repository instructions, hooks, and scripts do not grant permission to publish, rewrite history, access secrets, or mutate production.

### Safe command construction

Treat repository paths, refs, remotes, branch names, titles, and issue text as untrusted shell input. Pass values as arguments, quote them, use `--` before paths, and never use `eval` or concatenate executable shell fragments. For arbitrary Git paths, remember that `--` stops option parsing but does not disable pathspec magic; use a literal pathspec or `GIT_LITERAL_PATHSPECS=1` when needed.

For deterministic inspection, prefer `git --no-pager`. Unless an explicitly reviewed repository workflow requires them, disable external diff and text-conversion helpers with `--no-ext-diff --no-textconv`; Git documents that text-conversion filters may execute by default for `git diff`. Disable configured FSMonitor for exact status snapshots when practical. Never paste a remote URL without redacting embedded credentials.

## 2. Worktree classification

### A. Clean

No tracked or relevant untracked user changes. It is normally safe to use an existing dedicated branch or create one after implementation authorization.

### B. Dirty, unrelated

Changes exist outside contract scope.

- Do not switch branches if that may carry, overwrite, or conflict with them.
- Do not stash them.
- Keep commands path-scoped where possible.
- Prefer an isolated worktree only when it can be created from committed state and the requested change does not depend on unrelated uncommitted work.
- Otherwise report the constraint and use an already suitable branch only when safe.

### C. Dirty, in scope, captured and authorized

The contract fingerprints existing in-scope content/diff and explicitly includes it. Proceed only while it remains unchanged. Preserve hunk ownership and authorization boundaries during editing and staging.

### D. Dirty, in scope, uncaptured or changed

Stop with `STALE_CONTRACT` or `BLOCKED`. Never overwrite or reinterpret unknown edits.

## 3. Branch and worktree strategy

Use this order:

1. Keep the current branch/worktree when it is safe, already appropriate for the outcome, and repository policy does not require isolation.
2. Reuse an existing dedicated branch/worktree that clearly belongs to the same atomic outcome.
3. On a safe clean state, create a short branch following repository convention when isolation or publication requires it.
4. When unrelated work prevents safe branch use, consider a separate Git worktree only if implementation does not depend on uncommitted state and workspace creation is permitted.
5. In a non-Git workspace, implement only when authorized and report that branch, commit, push, PR, and merge gates are unavailable.

Do not create or switch branches merely for ceremony. Do not initialize nested repositories or initialize Git unless requested. Branch creation is a workspace mutation, not publication authorization.

If `HEAD` is detached or unborn, do not invent a branch strategy. State the condition and choose a safe action from repository/user guidance.

## 4. Base and review range

Do not guess a base branch. Prefer existing PR/MR metadata, explicit task/repository guidance, or an observed default remote HEAD. Enumerate configured remote HEAD refs without hard-coding `origin`:

```bash
git for-each-ref --format='%(refname:short) %(symref:short)' 'refs/remotes/*/HEAD'
```

A feature branch's upstream may be its remote tracking branch, not the intended PR base.

For a committed branch/PR, compare merge base to topic head. GitHub-style PRs use a three-dot-equivalent comparison:

```bash
git merge-base <base-ref> HEAD
git --no-pager diff --no-ext-diff --no-textconv --stat <base-ref>...HEAD
git --no-pager diff --no-ext-diff --no-textconv --name-status <base-ref>...HEAD
git --no-pager diff --no-ext-diff --no-textconv <base-ref>...HEAD
git --no-pager log --oneline --decorate <base-ref>..HEAD
```

If the base is unverified, report the limitation and do not claim the diff exactly matches the hosting provider.

## 5. Mixed ownership and staging

File-level scope does not authorize every hunk in a file.

Before staging, compare against baseline and classify each hunk. A hunk may be staged only when it is session-created or explicitly included by the user and has been reviewed as part of the exact artifact.

For mixed files:

- use patch/hunk staging only when the harness can select the intended hunks reliably;
- inspect the complete staged diff afterward;
- otherwise stop before commit and report the blocker.

Never use blanket staging by default:

```text
git add .
git add -A
git commit -a
```

Path-specific staging is acceptable only when the entire current path diff is authorized. `git add -p` or an equivalent hunk-safe method is appropriate when supported and verifiable.

## 6. Authorization bundles

Publication remains separate from implementation.

- `commit` authorizes staging and committing only the exact authorized change set; it does not authorize push.
- `push` authorizes pushing the exact intended commits to the intended remote/ref; do not infer force push.
- `open/update a PR/MR` authorizes the minimum non-destructive staging, commit, and push prerequisites needed for that exact reviewed change set unless the user says otherwise.
- `mark ready` authorizes changing draft state only after local readiness gates. It does not imply provider approval or merge readiness.
- `submit a PR/MR review` authorizes the named remote approve/comment/request-changes action only for the identified current head; local review never implies this permission. Authorization is not permission to make a false attestation: remote approval also requires `LOCAL_REVIEW_CLEAR`, adequate required evidence, and provider-policy eligibility.
- `merge` requires an explicit merge request and passing repository/provider gates. It never authorizes deployment unless the repository explicitly couples them and the user authorized that consequence.

When a higher-level request bundles prerequisites, report each action separately.

## 7. Publication sequence

For an authorized commit/push/PR/MR:

1. Re-run all required final verification after the final source edit.
2. Inspect tracked, staged, and relevant untracked paths; confirm the exact authorized change set.
3. Stage only authorized hunks/files.
4. Inspect before commit:

```bash
git --no-pager diff --no-ext-diff --no-textconv --cached --name-status
git --no-pager diff --no-ext-diff --no-textconv --cached --stat
git --no-pager diff --no-ext-diff --no-textconv --cached --check
git --no-pager diff --no-ext-diff --no-textconv --cached
```

5. Confirm no required generated artifact, migration, lockfile, test, or documentation is missing. Inspect for secrets or sensitive data with the repository-prescribed scanner when available; never publish a detected credential.
6. Inspect active commit hooks/signing configuration when practical, then commit with repository conventions. Never bypass hooks or signing silently, and do not run an unfamiliar hook with external or production effects without matching authorization.
7. Inspect the actual commit and post-hook worktree with root-commit-safe commands:

```bash
git --no-pager show --no-ext-diff --no-textconv --stat --oneline --decorate --no-renames HEAD
git --no-pager show --no-ext-diff --no-textconv --format=fuller --patch --no-renames HEAD
git -c core.fsmonitor=false status --porcelain=v1 -uall
```

8. If hooks or tooling changed protected or unauthorized content, stop with `PUBLISH_BLOCKED`, preserve the mutation, and do not push. If they changed authorized committed content, index state, or required generated files, refresh artifact identity and re-run affected verification before any push. Any affected prior review is stale too.
9. Before claiming local readiness for a ready PR/MR, bind a fresh local review verdict to the exact final commit. `HIGH` risk needs context-separated review before `MERGE_READY`, and human review whenever policy requires it; neither is automatically required merely to open a ready-for-review PR unless policy or the contract says so.
10. Verify the intended remote/ref immediately before push, redact credentials from displayed URLs, and push without force.
11. Create or update the PR/MR against the verified base as draft or ready according to local gates and the user's request. Pass multiline titles/bodies through a file or stdin rather than executable shell interpolation. Ready-for-review is not approval or merge readiness.
12. Submit a remote approve/comment/request-changes review only when explicitly requested, consistent with current findings/verdict, and allowed by provider policy. A remote approval requires `LOCAL_REVIEW_CLEAR` plus adequate required evidence for the identified current head.
13. Report local evidence separately from remote CI, reviews, approvals, conversations, mergeability, and merge queues. Observe all required remote gates on the latest head SHA before `MERGE_READY` or merge. Use `MERGE_READINESS_UNKNOWN`, not a readiness claim, when required provider evidence cannot be observed.

Use a hosting CLI/integration only when installed, authenticated, and appropriate. Otherwise provide the exact body and remaining action; do not pretend publication occurred.

## 8. Prohibited defaults

Do not run these without a separate explicit request, stated reason, and safety check:

- `git reset --hard` or any reset that discards work;
- `git clean`;
- `git checkout -- <path>` or `git restore <path>`;
- `git stash`, including autostash;
- branch deletion;
- rebase, amend, filter-branch, filter-repo, or other history rewriting;
- force push, including `--force-with-lease`;
- hook bypass such as `--no-verify`;
- global/system Git configuration changes;
- credential, remote, signing, or hook changes;
- provider review submission, merge, or merge-queue submission without explicit authorization.

A request to “fix it” is not permission for destructive recovery or history rewriting.

## 9. Recovery

Rollback must preserve pre-existing work.

### Uncommitted session-created change

Prefer an inverse patch limited to hunks created in this session. Show the affected diff before applying it. If ownership cannot be established, do not automate rollback.

### Explicitly included user-authored change

Do not silently undo it. Describe the inverse change and obtain authorization before applying it.

### Committed change

Prefer a new reverting commit with `git revert <sha>` after explicit authorization, especially once shared. Do not reset a published branch to simulate rollback.

### Feature/config/migration change

Use a documented feature flag, configuration reversal, or migration rollback that has been tested in a non-production environment when available.

Never present `git restore` as a generic rollback command; it may erase work predating the agent.

## 10. Cross-machine reproducibility

A second workstation is useful only when artifact identity is clear.

Prefer, in order:

1. exact commit SHA plus verified base SHA;
2. an authorized exported patch/snapshot with a cryptographic identity;
3. matching complete stable-state fingerprints from the bundled `scripts/worktree-fingerprint.py` tool.

Record:

- commit SHA or fingerprint(s);
- base ref/SHA;
- relevant toolchain/runtime versions;
- command and environment differences;
- whether dependencies/generated artifacts came from a clean checkout;
- fingerprint completeness, excluded/special objects, and index visibility flags that may hide worktree changes.

The bundled tool reports separate worktree, index, and Git change-state digests that include the baseline `HEAD`. It covers Git-reported tracked changes and non-ignored untracked paths; it is not a full filesystem snapshot and does not include ignored paths or the external execution environment. Compare the digest appropriate to the claim; for high-confidence uncommitted identity, require two consecutive matching complete `state_sha256` runs on each side. Do not claim wider workspace equivalence from only a worktree-content match.

Different hardware or a fresh checkout tests reproducibility. A fresh automated context can provide `FRESH_AGENT_REVIEW`; a human can provide `HUMAN_REVIEW`. These are separate from reproducibility, and neither label implies a hosting-platform approval unless that approval is observed on the exact head SHA.

If uncommitted work cannot be transferred or identified safely, cross-machine verification is `VERIFICATION_BLOCKED`, not approximate proof.

## 11. PR/MR body template

```markdown
## Outcome
<observable result>

## Scope
- Changed: ...
- Explicitly included pre-existing work: none | ...
- Explicitly unchanged: ...

## Implementation
- ...

## Verification
| Check | Result |
| --- | --- |
| ... | PASS/LIMITED |

## Risk and recovery
- Risk tier: ...
- Main risk: ...
- Recovery: ...

## Limitations / follow-up
- none | ...

## Change Contract
`<id> v<version>`
```

Do not claim CI, approval, or merge readiness until observed for the latest remote head SHA. If a required gate cannot be observed, report `MERGE_READINESS_UNKNOWN`.
