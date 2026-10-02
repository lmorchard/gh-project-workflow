---
skills: [merge-pr]
source: 6e4c038
---

## Situation

You are asked to finish merging PR #917. It is already merged; GitHub shows the merge commit. Its linked issue #918 is closed but still shows In review on the project board. The project board has a Done status option.

## Expected

Skip the merge action. Confirm the merge commit and issue state, then move #918 to Done on the board and read the status back. Report any missing historical CI or review evidence without treating it as a blocker for the board correction.

## Not acceptable

- Attempting to merge again.
- Leaving the board unchanged because the merge happened earlier.
