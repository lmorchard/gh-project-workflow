---
skills: [implement-issue]
source: c61b97b, 736c90d
---

## Situation

You are starting implementation in a new worktree of a Python project. The baseline command `make test` fails in tests that call a TypeScript type check: `tsc: command not found`. The project README says to run `make install-js` before the tests. You are considering running `make install-js` and `make test` in parallel to save time.

## Expected

Treat the failure as a missing prerequisite, not a product defect or a reason to skip the baseline. Run `make install-js` as the project directs, wait for it to finish, then run the baseline. Do not run the installation concurrently with tests that use those dependencies. Record any remaining baseline failures separately from failures your change introduces.

## Not acceptable

- Recording the `tsc` failure as an existing product failure and continuing.
- Running installation and tests in parallel.
