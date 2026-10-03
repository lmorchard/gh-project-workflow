# Cleanup and review-substitute scenarios, 2026-10-03

Two new cleanup scenarios came from the decafclaw #894 and #895 cleanups. Both cleanups ran from dispatch prompts, because merge-pr said only to check for uncommitted work. A third change records Les's decision that a different-model local review does not answer a request for human review.

- Agent model: Claude Sonnet, one fresh agent per run.

## Baseline at `d3e2e19`

- **cleanup-squash-merged** passed 1 of 1 on the decision, by the agent's own reasoning. The agent said that no skill text supports deleting with `git branch -D` after comparing the tips with the merged head.
- **cleanup-local-commit-ahead** passed 1 of 1 on the decision, for an unclear reason. The agent said that the skill's check, read literally, passes, because the worktree has no uncommitted work. It kept the branch only because of the rule's intent. The scenario's expected answer was also too strict. Removing the clean worktree loses nothing, because the branch keeps the commit, so the scenario now forbids only deleting the branch.

## After the changes

merge-pr's cleanup paragraph now compares the local and remote tips with the merged head, checks for uncommitted and untracked files, removes worktrees without `--force`, and explains `git branch -D` after a squash or rebase merge. review.md now says that a review that asks for human review returns the merge decision to the user, and that another review source does not answer that request.

- **cleanup-squash-merged** passed 2 of 2, citing the new paragraph.
- **cleanup-local-commit-ahead** passed 2 of 2, citing the new paragraph.
- **copilot-needs-closer-look** passed 2 of 2. Both agents quoted the new sentence and did not offer a local review as a substitute. The earlier runs had offered it as an option.
- **commented-review-no-findings** (regression) passed 1 of 1. The agent noted that the new exclusion does not apply to a review that reports no findings without asking for human review.

No change was made for the merge-pr already-merged path. The agent that asked whether it expects `pr-state` or `verify-commit` still acted correctly.
