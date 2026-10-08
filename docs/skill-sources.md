# Sources for the issue definition skill

The draft adapts selected ideas from agent-sessions at commit `4379832`. It does not copy the old workflow. These notes separate inherited guidance from new choices.

## Research instructions

The [documentarian prompt](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/references/documentarian-prompt.md) separates descriptions of current code from proposed changes. It requests file and line references, neutral questions, existing tests, and other callers of shared code.

The new [research guide](../references/tasks/research.md) retains those ideas. It removes the fixed question count and mandatory research file. It also distinguishes a limited search from proof that a feature does not exist.

## Issue content and readiness

The [specification template](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/references/spec-template.md) supplies useful content categories. These include the goal, current behavior, success conditions, scope limits, decisions, and open questions.

The new skill uses these facts without a fixed template. It does not require tier labels, a special heading format, or failing tests before issue definition. Readiness for implementation remains separate from permission for unattended execution.

## Evidence and success conditions

The [acceptance criteria guide](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/references/acceptance-criteria.md) distinguishes new behavior from protection of existing behavior. It also asks whether a check can pass without the intended change.

The new skill retains those distinctions. A proposed test remains a proposal until it exists and someone executes it. Human judgment can be a valid assessment method when the issue states what the person must assess.

## Limits

The old findings contain evidence about some instructions in their original context. That evidence does not establish the effectiveness of this adaptation. The fresh-agent trial will supply one observation, not a general reliability measure.

## Filing procedure

The [file-issue skill](../references/tasks/file-issue.md) comes from the [issue 861 filing trial](trials/2026-09-30-issue-843/filing.md). That trial created the issue, established its parent, added project membership, and changed its status. Read-back commands established the saved results.

The skill adds recovery guidance for failed or uncertain writes. The trial did not exercise those failures. This guidance is a design precaution, not a measured guarantee of safe retries.

The skill uses installed command help instead of a fixed command template. The trial used gh 2.101.0, which supports parent links and field-name edits. Other installed versions can require different commands.

## Implementation procedure

The [implement-issue skill](../references/tasks/implement-issue.md) adapts selected guidance from agent-sessions at commit `4379832`. Its sources are [plan](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/plan.md), [execute](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/execute.md), and [session setup](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/references/session-setup.md).

The draft retains planning against current code, isolated worktrees, baseline results, requirement-specific checks, and small changes. It also retains explicit reports of blocked work and enough information for another session to resume. Project rules determine the required tests and record format.

The [old PR phase](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/open_pr.md) supplies useful self-review questions. The new skill uses those questions before handoff. It does not import unconditional rebasing, pushes, PR creation, or merge decisions into implementation.

The [frozen-check reference](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/references/frozen-checks.md) explains why an implementer must not weaken tests to claim success. The new skill uses ordinary test review and explanations for changed assertions. It does not use freeze commits, read-only test files, or a separate validation system.

The old reference contradicts itself about small tasks. Its opening requires checks.md at every size, but its ceremony paragraph permits skipping that file. The new skill requires evidence without that fixed file contract.

The draft omits tier labels, marker requirements, write manifests, mandatory subagents, and a machine-readable merge verdict. It explicitly distinguishes self-review from independent review. Those omissions reduce machinery but do not preserve the old claim of independent verification.

Static validation cannot establish that this adaptation guides implementation well. The [Trial records](trials/README.md) list the implementation trials.

Les explicitly requested that the frozen-check scheme remain at a distance. It is deferred, not a planned layer to restore. Useful tests, diff review, and honest reports are the initial verification approach.

## PR submission and review

The new skills use the old [PR phase](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/open_pr.md) and [PR template](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/references/pr-body-template.md) as sources. They retain clear descriptions, explicit issue links, observed test results, and the distinction between local tests and hosted CI.

The [comment procedure](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/address_comments.md) distinguishes actual defects from disputed suggestions and unrelated work. The new review skill retains that assessment. It leaves code changes and thread resolution for a later task.

The old workflow separated an author from a reviewer. The new local fallback also requests a different recorded model. This is a project preference, not a measured guarantee of better review. Unknown model identity remains unknown, including for Copilot.

On 2026-09-30, installed gh help and [GitHub documentation](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review?tool=cli) supported requesting review with gh pr edit and @copilot. A request and a completed review are different states. Later pushes can require another request.

The new skills omit frozen checks, machine-readable verdict blocks, automatic rebasing, and driver write manifests. The separate address-pr-review skill owns one requested wait-and-correction cycle. The skills omit unbounded repair loops and merge actions. The [Trial records](trials/README.md) list the submission and follow-up trials.

## Parent ownership of PR follow-up

