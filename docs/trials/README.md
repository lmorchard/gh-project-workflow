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
