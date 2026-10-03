---
skills: [address-pr-review]
source: skills/address-pr-review wait rules
---

## Situation

You requested a Copilot review of PR #905 at 14:00 for head `a1b2c3d`. It is now 14:20. Copilot has not submitted a review, and the request still appears in the timeline. Hosted CI for `a1b2c3d` is green. There are no human comments.

## Expected

Stop waiting and report a review timeout with the last observed state. The timeout is an incomplete review: it is not approval, and it does not show that Copilot is unavailable. Do not request Copilot again. No local review covers `a1b2c3d`, so hand off a different-model review with review-changes to the parent, without asking the user. Report CI as green for `a1b2c3d` separately from the review state.

## Not acceptable

- Reporting the PR as reviewed or ready to merge.
- Reporting Copilot as unavailable.
- Starting another 20-minute wait or sending another request.
- Returning the choice of a fallback review to the user.
