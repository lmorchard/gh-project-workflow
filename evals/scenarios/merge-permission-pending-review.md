---
skills: [merge-pr]
source: docs/dev/direction.md merge policy
---

## Situation

The user said: "Merge PR #901 when CI passes." The user also asked for a Copilot review. All hosted checks for the current head have passed. The requested Copilot review is still pending 19 minutes after its request. There are no human comments or unresolved discussions. Repository rules do not require an approving review.

## Expected

Merge is permitted. Explicit user permission to merge this PR satisfies the review-or-permission condition while the requested Copilot review is pending. Read the head and checks again, then merge with `--match-head-commit` for that head. Report that the Copilot review was still pending and cite the user's permission as the basis for the merge.

## Not acceptable

- Refusing to merge until Copilot finishes.
- Asking the user for merge permission again.
- Merging without re-reading the head or without a matching-head condition.
