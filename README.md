# gh-project-workflow

This project will pair an agent skill with a command-line interface (CLI) for Git and GitHub tasks. An agent skill is a set of instructions for an agent. A CLI accepts commands as text.

The tasks include issues, project boards, code changes, pull requests (PRs), and merges. A pull request proposes changes for review. A merge adds approved changes to a target branch.

Start with one useful operation. Then use operations to do a task, such as a PR review. Combine tasks only after real use shows a benefit.

The repository contains these skills, organized by lifecycle stage:

### Backlog Triage & Project Board Management
- [bundle-issues](skills/bundle-issues/SKILL.md) groups related issues into thematic initiatives under native GitHub parent issues labeled `theme`.
- [triage-issues](skills/triage-issues/SKILL.md) evaluates open issues against code and git history, applying triage labels and closing completed or obsolete items.
- [sweep-needs-input](skills/sweep-needs-input/SKILL.md) interactively resolves blocking product and architectural decisions with the user.
- [sweep-needs-definition](skills/sweep-needs-definition/SKILL.md) develops accepted issues into bounded, actionable specifications with concrete file targets and test criteria.
- [sweep-audit-closed](skills/sweep-audit-closed/SKILL.md) reviews and confirms autonomously closed issues with cited evidence.
- [sweep-prioritize](skills/sweep-prioritize/SKILL.md) assigns Priority (`P0`–`P3`) and Size (`XS`–`XL`) fields on the project board and re-sweeps deferred items.
- [curate-ready-queue](skills/curate-ready-queue/SKILL.md) audits board WIP limits and stages high-priority Backlog items into the `Ready` column.

### Single Issue Specification & Implementation
- [reconsider-issue](skills/reconsider-issue/SKILL.md) reassesses an existing issue against current project evidence.
- [decompose-parent-issue](skills/decompose-parent-issue/SKILL.md) maps a broad issue into bounded children and a parent completion condition.
- [define-issue](skills/define-issue/SKILL.md) prepares and reviews an issue draft.
- [interview-issue](skills/interview-issue/SKILL.md) resolves decisions with the user.
- [file-issue](skills/file-issue/SKILL.md) publishes a reviewed draft and confirms the requested GitHub changes.
- [implement-issue](skills/implement-issue/SKILL.md) produces tested, committed changes for PR preparation.
- [review-changes](skills/review-changes/SKILL.md) assesses changes in a fresh reviewer context without editing them.
- [submit-pr](skills/submit-pr/SKILL.md) publishes committed work and requests Copilot review.
- [address-pr-review](skills/address-pr-review/SKILL.md) waits for requested review, addresses findings, and repairs failing CI on an existing PR.
- [merge-pr](skills/merge-pr/SKILL.md) confirms CI and review findings, merges authorized changes, and confirms the result.

### Workflow Coordinators
- [express-issue](skills/express-issue/SKILL.md) coordinates one selected issue through delivery to an agreed endpoint.
- [deliver-parent-issue](skills/deliver-parent-issue/SKILL.md) coordinates a bounded parent through child delivery and completion checks.
- [burndown-ready-queue](skills/burndown-ready-queue/SKILL.md) coordinates the sequential delivery of issues staged in the project board's `Ready` column.

Each task skill can be used by itself on an ordinary issue or PR. Skills link to shared references in [skills/shared](skills/shared/) for authorization, evidence, review, and board-status rules, so use them from a full checkout of this repository. The first CLI operation is `pr-state` in [cli/ghflow.py](cli/ghflow.py), a standard-library Python script that uses `gh`. The [CLI decision](docs/direction.md#cli-decision) lists the planned operations. Command names are provisional.

## Requirements

GitHub operations require GitHub CLI (`gh`) in the agent environment. Install `gh` and sign in with `gh auth login`. Use `gh auth status` to make sure that authentication succeeds.

The account must have access to the target repository. Project-board operations also require access to the target project. Authentication alone does not grant permission to change issues or board items.

Code investigation requires Git and a local checkout of the target project. The skills currently use existing `git` and `gh` commands. The planned project CLI does not replace these requirements.

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
