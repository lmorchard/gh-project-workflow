# Authorization and roles

These rules apply to every skill in this repository. They cover what the user has permitted and who does what.

## Roles

The **parent** agent owns the conversation with the user. It makes workflow decisions, conducts interviews, and dispatches tasks. A **subagent** does work in the **subject repository**, the project that the task changes. That work includes code changes, commits, pushes, issue and board updates, PRs, review replies, and merges. When a separate identity is configured, subagents follow [Agent identity](identity.md).

A subagent returns questions to the parent. It does not interview the user, wait for an answer, or treat a missing answer as approval. Give each question its reason, a recommended answer, and the tradeoff.

In a direct session with no parent, the agent that does the work also talks to the user.

## Handoffs

A coordinator dispatches each task to a subagent. Give the subagent its skill path, the subject, current revisions, relevant evidence, confirmed decisions, and authorization limits. Include unresolved questions only when they affect that task. Require actual results and evidence limits in return.

If a needed skill or delegation is unavailable, report the limit. Do not do the subject-repository work in the parent instead, or silently replace a skill's procedure. If nested dispatch hits a capacity limit, let the coordinator finish its handoff and let the parent dispatch the next task. Preserve completed work and recorded model identities across that change.

Keep progress updates in the conversation and durable facts in issues, commits, and PRs. A coordinator does not need a custom state file, scheduler, fixed report format, or approval document.

## Use the authorization that exists

Use the authorization already given in the conversation. Do not ask for it again because the next task uses a different skill.

An agreed flow, such as issue preparation through publication or delivery through review follow-up, authorizes each task that it includes. Carry that authorization and its limits into every handoff. When a subagent finishes one task, dispatch the next included task. Do not stop and wait for the user to ask what is next.

Changes that the user reviews or decides stay within the authorized flow. Revisit authorization only when a significant change falls outside the reviewed or authorized scope.

An interview settles decisions. It does not grant or renew permission.

## Limits

An explicit narrower limit takes precedence. Examples are draft-only work, read-only assessment, a selected subset, or a time or cost budget. Do not invent a budget that the user did not give.

Permission for one action does not imply the next:

- Agreement with an idea does not authorize publishing it.
- Definition, reconsideration, and decomposition do not authorize publication or implementation.
- Issue preparation does not authorize implementation or merge.
- Permission to implement, submit, or address review does not authorize merge.
- A favorable review does not authorize merge. See [Review](review.md).
- Delivery does not authorize deployment or cleanup, such as deleting branches or worktrees.

Never infer a decision or a permission from silence.

## Questions for the user

Ask only about decisions that evidence cannot settle: intent, scope, behavior, cost, compatibility, permissions, and disputed findings. Research facts instead of asking about them.

Ask one focused question at a time. Include a recommendation and its tradeoff when the evidence supports one. Use answers that the user already gave.

Return to the user when a material decision or blocker prevents further useful work. Continue independent work that does not depend on the answer.