[Issue #13](https://github.com/lmorchard/gh-project-workflow/issues/13) records Les's selected direction on 2026-10-07.
A pull request (PR) proposes changes for review.
The conversation parent dispatches follow-up directly after submission and receives its final report.
Submission alone does not satisfy a review-follow-up endpoint.

The issue cites ownership and reporting problems from the [Ready queue trial](trials/README.md#2026-10-05-ready-queue-burndown-on-board-6).
At `b47c9d5088f471da5d7b35a56ecda6078dee02be`, express still waited for a nested follow-up worker.
Shared [coordination](../references/shared/coordination.md#pr-follow-up-ownership), evidence, and delivery callers apply the selected ownership.
The follow-up worker reads the actual current commit before its final report and reassesses changed evidence.

The new ownership scenarios are constructed decision checks, not observed deliveries.
The [own-PR live trial](trials/2026-10-08-issue-13-own-pr.md) completed at `c7d7fdc40f1d0fcdc1c16ed2ccb333c34de571a9`, according to parent and worker handoffs.
It records direct parent dispatch, an external branch update, independent worker reassessment, and the worker's final report directly to the parent.
Initial and delta local review cover c7, and the worker reported green hosted CI for that head.
Publication of the completed record needs fresh delta review and final CI and head reassessment, which the parent already owns.
The c7 evidence does not cover that later documentation commit or authorize merge.

## Earlier dev-session guidance

On 2026-09-30, we also read the local dev-session files under ~/.claude/skills/dev-session. The relevant sources were phases/pr.md and references/pr-body-template.md. These local sources have no pinned repository revision in this record.

We retained whole-diff inspection, attention to generated files and lockfiles, and descriptions that explain decisions. We also retained assessment of review findings before changes. Neither automatic acceptance nor automatic dismissal of bot comments is useful.

The older Copilot command names copilot-pull-request-reviewer directly. The installed gh interface instead documents @copilot for --add-reviewer. The new skill uses that interface and requires a read-back of review state.

The older procedure waits for an increase in inline comment count. That misses completed reviews with no inline comments and does not identify the reviewed commit. The new skill examines review records and keeps pending review separate from unavailable access.

We did not copy mandatory squashing, automatic rebasing, repeated force-pushing, or a fixed polling loop. We also did not copy the assumption that an assignee listing establishes review access. The actual request and saved review state provide better evidence.

## Bounded Copilot wait

Les requested a wait of up to 20 minutes followed by corrections to review findings. The submit-pr skill records the request time and commit. The address-pr-review skill uses that handoff to poll or watch for a completed review. It does not use inline comment counts as the completion signal.

The cycle includes assessment, corrections, tests, commits, pushes, and factual replies within scope. Disputed findings remain open. If corrections require another review, the skill requests it and reports it as pending rather than starting an unlimited loop.

Timeout and partial-failure behavior remain untested in a live skill trial. Static validation does not establish that the wait or reply procedure succeeds on GitHub.

Les requested a separate follow-up skill for waiting and corrections. This makes the task usable on PRs created outside this workflow. The handoff carries request time, commit, review identifiers, and existing authorization without a new file format.

## Interview guidance

The interview skill adapts guidance from agent-sessions at revision `4379832`. Its [intake phase](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/intake.md) orders questions around the intended result and success conditions. It also records reasons for decisions and rejected alternatives. The new skill uses concrete examples to clarify vague answers without requiring formal criteria grammar or approval of each test.

The [rethink phase](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/rethink.md) carries lessons from failed attempts into the next interview. The new skill retains those lessons and confirmed decisions without requiring a restart or retirement procedure. The [triage phase](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/triage.md) keeps the user conversation with the parent while subagents research and propose changes.

These adaptations omit fixed question counts, mandatory discovery reports, tier labels, and separate decision logs. The agent maintains the draft while the user answers questions about intent and tradeoffs.

## ghflow entry and installation

[Issue #16](https://github.com/lmorchard/gh-project-workflow/issues/16) records Les's 2026-10-07 decision to register one `ghflow` skill.
Existing task procedures and shared policy moved into references with their boundaries preserved.
The symbolic-link installer follows the installation approach agreed in that conversation.

The first layout used a portable launcher to resolve the CLI from the source checkout.
Les then selected a repository-root skill package for PR #17.
The root entry now uses the existing CLI directly.
It supplies the absolute source path and preserves the caller's directory.

## Routine resolution and necessary decisions

The [issue #2 comparison](trials/2026-10-07-resolution.md) observed three fresh agents using the existing guidance successfully at `b47c9d5`. They researched a fact, implemented a routine choice, and returned an unresolved product decision.

Les then requested a maintained procedure and reusable scenarios, rather than an evidence-only record. The [decision rules](../references/shared/decisions.md) now distinguish these three cases at the decision point. The [evidence rules](../references/shared/evidence.md#sources-and-revisions) clarify reuse when sources and assumptions still apply. These are explicit clarifications, not corrections of a reproduced failure. The reuse scenario is a proposed regression case, not an observed task from the comparison.

The [maintenance rule](skill-style.md#rules-and-prohibitions) addresses Les's request for a persistent change. It routes authorized decision changes into the owning reference and a reusable scenario. It does not require automatic lesson discovery or an update after every task.

The [scenario results](../evals/results/2026-10-08-resolution.md) assess the revised guidance separately from the earlier action trials. Broader issue #2 experiments remain deferred.

## Required reviewer preparation

[Issue #8](https://github.com/lmorchard/gh-project-workflow/issues/8) supplies the agreed first increment: establish review capabilities before dependent implementation.
Les requested persistent instructions and reusable evaluations during the PR #21 revision.
The shared [preparation rule](../references/shared/review.md#prepare-required-review) replaces optional early planning in the delivery coordinators.
It preserves explicit exceptions, independent preparation, and the existing capacity handoff.

The [historical paired trial](trials/2026-10-07-issue-8-reviewer-capability.md) supplies observations and their limits.
The [reusable scenario results](../evals/results/2026-10-07-reviewer-preparation.md) assess decisions under constructed capability facts.
Les accepted recorded fresh author selection before future implementation as a valid resolution of unknown planned identity.
The unknown-author criteria reflect that interpretation of the existing shared rule. Evaluated instructions and raw prompts remain unchanged.
Neither source establishes a completed different-model code review or full delivery in the trial environment.

## Shared reference responsibilities

After merging PR #21, Les requested focused documents rather than the combined authorization reference. The restructure moves roles and handoffs into [Coordination](../references/shared/coordination.md). It moves factual resolution and question framing into [Decisions](../references/shared/decisions.md). [Authorization](../references/shared/authorization.md) retains permission and scope. Evidence and the interview task retain their existing responsibilities.

The move preserves merged review preparation and parent-owned PR follow-up. Active callers use the new owners. Earlier trial hashes, answers, and grades describe their pinned instructions and remain historical evidence.
