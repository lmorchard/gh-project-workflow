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

## Filing procedure

The [file-issue skill](../skills/file-issue/SKILL.md) comes from the [issue 861 filing trial](trials/2026-09-30-issue-843/filing.md). That trial created the issue, established its parent, added project membership, and changed its status. Read-back commands established the saved results.

The skill adds recovery guidance for failed or uncertain writes. The trial did not exercise those failures. This guidance is a design precaution, not a measured guarantee of safe retries.

The skill uses installed command help instead of a fixed command template. The trial used gh 2.101.0, which supports parent links and field-name edits. Other installed versions can require different commands.

## Implementation procedure

The [implement-issue skill](../skills/implement-issue/SKILL.md) adapts selected guidance from agent-sessions at commit `4379832`. Its sources are [plan](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/plan.md), [execute](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/execute.md), and [session setup](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/references/session-setup.md).

The draft retains planning against current code, isolated worktrees, baseline results, requirement-specific checks, and small changes. It also retains explicit reports of blocked work and enough information for another session to resume. Project rules determine the required tests and record format.

The [old PR phase](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/open_pr.md) supplies useful self-review questions. The new skill uses those questions before handoff. It does not import unconditional rebasing, pushes, PR creation, or merge decisions into implementation.

The [frozen-check reference](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/references/frozen-checks.md) explains why an implementer must not weaken tests to claim success. The new skill uses ordinary test review and explanations for changed assertions. It does not use freeze commits, read-only test files, or a separate validation system.

The old reference contradicts itself about small tasks. Its opening requires checks.md at every size, but its ceremony paragraph permits skipping that file. The new skill requires evidence without that fixed file contract.

The draft omits tier labels, marker requirements, write manifests, mandatory subagents, and a machine-readable merge verdict. It explicitly distinguishes self-review from independent review. Those omissions reduce machinery but do not preserve the old claim of independent verification.

This adaptation is a draft. Static validation cannot establish that it guides implementation well. A real trial on issue 861 remains the next test.

Les explicitly requested that the frozen-check scheme remain at a distance. It is deferred, not a planned layer to restore. Useful tests, diff review, and honest reports are the initial verification approach.

## PR submission and review

The new skills use the old [PR phase](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/open_pr.md) and [PR template](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/references/pr-body-template.md) as sources. They retain clear descriptions, explicit issue links, observed test results, and the distinction between local tests and hosted CI.

The [comment procedure](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/address_comments.md) distinguishes actual defects from disputed suggestions and unrelated work. The new review skill retains that assessment. It leaves code changes and thread resolution for a later task.

The old workflow separated an author from a reviewer. The new local fallback also requests a different recorded model. This is a project preference, not a measured guarantee of better review. Unknown model identity remains unknown, including for Copilot.

On 2026-09-30, installed gh help and [GitHub documentation](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review?tool=cli) supported requesting review with gh pr edit and @copilot. A request and a completed review are different states. Later pushes can require another request.

The new skills omit frozen checks, machine-readable verdict blocks, automatic rebasing, and driver write manifests. They also omit automatic repair loops and merge actions. Both skills pass static validation but still require a real trial.

## Earlier dev-session guidance

On 2026-09-30, we also read the local dev-session files under ~/.claude/skills/dev-session. The relevant sources were phases/pr.md and references/pr-body-template.md. These local sources have no pinned repository revision in this record.

We retained whole-diff inspection, attention to generated files and lockfiles, and descriptions that explain decisions. We also retained assessment of review findings before changes. Neither automatic acceptance nor automatic dismissal of bot comments is useful.

The older Copilot command names copilot-pull-request-reviewer directly. The installed gh interface instead documents @copilot for --add-reviewer. The new skill uses that interface and requires a read-back of review state.

The older procedure waits for an increase in inline comment count. That misses completed reviews with no inline comments and does not identify the reviewed commit. The new skill examines review records and keeps pending review separate from unavailable access.

We did not copy mandatory squashing, automatic rebasing, repeated force-pushing, or a fixed polling loop. We also did not copy the assumption that an assignee listing establishes review access. The actual request and saved review state provide better evidence.
