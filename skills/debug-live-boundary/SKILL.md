---
name: debug-live-boundary
description: Debug mismatches between live behavior and local tests by tracing the real winning boundary instead of patching blindly. Use when code appears correct locally but fails in production, staging, preview, browser, deployed API, webhook, cache, proxy, build artifact, config path, or integration path; especially when repeated code changes do not move the live symptom.
---

# Debug Live Boundary

## Overview

Use this skill to stop speculative patching when live behavior contradicts local confidence. Add one narrow temporary diagnostic at the earliest suspected live boundary, prove which source or path actually wins in the real workflow, patch only that boundary, verify the live result, then remove the diagnostic.

## Use This Workflow

1. State the contradiction precisely.
   Example: "Unit and local E2E say submit uses endpoint A, but production still sends endpoint B."

2. List the earliest plausible live boundaries.
   Common boundaries:
   - deployed bundle or stale artifact
   - environment variable resolution
   - server route or proxy rewrite
   - cache layer or CDN
   - feature flag or config branch
   - webhook target or third-party callback
   - client/server divergence in the same workflow

3. Choose one boundary only.
   Pick the earliest point that can distinguish between competing explanations. Do not instrument multiple layers at once unless one diagnostic cannot separate them.

4. Add one narrow temporary diagnostic at that boundary.
   Make it cheap, explicit, and easy to remove.
   Good diagnostics:
   - a unique log line with a stable marker
   - a response header showing the selected branch
   - a temporary UI label or payload field exposing the chosen source
   - a one-off server log around env/config resolution

5. Run the real workflow where the bug appears.
   Prefer the actual live or preview path over local reenactment. Prove which code path, config source, artifact, or upstream response wins.

6. Patch only the winning boundary.
   Do not refactor adjacent code until the contradiction is resolved. If the evidence shows the earlier suspicion was wrong, move to the next earliest boundary and repeat.

7. Verify on the real path again.
   Confirm the live symptom changed for the reason you expected, not because of an unrelated side effect.

8. Remove the diagnostic.
   Treat temporary instrumentation as part of the fix cycle, not a follow-up task.

## Diagnostic Rules

- Keep the diagnostic narrower than the patch.
- Prefer proving "which source won" over collecting broad debug output.
- Use uniquely searchable markers so live logs are unambiguous.
- Avoid diagnostics that change control flow, timing, or persistence semantics unless the bug itself is timing-sensitive.
- If the system is high risk, use the safest observable surface available first: header, marker, no-op branch label, or read-only log.

## Stop Doing

- Do not keep editing downstream logic before proving the upstream winner.
- Do not stack multiple speculative fixes into one deploy.
- Do not trust local tests as proof of the deployed path.
- Do not leave temporary diagnostics behind after verification.

## Escalation Rule

If one boundary is disproven, move earlier or more external, not deeper into random code. The goal is to identify the first live decision point that makes the wrong result inevitable.

## Example Triggers

- "The tests pass, but production still renders the old CTA."
- "Locally the API uses the new prompt, but deployed responses still look old."
- "The route works in dev, but the live webhook keeps hitting the legacy handler."
- "We changed the parser, but the real uploaded CV still follows the old normalization path."
