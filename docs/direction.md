# Project direction

This document records the discussion with Les on 2026-09-30. The project will help a person and an agent take an idea through code review and merge. A merge adds approved changes to a target branch.

## Why start separately

In agent-sessions, the workflow grew into Bash scripts and then a Python program that controlled agents. Tools for repeatable operations produced useful results. Les questioned whether automatic control became the main concern before individual tasks were useful enough.

This concern motivates the new project. We did not measure which approach is better. A separate repository lets us reconsider the design and keep agent-sessions as a reference.

## Agreed direction

An agent skill supplies instructions to an agent. A command-line interface (CLI) accepts commands as text. This project will pair a skill with a CLI for repeatable operations.

The tasks include issue definition, issue creation, project boards, code changes, pull request review, and merge. A pull request (PR) proposes changes for review. Each task must be useful before we combine it with other tasks.

We will record findings first. We will not copy the entire old skill or its control program. The first useful tool does not require all phases of the workflow.

## Agent and CLI responsibilities

The agent interprets requests, defines scope, chooses actions, changes code, and assesses review findings. The CLI accepts explicit inputs and does a specified operation. It returns facts and the result of the operation.

Possible operations include issue reads, PR reads, workspace creation, issue updates, board updates, PR creation, and requested merges. These are proposals. We did not select command names.

The initial CLI will not call a model, select the next issue, or infer human approval. It will not select the next phase. Existing git and gh commands remain available.

The old control program gave the agent read-only GitHub credentials. Separate code made the requested changes with other credentials. Instructions alone cannot enforce that restriction.

This project initially relies on permissions in the agent application and authorization from the user. Stronger restrictions for unattended use require a separate design. A skill does not replace those restrictions.

## Development sequence

Use this sequence:

1. Make one operation useful by itself.
2. Use the operation and skill instructions to do one real task.
3. Try the task in a new session to find missing information.
4. Combine steps when repeated use shows a benefit.

Each phase must accept an ordinary existing issue or PR. Earlier tasks do not need this system. Use GitHub records and Git history to leave information for the next session where possible.

## Keep the process useful

Les observed that agent-sessions sought less documentation ceremony but introduced new ceremonies along the way. Ceremony means required steps or records that add little practical value. A simpler workflow can become complex again through individually reasonable additions.

A required document or step must help someone make a decision, do the task, or continue it later. Use an existing issue, commit, or test result when it supplies that information. Do not require another record merely to prove that the process occurred.

Keep trial records when they answer a real question about a skill. Do not turn the records from these first experiments into mandatory files for every task. Remove or combine steps when actual use shows that they duplicate effort.

This principle does not require another checklist, approval, or report. Judge the process by the useful work it supports and the effort it requires.

## Proposed design principles

These principles are proposals for the first experiments. They describe desired behavior, not implemented features. Real use will supply evidence for changes.

We propose that tools distinguish missing data, pending activity, and failed requests. A result must not show success when a request failed. When a change succeeds, the tool reports what changed.

We propose that tools use expected versions or commit identifiers to detect changes after a read, where supported. A commit records a version of files in Git. Its identifier names that version.

We propose that retries do not create duplicate changes where prevention is possible. If only some steps succeed, the tool reports those steps. It does not claim that all steps succeeded or that none took effect.

We propose separate decisions about task readiness, evidence, and permission. Plans and test records can be as short as the task permits. A favorable review does not itself authorize a merge.

## Open decisions

We selected issue definition for the first skill trial. The [First experiment](first-experiment.md) describes the task and evaluation. The CLI language, package format, command names, and first CLI operation remain open.

Automatic scheduling, background polling, custom session storage, attempt labels, and a special merge-result format remain outside the initial effort. Les also requested an ASD-STE100 trial. The [Writing rules](writing.md) describe that trial and its limits.

## Implementation scope

Les requested an implementation skill that uses ordinary development practices. It will plan against current code, use an isolated worktree, add useful tests, review changes, and report results. The skill ends with local commits for PR preparation.

The frozen-check scheme from agent-sessions is deferred. This project does not plan to restore freeze commits, locked test files, or a separate validation system. Any later proposal for such machinery requires evidence of a problem that ordinary tests and review do not address.

## Interactive issue review

Les prefers interviews and interactive questions to reviewing draft files. The agent explains its findings and recommendation in the conversation. It asks focused questions about decisions that need user judgment, then updates the draft itself.

Draft files support the conversation but are not required reading for approval. Before requesting publication permission, the agent summarizes the concrete changes. Existing decisions and permissions remain valid within their scope. Les wants an agreed issue-preparation flow to continue through publication without separate approval at every skill boundary. Explicit draft-only limits still apply. Product questions remain interactive; a change of skill alone is not a reason to stop.

## Review approach

PR submission will request Copilot review when available. If access is unavailable, the parent can dispatch a local reviewer in a fresh context. The local reviewer must use a different model from the implementer for this fallback.

The parent records model identities from available session or dispatch information. If identity or model selection is unavailable, it reports the limit. A same-model second opinion does not silently replace the requested different-model review.

Copilot is an external review service, but its underlying model can be unknown. We do not claim model diversity without evidence. This preference does not replace tests, human judgment, or review of the actual findings.

The independent reviewer reports findings without changing code. Submission publishes the PR and requests review. The separate address-pr-review task waits up to 20 minutes and addresses available findings. A further review after corrections remains pending unless another cycle is requested.

No fixed report files are required. None of these tasks merges the PR. A timeout remains an incomplete review, not approval.

PR follow-up also watches hosted CI for the current commit. It corrects failures and repeats checks until CI passes or a concrete blocker requires user action. The review deadline does not limit CI repair or turn missing checks into success.

## Merge policy

Les requires green CI and prefers Copilot review. A literal approving review is not required by this workflow. The agent often submits PRs as the user, and GitHub does not let authors approve their own PRs.

Green CI alone does not permit an autonomous merge. The agent also needs affirmative review evidence within existing merge authorization, or explicit user permission to merge the PR.

A favorable review can come from a person, Copilot, or an independent local reviewer. A COMMENTED review can qualify if its text recommends approval or clearly reports a completed review with no findings. Silence, an empty comment list, and a review timeout do not qualify.

Permission to implement or submit does not imply permission to merge. Existing explicit merge permission remains valid within its scope, so the agent does not need to ask again. Unresolved defects, human objections, and repository protection rules still require attention.

Merge uses explicit user authorization and checks the current commit. It does not bypass GitHub rules or weaken checks. The result includes confirmed merge, issue, and board state.

## Future agent identity

Les reported that agent-sessions tried a second GitHub account and later a GitHub App for agent contributions. A separate identity would distinguish agent actions from Les's actions in GitHub records. It could also let Les review contributions as a separate person.

We may return to this approach after the individual tasks work well. First inspect the earlier work for useful parts and limits. Then define the permissions and account setup that this project needs. This is a future option, not a requirement for the current skills.

## Possible next-task guidance

Les proposed a skill that helps answer “what is next?” after using the individual skills. One possible starting point is advice based on the current issue or PR, available evidence, unresolved decisions, and existing authorization. It can explain which task fits and why.

Automatic dispatch remains an open design choice. A recommendation does not grant permission to publish, implement, or merge. We will use the current trials to identify useful conditions before defining this skill. This proposal does not add a scheduler or require every task to pass through a fixed sequence.
