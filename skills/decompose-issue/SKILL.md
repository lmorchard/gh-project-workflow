---
name: decompose-issue
description: Break a broad existing issue into bounded child tasks grounded in current code, completed work, and actual callers. Explain dependencies, recommend the next child, and show how the tasks satisfy the parent goal. Do not implement or publish by default.
---

# Break an issue into useful tasks

Produce a concrete path from the current project to the parent issue's intended result. Preserve confirmed scope. Prefer independently useful changes that can be implemented and reviewed separately.

## Establish what remains

Read the parent issue, comments, existing children, related PRs, and project instructions. Identify current target and checkout revisions. Inspect the relevant target revision without resetting the user's checkout.

Compare completed work with the parent's success conditions. Credit delivered behavior without treating a merged child as proof of parent completion. If the parent needs reconsideration, apply [reconsider-issue](../reconsider-issue/SKILL.md) without repeating settled interviews.

Inspect actual callers, interfaces, tests, and relevant error paths. Do not invent consumers to fit a proposed task. For migrations, identify the concrete operations and their consumers before choosing groups. Include indirect requests and nonstandard transports where they affect the agreed boundary. A migrated operation can still have other unmigrated callers. For type-safety work, inspect whether each actual entry point is included in type checks.

Create a compact coverage map appropriate to the task. Link each remaining requirement or operation to completed work, an existing child, a proposed child, or an explicit exclusion. Name search coverage and uncertainty. Do not call the decomposition exhaustive when evidence is incomplete.

## Choose the child boundaries

Group changes by useful behavior, shared constraints, and review size. Prefer a working path through backend and consumer over separate layers that cannot demonstrate the intended result. Split a group when it contains independently useful changes or materially different risks.

Give each proposed child a title, intended result, exact included operations or behavior, limits, success conditions, and dependencies. Include source references where they establish the scope. Do not prescribe routine implementation details or duplicate the full parent body in every child.

Separate actual prerequisites from preferred order. A shared file alone does not establish a dependency. Reuse an existing child when its scope matches; do not propose duplicate issues for completed or active work.

Avoid both one giant replacement issue and automatic one-issue-per-endpoint fragmentation. Explain the grouping when alternatives affect cost or sequencing. Do not select a fixed number of children before inspecting the work.

Recommend one next child with a reason. Detail it enough for [define-issue](../define-issue/SKILL.md) to prepare an implementable draft without repeating the scope discussion. Mark unresolved decisions and uncertain later boundaries explicitly.

## Establish parent completion

Explain how the completed and proposed children satisfy every agreed parent success condition. Include any final integration check needed to establish the whole result. Closing all listed children is insufficient if requirements remain uncovered.

For behavior that does not fit the proposed implementation approach, return a scope or design question. Do not silently exclude it or replace the desired result with an easier test. Separate follow-up work outside the agreed boundary from work required to close the parent.

Review the decomposition for gaps, overlapping ownership, circular dependencies, and unsupported claims. Correct those problems before returning it. State which tests you ran and which assertions you only inspected.

## Discuss and hand off

Explain the proposed groups and recommended next child in the conversation. Ask one focused question at a time when user judgment changes the result. Include a recommendation and tradeoff. Use [interview-issue](../interview-issue/SKILL.md) when useful, without requiring a separate interview phase or file review.

When delegated, return the proposal, evidence, and questions to the parent. The parent conducts the interview. Carry confirmed decisions forward and revise the affected groups rather than restarting the decomposition.

Keep the plan provisional where facts or decisions remain unresolved. Do not label every proposed child Ready simply because it appears in the plan. Report what is ready for definition or implementation and what depends on another decision.

Decomposition alone does not authorize publication or implementation. If the agreed flow includes filing, pass reviewed children and existing authorization to [file-issue](../file-issue/SKILL.md). Do not ask again at that handoff. After the selected child completes definition, continue to filing within the agreed flow. Do not end with an unpublished draft merely because a subagent finished its assigned phase. Preserve explicit draft-only limits and report partial publication without creating duplicates on retry.

Use ordinary issue bodies and native child relationships for published work. No custom manifest, scheduler, fixed report template, or additional approval document is required.
