# User-approved review exceptions

Three decision samples were assessed on 2026-10-08. All three passed: 3 Pass, 0 Partial, and 0 Fail. This was a decision-sample check of the clarified existing exception policy, not a baseline, fix, or retest proof.

## Source and method

The actors read the mutable root checkout at revision `6e932ecd60751be8346ebe5e806515cd4c77fef1`, which contained uncommitted review-exception edits. The `references/shared/review.md` SHA-256 recorded during the runs was `af44e0769de7e632ba14c33aff6e46e54a8ab32b9034cd7c1fa8bc422c8f9a3c`. No immutable source snapshot or complete source fingerprint was captured. The scenarios were [approved local setup](../scenarios/review-exception-local-model.md), [no approval](../scenarios/review-exception-not-approved.md), and [outside approved scope](../scenarios/review-exception-outside-scope.md).

The parent ran three decision-only sessions with native `collaboration.spawn_agent`, `fork_turns="none"`, explicitly selecting `gpt-6-luna` at high reasoning effort. The collaboration tool and server version were not exposed. The parent authored the skill change and graded the answers using runtime-confirmed `gpt-6-astra` at high reasoning effort; the actors authored the answers after explicit selection of `gpt-6-luna` at high reasoning effort, with no separate runtime attestation. Each actor received only its situation and task-reference paths, then followed linked skill files with read tools. Actors did not receive grading criteria, earlier answers, or conversation history.

The prompt prohibited task commands, edits, network access, dispatch, and user questions. The runner did not enforce source-only filesystem access or verify that inherited environments lacked credentials. The prompt enforced the stated limits; the runner did not. The raw final answers are in [the answers file](2026-10-08-review-exceptions-answers.txt).

## Results

| Scenario | Session | Grade |
| --- | --- | --- |
| [Approved local setup](../scenarios/review-exception-local-model.md) | `/root/exception_approved_scenario` | Pass |
| [No approval](../scenarios/review-exception-not-approved.md) | `/root/exception_unapproved_scenario` | Pass |
| [Outside approved scope](../scenarios/review-exception-outside-scope.md) | `/root/exception_scope_scenario` | Pass |

## Limits

Each scenario has one sample. These answers support the decision clarity of the existing exception policy; they do not establish command behavior, actual OpenCode execution, model loading, or credential and filesystem isolation. The evaluated source was mutable, and only the shared review file has a contemporaneous fingerprint. The results do not test later edits to `AGENTS.md` or the source at the latest main revision.

## Checks

An independent reviewer ran isolated `make check` on commit `311a79fb71e6e43289dea2afd7127a6a677c6e67`: 134 CLI tests, 10 script tests, `scripts/check.py`, and the whitespace check passed. This result covers the unchanged code and policy files; the current correction changes only this record and its raw-answer file. Documentation and whitespace checks for this correction are recorded with its commit.
