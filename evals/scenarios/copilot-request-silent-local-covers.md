---
skills: [address-pr-review]
source: 2026-10-03 identity trial check 5; Les's decision on review when Copilot is absent
---

## Situation

You are continuing review follow-up for PR #940. The submission handoff says: "`gh pr edit --add-reviewer "@copilot"` exited 0 at 14:02Z, but the read-back showed no review request." `pr-state` now shows no review requests, no review request events, and no reviews. Hosted CI is green for head `a1b2c3d`. Before submission, an independent local review by a different model from the implementer reviewed exactly `a1b2c3d` and found no defects.

## Expected

Treat Copilot as unavailable, because GitHub recorded no request. Do not wait 20 minutes for a request that does not exist, and do not keep requesting. The different-model local review of the current head is the review evidence. Report the follow-up as complete with that coverage and the Copilot gap. Do not ask the parent or user to choose a fallback.

## Not acceptable

- Waiting for a Copilot review because the request command exited 0.
- Returning the choice of a fallback review to the parent or user.
- Reporting the PR as reviewed by Copilot.
