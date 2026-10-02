---
skills: [address-pr-review]
source: 2026-10-02 retrospective, CI cost
---

## Situation

Copilot's review of PR #896 has three findings. You assessed all three as real defects within the agreed result: a missing null check in `inbox.js`, a wrong error message in `inbox_api.py`, and a missing test case in `test_inbox.py`. Each fix is small and independent. Hosted CI for this repository takes about twenty minutes per push, and each push triggers another automatic review.

## Expected

Make all three corrections, run the affected local checks, and push them together. Then watch CI and review for the one new head. Do not push each correction separately.

## Not acceptable

- Pushing after each correction.
