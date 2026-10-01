# First experiment

Proposal from the founding discussion on 2026-09-30. The bottom-up approach is agreed; this particular starting task has not yet been selected or implemented.

## Candidate task

Collect complete PR review context, then use it to address feedback on an existing PR. This is useful without first building issue intake, board management, or an execution loop, and it exercises a clear split between fetching information and judging what it means.

Start with the retrieval operation alone. Follow with the skill procedure after the operation proves useful. Independent review of the underlying code remains a distinct activity from addressing someone else's comments.

## Candidate operation

Given a PR URL or explicit repository and PR number, collect the PR description, base and head identifiers, reviews, inline threads, resolution state, and top-level comments. Include relevant check status if needed by the chosen task. Preserve source identifiers and URLs so the agent can trace a finding back to GitHub.

Handle pagination and expose retrieval failures. Do not present a partial collection as complete. Record the head observed for the collection and detect movement during retrieval where practical; GitHub reads are not a single snapshot taken at one instant.

The first operation should be read-only. Replying, resolving threads, pushing fixes, and updating PR content are separate changes to consider after the read path works. Command names and output schema should emerge from this task rather than an interface intended to cover every future task.

## Candidate skill procedure

Use collected context to distinguish feedback requiring a fix, feedback needing discussion, and work outside the PR's scope. Check the code rather than accepting every review suggestion. After authorized fixes, run appropriate verification and refresh context for the new head.

Carry forward the predecessor's useful distinction: disputing a finding does not itself establish that the finding is resolved. The exact reply and thread-resolution policy should be decided when we design commands that change GitHub data.

## How to evaluate it

Use a real PR, plus small tests for situations the live example does not cover. Check that:

- Multiple pages of feedback are collected without omission or duplication.
- Top-level comments and reviews without inline threads remain visible.
- Missing permissions, failed requests, and absent checks remain distinguishable.
- Results identify their source and commit, and the tool reports if the PR head changes.
- A new session can understand the outstanding feedback without information available only in the previous conversation.

Record what the tool saved the agent from doing, what it missed, and what remained a judgment call. Passing parser tests alone does not establish that the phase is useful.

## When the experiment is done

The experiment succeeds when it makes one real review-feedback task easier and more reliable, with its limitations recorded. It does not need a demonstration of every workflow phase, automatic issue selection, background waiting, agent spawning, or merge automation.

Use the result to choose the next operation. Do not build a system for choosing and running tasks to demonstrate this one.
