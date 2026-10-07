# Burndown the ready queue

Coordinate the sequential delivery of issues currently staged in the project board's `Ready` column. Process each issue one at a time up to the agreed endpoint using [express-issue](express-issue.md). Stop immediately if an issue hits an unexpected blocker, check failure, or review objection. This skill is strictly bounded to the existing `Ready` queue and does not select or prioritize work from the backlog.

Apply [Authorization](../shared/authorization.md), [Evidence](../shared/evidence.md), [Review](../shared/review.md), [Board status](../shared/board-status.md), and [Agent identity](../shared/identity.md) throughout.

## Audit the Ready queue

Read the current items from the project board:

```bash
gh project item-list NUMBER --owner OWNER --format json
```

1. Identify all items where `status` is `Ready`.
2. Sort them by priority (`P0` before `P1`).
3. If the `Ready` column is empty, report that the queue is clear and hand off to [curate-ready-queue](curate-ready-queue.md).
4. Confirm the delivery endpoint with the user:
   - **Through review follow-up (default)**: Implements, verifies with independent review, submits PR, and addresses feedback, leaving the PR open for user review.
   - **Through merge**: Merges the PR upon green CI and affirmative review, following the merge policy in [merge-pr](merge-pr.md).

## Deliver issues sequentially

Process one issue at a time:

1. Select the top unblocked issue in `Ready`. When delivering to a review follow-up endpoint (without merge), ensure the selected task is independent of other in-flight PRs so it can branch cleanly from `origin/main`. If a task depends on code in an unmerged PR, either authorize merging the prerequisite PR first or defer the dependent task.
2. Dispatch a subagent to execute [express-issue](express-issue.md) on that issue, passing the confirmed repository, issue number, authorization, and endpoint.
3. Once the subagent completes, verify the result:
   - Did the task reach the expected endpoint?
   - Is the project board status updated to `In review` or `Done`?
4. **Hard stop on disruption**:
   - If the task encounters a persistent test failure, review defect that cannot be resolved within the cycle, or an unexpected merge conflict:
     - **Halt the burndown immediately.**
     - Do not advance to the next issue in the queue.
     - Preserve the worktree and branch.
     - Return the blocker, error logs, and proposed remediation to the user.
5. For a merge endpoint, wait for CI on the base branch's merge commit before you start the next issue. If it fails, treat it as a disruption and halt.
6. If the issue successfully completes to the authorized endpoint, proceed to the next item in `Ready`.

## Conclude and hand off

When all issues in the active `Ready` queue have been delivered:

1. Present a delivery summary table:
   - Issue number and title.
   - Pull request URL and head commit SHA.
   - Review evidence (local reviewer model or Copilot).
   - Final status on the project board (`In review` or `Done`).
2. Hand off to [curate-ready-queue](curate-ready-queue.md) to inspect the board's `Backlog` and curate the next batch of tasks into `Ready`.
