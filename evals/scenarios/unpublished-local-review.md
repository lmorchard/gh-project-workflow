---
skills:
  - references/tasks/implement-issue.md
  - references/tasks/review-changes.md
  - references/tasks/submit-pr.md
source: issue #24
---

## Situation

An implementation agent has committed the requested changes in `/tmp/work/project` on branch `fix/widget`. The commit has not been pushed. The report gives the full tested head and base commit identifiers. A different-model local reviewer must inspect the changes before anyone publishes them. The submitter will later publish the same branch.

## Expected

The parent supplies the checkout path, branch, base, tested head, and unpublished state to the reviewer. The reviewer resolves the supplied head and base with `git -C CHECKOUT rev-parse --verify 'REV^{commit}'`, checks that the branch points to the expected head, and reviews the local diff. The result establishes local existence only. On submission, the agent verifies the published commit and PR head remotely with `verify-commit`.

## Not acceptable

Do not require a push to satisfy evidence rules. Do not use `verify-commit` as proof of an unpublished commit. Do not treat local existence as evidence of publication.
