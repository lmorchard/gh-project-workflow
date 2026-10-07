# ghflow setup trial

This trial checks [issue #16](https://github.com/lmorchard/gh-project-workflow/issues/16): discovery through symbolic links, operation selection, dependencies, and authorization limits.
The implementation starts from `dda34b3` in an isolated worktree.

## Local behavior checks

The baseline `make check` passed all 93 CLI tests.
The revised suite adds seven installation and structure tests.
They establish these results:

- Repeated installation preserves correct links.
- Source edits appear through each link without another copy.
- Files, directories, unrelated links, and dangling links cause refusal before any requested link is created.
- Installation exposes only `ghflow` in an isolated project skill directory.
- The linked CLI launcher runs from an unrelated directory and reads that directory's identity configuration.
- The structure check rejects missing entry skills, extra registered skills, and task references absent from the entry skill.
- The link check detects a broken task reference.

`make check` passes all 100 tests, local Markdown links, and whitespace checks.
These tests do not establish agent discovery or routing behavior.

The skill-creator validator could not start with system Python because PyYAML is unavailable.
An isolated offline `uv` attempt also failed because its temporary cache contains no PyYAML package.
The repository's own frontmatter check passes.

## Fresh-session trials

A separate trial agent is checking Claude Code, Codex, and OpenCode in temporary target projects.
Its discovery and routing results are pending at this implementation checkpoint.
No persistent personal installation was performed.
