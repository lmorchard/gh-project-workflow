# Findings from agent sessions

These notes preserve useful lessons from agent-sessions without copying its entire design. Reviewed on 2026-09-30 against agent-sessions commit `4379832`. References below point to that revision so subsequent edits do not silently change the evidence.

The predecessor's findings include recorded experiments and incidents. This review read those records; it did not rerun their experiments or independently validate every historical claim.

## The workflow predates the harness

The original design identified dev-session as supplying most of the per-issue workflow. It treated acceptance criteria and verification as important additions and placed the code that chooses and runs board tasks outside the skill.

Implication for this project: extract useful operations and workflow guidance first. Neither requires a program that chooses and runs queued tasks.

Source: [design, origin and dev-session analysis](https://github.com/lmorchard/agent-sessions/blob/4379832/docs/design.md).

## The current skill requires its driver

The write-manifest reference requires the agent to record requested GitHub changes in a file for the driver to perform with its own credentials. The GitHub Projects reference uses that mechanism for board transitions. The review-comment phase assumes unresolved threads have already been supplied in context and exits so the driver can choose the next step.

Implication: copying the Markdown directory would not produce a self-contained skill. Each extracted phase needs clear inputs, a way to fetch the information it needs, and commands that works without the driver.

Sources: [write manifest](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/references/write-manifest.md), [board integration](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/references/github-projects.md), [addressing comments](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/address_comments.md).

## Evidence must establish the claim being made

The predecessor records recurring cases where nearby evidence satisfied the wrong condition: local tests stood in for CI, absence of threads stood in for review completion, or evidence described a different commit from the one being shipped. It also records failures where missing data appeared positive.

Implication: tools should collect and identify evidence precisely, including the commit it describes and whether retrieval is complete. An empty result, unavailable result, and successful check are different outcomes. The agent still has to decide whether the evidence establishes the intended behavior.

Sources: [recurring defect classes 1 and 2](https://github.com/lmorchard/agent-sessions/blob/4379832/docs/findings.md), [merge gate procedure](https://github.com/lmorchard/agent-sessions/blob/4379832/skills/agent-session/phases/grade_gate.md).

## Tests need to detect the intended failure

The findings record checks that passed without the requested work, guards satisfied by text in comments, and tests that missed absence of the object being tested. They distinguish regression protection from evidence of new behavior.

Implication: exercise a helper's meaningful failure cases, including missing or incomplete data. For a change, explain how verification demonstrates the requested outcome; a green test suite alone may not do that. This does not imply every task needs a separate commit recording the original checks and a file used to detect later changes to them.

Source: [defect classes 5 and 6 and rules about oracles](https://github.com/lmorchard/agent-sessions/blob/4379832/docs/findings.md).

## More instructions did not reliably improve behavior

The predecessor's evidence ledger reports wording experiments where additions made no difference or performed worse than their absence. It also describes important wording that helped, including the frozen-check amendment rule. Its conclusion is not that instructions are useless, but that plausible wording is not evidence of better behavior.

Implication: retain useful guidance with its provenance, avoid duplicating every incident as a new rule, and evaluate behavioral changes through actual use and targeted comparisons. The predecessor explicitly distinguishes wording experiments from real use that establishes whether an agent actually performs a procedure.

Source: [defect class 4, evidence ledger, and measurement limits](https://github.com/lmorchard/agent-sessions/blob/4379832/docs/findings.md).

## New sessions reveal missing information

The predecessor records failures discovered when a new agent session read a specification, rather than sharing the author's unstated knowledge.

Implication: test a phase on an ordinary issue or PR in a fresh session. A successful continuation inside the authoring conversation is weaker evidence that the handoff works independently.

Source: [operating rules and fresh context finding](https://github.com/lmorchard/agent-sessions/blob/4379832/docs/findings.md).

## Tools for repeatable operations remain valuable

The founding discussion explicitly retained the wins from extracting scriptable Git and GitHub procedures into tools. Existing code offers candidate implementations and failure cases for review context, board lookup, workspaces, and writes. That is a reason to inspect and selectively reuse code, not evidence that every current module belongs here.

Implication: prefer tools that do one operation and return control to the agent. Keep scheduling, support for multiple agent runtimes, locks shared across machines, spending limits, and automatic recovery out of the initial project.

Sources: founding discussion on 2026-09-30; [predecessor driver sources](https://github.com/lmorchard/agent-sessions/tree/4379832/src/agent_sessions/driver).

## Docs should explain decisions without copying live status

The predecessor repeatedly encountered written file lists and status claims that drifted from their live sources. It also found that historical explanations inside instructions read by the agent could reintroduce obsolete behavior into the agent's context.

Implication: keep rationale and historical evidence in docs, operational instructions in the skill, and current work state in its actual source. Date historical observations and link their evidence. Avoid copying the predecessor's instruction files as a starting set of rules.

Source: [documentation and skill-authoring conventions](https://github.com/lmorchard/agent-sessions/blob/4379832/CLAUDE.md).
