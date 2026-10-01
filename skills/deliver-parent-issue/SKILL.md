---
name: deliver-parent-issue
description: Coordinate a bounded parent issue across child definition, filing, and express delivery. Reconcile remaining scope after each child and verify the parent completion conditions. Use for an authorized multi-child effort, not general backlog selection.
---

# Deliver a parent issue

Work through the children needed to satisfy one selected parent issue. Reuse the existing skills and carry decisions between them. Do not require the user to restart the flow after each child.

## Establish the boundary

Read the parent, project instructions, confirmed decisions, existing children, and related PRs. Identify the intended result, exclusions, priority policy, and requested endpoint for the children. PR means pull request.

Use existing authorization for definition, filing, implementation, publication, and merge where the agreed flow includes them. State that scope at the start without requesting it again. If the endpoint is unspecified, use express-issue's default of review follow-up without merge. Do not infer deployment or cleanup permission from delivery permission.

Preserve explicit limits, including draft-only work, a selected subset, or a time or cost budget. If the user supplied no budget, do not invent one. Stop at an explicit limit with a truthful handoff.

A request to complete the parent includes maintaining its progress and closing it when its full success conditions are met. A request to process selected children does not by itself authorize closing a broader parent. Distinguish those endpoints before claiming completion.

## Reconcile the remaining work

Compare the parent goal with current target-branch code, related changes, tests, and child results. Use [reconsider-issue](../reconsider-issue/SKILL.md) when evidence challenges the parent's content or status. Use [decompose-parent-issue](../decompose-parent-issue/SKILL.md) when useful task boundaries or coverage are missing.

Reuse an existing decomposition when it still fits. Maintain a compact map from each parent requirement to completed work, an existing child, remaining work, or an explicit exclusion. Do not mistake a previously proposed list for a complete current inventory.

Keep ordinary progress and decisions in the parent and native child relationships. Small completed-work or next-task corrections do not require a full reconsideration cycle. Delegate subject updates and preserve intervening edits. No separate state store or fixed report format is required.

## Choose and prepare the next child

Choose from the agreed parent scope using real dependencies, current priority, useful results, and review size. Explain the choice briefly. Inspect current code and actual consumers before accepting an old candidate's technical claims.

Obey project rules for entering active work. Do not raise priority simply to make an issue eligible. Use priorities already approved for the selected work or return a material priority decision to the user.

Process one child at a time by default. Base each implementation on the target state after its prerequisites land. Do not start dependent work against an unmerged branch merely to keep agents busy. Parallel work requires independent scope and enough review capacity.

Use [define-issue](../define-issue/SKILL.md) for a child that lacks an implementable definition. Ask the parent conversation to settle material decisions through [interview-issue](../interview-issue/SKILL.md). The agent writes and revises the draft; file review is optional.

Split a candidate when it contains independently useful changes that are too large to review together. Keep the parent coverage intact and explain the split. Routine boundary refinement within agreed scope does not require another authorization check. A change to intended behavior, exclusions, or material cost returns to the user.

Use [file-issue](../file-issue/SKILL.md) once the draft is ready and publication is included in the authorized flow. Check for duplicates and reuse matching existing work. Do not pause at a completed draft merely because one subagent's assignment ended.

## Deliver and continue

Run [express-issue](../express-issue/SKILL.md) for the selected child with its endpoint, scope, decisions, and existing authorization. That skill owns implementation, independent review, submission, and review/CI follow-up. CI is the service that checks published commits.

For this parent-delivery flow, merge requires both affirmative independent review of the final changes and green hosted CI for the final head. Head means the latest proposed commit. Permission to merge does not substitute for favorable review. Honor repository rules, unresolved human objections, and the exact-head checks in merge-pr.

Preserve express-issue's different-model local review, review-wait limits, and correction behavior. Missing evidence remains missing. Do not repeat review cycles indefinitely or treat a pending review as approval.

After a child returns, verify its actual result through the responsible subagent. Credit only delivered behavior. Update the parent progress and remaining-work map, then continue to the next eligible child without another prompt.

If a child is blocked, record its state and dependency. Continue an independent child when useful and authorized. Do not conceal the blocker or skip work required for parent completion. Stop and return a focused question when no useful authorized progress remains.

Treat new user feedback, smoke-test results, and regressions as active evidence. Route defects caused by this effort into correction work before dependent tasks. Keep unrelated pre-existing defects explicit without silently adding them to the parent's scope.

## Keep agent roles clear

The parent owns the user conversation and workflow decisions. Subject-repository agents perform code, GitHub, board, and merge operations. Give them the necessary skill paths, revisions, decisions, authorization, and expected handoff.

Do not require a nested agent for every phase. A subject agent can define, file, and implement through the relevant skills. Independent review still needs fresh context and the required model selection.

If nested dispatch hits a capacity limit, let the coordinator finish its handoff and let the parent dispatch the next phase. Preserve completed work and recorded model identities. Do not replace independent review with self-review to work around capacity.

## Verify the parent result

After the planned children finish, reassess the original success conditions against current code and consumers. Refresh the coverage map and inspect integration across the children. A set of closed issues is not proof that the parent is complete.

Run the project checks and focused integration checks needed for remaining evidence gaps. Reuse valid results where they cover the current revision and behavior. Avoid repeating full suites merely to create another report.

Keep automated tests, hosted CI, deployment, and user-reported smoke checks distinct. Identify required live checks that remain unperformed. Do not claim parent completion while a required success condition remains unresolved.

If the authorized endpoint and all completion conditions are met, delegate parent closure and the configured board transition. Read back the result. Otherwise leave it open and report precisely what remains.

Return completed child and PR links, parent state, current coverage, decisions made, blockers, and verification limits. Stop at the agreed parent or subset boundary. Do not move on to unrelated backlog work.
