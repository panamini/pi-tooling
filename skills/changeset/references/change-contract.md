# Change Contract Reference

Use for `PLAN`, before `IMPLEMENT`, and whenever scope, risk, or acceptance criteria change.

## Contents

- 1. Contract principles
- 2. Risk and authorization
- 3. Canonical template
- 4. Compact same-run contract
- 5. Baseline capture
- 6. Anti-stale decision
- 7. Contract amendments
- 8. Status rules

## 1. Contract principles

A Change Contract is a reviewable agreement for one atomic outcome. It fixes observable behavior, invariants, scope, required evidence, and decisions needing approval. It is not a brittle line-by-line prediction of the final patch.

Allow bounded discretion for naming, local code shape, or equivalent test mechanics. Over-specifying exact lines makes a contract stale too easily; under-specifying behavior makes it unverifiable.

Do not write a contract from filenames alone. Read the active path and enough context to justify each in-scope file.

## 2. Risk and authorization

Classify the highest applicable tier.

### `LOW`

Examples: isolated docs/comments, test-only maintenance, or local non-runtime cleanup without public contract change.

A clear direct implementation request may authorize same-run implementation.

### `MEDIUM`

Examples: application behavior, shared library code, configuration, dependencies/lockfiles, public UI behavior, or non-destructive schema additions.

Same-run implementation is allowed only when behavior and acceptance criteria are unambiguous and reversible. Otherwise require exact approval.

### `HIGH`

Examples: authentication/authorization, secrets, trust boundaries, payments, destructive or irreversible data migration, production infrastructure/deployment, public API breaks, cryptography, tenant isolation, privacy-sensitive data, or broad concurrency/availability risk.

Require exact contract approval before editing and stronger evidence. Require a context-separated review before `MERGE_READY`, and earlier only when repository policy, domain policy, the user, or the contract explicitly requires it; require human review or approval wherever policy demands it. A fresh agent is not a human approval. Implementation authorization never authorizes a production mutation.

Raise risk for high blast radius, irreversibility, uncertainty, weak observability, or weak testability even when the patch is small.

## 3. Canonical template

Omit irrelevant subsections, but never omit outcome, scope, baseline, acceptance evidence, risk, authorization, and status.

```markdown
# CHANGE CONTRACT

- ID: CC-YYYYMMDD-<short-slug>
- Version: 1
- Operation: PLAN | IMPLEMENT
- Authorization basis: plan-only | direct implementation request | approved version
- Authorization evidence: exact user instruction or approval reference
- Risk: LOW | MEDIUM | HIGH
- Status: READY_FOR_APPROVAL | AUTHORIZED_TO_IMPLEMENT | NEEDS_DECISION | BLOCKED

## 1. ATOMIC OUTCOME

One observable result, target behavior, and why it matters.

### Non-goals
- ...

## 2. SOURCES OF TRUTH

- Current user request:
- Issue/specification:
- Repository instructions:
- Existing tests/public contract:
- Conflicts or uncertainty:

## 3. INVARIANTS, ASSUMPTIONS, DECISIONS

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
- Branch state: <name> | DETACHED | UNBORN
- HEAD: <sha> | UNBORN
- Candidate base ref(s): observed | inferred | unverified, with evidence
- Worktree status summary:
- Applicable instruction files read/fingerprinted:
- Target/context files read/fingerprinted:
- Stable anchors/symbols:
- Existing in-scope diff captured:
- Worktree fingerprint: unavailable | worktree/index/state SHA-256

## 5. CURRENT STATE OBSERVED

Verified behavior and active code paths only. Use symbols and semantic anchors; line numbers are secondary hints.

## 6. SCOPE

### Allowed files
| Path or pattern | Reason |
| --- | --- |
| ... | ... |

### Conditional files
| Path or pattern | Allowed only when |
| --- | --- |
| ... | ... |

### Explicitly included pre-existing changes
| Path/hunk | Authorization/evidence |
| --- | --- |
| none | ... |

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

| ID | Binary criterion | Evidence class | Command/inspection | Expected | Required |
| --- | --- | --- | --- | --- | --- |
| AC-1 | ... | structural/static/behavioral/negative/manual | ... | ... | yes/no |

## 9. FAILURE MODES AND LIMITS

- Risk:
  - Trigger:
  - Detection:
  - Mitigation:
- Known environment or test gap:

## 10. RECOVERY / ROLLBACK

A non-destructive recovery strategy. Do not prescribe commands that may erase pre-existing work. Prefer inverse patches limited to authorized session hunks, a small revert commit after authorization, documented feature disablement, or a tested migration rollback.

## 11. BRANCH AND PR FRAMING

- Existing branch/worktree or proposed name:
- Base branch: observed | inferred | unverified
- Proposed PR title:
- PR summary:
- Reviewer focus:

## 12. APPROVAL

- Approval required: yes/no
- Exact version to approve: CC-... v1
- Smallest unresolved decision: none | ...
```

