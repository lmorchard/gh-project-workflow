# Blocked and parked triage labels, 2026-10-08

Four fresh decision-only sessions ran the two scenarios that this change added. Each scenario ran twice. All four answers passed their full criteria.
The author of the skill change graded the answers. Independent review remains separate.

## Source and method

The evaluated source commit is `c96332a` on branch `triage-blocked-parked-labels` (PR #41).

Following the [scenario procedure](../README.md), each session received only its Situation, the scenario prompt, and the skill paths. The prompt also told each session not to read files under `evals/`. No sandbox enforced that limit.

Each session was a Claude Code `general-purpose` subagent with no conversation history. The parent ran `claude-opus-5-5`. The subagents did not report a separate model identity, so they probably used the same model. The skill author was the same parent session, so these runs do not compare different models.

- `blocked-partial-blockers` received `SKILL.md` and `references/tasks/sweep-blocked.md`.
- `definition-hits-dependency` received `SKILL.md`, `references/tasks/sweep-needs-definition.md`, and `references/tasks/define-issue.md`.

Each session reported reading only skill and shared-reference files. No session reported a command, a write, or a read under `evals/`.

## Results

| Scenario | Run | Grade |
| --- | --- | --- |
| `blocked-partial-blockers` | 1 | Pass |
| `blocked-partial-blockers` | 2 | Pass |
| `definition-hits-dependency` | 1 | Pass |
| `definition-hits-dependency` | 2 | Pass |

### blocked-partial-blockers

Both answers left #964 blocked because #1007 is open, and both cited the rule that every blocker must be closed. Both returned #999 to `triage:needs-definition` with a comment that names #956, its closing PR, and the need for a full specification. Both kept #1000 on `triage:blocked` and reported its text-only blocker so that the relationship can be set. Neither answer wrote a specification for #999.

Run 2 also checked that the sweep request authorizes label writes before it makes them. That check is correct under [Authorization](../../references/shared/authorization.md), but the scenario did not require it.

### definition-hits-dependency

Both answers stopped specification under step 5 of sweep-needs-definition. Both set native blocked-by relationships to #163 and #1007, described an optional outline without file targets, and applied `triage:blocked`. Both rejected `triage:needs-input` because no user question is open. Both rejected a split because the whole adapter depends on the interface.

Both answers also said to leave the issue on its label if the relationships cannot be set. That behavior comes from [Triage labels](../../references/shared/triage-labels.md). The scenario did not test it.

## Limits

Two runs of each scenario are samples, not proof. The runs used one model family, and the skill author graded them. The scenarios test decisions only. They do not test GitHub writes, such as setting a blocked-by relationship with the installed `gh`.
