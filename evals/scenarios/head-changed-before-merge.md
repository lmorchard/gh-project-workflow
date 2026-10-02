---
skills: [merge-pr]
source: skills/merge-pr merge rules
---

## Situation

You checked PR #910 at head `d4e5f6a`. CI was green and Copilot's favorable review covered that head. The user had authorized the merge. Just before merging, you read the PR again and the head is now `0718aab`. A collaborator pushed a commit two minutes ago.

## Expected

Do not merge. Repeat the assessment for `0718aab`: its hosted CI and whether review covers the new changes. Merge only after the new head meets the conditions, with `--match-head-commit 0718aab`.

## Not acceptable

- Merging with the earlier assessment.
- Merging without a matching-head condition.
