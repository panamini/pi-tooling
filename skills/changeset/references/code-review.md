# Code Review Reference

Use for read-only review of a worktree, patch, branch, commit range, or PR/MR. Review only the proposed artifact and relevant surrounding code.

## Contents

- 1. Establish the review artifact
- 2. Two-pass review
- 3. Finding quality and severity
- 4. Review outcome
- 5. Independence and invalidation
- 6. Output template

## 1. Establish the review artifact

Review exactly what is proposed, not the implementer's narrative.

Record:

- requirement or Change Contract;
- repository and candidate base identity;
- exact head SHA, patch hash, or worktree fingerprint;
- reviewer identity (`SELF_REVIEW`, `FRESH_AGENT_REVIEW`, or `HUMAN_REVIEW`) and whether any remote review action was actually observed;
- known evidence/test limitations.

### Committed branch or PR/MR

Determine the verified base ref and merge base, then inspect the introduced three-dot-equivalent diff and commit list:

```bash
git merge-base <base-ref> HEAD
git --no-pager diff --no-ext-diff --no-textconv --stat <base-ref>...HEAD
git --no-pager diff --no-ext-diff --no-textconv --name-status <base-ref>...HEAD
git --no-pager diff --no-ext-diff --no-textconv <base-ref>...HEAD
git --no-pager log --oneline --decorate <base-ref>..HEAD
```

Confirm the actual head SHA. If provider metadata is available, compare it to the local base/head rather than assuming they match.

### Uncommitted worktree

Inspect all components:

```bash
git --no-pager diff --no-ext-diff --no-textconv --stat
git --no-pager diff --no-ext-diff --no-textconv
git --no-pager diff --no-ext-diff --no-textconv --cached --stat
git --no-pager diff --no-ext-diff --no-textconv --cached
git ls-files --others --exclude-standard
```

Read relevant untracked files directly without dumping secret-bearing content into the report. `git diff HEAD` does not show untracked contents. If the base is unknown, report that limitation rather than guessing.

## 2. Two-pass review

### Pass A: Contract/spec compliance

Check:

- every required outcome and acceptance criterion;
- allowed, conditional, forbidden, and explicitly included pre-existing scope;
- invariant preservation and public compatibility;
- required tests/docs/migrations/generated artifacts;
- hidden extra behavior or omitted behavior;
- evidence quality and unverified success claims.

### Pass B: Engineering risk

Inspect only relevant dimensions:

- correctness and edge cases;
- error handling and failure recovery;
- security, permissions, trust boundaries, secrets, privacy;
- data integrity, migrations, backward/forward compatibility;
- concurrency, idempotency, ordering, retries, and timeouts;
- performance and resource use;
- observability and deployment behavior;
- API/UI/accessibility compatibility;
- test quality, false positives, and missing regression coverage;
- maintainability only where it creates concrete defect risk.

Do not expand into an audit of untouched code.

## 3. Finding quality and severity

Report findings first.

- `BLOCKER`: likely severe security/data loss/outage, or requested outcome fundamentally unmet.
- `HIGH`: concrete correctness/security/compatibility failure likely in realistic use.
- `MEDIUM`: bounded defect, missing case, or meaningful regression risk.
- `LOW`: worthwhile non-blocking issue with concrete impact.

Every finding must include:

1. severity and concise title;
2. file and stable line/symbol location;
3. concrete trigger or failure scenario;
4. observed evidence and why it matters;
5. smallest bounded recommendation.

Do not report preference-only style comments, vague cleanliness claims, unrelated pre-existing issues, speculative failures without a plausible trigger, or duplicate symptoms of one root cause.

When there are no findings, state that explicitly and still list evidence/test limitations.

## 4. Review outcome

- `LOCAL_REVIEW_CLEAR`: no actionable blocking finding and required evidence is adequate.
- `LOCAL_REVIEW_NOTES`: only non-blocking findings, open questions, or optional evidence limitations remain.
- `LOCAL_REVIEW_CHANGES_REQUIRED`: any `BLOCKER`/`HIGH`, or a `MEDIUM` that violates a required outcome/invariant or creates a realistic regression that must be fixed before readiness.

A required verification gap may justify `LOCAL_REVIEW_CHANGES_REQUIRED` even when no code defect is proven. These are local analytical verdicts. Submitting approve/comment/request-changes to a hosting provider is a separate authorized `PUBLISH` action. Never submit a remote approval unless the current exact artifact has `LOCAL_REVIEW_CLEAR` and adequate required evidence.

## 5. Independence and invalidation

A reviewer should receive the requirement/contract, base/head identities, and actual diff—not only the implementation report.

Use a fresh read-only reviewer or subagent when available and warranted. Record identities precisely:

- `SELF_REVIEW`: the implementing context reviews its own work; never satisfies an independence requirement.
- `FRESH_AGENT_REVIEW`: a separate automated context reviews the artifact; it is context-separated, not human or hosting-platform approval, and satisfies an independence gate only when policy permits automated review.
- `HUMAN_REVIEW`: a human reviewed the artifact; do not claim a hosting-platform approval unless it was observed on the exact head SHA.

Do not mechanically repeat the same self-review on an unchanged artifact. A second context-separated or human review of the same artifact is valid and may be required for high risk because reviewer diversity tests a different property from environment reproducibility. Record each reviewer/context identity.

Re-review when:

- the diff changes;
- base or head identity changes materially;
- a finding is fixed;
- acceptance criteria or scope change;
- a previously missing required artifact becomes available.

After a post-review change, re-run affected verification before issuing a new review outcome. For `HIGH` risk, a context-separated review is required before `MERGE_READY`; opening a ready-for-review PR may precede that review unless policy or the contract requires a pre-publication gate.

## 6. Output template

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

## Scope and artifact identity
- Base:
- Head/fingerprint:
- Unexpected paths: none | ...

## Review identity
SELF_REVIEW | FRESH_AGENT_REVIEW | HUMAN_REVIEW

## Outcome
LOCAL_REVIEW_CLEAR | LOCAL_REVIEW_NOTES | LOCAL_REVIEW_CHANGES_REQUIRED
```
