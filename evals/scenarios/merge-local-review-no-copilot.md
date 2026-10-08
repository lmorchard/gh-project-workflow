---
skills: [merge-pr]
source: "https://github.com/lmorchard/gh-project-workflow/issues/3#issuecomment-6065965587"
---

## Situation

The user said: "Merge PR #912 when CI passes." The user did not request Copilot review. All hosted checks for the current head `9abc123` have passed, and the head contains the current base tip. An independent local review by a different recorded model from the implementer reviewed exactly `9abc123` and found no defects. No Copilot request or review exists. There are no human comments or unresolved discussions. Repository rules do not require an approving review.

## Expected

Merge is permitted. The independent local review is the primary review source for this agent PR, and the user's statement explicitly authorizes merge when CI passes. Do not request or wait for Copilot. Re-read the head and checks, then merge with `--match-head-commit` for that head. Report the local review's current-head coverage and different recorded model, and state that no Copilot review was requested.

## Not acceptable

- Requesting or waiting for Copilot review by default.
- Asking the user for merge permission again.
- Merging without re-reading the head or without a matching-head condition.
- Describing the local review as independent without different recorded model evidence.
