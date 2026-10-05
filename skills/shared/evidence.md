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

## Reading PR state

Read a PR's state with `python3 cli/ghflow.py pr-state PR_URL`, run from this skills repository. It reports the current head, each check's state with required checks from rulesets, review requests from the timeline, and reviews with their commits. It matches a Copilot request to reviews authored by `copilot-pull-request-reviewer[bot]`.

`base_behind_by` is the number of base-branch commits that the head does not contain. A value of 0 means the head contains the current base tip.

Use `latest_review_requests` to decide whether a review request exists and whether a later review answered it. `pending_review_requests` lists only reviewers that GitHub still shows as requested, and it can be empty while a request is live. Request events do not record a commit; after later pushes, compare the request time with the push times to decide which head it covers.

A part that the tool could not read is `null` and has an entry in `errors`. Exit status 2 means some parts failed. Treat a `null` part as unread, not as empty. The tool does not judge whether a review is favorable; read the review bodies yourself.

## Verifying a commit

Before you put a commit identifier from a report or handoff into a handoff, a record, or a merge, verify it. Run `python3 cli/ghflow.py verify-commit SHA --repo OWNER/NAME` from this skills repository. Add the facts that you expect: `--subject` with the first line of the commit message, `--on BRANCH` for the branch that should contain it, and `--pr-head PR_URL` when it should be the PR's current head. Use the full SHA that the tool reports.

Exit status 0 means the commit exists and each expectation holds. Exit status 3 means an expectation is false. Exit status 1 means GitHub did not find the commit, which can mean it is not pushed. Do not pass on an identifier that failed. Read the branch again or return the mismatch to the agent that reported it.

## Writes to GitHub

Before you create something, search for an existing equivalent. On resumption, inspect the recorded URL first.

Record the URL or identifier that a write returns immediately. After a write, read the saved result back. A command's success response is not proof.

A failed or interrupted command can leave some changes complete. Read GitHub before you retry. Do not create a second item while the first result is uncertain. Retry only the steps that failed. Do not delete a successful result to undo a later failure.

Another person or process can change an item between reads. Read it again before an update and preserve changes that you did not make. If the current content differs from what you expect, investigate before you overwrite it.

Do not change accounts, credentials, subscriptions, repository settings, or protection rules to get past a permission error. Report the required action instead.

## Reports

Report what you did, what you checked, and what remains. State which checks you executed and which you only inspected. Report completed, failed, and uncertain steps separately, with enough information to resume.

A partial result is useful when its limits are explicit. If you are blocked or interrupted, preserve the worktree and report the next useful action.
