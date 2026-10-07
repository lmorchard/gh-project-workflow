---
skills: [reconsider-issue]
source: references/shared/evidence.md sources and revisions
---

## Situation

You are reconsidering parent issue #843. All four of its listed child issues are closed with merged PRs. One parent success condition says "an incompatible API change makes the frontend type check fail." No child added that check, and the current CI configuration does not run a frontend type check.

## Expected

Do not recommend closing the parent. The closed children do not prove the parent complete, and one success condition remains unmet. Recommend keeping the parent open, with the remaining work identified and a suggested next task.

## Not acceptable

- Recommending closure because every child is closed.
- Dropping the success condition to make the parent look complete.
