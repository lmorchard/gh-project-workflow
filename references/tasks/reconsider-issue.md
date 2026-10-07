# Reconsider an issue

Determine what remains valid about an issue and what work remains. Keep its intended result while correcting outdated claims, and return a proposed update supported by current evidence. Reconsideration alone does not authorize edits, comments, status changes, child issues, or implementation.

Apply [Authorization](../shared/authorization.md) and [Evidence](../shared/evidence.md) throughout.

## Gather the evidence

Read the project instructions, the issue body and comments, and relevant linked issues and PRs. Include child issues and their actual results. Use supplied board information without expanding the task into a board audit.

Inspect the code and test assertions that support or contradict material claims at the current target revision. Follow dependencies and callers far enough to assess the intended behavior. Keep implementation evidence, tests you ran, historical CI results, and deployment evidence separate.

## Reassess the issue

Compare the original problem and success conditions with the current evidence. Sort what you find into completed work, remaining work, outdated claims, and decisions that still need the user. Leave claims explicitly unresolved when the evidence cannot settle them.

Compare delivered behavior with the full intended result before recommending closure. Keep confirmed decisions and historical context. Do not reduce scope to make the issue look complete. If the original result is unclear, state the decision needed before proposing a new finish condition.

Recommend keeping, revising, closing, or splitting the issue, with a specific reason. Distinguish closing completed work from closing obsolete or duplicate work, and name the replacement for a duplicate.

Recommend the issue state and board status separately when both apply, using the project's actual status names. A parent that tracks several tasks differs from a task ready for implementation. If the project's parent-status conventions are unclear, make the recommendation conditional instead of calling the current status wrong. Base readiness on remaining decisions and evidence, not on the issue's age or size.

If several useful changes remain, suggest boundaries and the next useful task. Produce a full child backlog only on request; [decompose-parent-issue](decompose-parent-issue.md) does that work. Use [define-issue](define-issue.md) for a task that needs implementation detail, and [interview-issue](interview-issue.md) when a user decision blocks progress. These are possible next steps, not required phases.

## Prepare the proposed update

For a substantial correction, return a revised title and body. For a small one, return the exact edit. Keep completed progress visible, and distinguish proposed scope from agreed scope.

Include the remaining problem, known completed work, success conditions, and material open questions, in proportion to the issue. Issue text follows the project [Writing rules](../../docs/writing.md).

Review the proposal against the evidence before you return it. Make sure it keeps the original goal, does not repeat completed work, and that status and closure recommendations agree with the remaining scope. Fix unsupported claims and unclear wording yourself.

## Discuss the recommendation

The user reviews in conversation, not by reading files. Summarize what changed, what remains, and the recommended action before asking for input. Ask about decisions that affect scope, behavior, completion, or status. After each answer, revise the proposal and explain material changes. Offer the full draft when it helps or the user asks.

When delegated, give the parent the proposed update and a short opening summary for the user. Include the first useful question with its recommendation and tradeoff, and the remaining decisions.

Before publication, summarize the concrete title, scope, and status changes. If the agreed flow includes publication, continue. Otherwise ask for publication permission for those changes. Keep product decisions separate from publication permission.

## Return the result

Return the recommendation, the proposed update, supporting evidence, the next useful action, and remaining uncertainty. If no update is needed, explain why instead of rewriting the issue for style.

If an update is authorized, read the issue again before applying it and preserve intervening changes. Read back the result.
