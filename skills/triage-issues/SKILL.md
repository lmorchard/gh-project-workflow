---
name: triage-issues
description: Evaluate a batch of open issues against current target code and git history. Add triage labels, post findings comments, and close already completed or obsolete issues with evidence. Do not implement code or modify project boards.
---

# Triage issues

Evaluate a batch of open issues to identify completed, obsolete, well-defined, or uncertain work. Post findings comments on the issues and apply triage labels (`triage:agent-closed`, `triage:needs-input`, `triage:needs-definition`, `triage:ready`). Close confirmed completed or obsolete issues with evidence. This skill does not implement changes, submit PRs, or modify project boards.

Apply [Authorization](../shared/authorization.md), [Evidence](../shared/evidence.md), and [Agent identity](../shared/identity.md) throughout.

## Select the issue batch

Identify the issues to evaluate:
- A parent issue number (evaluating the sub-issues attached to that parent),
- An explicit list of issue numbers, or
- A query of open issues without `triage:*` labels, optionally filtered by area label (such as `core` or `tui`).

Keep batch sizes bounded to 5 to 10 issues per run to ensure thorough inspection of target code and git history.

## Inspect code and history

For each issue in the batch:

1. Read the issue title, body, comments, and any linked issues or PRs.
2. Search git history and merged PRs in the subject repository for relevant changes or commits that already address the problem.
3. Inspect current code and tests at the target revision (such as `main`).
4. Compare requested behavior and assumptions against current architecture and implementation.

Treat issue claims and older comments as unverified until you check current code.

## Classify each issue

Assign each issue to one classification based on evidence:

- **Already completed**: Current code, merged PRs, or existing tests already satisfy the requested result. Note the exact commit SHA, PR number, or test path.
- **Obsolete or not planned**: Architectural direction changed, the referenced component was removed or superseded, or the issue is no longer relevant. Note the reason and current state.
- **Needs human input**: The core purpose or scope requires product or design decisions from the user. Identify the exact 1 to 2 questions with specific choices or tradeoffs.
- **Needs technical definition**: The goal is valid and desirable, but the issue lacks concrete technical scope, file boundaries, or acceptance criteria.
- **Ready as-is**: Problem, scope, and verification criteria are clear, accurate, and actionable against current code.

## Update GitHub records

For each evaluated issue:

1. Post a concise comment with:
   - Summary of findings against current code.
   - Cited evidence (commit SHAs, file paths, test assertions, PRs).
   - The blocking questions or missing criteria, if applicable.
2. Apply the matching triage label:
   - `triage:agent-closed`
   - `triage:needs-input`
   - `triage:needs-definition`
   - `triage:ready`
3. If the issue is already completed, close it:
   - `gh issue close ISSUE_URL --reason completed`
4. If the issue is obsolete or not planned, close it:
   - `gh issue close ISSUE_URL --reason "not planned"`
   - Add the `wontfix` label if the repository uses it.
5. If updating labels fails because a label does not exist in the repository, create the label with a brief description and retry.

## Return the batch summary

Return a structured summary table to the parent:

- Issue number and title.
- Classification.
- Key evidence or blocking question.
- GitHub action taken (closed with reason, labeled).

Do not implement code, open pull requests, or alter project board cards during triage.
