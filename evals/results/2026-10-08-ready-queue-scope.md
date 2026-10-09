# Ready queue task-scope scenarios

The exact-source baseline had 4 runs: 2 Pass and 2 Partial. After the skill change, all 8 exact-source runs passed across the four scenarios (4 scenarios × 2 runs). These decision samples support the clarity of the selected queue scope and endpoint rules; they do not establish task execution behavior.

## Source and method

The baseline used the unchanged skill at `751e8d54ea5aeef2204c3bf1c95d1307a4e865e0`. Three final scenario versions were committed at `a6097a51c048f558a4f9f848b1e059cf6eae2732`; the later-arrival scenario was revised for its baseline run at `00d699ff6b677418bea1169da09df79a19dd8836`. The changed skill and final four scenarios are at `c70d334a378306304ed3d1ea7e60e79d37f25c4f`.

The [empty-queue criteria](../scenarios/ready-queue-empty-no-curation.md), [later-arrival criteria](../scenarios/ready-queue-completed-later-arrival.md), [resumption criteria](../scenarios/ready-queue-resume-preserves-scope.md), and [authorized-curation criteria](../scenarios/ready-queue-authorized-curation.md) are the criteria for these runs. The earlier paraphrase-pilot answers are preserved in the raw answers file but are excluded from the grades below. The earlier `baseline28_complete2` answer used a superseded later-arrival scenario and remains ungraded.

The parent dispatched fresh collaboration-agent contexts for the decision-only runs. The selected actor model was `gpt-6.1-sol/high`, based on dispatch metadata. The runner did not provide runtime model attestation or native session IDs; canonical task IDs are used below as run identifiers. The skill author model was `gpt-6-luna/high`. The parent graded the answers; the grader model was not recorded.

Actors received verbatim relevant source excerpts, not full files. The parent pasted those passages into the prompts, so link discovery was not tested. Prompts prohibited task commands, edits, network access, dispatch, and user questions; the actors did not use commands, network, or edits. Tool isolation was not verified. No CLI runner, version, or flags were used, and no source snapshot fingerprint was captured. Verbatim exact-source answers are in the [raw answers file](2026-10-08-ready-queue-scope-answers.txt).

## Results

| Scenario | Phase | Run | Grade |
| --- | --- | --- | --- |
| [Empty queue](../scenarios/ready-queue-empty-no-curation.md) | Baseline | `baseline28_exact_empty` | Partial: omitted the curation suggestion |
| [Later arrival](../scenarios/ready-queue-completed-later-arrival.md) | Baseline | `baseline28_exact_later` | Partial: omitted the curation suggestion |
| [Resumption](../scenarios/ready-queue-resume-preserves-scope.md) | Baseline | `baseline28_exact_resume` | Pass |
| [Authorized curation](../scenarios/ready-queue-authorized-curation.md) | Baseline | `baseline28_exact_curation` | Pass |
| [Empty queue](../scenarios/ready-queue-empty-no-curation.md) | Changed skill | `post28_exact_empty_r1` | Pass |
| [Empty queue](../scenarios/ready-queue-empty-no-curation.md) | Changed skill | `post28_exact_empty_r2` | Pass |
| [Later arrival](../scenarios/ready-queue-completed-later-arrival.md) | Changed skill | `post28_exact_later_r1` | Pass |
| [Later arrival](../scenarios/ready-queue-completed-later-arrival.md) | Changed skill | `post28_exact_later_r2` | Pass |
| [Resumption](../scenarios/ready-queue-resume-preserves-scope.md) | Changed skill | `post28_exact_resume_r1` | Pass |
| [Resumption](../scenarios/ready-queue-resume-preserves-scope.md) | Changed skill | `post28_exact_resume_r2` | Pass |
| [Authorized curation](../scenarios/ready-queue-authorized-curation.md) | Changed skill | `post28_exact_curation_r1` | Pass |
| [Authorized curation](../scenarios/ready-queue-authorized-curation.md) | Changed skill | `post28_exact_curation_r2` | Pass |

Both baseline Partial answers stayed within scope but omitted the expected suggestion to consider curation as a possible next task. The baseline Pass answers preserved the original scope on resumption and followed separately authorized curation without asking again.

## Limits

Each baseline scenario has one exact-source sample. Each changed-skill scenario has two exact-source samples from the same selected model. Earlier runs that received summarized excerpts are uncounted pilots, not baseline or final results. The old `baseline28_complete2` answer is also ungraded because it used a superseded scenario version. These results do not establish general reliability, actual board behavior, or successful task execution. Source-link discovery and technical isolation were not tested.

## Checks

After editing these result files, `make check` passed: 134 CLI tests, 10 script tests, `scripts/check.py`, and the whitespace check. The check ran on the exact file contents committed with this result record.
