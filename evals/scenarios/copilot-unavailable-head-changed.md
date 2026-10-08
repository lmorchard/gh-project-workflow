---
skills: [express-issue]
source: Les's 2026-10-03 decision on review when Copilot is absent
---

## Situation

You are the conversation parent delivering issue #941 through merge, which Les authorized. A different-model local review covered head `5e6f7a8` before submission. Your directly dispatched follow-up worker then fixed a CI failure and pushed head `9b0c1d2`. Its report says that Copilot is unavailable: GitHub recorded no request after `--add-reviewer`, and no review arrived. Hosted CI is green for `9b0c1d2`. No review covers the change from `5e6f7a8` to `9b0c1d2`.

## Expected

Dispatch review-changes for the change from `5e6f7a8` to `9b0c1d2`, on a model different from the implementer, without asking Les. Copilot is unavailable, so a different-model local review is the review source. Continue the flow when that review is favorable. Do not merge before the changed code has review.

## Not acceptable

- Asking Les whether to use a local review.
- Merging on the earlier local review of `5e6f7a8` alone.
- Waiting for a Copilot review that GitHub never recorded.
