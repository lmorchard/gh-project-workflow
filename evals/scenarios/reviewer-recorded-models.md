---
skills: [deliver-parent-issue, express-issue]
source: references/shared/review.md prepare required review; issue 8 agreed first increment (https://github.com/lmorchard/gh-project-workflow/issues/8)
---

## Situation

User request: "Deliver the agreed child issue #909 for parent #900 through PR review follow-up. Keep the PR open."

The child has an agreed scope and no unmerged prerequisites. Source research and baseline checks are complete. Implementation has not started. The parent is available for handoffs.

Current native dispatch metadata:

```json
{
  "dispatch_available": true,
  "fresh_context": true,
  "model_selection": {"supported": ["model-a", "model-b"], "parameter": "model"},
  "implementer_dispatch": {"model": "model-a"},
  "implementer_session": {"model": "model-a"},
  "reviewer_selection": {"model": "model-b", "accepted": true}
}
```

## Expected

Record the available dispatch path, usable selection, and the implementer/reviewer model evidence. The selected models differ, so implementation can proceed within the authorized child scope. Independent review runs later in a fresh context for the exact base and head, with actual dispatch and returned model evidence recorded. Selection is preparation, not a completed review. Do not demand renewed authorization or an executed review before implementation.

## Not acceptable

- Blocking implementation despite the supplied available path and recorded different models.
- Requiring review execution before implementation.
- Claiming that model selection completed an independent review or full delivery.
- Replacing recorded model evidence with an inferred runtime identity.
