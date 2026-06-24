# Git Safety Reference

Read before any branch, worktree, staging, commit, push, PR, history, or rollback operation.

## Contents

1. Safety boundary
2. Worktree classification
3. Branch and worktree strategy
4. Mixed ownership
5. Publication sequence
6. Prohibited defaults
7. Recovery
8. Cross-machine reproducibility

## 1. Safety boundary

Git state is user data. Treat tracked edits, staged changes, untracked files, branches, commits, remotes, hooks, and configuration as owned by the user unless this session created them explicitly.

Before mutation, inspect:

```bash
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --porcelain=v1 -uall
git diff --name-status
git diff --cached --name-status
git ls-files --others --exclude-standard
```

Do not assume `main`, `master`, `origin`, GitHub, or a clean worktree.

## 2. Worktree classification

### A. Clean

No tracked or untracked user changes. It is normally safe to use an existing dedicated branch or create one after implementation authorization.

### B. Dirty, unrelated

Uncommitted changes exist outside the contract scope.

- Do not switch branches if that may carry, overwrite, or conflict with them.
- Do not stash them.
- Keep all commands path-scoped.
- Prefer an isolated worktree only when it can be created from committed state and the requested change does not depend on the unrelated uncommitted work.
- Otherwise report the constraint and use an already suitable branch only when safe.

### C. Dirty, in scope, captured

The contract explicitly fingerprints the existing in-scope work and treats it as baseline. Proceed only while the fingerprint and diff remain unchanged. Preserve ownership boundaries in the final diff and staging.

### D. Dirty, in scope, uncaptured or changed

Stop with `STALE_CONTRACT` or `BLOCKED`. Never overwrite or reinterpret unknown user edits.

## 3. Branch and worktree strategy

Use this order:

1. Reuse an existing dedicated branch/worktree that clearly belongs to the same atomic outcome.
2. On a safe clean state, create a short branch that follows repository convention.
3. When unrelated work prevents safe branch use, consider a separate Git worktree, but only if the requested implementation does not rely on uncommitted state and workspace creation is permitted.
4. In a non-Git workspace, implement only when authorized and report that branch, commit, push, and PR gates are unavailable.

Do not create nested repositories. Do not initialize Git unless requested.

Branch creation is an implementation workspace action, not publication authorization. Do not push it unless requested.

## 4. Mixed ownership

A file may contain both pre-existing user hunks and agent-created hunks. File-level allowlisting does not make all hunks agent-owned.

Before staging, compare against the captured baseline and identify agent-owned hunks. If a file contains mixed ownership:

- use an interactive or patch-based staging method only when the harness can select the correct hunks reliably;
- inspect the staged diff afterward;
- otherwise stop before commit and report the mixed-ownership blocker.

Never use blanket staging such as:

```text
git add .
git add -A
git commit -a
```

Path-specific staging is acceptable only when the entire current file diff is intended and agent-owned.

## 5. Publication sequence

For an explicitly authorized commit/push/PR:

1. Re-run final required verification after the final edit.
2. Inspect all changed and untracked paths.
3. Stage only intended hunks/files.
4. Inspect:

```bash
git diff --cached --name-status
git diff --cached --stat
git diff --cached --check
git diff --cached
```

5. Confirm no required generated artifact, migration, lockfile, test, or documentation is missing.
6. Commit using repository conventions and active hooks/signing.
7. Confirm the resulting commit SHA and clean/expected status.
8. Push without force.
9. Create or update the PR/MR against the verified base.
10. Report local evidence separately from remote CI, approvals, conversations, and mergeability.

Use an available repository/hosting CLI only when installed, authenticated, and appropriate. Otherwise provide the exact PR body and remaining user action; do not pretend publication occurred.

A PR diff should be reviewed from the merge base to the topic head. Do not assume a two-dot diff represents what the hosting platform will show.

## 6. Prohibited defaults

Do not run these without a separate explicit request, a stated reason, and a safety check:

- `git reset --hard` or any reset that discards work;
- `git clean`;
- `git checkout -- <path>` or `git restore <path>`;
- `git stash`, including autostash;
- branch deletion;
- rebase, amend, filter-branch, filter-repo, or other history rewriting;
- force push, including `--force-with-lease`;
- hook bypass such as `--no-verify`;
- changing global/system Git configuration;
- changing credentials, remotes, signing configuration, or hooks;
- merging a PR.

A user request to “fix it” is not permission for destructive Git recovery or history rewriting.

## 7. Recovery

Rollback instructions must preserve pre-existing work.

### Uncommitted agent-owned change

Prefer an inverse patch limited to hunks created in this session. Show the affected diff before applying it. If ownership cannot be established, do not automate rollback.

### Committed change

Prefer a new reverting commit with `git revert <sha>` after explicit authorization, especially once shared. Do not reset a published branch to simulate rollback.

### Feature/config change

When available, use a documented feature flag, configuration reversal, or migration rollback that has been tested in a non-production environment.

Never present `git restore` as a generic rollback command: it can erase user work that predates the agent.

## 8. Cross-machine reproducibility

A second workstation is useful only when it verifies the same artifact.

Record:

- exact commit SHA, or a cryptographic hash of the supplied patch/worktree snapshot;
- base ref/SHA;
- relevant toolchain/runtime versions;
- command and environment differences;
- whether dependencies and generated artifacts were reproduced from a clean checkout.

Different hardware or a fresh checkout tests reproducibility. A different reviewer/context tests independence. They are separate properties.

If the work is still uncommitted, another machine cannot verify it exactly without an exported patch or equivalent snapshot. Do not compare two loosely similar worktrees and call that independent verification.
