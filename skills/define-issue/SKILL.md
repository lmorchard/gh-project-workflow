---
name: define-issue
description: Develop a request or existing GitHub issue into a scoped issue draft with evidence, success conditions, and unresolved decisions. Use before implementation or when an issue is not clear enough to attempt.
---

# Define an issue

Produce an issue draft that another agent can understand without this conversation. Determine whether implementation can start or a decision is still necessary. Issue definition does not include implementation.

## Read the request and evidence

Read the project instructions and the supplied request. For an existing issue, read its body and comments. Read linked issues or pull requests when they affect scope or decisions.

For code investigation, read [Research the current code](references/research.md).

Inspect relevant code and tests before accepting technical claims. Record the source revision and specific files that support your findings. Distinguish observations from assumptions and reports in older comments.

A board status or label is evidence of a previous decision, not proof of readiness. If board information is supplied, compare it with the issue. Do not expand one issue review into a board audit.

Read test assertions before citing a test as evidence. Distinguish a proposed test from an existing test. If you do not execute a test, state that limit.

If a necessary source is unavailable, report the missing evidence. Continue with independent investigation where useful. Do not infer success from missing results.

## Resolve the task

State the intended user result before choosing a solution. Preserve decisions that the user already made. Do not ask the user to approve those decisions again.

If a missing decision changes scope or behavior, propose an answer with its tradeoff. Ask one focused question at a time. Continue investigation that does not depend on the answer.

Keep routine implementation choices out of the interview unless they change cost, compatibility, permissions, or the intended result. A missing implementation plan does not itself block readiness.

If the issue contains several independently useful changes, propose a smaller first issue. Explain what it proves and what remains. Do not silently replace the original goal with the smaller task.

When delegated, return necessary questions to the parent agent. Do not treat the absence of a human answer as approval. You can still produce a draft that identifies the open decision.

## Draft the issue

Use short sentences and familiar technical terms. Define unfamiliar terms at first use. Keep exact identifiers and commands unchanged.

Keep the draft proportional to the task. Include these facts in the structure that fits:

- The problem and intended result.
- Included changes and explicit limits.
- Success conditions and how to assess them.
- Dependencies, confirmed decisions, and unresolved questions.
- Relevant source links and code references.

A success condition describes observable behavior, not merely a file that exists or a command that succeeds. Explain what each proposed test establishes. Separate evidence of new behavior from tests that protect existing behavior.

An existing automated test is not required for every condition. Name tests that implementation must add. If human judgment is necessary, state what the person must assess.

Keep the original issue text separate from proposed edits. Do not erase the original intent when proposing a split. Do not put essential decisions only in a separate conversation or report.

## Return the result

State whether the draft is ready for implementation, needs a decision, or lacks evidence. Give the specific reason. This assessment does not authorize implementation or merge.

Return the draft, unresolved questions, and a short evidence summary. State which checks you executed and which you only inspected. If you propose a child issue, explain its relationship to the original issue.

By default, return a draft without changing GitHub. If the user explicitly requests filing or updates, use that authorization and preserve unrelated content. Issue definition alone does not authorize comments, labels, board changes, or code edits.
