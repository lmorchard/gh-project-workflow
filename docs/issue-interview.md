# Issue review and user interviews

The issue-definition agent corrects problems that it can resolve from evidence. The parent agent conducts the conversation when a decision needs user judgment. This separates draft review from an interactive interview.

## Responsibilities

The [define-issue skill](../references/tasks/define-issue.md) researches, drafts, and reviews an issue. A delegated agent returns the draft, confirmed decisions, and unresolved questions. Each question includes its reason, recommendation, and tradeoff.

The [interview-issue skill](../references/tasks/interview-issue.md) helps the parent discuss those questions with the user. It can also start from a rough idea. It updates the draft as the user supplies answers.

The parent can then return the draft and decisions for another issue review. After authorization, `file-issue` publishes the reviewed draft. No skill requires a scheduler or another skill to be installed.

## When to ask

The shared [Decisions](../references/shared/decisions.md) reference supplies the boundary. [Coordination](../references/shared/coordination.md#roles) assigns the conversation and delegated work. [Authorization](../references/shared/authorization.md) supplies permission limits.

A missing fact calls for research when a source can answer it. A choice about intent or scope calls for a conversation. A routine implementation choice can remain open when the issue states sufficient success conditions.

Editing unclear prose does not require a user interview. The reviewing agent makes that correction itself. The parent asks only when a correction changes a decision that belongs to the user.

## Status

The first define-issue trial demonstrated a question returned to the parent and a revision after a confirmed scope decision. Later trials used conversation as the default review path. The [Trial records](trials/README.md) list them.
