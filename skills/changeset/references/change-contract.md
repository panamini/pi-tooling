# Change Contract Reference

Use this reference for `PLAN`, before `IMPLEMENT`, and whenever scope or acceptance criteria change.

## Contents

1. Contract principles
2. Risk and authorization
3. Canonical template
4. Baseline capture
5. Anti-stale decision
6. Contract amendments
7. Status rules

## 1. Contract principles

A Change Contract is a reviewable agreement about one atomic outcome. It is not a line-by-line prediction of the final patch.

A strong contract fixes:

- the desired observable outcome;
- invariants and non-goals;
- allowed and forbidden scope;
- required evidence;
- decisions that require human approval.

It may leave bounded discretion for naming, local code shape, or equivalent test mechanics. Over-specifying exact lines makes a plan fragile; under-specifying behavior makes it unverifiable.

Do not write a contract from filenames alone. Read the actual active path and enough context to know why each file is in scope.

## 2. Risk and authorization

Classify the highest applicable tier:

### `LOW`

Examples: isolated docs, comments, test-only maintenance, a local non-runtime cleanup with no public contract change.

Same-run implementation is allowed after a clear direct implementation request.

### `MEDIUM`

Examples: application behavior, shared library code, configuration, dependency/lockfile updates, public UI behavior, non-destructive schema additions.

Same-run implementation is allowed only when the behavior and acceptance criteria are unambiguous and the change is reversible. Otherwise require approval.

### `HIGH`

Examples: authentication or authorization, secrets, trust boundaries, payments, destructive or irreversible data migration, production infrastructure/deployment, public API compatibility breaks, cryptography, tenant isolation, privacy-sensitive data, broad concurrency or availability risk.

Require an exact contract approval before editing. Require stronger evidence and independent review. Never execute production mutations merely because implementation was authorized.

Raise the tier when blast radius, irreversibility, uncertainty, or weak testability warrants it.

## 3. Canonical template

Use this shape. Omit irrelevant subsections, but never omit outcome, scope, baseline, acceptance evidence, risk, and status.

```markdown
# CHANGE CONTRACT

- ID: CC-YYYYMMDD-<short-slug>
- Version: 1
- Operation: PLAN | IMPLEMENT
- Authorization basis: plan-only | direct implementation request | approved version
- Risk: LOW | MEDIUM | HIGH
- Status: READY_FOR_APPROVAL | AUTHORIZED_TO_IMPLEMENT | NEEDS_DECISION | BLOCKED

## 1. ATOMIC OUTCOME

One observable result. Include the target user/system behavior and why it matters.

### Non-goals
- ...

## 2. SOURCES OF TRUTH

- User request / issue / specification:
- Repository instructions:
- Existing tests or public contract:
- Conflicts or uncertainty:

## 3. INVARIANTS AND ASSUMPTIONS

### Must remain true
- ...

### Assumptions
- Observed: ...
- Inferred: ...
- Unverified: ...

### Decisions requiring approval
- None | ...

## 4. BASELINE

- Repository root:
- Git/non-Git workspace:
- Current branch:
- HEAD:
- Likely base ref:
- Worktree status summary:
- Applicable instruction files read:
- Target/context files read:
- File fingerprints:
- Stable anchors/symbols:
- Existing in-scope diff captured:

## 5. CURRENT STATE OBSERVED

Describe only verified behavior and code paths. Use symbols and semantic anchors; line numbers are secondary hints.

## 6. SCOPE

### Allowed files
| Path or pattern | Reason |
| --- | --- |
| ... | ... |

### Conditional files
| Path or pattern | Allowed only when |
| --- | --- |
| ... | ... |

### Forbidden scope
- ...

## 7. CHANGE DESIGN

### Required behavior
- ...

### Fixed implementation constraints
- ...

### Implementation discretion
- ...

### Intended patch by anchor
- `path` — symbol/anchor — add/change/remove ...

## 8. ACCEPTANCE AND EVIDENCE MATRIX

| ID | Binary criterion | Evidence type | Command or inspection | Expected result | Required |
| --- | --- | --- | --- | --- | --- |
| AC-1 | ... | structural/static/behavioral/negative/manual | ... | ... | yes/no |

## 9. FAILURE MODES AND LIMITS

- Risk:
  - Trigger:
  - Detection:
  - Mitigation:
- Known test gap or environment limit:

## 10. RECOVERY / ROLLBACK

Describe a non-destructive recovery strategy. Do not prescribe commands that may erase pre-existing user work. Prefer a small reversible commit, an inverse patch limited to agent-owned hunks, feature disablement, or `git revert` after explicit authorization.

## 11. BRANCH AND PR FRAMING

- Existing branch/worktree to use or proposed name:
- Base branch: observed | inferred | unverified
- Proposed PR title:
- PR summary:
- Reviewer focus:

## 12. APPROVAL

- Approval required: yes/no
- Exact version to approve: CC-... v1
- Smallest unresolved decision: none | ...
```

