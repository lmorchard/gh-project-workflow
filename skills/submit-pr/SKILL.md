---
name: submit-pr
description: Prepare and publish a pull request from committed issue work, confirm the remote state, wait for Copilot review, and address its findings. Use for authorized PR submission or resumption after a partial submission.
---

# Submit a pull request

Prepare a pull request (PR) from existing committed work. Request Copilot review after publication and wait up to 20 minutes. Address the findings, then report the current checks and review state without merging.

## Prepare the branch and description

Read the issue, project instructions, and implementation report. Confirm the repository, worktree, branch, intended base, and authorization to publish. Use existing authorization without asking again.

Inspect the working tree and task commits. Preserve unrelated or uncommitted work. Do not publish an incomplete change as ready for review.

Refresh remote references and inspect changes on the intended base. Do not rebase merely to obtain a cleaner report. If integration is necessary, obey project rules and repeat affected checks after conflict resolution.

Review the task diff through the shared ancestor of the base and task branches.

Inspect the full list of changed files, including generated output and lockfiles. Explain unexpected changes before publishing. Make sure that the published commits contain the tested changes. Report missing or stale test evidence rather than copying an earlier success claim.

Write a title and body that explain the problem, resulting behavior, test evidence, and material limits. Use the repository template when present. Keep detail proportional to the change.

Use a closing issue reference only when the PR completes that issue. A child issue does not authorize closing its broader parent. Distinguish local tests from hosted CI, the service that checks published commits.

Keep the body in a UTF-8 file and use `--body-file`. A prepared PR body is sufficient for a preparation-only request. Do not push or create a PR without publication authorization.

## Publish and confirm

Use `gh auth status` and inspect relevant command help. Search for an existing PR for the exact repository, branch, and base. On resumption, inspect the known PR URL first.

Push the intended branch explicitly, then make sure that the remote commit matches the intended local commit. Do not force-push over unexpected remote work. Resolve the difference before publishing.

Create the PR with explicit repository, head, base, title, and body. Set draft status when requested or when work remains incomplete. Do not use `gh pr create --dry-run` as a promise of no writes: it can push changes.

Record the returned URL immediately. Read back the body, branch, base, and head commit. If a command fails, inspect GitHub before repeating creation.

Apply requested board changes only after the PR exists. Report a board failure separately from PR creation. Do not add unrelated labels, assignees, or comments.

## Request Copilot review

This workflow requests Copilot review unless the user selects another reviewer. Inspect the current requests and completed reviews first. Do not submit another request for the same commit merely because the response is pending.

On versions that support it, use this command with the actual PR URL:

```sh
gh pr edit PR_URL --add-reviewer "@copilot"
```

Inspect installed help before relying on the flag. Request a reviewer, not a coding-agent assignment or a comment that asks Copilot to modify code. Do not change account subscriptions or repository policy to obtain access.

Read back the request or resulting review. Distinguish requested, pending, completed, unavailable, and failed.

Inspect completed reviews and their commit identifiers, not only inline comment counts. A completed review can have no inline comments. Comments alone do not prove that the requested reviewer examined the current head.

If access is unavailable, return the reason and the local-review handoff. A pending request or temporary network error does not establish lack of access. Do not recreate the PR when requesting review fails.

The parent can use `review-changes` for local review. Supply the issue, base and head commits, repository, and known implementation model. Do not claim that another service necessarily uses a different underlying model.

## Wait for the review

After the request, record its time, current head commit, and existing review identifiers. Set a deadline 20 minutes after the request. If resuming, retain the original deadline rather than starting another 20-minute wait.

Use a supported watch mechanism or poll GitHub about once per minute. Keep individual waits short enough to report progress and accept user input. Do not send another review request on each poll.

Inspect review records, their authors, their commit identifiers, and submission times. A new completed Copilot review for the requested commit ends the wait. Its inline comment count can be zero.

Do not treat CI completion, unrelated comments, or disappearance from the reviewer list as proof that Copilot finished. If the head changes, identify which commit the review covers. Do not silently restart the deadline.

Handle temporary read errors within the existing deadline. Report persistent access failures rather than treating missing data as an empty review. Stop waiting when the deadline arrives or the user interrupts.

At the deadline, report a timeout and the last observed state. Address available findings, but state if the review is incomplete. Do not interpret a timeout as approval or proof that Copilot is unavailable.

## Address the findings

Read the completed review body, inline discussions, and relevant top-level comments. Get all result pages. Assess each finding against the issue and current code before changing anything.

Use these responses:

- Fix a demonstrated problem within the agreed scope.
- Explain a disputed suggestion with evidence.
- Identify an unrelated problem for separate work.

When submission includes this review cycle, corrections and factual replies to its findings are part of the requested task. Obey narrower user instructions. A new product decision or broader scope returns to the parent or user.

Make corrections in the task worktree. Add or update useful tests and execute affected checks plus required project checks. Commit the corrections and push them to the same PR branch.

Reply with the correction and relevant commit, or explain why no change was made. Resolve only discussions whose concern was fixed and whose resolution the project permits. Leave disputed and undecided discussions open.

Do not file unrelated issues automatically. Report proposed follow-up work unless filing it is also authorized. Do not weaken a success condition to satisfy a review suggestion.

After a push, refresh CI and review information for the new head. Update the PR description if the changes invalidate its claims. Earlier review and test results still describe the earlier commit.

If corrections need another Copilot review, request it and report it as pending. This invocation waits for one review cycle by default. Do not start unlimited 20-minute waits or repair cycles without a further request.

## Report and hand off

Read current CI and review state for the published head. Report pending checks as pending and absent checks as absent. Do not substitute local test success for hosted results.

Return the PR URL, head commit, requested board changes, and observed CI and review state. Include fixed, disputed, and deferred findings, missing operations, and the next useful action. State whether the wait completed or timed out.

If review or tests concern an earlier commit, state that limit. A later push requires a new assessment of affected checks and review coverage. Request another review when necessary rather than assuming it happens automatically.

Do not merge or enable automatic merge. Return unresolved findings and pending follow-up review to the parent. Preserve authorization for further requested actions without silently expanding it.
