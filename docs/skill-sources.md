# Sources for the issue definition skill

The draft adapts selected ideas from agent-sessions at commit `4379832`. It does not copy the old workflow. These notes separate inherited guidance from new choices.

## Research instructions

The [documentarian prompt](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/references/documentarian-prompt.md) separates descriptions of current code from proposed changes. It requests file and line references, neutral questions, existing tests, and other callers of shared code.

The new [research guide](../skills/define-issue/references/research.md) retains those ideas. It removes the fixed question count and mandatory research file. It also distinguishes a limited search from proof that a feature does not exist.

## Issue content and readiness

The [specification template](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/references/spec-template.md) supplies useful content categories. These include the goal, current behavior, success conditions, scope limits, decisions, and open questions.

The new skill uses these facts without a fixed template. It does not require tier labels, a special heading format, or failing tests before issue definition. Readiness for implementation remains separate from permission for unattended execution.

## Evidence and success conditions

The [acceptance criteria guide](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/references/acceptance-criteria.md) distinguishes new behavior from protection of existing behavior. It also asks whether a check can pass without the intended change.

The new skill retains those distinctions. A proposed test remains a proposal until it exists and someone executes it. Human judgment can be a valid assessment method when the issue states what the person must assess.

## Limits

The old findings contain evidence about some instructions in their original context. That evidence does not establish the effectiveness of this adaptation. The fresh-agent trial will supply one observation, not a general reliability measure.
