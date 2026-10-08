# Issue 8 reviewer preparation, 2026-10-07

Delivery now establishes an available independent review path before substantial dependent implementation.
The shared [review preparation rule](../../references/shared/review.md#prepare-required-review) owns this instruction.
The three delivery coordinators link to it.
Four reusable [decision scenarios](../../evals/results/2026-10-07-reviewer-preparation.md) assess the revised instruction.
This is the first increment for [issue #8](https://github.com/lmorchard/gh-project-workflow/issues/8), which remains open.

## Historical paired trial

The earlier trial used three pairs of fresh native Claude Code sessions at skill revision `b47c9d5088f471da5d7b35a56ecda6078dee02be`.
Each pair compared delivery through PR review follow-up with an ordinary draft-only request.
The public synthetic [fixture](2026-10-07-issue-8-reviewer-capability/fixture) contains a slug function and one existing test.
A fixture is a small project used for a trial.
The [delivery prompt](2026-10-07-issue-8-reviewer-capability/dependent-prompt.txt) and [draft prompt](2026-10-07-issue-8-reviewer-capability/ordinary-prompt.txt) remain available.
Neither prompt named a reviewer problem.

All three delivery sessions reported unavailable dispatch and different-model review before edits.
They researched the function and proposed tests without implementation, tests, commits, or PR preparation.
All three draft sessions returned drafts without reviewer capability assessment or review-source reads.
No session used Edit or Write, and all reported zero spawned subagents.
The ordinary repeat did a scoped Git read and one passing fixture test.
The ordinary final stated that it did not execute tests.
The drafts differed about tabs and newlines, which the trial did not assess.

The original [record](https://github.com/lmorchard/gh-project-workflow/blob/7e3f90dbc8db7a765d30fb515ff584a31ee618d9/docs/trials/2026-10-07-issue-8-reviewer-capability.md) preserves all six observations and their qualifications.
Its pinned [actions](https://github.com/lmorchard/gh-project-workflow/blob/7e3f90dbc8db7a765d30fb515ff584a31ee618d9/docs/trials/2026-10-07-issue-8-reviewer-capability/actions.json) identify the six exact response files and source reads.
The original streams remain at `/private/tmp/ghflow-issue8-trial-kzdmu9xm` where available.
The pinned [source manifest](https://github.com/lmorchard/gh-project-workflow/blob/7e3f90dbc8db7a765d30fb515ff584a31ee618d9/docs/trials/2026-10-07-issue-8-reviewer-capability/source-manifest.json) records sizes, SHA-256 hashes, and supplied launch provenance.
SHA-256 is a content hash that identifies file bytes.
The compact summary replaces repeated responses and action extracts in this branch.

## Historical environment and limits

All six sessions reported Claude Code `2.1.293`, `dontAsk` permissions, and no MCP servers.
MCP connects external tools to an agent.
Their tool roster contained Bash, Edit, Glob, Grep, Read, Skill, and Write, with no Agent or Task.
The supplied [launch record](https://github.com/lmorchard/gh-project-workflow/blob/7e3f90dbc8db7a765d30fb515ff584a31ee618d9/docs/trials/2026-10-07-issue-8-reviewer-capability/launch-record.json) preserves exact scoped allowances and all six exit codes of 0.
It is orchestration evidence, recorded after the original author inspected the streams.
It is separate from provider-returned model metadata.

All launches selected `claude-opus-5-5`.
All streams returned that model in startup, assistant events, and model usage.
No reviewer was dispatched.
Response examples that named another model did not establish its availability.
The fixture history named `5a1c463`; the ordinary repeat returned `5a1c463f5d9dd65c1f71d0b5a1f414f20946fecd`.

General implementation dispatch was also absent, so the trial did not isolate a reviewer-only failure.
The fixture had no GitHub remote.
The first delivery status denial came from mismatched command allowances.
Later launches added those harmless Git patterns, but delivery sessions did not retry that status form.
Compound Bash reads still received denials while file Read succeeded.
All delivery responses incorrectly described Bash as unavailable and their first Bash command as denied.
Those first commands succeeded.
The ordinary baseline and final also overstated shell restrictions.
The ordinary repeat showed that a scoped Git/test command succeeded.
A compound-command denial does not establish that each operation is unavailable.

The delivery responses requested dispatch and a different reviewer model, plus broader Bash permission than the evidence supported.
They offered direct implementation only with an explicit exception, and left the different-model requirement unmet.
No exception arrived and no alternative ran.
The trial did not exercise publication, review execution, different-model dispatch, recovery, or full delivery.

## Decision and provenance

The historical trial supported task-specific preparation and the draft comparison.
It did not independently establish a missing review rule.
Les subsequently requested persistent shared guidance and reusable evaluations, rather than an archive-only change.
That decision strengthens the earlier “when possible” planning instruction.
The new scenarios assess decisions under constructed capability facts, separately from the historical observed runtime limits.

The original substantive author and launch-record correction author each had native dispatch selection `gpt-6.1-sol`.
Their independent `gpt-6-astra` reviews covered the published `7e3f90dbc8db7a765d30fb515ff584a31ee618d9`, as recorded in [PR #21](https://github.com/lmorchard/gh-project-workflow/pull/21).
Those reviews do not cover this revision.
This revision's source, trial execution, and evaluation-record author also has explicit native dispatch selection `gpt-6.1-sol`.
The orchestration host's original model is unknown and it authored no product content.
A fresh independent native `gpt-6-astra` source review is planned after the local commit.
Dispatch selections are evidence of selection, not separate provider confirmation.

The author read issue #8 and PR #21 through this worktree's absolute `cli/ghflow.py exec -- gh`.
Issue #8 was OPEN, with no comments and `updatedAt` of `2026-10-08T00:05:44Z`.
Broader identity, authentication, repository and board access, and project-check preparation remain open.
No diagnostic command, capability registry, scheduler, or account or settings change belongs to this increment.
The historical trial records do not become mandatory records for other projects.
