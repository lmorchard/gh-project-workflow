# gh-project-workflow

Use `ghflow` for Git and GitHub tasks in Claude Code, Codex, and OpenCode. An agent skill supplies reusable task instructions. This collection registers one skill and keeps each operation in a task reference.

## Setup

Keep a full checkout of this repository. Install personal symbolic links with:

```sh
python3 scripts/install-skill.py claude codex
```

A symbolic link points to the source checkout root. Source edits appear through the links without another installation.
The installer preserves correct links and refuses existing conflicting entries before it creates links.
It creates `~/.claude/skills/ghflow` and `~/.agents/skills/ghflow`.
OpenCode also discovers these compatible directories. See the [setup trial](docs/trials/2026-10-07-ghflow-setup.md) for tested discovery and limits.
If you use only OpenCode, run `python3 scripts/install-skill.py opencode` for its native personal directory.
Do not add a native OpenCode link when compatible links already expose `ghflow`.

For one target project, use `--project TARGET_PATH` with the agent names.
For an isolated personal installation trial, use `--home TEMP_HOME`.
These options change the link destinations, not agent authentication or configuration.
The installer does not remove older generic skill installations. Remove those links separately after you inspect their sources.
If you move the source checkout, replace its stale links manually. The installer refuses to overwrite them.

Start a new agent session in the target project. Request an operation explicitly:

> Use ghflow to define issue #123. Produce a draft only. Do not publish or implement.

> Use ghflow to deliver issue #123 through review follow-up.

> Use ghflow to review PR #456.

Read [ghflow](SKILL.md) for routing and dependency access.
The entry skill resolves the source checkout root and uses its absolute `cli/ghflow.py` path.
Commands preserve the target project's current directory.
It does not require the workflow checkout to be the current directory.

## Source access permissions

The agent needs access to the resolved source checkout, including `references/`, `docs/writing.md`, and `cli/ghflow.py`.
If the agent requests external directory access, permit that source checkout for this task.
A link does not grant tool permissions.
For Claude Code, `--add-dir SOURCE_CHECKOUT` includes that checkout in the session's allowed directories.
Codex's read-only sandbox allowed these dependency reads in the setup trial.

OpenCode prompts for external directory access by default.
For unattended sessions, merge this narrowly scoped rule into the target project's `opencode.json` after you inspect its existing rules:

```json
{
  "permission": {
    "external_directory": {
      "/ABSOLUTE/SOURCE_CHECKOUT/*": "allow"
    },
    "edit": {
      "/ABSOLUTE/SOURCE_CHECKOUT/*": "deny"
    }
  }
}
```

Replace both paths with the resolved source checkout.
This permits source access and blocks file-tool edits to it. Other tool permissions still apply.
The installer does not change agent permissions or write this configuration.
See [OpenCode permissions](https://opencode.ai/docs/permissions/#external-directories) for directory and tool rules.

## Operations

The entry skill selects these independently usable operations:

### Backlog Triage & Project Board Management

- [bundle-issues](references/tasks/bundle-issues.md) groups related issues into thematic initiatives under native GitHub parent issues labeled `theme`.
- [triage-issues](references/tasks/triage-issues.md) evaluates open issues against code and git history, applying triage labels and closing completed or obsolete items.
- [sweep-needs-input](references/tasks/sweep-needs-input.md) interactively resolves blocking product and architectural decisions with the user.
- [sweep-needs-definition](references/tasks/sweep-needs-definition.md) develops accepted issues into bounded, actionable specifications with concrete file targets and test criteria.
- [sweep-audit-closed](references/tasks/sweep-audit-closed.md) reviews and confirms autonomously closed issues with cited evidence.
- [sweep-prioritize](references/tasks/sweep-prioritize.md) assigns Priority (`P0`–`P3`) and Size (`XS`–`XL`) fields on the project board and re-sweeps deferred items.
- [curate-ready-queue](references/tasks/curate-ready-queue.md) audits board WIP limits and stages high-priority Backlog items into the `Ready` column.

### Single Issue Specification & Implementation

- [reconsider-issue](references/tasks/reconsider-issue.md) reassesses an existing issue against current project evidence.
- [decompose-parent-issue](references/tasks/decompose-parent-issue.md) maps a broad issue into bounded children and a parent completion condition.
- [define-issue](references/tasks/define-issue.md) prepares and reviews an issue draft.
- [interview-issue](references/tasks/interview-issue.md) resolves decisions with the user.
- [file-issue](references/tasks/file-issue.md) publishes a reviewed draft and confirms the requested GitHub changes.
- [implement-issue](references/tasks/implement-issue.md) produces tested, committed changes for PR preparation.
- [review-changes](references/tasks/review-changes.md) assesses changes in a fresh reviewer context without editing them.
- [submit-pr](references/tasks/submit-pr.md) publishes committed work and requests a review; for an agent pull request, independent local review is the primary source and the user may request Copilot review.
- [address-pr-review](references/tasks/address-pr-review.md) waits for requested review, addresses findings, and repairs failing CI on an existing PR.
- [merge-pr](references/tasks/merge-pr.md) confirms CI and review findings, merges authorized changes, and confirms the result.

### Workflow Coordinators

- [express-issue](references/tasks/express-issue.md) coordinates one selected issue through delivery to an agreed endpoint.
- [deliver-parent-issue](references/tasks/deliver-parent-issue.md) coordinates a bounded parent through child delivery and completion checks.
- [burndown-ready-queue](references/tasks/burndown-ready-queue.md) coordinates the sequential delivery of issues staged in the project board's `Ready` column.

Each operation accepts an ordinary issue or PR. References share [authorization and evidence rules](references/shared).
Delivery through review follow-up leaves the PR open. Merge requires explicit authorization and the existing review policy.

## Requirements

Install Git, Python 3, and GitHub CLI (`gh`) in the agent environment.
Keep a local checkout of the target project for code investigation.
The standard-library CLI in [cli/ghflow.py](cli/ghflow.py) handles repeatable operations.
It uses existing Git and `gh` commands for other work.

Configure the machine account through [Agent identity](references/shared/identity.md) before subagents run Git or GitHub commands.
The account needs access to the target repository. Board operations also need writer access to the selected project.
Do not change accounts to work around access failures.

Coordinated delivery requires subagent dispatch. Independent code review requires a fresh reviewer context and a different recorded model from the implementer.
Report unavailable dispatch or model information. Self-review does not replace independent review.
Direct operations remain usable without a coordinator, subject to their own requirements and boundaries.

## Checks

Run `make check` before you commit. It validates skill frontmatter, local Markdown links, and whitespace. It does not assess skill quality.

## Project documents

Read these documents:

- [Project direction](docs/direction.md) records decisions and open questions.
- [Findings from agent-sessions](docs/findings.md) records lessons and their sources.
- [First experiment](docs/first-experiment.md) describes the issue-definition trial.
- [Issue interviews](docs/issue-interview.md) explains how review questions return to the user conversation.
- [Skill sources](docs/skill-sources.md) records ideas adapted from agent-sessions.
- [Trial records](docs/trials/README.md) lists the trials of the skills on real issues.
- [Skill scenarios](evals/README.md) checks whether agents make the decisions that the skills intend.
- [Writing rules](docs/writing.md) describes the ASD-STE100 trial for documents and issues.
- [Skill style](docs/skill-style.md) describes how to write and revise skills.

The separate agent-sessions repository remains a reference. We will bring useful ideas into this project one at a time.
