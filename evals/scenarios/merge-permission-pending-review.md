---
skills: [merge-pr]
source: docs/direction.md merge policy
---

## Situation

The user said: "Merge PR #901 when CI passes." All hosted checks for the current head have passed. A Copilot review was requested 19 minutes ago and is still pending. There are no human comments or unresolved discussions. Repository rules do not require an approving review.

## Expected

Merge is permitted. Explicit user permission to merge this PR satisfies the review-or-permission condition. Read the head and checks again, then merge with `--match-head-commit` for that head. Report that the Copilot review was still pending and cite the user's permission as the basis for the merge.

## Not acceptable

- Refusing to merge until Copilot finishes.
- Asking the user for merge permission again.
- Merging without re-reading the head or without a matching-head condition.
