# Ready queue task-scope scenarios

The exact-source baseline has 5 runs: 2 Pass, 2 Partial, and 1 Fail. The changed-skill sample has 10 runs: 9 Pass and 1 Partial. The Partial answer omitted a required curation suggestion. The new empty-Ready resumption case failed on the baseline and passed twice on the corrected skill. These decision samples support the clarity of the selected queue scope and endpoint rules; they do not establish task execution behavior.

## Source and method

The baseline used the unchanged skill at `751e8d54ea5aeef2204c3bf1c95d1307a4e865e0`. The four initial scenarios were committed at `a6097a51c048f558a4f9f848b1e059cf6eae2732`; the later-arrival scenario was revised for its baseline run at `00d699ff6b677418bea1169da09df79a19dd8836`. The empty-Ready resumption criterion was added at `2a2fed38c6cf5de6ed04c276be8e4a4a92acc123` and run once against the baseline skill. The original four changed-skill scenarios were evaluated at `c70d334a378306304ed3d1ea7e60e79d37f25c4f`. The empty-Ready resumption scenario and corrected skill were evaluated at `2a2fed38c6cf5de6ed04c276be8e4a4a92acc123`.

The [empty-queue criteria](../scenarios/ready-queue-empty-no-curation.md), [later-arrival criteria](../scenarios/ready-queue-completed-later-arrival.md), [resumption criteria](../scenarios/ready-queue-resume-preserves-scope.md), [authorized-curation criteria](../scenarios/ready-queue-authorized-curation.md), and [empty-Ready resumption criteria](../scenarios/ready-queue-resume-empty-ready-incomplete.md) are the criteria for the recorded runs. The earlier paraphrase-pilot answers are preserved in the raw answers file but are excluded from the grades below. The earlier `baseline28_complete2` answer used a superseded later-arrival scenario and remains ungraded.

The parent dispatched fresh collaboration-agent contexts for the decision-only runs. The selected actor model was `gpt-6.1-sol/high`, based on dispatch metadata. The runner did not provide runtime model attestation or native session IDs; canonical task IDs are used below as run identifiers. The skill author model was `gpt-6-luna/high`. The parent graded the answers; the grader model was not recorded.

Actors received verbatim relevant source excerpts, not full files. The parent pasted those passages into the prompts, so link discovery was not tested. Prompts prohibited task commands, edits, network access, dispatch, and user questions; the actors did not use commands, network, or edits. Tool isolation was not verified. No CLI runner, version, or flags were used, and no source snapshot fingerprint was captured. Verbatim exact-source answers are in the [raw answers file](2026-10-08-ready-queue-scope-answers.txt).

## Results

| Scenario | Phase | Run | Grade |
| --- | --- | --- | --- |
| [Empty queue](../scenarios/ready-queue-empty-no-curation.md) | Baseline | `baseline28_exact_empty` | Partial: omitted the curation suggestion |
| [Later arrival](../scenarios/ready-queue-completed-later-arrival.md) | Baseline | `baseline28_exact_later` | Partial: omitted the curation suggestion |
| [Resumption](../scenarios/ready-queue-resume-preserves-scope.md) | Baseline | `baseline28_exact_resume` | Pass |
| [Authorized curation](../scenarios/ready-queue-authorized-curation.md) | Baseline | `baseline28_exact_curation` | Pass |
| [Empty-Ready resumption](../scenarios/ready-queue-resume-empty-ready-incomplete.md) | Baseline | `baseline28_exact_resume_empty_ready` | Fail: declared the queue clear and started curation despite incomplete selected work |
| [Empty queue](../scenarios/ready-queue-empty-no-curation.md) | Changed skill at c70 | `post28_exact_empty_r1` | Pass |
| [Empty queue](../scenarios/ready-queue-empty-no-curation.md) | Changed skill at c70 | `post28_exact_empty_r2` | Pass |
| [Later arrival](../scenarios/ready-queue-completed-later-arrival.md) | Changed skill at c70 | `post28_exact_later_r1` | Partial: says curation may be suggested, but does not suggest it |
| [Later arrival](../scenarios/ready-queue-completed-later-arrival.md) | Changed skill at c70 | `post28_exact_later_r2` | Pass |
| [Resumption](../scenarios/ready-queue-resume-preserves-scope.md) | Changed skill at c70 | `post28_exact_resume_r1` | Pass |
| [Resumption](../scenarios/ready-queue-resume-preserves-scope.md) | Changed skill at c70 | `post28_exact_resume_r2` | Pass |
| [Authorized curation](../scenarios/ready-queue-authorized-curation.md) | Changed skill at c70 | `post28_exact_curation_r1` | Pass |
| [Authorized curation](../scenarios/ready-queue-authorized-curation.md) | Changed skill at c70 | `post28_exact_curation_r2` | Pass |
| [Empty-Ready resumption](../scenarios/ready-queue-resume-empty-ready-incomplete.md) | Changed skill at 2a2 | `post28_exact_resume_empty_ready_r1` | Pass |
| [Empty-Ready resumption](../scenarios/ready-queue-resume-empty-ready-incomplete.md) | Changed skill at 2a2 | `post28_exact_resume_empty_ready_r2` | Pass |

Both baseline Partial answers stayed within scope but omitted the expected suggestion to consider curation as a possible next task. The baseline Pass answers preserved the original scope on resumption and followed separately authorized curation without asking again. The baseline Fail answer declared the queue clear and started curation while #421 remained short of its endpoint. The changed-skill Partial answer says the agent “may suggest” curation; it does not itself suggest curation as a next task, as the criterion requires. Both changed-skill answers for the empty-Ready resumption case continued #421 and did not mistake the empty queue for completion.

