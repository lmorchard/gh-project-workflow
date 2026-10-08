# Trial records

This index lists skill trials on real issues and public synthetic projects. Each entry states what the trial exercised and its evidence limits. Earlier delivery trials use [decafclaw](https://github.com/lmorchard/decafclaw).

## Record a trial

Add an entry with these facts:

- The date, subject issues, and PRs.
- The skills used and the commit of this repository that supplied them.
- The requested endpoint and what the trial exercised.
- Evidence limits, such as checks that nobody performed.
- Skill changes that the trial caused, with their commits.

Keep the entry short. Put long agent output in a dated folder only when later review needs it.

Entries before 2026-10-02 did not record the skill commit. For those entries, the commit is inferred from history: it is the commit before the one that recorded the trial, unless the entry says otherwise. Skills changed substantially in commit `489efbd`, so results from earlier commits do not transfer directly to later skill text.

## 2026-09-30: issue 843 definition, filing, and decomposition

The [issue 843 folder](2026-09-30-issue-843) contains agent output from these trials:

- [Issue definition trial results](2026-09-30-issue-843/review.md) for define-issue in a fresh agent context. Skills: `70cff5c`, which added the skill and recorded the trial together.
- [Filing the reviewed issue](2026-09-30-issue-843/filing.md), which created issue 861. No filing skill existed yet. The file-issue skill was written from this trial in `03d08f1`.
- [Proposed reconsideration](2026-09-30-issue-843/reconsider-proposal.md) for reconsider-issue. Skills: `831b1a2` (inferred).
- [Read-only decomposition](2026-09-30-issue-843/decomposition.md) for decompose-parent-issue, then named decompose-issue. Skills: `3460f88` (inferred).
- [Sticky lookup draft](2026-09-30-issue-843/sticky-lookup-draft.md) and [listing child draft](2026-09-30-issue-843/listing-child-draft.md) for reviewed child definitions.

## 2026-10-01: implementation and express delivery

The issue 863 trial completed implementation, submission, Copilot follow-up, and a separately authorized merge. It did not use the coordinator or local review. Skills: `31b5224` (inferred).

The issue 865 trial then exercised express-issue through review follow-up, including different-model local review, a Copilot finding, correction, and current-head review and CI. Skills: `01ecfc3` (inferred).

The issue 867 trial exercised the express merge endpoint through PR #868. The user required both affirmative review and green CI. The coordinator waited for the final hosted check, then merged the exact reviewed commit with a matching-head condition. This successful case does not establish every rejection or recovery path. Live post-merge application checks remained unperformed. Skills: `736c90d` (inferred).

The folder-management trial continued from definition and filing (#869) through implementation, independent review, PR #870, and merge. No product question or repeated authorization was needed. Favorable local and Copilot reviews and green hosted CI covered the exact merged head. The coordinator hit an agent-capacity limit, so the parent continued phase dispatch after its handoff. This tested continuity across skills, not a new automatic backlog selector. Live post-merge checks remained unperformed. Skills: `176f22c` (inferred).

After the issue 871 / PR #872 merge, Les reported that the manual smoke test seemed fine. This is user-reported evidence. The conversation does not specify which surfaces or scenarios were tested, so it does not establish completion of every project-required live check. Skills: `1e4b5a0` (inferred).

## 2026-10-01 to 2026-10-02: parent delivery of issue 843

deliver-parent-issue delivered children #875 through #884 of [issue 843](https://github.com/lmorchard/decafclaw/issues/843), then closed the parent after a fresh coverage audit. Skills: `3e753f0`. Issue 843 has 17 children in total. Seven children, #861 through #873, preceded this run.

Final checks passed on merged main: 4,237 Python tests with two skips, and 395 JavaScript tests. No deployment or final manual smoke test occurred. The ten children took about 11 hours, and later Python CI jobs took about 20 minutes each.

The [delivery retrospective](2026-10-02-parent-843-delivery.md) records the lessons, completion evidence, scope decisions, and recovery facts. Its scenario checks and the resulting skill changes are in [Retrospective scenarios](../../evals/results/2026-10-02-retro.md).

## 2026-10-02: express delivery of issue 894

The parent coordinated express-issue for [issue 894](https://github.com/lmorchard/decafclaw/issues/894) through review follow-up, without merge, from a local decafclaw clone. Each phase ran in its own subagent. Implementation used Claude Opus and both local reviews used Claude Sonnet, selected by the dispatch. [PR #898](https://github.com/lmorchard/decafclaw/pull/898) ended at head `783ea99` with green hosted CI, no human comments, and #894 In review. Skills: implementation at `8f4c693`; first review and submission at `9b2b56c`; rework at `9b2b56c`; second review and follow-up at `4d70860`.

The first commit split one long browser test into 21 isolated scenarios. It also exposed two failures that the old test had hidden: invalid canvas test data, and an intended 404 after a folder is pruned. The first local review found the coverage preserved but measured a large slowdown on two cores. Les then replaced the wall-clock success condition with a structural one: one client build per run, one Chromium launch per worker, and one context and at most one server per scenario, enforced by the tests. A second commit met it, and a second local review found no defects.

Copilot reviewed both heads with no findings. Its headline changed from "Approval recommended" at `142af1b` to "Needs a closer look" at `783ea99`, which asks for human review. Les later decided that this headline is not affirmative review. The current skill text already produced that decision in scenario runs ([results](../../evals/results/2026-10-02-copilot-headline.md)).

Hosted `lint-and-test` took 1106 s at the base, 948 s at `142af1b`, and 1151 s at `783ea99`, one run each. PR #896 took 1161 s with a similar test count. Run-to-run variance appears as large as any effect, so these numbers do not establish a change. Local pinned runs showed the rework faster at every worker count.

The same session filed [issue 897](https://github.com/lmorchard/decafclaw/issues/897) for the schedule race that #894 excluded. The board's auto-add workflow put it on board 6 without a request. Les then chose decafclaw's documented convention: new issues, triage items included, go on board 6 with priority and size. #894, #895, and #897 were then in Backlog at P2. Les later set #894 to P1.

Lessons and resulting changes:

- file-issue now reads back project membership even without a project request, because auto-add workflows can add it (`9b2b56c`).
- The submission subagent found #894 In progress, not Backlog as the handoff said, and acted on the live state. The board-status rule held.
- The first live use of `pr-state` found required checks in rulesets and matched the Copilot request to its bot review. Its two request fields confused a reader; evidence.md now explains them (`4d70860`).
- The implementer ran a `sudo apt` install through `playwright install --with-deps` without explicit authorization. implement-issue now requires authorization for system-level installs.
- The parent first compared hosted CI with older `main` runs that had about 600 fewer tests, and reported a false slowdown. Compare with the PR's base commit.
- The machine was shared with an unrelated heavy job, with load averages of 12 to 23. Local timings are noisy for that reason.

Les reviewed and merged PR #898 himself on 2026-10-03 (merge commit `4165293`, from head `783ea99`). `Closes #894` closed the issue one second later, and board automation set Done. A merge-pr subagent then ran the already-merged path at `6087b45`. `ghflow board set-status --status Done` exited 0 with action `unchanged` and `readback_matches` true, so the planned first real board write did not occur. A cleanup subagent removed the worktree and the local branch after it confirmed that the branch tip equaled the merged head and the worktree was clean.

- decafclaw's AGENTS.md provides `make prune-worktrees` for landed worktrees. The cleanup used git commands instead. The #895 cleanup later found that the target removes worktrees with `--force` and does not delete remote branches, so the explicit commands were the safer choice.
- The merge-pr agent asked whether the already-merged path expects `pr-state` or `verify-commit`. The skill does not say.

## 2026-10-03: express delivery of issue 895 through merge

The parent coordinated express-issue for [issue 895](https://github.com/lmorchard/decafclaw/issues/895) through merge, which Les authorized. Each phase ran in its own subagent. Implementation and review follow-up used Claude Opus 5.5; local review, submission, and merge used Claude Sonnet 5.5, selected by the dispatch. Skills at `2603989`. [PR #900](https://github.com/lmorchard/decafclaw/pull/900) merged as `6604c0b` from head `ff360b1`, with green hosted CI and Copilot "🟢 Approval recommended" with no findings for that head. This was the first full delivery that used all three CLI operations.

The fix let Starlette's `FileResponse` build the attachment header. Both new regressions failed on the base `4165293` with the reported `UnicodeEncodeError` and passed with the fix. The full suite went from 4257 to 4260 passed. No system install was needed, although Les had authorized Playwright dependencies.

The implementer reported, and the independent local review found without a prompt, one difference from the issue text. ASCII names that need URL quoting, such as `my report.txt`, now get only `filename*=utf-8''my%20report.txt`. Les accepted that form. The implementer pinned it with a test in a second commit, and the reviewer assessed only that change.

Lessons:

- `board set-status` made its first real writes: Backlog to In progress, and In progress to In review, each with a matching readback. Board automation set Done at both merges before the agent ran, so the Done step reported `unchanged`.
- `verify-commit` reads only published commits. The implementer-to-reviewer handoff happens before a push, so the parent verified those identifiers with git. After the push, submission, follow-up, and merge used the tool. Watch whether this gap causes an error before adding a local mode.
- Leaving the implementer's risk note out of the reviewer's handoff let the review confirm it independently.
- The submission agent stated that the automatic Copilot request "came from automation" because its actor was `lmorchard`. That actor does not show the cause; see [issue 1](https://github.com/lmorchard/gh-project-workflow/issues/1).
- decafclaw's AGENTS.md asks for a live test in Mattermost and the web UI after merge. That remains for Les.

## 2026-10-03: express delivery of issue 897 under MokaGnome

The parent coordinated express-issue for [issue 897](https://github.com/lmorchard/decafclaw/issues/897) through review follow-up, without merge, using the machine account `MokaGnome`. Subagents performed all subject-repository writes using the classic token at `~/.config/ghflow/mokagnome.token`. Skills commit was `7c59ab7`.

The task guarded four asynchronous functions in `schedule-page.js` against stale responses when a user selects another schedule. The first commit `8fa6b3f` added guards and eight component tests. An independent local review by Claude Sonnet found that `#onWikiSaved` did not guard against an A to B to A selection sequence. The implementer fixed the defect in commit `542db3d`, and a second local review confirmed the fix.

The reviewer also noted an in-flight status race in `#runNow`. A subagent verified the race and filed follow-up [issue 904](https://github.com/lmorchard/decafclaw/issues/904) as `MokaGnome`.

Subagents pushed the branch, submitted [PR #907](https://github.com/lmorchard/decafclaw/pull/907), moved issue 897 to In review on board 6, and verified green hosted CI. The subagent requested Copilot review. GitHub recorded no request because `MokaGnome` has no Copilot seat. Affirmative local review covered the published head commit `542db3d`.

Les explicitly authorized the merge. A subagent merged PR #907 as `MokaGnome` with merge commit `6b66ce0`. The merge closed issue 897, and board automation set Done. Local worktrees and branches were preserved.

## 2026-10-05: ready-queue burndown on board 6

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

## ghflow installation

[Setup trial, 2026-10-07](2026-10-07-ghflow-setup.md) assesses one registered skill, symbolic-link discovery, routing, and dependency access in Claude Code, Codex, and OpenCode.

[Root-package setup trial, 2026-10-07](2026-10-07-ghflow-root-setup.md) repeats discovery and routing after the repository-root layout change.
It records the subject-resolution correction and the unresolved OpenCode discovery of ignored nested worktrees.

## 2026-10-07: issue 8 reviewer preparation

The [reviewer preparation record](2026-10-07-issue-8-reviewer-capability.md) summarizes three historical paired trials and preserves pinned sources.
The shared instruction now establishes the required review path before substantial dependent implementation.
Four reusable [decision scenarios and results](../../evals/results/2026-10-07-reviewer-preparation.md) assess the revised instruction.
The broader identity and access scope remains open.
