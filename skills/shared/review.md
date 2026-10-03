# Review

These rules apply to every skill that requests, performs, waits for, or relies on a code review.

## Review sources

This workflow uses three review sources:

- **Copilot**, requested on the PR. It is the preferred source. Its underlying model is unknown unless something identifies it.
- **Independent local review**, done with [review-changes](../review-changes/SKILL.md) in a fresh context.
- **Human review**, from the user or another person.

The local review must use a different model from the implementer. Record each model identity from runtime or dispatch metadata. Do not infer it from an agent's name, writing style, or claims. A different agent name, a fresh context, or a changed reasoning setting does not make a different model.

If either identity is unknown or a different model is unavailable, report that and return the review choice to the parent. A same-model second opinion can still help. Label it as same-model, and leave the different-model requirement unmet. A user-approved alternative stays explicit in later handoffs.

No review source guarantees correct findings. Review does not replace tests or human judgment.

## Copilot request state

Request a review with `gh pr edit PR_URL --add-reviewer "@copilot"` when the installed help supports it. Request a reviewer, not a coding-agent assignment or a comment that asks Copilot to change code.

Before you request, inspect current review requests, completed reviews, and review-request timeline events. Repository automation can request Copilot as soon as the PR opens. An empty requested-reviewer list does not prove that no request exists. If a request for the current head exists, keep its timestamp and do not request again.

Repository automation varies: a push may or may not trigger a new review. After a push, check for an automatic request first. Request a review only when the changes need one and no request exists.

Keep these states separate: requested, pending, completed, unavailable, and failed. A pending request or a temporary network error does not show that Copilot is unavailable.

A review is complete when the requested reviewer has submitted a review for the requested commit. Identify it by its author, commit, and submission time. It can have zero inline comments. CI completion, unrelated comments, and disappearance from the reviewer list do not show that Copilot finished.

## Affirmative review

**Affirmative review** is a favorable review that covers the changes being merged. It can come from a person, Copilot, or an independent local review.

A COMMENTED review qualifies when its text recommends approval or clearly reports a completed review with no findings. These do not qualify: silence, an empty comment list, a timeout, or the COMMENTED state alone. A review whose text asks for human review, such as Copilot's "Needs a closer look", does not qualify even with no findings. It returns the merge decision to the user. Another review source, including a different-model local review, does not answer that request. This workflow does not require the GitHub APPROVED state. Authors cannot approve their own PRs, and the agent often submits PRs as the user.

A favorable review does not by itself authorize merge. [merge-pr](../merge-pr/SKILL.md) states when it counts.

If a review covers an earlier commit, assess what changed since then and state the coverage limit. Do not describe it as a review of the current head.

## Human feedback

A human COMMENTED review that requests changes is actionable, including a review from the PR author. The review state does not decide whether a finding needs a response. A comment that requests no change does not need a code edit.

Do not resolve a disputed discussion to make a PR look ready. Return disputes and human objections to the parent or user.
