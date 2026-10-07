# ghflow setup trial

This trial checks [issue #16](https://github.com/lmorchard/gh-project-workflow/issues/16): discovery through symbolic links, operation selection, dependencies, and authorization limits.
The implementation starts from `dda34b3` in an isolated worktree.

## Local behavior checks

The baseline `make check` passed all 93 CLI tests.
The revised suite adds nine installation and structure tests.
They establish these results:

- Repeated installation preserves correct links.
- Source edits appear through each link without another copy.
- Files, directories, unrelated links, and dangling links cause refusal before any requested link is created.
- Conflicting destination ancestors also cause refusal before any directory or link is created.
- Installation exposes only `ghflow` in an isolated project skill directory.
- The linked CLI launcher runs from an unrelated directory and reads that directory's identity configuration.
- The structure check rejects missing entry skills, extra registered skills, and task references absent from the entry skill.
- The link check detects a broken task reference and a stale scenario source path.

`make check` passes all 102 tests, local Markdown links, and whitespace checks.
These tests do not establish agent discovery or routing behavior.

The skill-creator validator could not start with system Python because PyYAML is unavailable.
An isolated offline `uv` attempt also failed because its temporary cache contains no PyYAML package.
The repository's own frontmatter check passes.

## Fresh-session trials

Fixtures: `/tmp/ghflow-native-trial-_y80vp42`; source: `/Users/lmorchard/devel/mine/gh-project-workflow/.claude/worktrees/issue-16-ghflow/skills/ghflow`.

Each target is an unborn Git repo with only README.md and request.txt describing optional task due dates. Fresh prompts are in draft-prompt.txt and delivery-prompt.txt. No expected answers were supplied. No target code, GitHub record, commit or push was changed. Native CLI runtime logs/cache/session records may persist in existing runtime directories; no global installation or configuration change was made.

### Versions and model evidence

- Claude Code 2.1.293. Startup and assistant event metadata: claude-opus-5-5.
- Codex CLI 0.161.0. Existing config selects gpt-6-astra/high. JSON events do not expose returned model identity, so config selection is evidence, not a separate provider-confirmed identity. Startup reports unknown enterprise requirement ultrafast_mode; requests still complete.
- OpenCode 1.18.35. Existing configured ollama/qwen3-coder:30b failed with UnknownError and was absent from `opencode models`. Selected supported `opencode/big-pickle`; sanitized session export records providerID opencode and modelID big-pickle, agent plan.

### Discovery

Claude `.claude/skills/ghflow` appears in startup skills and Skill tool successfully loads it. Codex `.agents/skills/ghflow` is discovered and read. OpenCode `debug skill` with both `.claude/skills/ghflow` and `.agents/skills/ghflow` returns exactly one ghflow, choosing `.agents`. Removing `.agents` returns exactly one at `.claude`. Retaining one `.agents` installation is enough; no duplicate entry was observed.

### Draft routing

Claude and Codex select define-issue, read shared authorization/evidence and linked source docs/writing.md, produce in-response drafts, distinguish proposals from confirmed facts and identify missing application code/revision. Both run launcher help from target cwd. Codex also executes launcher through the symlink path. OpenCode fresh scoped-permission run selects define-issue, reads task/shared references and linked docs/writing.md, runs launcher help, and produces an in-response draft. It reports missing implementation and revision evidence, retains ordering and due-date display as unresolved decisions, and does not publish or implement. Earlier runs without the allowance ended without final conversational output.

### Delivery routing

Claude and Codex select express-issue; identify review-follow-up endpoint with PR left open, fresh-context different-model independent review, recorded runtime/dispatch identities, explicit merge authorization and read-only trial limits. Claude correctly reports this tool-limited session lacks delegation/model dispatch; Codex reports exposed delegation but the prompt forbids it. Missing real GitHub issue and unborn fixture are explicit evidence limits. Neither dispatches. OpenCode reads express/review policy and executes CLI help but its completed JSON stream contains only tools and step events; no final assessment was delivered.

### Paths and permission limits

All three execute source `scripts/ghflow.py --help` with target checkout as cwd and observe ghflow usage. All three read task/shared references through native symlink installation. Claude/Codex actually read source docs/writing.md. OpenCode initially auto-rejected that outside-cwd read; fresh run with the scoped project-only config below successfully reads it. No blanket external allowance or global configuration was added.

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

Claude initial delivery command was denied by restrictive trial Bash permissions for compound pwd/python/echo commands. Fresh retry allows harmless pwd/echo and successfully runs standalone python3 help; this was a harness limitation, not a source portability defect. Source-checkout access is supplied with --add-dir. Codex/OpenCode initially require escalation because runtime directories outside tmp are sandbox-protected. Claude initially retried network requests under the sandbox; narrow escalation permits model access.

### Commands

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

Logs are JSONL plus stderr beside this report. Source files were being edited concurrently, so this is an in-progress implementation trial, not final-tree certification.
