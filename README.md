# gh-project-workflow

This project will pair an agent skill with a command-line interface (CLI) for Git and GitHub tasks. An agent skill is a set of instructions for an agent. A CLI accepts commands as text.

The tasks include issues, project boards, code changes, pull requests (PRs), and merges. A pull request proposes changes for review. A merge adds approved changes to a target branch.

Start with one useful operation. Then use operations to do a task, such as a PR review. Combine tasks only after real use shows a benefit.

The repository contains draft [define-issue](skills/define-issue/SKILL.md) and [interview-issue](skills/interview-issue/SKILL.md) skills. We did not select a CLI language or command names. The CLI is not implemented.

Read these documents:

- [Project direction](docs/direction.md) records decisions and open questions.
- [Findings from agent-sessions](docs/findings.md) records lessons and their sources.
- [First experiment](docs/first-experiment.md) describes the issue-definition trial.
- [Issue interviews](docs/issue-interview.md) explains how review questions return to the user conversation.
- [Skill sources](docs/skill-sources.md) records ideas adapted from agent-sessions.
- [Trial results](docs/trials/2026-09-30-issue-843/review.md) records the first use of the skill.
- [Writing rules](docs/writing.md) describes the ASD-STE100 trial.

The separate agent-sessions repository remains a reference. We will bring useful ideas into this project one at a time.
