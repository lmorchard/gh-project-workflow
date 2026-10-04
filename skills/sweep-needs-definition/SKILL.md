---
name: sweep-needs-definition
description: Process issues labeled triage:needs-definition into concrete technical specifications with boundaries and test criteria, transitioning them to triage:ready.
---

# Sweep issues needing definition

Develop open issues labeled `triage:needs-definition` into concrete, bounded specifications grounded in current target code. Define file boundaries, observable success conditions, and required tests, advancing each issue to `triage:ready`.

Apply [Authorization](../shared/authorization.md) and [Evidence](../shared/evidence.md) throughout. The parent agent coordinates the sweep; subagents execute research and issue updates in the subject repository following [Agent identity](../shared/identity.md).

## List pending issues

Query open issues in the subject repository with the label `triage:needs-definition`:

```bash
gh issue list --repo OWNER/REPO --label "triage:needs-definition" --limit 50
```

Optionally filter by a specific parent issue or component area. If no issues carry the label, report that all accepted issues are fully defined and stop.

## Define each issue

Process issues one at a time or in bounded slices of 2 to 5 issues. For each issue, dispatch a subagent to apply [define-issue](../define-issue/SKILL.md):

1. Read the issue body and comments to understand the original intent and confirmed decisions.
2. Inspect current code and test seams at the target revision (such as `main`).
3. Formulate concrete technical boundaries:
   - Specific source files and classes to touch.
   - Observable success conditions and test cases to add or run.
   - Explicit exclusions (what remains out of scope or follow-up).
4. If the scope is too broad for a single implementation task, scope a bounded first slice and recommend child issues or follow-up tasks.
5. If technical investigation reveals a blocking product or design uncertainty that needs user judgment, stop specification, label the issue `triage:needs-input`, post the specific question, and return it to the parent.

## Update the issue record

Once the specification is solid:

1. Update the issue body in the subject repository to include the refined problem, boundaries, success conditions, and test criteria:
   ```bash
   gh issue edit ISSUE_NUMBER --repo OWNER/REPO --body-file /tmp/defined-body.md
   ```
2. Transition labels:
   - Remove `triage:needs-definition`.
   - Add `triage:ready`.
3. Post a brief comment linking to the revised body and noting that the issue is now actionable for implementation.

## Conclude the sweep

Return a summary table to the parent:

- Issue number and title.
- Defined technical boundary (primary files and tests).
- Updated label (`triage:ready`, or reassigned to `triage:needs-input` if blocked).
- Suggested next step (direct implementation or queue for board scheduling).
