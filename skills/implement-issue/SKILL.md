---
name: implement-issue
description: Implement a specified GitHub issue in an isolated worktree, assess its success conditions, review the changes, and commit them for PR preparation. Use when implementation is requested, including continuation of existing work.
---

# Implement an issue

Produce tested, committed changes for the requested issue. A commit records a version of project files. Return enough evidence for another agent to prepare a pull request (PR).

This skill ends with a local branch and a report. It does not include publishing a PR, external review, or merge. Preserve separately authorized next actions for the parent or next operation.

## Read the issue and current code

Read the project instructions, issue body, and relevant comments. Identify the intended result, scope limits, success conditions, and confirmed decisions. Do not require labels or documents from another skill.

Inspect relevant code and tests at the current revision. Treat issue file references and earlier test results as historical evidence until examined. Determine whether the reported problem remains.

If part of the issue is already satisfied, record the evidence and implement only the remaining requirements. If no change remains, report that result. Do not create unrelated work to justify a commit.

Resolve routine implementation choices from current code and project conventions. If a missing decision changes scope or user behavior, explain the question and recommend an answer. Do not silently redefine the issue.

When delegated, return necessary questions to the parent agent. In a direct session, ask the user. The parent can use `interview-issue`, but this skill does not require it.

## Prepare an isolated workspace

A worktree is a separate checkout connected to a Git repository. Inspect the current status, branches, and existing worktrees before making changes. Preserve unrelated work.

Determine the intended base branch from the project or request. Refresh its remote reference when access permits. Do not assume that the branch is named main or that the current checkout is the correct base.

Create a worktree and task branch using the project conventions. Do not reset or switch the shared checkout. Do not use another session's worktree merely because its name matches the issue.

If resuming, confirm the supplied worktree and branch before editing. Read its existing changes and records. Resume authorized work rather than creating a second competing implementation.

Install dependencies as the project directs. Use test configuration and isolated data where required. Do not copy credentials or connect to live services merely to make tests pass.

Establish the relevant baseline before implementation. A baseline records test results before your changes. Record existing failures and environment limits separately from new failures.

If a baseline problem prevents meaningful verification, investigate or report the blocker. Independent implementation can continue when it remains useful. Do not describe incomplete verification as success.

## Plan the change and its evidence

Make a short plan against the current code. Connect each planned change to an issue requirement. Prefer small steps that demonstrate useful behavior across the relevant components.

For each success condition, identify a test, command, or human assessment. Distinguish existing checks from checks that you must add. Record what each check establishes and its expected result.

Keep tests for new behavior separate from tests that protect existing behavior. A passing test suite does not by itself prove the new result. Missing tests or setup errors do not demonstrate the reported bug.

Use the project's record format when it has one. Otherwise, keep brief notes with the task. Do not create a fixed set of planning files for every issue.

## Implement and test

Obey the project's test-first rules. For a bug fix, demonstrate the relevant failure before changing the implementation when feasible. Make sure that the failure comes from the reported behavior, not a broken setup.

Implement the smallest change that satisfies the issue. Add tests for the intended behavior and relevant error cases. Keep unrelated cleanup outside the task.

Execute the specific checks for each changed behavior and read their output. Then do the broader checks required by the project. Use project commands rather than copying their internal steps into a new test procedure.

Change tests when the intended behavior requires it, and explain why. Do not remove useful assertions merely to make the suite pass. If the issue requirement itself is wrong, return that decision to the parent or user.

If a requirement needs human judgment, prepare the requested example or demonstration. State what remains for the person to assess. An automated result does not replace that judgment.

## Review and commit

Inspect the complete task diff, not only the last edited file. Compare the branch with its intended base through their shared ancestor. Include uncommitted and newly created files in the review.

Look for incomplete changes, missed callers, error cases, unrelated edits, and missing documentation. Examine changed tests for assertions that no longer establish the intended behavior. Correct findings within scope.

After relevant edits, execute the affected checks again. If the base changes or conflicts require resolution, reassess which results remain valid. Do not reuse evidence for code that the check did not examine.

Stage only intended files and inspect the staged diff. Commit logical changes according to project conventions. Do not describe a partial or failing implementation as ready for PR preparation.

Record the tested revision and remaining working-tree changes. If a commit hook changes tested files, execute the affected checks again. Make sure that the commit contains the changes described in the report.

This self-review is not independent review. If another reviewer supplies findings, distinguish that review from your own checks. Do not claim independent verification when none occurred.

## Return the result

Return the issue URL, worktree path, branch, base revision, and final commit identifiers.

Include the implementation model when session metadata identifies it. Otherwise, record it as unknown. This lets the parent select a different model for later local review. Summarize the changes and the result for each success condition. Give the executed commands and observed results, including failures and checks not executed.

State whether the changes are ready for PR preparation, incomplete, or awaiting a decision. Include existing failures, remaining human assessments, and unresolved risks that affect the result. Keep the report in plain technical English.

If interrupted or blocked, preserve the worktree and report completed work and the next useful action. Do not publish comments or change board fields merely to report a blocker. Use separate authorization for GitHub changes.

Do not push, open a PR, merge, or remove the worktree as part of this skill. Hand off separately requested actions with their authorization. Do not ask for approval that the user already gave.
