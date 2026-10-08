# Authorization and roles

These rules apply to every skill in this repository. They cover what the user has permitted and who does what.

## Roles

The **parent** agent owns the conversation with the user. It makes workflow decisions, conducts interviews, and dispatches tasks. A **subagent** does work in the **subject repository**, the project that the task changes. That work includes code changes, commits, pushes, issue and board updates, PRs, review replies, and merges. When a separate identity is configured, subagents follow [Agent identity](identity.md).

A subagent returns questions to the parent. It does not interview the user, wait for an answer, or treat a missing answer as approval. Give each question its reason, a recommended answer, and the tradeoff.

In a direct session with no parent, the agent that does the work also talks to the user.

## Handoffs

A coordinator dispatches each task to a subagent, except for PR follow-up owned by the parent as described next. Give the subagent its resolved entry skill, task-reference, and CLI paths, the source checkout revision used for instructions and tools, the target checkout, the subject, current revisions, relevant evidence, confirmed decisions, and authorization limits. Include unresolved questions only when they affect that task. Require actual results and evidence limits in return.

If a needed skill or delegation is unavailable, report the limit. Do not do the subject-repository work in the parent instead, or silently replace a skill's procedure. If nested dispatch hits a capacity limit, let the coordinator finish its handoff and let the parent dispatch the next task. Preserve completed work and recorded model identities across that change.

Keep progress updates in the conversation and durable facts in issues, commits, and PRs. A coordinator does not need a custom state file, scheduler, fixed report format, or approval document.

## PR follow-up ownership

After PR submission, a delegated delivery coordinator stops and returns the submission handoff to the parent. An intervening coordinator relays that handoff to the parent that owns the user conversation. Include the issue and PR URLs, worktree, branch, base and published head, exact source revisions, check results and their commits, review coverage and model evidence, original review request times and deadlines, review identifiers, chosen endpoint, and authorization limits. Mark follow-up as incomplete when the endpoint includes it.

For an authorized review-follow-up endpoint, the parent directly dispatches [address-pr-review](../tasks/address-pr-review.md) and receives its final report for each PR. Submission alone does not complete that endpoint. Continue the included work without renewed permission. In a direct session with no parent, the agent handling the conversation owns this dispatch.

If another worker updates the PR branch during follow-up, the parent notifies the responsible follow-up worker with the PR, new head, and available change evidence. The worker independently reads the actual current head and reassesses its evidence under [Evidence](evidence.md). The parent does not replace the worker's CI repair or final verification with its own subject-repository actions.

After follow-up, the parent dispatches any remaining authorized task, including [merge-pr](../tasks/merge-pr.md) only for an authorized merge endpoint. Return the verified endpoint result to a queue or parent-issue coordinator before it credits completion or selects dependent work. Keep merge checks and separate merge permission intact.

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

Before asking, identify what is missing: a fact, an implementation choice, or a decision about the intended result.

Research discoverable facts in current code, tests, documentation, or other relevant sources. Follow [Evidence](evidence.md#sources-and-revisions) when reusing earlier findings. An unread source is an evidence gap, not a user decision.

Resolve routine, reversible implementation choices from project conventions, current evidence, and confirmed decisions. Act within the existing authorization. Explain the choice when it affects the result or handoff. Reversibility alone does not settle a product decision.

Return an unresolved decision when viable answers change intent, scope, user-visible behavior, compatibility, cost, or permissions. Return disputed findings when current evidence cannot settle a material disagreement. Research can establish the alternatives and their effects. It cannot choose between conflicting user requirements. Do not silently add a requirement or widen authorization.

Ask one focused question at a time. State the evidence, a recommended answer, and its tradeoff when the evidence supports one. Identify uncertainty that affects the recommendation. Use answers that the user already gave.

A subagent returns that question to the parent. Continue independent work that does not depend on the answer. Keep dependent work pending until the decision arrives. If a blocker leaves no useful independent work, report it to the parent or user. Apply the existing authorization and silence limits above.
