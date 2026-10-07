---
name: submit-pr
description: Prepare and publish a pull request from committed issue work, confirm the remote state, and request a review. Use for authorized PR submission or resumption after a partial submission.
---

# Submit a pull request

Publish a PR from existing committed work, move the issue to In review, and request a review. Hand off to a follow-up task without waiting for findings. Do not change code to address findings, merge, or enable automatic merge.

Apply [Authorization](../shared/authorization.md), [Evidence](../shared/evidence.md), and [Review](../shared/review.md) throughout.

## Prepare the branch and description

Read the issue, project instructions, and implementation report. Confirm the repository, worktree, branch, intended base, and authorization to publish.

Inspect the working tree and task commits, and preserve unrelated or uncommitted work. Do not publish an incomplete change as ready for review.

Refresh remote references and inspect changes on the base. Do not rebase merely to get a cleaner history. If integration is necessary, follow the project rules and repeat the affected checks after resolving conflicts.

Review the task diff from the merge base of the base and task branches. Inspect the full list of changed files, including generated output and lockfiles, and explain unexpected changes before you publish. Make sure that the published commits contain the tested changes. Report missing or stale test evidence instead of copying an earlier success claim.

Write a title and body that explain the problem, the resulting behavior, the test evidence, and material limits. Use the repository template when one exists. Keep detail proportional to the change, and distinguish local tests from hosted CI.

Use a closing reference such as `Closes #N` only when the PR completes that issue. A child PR does not close its broader parent.

Write the body to a UTF-8 file and pass it with `--body-file`. For a preparation-only request, the prepared body is the result. Do not push or create a PR without publication authorization.

## Publish and confirm

Run `gh auth status` and check the installed help for the commands you need. Search for an existing PR for the same repository, branch, and base. On resumption, inspect the known PR URL first.

Push the branch explicitly, then make sure that the remote commit matches the intended local commit. If the remote has unexpected work, resolve the difference before publishing. Do not force-push over it.

Create the PR with an explicit repository, head, base, title, and body file. Make it a draft when requested or when work remains incomplete. Do not add labels, assignees, or comments that nobody requested. Do not use `gh pr create --dry-run` to avoid writes: it can push changes.

Record the returned URL immediately. Read back the body, branch, base, and head commit.

## Mark the issue in review

When the PR is ready for review, move the issue it implements to In review, following [Board status](../shared/board-status.md). A draft PR for unfinished work does not qualify. If the board update fails, report it and continue with the review request.

## Request a review

For an agent pull request, the primary review source is a different-model local review, as [Review](../shared/review.md) states. A completed independent local review of the published head lets the PR proceed. A review that covers an earlier commit does not qualify. Do not request Copilot by default.

Request Copilot review only when the user asked for it. Read the current requests and reviews with `pr-state`, described in [Evidence](../shared/evidence.md). Follow the request rules in [Review](../shared/review.md): check for an existing request first, including an automatic one.

Record the request time, the requested head, and existing review identifiers. Read back the request or the resulting review.

If the user requested Copilot and it is unavailable, use a completed different-model local review that covers the head as the review source. Only when no such review covers the head, return the reason and a handoff for local review with [review-changes](../review-changes/SKILL.md), supplying the issue, repository, base and head commits, and the implementation model if known. Do not recreate the PR because a review request failed.

## Report and hand off

Read the CI and review state for the published head. Return:

- The PR URL, head commit, worktree, and branch.
- The review source used. For a local review, include its head, findings, and the recorded model identities that show it is different from the implementer. For a Copilot request, include its time, requested reviewer, and existing review identifiers.
- The observed CI and review state.
- The board transition result, or why it was skipped or failed.
- Any other incomplete operations.

The parent can run [address-pr-review](../address-pr-review/SKILL.md) next to wait for review, address findings, and repair CI. Pass the existing authorization with the handoff. Each follow-up task can also start from an existing PR without this handoff.
