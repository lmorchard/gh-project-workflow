# Sweep and prioritize issues

Evaluate open `triage:ready` issues, assign their `Priority` (`P0`–`P3`) and `Size` (`XS`–`XL`) fields, and stage high-priority (`P0`/`P1`) issues into the project board's `Backlog`. Re-sweep lower-priority (`P2`/`P3`) issues when the high-priority queue runs low or circumstances warrant a rethink. This skill does not move issues to `Ready` or begin implementation.

Apply [Authorization](../shared/authorization.md), [Evidence](../shared/evidence.md), [Board status](../shared/board-status.md), and [Agent identity](../shared/identity.md) throughout. The parent agent conducts the ranking review with the user; subagents execute project board field updates in the subject repository.

## Select the candidate pool

Identify the set of issues to prioritize:
- **Unprioritized sweep**: Open issues with label `triage:ready` that lack a `Priority` field on the project board, typically scoped by parent theme.
- **Re-sweep of P2/P3 issues**: Query existing `P2` and `P3` issues when the active `P0`/`P1` queue is exhausted, when a milestone completes, or when new architecture makes previously deferred tasks high-leverage.

## Estimate priority and size

For each candidate issue, evaluate its technical specification against current code:

### Priority Tiers
- **P0 (Critical / Blocker)**: Active bug, data loss risk, test execution hazard (e.g. real LLM calls in unit tests), or gate landmine blocking development.
- **P1 (High Priority)**: Core product capability, major user-facing improvement, or high-leverage architectural unblocker.
- **P2 (Medium Priority)**: Quality-of-life improvement, secondary feature, or UI polish without urgent user impact.
- **P3 (Low Priority)**: Minor edge-case optimization, cosmetic cleanup, or low-urgency refactoring.

### Size Tiers
- **XS**: One-liner fix or single config field change.
- **S**: Small, self-contained change (<100 lines, 1–2 files).
- **M**: Medium component or module change with targeted tests.
- **L**: Substantial cross-module change requiring broader integration verification.
- **XL**: Major architectural task (consider whether it should be decomposed).

## Review ranking with the user

Present candidate rankings in a summary table grouped by parent theme:

| Issue | Title | Suggested Priority | Suggested Size | Rationale |
|---|---|:---:|:---:|---|

Highlight items recommended for `P0` or `P1` vs those deferred to `P2` or `P3`. Discuss adjustments with the user and record confirmed values.

## Update project board fields

Once rankings are confirmed, dispatch a subagent to update the project board under the machine identity:

1. Add the issue to the project board if not already present.
2. Set the `Priority` single-select field (`P0`, `P1`, `P2`, `P3`).
3. Set the `Size` single-select field (`XS`, `S`, `M`, `L`, `XL`).
4. Set the `Status` field:
   - For **P0 and P1 issues**: Set Status to `Backlog` (or preserve a later state such as `Ready` or `In progress`).
   - For **P2 and P3 issues**: Leave in `Backlog` or manage according to board filtering rules (e.g. filtered out of active views).

## Return and hand off

Return a summary table of prioritized issues:
- Total counts by priority (`P0`, `P1`, `P2`, `P3`).
- List of newly staged `P0`/`P1` items in the board's `Backlog`.

Hand off to [curate-ready-queue](curate-ready-queue.md) to select the next tasks to pull into the board's `Ready` column.
