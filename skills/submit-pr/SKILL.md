---
name: submit-pr
description: Prepare and publish a pull request from committed issue work, confirm the remote state, and request Copilot review. Use for authorized PR submission or resumption after a partial submission.
---

# Submit a pull request

Prepare a pull request (PR) from existing committed work. Request Copilot review after publication. Return the PR and review-request details for a follow-up task without waiting for findings or merging.

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

Record the request time, requested head commit, and existing review identifiers. Read back the request or resulting review. Distinguish requested, pending, completed, unavailable, and failed.

Inspect completed reviews and their commit identifiers, not only inline comment counts. A completed review can have no inline comments. Comments alone do not prove that the requested reviewer examined the current head.

If access is unavailable, return the reason and the local-review handoff. A pending request or temporary network error does not establish lack of access. Do not recreate the PR when requesting review fails.

The parent can use `review-changes` for local review. Supply the issue, base and head commits, repository, and known implementation model. Do not claim that another service necessarily uses a different underlying model.

## Report and hand off

Read current CI and review state for the published head. Report pending checks as pending and absent checks as absent. Do not substitute local test success for hosted results.

Return the PR URL, head commit, worktree, and branch. Include the request time, requested reviewer, existing review identifiers, and observed CI and review state. Report requested board changes and incomplete operations.

If review or tests concern an earlier commit, state that limit. A later push requires a new assessment of affected checks and review coverage. Request another review when necessary rather than assuming it happens automatically.

The parent can use `address-pr-review` to wait, address findings, and repair failing CI. Pass existing authorization for that task with the handoff. Do not repeat publication or ask for authorization already supplied.

Do not wait for review, change code to address findings, merge, or enable automatic merge in this skill. Each follow-up task can also start from an existing PR without this handoff.
