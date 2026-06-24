# Verification Reference

Use for final implementation evidence, standalone verification, and publication gates.

## Contents

- 1. Evidence model
- 2. Required versus optional evidence
- 3. Verification depth by risk
- 4. Freshness and artifact identity
- 5. Command safety during verification
- 6. Failure classification
- 7. Verification procedure
- 8. Status definitions
- 9. Output templates

## 1. Evidence model

Map every acceptance criterion to at least one suitable evidence class.

### Structural

Proves files, symbols, routes, keys, generated artifacts, or removals exist as expected through diff/search/schema inspection. Structural evidence does not prove runtime behavior.

### Static

Proves syntax, formatting, lint, types, compilation, policy, or schema validity using actual repository commands.

### Behavioral

Proves an observable outcome through focused unit, integration, end-to-end, smoke, or isolated manual checks. Inspect assertions and output, not only process success.

### Negative

Proves an obsolete path, unsafe fallback, warning, duplicate behavior, or secret is absent. Use a scope where absence is meaningful.

### Operational/manual

Proves behavior automation cannot safely exercise. State exact steps, expected observation, environment, and whether they were actually performed.

No evidence class is universally sufficient. A grep-only criterion is valid only for a purely structural requirement.

## 2. Required versus optional evidence

The Change Contract marks each criterion required or optional.

- `PASS`: expected result observed on the final artifact.
- `FAIL`: expected result not observed.
- `NOT_RUN`: check was not executed.
- `LIMITED`: check ran or inspection occurred, but evidence is incomplete or environment-constrained.

A required criterion that is `FAIL` prevents success. A required criterion that is `NOT_RUN` or materially `LIMITED` prevents a verified/pass status and produces a blocked/incomplete status.

Use limitation statuses only when all required criteria pass and the remaining limitations are optional, remote, informational, or explicitly non-gating:

- `LOCAL_PASS_WITH_LIMITATIONS`
- `VERIFIED_WITH_LIMITATIONS`

Use blocked statuses when required evidence cannot be obtained safely:

- `LOCAL_BLOCKED`
- `VERIFICATION_BLOCKED`

Never downgrade missing required evidence into a cosmetic limitation.

## 3. Verification depth by risk

### `LOW`

Minimum:

- complete change-set and changed-path inspection;
- syntax/format/doc build or equivalent when relevant;
- focused check for the changed artifact;
- `git --no-pager diff --no-ext-diff --no-textconv --check` in Git repositories.

### `MEDIUM`

Minimum:

- all `LOW` checks;
- focused behavioral test or justified equivalent;
- affected lint/typecheck/build/test slice;
- negative/compatibility evidence when behavior is removed or replaced;
- broader suite when shared or user-facing code creates wider blast radius.

### `HIGH`

Minimum:

- all `MEDIUM` checks;
- exact approved contract and artifact identity;
- domain-specific security/data/migration/compatibility checks;
- clean or reproducible environment when practical;
- explicit recovery/containment evidence;
- no production execution without separate operational authorization.

Review is a separate gate, not an evidence class. `HIGH` risk requires context-separated review before `MERGE_READY`, plus human review/approval whenever repository or domain policy requires it; an earlier gate applies only when the contract or policy says so. Missing required review can block publication or merge readiness without falsifying otherwise complete local verification.

Increase depth for high blast radius even when the patch is small.

## 4. Freshness and artifact identity

Evidence is valid only for the final artifact.

- Identify a worktree fingerprint, patch hash, commit SHA, branch head, or PR/MR head.
- Prefer commit SHA for cross-machine or remote verification.
- For uncommitted work, use the bundled fingerprint tool when appropriate; record the digest type, `complete` value, ignored-path/external-environment exclusions, and any index visibility flags. For high-confidence identity, compare two consecutive complete `state_sha256` results without intervening actions.
- After any code, config, test, lockfile, migration, or generated-file change, re-run affected required checks.
- After commit hooks alter content, verify the actual commit before push.
- After a new commit/push, remote checks must correspond to the latest head SHA.
- Do not reuse output from before the final edit.

A changed artifact invalidates only affected evidence, but scope/diff inspection must always be refreshed.

## 5. Command safety during verification

Verification is read-only with respect to source, index, branches, remotes, production, and external services.

Before running a repository-defined command, inspect its actual script/task definition when practical and treat it as code execution. Redact credentials, tokens, private keys, and personal data from captured output.

Before running a command, distinguish:

- read-only inspection/test;
- known disposable ignored output (for example an isolated cache/build directory);
- source/index mutation (`--fix`, snapshot update, formatter write mode, codegen, install/lockfile update);
- external mutation (deployment, migration, API write, shared database).

