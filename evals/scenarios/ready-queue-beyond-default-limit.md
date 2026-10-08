---
skills: [burndown-ready-queue]
source: issue #27; references/tasks/burndown-ready-queue.md#audit-the-ready-queue
---

## Situation

The selected project has 35 items. A read with the default `gh project item-list` limit returns 30 items, and none has Status `Ready`.
The remaining five items include issue `https://github.com/acme/widgets/issues/314`, with repository identity `acme/widgets`, Status `Ready`, and Priority `P1`.
The paginated GraphQL read returns all 35 items and its final page has `hasNextPage: false`.
The user has already selected delivery through review follow-up.

## Expected

Use the complete paginated inventory. Include issue #314 in the Ready queue because it is outside the default 30-item result.
Preserve its Priority ordering and the selected review-follow-up endpoint. Do not report that the queue is clear.

## Not acceptable

- Reporting an empty Ready queue from the 30-item result.
- Treating a larger fixed item-list limit as proof of complete coverage.
- Asking again for the already selected delivery endpoint.
