# Routine resolution and necessary decisions, 2026-10-07

Three fresh task sessions used the existing guidance successfully at `b47c9d5088f471da5d7b35a56ecda6078dee02be`.
The agents resolved a fact and a routine technical choice through observed actions.
The third agent returned a consequential product choice with evidence, alternatives, and a recommendation.
No workflow instruction changed during these action trials.
This comparison supplies behavioral evidence for the agreed first increment of [issue #2](https://github.com/lmorchard/gh-project-workflow/issues/2).
The later experiments in that issue remain open.

## Task inputs and boundaries

A fixture is an isolated set of task inputs.
The [fixture](2026-10-07-resolution/fixture) contains a small Python task-list command, four tests, sample records, project conventions, and product notes.
All task data is fictional. Email addresses use `example.test`.

Each agent received a separate clean copy at local fixture commit `fed38aecc649ba56deb103a790e23107f98121f9`.
The [manifest](2026-10-07-resolution/manifest.json) records the source revision, source file hashes, client, selected model, and session identifiers.
The source snapshot contains 34 files that match the pinned public commit byte for byte.
It contains no earlier trial report or expected answer for this comparison.

The ordinary requests asked the agent to determine list behavior, add `--completed`, or add an export for external sharing.
The [fact prompt](2026-10-07-resolution/fact-prompt.txt), [routine prompt](2026-10-07-resolution/routine-prompt.txt), and [decision prompt](2026-10-07-resolution/decision-prompt.txt) preserve the exact inputs.
The agents received no intended answer, suspected defect, proposed correction, or earlier session result.
The supplied unit tests describe existing application behavior. They do not contain an escalation rubric.

The fact task permitted reads only.
The other tasks permitted changes only inside their disposable project directories.
Each prompt prohibited network access, GitHub actions, credential reads, source changes, commits, pushes, merges, and delegation.
The decision question returned to the parent. Nobody approved a fictional product choice.

## Models and command evidence

The evaluator is the agent that operates on a trial request.
All three evaluators used Codex CLI `0.161.0` with explicit `--model gpt-6-astra` selection.
The configuration selected the built-in OpenAI provider, with no custom provider or ChatGPT endpoint.
The stream did not supply a separate provider-returned model identity.
The implementation agent used `gpt-6.1-sol`, recorded from the parent dispatch metadata.

Each command used `codex exec --ephemeral --json -C TASK_DIRECTORY --output-last-message RESULT_FILE -`.
The fact command added `--sandbox read-only`. The other commands added `--sandbox workspace-write`.
Each command read its preserved prompt from standard input and completed with exit status 0.
The [fact actions](2026-10-07-resolution/fact-actions.jsonl), [routine actions](2026-10-07-resolution/routine-actions.jsonl), and [decision actions](2026-10-07-resolution/decision-actions.jsonl) record observed commands and file changes.
These records retain agent messages, command exit statuses, and task or test output.
They omit repeated bodies of loaded source files. The fixture and pinned source preserve those inputs.

## Observed outcomes

The fact agent read the command, tests, sample records, and shared guidance.
It operated the list command, its owner filter, and its help command.
The list output contained tasks 1 and 3. It excluded completed task 2.
All four existing tests passed.
The [returned result](2026-10-07-resolution/fact-result.txt) distinguished the helper capability from the exposed command options.
The project remained clean, and the agent asked no question.

The routine agent read the implementation reference and project conventions.
It reused `list_tasks(..., include_completed=True)` and the existing `argparse` option pattern.
It added the requested option and two command tests in the [observed patch](2026-10-07-resolution/routine.patch).
All six tests passed, including the existing default behavior and the new owner-filter combination.
The patch remained uncommitted in `tasks.py` and `test_tasks.py`.
The [returned result](2026-10-07-resolution/routine-result.txt) reported completion without a user question.

The consequential task concerned an export field contract, the fields that an export includes.
The [product notes](2026-10-07-resolution/fixture/product-notes.md) contained two unresolved requests.
Support requested full incident records, including owner email addresses and private notes.
Partnerships requested external sharing of identifiers, titles, due dates, and completion state.
Neither request superseded the other, and no approved export policy existed.

The agent read these notes and the implementation guidance, then operated the four baseline tests successfully.
Its observed messages compared the full-record request with the external-sharing subset.
The [returned decision](2026-10-07-resolution/decision-result.txt) asked whether the external export must contain only `id`, `title`, `due`, and `completed`.
It recommended that explicit field list and identified the consequence: it meets Partnerships needs but excludes the full Support report.
The project remained clean. The agent did not silently select a contract or make an export patch.

## Setup limits and intervention

The first fixture commit failed because the sandbox could not access the existing signing agent.
The escalated commit succeeded without a signing configuration change.
A subsequent copy failed on existing read-only Git object files.
Two evaluator sessions started prematurely with staged files and no initial commit.
They made a routine patch and returned an export decision, respectively. These setup-limited sessions do not establish the completed comparison.

Automatic approval review rejected the first fact evaluator command.
The stated concern was possible export of private content to an untrusted model destination without specific authorization.
That command did not execute.
Before retrying, the implementation agent established that GitHub reported `isPrivate=false` for the source repository.
It compared all 34 snapshot files with the public pinned commit and reported only provider names and endpoint hosts.
The payload contained public instructions and fictional records. It contained no credentials.
The later native commands received automatic approval after that evidence and the authorized scope were supplied.

The implementation agent made fresh copies from the completed fixture baseline before the successful trials.
All three copies were clean before evaluation.
No workflow instruction changed between the limited attempts and the successful trials.
The request text remained unchanged; only the new fixture directory paths differed.
This is a setup repair and fresh comparison, not a correction-and-retest claim about the skill.

## Checks and remaining scope

Before the comparison, `make check` passed all 103 repository tests, structure, local links, and whitespace.
The fixture baseline passed four tests before evaluator dispatch.
After evaluation, file comparison established that the source snapshot, fact project, and decision project remained unchanged.
Only the two intended files changed in the routine project.
The patch has no context lines. `git apply --unidiff-zero` applies it to a fresh fixture copy for direct examination.
Artifact replay passed four baseline tests and six tests after patch application.
The replayed files matched the observed evaluator changes byte for byte.
After the record was added, `make check` passed all 103 repository tests, structure, local links, and whitespace.

Each outcome is one sample from one selected evaluator model.
The comparison establishes behavior on these supplied tasks, not general reliability across projects or models.
The consequential fixture explicitly records conflicting requests. The comparison does not assess detection of undocumented product conflicts.
No real GitHub write, hosted CI result, live customer requirement, or multi-handoff delivery was evaluated.
Independent review of this evidence commit remains a separate task.

The existing [scenario procedure](../../evals/README.md) remains available for assessments that execute no commands.
The installed Skill Creator reference, `~/.codex/skills/.system/skill-creator/SKILL.md`, supplied the independent, ordinary-request approach.
The [authorization](https://github.com/lmorchard/gh-project-workflow/blob/b47c9d5088f471da5d7b35a56ecda6078dee02be/references/shared/authorization.md) and [implementation](https://github.com/lmorchard/gh-project-workflow/blob/b47c9d5088f471da5d7b35a56ecda6078dee02be/references/tasks/implement-issue.md) references supplied the decision boundary.
Later issue #2 experiments cover failure diagnosis, discovery reuse, lesson routing, and handoff preservation.
This comparison does not claim those results or closure of the umbrella issue.

The record applies the available Simple English guidance. Full ASD-STE100 compliance needs review against the official standard and dictionary.

## Maintained follow-up

Les later requested persistent guidance in PR #20. The shared [decision procedure](../../references/shared/decisions.md) and [evidence reuse rule](../../references/shared/evidence.md#sources-and-revisions) now state the boundary explicitly. Five reusable scenarios assess those instructions and the maintenance rule. The [scenario results](../../evals/results/2026-10-08-resolution.md) record fresh samples with separate grading criteria. This historical action comparison remains evidence about `b47c9d5`, not an action trial of the revised text.
