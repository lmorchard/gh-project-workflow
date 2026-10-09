# ghflow setup trial

This is the historical nested-package trial before Les selected a repository-root skill package.
The [root-package trial](2026-10-07-ghflow-root-setup.md) records the later layout.

This trial assesses symbolic-link installation, discovery, routing, and source access for [issue #16](https://github.com/lmorchard/gh-project-workflow/issues/16).
A symbolic link points to the source directory. A fresh session has no earlier conversation.

## Local checks

Implementation starts from `dda34b3` in `.claude/worktrees/issue-16-ghflow`.
The baseline `make check` passed 93 CLI tests.
The revised suite adds nine installer and structure tests.
`make check` passes all 102 tests, local links, skill structure, scenario source paths, and whitespace.

Repeated installation preserves correct links. Source edits appear through each link without another copy.
Conflicting entries and ancestors cause refusal before any requested directory or link is created.
Tests cover files, directories, unrelated links, dangling links, and links to files.

An isolated project installation exposes only `ghflow`.
Its launcher runs from another directory and reads that directory's identity configuration.
Structure checks reject missing entry skills, extra registered skills, and tasks absent from the entry skill.
Link checks detect broken task references and stale scenario source paths.

The bundled skill validator could not start because system Python lacks PyYAML.
An isolated offline `uv` attempt also failed because its temporary cache contains no PyYAML.
Repository frontmatter checks pass. These local tests do not establish agent behavior.

## Fresh-session sources

A separate trial agent used fixtures in `/tmp/ghflow-native-trial-_y80vp42`.
Each target was a new Git repository with `README.md` and `request.txt` about optional task due dates.
Prompts requested an issue draft and a read-only delivery assessment. They supplied no expected answers.

The source skill was `/Users/lmorchard/devel/mine/gh-project-workflow/.claude/worktrees/issue-16-ghflow/skills/ghflow`.
The source changed during the trials. These results describe setup and routing during implementation, rather than certification of the final tree.
Logs and the original report remain beside the temporary fixtures.

## Versions and models

Claude Code was `2.1.293`. Startup and assistant metadata recorded `claude-opus-5-5`.
Codex CLI was `0.161.0`. Its configuration selected `gpt-6-astra/high`.
Codex JSON events did not report a returned model identity. Configuration proves selection, not a separate provider-confirmed identity.
Codex reported an unknown enterprise requirement, `ultrafast_mode`. Requests still completed.

OpenCode was `1.18.35`.
Its configured `ollama/qwen3-coder:30b` failed with `UnknownError` and was absent from the supported model list.
The trial used supported `opencode/big-pickle`.
A sanitized session export recorded `providerID=opencode`, `modelID=big-pickle`, and `agent=plan`.

## Discovery and routing

Claude discovered `.claude/skills/ghflow`, and its Skill tool loaded the entry instructions.
Codex discovered and read `.agents/skills/ghflow`.
OpenCode's `debug skill` reported exactly one `ghflow` with both compatible links present. It selected `.agents`.
After removal of `.agents`, OpenCode reported exactly one entry at `.claude`.
A final duplicate-discovery check repeated the same result.
The delivery agent used the equivalent `.claude` paths. Both links resolve to the same source.

All three agents selected `define-issue` for the draft request.
They read task references, shared rules, and source writing guidance.
They produced drafts in the response without publication or implementation.
They identified missing application code and revision evidence. Proposed behavior stayed separate from confirmed facts.

All three agents selected `express-issue` for the delivery assessment.
They retained the review-follow-up endpoint with an open PR and the requirement for fresh, different-model independent review.
They retained explicit merge authorization and the read-only trial limit.
They reported the missing selected issue and did not dispatch work.
Claude reported unavailable delegation in the restricted session. Codex reported exposed delegation that the prompt prohibited.
These assessments do not establish complete implementation or delivery.

## Source access and trial limits

All three agents ran launcher `--help` from the target directory.
Codex and OpenCode also ran it through a symlink path.
Claude and Codex read source `docs/writing.md` directly.
OpenCode initially rejected this external read and supplied no final conversational output.

A fresh OpenCode retry used this scoped configuration in the temporary target's `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "deny",
    "external_directory": {
      "/Users/lmorchard/devel/mine/gh-project-workflow/.claude/worktrees/issue-16-ghflow/*": "allow"
    }
  }
}
```

The retry read writing guidance and completed both requested responses.
The final delivery stream, `opencode-delivery-allowance.jsonl`, included final text and exit status 0.
The README documents scoped source access. The installer changes no permissions.

Claude's restricted Bash rules initially denied a compound help command.
A fresh retry permitted harmless `pwd` and `echo` commands. Standalone Python help then succeeded.
Claude used `--add-dir` for source access.
Codex and OpenCode needed sandbox escalation for existing runtime directories. Claude needed escalation for model network access.

All trial processes completed.
The agents changed no target code, GitHub records, commits, or branches.
The trial setup added only links and the temporary OpenCode configuration.
No personal installation or global configuration change occurred. Existing runtime directories can retain session records and caches.

## Commands

Run Claude from fixture/claude:

```sh
/Users/lmorchard/.local/bin/claude -p --no-session-persistence --output-format stream-json --verbose --permission-mode dontAsk --tools Read,Bash,Skill --allowedTools 'Read' 'Skill' 'Bash(python3 *)' 'Bash(realpath *)' 'Bash(pwd)' 'Bash(echo *)' --strict-mcp-config --setting-sources project --add-dir /Users/lmorchard/devel/mine/gh-project-workflow/.claude/worktrees/issue-16-ghflow < /tmp/ghflow-native-trial-_y80vp42/delivery-prompt.txt
```

Codex:

```sh
/Users/lmorchard/.local/bin/codex exec --ephemeral --sandbox read-only --json -C /tmp/ghflow-native-trial-_y80vp42/codex - < /tmp/ghflow-native-trial-_y80vp42/draft-prompt.txt
```

Delivery uses delivery-prompt.txt with the same command.

OpenCode:

```sh
/Users/lmorchard/.opencode/bin/opencode run --pure --agent plan --format json -m opencode/big-pickle --dir /tmp/ghflow-native-trial-_y80vp42/opencode 'Use the installed ghflow skill. Read README.md and request.txt, then prepare the requested draft in your response only. This is a read-only trial: no file edits, GitHub writes, commits, pushes, or delegation. Read only needed references including their linked writing guidance. Check its CLI --help from this target directory through the symlinked installation. Report operation, draft, unresolved decisions, resolved paths and limits.'
```

Discovery: `opencode debug skill` from target cwd. Actual model: `opencode export --sanitize ses_ee7777abaffetl3kb0y0Z977oX`.