## 4. Baseline capture

Use repository-prescribed wrappers when present and available. Otherwise use native commands. Typical read-only Git evidence is:

```bash
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --porcelain=v1 -uall
git symbolic-ref --quiet --short refs/remotes/origin/HEAD
git diff --name-only
git diff --cached --name-only
git ls-files --others --exclude-standard
```

For every target and context file, record a stable semantic anchor and, when practical, a worktree content fingerprint:

```bash
git hash-object path/to/file
git diff --no-ext-diff -- path/to/file
git diff --cached --no-ext-diff -- path/to/file
```

For a missing file, record `ABSENT`. For a new untracked file, record its content hash and untracked status.

A line number without a function, class, command, route, test, key, or unique text anchor is not a durable baseline.

Capture applicable instruction files too. A changed instruction can invalidate the process even when target code is unchanged.

## 5. Anti-stale decision

Immediately before editing, compare the current state with the contract.

### Proceed

Proceed when all required anchors still resolve, observed files and instructions match their captured content, and any Git drift is unrelated to the contract after inspection.

Record unrelated drift as `DRIFT_REVALIDATED`; do not ignore it silently.

### `STALE_CONTRACT`

Stop when any of these is true:

- an in-scope or context file changed after the baseline without being part of the approved baseline;
- a required anchor disappeared, became ambiguous, or changed meaning;
- repository instructions or test/build commands changed materially;
- the requirement, public contract, or accepted behavior changed;
- a new file is required outside allowed or conditional scope;
- the approved contract version is not the latest version;
- current user work in an in-scope file cannot be separated safely from the intended patch.

A changed `HEAD` by itself is a revalidation trigger, not an automatic failure. Inspect:

```bash
git diff --name-only <baseline-head>..HEAD
```

If changes touch observed files, dependencies, tests, generated-source rules, or instructions relevant to the outcome, treat the contract as stale unless a new version is approved.

## 6. Contract amendments

Increment the version when changing any of these:

- atomic outcome or externally visible behavior;
- allowed, conditional, or forbidden scope;
- invariant or public compatibility expectation;
- risk tier;
- required acceptance criterion or evidence class;
- a human-approved design decision.

Do not increment for a mechanical choice already listed under implementation discretion, a corrected line number with the same anchor, or an unrelated revalidated `HEAD` drift.

When an implementation uncovers a new necessary change, stop, explain the discovery, and issue the smallest amended contract. Do not smuggle it into the current patch.

## 7. Status rules

- `READY_FOR_APPROVAL`: Contract is complete and testable, but the request did not authorize implementation or policy requires approval.
- `AUTHORIZED_TO_IMPLEMENT`: The exact version is authorized by a direct implementation request or explicit approval, and the risk gate allows execution.
- `NEEDS_DECISION`: A product, behavior, compatibility, data, or risk decision cannot be inferred safely.
- `BLOCKED`: Required repository access, artifact, tool, or safe workspace is unavailable.

Never use `AUTHORIZED_TO_IMPLEMENT` merely because the agent believes its own plan is good.
