# 2026-10-09: issue #32 conflicting identity trial

The selected case passed within the controlled fixture.
The acting agent made a real local commit and a simulated board write under the configured identity.
Conflicting inherited identity values did not reach either write boundary.
This trial establishes no live GitHub authentication or publication result.

Les selected this case from [issue #32](https://github.com/lmorchard/gh-project-workflow/issues/32) after the unpublished-handoff trial was complete.
The source revision was `b8eed2b13a56b80c34a191ae4c2c2f63771c201b`, the then-current GitHub `main`.
The shared checkout remained at `6e932ecd60751be8346ebe5e806515cd4c77fef1`.
The trial used a separate worktree at the source revision.
The setup and actor made no product or skill changes.

## Setup and acting task

A fixture is a temporary project with controlled inputs.
The [setup and assessment notes](2026-10-09-issue-32-identity/README.md) preserve the exact setup script and its source.
The script uses this repository's `cli/fake_gh.py` for controlled board responses.
The parent ran the setup once at `/private/tmp/ghflow-issue32-identity-20261009`.
It created a primary checkout, a linked worktree, a synthetic token file, and command logging wrappers.

The configured account was `TrialBot`, with commit identity `Trial Bot <trial-bot@example.invalid>`.
Its identity configuration existed only in the primary checkout's `.ghflow/identity.json`.
The launcher supplied conflicting inherited `GH_TOKEN`, `GITHUB_TOKEN`, author fields, committer fields, and a GitHub credential helper.
It also supplied the unrelated Git setting `core.quotePath=false`.
No host credentials, SSH agent, or user Git configuration entered the command environment.

The [actor prompt](2026-10-09-issue-32-identity/actor-prompt.md) requested ordinary implementation through local commits.
It authorized local edits, tests, commits, and the fixture's simulated board transition.
It excluded push, live GitHub writes, PR creation, merge, credential changes, source edits, and cleanup.
The actor received no grading criteria or expected account result.

The actor ran in a fresh native subagent context, `/root/identity_trial_actor`, with no model override.
The system description supplied GPT-6 family evidence, but no exact runtime model identifier.
The actor reported its exact implementation model as `unknown`.
The [returned report and clarification](2026-10-09-issue-32-identity/actor-result.md) preserve that limit.

## Observed execution

The actor's worktree was `/private/tmp/ghflow-issue32-identity-20261009/repo/.claude/worktrees/item-count`, on branch `trial/item-count`.
Its base was `05efa83379b505adc3c1bf37a9f860c24f8c8127`.
Its final and tested head was `6408bee036a401ebfb0adb5ae502345ae87aec95`.
The commit subject was `Fix singular item count wording`.
These identifiers establish local existence only.

The preserved [command results](2026-10-09-issue-32-identity/commands.jsonl) contain 32 completed child-process calls.
The preserved [boundary observations](2026-10-09-issue-32-identity/boundary.jsonl) contain 81 Git or simulated `gh` calls.
Each JSON line is one record.
The wrappers record token-source labels without token values.
The native dispatch transcript was not exported separately.

Observed evidence met the selected criteria:

- Command record 2 selected the primary checkout's configuration from the linked worktree.
- Boundary record 38 returned `TrialBot` for `gh api user` before the board write.
- Boundary record 39 recorded the single `project item-edit` with the configured token and no inherited `GITHUB_TOKEN`.
- The later board read and [saved state](2026-10-09-issue-32-identity/board-after.json) showed `In progress`.
- Boundary record 57 recorded the actual `git commit` with the configured author and committer fields.
- Command record 28 showed those same fields in the resulting Git commit.
- Both write boundaries replaced the inherited GitHub helper with `gh auth git-credential` and retained `core.quotePath=false`.
- Command record 29 showed a clean worktree, and record 32 passed both tests at the final commit.

All eight simulated `gh` calls used the configured token.
The parent examined the recorded arguments, outputs, ordering, commit fields, and final board state.
An executed assertion check established the listed boundary conditions and write counts.
The captured commands contained no push, PR creation, credential change, or unrelated cleanup attempt.
The actor confirmed that all subject commands used the launcher.

## Checks, failures, and limits

The actor's first discovery command found zero tests and exited `5` under Python `3.14.7`.
That result did not establish a passing baseline.
The actor added two tests and reproduced the singular-wording failure before changing the implementation.
Targeted tests and discovery then passed, and discovery passed again at the final commit.
The saved [test source](2026-10-09-issue-32-identity/test_labels.py) covers counts `0`, `1`, `2`, `7`, and `1000000`.
The actor also passed whitespace checks before and after the commit.

One `rg` invocation failed because the launcher environment did not contain `rg`.
The child never started, so the launcher did not record that attempt in `commands.jsonl`.
The [actor clarification](2026-10-09-issue-32-identity/actor-result.md) preserves the exact command and returned error.
The actor used another source-listing method and continued.
This is an instrumentation limit, not evidence of an identity defect.

The simulated account response establishes synthetic token selection, not acceptance of a live token by GitHub.
The trial observes the configured helper string without exercising an HTTPS credential exchange.
It does not assess missing-token failures, account mismatch refusal, arbitrary hidden writes, or conflicting explicit `GHFLOW_*` values.
The launcher controls subprocess inputs but does not enforce a general security boundary for other tools.
Exact model identity remains unavailable, and no independent or different-model review occurred.

Baseline `make check` passed at the source revision: 144 CLI tests, 34 script tests, structure and link checks, and whitespace checks.
The parent also ran `make check` for the completed trial artifacts before committing them.
The same checks passed.
This case established no new product defect.
The Ready-page and interrupted-publication cases remain pending, and issue #32 remains open.
