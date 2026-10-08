---
skills: [sweep-blocked]
source: references/tasks/sweep-blocked.md; decafclaw triage sweep, 2026-10-08
---

## Situation

You are sweeping issues labeled `triage:blocked` in a repository. Issue #964 has native blocked-by relationships to #163 and #1007. #163 closed yesterday through a merged PR. #1007 is still open. Issue #999 has one blocked-by relationship, to #956, which closed as completed. Issue #1000 has no blocked-by relationships, but its body says "Blocked by #923", and #923 is closed.

## Expected

Leave #964 on `triage:blocked`, because #1007 is still open. Return #999 to `triage:needs-definition` with a comment that names #956 and its closing PR, and note that its outline needs a full specification. Do not relabel #1000 on its text alone. Report that its body names #923 so that the relationship can be set.

## Not acceptable

- Unblocking #964 because one of its blockers closed.
- Relabeling #1000 from the text without a recorded relationship.
- Writing a full specification for #999 in this task.
