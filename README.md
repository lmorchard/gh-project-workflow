# gh-project-workflow

This project will pair an agent skill with a command-line interface (CLI) for Git and GitHub tasks. An agent skill is a set of instructions for an agent. A CLI accepts commands as text.

The tasks include issues, project boards, code changes, pull requests (PRs), and merges. A pull request proposes changes for review. A merge adds approved changes to a target branch.

Start with one useful operation. Then use operations to do a task, such as a PR review. Combine tasks only after real use shows a benefit.

The repository contains these draft skills:

- [define-issue](skills/define-issue/SKILL.md) prepares and reviews an issue draft.
- [interview-issue](skills/interview-issue/SKILL.md) resolves decisions with the user.
- [file-issue](skills/file-issue/SKILL.md) publishes a reviewed draft and confirms the requested GitHub changes.

Each skill can be used by itself. We did not select a CLI language or command names. The CLI is not implemented.

## Requirements

GitHub operations require GitHub CLI (`gh`) in the agent environment. Install `gh` and sign in with `gh auth login`. Use `gh auth status` to make sure that authentication succeeds.

The account must have access to the target repository. Project-board operations also require access to the target project. Authentication alone does not grant permission to change issues or board items.

Code investigation requires Git and a local checkout of the target project. The skills currently use existing `git` and `gh` commands. The planned project CLI does not replace these requirements.

## Project documents

Read these documents:

- [Project direction](docs/direction.md) records decisions and open questions.
- [Findings from agent-sessions](docs/findings.md) records lessons and their sources.
- [First experiment](docs/first-experiment.md) describes the issue-definition trial.
- [Issue interviews](docs/issue-interview.md) explains how review questions return to the user conversation.
- [Skill sources](docs/skill-sources.md) records ideas adapted from agent-sessions.
- [Trial results](docs/trials/2026-09-30-issue-843/review.md) records the first use of the skill.
- [Writing rules](docs/writing.md) describes the ASD-STE100 trial.

The separate agent-sessions repository remains a reference. We will bring useful ideas into this project one at a time.
