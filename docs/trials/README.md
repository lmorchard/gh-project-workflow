# Trial records

This index lists trials of the skills on real issues. Each entry states what the trial exercised and its evidence limits. The subject repository is [decafclaw](https://github.com/lmorchard/decafclaw).

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

The [issue 843 folder](2026-09-30-issue-843/) contains agent output from these trials:

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
