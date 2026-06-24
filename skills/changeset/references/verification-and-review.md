# Verification and Review Reference

Use for final implementation evidence, standalone verification, code review, and publication gates.

## Contents

1. Evidence model
2. Verification depth by risk
3. Freshness and baseline failures
4. Verification procedure
5. Review artifact and diff range
6. Two-pass review
7. Finding quality and severity
8. Independence and invalidation
9. Output templates
10. PR body template

## 1. Evidence model

Map every acceptance criterion to at least one suitable evidence class.

### Structural

Proves files, symbols, routes, keys, generated artifacts, or removals exist as expected. Examples: diff inspection, targeted search, schema inspection.

Structural evidence does not prove runtime behavior.

### Static

Proves parse/syntax, formatting, lint, types, compilation, policy, or schema validation. Use the repository's actual commands.

### Behavioral

Proves an observable outcome through a focused unit, integration, end-to-end, smoke, or isolated manual check. Inspect assertions and output, not only process success.

### Negative

Proves an obsolete path, call, secret, warning, unsafe fallback, or duplicate behavior is absent. Absence searches are useful but must use a scope where absence is meaningful.

### Operational/manual

Proves behavior that automation cannot safely exercise. State exact steps, expected observation, environment, and whether it was actually performed.

No single evidence class is universally sufficient.

## 2. Verification depth by risk

### `LOW`

Minimum:

- complete diff and changed-path inspection;
- syntax/format/doc build or equivalent when relevant;
- focused check for the changed artifact;
- `git diff --check` in Git repositories.

### `MEDIUM`

Minimum:

- all LOW checks;
- focused behavioral test or a justified equivalent;
- affected lint/typecheck/build/test slice;
- negative or compatibility evidence where behavior is removed/replaced;
- broader suite when code is shared or user-facing.

### `HIGH`

Minimum:

- all MEDIUM checks;
- exact approved contract and independent review;
- domain-specific security/data/migration/compatibility checks;
- clean or reproducible environment when practical;
- explicit rollback/containment evidence;
- no production execution without separate authorization and operational procedure.

Increase depth for high blast radius even when the patch is small.

## 3. Freshness and baseline failures

Evidence is valid only for the final artifact.

- Record the worktree fingerprint or exact commit SHA being verified.
- After any code/config/test/generated-file change, re-run affected required checks.
- After a new commit/push, remote checks must correspond to the latest commit SHA.
- Do not reuse test output from before the final edit.

When a test fails:

1. Capture the command, exit code, and relevant output.
2. Determine whether it is introduced by the change, pre-existing on the recorded baseline, environmental, flaky, or unknown.
3. Reproduce on the baseline only when safe and useful; do not destroy the current worktree to do so.
4. A pre-existing failure is not a pass. Report it as a limitation and apply repository policy to the PR gate.
5. Never dismiss a failure as “unrelated” without evidence.

## 4. Verification procedure

1. Identify the artifact: worktree, patch hash, commit SHA, branch head, or PR head.
2. Load the approved contract or reconstruct explicit acceptance criteria from the request.
3. Inspect changed tracked paths, staged paths, and relevant untracked files.
4. Check scope before behavior: unexpected files are a failure even when tests pass.
5. Run the narrowest high-signal checks first.
6. Run broader checks required by risk and blast radius.
7. Inspect outputs and observable outcomes.
8. Fill the evidence matrix criterion by criterion.
9. List limitations and checks not run with reasons.
10. Issue one status without overstating merge readiness.

Suggested evidence matrix:

```markdown
| Criterion | Evidence | Expected | Observed | Result |
| --- | --- | --- | --- | --- |
| AC-1 | command/inspection | ... | ... | PASS/FAIL/NOT_RUN/LIMITED |
```

A grep-only criterion is acceptable for a purely structural requirement. It is insufficient for a behavioral requirement.

Avoid destructive proof construction. Use temporary directories, ephemeral environment variables, isolated fixtures, test databases, mocks/fakes, or disposable containers when repository policy permits.

## 5. Review artifact and diff range

Review exactly what is proposed.

### Committed branch or PR

Determine the verified base ref and merge base, then inspect the introduced three-dot-equivalent diff and commit list. Confirm the head SHA.

Typical read-only commands:

```bash
git merge-base <base-ref> HEAD
git diff --stat <base-ref>...HEAD
git diff --name-status <base-ref>...HEAD
git diff <base-ref>...HEAD
git log --oneline --decorate <base-ref>..HEAD
```

### Uncommitted worktree

Inspect all components:

