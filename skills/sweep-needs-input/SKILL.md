---
name: sweep-needs-input
description: Interactively step through issues labeled triage:needs-input to resolve blocking decisions with the user, update the issues with confirmed choices, and assign their next triage state.
---

# Sweep issues needing input

Conduct an interactive review of issues marked `triage:needs-input`. Settle the blocking product and design questions with the user, update the issue records, and advance each issue to its next state.

Apply [Authorization](../shared/authorization.md) and [Evidence](../shared/evidence.md) throughout. The parent agent conducts the conversation; subagents execute updates in the subject repository following [Agent identity](../shared/identity.md).

## List pending issues

Query open issues in the subject repository with the label `triage:needs-input`:

```bash
gh issue list --repo OWNER/REPO --label "triage:needs-input" --limit 50
```

If no issues carry the label, report that the input backlog is clear and stop.

## Present each issue

Process issues one at a time:

1. Read the issue title, body, and recent comments, focusing on the triage findings comment.
2. Present a short summary in conversation:
   - Issue number, title, and URL.
   - Core problem and current code status.
   - The specific 1 to 2 questions needing the user's decision, with clear choices or trade-offs.
3. If more background is needed, follow [interview-issue](../interview-issue/SKILL.md) to explore the tradeoffs.

Do not ask the user to read raw code or diffs unless they ask.

## Record the decision

Once the user provides a direction:

1. Dispatch a subagent to update the issue in the subject repository:
   - Post a comment recording the user's confirmed decision and rationale.
   - Remove the `triage:needs-input` label.
2. Apply the resulting state:
   - **User decided not to proceed**: Close the issue with reason `not planned` (and add `wontfix` if used).
   - **Decision makes the task actionable as-is**: Add `triage:ready`.
   - **Decision settles direction, but technical details or criteria remain open**: Add `triage:needs-definition`.
3. Report the updated status to the user and proceed to the next issue.

## Conclude or pause

Stop when all `triage:needs-input` issues have been resolved, or when the user requests a pause. Return a summary of issues updated, closed, or queued for technical definition.
