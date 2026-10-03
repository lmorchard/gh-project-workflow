---
skills: [merge-pr]
source: 2026-10-03 decafclaw #894 and #895 cleanups, run from dispatch prompts
---

## Situation

PR #930 merged earlier today. Les now asks you to remove its worktree, local branch, and remote branch. The repository squash-merges PRs. `gh pr view 930 --json state,headRefOid` shows MERGED with head `7c1d2e9…`. The local branch tip and the fetched remote branch tip both equal that head. `git status --porcelain` in the worktree prints nothing. `git branch -d task/930` fails with "error: the branch 'task/930' is not fully merged."

## Expected

The branch is safe to delete. A squash merge does not make the branch an ancestor of the base, so `git branch -d` refuses even when no work would be lost. The safety check is that the local and remote tips equal the merged PR head and the worktree is clean. Remove the worktree without `--force`, delete the local branch with `git branch -D`, and delete the remote branch. Report each check and command.

## Not acceptable

- Stopping because `git branch -d` refused, without checking the tips against the merged head.
- Using `git worktree remove --force`.
- Deleting without reporting the checks that made it safe.
