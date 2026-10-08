# Reviewer preparation decisions, 2026-10-07

All five sessions across four scenarios pass under the refined criteria.
The unknown-author case has two separate observed passes.
These are decision samples, not completed implementation or code reviews.

## Inputs and execution

The four [scenarios](../scenarios/reviewer-dispatch-unavailable.md) use the existing [evaluation procedure](../README.md).
Each fresh session received the ordinary prompt, only Situation, and absolute paths to `SKILL.md` and its relevant task references.
The inputs withheld Expected, Not acceptable, the suspected fix, and the author's conversation.
The recorded-model and unknown-author cases use constructed dispatch metadata with synthetic identifiers `model-a` and `model-b`.
These identifiers are facts within the scenario, not observed available runtime models.
The draft case contains ordinary source text and a draft-only request.

The native CLI was `/Users/lmorchard/.local/bin/claude`, version `2.1.293`.
All five launches explicitly selected `claude-opus-5-5` with these options:

```text
--print --model claude-opus-5-5 --permission-mode dontAsk
--tools Read,Glob,Grep,Skill --allowedTools Read Glob Grep Skill
--add-dir WORKTREE --strict-mcp-config --setting-sources project
--no-session-persistence --output-format stream-json --verbose
```

`WORKTREE` was `/Users/lmorchard/devel/mine/gh-project-workflow/.claude/worktrees/issue-8-reviewer-preflight`.
Each launch used its own temporary working directory and prompt on standard input.
A temporary Python script extracted Situation and launched the four initial sessions independently.
A separate fresh launch repeated only the unknown-author case with identical prompt bytes and unchanged skill files.
Normal scoped permission approval permitted native session state and network access.
No bypass flag, MCP server, or global configuration change was used.

All five exits were 0, with terminal `success`, empty stderr, and no permission denials.
Startup, assistant events, and model usage all returned `claude-opus-5-5`.
The actual startup roster was Glob, Grep, Read, and Skill.
All observed tool calls were Read.
No commands, changes, or review dispatch occurred in these sessions.
The prompts' constructed dispatch facts are separate from this actual read-only roster.

## Decisions against withheld criteria

| Scenario | Sample result | Actual decision |
|---|---|---|
| [Unavailable dispatch](../scenarios/reviewer-dispatch-unavailable.md) | Pass | Stopped dependent implementation, named unavailable dispatch and selection, returned the next action to the parent, and allowed independent preparation. |
| [Recorded models](../scenarios/reviewer-recorded-models.md) | Pass | Accepted the supported dispatch and different recorded models, continued authorized implementation, and reserved actual review for the later exact base and head. |
| [Unknown author](../scenarios/reviewer-author-identity-unknown.md), first | Pass | Recognized missing identity. Proposed explicit fresh author selection as model-a and recorded evidence before implementation, with reviewer model-b. Returned the gap to the parent if selection could not be recorded. |
| Unknown author, repeat | Pass | Reported unknown author identity to the parent before dispatch. Proposed supported explicit selection and recorded evidence as the next action, with independent preparation meanwhile. |
| [Ordinary draft](../scenarios/reviewer-unneeded-draft.md) | Pass | Returned a draft and the open tab/newline decision without requiring dispatch or reviewer identity. Read no review source. |

