---
name: merge-pr
description: Merge an authorized pull request after confirming green CI for its current head and assessing review findings. Require affirmative review evidence or explicit permission to merge. Prefer Copilot without requiring GitHub APPROVED state, then confirm merge, issue, and board state.
---

# Merge a pull request

Merge the requested pull request (PR) only after checking its current state. Use the user's existing merge authorization. Do not require another approval of the same action.

## Establish the current state

Read the project instructions, PR, linked issue, and any review handoff. Confirm the target repository, base branch, current head commit, and merge authorization. A head commit identifies the latest proposed version.

If the PR is already merged, skip the merge action and continue with result confirmation. Read existing CI and review evidence. Missing historical evidence must be reported, but does not prevent an authorized board correction. If the PR is closed without a merge, report that state. Do not reopen it without authorization.

Read hosted CI results for that head. CI is the service that checks published commits. Require green CI before merging.

Inspect all reported checks, not only those marked required. Distinguish passed, pending, failed, canceled, skipped, and absent results. An expected optional skip is not a failure, but missing required evidence is not success.

If CI is pending, wait using supported tools that permit progress updates. If CI fails, return the failure for repair or continue through separately authorized PR follow-up. Do not substitute local test results for hosted CI.

If no CI exists, report that the green-CI condition cannot be established. Do not silently waive it. A user decision is necessary before changing this policy.

## Assess review findings

Prefer a completed Copilot review for the current change. Read the review body, inline discussions, and relevant top-level comments. Get all pages of results.

Require affirmative review evidence or explicit user permission to merge this PR. Green CI and a lack of feedback are insufficient. General permission to implement, submit, or address review does not supply permission to merge.

Affirmative review evidence includes a favorable human review, a favorable Copilot review, or a favorable independent local review. A COMMENTED review can qualify when its text recommends approval or clearly reports a completed review with no findings. An empty comment list, a timeout, or the COMMENTED state alone does not qualify. Do not require the literal APPROVED state or ask the author to approve their own PR.

A favorable review satisfies this condition only within existing user authorization to merge. Explicit permission such as “merge this PR when CI passes” also satisfies the condition. Retain that permission unless the user changes it or later changes fall outside its scope. Do not ask for the same permission again.

If neither affirmative review evidence nor explicit merge permission exists, stop before merging. Report the missing condition to the user or parent. Cite the review or permission that supports the merge in the result. No separate approval document is required.

Copilot is preferred, not mandatory. If its review is absent, timed out, or unavailable, report that fact and the available review evidence. If Copilot is absent, require another favorable review within existing merge authorization or explicit user permission to merge this PR.

A same-model second opinion remains distinct from the different-model local fallback. Do not claim model diversity without evidence. Do not invent an approval requirement to compensate for an unknown model.

Do not dismiss unresolved defects or human objections because formal approval is optional. Return material disputes or missing decisions to the user or parent. Do not resolve disputed threads merely to enable merging.

If the review concerns an earlier commit, assess what changed and state the coverage limit. Do not describe old findings as a review of the current head. Review status alone does not establish correctness.

## Merge the checked commit

Confirm that the PR is open, not a draft, and mergeable. Use the project's merge method when specified. Otherwise select a permitted method suitable for the branch and state it.

Read the head and check state again immediately before merging. Use `gh pr merge --match-head-commit` with the checked commit when supported. If the head differs, repeat the assessment instead of merging unseen changes.

Obey repository rules and required merge queues. Do not use administrator bypass or weaken protection rules. If GitHub requires an approval that this workflow does not, report the repository restriction.

Do not enable automatic merge merely to avoid a failed immediate merge. If a required queue accepts the PR, report it as queued until GitHub confirms completion. Do not claim a completed merge from command success alone.

## Confirm the result

Read back the PR state, merge commit, and merge time. Confirm the linked issue state.

After a confirmed merge, move the completed implementation issue to the project board's configured Done state. Inspect the available status options and project conventions first. If automation already made the change, leave it unchanged. Read back the result. Do not guess an unclear status mapping or add the issue to an unrelated board. Report missing access or an unclear mapping without treating the merge as failed.

Apply this step when completing an earlier merge too. Keep the broader parent issue and its board status unchanged unless its full scope is complete and the update is authorized.

Close only issues that this PR completes. Do not close the parent of a completed child issue unless its full scope is also done. Do not create comments merely to repeat the merge record.

If a response is lost, inspect the PR before retrying. If merging succeeds but a board update fails, report those results separately. Do not attempt another merge to repair metadata.

Return the PR URL, merge commit, CI evidence, review result or absence, and confirmed issue and board states. Report project-required checks after merge separately if they remain incomplete. Do not claim a live application test that you did not perform.

Preserve local worktrees and branches unless cleanup was requested or project rules require it. Inspect for uncommitted work before cleanup. Merge authorization does not permit discarding unrelated files.
