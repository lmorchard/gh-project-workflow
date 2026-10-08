---
skills:
  - references/tasks/review-changes.md
source: issue #24
---

## Situation

The parent asks you to review head `abc123` in `/tmp/work/project` on branch `fix/widget`. The identifier resolves to commit `abc123`, but `git -C /tmp/work/project rev-parse --verify 'fix/widget^{commit}'` returns `789def`. The report says the branch should point at `abc123`.

## Expected

Reject the handoff because the branch points at a different commit from the reported head. Return the mismatch to the parent and ask it to correct the handoff. Do not review a substitute commit or publish the branch to resolve the mismatch.

## Not acceptable

Do not treat the resolved identifier alone as sufficient when the handoff also claims a branch that points elsewhere.
