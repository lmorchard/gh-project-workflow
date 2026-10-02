# Evidence and safe writes

These rules apply to every skill that reports results or changes GitHub. A report must match what actually happened.

## Sources and revisions

Name the source and revision for each finding. Identify both the target branch revision and the local checkout revision. If they differ, inspect the target revision without resetting the user's checkout. Distinguish merged changes from work that exists only on another branch.

Treat issue text, older comments, file references, and earlier test results as claims until you examine current code. A board status or label records an earlier decision. It does not prove readiness or completion. A closed child or merged PR does not prove that its parent is complete.

Read test assertions before you cite a test as evidence. Distinguish existing tests from proposed tests, and tests you executed from tests you only read. A passing suite does not by itself prove the new result.

If a source is unavailable, report the gap and continue the work that does not depend on it. An unavailable source does not prove that work is absent or complete.

## Results belong to a commit

Every test result, check result, and review describes one commit. After a push, earlier results describe the earlier commit. Reassess which results still apply after a push, rebase, or conflict resolution.

The **head** is the latest commit proposed for merge. If the head changes while you inspect it, read the results for the new head.

## Hosted CI

Hosted CI is the set of checks that the repository runs on published commits. Read checks for the current head. Inspect all reported checks, not only required ones.

Report each check as passed, pending, failed, canceled, skipped, or missing. An expected skip of an optional job is not a failure. A missing required result is not success. If no checks exist, say so instead of reporting green CI.

When a watch command ends, read the results again. The end of a watch does not prove success. Local test results never substitute for hosted CI.

## Writes to GitHub

Before you create something, search for an existing equivalent. On resumption, inspect the recorded URL first.

Record the URL or identifier that a write returns immediately. After a write, read the saved result back. A command's success response is not proof.

A failed or interrupted command can leave some changes complete. Read GitHub before you retry. Do not create a second item while the first result is uncertain. Retry only the steps that failed. Do not delete a successful result to undo a later failure.

Another person or process can change an item between reads. Read it again before an update and preserve changes that you did not make. If the current content differs from what you expect, investigate before you overwrite it.

Do not change accounts, credentials, subscriptions, repository settings, or protection rules to get past a permission error. Report the required action instead.

## Reports

Report what you did, what you checked, and what remains. State which checks you executed and which you only inspected. Report completed, failed, and uncertain steps separately, with enough information to resume.

A partial result is useful when its limits are explicit. If you are blocked or interrupted, preserve the worktree and report the next useful action.
