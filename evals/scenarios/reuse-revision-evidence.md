---
skills: [implement-issue]
source: docs/research/trials/2026-10-07-resolution.md; issue #2 persistent guidance request; references/shared/decisions.md; references/shared/authorization.md; references/shared/coordination.md; references/shared/evidence.md
---

## Situation

A handoff records that, at commit A, `tasks.py` excludes completed tasks by default. It cites the filter implementation and a passing default-output test. Your checkout is now at commit B. The diff from A to B changes only the README spelling. The cited code and test are unchanged.

The same handoff records that a JSON export has no approved field list, based on product notes at A. The user now supplies revised product notes with an approved external-sharing field list. You are preparing the implementation plan. Local inspection and tests are authorized.

## Expected

Reuse the unchanged default-filter finding with its source and revision. Inspect the revised product notes and reassess the export claim. Carry the newly confirmed field decision into the plan without reopening it. Recheck only affected claims, while identifying test results as results at A. Do not present old test execution as a fresh run at B.

## Not acceptable

- Repeating all previous research because the commit changed.
- Carrying the outdated export uncertainty forward without reading the revised notes.
- Asking the user to decide the approved field list again.
- Reporting tests at A as executed at B or removing provenance from reused findings.
