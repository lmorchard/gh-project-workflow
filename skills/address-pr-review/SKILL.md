---
name: address-pr-review
description: Read and address feedback on an existing pull request, waiting up to 20 minutes for a pending requested review. Address findings and failing CI, test and push corrections, and watch until CI passes or a concrete blocker remains. Do not merge.
---

# Address pull request review

Use an existing pull request (PR) and its review feedback. This skill can follow `submit-pr` or start from a PR created elsewhere. It consumes findings rather than providing independent review. It also watches CI, the service that checks published commits, and corrects failures.

## Establish the task

Read the issue, PR, project instructions, current branch, and supplied review report. Confirm the current head commit, which is the latest commit proposed for merge. Use existing authorization and obey narrower limits such as read-only assessment.

For a local review report, identify the reviewed commit and evidence limits. Do not wait for Copilot when local findings are the supplied input. A review of an earlier commit requires comparison with current code before corrections.

If no review exists or is requested, report that state. Do not wait for a review that nobody requested. The parent can request Copilot or use `review-changes` for a local review.

If Copilot is unavailable, report the reason and return the fallback choice to the parent. Do not call a pending request unavailable. The local fallback uses a fresh reviewer context and a different recorded model under `review-changes`.

## Watch and repair CI

Monitor CI while waiting for review and after each push. Read checks for the current PR head, not an earlier successful commit. Use the installed watch command when available:

```sh
gh pr checks PR_URL --watch --interval 30 --fail-fast
```

Use a tool session that yields control so you can report progress and handle review feedback. After the watch ends, read all check results and the current head again. Watch completion alone does not prove success.

If a check fails, read its job log before making changes. Distinguish a code defect from setup, permissions, service outages, and cancellation. Correct failures within the issue and required build setup without weakening checks.

Execute affected local checks, commit corrections, and push to the same PR. Then watch checks for the new head. Continue until CI passes or a concrete blocker prevents further useful work.

Do not repeat an unchanged failure without new evidence or a specific reason that a retry can help. Report unavailable credentials, persistent service failures, and decisions that require the user. Preserve completed fixes.

Inspect all reported checks rather than only checks marked required. Report pending, canceled, skipped, and missing checks separately. A skipped optional job can be expected, but a missing required result is not success.

If no checks exist, report that fact instead of claiming green CI. If the head changes during inspection, read results for the new head. Do not substitute local results for hosted CI.

The 20-minute deadline applies to the requested review, not to CI repair. Do not reset that deadline after a push. A review timeout does not end useful CI repair work.

## Wait for the review

Inspect existing feedback first. If the requested review already completed, proceed to its findings without waiting. Otherwise, use the request time, requested head, and prior review identifiers from the handoff or GitHub.

Set the deadline 20 minutes after the request. If its time cannot be established, record that limit and start one bounded wait from now. On resumption, retain the recorded deadline rather than starting another 20-minute wait.

Use a supported watch mechanism or poll GitHub about once per minute. Keep individual waits short enough to report progress and accept user input. Do not send another review request on each poll.

Inspect review records, their authors, their commit identifiers, and submission times. A completed review from the requested reviewer for the requested commit ends the wait. Its inline comment count can be zero.

Do not treat CI completion, unrelated comments, or disappearance from the reviewer list as proof that Copilot finished. If the head changes, identify which commit the review covers. Do not silently restart the deadline.

Handle temporary read errors within the existing deadline. Report persistent access failures rather than treating missing data as an empty review. Stop waiting when the deadline arrives or the user interrupts.

At the deadline, report a timeout and the last observed state. Address available findings, but state if the review is incomplete. Do not interpret a timeout as approval or proof that Copilot is unavailable.

## Address the findings

Read the completed review body, inline discussions, and relevant top-level comments. Get all result pages. Assess each finding against the issue and current code before changing anything.

Treat requested changes in a human COMMENTED review as actionable, including reviews from the PR author. GitHub's review state does not determine whether a finding needs a response. Address these requests with the same care as CHANGES_REQUESTED findings. Do not require the user to submit a formal change request. A comment with no requested change does not require a code edit.

Address available human findings while a Copilot request remains pending. Those findings do not complete the Copilot wait. Before reporting completion, read human feedback again and address new requests within scope. Report unresolved requests even if CI is green or Copilot found no problems.

Use these responses:

- Fix a demonstrated problem within the agreed scope.
- Explain a disputed suggestion with evidence.
- Identify an unrelated problem for separate work.

A request to address review includes corrections and factual replies within the agreed scope. Obey narrower user instructions. A new product decision or broader scope returns to the parent or user.

Before editing, confirm the task worktree and branch against the PR head. Preserve unrelated work. Make corrections in that worktree or a new isolated worktree. Add or update useful tests and execute affected checks plus required project checks. Commit the corrections and push them to the same PR branch. Inspect unexpected remote changes before pushing. Do not force-push over another contributor’s work.

Reply with the correction and relevant commit, or explain why no change was made. Resolve only discussions whose concern was fixed and whose resolution the project permits. Leave disputed and undecided discussions open.

Do not file unrelated issues automatically. Report proposed follow-up work unless filing it is also authorized. Do not weaken a success condition to satisfy a review suggestion.

After a push, refresh CI and review information for the new head. Update the PR description if the changes invalidate its claims. Earlier review and test results still describe the earlier commit.

If corrections need another Copilot review, inspect current-head requests, timeline events, and completed reviews first. Reuse an automatic request and its timestamp instead of duplicating it. If no applicable request or review exists, request one. Report the observed review state. This invocation waits for one review cycle by default. Do not start another 20-minute review wait without a further request. Continue the CI repair cycle for the latest head.

## Report the result

Return the PR URL, current head commit, corrections, and executed test results. Distinguish fixed, disputed, deferred, and unanswered findings. Include current CI and review state and whether the review wait completed or timed out. State the commit whose hosted checks passed, or the concrete CI blocker.

Record a new review request time when corrections require another review. Pass that time and the requested commit to the next invocation. Do not treat an earlier clean review as approval of later changes.

If blocked or interrupted, preserve the worktree and report the next useful action. Return product decisions to the parent when delegated. Do not ask the user directly from a subagent.

Do not merge or enable automatic merge. Do not create a replacement PR because review handling failed. A partial result remains useful when its limits are explicit.
