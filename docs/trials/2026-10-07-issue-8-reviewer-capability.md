# Issue 8 reviewer capability trial, 2026-10-07

Existing guidance detected unavailable dispatch before fixture implementation. The comparison task returned an issue draft without a reviewer capability assessment. This first increment records evidence only. It changes no skill instructions or review policy.

The dependent task stopped for several reasons. This controlled setup does not isolate reviewer availability from general implementation dispatch or shell permission errors. It does not establish full delivery. The broader scope of [issue #8](https://github.com/lmorchard/gh-project-workflow/issues/8) remains open.

## Requests and sources

The trial used two identical public synthetic fixtures, small projects used for a trial. Their [source files](2026-10-07-issue-8-reviewer-capability/fixture) contain one function and one existing test. The function converts text to URL slugs. It changes letters to lowercase and all spaces to hyphens.

The [dependent raw request](2026-10-07-issue-8-reviewer-capability/dependent-prompt.txt) was:

```text
Use ghflow to deliver the selected issue in issue.md in this local synthetic repository through PR review follow-up. Implementation, tests, commits, and PR preparation are authorized; do not merge. The selected subject is this checkout. It has no GitHub remote, so keep publication local if remote access is unavailable.
```

The [ordinary raw request](2026-10-07-issue-8-reviewer-capability/ordinary-prompt.txt) was:

```text
Use ghflow to prepare a draft issue for the idea in issue.md in this local synthetic repository. This is draft-only. Return the draft in your response; do not publish or implement it.
```

Neither request told the agent to find a reviewer problem. The skill source and this author task started at `b47c9d5088f471da5d7b35a56ecda6078dee02be`. Fixture Git history named `5a1c463`, and the ordinary repeat returned `5a1c463f5d9dd65c1f71d0b5a1f414f20946fecd`.

The author read the issue through the absolute root `cli/ghflow.py exec -- gh issue view`. It was OPEN, with no comments and `updatedAt` equal to `2026-10-08T00:05:44Z`. This record addresses its agreed first increment.

The author inspected all six event streams and final responses in `/private/tmp/ghflow-issue8-trial-kzdmu9xm`. The inspection included prompts, fixtures, metadata, baseline summaries, and all six empty stderr files. Retained [actions](2026-10-07-issue-8-reviewer-capability/actions.json) contain every tool call and result status. Response files preserve terminal text. The [source manifest](2026-10-07-issue-8-reviewer-capability/source-manifest.json) records original sizes and SHA-256 content hashes.

Long successful reads appear as lengths and hashes. The extract omits internal reasoning and machine details and adds no expected actions. Original streams remain in the source bundle. Supplied [metadata](2026-10-07-issue-8-reviewer-capability/fixture-metadata.json) identifies the revision and public synthetic scope.

## Environment and model evidence

All six native Claude Code sessions reported version `2.1.293` and permission mode `dontAsk`. Their startup tool roster was `Bash`, `Edit`, `Glob`, `Grep`, `Read`, `Skill`, and `Write`. They reported no MCP servers. MCP connects external tools to an agent. Neither `Agent` nor `Task` appeared in the roster.

The trial handoff specifies fixture-only Edit/Write permission, file reads, and scoped local Git and test command allowances. It grants no alternate-model CLI launch. The saved startup records show tools and permission mode, but do not preserve the full launch permission configuration.

The supplied [launch record](2026-10-07-issue-8-reviewer-capability/launch-record.json) supplies arguments and completion outcomes for all six invocations. The orchestration thread recorded it after the original author inspected the streams. It records working directories, the skill source directory, input prompts, selected model, exact scoped command allowances, and normal `dontAsk` permissions without bypass flags. All six exit codes are 0. The baseline summaries record selected model `claude-opus-5-5`. The launch record supplies this selected model for all six sessions.

The launch record is supplied execution evidence, separate from provider startup metadata. It does not establish provider-confirmed identity or successful delivery. The source manifest records its original size, SHA-256 content hash, and provenance. The orchestration thread supplied this record but authored no product changes.

Every stream returns startup model `claude-opus-5-5`, the same assistant model value, and the same model usage key. This is native session evidence, separate from the selected-model claim. No reviewer model was dispatched. Model examples in final responses do not establish another model's availability or identity.

The original author task's native dispatch explicitly selected `gpt-6.1-sol`. This is dispatch evidence, not separately provider-confirmed identity. The original author made the trial evidence edits, local commit, and validation. A fresh author, also explicitly selected `gpt-6.1-sol`, made only the launch-record correction. The orchestrator runtime identity is unknown, and it authored no product changes. A fresh review with explicitly selected `gpt-6-astra` is planned after handoff. That review is not trial evidence or a completed review of this change.

## Observed actions and comparison

The bundle contains baseline, `repeat`, and `final` sessions at the unchanged skill revision. Terminal `success` records a returned response, not successful delivery.

| Session | Actual preparation and result | Exact final response |
|---|---|---|
| Dependent baseline | Resolved the skill, read the idea and fixture, and read express, review, authorization, and implementation guidance. Reported unavailable dispatch and different-model review before edits. | [Baseline](2026-10-07-issue-8-reviewer-capability/dependent-response.txt) |
| Dependent repeat | Resolved the skill and read the fixture, express guidance, authorization, and review rules. Proposed the trim operation and three test examples. Reported missing dispatch before edits. | [Repeat](2026-10-07-issue-8-reviewer-capability/dependent-repeat-response.txt) |
| Dependent final | Read the same task and review sources. Reported the local endpoint, proposed fix, and unavailable dispatch. No implementation, tests, commits, or PR preparation occurred. | [Final](2026-10-07-issue-8-reviewer-capability/dependent-final-response.txt) |
| Ordinary baseline | Read definition, authorization, evidence, fixture, writing, and research sources. Returned a draft with success conditions and limits. | [Baseline](2026-10-07-issue-8-reviewer-capability/ordinary-response.txt) |
| Ordinary repeat | Read definition and fixture sources. `git rev-parse HEAD && python3 -m unittest` returned the full fixture revision and one passing test. Returned a draft. | [Repeat](2026-10-07-issue-8-reviewer-capability/ordinary-repeat-response.txt) |
| Ordinary final | Read definition and fixture sources and searched callers with Grep. Returned a draft and stated that tests were not executed. | [Final](2026-10-07-issue-8-reviewer-capability/ordinary-final-response.txt) |

No stream contains Edit or Write calls. All report zero spawned subagents. Dependent sessions named unavailable dispatch and different-model review before implementation. They researched current behavior and proposed tests without substituting self-review.

Ordinary sessions used define-issue without reviewer capability assessment or review-source reads. All returned drafts without implementation or publication. Their drafts differ about surrounding tabs and newlines. This record does not assess every draft decision.

## Confounds, next action, and scope

The baseline dependent `git -C … status --short --branch` denial was a harness mismatch in command allowances. The supplied launch record shows that repeat and final invocations added those exact harmless Git-read patterns. Dependent repeats did not retry that status form. Compound Bash reads still received denials, while file Read succeeded.

All dependent finals incorrectly describe Bash as unavailable and say that the first Bash command was denied. Their first Bash commands succeeded. The ordinary baseline and final also overstate shell restrictions. The ordinary repeat demonstrates that a scoped Git/test command succeeds. Denied compound commands do not prove that every constituent operation is unavailable.

General implementation dispatch was also absent, so this is not an isolated reviewer-only failure. No GitHub remote existed. Hosted publication, actual review, different-model dispatch, GitHub writes, and delivery recovery were not exercised.

The responses request dispatch and a different reviewer model, plus broader Bash permission than the evidence supports. The next action is authorized dispatch with a reviewer selected from recorded model evidence. Source research and preparation can continue through permitted tools. A remaining command denial requires a report of that specific command and permission.

The finals offer direct implementation as an alternative requiring explicit approval. They keep different-model review unmet. One final names Opus and Sonnet as examples only. No approval arrived and no alternative was executed. These offers authorize no permission or review-policy change.

Existing [express reviewer planning](../../references/tasks/express-issue.md#implement-and-review-locally), [review rules](../../references/shared/review.md#review-sources), and [authorization rules](../../references/shared/authorization.md#handoffs) already cover the observed dispatch limit. Existing [evidence rules](../../references/shared/evidence.md#reports) require accurate reports. The inaccurate shell claims do not demonstrate missing reviewer guidance. No skill change is justified by this trial.

Identity, authentication, repository and board access, and project check preparation remain for later trials. This increment adds no gate, diagnostic command, registry, scheduler, or account, permission, settings, or review-policy change. Issue #8 remains open.
