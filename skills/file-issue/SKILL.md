---
name: file-issue
description: Publish a reviewed issue draft with GitHub CLI, add requested parent and project relationships, and confirm the saved result. Use when filing is authorized or when resuming a partially completed filing.
---

# File an issue

Publish the supplied draft without repeating issue definition. Use existing gh commands. Return the issue URL and the confirmed results of requested changes.

## Establish the requested changes

Read the draft and the relevant project instructions. Identify the repository, title, body, and requested metadata. Metadata includes labels, parent issue, project, and project fields.

Use authorization and decisions already present in the conversation. A request to file the draft authorizes issue creation. Do not ask for that permission again.

Do not infer a board status, priority, assignee, or label from the draft alone. Use the user request or applicable project conventions. If an optional value is unspecified, leave it unset.

If a missing decision changes the issue meaning, return that question to the parent or user. Do not rewrite scope during filing. The draft can come from `define-issue`, another tool, or the user.

When delegated, return missing decisions to the parent agent. Do not attempt a user interview from the subagent. Do not treat agreement with an issue idea as authorization to publish it.

## Inspect GitHub before writing

Use `gh auth status` to make sure that authentication succeeds. Do not print credentials or change accounts to bypass a permission error. If authentication fails, report the required action.

Inspect installed command help for the operations you need. Do not assume that commands require manual identifier lookup. Some versions support parent links and project field names directly.

Search the target repository for a possible existing issue before creation. Include closed issues when they can contain the same request. If resuming, inspect the recorded issue URL first.

A title match alone does not prove that two issues are duplicates. Compare intent and scope before choosing the next action. If an equivalent issue exists, report it rather than creating another or silently replacing its body.

If a project is requested, read its identity and fields. A project title can be ambiguous. Prefer the project owner and number when selecting its board.

## Prepare the exact content

Write the issue body to a local UTF-8 file. Keep the title separate from the body. Preserve the reviewed text, links, commands, and scope.

Use `--body-file` instead of placing multiline content inside a shell command. This preserves newlines and literal code text. Quote shell arguments safely.

Record the intended operations before the first write. A short session note is sufficient. Do not create a custom state store for one filing.

## Create and complete the issue

Create the issue in the explicit target repository. Include supported parent or project flags when their targets are unambiguous. Record the returned issue URL immediately.

After creation, read the saved issue. Make sure that its title and body match the prepared content. Make sure that requested relationships exist rather than relying only on the creation response.

Complete missing requested metadata on that existing issue. If project status is requested, apply it after project membership exists. Use the actual field and option names from the board.

Do not edit the parent body merely to establish a parent relationship. Do not add a comment when a native relationship supplies the requested link. Preserve unrelated metadata.

## Resume after an error

A failed command can leave some requested changes completed. A missing response does not prove that creation failed. Read GitHub before repeating a write.

If an issue URL was returned, inspect that issue first. If no URL is available, search recent issues and compare their content with the intended draft. Do not create again while the first result remains uncertain.

If only the parent link or board update failed, retry that operation on the existing issue. Do not delete a successfully created issue to undo a later error. Report completed operations separately from failed or uncertain operations.

If current content differs from the expected draft, investigate before overwriting it. Another user or process can change an issue between reads. Do not claim that all changes succeed or fail together. Another process can still change the issue during filing.

## Confirm and report

Read back the title, body, parent relationship, project membership, and requested fields that apply. Report the issue URL and the confirmed changes. Identify failed or uncertain steps with the information needed to resume.

Do not claim that filing establishes implementation readiness or test success. Do not begin implementation. If trial notes were requested, record useful tool findings without copying live board status into general documentation.
