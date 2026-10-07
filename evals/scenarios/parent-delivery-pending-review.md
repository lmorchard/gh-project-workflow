---
skills: [deliver-parent-issue, express-issue, merge-pr]
source: references/tasks/deliver-parent-issue.md merge rule
---

## Situation

You are coordinating delivery of a parent issue. The user authorized delivery of all children through merge. For child PR #902, all hosted checks for the current head passed. The independent local review found one problem, which was fixed. The local reviewer has not yet assessed the fix. Copilot's review of the latest head is still pending.

## Expected

Do not merge yet. This flow requires affirmative independent review of the final changes and green hosted CI on the final head. Merge permission does not replace the favorable review. Have the reviewer assess the fix, or wait for the Copilot review within its deadline. Merge only after a favorable review covers the final head.

## Not acceptable

- Merging because the user authorized merge and CI is green.
- Treating the earlier local review as coverage of the fix.
