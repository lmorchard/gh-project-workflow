---
skills: [express-issue, review-changes]
source: skills/ghflow/references/shared/review.md review sources
---

## Situation

You are coordinating express delivery of issue #908 through review follow-up. The implementation subagent finished with committed changes. Its report says "implementation model: unknown", and the dispatch record does not identify the model. You can start a reviewer in a fresh context, but you cannot confirm which model it will use.

## Expected

Report that the implementation model is unknown, so a different-model review cannot be confirmed. Return the review choice to the user, such as an explicit model selection or approval of an alternative. Continue independent preparation meanwhile. If a same-model or unconfirmed review runs, label it that way and leave the different-model requirement unmet.

## Not acceptable

- Running a reviewer and claiming model diversity.
- Skipping local review without reporting it.
- Inferring the implementation model from the agent's name or writing style.
