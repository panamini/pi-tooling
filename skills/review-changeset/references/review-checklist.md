# Focused review checklist

Use this reference to generate hypotheses. A checklist item is never a finding by
itself. Admit a finding only after the `SKILL.md` evidence gate is satisfied.

## Correctness and boundaries

- off-by-one, truncation, rounding, units, timezone, locale, encoding, ordering
- null/undefined/empty/missing values and defaults
- partial success incorrectly treated as complete success
- error swallowed, retried forever, double-reported, or converted to a valid result
- fallback path no longer reachable or unexpectedly becomes the default
- changed condition reverses behavior or skips a required branch
- resources leaked on early return, exception, cancellation, or timeout
- cache key, memoization key, or invalidation no longer matches semantics
- renamed or removed field still consumed elsewhere
- old persisted or queued data no longer parses after deployment

## Interfaces and compatibility

- public export or package entry point changed unintentionally
- request/response, event, RPC, MCP, CLI, or file format changes without compatibility
- optional becomes required, nullable becomes assumed non-null, enum/value set narrows
- validation and runtime parsing disagree with static types
- status codes, error codes, headers, or serialization semantics change
- client and server versions cannot overlap during rollout
- migration cannot handle existing rows, partial rollout, retry, or rollback
- feature flag default differs across local, test, staging, and production
- environment variable is read on the wrong side of a client/server boundary

## Security, privacy, and tenancy

- authorization is checked in UI/middleware but not at the sensitive server operation
- object lookup is not scoped to the authenticated owner/tenant
- newly reachable path bypasses authentication, CSRF, rate limit, or permission check
- secret, token, PII, private prompt/context, or internal error is logged or returned
- untrusted input reaches command, SQL, template, path, URL, HTML, regex, or deserializer
- redirect, callback, webhook, hostname, or file path is insufficiently constrained
- mass assignment or broad update accepts fields the caller must not control
- cache or singleton state mixes users, tenants, requests, or environments
- cryptographic verification, signature, expiry, audience, or issuer check is weakened

## Data integrity and persistence

- write is not idempotent under retry or at-least-once delivery
- read-modify-write loses concurrent updates
- uniqueness is checked outside the transactional boundary
- transaction no longer includes all dependent writes
- deletion or migration can orphan or silently drop data
- changed default overwrites an existing user choice
- schema/index/query change creates unbounded scans or misses records
- cursor/pagination logic skips or duplicates records
- stale cache survives mutation or rollback
- persistence succeeds but downstream side effect fails without recovery

## Async, state, and lifecycle

- stale closure or dependency list reads old state
- response from an older request overwrites a newer request
- cancellation/abort is missing or ignored
- retry duplicates work, charges, emails, jobs, or writes
- loading, error, and success states can become impossible or contradictory
- effect/listener/subscription is registered more than once or not cleaned up
- lock/lease/heartbeat ownership can expire or be stolen incorrectly
- process shutdown loses buffered data or acknowledges work too early
- background task outlives credentials, request scope, or transaction
- initialization order differs between cold start, hot reload, and test

## Performance with correctness impact

Report only when the performance issue creates a credible availability, cost, timeout,
or user-visible correctness risk.

- unbounded query, traversal, loop, recursion, or in-memory accumulation
- N+1 network/database calls introduced on a common path
- missing index or filter causes production-scale scan
- expensive work moved into request, render, lock, or transaction critical path
- retry/backoff creates thundering herd or indefinite work
- event/listener leak grows with navigation or requests
- large payload or full dataset crosses client/server boundary unnecessarily

## Tests and false confidence

- changed behavior has no test at the boundary where it can fail
- test asserts mock implementation rather than observable contract
- fixture cannot represent old persisted data or partial migration
- test passes because errors are swallowed or timers/promises are not awaited
- snapshot/update masks a semantic regression
- mocked authorization, clock, randomness, network, or storage avoids the risky path
- test command excludes the changed package/path
- new test proves happy path only while the defect is in retry/failure/concurrency
- generated types pass but runtime schema/parser differs

## Configuration, dependencies, and supply chain

- dependency or action version changed without matching API/runtime update
- lockfile delta contains an unexpected package, source, integrity, or major change
- build target, runtime, module format, or package export no longer matches consumers
- permission scope, token exposure, fork behavior, or untrusted-input execution changed
- secret is available to code or workflow steps that do not need it
- production configuration diverges from test/local assumptions
- generated file changed without its source, or source changed without regenerated output

## User-interface and browser behavior

Use rendered evidence when the claim depends on the browser.

- event propagation, focus, keyboard, form submit, or navigation behavior changes
- server/client hydration or serialization mismatch
- stale state after route transition, optimistic update, or failed mutation
- accessibility regression blocks a real interaction, not merely a preference
- storage, cookie, origin, iframe, CSP, or browser API boundary is incorrect
- responsive/layout change hides or prevents a required action
- cleanup missing for observer, listener, timer, object URL, stream, or media resource
