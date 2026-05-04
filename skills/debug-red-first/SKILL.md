---
name: debug-red-first
description: Debug inconsistent UI and state bugs by forcing one exact user symptom, one invariant, one failing reproduction test, one minimal fix, and green guard-rail tests. Use when clicks behave inconsistently, UI flickers, lists reorder under the cursor, state appears to jump, the bug spans multiple surfaces, or tests are green while the real user symptom still happens.
disable-model-invocation: true
---

# Debug RED First

Reduce an unstable UI or state bug to one exact user-facing invariant, reproduce it with one failing test, and only then fix the shared path or smallest responsible code path.

## Core Rule

Do not fix anything without a RED test for the exact user symptom.

Do not accept:
- probable root cause
- low-level sub-case coverage
- green tests without symptom reproduction

Require:
1. Define the exact user symptom.
2. State one invariant in user terms.
3. Write one failing test that reproduces it on current code.
4. Apply one minimal fix.
5. Re-run adjacent guard rails and one short smoke check.

## Workflow

### 1. Reduce To One Invariant

Prefer user-visible invariants such as:
- one click on a CV card must always open that CV
- opening a CV must never reorder the visible list without a real business edit

Reject vague statements such as:
- the library is glitchy
- state seems broken

### 2. Keep One Pass Per Symptom

Do not mix different symptoms in the same pass:
- multi-click bug
- reorder bug
- disappearance bug
- reload bug
- sidebar bug
- library bug

Split them and handle one symptom at a time.

### 3. Go RED Before Product Changes

Before editing product code:
- reproduce the real user path
- include the real preconditions
- make the test fail on current code

If no RED exists, stop. Audit the path again instead of fixing blindly.

### 4. Fix The Shared Path First

Use this priority order:
1. shared source of truth
2. shared load or switch path
3. local component
4. styling or render-only behavior

If the same symptom appears in multiple surfaces, assume shared-path until current call sites prove otherwise.

### 5. Re-Run Guard Rails

Always verify:
- the new RED test is now green
- nearby bug-fix tests stay green
- one short manual smoke test still matches the user path

## Heuristics

### Non-Deterministic Bugs

Suspect first:
- async state races
- autosave on switch
- sorting on `updatedAt`
- hydration or local-remote merge
- navigation too early
- multiple render branches
- stale derived state

### UI Moves Under The Cursor

Suspect first:
- list reorder
- timestamp bump
- filter or sort reapplication
- unstable list source
- local state mutation before navigation

### Bug Appears In Library And Sidebar

Suspect first:
- shared context
- shared load or switch function
- shared state mutation

Do not assume the page component is the cause until the shared path is ruled out.

## Anti-Patterns

Never:
- fix before reproducing
- mix multiple symptoms in one pass
- test a technical sub-case instead of the real interaction
- improve architecture during a bug pass
- add adjacent cleanup
- claim success while the user symptom still exists

## Standard Outputs

### Phase A - Audit

Return:
- broken invariant
- exact responsible path
- shared versus local boundary
- smallest recommended RED test

### Phase B - RED

Return:
- retained reproduction path
- failing test
- exact failure
- probable cause suggested by the failing result

### Phase C - Minimal Fix

Return:
- corrected cause
- files changed
- tests run
- guard-rail proof

## Standard Audit Prompt

```text
Mission unique:
identifier la cause exacte du symptome suivant, sans le corriger:
<SYMPTOM>

Scope autorise:
- <FILES ONLY>

Interdit:
- pas de fix
- pas de refactor
- pas de cleanup
- pas de redesign

A prouver:
1. quel invariant utilisateur est casse
2. quel path exact le casse
3. si la cause est locale ou partagee
4. quel plus petit test peut reproduire ce symptome

Output final:
A. invariant casse
B. path responsable exact
C. fichiers inspectes
D. test rouge recommande
E. next fix pass minimal
```
