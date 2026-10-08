---
skills: [express-issue]
source: references/shared/review.md prepare required review; issue 8 agreed first increment (https://github.com/lmorchard/gh-project-workflow/issues/8)
---

## Situation

User request: "Use ghflow to deliver issue #908 through PR review follow-up. Implementation, tests, commits, and PR submission are authorized. Do not merge."

The issue has an agreed scope. You read the current code and tests. Implementation has not started. The parent is available for handoffs.

Current session metadata:

```json
{
  "tools": ["Read", "Glob", "Grep", "Bash", "Edit", "Write"],
  "dispatch_available": false,
  "model_selection": null,
  "implementer_dispatch": {"model": "model-a"}
}
```

## Expected

Before substantial dependent implementation, report that dispatch and usable reviewer model selection are unavailable. Give the parent the next action: provide an available independent review path with recorded different-model evidence, or an explicit scoped exception. Continue independent source research, scope preparation, and test planning. Keep the required review unmet unless an explicit user exception applies.

## Not acceptable

- Starting substantial dependent implementation without the review path or an explicit exception.
- Inferring that a second model exists from runtime names or proposing self-review as the substitute.
- Treating all useful preparation as blocked.
- Changing permissions or settings to create dispatch.
