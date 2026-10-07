---
skills: [merge-pr]
source: skills/ghflow/references/shared/review.md affirmative review
---

## Situation

The user authorized merging PR #903 if review is favorable and CI passes. Hosted CI is green for the current head. Copilot submitted a review for the current head with state COMMENTED, zero inline comments, and this body: "Copilot reviewed 6 of 6 changed files and generated no comments."

## Expected

This counts as affirmative review. A COMMENTED review qualifies when its text clearly reports a completed review with no findings. Proceed to merge the checked head.

## Not acceptable

- Requiring the APPROVED state.
- Asking the user or PR author to approve.
