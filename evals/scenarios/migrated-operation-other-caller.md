---
skills: [decompose-parent-issue]
source: bf008f7
---

## Situation

You are decomposing parent issue #843, which moves the frontend to a generated API client. Child #861 migrated `GET /api/auth/me` in `AuthClient.checkSession()` and is merged. A search finds a second caller of the same endpoint in `widgets/sticky.js`, which still uses a handwritten `fetch` call.

## Expected

Do not count the endpoint as fully migrated. Record the sticky-widget caller in the coverage map as remaining work, assigned to a proposed child or an explicit exclusion. Credit #861 for the caller it migrated. State what your caller search covered.

## Not acceptable

- Marking the endpoint complete because #861 merged.
