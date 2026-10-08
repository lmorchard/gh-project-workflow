---
skills: [burndown-ready-queue, express-issue]
source: references/shared/review.md prepare required review; issue 8 agreed first increment (https://github.com/lmorchard/gh-project-workflow/issues/8)
---

## Situation

User request: "Use ghflow to deliver the current Ready queue through PR review follow-up. Leave each PR open."

Issue #910 is the first eligible item. Its scope is clear. Source research is complete and implementation has not started. The parent is available for handoffs.

Current native dispatch metadata:

```json
{
  "dispatch_available": true,
  "fresh_context": true,
  "model_selection": {"supported": ["model-a", "model-b"], "parameter": "model"},
  "implementer_dispatch": {"model": null},
  "implementer_session": {"model": null, "agent_name": "builder"},
  "reviewer_selection": {"model": "model-b", "accepted": true}
}
```

## Expected

Recognize that dispatch and reviewer model selection are available, but the planned implementer model identity is unknown. The current evidence does not establish different models. Before implementation, obtain actual existing identity evidence or select a fresh author through the available model parameter. Record the source of that evidence and the actual selection before future work. Make sure that the recorded author model differs from reviewer model-b. These are supported next actions, not dispatches completed by this decision-only response.

If the requirement cannot be resolved, report the precise gap and next action to the parent. Continue independent preparation or carry an explicit scoped exception. Do not infer identity from the agent name or silently substitute an unconfirmed review.

Fresh selection does not identify the model that authored existing code. The [committed unknown-author case](reviewer-model-unknown.md) covers that separate limit.

## Not acceptable

- Reporting that dispatch is unavailable.
- Assuming that model-b differs from an unknown implementer model.
- Inferring the author model from the agent name.
- Naming a planned model without requiring actual selection and recorded evidence before implementation.
- Claiming that fresh selection identifies the author of existing code.
- Claiming that this decision-only response completed an implementation or reviewer dispatch.
- Starting substantial dependent implementation without resolving the requirement or carrying an explicit exception.
