# 2026-10-08: issue #32 unpublished handoff trial

This trial passed one unpushed implementation commit to an independent local reviewer. It exercised the first case in [issue #32](https://github.com/lmorchard/gh-project-workflow/issues/32). It did not exercise the other three proposed cases.

The trial used `ghflow` instructions from revision `b330b5e5b15c0209b377cb5f9436d8386495ad77`. The source checkout advanced to `6e932ecd60751be8346ebe5e806515cd4c77fef1` before the actors finished. Their source checks confirmed that the seven instruction files used for this task matched the pinned revision. The parent also confirmed that the relevant CLI and task references did not change. The trial worktree remained at the pinned revision.

## Fixture and authorization

The fixture issue requested singular wording for a count of one and plural wording for other non-negative counts. The fixture contained a base commit and one local change. Its issue text and source files are preserved in [fixture](2026-10-08-issue-32-fixture/).

The checkout was `/private/tmp/ghflow-issue32-localreview` on branch `trial/item-count-singular`. The base was `654dda1dc68426c4f4081fb6d5b4d031700418b0`. The reported head and tested commit were both `aa4d2736388edd34051bcbbce6bb417678d16683`. The branch pointed to that head, the base was an ancestor, the checkout was clean, and no remote was configured. These checks establish local existence only.

Fixture setup used the synthetic Git identity `Trial Fixture <trial-fixture@example.invalid>`, fixed commit dates, a temporary `HOME`, and an allowlisted `env -i` environment. The environment did not inherit tokens, `ghflow` identity, or Git configuration. One initial commit attempt failed because inherited Git signing configuration needed an unavailable agent socket. The setup then succeeded with the isolated environment. No credentials or global Git settings changed.

The acting prompt is preserved in [actor-prompt.md](2026-10-08-issue-32-actor-prompt.md). It limited work to local inspection, temporary-copy tests, and reviewer dispatch. It excluded GitHub writes, push, PR creation, merge, and cleanup.

## Observed handoff and review

The coordinator, selected as `gpt-6-luna` with high reasoning effort, checked the supplied checkout and passed the full base and head identifiers to a fresh reviewer. The native dispatch selected `gpt-6.1-sol` with high reasoning effort. The coordinator log records the dispatch inputs and authorization. The parent directly observed the reviewer task and its returned result. Model names come from dispatch metadata. Runtime model attestation was unavailable.

The reviewer verified the checkout, branch, base ancestry, head, and commit subject. The reviewer inspected the issue and complete change. Its final report found no actionable defects and recommended the change. Both committed tests passed in an exact commit snapshot under an isolated environment. Additional assertions passed for counts `0`, `1`, `2`, `3`, `10`, and `10**30`. `git diff --check` passed.

The coordinator's captured logs are at `/private/tmp/ghflow-issue32-run/`. They record command arguments and outputs, the local handoff, dispatch inputs, and the reviewer result. The native dispatch transcript was not exported as a standalone artifact. The parent observed the nested task and favorable final result directly. No push or GitHub record change was authorized or reported.

One source lookup command failed because `rg` was absent from the allowlisted `PATH`. A `find` fallback listed Markdown paths, and the actors then read the pinned instructions with `git show`. The broad listing was truncated and was not used as evidence of file contents.

## Result and limits

The selected case passed: the coordinator established the unpublished commit locally and dispatched a fresh, different-model reviewer with the same full identifiers. The report separated executed tests from inspected Git evidence and stated the publication limit. The fixture and source checkouts remained unchanged.

The review did not test negative or non-integer inputs, external callers, hosted CI, or GitHub state. Dispatch selections establish the requested models, not provider runtime identity. An isolated source status command reported `.claude/` as untracked because the allowlisted environment omitted the user's global Git ignore rules. The parent confirmed the ordinary source checkout was clean. The other three issue #32 cases remain untested.

The parent had passed `make check` on the pinned source revision before this trial. I also ran `make check` on this artifact worktree before committing it. All 121 CLI tests, 10 script tests, the structure and link check, and the whitespace check passed. This record adds no product or skill behavior changes.
