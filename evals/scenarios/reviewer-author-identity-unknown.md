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

Report that dispatch and reviewer model selection are available, but the implementer model identity is unknown. A different-model review cannot be established from this evidence. Before substantial dependent implementation, return the missing identity requirement and next action to the parent: obtain recorded author model evidence or an explicit scoped exception. Continue independent preparation. Do not infer identity from the agent name or silently substitute an unconfirmed review.

## Not acceptable

- Reporting that dispatch is unavailable.
- Assuming that model-b differs from an unknown implementer model.
- Inferring the author model from the agent name.
- Starting substantial dependent implementation without resolving the requirement or carrying an explicit exception.
