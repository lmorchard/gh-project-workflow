# Ready queue task-scope scenarios

The baseline sample had 4 runs: 2 Pass and 2 Partial. After the skill change, all 8 runs passed across the four scenarios (4 scenarios × 2 runs). These decision samples support the clarity of the selected queue scope and endpoint rules; they do not establish task execution behavior.

## Source and method

The baseline used the unchanged skill at `751e8d54ea5aeef2204c3bf1c95d1307a4e865e0`. Three final scenario versions were committed at `a6097a51c048f558a4f9f848b1e059cf6eae2732`; the later-arrival scenario was clarified for baseline rerun at `00d699ff6b677418bea1169da09df79a19dd8836`. The changed skill and final four scenario files are at `c70d334a378306304ed3d1ea7e60e79d37f25c4f`.

The [scenario criteria](../scenarios/ready-queue-empty-no-curation.md), [later-arrival criteria](../scenarios/ready-queue-completed-later-arrival.md), [resumption criteria](../scenarios/ready-queue-resume-preserves-scope.md), and [authorized-curation criteria](../scenarios/ready-queue-authorized-curation.md) were unchanged during post-change runs. The initial later-arrival baseline answer used a superseded scenario version and is preserved as ungraded in the raw answers file; it is not included in the final baseline sample set.

The parent dispatched fresh collaboration-agent contexts for the decision-only runs. The selected actor model was `gpt-6.1-sol/high`, based on dispatch metadata. The runner did not provide runtime model attestation or native session IDs; canonical task IDs are used below as run identifiers. The skill author model was `gpt-6-luna/high`. The parent graded the answers; the grader model was not recorded.

The actors lacked a Read tool and could not run commands. The parent pasted the skill and source text into the prompts, so link discovery was not tested. Prompts prohibited task commands, edits, network access, dispatch, and user questions. Fresh contexts were used, but the runner did not verify filesystem, network, or credential isolation. No CLI runner, version, or flags were used, and no source snapshot fingerprint was captured. Verbatim answers are in the [raw answers file](2026-10-08-ready-queue-scope-answers.txt).

## Results

| Scenario | Source phase | Run | Grade |
| --- | --- | --- | --- |
| [Empty queue](../scenarios/ready-queue-empty-no-curation.md) | Baseline | `baseline28_empty2` | Partial: omitted the curation suggestion |
| [Later arrival](../scenarios/ready-queue-completed-later-arrival.md) | Baseline | `baseline28_late_arrival` | Partial: omitted the curation suggestion |
| [Resumption](../scenarios/ready-queue-resume-preserves-scope.md) | Baseline | `baseline28_resume2` | Pass |
| [Authorized curation](../scenarios/ready-queue-authorized-curation.md) | Baseline | `baseline28_curation2` | Pass |
| [Empty queue](../scenarios/ready-queue-empty-no-curation.md) | Changed skill | `post28_empty_r1` | Pass |
| [Empty queue](../scenarios/ready-queue-empty-no-curation.md) | Changed skill | `post28_empty_r2` | Pass |
| [Later arrival](../scenarios/ready-queue-completed-later-arrival.md) | Changed skill | `post28_later_r1` | Pass |
| [Later arrival](../scenarios/ready-queue-completed-later-arrival.md) | Changed skill | `post28_later_r2` | Pass |
| [Resumption](../scenarios/ready-queue-resume-preserves-scope.md) | Changed skill | `post28_resume_r1` | Pass |
| [Resumption](../scenarios/ready-queue-resume-preserves-scope.md) | Changed skill | `post28_resume_r2` | Pass |
| [Authorized curation](../scenarios/ready-queue-authorized-curation.md) | Changed skill | `post28_curation_r1` | Pass |
| [Authorized curation](../scenarios/ready-queue-authorized-curation.md) | Changed skill | `post28_curation_r2` | Pass |

The two baseline Partial answers reached the safe no-curation decision but omitted the expected suggestion to consider curation as a next task. The later-arrival baseline also identified the ambiguity in the old “next item in Ready” wording. The two baseline Pass answers preserved the original scope on resumption and followed separately authorized curation without asking again.

## Limits

Each baseline scenario has one final sample. Each changed-skill scenario has two samples from the same selected model. The earlier `baseline28_complete2` answer evaluated a superseded later-arrival scenario and is retained only as ungraded evidence. These results do not establish general reliability, actual board behavior, or successful task execution. Source-link discovery and technical isolation were not tested.

## Checks

After adding these result files, `make check` passed: 134 CLI tests, 10 script tests, `scripts/check.py`, and the whitespace check. The check ran on the exact file contents committed with this result record.
