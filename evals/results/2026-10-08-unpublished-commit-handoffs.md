# Unpublished commit handoff scenarios, 2026-10-08

Three fresh decision-only sessions assessed the issue #24 scenarios. Two passed the expected decision. The local-review answer reached the core decision but omitted checks required by the full criteria.

## Source and method

The evaluated skill and scenario commit is `2340bd70386020fa7bab70f7285e727a50ddf320`.
Per the parent dispatch report, each fresh session used `gpt-6-luna` at high reasoning and received only its scenario Situation and the applicable skill paths. The Expected and Not acceptable sections were withheld.
The parent supplied the final answers and dispatch model selection. Session identifiers and raw prompt or runtime logs were not supplied.
The [returned answers](2026-10-08-unpublished-commit-handoffs-answers.txt) preserve the exact answer text supplied by the parent.

The sessions were asked for a decision only. They did not run commands, inspect a repository, push a branch, or perform a review.

## Results

| Scenario | Grade | Observed decision |
| --- | --- | --- |
| `unpublished-local-review` | Partial | Dispatch `review-changes` for the unpublished commit. Include the checkout, publication state, base, and head; verify both commits locally. Preserve the no-push boundary and require reassessment if the published head differs from the reviewed head. The answer did not state that local verification proves local existence only, explicitly check the branch pointer, or require remote `verify-commit` after publication. |
| `unpublished-local-commit-missing` | Pass | Stop before review, return the missing `abc123` head to the parent, request a corrected checkout or head, then verify the head, base, and branch before continuing. No replacement commit or push was proposed. |
| `unpublished-local-commit-mismatch` | Pass | Stop before review because `fix/widget` points to `789def` instead of `abc123`; return the mismatch to the parent without reviewing a substitute or publishing the branch. |

The local-review answer correctly chose an unpublished local-review handoff and kept publication separate. Its omissions make this a partial result against the full Expected criteria. Do not treat the answer as evidence that the branch-pointer check or later remote verification was observed.

## Local Git demonstration

Separately from the decision-only sessions, a temporary repository with no remote exercised the local checks at implementation commit `2340bd70386020fa7bab70f7285e727a50ddf320`.
The supplied base and head resolved with `git -C CHECKOUT rev-parse --verify 'REV^{commit}'`. The reported branch resolved to the head, and `git -C CHECKOUT show -s --format=%s FULL_SHA` returned the expected subject.
A missing reference failed to resolve. Comparing the branch head with an incorrect expected head rejected the mismatch. The fixture had no remote, and no push occurred.
This demonstrates local Git check behavior. It does not demonstrate a fresh-agent review or remote verification after publication.

After adding this result record, `make check` passed all 119 CLI tests, all 10 script tests, `scripts/check.py`, and tracked whitespace checks.

## Limits

Each scenario has one sample from the same selected model. These answers assess proposed decisions, not task execution or general reliability. No scenario was repeated. The real implementation-and-review trial remains out of scope for issue #24.

## Coverage records

These records summarize the evidence in this report. Null values identify information that the report does not establish.

```scenario-results
[
  {"scenario": "unpublished-local-commit-missing", "date": "2026-10-08", "skill_commit": "2340bd70386020fa7bab70f7285e727a50ddf320", "runner": null, "model": "gpt-6-luna", "grade": "Pass", "phase": "sample", "note": "Parent dispatch selection only. Runner tool not named in the report.", "order": null},
  {"scenario": "unpublished-local-commit-mismatch", "date": "2026-10-08", "skill_commit": "2340bd70386020fa7bab70f7285e727a50ddf320", "runner": null, "model": "gpt-6-luna", "grade": "Pass", "phase": "sample", "note": "Parent dispatch selection only. Runner tool not named in the report.", "order": null},
  {"scenario": "unpublished-local-review", "date": "2026-10-08", "skill_commit": "2340bd70386020fa7bab70f7285e727a50ddf320", "runner": null, "model": "gpt-6-luna", "grade": "Partial", "phase": "sample", "note": "Parent dispatch selection only; branch-pointer and remote-verification omissions. Runner tool not named in the report.", "order": null}
]
```
