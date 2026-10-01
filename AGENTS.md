# Instructions for agents

Before you propose a design, read [Project direction](docs/direction.md). Before you copy code or instructions from agent-sessions, read [Findings](docs/findings.md). The instructions in agent-sessions do not apply to this repository.

## Development

Start with an operation that is useful by itself. A phase is a task such as an issue definition or a PR review. Combine operations into phases after real use shows their value.

Do not add automatic task selection without evidence of a need and an explicit project decision. Use existing git and gh commands when they are sufficient. Add a tool when it removes a repeated procedure or a known cause of errors.

Keep decisions separate from proposals. Give a source for each lesson or code section that you copy. Select a language and command names when a specific task supplies enough information.

## Parent and trial agent roles

The parent agent develops skills with Les and evaluates their trials. It can edit this workflow repository and inspect subject repositories for research. A subject repository is a project used to try the skills.

Subagents perform subject-repository tasks through the relevant skills. This includes code changes, commits, pushes, issue and board updates, PR submission, review replies, merges, and cleanup. The parent must not perform those actions directly merely because the user authorized the task.

Give each subagent the skill, necessary inputs, and the authorized scope. Return decisions that need user judgment to the parent conversation. The parent reviews results and improves the skills without silently completing missing subject-repository actions itself.

If a skill is incomplete, revise it here and let a subagent continue the task. If delegation is unavailable, report that limit. Only an explicit user exception permits the parent to act directly in the subject repository.

## Authorization across issue tasks

Les wants an agreed issue-preparation flow to continue through research, interviews, draft review, and publication without approval at every skill boundary. Carry that authorization and its limits into each subagent handoff. Once decisions are settled, publish the reviewed result within the agreed scope and report it.

An explicit draft-only or read-only request still limits the work. Ask about unresolved product decisions or actions beyond the agreed scope, not merely because the next skill changes. Issue preparation does not authorize implementation or merge. Keep the existing merge policy.

## Writing

Use [Writing rules](docs/writing.md) for documents and specifications. This project is trying ASD-STE100 with the available simple-english skill. Do not claim full compliance without a review against the official standard and dictionary.

Keep facts, command names, identifiers, and quoted errors unchanged. Define necessary technical terms at first use. Do not invent terms when ordinary words are sufficient.
