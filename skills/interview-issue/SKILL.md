---
name: interview-issue
description: Conduct an interactive interview to clarify a request or improve an issue draft when scope, intended behavior, or success conditions need user judgment. Use in the parent conversation, including after define-issue or reconsider-issue returns questions.
---

# Interview about an issue

Help the user settle decisions that prevent a useful issue draft. Conduct the interview in the conversation with the user. A delegated research or review agent returns findings to that conversation instead.

If this skill is invoked in a subagent, return proposed questions to the parent. Do not attempt an interview without the user. Do not infer answers from silence.

## Establish the starting point

Read the request or current draft and available review findings. Identify the intended result, confirmed decisions, unresolved choices, and evidence limits. Use existing answers instead of restarting the interview.

The input can be a rough idea or an issue draft. If no draft exists, start with the problem and desired result. Do not require a completed review before helping the user.

When revisiting earlier work, carry forward its confirmed decisions, completed results, and lessons from failed attempts. Separate observed failures from assumptions about their cause. Do not restart from a blank page or repeat questions that the evidence already settles.

Separate missing facts from decisions. Investigate a fact when available sources can answer it. Ask the user about intent, priorities, constraints, and tradeoffs that the sources cannot settle.

## Conduct the interview

Make conversation the default review path. Summarize the proposed result and relevant changes before asking for a decision. Do not require the user to open a draft file or edit its wording. Maintain the draft yourself as answers arrive, and make the full text available when useful or requested.

Order questions by their dependencies. Settle the intended result before scope boundaries, then discuss how to recognize success. Skip decisions that are already settled.

Start with the decision that most changes the scope or intended result. Explain why it matters in ordinary words. Ask one focused question, with a recommended answer and its tradeoff when the evidence supports one.

Offer alternatives when they represent real choices. Do not force a choice between artificial options or hide uncertainty behind a recommendation. Let the user propose another approach.

If the idea is unclear, discuss a concrete example before selecting an implementation. Ask what the user expects to happen in that example. Explore alternatives only as far as necessary to define the result and limits.

If an answer stays vague, propose a concrete example of success and ask whether it captures the intent. Explain how someone can observe that result. Do not make the user design a test or approve every test command.

Do not require the user to choose routine implementation details. A choice matters here when it changes scope, behavior, compatibility, cost, or permissions. Keep other choices open for implementation.

After each answer, update the affected parts of the draft. Preserve requirements that the answer does not change. Ask the next question only if a material uncertainty remains.

If an answer conflicts with an earlier decision, explain the conflict. Ask which result the user intends. Do not silently discard either decision.

## Finish the draft

Stop the interview when the remaining choices no longer prevent issue definition. Do not require a fixed question count or another approval of settled decisions. If the user defers a decision, leave it explicit and state its effect on readiness.

Return an updated draft with the confirmed decisions and remaining questions. State what changed and why. Include essential answers in the draft so another agent does not need this conversation. For consequential decisions, include the reason and why a plausible alternative was rejected. Keep this explanation proportional to the decision. Do not require a separate decision log.

Review the draft before returning it. Make sure that scope, success conditions, and confirmed decisions agree. Distinguish existing evidence from proposed tests and correct unclear wording yourself.

Use active voice and familiar words. Define unfamiliar technical terms at first use. Keep instruction sentences within 20 words and description sentences within 25 words.

When using `define-issue`, pass the updated draft and decisions back for its review. Do not restart research unless an answer invalidates existing evidence. Either skill can be used without installing the other.

An interview does not expand authorization. If the agreed flow includes publication, continue after the necessary decisions are settled. Do not ask for publication permission again merely because the interview ended. User-reviewed scope changes carry forward within the authorized flow. Revisit authorization only for a significant change outside the reviewed or authorized scope. Preserve draft-only limits. Agreement with a product decision alone does not authorize unrelated actions or implementation.
