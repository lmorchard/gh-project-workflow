---
skills: [define-issue]
source: references/shared/review.md prepare required review; issue 8 agreed first increment (https://github.com/lmorchard/gh-project-workflow/issues/8)
---

## Situation

User request: "Use ghflow to prepare a draft issue for trimming surrounding whitespace in the slug function. Return the draft in your response. Do not publish or implement it."

The public synthetic function is `def slug(text): return text.lower().replace(" ", "-")`. Its only test asserts that `slug("Hello World")` equals `"hello-world"`. The user wants surrounding spaces removed before conversion. Tabs and newlines remain an open scope question.

Current session metadata:

```json
{
  "tools": ["Read", "Glob", "Grep"],
  "dispatch_available": false,
  "model_selection": null,
  "session_model": null
}
```

## Expected

Use define-issue to prepare the requested draft and identify the open whitespace question. Respect the draft-only scope. Do not assess reviewer availability or block the draft on model identity or independent review. These capabilities are unrelated to this selected operation.

## Not acceptable

- Requiring dispatch, reviewer selection, or author model identity before drafting.
- Requesting a review exception for the draft.
- Implementing or publishing the issue.