## 4. Compact same-run contract

Use this only for a clear direct implementation request when all of the following hold:

- risk is `LOW` or reversible `MEDIUM`;
- outcome and acceptance criteria are unambiguous;
- no product, design, data, security, or compatibility decision remains;
- current in-scope work is clean or exactly captured and authorized;
- the work can be completed and verified in the current session.

Record it before editing even when it is not expanded into a long user-facing plan:

```markdown
# COMPACT CHANGE CONTRACT

- ID / Version:
- Authorization evidence:
- Risk: LOW | MEDIUM
- Status: AUTHORIZED_TO_IMPLEMENT
- Atomic outcome:
- Non-goals:
- Sources of truth / invariants:
- Baseline: repository, branch/HEAD, status, applicable instructions, target fingerprints, stable anchors, included existing diff
- Scope: allowed | conditional triggers | forbidden | explicitly included pre-existing hunks
- Patch intent by stable anchor:
- Acceptance/evidence matrix: criterion | evidence | expected | required
- Recovery:
```

If any qualifying condition stops being true, stop and issue the smallest canonical contract version or amendment. Do not stretch the compact form to hide risk or ambiguity.

## 5. Baseline capture

Use repository-prescribed wrappers only when present, required, and available. Otherwise use native commands.

Typical read-only Git evidence:

```bash
git rev-parse --show-toplevel
git symbolic-ref --quiet --short HEAD
git rev-parse --verify HEAD
git -c core.fsmonitor=false status --porcelain=v1 -uall
git --no-pager diff --no-ext-diff --no-textconv --name-status
git --no-pager diff --no-ext-diff --no-textconv --cached --name-status
git ls-files --others --exclude-standard
git for-each-ref --format='%(refname:short) %(symref:short)' 'refs/remotes/*/HEAD'
```

Interpret failures rather than hiding them:

- empty/failed symbolic-ref with valid `HEAD` → `DETACHED`;
- failed `git rev-parse --verify HEAD` in a Git worktree → `UNBORN`;
- no remote HEAD ref → base remains inferred or unverified, not assumed to be `origin/main`.

For target files and material context files, record a stable semantic anchor and, when practical, a worktree content fingerprint:

```bash
git hash-object -- path/to/file
git --no-pager diff --no-ext-diff --no-textconv -- path/to/file
git --no-pager diff --no-ext-diff --no-textconv --cached -- path/to/file
```

For a missing file, record `ABSENT`. For an untracked file, record its content hash and untracked status. A line number without a function, class, command, route, test, key, or unique text anchor is not durable.

Capture applicable instruction files too. A changed instruction can invalidate the process even when target code is unchanged.

### Base-ref evidence order

Do not assume `main`, `master`, `origin`, or any hosting provider.

Prefer, in order:

