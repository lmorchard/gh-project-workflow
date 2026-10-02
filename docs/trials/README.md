# Trial records

This index lists trials of the skills on real issues. Each entry states what the trial exercised and its evidence limits. The subject repository is [decafclaw](https://github.com/lmorchard/decafclaw).

## 2026-09-30: issue 843 definition, filing, and decomposition

The [issue 843 folder](2026-09-30-issue-843/) contains agent output from these trials:

- [Issue definition trial results](2026-09-30-issue-843/review.md) for define-issue in a fresh agent context.
- [Filing the reviewed issue](2026-09-30-issue-843/filing.md) for file-issue, which created issue 861.
- [Proposed reconsideration](2026-09-30-issue-843/reconsider-proposal.md) for reconsider-issue.
- [Read-only decomposition](2026-09-30-issue-843/decomposition.md) for decompose-parent-issue.
- [Sticky lookup draft](2026-09-30-issue-843/sticky-lookup-draft.md) and [listing child draft](2026-09-30-issue-843/listing-child-draft.md) for reviewed child definitions.

## 2026-10-01: implementation and express delivery

The issue 863 trial completed implementation, submission, Copilot follow-up, and a separately authorized merge. The issue 865 trial then exercised express-issue through review follow-up, including different-model local review, a Copilot finding, correction, and current-head review and CI.

The issue 867 trial exercised the express merge endpoint through PR #868. The user required both affirmative review and green CI. The coordinator waited for the final hosted check, then merged the exact reviewed commit with a matching-head condition. This successful case does not establish every rejection or recovery path. Live post-merge application checks remained unperformed.

The folder-management trial continued from definition and filing (#869) through implementation, independent review, PR #870, and merge. No product question or repeated authorization was needed. Favorable local and Copilot reviews and green hosted CI covered the exact merged head. The coordinator hit an agent-capacity limit, so the parent continued phase dispatch after its handoff. This tested continuity across skills, not a new automatic backlog selector. Live post-merge checks remained unperformed.

After the issue 871 / PR #872 merge, Les reported that the manual smoke test seemed fine. This is user-reported evidence. The conversation does not specify which surfaces or scenarios were tested, so it does not establish completion of every project-required live check.
