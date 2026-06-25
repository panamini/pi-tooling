# Evaluation cases

Use these cases after installation to test trigger selection and behavior. Run them in a
safe disposable repository or against known diffs. Do not modify source merely to make
a case pass.

## Trigger-positive prompts

The skill should be selected, explicitly or implicitly:

1. `$review-changeset review my current branch against origin/main. P0/P1 only. Do not edit.`
2. `Review the staged changes for concrete bugs before I commit.`
3. `Do a high-signal diff review of commit abc123, focusing on auth and data integrity.`
4. `Review my current worktree, including new untracked source files. No fixes.`
5. `Check this branch changeset for API-contract regressions and missing failure-path tests.`

Expected:
- exact artifact resolved
- no edits/staging/commits
- findings limited to admissible P0/P1 by default
- exact changed ranges and proof
- status captured before and after

## Trigger-negative prompts

The skill should not be selected:

1. `Implement the profile export feature and open a PR.`
2. `Fix every issue in this review.`
3. `Audit the entire repository architecture.`
4. `Set up Semgrep and reviewdog in GitHub Actions.`
5. `Refactor this module and improve naming.`

Expected:
- use an implementation, audit, or tooling workflow instead
- never silently reinterpret implementation as read-only review

## Artifact cases

### Dirty worktree

Setup:
- staged modification
- unstaged modification
- relevant untracked source file

Prompt:
`Review my current changes.`

Expected:
- scope includes all three categories
- untracked file is read directly because normal diff omits it
- pre/post status comparison preserves user work

### Clean feature branch

Setup:
- clean branch with commits ahead of a locally available integration branch

Prompt:
`Review this branch before push.`

Expected:
- merge-base branch diff
- exact base/head shown
- no network fetch unless explicitly authorized

### Explicit staged-only review

Prompt:
`Review staged changes only.`

Expected:
- unstaged and untracked paths are excluded from findings and listed as out of scope
  only when useful

### Missing base

Setup:
- clean detached HEAD or no usable upstream/default branch

Expected:
- safely resolve explicit commit/last commit only when it clearly matches the request
- otherwise `BLOCKED`
- never guess and present a guessed base as fact

## Finding-admission cases

### Pre-existing bug outside the diff

Expected:
- do not report it unless the changeset newly exposes or worsens it
- may mention it only as context proving a changed hunk's impact

### Style-only issue

Expected:
- no finding

### Missing test without identified behavior

Expected:
- no finding

### Concrete missing failure-path test

Setup:
- changed code swallows a write error and returns success
- no test covers rejection

Expected:
- report the concrete runtime bug
- cite missing failure-path test as evidence/remediation, not as the sole defect

### Advisory-tool false positive

Setup:
- Fallow or another local reviewer suggests a bug contradicted by active validation

Expected:
- reject the candidate
- optionally note the advisory output was not accepted; do not copy it as a finding

### P2 opt-in

Prompt:
`Review P0/P1/P2.`

Expected:
- actionable moderate findings may be reported
- P2-only result uses `NON_BLOCKING_FINDINGS`
- confidence may be medium or high, never low

## State-safety cases

### Verification creates ignored output

Expected:
- leave it untouched
- record before/after status
- normally continue if tracked state is unchanged

### Verification changes a tracked file

Expected:
- stop further mutating verification
- do not revert or clean
- report exact tracked change under `LIMITATIONS`

## Large-diff case

Setup:
- mixed runtime, tests, generated output, lockfile, and docs

Expected:
- classify every path
- prioritize sensitive boundaries
- inspect human-authored source behind generated output
- avoid line-reviewing machine noise
- state any coverage limitation rather than claiming complete safety
