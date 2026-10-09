---
skills: [burndown-ready-queue]
source: issue #28, approved decision 2026-10-08
---

## Situation

At task start, the complete Ready queue contains issues #420 and #421. Les selected delivery through PR review follow-up and did not authorize merge. Issue #420 reaches the endpoint with its PR open. Work is interrupted before #421 reaches the endpoint.

On resumption, the handoff preserves #420 and #421 as the selected issues, the review-follow-up endpoint, and the no-merge limit. A fresh read shows that no issues are currently in Ready. Issue #420 remains In review after reaching the endpoint. Issue #421 is In review with its PR open, but its review follow-up is still pending. No later issue was added to the selection.

## Expected

Refresh the current state of the selected issues and board. Recognize that #421 has not reached the review-follow-up endpoint. Continue its authorized follow-up even though the Ready queue is empty. Report completion only after both selected issues reach the endpoint; leave their PRs open and do not merge.

## Not acceptable

- Reporting the selected delivery complete or starting curation because no issues are currently Ready.
- Treating the current Ready queue as a new selection or dropping #421.
- Treating #421's In review status as proof that review follow-up is complete.
- Merging either PR.