```bash
git diff --stat
git diff
git diff --cached --stat
git diff --cached
git ls-files --others --exclude-standard
```

Read relevant untracked files directly. `git diff HEAD` does not include their contents.

If the base is unknown, report it as a review limitation rather than guessing.

## 6. Two-pass review

### Pass A: Contract/spec compliance

Check:

- every required outcome and acceptance criterion;
- allowed, conditional, and forbidden scope;
- invariant preservation and public compatibility;
- tests/docs/migrations/generated artifacts required by the contract;
- hidden extra behavior or omitted behavior;
- evidence quality and unverified claims.

### Pass B: Engineering risk

Inspect only relevant dimensions:

- correctness and edge cases;
- error handling and failure recovery;
- security, permissions, trust boundaries, secrets, privacy;
- data integrity, migrations, backward/forward compatibility;
- concurrency, idempotency, ordering, retries, timeouts;
- performance and resource use;
- operational observability and deployment behavior;
- API/UI/accessibility compatibility;
- test quality, false positives, and missing regression coverage;
- maintainability only where it creates a concrete defect risk.

Do not expand into an audit of untouched code.

## 7. Finding quality and severity

Report findings first. Use:

- `BLOCKER`: likely severe security/data loss/outage or the requested outcome is fundamentally not met.
- `HIGH`: concrete correctness/security/compatibility failure likely in realistic use.
- `MEDIUM`: bounded defect, missing case, or meaningful regression risk.
- `LOW`: worthwhile non-blocking issue with concrete impact.

Every finding must include:

1. severity and concise title;
2. file and stable line/symbol location;
3. concrete trigger or failure scenario;
4. observed evidence and why it matters;
5. smallest bounded recommendation.

Do not report:

- preference-only style comments;
- vague “could be cleaner” claims;
- issues unrelated to the introduced diff unless they directly block it;
- speculative failures without a plausible trigger;
- duplicate manifestations of the same root cause.

When there are no findings, state that explicitly and still list test/evidence limitations.

Use review outcomes:

- `APPROVE`: no blocking finding and required evidence is adequate for review.
- `COMMENT`: no blocking finding, but limitations or non-blocking findings remain.
- `REQUEST_CHANGES`: at least one blocking/high-confidence issue must be fixed before readiness.

## 8. Independence and invalidation

A reviewer should receive the requirement/contract, base and head identities, and the diff—not merely the implementer's success narrative.

When supported, use a fresh read-only reviewer or subagent. The reviewer must not edit code. If only self-review is possible, label it `SELF_REVIEW`; do not describe it as independent.

Do not run duplicate reviews on an unchanged artifact. Do re-review when:

- the diff changes after review;
- the base or head SHA changes materially;
- a finding is fixed;
- acceptance criteria or scope change.

After a post-review change, re-run affected verification before issuing a new review outcome.

## 9. Output templates

### Implementation/final verification report

```markdown
# EXECUTION REPORT — <contract-id> v<version>

- Authorization:
- Baseline result: MATCH | DRIFT_REVALIDATED | STALE
- Branch/worktree:
- Final artifact: worktree hash | commit SHA
- Files changed:
- Unexpected files: none | ...

## Commands and results
| Command | Exit | Relevant result |
| --- | ---: | --- |
| ... | ... | ... |

## Acceptance evidence
| Criterion | Evidence | Observed | Result |
| --- | --- | --- | --- |
| ... | ... | ... | PASS/FAIL/NOT_RUN/LIMITED |

## Diff and risk summary
- ...

## Limitations
- none | ...

## Status
LOCAL_PASS | LOCAL_PASS_WITH_LIMITATIONS | LOCAL_FAIL | STALE_CONTRACT
```

### Standalone review report

```markdown
# REVIEW — <artifact identity>

## Findings
1. [SEVERITY] Title — `path:anchor`
   - Trigger:
   - Evidence/impact:
   - Recommendation:

## Open questions
- none | ...

## Evidence/test gaps
- none | ...

## Review identity
INDEPENDENT_REVIEW | SELF_REVIEW

## Outcome
APPROVE | COMMENT | REQUEST_CHANGES
```

## 10. PR body template

```markdown
## Outcome
<observable result>

## Scope
- Changed: ...
- Explicitly unchanged: ...

## Implementation
- ...

## Verification
| Check | Result |
| --- | --- |
| ... | PASS/LIMITED |

## Risk and rollback
- Risk tier: ...
- Main risk: ...
- Recovery: ...

## Limitations / follow-up
- none | ...

## Change Contract
`<id> v<version>`
```

Do not claim CI, approval, or merge readiness until observed on the latest remote head SHA.
