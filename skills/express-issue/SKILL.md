---
name: express-issue
description: Coordinate existing skills for one selected issue through implementation, independent review, PR submission, and review follow-up, with optional explicitly authorized merge. Resume from current state and return material decisions to the user. Do not select work from a backlog.
---

# Take one issue through delivery

Coordinate the existing skills rather than repeating their procedures. The parent owns the conversation and dispatches subject-repository work to subagents. Each task remains usable without this coordinator.

## Establish the task and endpoint

Read the selected issue, repository instructions, existing work, and user decisions. Identify the repository, issue, and requested endpoint. An endpoint states where this invocation stops.

Use the endpoint already agreed in the conversation. For an express request with no endpoint, state the default: through PR review follow-up, without merge. An explicit narrower request takes precedence. A request through merge authorizes that step subject to the merge policy.

Carry the initial authorization through included tasks and routine corrections. Do not ask permission again merely because the next skill changes. User-reviewed scope changes carry forward within the authorized flow. Revisit authorization only for a significant change outside the reviewed or authorized scope.

Keep interviews for product decisions, disputed findings, and other questions that evidence cannot settle. Ask one focused question with a recommendation and tradeoff. Maintain the draft yourself instead of requiring file review. Do not infer an answer from silence.

Locate the skills linked here before dispatch. Read each skill when its task becomes relevant. If a needed skill or delegation capability is unavailable, report the limit. Do not silently replace its procedure or perform subject mutations in the parent.

## Resume from evidence

Inspect existing branches, worktrees, PRs, review records, and check results for the selected issue. Reuse completed work when it still applies to the current revision. Do not create another branch or PR simply because this invocation is new.

Resolve uncertain partial writes through readback before retrying. A board status is not proof that a task is complete. Distinguish implementation, tests, independent review, publication, and merge evidence.

If the issue is stale or contradicts current code, use [reconsider-issue](../reconsider-issue/SKILL.md). If its implementation scope is unclear, use [define-issue](../define-issue/SKILL.md). Use [interview-issue](../interview-issue/SKILL.md) in the parent when a material decision remains. Do not require these tasks for an already clear issue.

Changes to the selected issue can stay within the agreed flow. Creating a new child or choosing a replacement task requires a scope decision. Do not expand this invocation into backlog selection or automatic decomposition.

## Implement and review locally

Dispatch [implement-issue](../implement-issue/SKILL.md) when implementation remains. Supply the issue, confirmed scope, existing work, and authorization. Let that skill manage the worktree, tests, commits, and In progress transition.

Plan reviewer selection before implementation when possible. Record model identities from reliable runtime or dispatch information. Do not infer them from an agent name or writing style.

Dispatch [review-changes](../review-changes/SKILL.md) in fresh context for the exact implementation base and head before submission. Give the reviewer the issue and necessary facts, not the author's conversation or desired conclusion. The reviewer reports findings without changing code.

Use a different recorded model from the implementer for this express path's local review. If identities or model selection are unavailable, report the limitation and return the review choice to the user. Continue independent preparation where useful, but do not silently skip review or claim model diversity. A user-approved alternative remains explicit in later handoffs.

Return actionable local findings to the implementation agent for assessment and correction. Keep the same task branch and execute affected checks. Return disputed findings or scope changes to the parent interview.

After corrections, have the reviewer assess the changed code and unresolved findings. Do not repeat completed checks without a new reason. If the same blocker persists without useful progress, report it instead of cycling indefinitely.

On resumption with an existing PR, use current independent review evidence when it satisfies the agreed review plan. Do not demand a retroactive pre-submission stage merely to replay the sequence. Report any unmet review requirement and resolve it explicitly.

## Submit and address feedback

Dispatch [submit-pr](../submit-pr/SKILL.md) for reviewed local commits that are not yet published. Pass the verified worktree, branch, base, head, checks, review outcome, and existing authorization. That skill publishes the PR, requests Copilot, and manages the In review transition.

Pass its PR URL, published head, review request time, and prior review identifiers to [address-pr-review](../address-pr-review/SKILL.md). Preserve its original review deadline on resumption. Do not reset the wait or duplicate review requests at a handoff.

That skill owns review assessment, in-scope corrections, tests, pushes, and CI repair. CI is the service that checks published commits. Human COMMENTED reviews remain actionable. Green CI and silence do not establish a favorable review.

Respect the follow-up skill's review-cycle limit. A new review after corrections can remain pending at the end of this invocation. Do not turn express mode into unlimited review requests. Report missing or timed-out review separately from passed CI and completed repairs.

## Finish at the agreed endpoint

For a review endpoint, report current-head CI, review coverage, resolved findings, and outstanding work. Distinguish a completed review from an invocation that ended with pending or unavailable evidence. Do not merge.

For an explicitly authorized merge endpoint, dispatch [merge-pr](../merge-pr/SKILL.md) after follow-up. It must assess current checks, review evidence, unresolved objections, and repository rules. Authorization for the full flow does not waive those requirements. Do not ask for the same merge permission again.

Read back the final subject state through the responsible subagent. Report the issue and PR URLs, current or merged commit, test and review evidence, and remaining limits. Include required post-merge checks that remain unperformed.

Stop at the selected endpoint or a concrete blocker that prevents further useful work. Preserve the worktree and enough information to resume. Do not deploy, remove branches, or select the next issue unless those actions are included in the request.

## Keep handoffs small

Give each subagent its skill, subject, current revisions, relevant evidence, confirmed decisions, and authorization limits. Include unresolved questions only when they affect that task. Require actual results and evidence limits in return.

Keep status updates in the conversation and durable facts in existing issues, commits, and PRs. Do not require a custom state file, fixed report format, scheduler, frozen checks, or another approval document.