1. base metadata from the existing PR/MR;
2. explicit repository instructions or task/issue metadata;
3. a configured repository default remote HEAD observed locally;
4. a clearly documented project convention;
5. an inferred candidate, labeled `inferred`;
6. `unverified` when evidence is insufficient.

A feature branch's upstream is not automatically its PR base.

### Optional stable-state worktree fingerprint

When reproducible uncommitted identity matters and Python 3.10+ is available, resolve the directory containing this skill's `SKILL.md` and run the bundled tool by absolute path. Do not look for it in the target repository:

```bash
python3 /absolute/path/to/changeset/scripts/worktree-fingerprint.py --repo /absolute/path/to/repository
```

It is read-only by design and reports:

- `worktree_sha256`: baseline `HEAD` plus Git-reported tracked changes and non-ignored untracked filesystem state;
- `index_sha256`: baseline `HEAD` plus index entries for changed paths;
- `state_sha256`: status, index, and worktree state together for the Git-reported change set;
- `complete`: whether encountered objects were supported, the observed state remained stable, and no `assume-unchanged`/`skip-worktree` index flag could hide a worktree difference.

Use a commit SHA when possible. For a high-confidence uncommitted comparison, run the helper twice without intervening actions and require the same complete `state_sha256`. A complete fingerprint identifies the observed Git change state; it is not a full filesystem snapshot, excludes ignored paths and external environment, does not transfer file contents, and does not prove reviewer independence. The helper marks the result incomplete when Git index visibility flags could conceal changes. Its JSON manifest includes path names, which may themselves be sensitive. Treat `complete=false` or differing repeated digests as a limitation/blocker according to the evidence requirement. Never export manifests, untracked files, or patches without explicit authorization; they may reveal sensitive information.

## 6. Anti-stale decision

Immediately before editing, compare current state with the contract.

### Proceed

Proceed when required anchors still resolve, relevant observed files/instructions match their baseline, and any Git drift is unrelated after inspection.

Record unrelated drift as `DRIFT_REVALIDATED`; do not ignore it silently.

### `STALE_CONTRACT`

Stop when any of these is true:

- an in-scope or relevant context file changed after baseline outside the captured/authorized change set;
- a required anchor disappeared, became ambiguous, or changed meaning;
- repository instructions or test/build commands changed materially;
- requirement, public contract, or accepted behavior changed;
- a required file falls outside allowed/triggered conditional scope;
- the approved contract is not the latest version;
- current work in an in-scope file cannot be separated safely;
- exact authorization evidence is missing for a required high-risk decision.

A changed `HEAD` alone is a revalidation trigger, not an automatic failure. Inspect endpoint drift without range ambiguity:

```bash
git --no-pager diff --no-ext-diff --no-textconv --name-only <baseline-head> HEAD
```

If drift touches relevant code, dependencies, tests, generated-source rules, or instructions, issue a new contract version unless the contract explicitly left that change to implementation discretion.

## 7. Contract amendments

Increment the version when changing:

- atomic outcome or externally visible behavior;
- allowed, conditional, forbidden, or explicitly included pre-existing scope;
- invariant or compatibility expectation;
- risk tier;
- required acceptance criterion or evidence class;
- a human-approved design/data decision.

Do not increment for a mechanical choice already delegated, a corrected line number with the same anchor, or unrelated revalidated `HEAD` drift.

When implementation reveals a new necessary change, stop and issue the smallest amendment. Do not smuggle it into the current patch.

## 8. Status rules

- `READY_FOR_APPROVAL`: complete/testable contract, but implementation is not authorized or policy requires exact approval.
- `AUTHORIZED_TO_IMPLEMENT`: exact version authorized by a direct request or explicit approval, and risk gate permits execution.
- `NEEDS_DECISION`: a product, behavior, compatibility, data, or risk decision cannot be inferred safely.
- `BLOCKED`: required access, artifact, tool, safe workspace, or authorization evidence is unavailable.

Never use `AUTHORIZED_TO_IMPLEMENT` because the agent considers its own plan good.
