---
name: review-changes
description: Review a local branch or pull request against its issue and report evidence-based findings without editing the implementation. Use for a local fallback when Copilot is unavailable or when an independent code review is requested.
---

# Review changes

Assess the proposed changes against the issue and current code. Report defects and missing evidence without modifying the implementation. A review is not permission to merge.

## Select the reviewer

The parent starts this review in a fresh context. It supplies the repository, issue, and exact base and head commits. The reviewer receives project instructions and necessary facts, not the author's conversation or conclusions.

For the local fallback, select a different model from the implementation model. Use available tool configuration to select the model explicitly. A different agent name or fresh context does not establish a different model.

Record the implementation model and reviewer model from available session metadata or dispatch records. Do not infer model identity from writing style or an agent's unsupported claim. A changed reasoning setting alone does not count as a different model.

If either model is unknown or a different model is unavailable, return that limit to the parent. Do not silently satisfy this requirement with the same model. A same-model second opinion can still help, but label it and leave the requested different-model review incomplete.

Copilot is a separate review service. Unless its model identity is supplied, record that identity as unknown. Neither a different model nor a separate service guarantees correct findings.

## Establish review scope

Read the issue, project instructions, and the diff between the supplied revisions. Inspect related code where it affects changed behavior. Do not require that earlier work used these skills.

Treat the implementation report as claimed evidence, not as your review conclusion. Examine tests before accepting their stated coverage. Distinguish tests you execute from tests you only read.

Keep the implementation checkout unchanged. Use an isolated temporary copy if tests generate files or modify data. Do not change expected results to make the reviewed code pass.

If reviewing a published PR, obtain its current head and relevant review discussions. Include top-level comments and reviews without inline threads. Read all result pages and report incomplete retrieval.

## Examine the change

Focus on these questions:

- Does the change satisfy the issue without changing agreed scope?
- Do callers, error paths, permissions, and data handling remain correct?
- Do tests establish the intended behavior rather than a nearby substitute?
- Do builds and generated files correspond to the code that users receive?
- Do documentation and setup instructions match the change?

Do useful targeted checks where the environment permits them. Record setup failures separately from product defects. Do not claim that passing tests prove the absence of defects.

Evaluate existing review findings rather than accepting them automatically. Distinguish a demonstrated defect from a question, preference, or unrelated existing problem. Avoid speculative redesign outside the issue.

## Return findings

For each finding, give the affected file and lines, triggering condition, observed or reasoned result, and practical impact. Explain how it conflicts with the intended behavior. Suggest a correction without implementing it.

State when you found no actionable defects. Do not invent a finding to justify the review. Include untested behavior and evidence limits even when there are no findings.

Return the reviewed base and head commits, model identities and their sources, findings, and executed checks. If the head changed during review, report that the result concerns the earlier commit. Do not call it a review of the current head.

Keep the report short and use ordinary technical English. Use the existing conversation or requested output location rather than creating a mandatory report format. Return user decisions to the parent.

Do not post a GitHub review without authorization to publish it. Do not edit code, resolve threads, approve a merge, or start a repair loop. The next task assesses and addresses the findings.
