---
skills: [submit-pr]
source: 01ecfc3
---

## Situation

You just created PR #900 and moved its issue to In review. `gh pr view 900 --json reviewRequests` returns an empty list. The PR timeline shows a `review_requested` event for Copilot, created by repository automation 40 seconds after the PR opened, for the current head commit. No review has been submitted.

## Expected

Treat the automatic request as the current-head Copilot request. Do not request another review. Record the automatic request's timestamp and the head commit, and hand them to address-pr-review as the start of the 20-minute wait.

## Not acceptable

- Requesting Copilot again because the requested-reviewer list is empty.
- Using the time of your own report as the request time.
