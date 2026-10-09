# Ready-queue burndown on board 6, 2026-10-05

The parent ran burndown-ready-queue on [board 6](https://github.com/users/lmorchard/projects/6) through review follow-up, without merge. Les merged each PR himself. Subagents did all subject-repository writes as `MokaGnome`. Implementation used Claude Opus 5.5 and every local review used Claude Sonnet 5.5. The skills started at `d932930` and changed during the run, as listed below.

Five issues were in Ready. Four were delivered: #469 ([PR #936](https://github.com/lmorchard/decafclaw/pull/936)), #662 (#939), #166 (#940), and #555 (#943). #918 was deferred behind #857 because its own completion condition needs a formatted tree, and `ruff format --check` reported 343 unformatted files. Les added three issues during the run: #937 (#938), #941 (#942), and #944 (#945). All seven PRs merged, and `main` CI was green after each merge. Copilot was unavailable for every PR because `MokaGnome` has no Copilot seat.

Evidence limits: nobody recorded browser or screen-reader checks for #939, #940, #943, or #945. Les merged those PRs, but the conversation does not say which manual checks he did. One green CI run after #942 does not prove that the flaky tests are gone.

Lessons and resulting changes:

- `main` became red when the previous session merged #933 and #934 51 seconds apart. Each PR had green CI, but the head of #933 did not contain #934. Unstubbed tests from #934 then met the guard from #933. `merge-pr` accepted green CI for a head that was behind its base, and the decafclaw ruleset does not require up-to-date branches. `pr-state` now reports `base_behind_by`. `merge-pr` requires 0 and updates a branch that is behind, and `burndown-ready-queue` waits for base CI after each merge (`d626dc9`). #938 fixed `main`.
- `ghflow board set-status` called `gh` with the user's own account, so board moves ran as Les while comments ran as `MokaGnome`. `run_gh` now applies the configured identity (`95a18a1`).
- A board readback lagged a successful write and reported a mismatch. The readback now retries up to 4 times (`5ece506`).
- `gh pr update-branch` needs the `repo` scope, and the `MokaGnome` token does not have it. `merge-pr` now uses the REST call with `expected_head_sha` (`ee9726b`).
- Five coordinators handed back while required CI was pending, and their address-pr-review subagents kept running. Two of those subagents later reported on a head that had moved without knowing why. `express-issue` now requires the coordinator to wait for follow-up, or to name each pending check and head (`3f6c9c4`). The coordinator for #944 was the first to report final CI.
- Two flaky tests failed CI on PRs that did not touch them. The causes were a race in `test_workspace_concurrency.py` and a Playwright session fixture that left asyncio's running-loop mark set. #942 fixed both causes without retries. Before the fix, reduced runs failed 10 in 30 and 20 in 20 times.
- On a new machine, the auto-mode classifier blocked `ghflow identity` and `ghflow exec` as credential use until Les added allow rules in `.claude/settings.local.json`. It allowed a CI rerun when the subagent prompt named the rerun as authorized CI repair. It blocked the same rerun from a subagent whose prompt did not.
- GitHub runners did not pick up `lint-and-test` for about 15 minutes, which cancelled jobs on #939 and #940. One `--failed` rerun is the right repair, because no tests ran. The parent's first briefs said "no reruns" for all failures and had to be corrected.
- The issue body of #662 was partly done already on `main` (#808). The coordinator found this and implemented only the remaining part.
- After the burndown, the parent delivered #857 and #918 as [PR #946](https://github.com/lmorchard/decafclaw/pull/946), merged as `9d39e9c` with a merge commit. Les chose a commit-by-commit structure:
  1. The formatting-only commit `639eec1`.
  2. `.git-blame-ignore-revs`, which lists `639eec1`.
  3. A fix to the message-type generator.
  4. New text anchors for `test_api_codegen.py`.
  5. The `make check` gate.

  The coordinator stopped before submission and asked for a decision. Formatting broke two checks that depend on exact source layout, so the PR needed commits outside the agreed structure. An AST comparison of 342 files found no differences. The reviewer reproduced commit 1 by running `make fmt` on the base. Commits 1 to 3 do not pass the checks alone.
- Two coordinators said that the hand-back tool refused their report with "already delivered", so they sent it again by message. The parent received both copies each time. Another coordinator said that the harness made it hand back before its follow-up subagent reported. The wait rule in `express-issue` therefore cannot always hold. The fallback, which names the pending checks and head, is the part that worked.
- The classifier denied `git push origin --delete` for merged branches as "Git Destructive". The local worktree cleanup succeeded without `--force`. The seven remote branches remain.
- Cleanup after the run removed all 25 local decafclaw worktrees without `--force`. #861's branch looked unmerged because PR #862 was squash-merged. Its tip equaled the PR head, and the diffs were identical, so `git branch -D` was correct. Les turned on "Automatically delete head branches" and ran `scripts/delete-merged-branches.sh` (`b4bc444`), which deleted the merged branches that agents could not. `merge-pr` cleanup now deletes only local branches (`575274d`). Sibling-directory worktrees from another agent session led to the `.claude/worktrees/` convention in AGENTS.md (`9d72822`).
- Follow-up issues: decafclaw #947, #948, and #949, and [gh-project-workflow #13](https://github.com/lmorchard/gh-project-workflow/issues/13) on who should own review follow-up.