Do not run the last two categories without matching implementation/operational authorization and scope.

Capture repository status before and after checks. If a supposedly read-only command changes tracked, staged, or relevant untracked content unexpectedly:

1. stop the verification sequence;
2. preserve the change;
3. report the command and changed paths;
4. classify the result as blocked or failed;
5. never clean or restore automatically.

## 6. Failure classification

When a check fails:

1. capture command, exit code, and relevant output;
2. determine whether it is introduced, reproducible on baseline, environmental, flaky, or unknown;
3. reproduce on baseline only when safe and useful without destroying current work;
4. treat pre-existing failure as a limitation, never a pass;
5. do not call a failure “unrelated” without evidence.

A required check that fails on both baseline and final artifact may be non-regression evidence, but repository policy still determines whether publication is allowed. Report both facts.

## 7. Verification procedure

1. Identify the exact artifact.
2. Load the approved contract or reconstruct explicit acceptance criteria from the current request.
3. Inspect the complete supplied artifact. Include staged, unstaged, and relevant untracked content only for a worktree artifact; for a commit, branch, or PR/MR, use its exact base/head identity and report unrelated workspace dirt separately.
4. Check scope before behavior; unexpected paths are a failure or blocker even when tests pass.
5. Run the narrowest high-signal checks first.
6. Run broader checks required by risk/blast radius.
7. Inspect assertions, output, and observable behavior.
8. Re-check status for unexpected command side effects.
9. Fill the evidence matrix criterion by criterion.
10. List checks not run and reasons.
11. Issue one status using the required/optional rules.

Suggested matrix:

```markdown
| Criterion | Required | Evidence | Expected | Observed | Result |
| --- | --- | --- | --- | --- | --- |
| AC-1 | yes | command/inspection | ... | ... | PASS/FAIL/NOT_RUN/LIMITED |
```

Avoid destructive proof construction. Prefer temporary directories, ephemeral environment variables, isolated fixtures, test databases, mocks/fakes, or disposable containers allowed by repository policy.

## 8. Status definitions

### Implementation/local

- `LOCAL_PASS`: all required local criteria pass on the final artifact; no material local limitation.
- `LOCAL_PASS_WITH_LIMITATIONS`: all required local criteria pass; only optional/remote/non-gating limitations remain.
- `LOCAL_FAIL`: at least one required criterion fails or scope is violated.
- `LOCAL_BLOCKED`: required evidence cannot be obtained safely or the environment/tool is unavailable.
- `STALE_CONTRACT`: baseline/authorization contract no longer matches.

### Standalone verification

- `VERIFIED`: all required criteria pass for the identified artifact.
- `VERIFIED_WITH_LIMITATIONS`: all required criteria pass; only optional/non-gating limitations remain.
- `VERIFICATION_FAILED`: at least one required criterion fails or artifact scope is invalid.
- `VERIFICATION_BLOCKED`: required evidence or exact artifact identity is unavailable.
- `STALE_CONTRACT`: verification is against a superseded contract/artifact.

A `*_WITH_LIMITATIONS` status is not a substitute for missing required evidence.

## 9. Output templates

### Implementation report

```markdown
# EXECUTION REPORT — <contract-id> v<version>

- Authorization evidence:
- Baseline result: MATCH | DRIFT_REVALIDATED | STALE
- Branch/worktree:
- Final artifact: worktree/index/state fingerprint | commit SHA
- Files changed:
- Unexpected files: none | ...

## Commands and results
| Command | Exit | Relevant result |
| --- | ---: | --- |
| ... | ... | ... |

## Acceptance evidence
| Criterion | Required | Evidence | Observed | Result |
| --- | --- | --- | --- | --- |
| ... | yes/no | ... | ... | PASS/FAIL/NOT_RUN/LIMITED |

## Diff and risk summary
- ...

## Limitations
- none | ...

## Status
LOCAL_PASS | LOCAL_PASS_WITH_LIMITATIONS | LOCAL_FAIL | LOCAL_BLOCKED | STALE_CONTRACT
```

### Standalone verification report

```markdown
# VERIFICATION — <artifact identity>

- Contract/request:
- Artifact identity:
- Baseline/base identity:
- Scope result:

## Acceptance evidence
| Criterion | Required | Evidence | Observed | Result |
| --- | --- | --- | --- | --- |
| ... | yes/no | ... | ... | PASS/FAIL/NOT_RUN/LIMITED |

## Failures and limitations
- none | ...

## Status
VERIFIED | VERIFIED_WITH_LIMITATIONS | VERIFICATION_FAILED | VERIFICATION_BLOCKED | STALE_CONTRACT
```