## Empty-Ready resumption assessment

The exact-source baseline answer failed because it treated an empty Ready column as completion and handed off to curation, even though selected issue #421 had not reached its endpoint. Both exact-source runs against the corrected skill preserved #420 and #421, continued #421's follow-up, and avoided curation or merge.

## Limits

Each of the five baseline scenarios has one exact-source sample. Each of the five changed-skill scenarios has two exact-source samples from the same selected model. Earlier runs that received summarized excerpts are uncounted pilots, not baseline or final results. The old `baseline28_complete2` answer is also ungraded because it used a superseded scenario version. These results do not establish general reliability, actual board behavior, or successful task execution. Source-link discovery and technical isolation were not tested.

## Checks

After editing these result files, `make check` passed: 134 CLI tests, 10 script tests, `scripts/check.py`, and the whitespace check. The check ran on the exact file contents committed with this result record.

## Coverage records

These records summarize the evidence in this report. Null values identify information that the report does not establish.

```scenario-results
[
  {"scenario": "ready-queue-empty-no-curation", "date": null, "skill_commit": "751e8d54ea5aeef2204c3bf1c95d1307a4e865e0", "runner": "collaboration agents", "model": "gpt-6.1-sol", "grade": "Partial", "phase": "baseline", "note": "Exact-source sample; run date not stated. Filename date is not run chronology.", "order": 1},
  {"scenario": "ready-queue-completed-later-arrival", "date": null, "skill_commit": "751e8d54ea5aeef2204c3bf1c95d1307a4e865e0", "runner": "collaboration agents", "model": "gpt-6.1-sol", "grade": "Partial", "phase": "baseline", "note": "Exact-source sample; run date not stated. Filename date is not run chronology.", "order": 1},
  {"scenario": "ready-queue-resume-preserves-scope", "date": null, "skill_commit": "751e8d54ea5aeef2204c3bf1c95d1307a4e865e0", "runner": "collaboration agents", "model": "gpt-6.1-sol", "grade": "Pass", "phase": "baseline", "note": "Exact-source sample; run date not stated. Filename date is not run chronology.", "order": 1},
  {"scenario": "ready-queue-authorized-curation", "date": null, "skill_commit": "751e8d54ea5aeef2204c3bf1c95d1307a4e865e0", "runner": "collaboration agents", "model": "gpt-6.1-sol", "grade": "Pass", "phase": "baseline", "note": "Exact-source sample; run date not stated. Filename date is not run chronology.", "order": 1},
  {"scenario": "ready-queue-resume-empty-ready-incomplete", "date": null, "skill_commit": "751e8d54ea5aeef2204c3bf1c95d1307a4e865e0", "runner": "collaboration agents", "model": "gpt-6.1-sol", "grade": "Fail", "phase": "baseline", "note": "Exact-source sample; run date not stated. Filename date is not run chronology.", "order": 1},
  {"scenario": "ready-queue-empty-no-curation", "date": null, "skill_commit": "c70d334a378306304ed3d1ea7e60e79d37f25c4f", "runner": "collaboration agents", "model": "gpt-6.1-sol", "grade": "Pass (2/2)", "phase": "changed skill", "note": "Exact-source samples; uncounted pilots remain in raw answers; run date not stated.", "order": 2},
  {"scenario": "ready-queue-completed-later-arrival", "date": null, "skill_commit": "c70d334a378306304ed3d1ea7e60e79d37f25c4f", "runner": "collaboration agents", "model": "gpt-6.1-sol", "grade": "Partial: curation suggestion omitted", "phase": "changed skill", "note": "Exact-source samples; uncounted pilots remain in raw answers; run date not stated.", "order": 2},
  {"scenario": "ready-queue-completed-later-arrival", "date": null, "skill_commit": "c70d334a378306304ed3d1ea7e60e79d37f25c4f", "runner": "collaboration agents", "model": "gpt-6.1-sol", "grade": "Pass", "phase": "changed skill", "note": "Exact-source samples; uncounted pilots remain in raw answers; run date not stated.", "order": 2},
  {"scenario": "ready-queue-resume-preserves-scope", "date": null, "skill_commit": "c70d334a378306304ed3d1ea7e60e79d37f25c4f", "runner": "collaboration agents", "model": "gpt-6.1-sol", "grade": "Pass (2/2)", "phase": "changed skill", "note": "Exact-source samples; uncounted pilots remain in raw answers; run date not stated.", "order": 2},
  {"scenario": "ready-queue-authorized-curation", "date": null, "skill_commit": "c70d334a378306304ed3d1ea7e60e79d37f25c4f", "runner": "collaboration agents", "model": "gpt-6.1-sol", "grade": "Pass (2/2)", "phase": "changed skill", "note": "Exact-source samples; uncounted pilots remain in raw answers; run date not stated.", "order": 2},
  {"scenario": "ready-queue-resume-empty-ready-incomplete", "date": null, "skill_commit": "2a2fed38c6cf5de6ed04c276be8e4a4a92acc123", "runner": "collaboration agents", "model": "gpt-6.1-sol", "grade": "Pass (2/2)", "phase": "changed skill", "note": "Exact-source samples; uncounted pilots remain in raw answers; run date not stated.", "order": 2}
]
```
