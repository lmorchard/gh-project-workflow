---
name: express-issue
description: Coordinate existing skills for one selected issue through implementation, independent review, PR submission, and review follow-up, with optional explicitly authorized merge. Resume from current state and return material decisions to the user. Do not select work from a backlog.
---

# Take one issue through delivery

Coordinate the existing skills for one selected issue, up to an agreed endpoint. Dispatch each task to a subagent rather than repeating its procedure here. Each task skill remains usable without this coordinator.

Apply [Authorization](../shared/authorization.md), [Evidence](../shared/evidence.md), and [Review](../shared/review.md) throughout, including the handoff rules.

## Establish the task and endpoint

Read the selected issue, repository instructions, existing work, and user decisions. Identify the repository, the issue, and the **endpoint**: where this invocation stops.

Use the endpoint agreed in the conversation. If none was given, state the default: through PR review follow-up, without merge. A narrower request takes precedence. A request through merge authorizes that step, subject to the merge rules in [merge-pr](../merge-pr/SKILL.md).

Locate the linked skills before dispatch, and read each one when its task becomes relevant.

## Resume from evidence

Inspect existing branches, worktrees, PRs, review records, and check results for the issue. Reuse completed work when it still applies to the current revision. Do not create another branch or PR because this invocation is new. Keep evidence of implementation, tests, independent review, publication, and merge distinct.

If the issue is stale or contradicts current code, use [reconsider-issue](../reconsider-issue/SKILL.md). If its scope is unclear, use [define-issue](../define-issue/SKILL.md). Settle material decisions in the parent with [interview-issue](../interview-issue/SKILL.md). A clear issue needs none of these.

Changes to the selected issue can stay within the agreed flow. Creating a new child or choosing a replacement task is a scope decision for the user. This skill does not select work from a backlog or decompose issues.

## Implement and review locally

Dispatch [implement-issue](../implement-issue/SKILL.md) when implementation remains, with the issue, confirmed scope, existing work, and authorization.

Plan reviewer selection before implementation when possible. Before submission, dispatch [review-changes](../review-changes/SKILL.md) in a fresh context for the exact base and head. Give the reviewer the issue and necessary facts, not the author's conversation or desired conclusion. The reviewer must use a different model from the implementer, as [Review](../shared/review.md) describes. If that is not possible, return the review choice to the user and continue independent preparation meanwhile. Do not skip the review silently.

Return actionable local findings to the implementation agent, on the same task branch, with affected checks run again. Return disputed findings and scope changes to the parent interview. After corrections, have the reviewer assess the changed code and the unresolved findings. Do not repeat completed checks without a new reason. If the same blocker persists without progress, report it instead of cycling.

When resuming with an existing PR, use current independent review evidence if it satisfies the review plan. Do not demand a retroactive pre-submission review just to replay the sequence. Report any unmet review requirement and resolve it explicitly.

## Submit and address feedback

Dispatch [submit-pr](../submit-pr/SKILL.md) for reviewed local commits that are not yet published. Pass the verified worktree, branch, base, head, checks, review outcome, and authorization.

Pass its PR URL, published head, review request time, and prior review identifiers to [address-pr-review](../address-pr-review/SKILL.md). Preserve the original review deadline on resumption, and do not duplicate review requests at a handoff.

Respect that skill's one-cycle review limit. A review requested after corrections can still be pending when this invocation ends. Report a missing or timed-out review separately from passed CI and completed repairs.

## Finish at the endpoint

For a review endpoint, report current-head CI, review coverage, resolved findings, and outstanding work. Distinguish a completed review from pending or unavailable evidence. Do not merge.

For an authorized merge endpoint, dispatch [merge-pr](../merge-pr/SKILL.md) after follow-up, without asking for the same permission again. Authorization for the full flow does not waive its checks.

Read back the final state through the responsible subagent. Report the issue and PR URLs, the current or merged commit, test and review evidence, and remaining limits, including required post-merge checks not yet done.

Stop at the endpoint or at a concrete blocker. Preserve the worktree and enough information to resume. Do not deploy, remove branches, or select the next issue unless the request includes it.