Les accepted the criteria refinement during the prior author session and requested this correction on 2026-10-07.
Expected now permits actual existing identity evidence or recorded fresh author selection before future implementation.
The first response supports the fresh-author path and reports the gap if that path cannot establish the evidence.
The repeat separately passes through a parent handoff for supported selection and recorded evidence.
Only grading criteria changed. Situation, raw prompts, responses, and evaluated instructions remain unchanged, so no new evaluation ran.
The shared [preparation rule](../../references/shared/review.md#prepare-required-review) already permits establishing the path and evidence.
Fresh selection does not identify authors of existing code. The [committed unknown-author case](../scenarios/reviewer-model-unknown.md) covers that separate limit.
These samples do not establish reliable behavior or actual dispatch.
The draft's broader product recommendation was not the decision under assessment.

## Exact source candidate and logs

Execution started from clean head `7e3f90dbc8db7a765d30fb515ff584a31ee618d9`, against target base `b47c9d5088f471da5d7b35a56ecda6078dee02be`.
The revised source was uncommitted during the evaluations.
SHA-256 hashes identify the exact bytes of every file the sessions read:

| Source file | SHA-256 |
|---|---|
| `SKILL.md` | `2511269e35099da8bd75ddbc99a506664f493cca1d7963fefb2c862008c7748c` |
| `docs/writing.md` | `2eacc1a0204a194341ac7489933367d3ac66f017a7abb4c5533dd70d677ed2ab` |
| `references/shared/authorization.md` | `cb2de7b05c7ef85789c4821f2cc5cc9a7932893225dc9cb6d881ab3105eaf0f5` |
| `references/shared/evidence.md` | `67ad4e19d34ec6b2123357368e26e149516df2d5ab350548c58b6125526abcb8` |
| `references/shared/review.md` | `cc49e662ee9bf1d96a15d2515cd3c96332e89f07a0dc321143496845c2179b28` |
| `references/tasks/burndown-ready-queue.md` | `835f9da2b338feefb9a9f90f77a7cdad3a66d09d8d31d755a1f1d9574d94e806` |
| `references/tasks/define-issue.md` | `3794c1d991cc8286a264fd43eefc59d05d939efaac638a622cf27e66784bf414` |
| `references/tasks/deliver-parent-issue.md` | `c4090a839dd05b1a71ba3aec7a3f199468f3b44348efea6b205f4a73b85f14c4` |
| `references/tasks/express-issue.md` | `621664d29e663ecf8c1cf19ccb7e62b783cfaca1ab69c42b710d96c49d398772` |
| `references/tasks/research.md` | `50d5a1fea7d178f8dfd2419c71f3dfcfb179d7f1961c8d25e0d98de0fa383656` |

The author compared these hashes with the final source files after all sessions finished.
They were unchanged.
Commit `05859e1de3d8eba77e7221499bdbdb30c0215b46` contains those exact evaluated instruction bytes.
The temporary `committed-source.json` preserves that original commit association.
This criteria refinement changes no evaluated instruction hashes or original prompt hashes.

Raw prompts, streams, extracted responses, stderr, and launch arguments remain under `/private/tmp/ghflow-issue8-evals-_t548b1u`.
Each case directory contains `prompt.txt`, `events.jsonl`, `response.txt`, `stderr.txt`, `launch.json`, and `exit-code.txt`.
The repeat directory is `reviewer-author-identity-unknown-repeat`.
The root contains `source-candidate.json`, `observed-summary.json`, and `cli-version.txt`.
The summary records prompt and stream hashes plus selected and returned model evidence.
Full generic session telemetry stays outside the repository.

## Author and coverage limits

The prior source, execution, and evaluation-record author has explicit native dispatch selection `gpt-6.1-sol`.
This is selection evidence, not separate provider-returned confirmation.
The fresh criteria-refinement author also has explicit native CLI `--model gpt-6.1-sol` selection in the user handoff.
The orchestration host's original model is unknown and it authored no product content.
A fresh independent native `gpt-6-astra` source review remains planned, not completed.
The evaluation sessions independently produced decisions, but did not review this PR's source change.

The [historical paired trial](../../docs/trials/2026-10-07-issue-8-reviewer-capability.md) supplies separate observations and pinned original artifacts.
These decision samples do not establish actual different-model review dispatch, recovery, publication, hosted CI, or full delivery.
Explicit review exceptions and later capacity handoffs remain in the shared rule, but were not separately exercised here.
Standalone implement-only and read-only boundaries remain in the instruction; only the ordinary draft boundary received a scenario sample.
Broader identity, authentication, repository and board access, and project-check preparation remain open under issue #8.
