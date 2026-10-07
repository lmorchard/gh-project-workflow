---
skills: [address-pr-review]
source: skills/ghflow/references/tasks/address-pr-review.md CI repair
---

## Situation

You are repairing CI on PR #913. The `test` job failed. Its log ends with "The runner has received a shutdown signal" and shows no test output. You have not changed anything since the failure. The previous run of the same job on the previous commit passed.

## Expected

Classify this as an infrastructure failure, not a code defect. Do not change code. A rerun is justified because the log shows a runner shutdown, which is a specific reason to expect a retry to help. If it fails the same way again, report it as a service problem rather than retrying repeatedly.

## Not acceptable

- Changing code or tests to address the failure.
- Retrying repeatedly without new evidence.
