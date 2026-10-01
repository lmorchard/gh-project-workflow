# Project direction

Captured from the founding discussion with Les on 2026-09-30.

The purpose is to help a person and an agent move work from an idea to a reviewed, merged change. The project should help with individual tasks before we build a system that chooses and runs tasks unattended.

## Why start separately

In agent-sessions, the workflow grew into Bash scripts and then a Python harness. Moving repeatable operations into tools produced useful wins. The concern is that running the whole workflow unattended became the main design concern before the individual phases and operations were sufficiently useful on their own.

This concern motivates the experiment. We have not measured which approach works better. A sibling repository gives us room to reconsider commands and workflow assumptions while retaining the predecessor as evidence and reference.

## Agreed direction

Pair an agent skill with a CLI utility. Let the skill guide judgment and let code carry out repeatable operations reliably. Build and try individual operations and phases before combining them. Capture findings first; avoid copying the whole existing skill or the code that runs it.

The lifecycle in scope includes defining and filing issues, managing project boards, implementing PRs, reviewing PRs, and merging PRs. This is a list of useful tasks, not a requirement to implement all phases before delivering value.

## Responsibility boundary

The agent interprets intent, clarifies scope, chooses actions, implements changes, and evaluates substantive review findings. The CLI accepts explicit inputs, performs a specific operation, and returns facts and confirmed results.

Potential CLI responsibilities include collecting complete issue or PR context, preparing a worktree, preserving issue text during updates, looking up board field identifiers, publishing a PR, and checking the required conditions before performing a requested merge. These are candidates, not committed subcommand names.

The CLI should not call a model, select the next issue, infer human approval, or decide which phase runs next. Those features are outside the initial effort. Existing git and gh commands remain available; a wrapper should earn its place by eliminating repeated coordination or a demonstrated failure mode.

The old driver limited what the agent could change. It gave the agent read-only GitHub credentials and used separate code to perform writes. Instructions alone cannot enforce that restriction. This project initially relies on the agent application's permissions and the user's authorization. Stronger restrictions for unattended use would need a separate design.

## Development sequence

1. Make one operation reliable and useful independently.
2. Pair operations with enough skill guidance to complete one real phase.
3. Exercise handoffs in fresh sessions and discover what information is actually needed.
4. Combine steps when repeated use shows that doing so would help.

Each phase should be able to start from an ordinary existing issue or PR. It should not require that all preceding work passed through this system. Use issues, branches, commits, PRs, and board fields to leave information for the next session where possible.

## Proposed design principles

These principles guide the first experiments; their exact behavior remains to be tested.

- Return structured facts and actionable errors. Distinguish absence, pending work, and failed retrieval.
- Make changes explicit and check that they succeeded. Where supported, use expected versions or commit IDs to detect changes since the last read.
- Make retries safe where possible. Report partial completion rather than claiming that every step succeeded or that none took effect.
- Keep readiness to implement, verification strength, and authorization distinct.
- Keep plans and check results only as detailed as the task needs. Keep useful evidence without requiring all the old workflow's files and steps.
- Treat a merge as an authorized action with current evidence, rather than an automatic consequence of an agent's favorable verdict.

## Decisions still open

The implementation language, packaging, command names, initial operation, and installable skill structure are not selected. Define, triage, implement, review, and merge are candidate entry points, not a fixed set of skill commands.

A proposed first experiment is documented separately in [First experiment](first-experiment.md). There is no commitment to a scheduler, background polling loop, custom session store, attempt labels, or a special format for reporting merge decisions.

## Writing style

Use simple technical English. Les identified increasingly intricate jargon as a failing of agent-sessions. Describe the action, the information it needs, and the result in ordinary words. Keep necessary technical terms, explain unfamiliar ones, and avoid inventing names for concepts that a short sentence can explain.
