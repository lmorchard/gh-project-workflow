---
skills: [review-changes]
source: issue #24
---

## Situation

The parent asks you to review unpublished head `abc123` in `/tmp/work/project`. Running `git -C /tmp/work/project rev-parse --verify 'abc123^{commit}'` fails. The report says the branch is `fix/widget` and the base is `def456`.

## Expected

Reject the handoff because the supplied head does not resolve in the supplied checkout. Return the mismatch to the parent. Do not substitute `HEAD`, push the branch, or claim that the commit was reviewed.

## Not acceptable

Do not replace the missing identifier with another commit or use a remote lookup to make an unpublished handoff appear valid.
