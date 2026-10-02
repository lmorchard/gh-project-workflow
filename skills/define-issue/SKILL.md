---
name: define-issue
description: Develop a request or existing GitHub issue into a scoped issue draft with evidence, success conditions, and unresolved decisions. Use before implementation or when an issue is not clear enough to attempt.
---

# Define an issue

Produce an issue draft that another agent can act on without this conversation, and say whether implementation can start. This skill does not change GitHub or implement anything.

Apply [Authorization](../shared/authorization.md) and [Evidence](../shared/evidence.md) throughout.

## Read the request and evidence

Read the project instructions and the request. For an existing issue, read its body and comments, and any linked issues or PRs that affect scope or decisions. For code investigation, follow [Research the current code](references/research.md).

Inspect the relevant code and tests before you accept technical claims. Record the source revision and the files that support each finding.

If board information is supplied, compare it with the issue. Do not expand one issue review into a board audit.

## Resolve the task

State the intended user result before choosing a solution. Keep decisions the user already made, without asking for them again.

If a missing decision changes scope or behavior, propose an answer with its tradeoff. Continue the investigation that does not depend on it. Keep routine implementation choices out of the questions unless they change cost, compatibility, permissions, or the intended result. A missing implementation plan does not block readiness.

If the issue contains several independently useful changes, propose a smaller first issue. Explain what it proves and what remains. Do not silently replace the original goal with the smaller task.

When delegated, return the draft, confirmed decisions, relevant evidence, and decision questions to the parent. The parent can settle them with [interview-issue](../interview-issue/SKILL.md). When answers arrive, revise and review the draft. Do not reopen resolved questions unless new evidence contradicts an answer.

## Draft the issue

Issue text follows the project [Writing rules](../../docs/writing.md): familiar words, active voice, instruction sentences within 20 words and description sentences within 25. Define unfamiliar terms at first use. Keep identifiers and commands exact.

Keep the draft proportional to the task. Include these facts in whatever structure fits:

- The problem and intended result.
- Included changes and explicit limits.
- Success conditions and how to assess them.
- Dependencies, confirmed decisions, and unresolved questions.
- Relevant source links and code references.

A success condition describes observable behavior, not merely a file that exists or a command that succeeds. Explain what each proposed test establishes, and separate evidence of new behavior from tests that protect existing behavior. Not every condition needs an existing automated test. Name the tests that implementation must add. Where human judgment is necessary, say what the person must assess.

Keep the original issue text separate from proposed edits, and do not erase the original intent when proposing a split. Put essential decisions in the draft, not only in a conversation or report.

## Review and revise the draft

Before returning the draft, review it as the next implementer would, and make the corrections yourself:

- Does the opening state the problem and intended result?
- Can the reader understand the scope without this conversation?
- Do success conditions demonstrate the intended result rather than a convenient substitute?
- Are source facts, proposed tests, and unresolved decisions clearly separate?
- Does the draft keep confirmed decisions and exclude unrelated changes?
- Can shorter sentences or ordinary words make it easier to use?

Edits must preserve meaning, permission, scope, and uncertainty. Do not turn a proposal into a requirement. Leave routine implementation choices open when the success conditions are sufficient. Read the result again for contradictions and lost requirements.

If a correction needs a new user decision, return the question with a recommendation. Otherwise continue without an extra approval step.

## Return the result

State whether the draft is ready for implementation, needs a decision, or lacks evidence, and why. Return the revised draft (not a list of suggested edits), unresolved questions, and a short evidence summary. Mention material corrections, and which checks you ran and which you only inspected. If you propose a child issue, explain its relationship to the original.

If filing is requested or included in the agreed flow, hand the draft to [file-issue](../file-issue/SKILL.md). Include the repository and any supplied parent, project, labels, and field values. Leave unspecified metadata unspecified.
