---
name: interview-issue
description: Conduct an interactive interview to clarify a request or improve an issue draft when scope, intended behavior, or success conditions need user judgment. Use in the parent conversation, including after define-issue or reconsider-issue returns questions.
---

# Interview about an issue

Help the user settle the decisions that block a useful issue draft. The interview happens in the parent conversation. A subagent that loads this skill returns proposed questions to the parent instead.

Apply [Authorization](../shared/authorization.md) throughout, including its rules for questions.

## Establish the starting point

Read the request or current draft and any review findings. Identify the intended result, confirmed decisions, unresolved choices, and evidence limits. The input can be a rough idea; if there is no draft, start with the problem and the desired result.

When revisiting earlier work, carry forward its confirmed decisions, completed results, and lessons from failed attempts. Separate observed failures from assumptions about their cause. Do not restart from a blank page or ask what the evidence already settles.

## Conduct the interview

Conversation is the review path. Summarize the proposed result and relevant changes before asking for a decision. Maintain the draft yourself as answers arrive. Do not ask the user to open a file or edit wording; share the full text when it helps or the user asks.

Order questions by their dependencies: the intended result, then scope boundaries, then how to recognize success. Start with the decision that most changes the scope or result, and explain in ordinary words why it matters.

Offer alternatives only when they are real choices. Do not hide uncertainty behind a recommendation. Let the user propose another approach.

If the idea is unclear, discuss a concrete example before an implementation, and ask what the user expects to happen. If an answer stays vague, propose a concrete example of success and how someone could observe it. Do not make the user design a test or approve test commands.

Leave routine implementation details for implementation. A choice belongs in the interview when it changes scope, behavior, compatibility, cost, or permissions.

After each answer, update the affected parts of the draft and keep the requirements that the answer does not change. Ask the next question only if a material uncertainty remains. If an answer conflicts with an earlier decision, explain the conflict and ask which result the user intends.

## Finish the draft

Stop when the remaining choices no longer block issue definition. There is no fixed question count. If the user defers a decision, leave it explicit and state how it affects readiness.

Return the updated draft, the confirmed decisions, and any remaining questions, with what changed and why. Put essential answers in the draft so another agent does not need this conversation. For consequential decisions, include the reason and why a plausible alternative was rejected, in proportion to the decision. A separate decision log is not needed.

Review the draft before returning it. Make sure scope, success conditions, and decisions agree, and that existing evidence stays separate from proposed tests. Issue text follows the project [Writing rules](../../docs/writing.md).

To continue with [define-issue](../define-issue/SKILL.md), pass back the updated draft and decisions. Research restarts only if an answer invalidates existing evidence. If the agreed flow includes publication, continue to it once the decisions are settled.
