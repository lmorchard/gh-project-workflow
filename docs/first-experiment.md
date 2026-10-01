# First experiment

This document proposes a first task from the discussion on 2026-09-30. Les agreed to start with individual operations. We did not select or implement this task.

## Proposed task

Get all review information for an existing pull request (PR). A PR proposes changes for review. Then use that information to assess and correct problems from the review.

The first tool will only read information. Skill instructions can use that tool after it proves useful. An independent code review remains a separate task from corrections to review comments.

## Proposed read operation

The input is a PR URL, or a repository name and PR number. A repository stores project files and their history. The result includes the PR description and identifiers for its base and head commits.

The base is the target version for the proposed changes. The head is the latest proposed version. The result also includes reviews, comment threads, thread status, and comments outside threads.

A thread groups comments about one code location. Keep source identifiers and URLs with each result. If the task requires automated check results, include their status.

Get all pages of results. Report failed requests. Do not describe a partial collection as all available information.

Record the head identifier for the collection. Where practical, detect a changed head during the read. Separate GitHub reads do not form a single snapshot.

Replies, thread resolution, code uploads, and PR edits remain separate operations for later design. Thread resolution marks a discussion as finished. The first read operation does not change GitHub data.

## Proposed skill procedure

The agent uses the results to identify necessary corrections, questions, and problems outside the PR scope. The agent examines the code before accepting a review suggestion. After authorized corrections, the agent does the relevant tests and gets current PR information.

Disagreement with a finding does not establish that the problem is resolved. We will decide reply and thread-resolution rules when we design commands that change GitHub data. Command names and result formats remain open.

## Evaluation

Use a real PR and small tests for other situations. Make sure that the results meet these conditions:

- The collection contains all pages without duplicate feedback.
- Comments outside threads and reviews without threads remain visible.
- Missing permissions, failed requests, and absent checks produce different results.
- Results identify their source and commit.
- The tool reports a changed head when it detects one.
- A new session can understand the feedback without information from an earlier conversation.

Record the steps that the tool removes from the agent task. Record omissions and decisions that still require judgment. Passing tests alone does not establish that the task is easier.

## Completion

The experiment succeeds when it makes one real review task easier and more reliable. Record its limits. Use the results to select the next operation.

The experiment does not require every phase of the workflow. It does not require automatic task selection, background polling, additional agents, or automatic merges. Do not add a system that controls all tasks to demonstrate this one.
