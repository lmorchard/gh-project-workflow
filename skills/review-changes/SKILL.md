---
name: review-changes
description: Review a local branch or pull request against its issue and report evidence-based findings without editing the implementation. Use for a local fallback when Copilot is unavailable or when an independent code review is requested.
---

# Review changes

Assess proposed changes against their issue and the current code. Report defects and missing evidence without modifying the implementation. The next task assesses and addresses the findings.

Apply [Evidence](../shared/evidence.md) and [Review](../shared/review.md) throughout.

## Set up the reviewer

The parent starts this review in a fresh context. It supplies the repository, issue, project instructions, and exact base and head commits. Give the reviewer the necessary facts, not the author's conversation or conclusions.

Select the reviewer model explicitly through the available tool configuration. It must differ from the implementation model, as [Review](../shared/review.md) describes. Record both identities and their sources.

## Establish the scope

Read the issue, project instructions, and the diff between the supplied commits. Inspect related code where it affects the changed behavior. Earlier work does not need to have used these skills.

Treat the implementation report as claims, not as your conclusion. Examine tests before you accept their stated coverage.

Keep the implementation checkout unchanged. If tests generate files or modify data, use an isolated temporary copy. Do not change expected results to make the reviewed code pass.

For a published PR, get its current head and review discussions. Include top-level comments and reviews without inline threads. Read all result pages, and report incomplete retrieval.

## Examine the change

Focus on these questions:

- Does the change satisfy the issue without changing the agreed scope?
- Do callers, error paths, permissions, and data handling remain correct?
- Do tests establish the intended behavior rather than a nearby substitute?
- Do builds and generated files match the code that users receive?
- Do documentation and setup instructions match the change?

Run useful targeted checks where the environment permits. Record setup failures separately from product defects. Passing tests do not prove that no defects exist.

Evaluate existing review findings instead of accepting them. Distinguish a demonstrated defect from a question, a preference, or an unrelated existing problem. Avoid speculative redesign outside the issue.

## Return findings

For each finding, give the file and lines, the triggering condition, the observed or reasoned result, and its practical impact. Explain how it conflicts with the intended behavior. Suggest a correction without implementing it.

If you found no actionable defects, say so. Do not invent a finding to justify the review. Include untested behavior and evidence limits either way.

Return the reviewed base and head, the model identities and their sources, the findings, and the checks you ran. If the head changed during review, say that the result covers the earlier commit. Keep the report short, in the conversation or a requested location. Return user decisions to the parent.

Do not post a GitHub review without authorization to publish it. Do not edit code, resolve threads, approve a merge, or start a repair loop.
