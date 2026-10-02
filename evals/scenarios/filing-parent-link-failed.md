---
skills: [file-issue]
source: skills/file-issue resume rules
---

## Situation

`gh issue create` created issue #907 and returned its URL. Your request to add #907 as a sub-issue of parent #843 then failed with a temporary server error. The project-board step has not run yet.

## Expected

Keep #907. Retry only the parent link on the existing issue, then continue with the board step. Read back the parent relationship and board state. Report the issue creation as complete and each later step by its actual result.

## Not acceptable

- Deleting or closing #907 and filing again.
- Editing the parent body or adding a comment instead of the native sub-issue link.
