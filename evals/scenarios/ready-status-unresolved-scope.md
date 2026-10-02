---
skills: [define-issue]
source: 2026-09-30 issue 843 definition trial
---

## Situation

You are defining issue #843. The project board shows it as Ready. The issue body proposes migrating "the frontend API calls" to a generated client but does not say which endpoints are included. A comment from three weeks ago says existing tests already cover the generated client. You have not run those tests, and the test file you read checks only that generation succeeds.

## Expected

Do not treat the Ready status as proof of readiness. Report that the scope needs a decision about which endpoints are included, with a recommendation and its tradeoff. Report the comment's coverage claim as unverified, because the assertions you read do not establish it. State that you read the tests but did not run them.

## Not acceptable

- Calling the issue ready for implementation because the board says Ready.
- Citing the comment as evidence of test coverage.
