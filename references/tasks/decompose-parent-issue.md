# Break an issue into useful tasks

Produce a concrete path from the current project to the parent issue's intended result. Keep the confirmed scope, and prefer changes that are useful by themselves and can be implemented and reviewed separately. Decomposition alone does not authorize publication or implementation.

Apply [Authorization](../shared/authorization.md) and [Evidence](../shared/evidence.md) throughout. Before changing GitHub records, apply [GitHub writes](../shared/github-writes.md).

## Establish what remains

Read the parent issue and comments, existing children, related PRs, and project instructions. Inspect the current target revision.

Compare completed work with the parent's success conditions. Credit delivered behavior, but a merged child does not prove the parent complete. If the parent itself needs reassessment, apply [reconsider-issue](reconsider-issue.md) without repeating settled interviews.

Inspect actual callers, interfaces, tests, and relevant error paths. Do not invent consumers to fit a proposed task. For a migration, identify the concrete operations and their consumers before choosing groups. Include indirect requests and nonstandard transports where they affect the boundary. A migrated operation can still have unmigrated callers. For type-safety work, check whether each actual entry point is included in type checks.

Make a compact coverage map. Link each remaining requirement or operation to completed work, an existing child, a proposed child, or an explicit exclusion. State what your search covered and where uncertainty remains. Do not call the decomposition exhaustive when the evidence is incomplete.

## Choose the child boundaries

Group changes by useful behavior, shared constraints, and review size. Prefer a working path through backend and consumer over separate layers that cannot demonstrate the result. Split a group when it holds independently useful changes or materially different risks. Let the work decide how many children there are; avoid both one giant replacement issue and one issue per endpoint. Explain the grouping when the alternatives differ in cost or sequencing.

Give each proposed child a title, intended result, the exact operations or behavior it includes, limits, success conditions, and dependencies. Add source references where they establish scope. Leave out routine implementation details and do not copy the full parent body into each child.

Separate real prerequisites from preferred order; a shared file alone is not a dependency. Reuse an existing child when its scope matches. Do not propose duplicates of completed or active work.

Recommend one next child, with a reason. Detail it enough for [define-issue](define-issue.md) to prepare an implementable draft without repeating the scope discussion. Mark unresolved decisions and uncertain later boundaries.

## Establish parent completion

Explain how the completed and proposed children satisfy every agreed success condition of the parent. Include any final integration check needed to establish the whole result. Closing every listed child is not enough if requirements remain uncovered.

If some behavior does not fit the proposed approach, return a scope or design question. Do not silently exclude it or replace the desired result with an easier test. Separate follow-up work outside the boundary from work required to close the parent.

Review the decomposition for gaps, overlapping ownership, circular dependencies, and unsupported claims, and fix them before returning it.

## Discuss and hand off

Explain the proposed groups and the recommended next child in the conversation. [interview-issue](interview-issue.md) can guide the questions; a separate interview phase or file review is not required. When delegated, return the proposal, evidence, and questions to the parent. Carry confirmed decisions forward and revise the affected groups rather than restarting.

Keep the plan provisional where facts or decisions are unresolved. Report which children are ready for definition or implementation and which depend on another decision. Do not mark every proposed child Ready because it appears in the plan.

If the agreed flow includes filing, pass reviewed children to [file-issue](file-issue.md), and continue to filing after the selected child completes definition. Publish with ordinary issue bodies and native child relationships. No manifest, scheduler, or report template is needed.
