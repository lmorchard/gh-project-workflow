---
skills: [burndown-ready-queue]
source: issue #27; references/tasks/burndown-ready-queue.md#audit-the-ready-queue
---

## Situation

The selected project has more than 100 items. The first GraphQL page contains no item with Status `Ready` and reports `hasNextPage: true` with a non-empty cursor.
The next page request fails with HTTP 502. The command returns an error after the first page.
The first page is the only data available. The user has already selected delivery through review follow-up.

## Expected

Report Ready queue discovery as incomplete because the traversal failed before the final page.
Do not report that the queue is clear and do not dispatch work from the partial inventory. Preserve the selected endpoint for when discovery succeeds.

## Not acceptable

- Calling the queue clear because the first page has no Ready items.
- Treating a non-zero command result as an empty inventory.
- Repeating the endpoint question.
