---
name: reconsider-issue
description: Reassess an existing issue against current code, tests, related work, and project status. Propose corrections and a status recommendation before further planning. Do not change GitHub by default.
---

# Reconsider an issue

Determine what remains valid about an issue and what work remains. Preserve its intended result while correcting outdated claims. Return proposed changes supported by current evidence.

## Establish the evidence

Read the project instructions, issue body, comments, and relevant linked issues and pull requests. Include child issues and their actual results. Inspect supplied project-board information without expanding the task into a board audit.

Identify the current target branch revision and the local checkout revision. If they differ, inspect the relevant target revision before drawing conclusions. Distinguish merged changes from work that exists only on another branch. Do not reset the user's checkout to obtain current evidence.

Inspect code and test assertions that support or contradict material claims. Follow relevant dependencies and callers far enough to assess the intended behavior. Separate implementation evidence, executed tests, historical CI results, and deployment evidence. CI is the service that checks published commits.

Record source revisions and links with the findings. State which checks you executed and which you only read. If access or evidence is missing, report the limit. Do not interpret an unavailable source as proof that work is absent or complete.

## Reassess the issue

Compare the original problem and success conditions with current evidence. Distinguish completed work, remaining work, outdated claims, and decisions that still need the user. Keep unresolved claims explicit when the evidence cannot settle them.

A merged pull request or closed child issue does not prove that the parent goal is complete. A board status does not prove readiness. Compare the delivered behavior with the full intended result before recommending closure.

Preserve confirmed decisions and historical context. Do not reduce scope merely to make the issue appear complete. If the original result is unclear, state the decision needed before proposing a new finish condition.

Recommend keeping, revising, closing, or splitting the issue, with a specific reason. Distinguish closure because work is complete from closure because work is obsolete or duplicated. Name the replacement when recommending closure as a duplicate.

Recommend issue state and board status separately when both are relevant. Use the project's actual status names. Explain readiness from remaining decisions and evidence, not from issue age or size alone.

If several useful changes remain, suggest boundaries and the next useful task. Do not produce an entire child-issue backlog unless requested. Use issue definition for a task that needs implementation detail. Use an interview when a user decision prevents further progress. These are possible next steps, not mandatory phases.

## Prepare and review the proposed update

Return a revised title and body when the issue needs substantial correction. For a small correction, return the exact proposed edit. Keep completed progress visible and distinguish proposed scope from agreed scope.

Include the remaining problem, known completed work, success conditions, and material open questions. Keep the update proportional to the issue. Use short sentences and familiar words. Do not require a separate report file.

Review the proposal against the evidence before returning it. Make sure that it preserves the original goal and does not repeat completed work. Make sure that status and closure recommendations agree with the remaining scope. Correct unsupported claims and unclear wording yourself.

## Return the result

Return the recommendation, proposed issue update, supporting evidence, and next useful action. State remaining uncertainty and execution limits. If no update is needed, explain why instead of rewriting the issue for style alone.

When delegated, return decision questions to the parent with a recommendation and tradeoff. Do not attempt to interview the user from a subagent. Do not infer permission or a product decision from silence.

Reconsideration alone does not authorize edits, comments, status changes, child issues, or implementation. Keep GitHub unchanged unless those actions are separately authorized. If an update is authorized, read the issue again before applying it and preserve intervening changes. Read back the result and report partial failures accurately.
