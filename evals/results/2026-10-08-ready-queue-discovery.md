Two fresh decision samples assessed Ready queue discovery at source commit `3c011eac6e56e0524b36a5b009343a35b79550a9`. Both answers passed their separate criteria. A controlled local fixture also showed that `gh api --paginate --slurp` follows the cursor and that a later-page failure leaves partial output.

## Source and method

The evaluated skill source is commit `3c011eac6e56e0524b36a5b009343a35b79550a9`, based on `03282e6de04574f1a452be20fc4f1d4202912054`.
The prompts supplied `SKILL.md` and `references/tasks/burndown-ready-queue.md` paths and each actor's Situation. They did not include grading criteria.
The parent used native Codex subagents through `collaboration.spawn_agent` with `fork_turns=none`. The tool did not report a runner version.
The requested actor model was `gpt-6.1-sol/high`; the author model was `gpt-6-luna/high`.
The dispatch specified both models, but runtime model attestation and full tool transcripts were unavailable.
The prompt prohibited commands, edits, network access, and user questions. These limits were prompt-enforced. The actors' credential-free environment was not verified.

## Results

| Scenario | Run | Grade |
|---|---|---|
| [Ready item beyond the default limit](../scenarios/ready-queue-beyond-default-limit.md) | `/root/scenario27_later` | Pass |
| [Later page fails](../scenarios/ready-queue-later-page-failure.md) | `/root/scenario27_failure` | Pass |

The parent agent (`gpt-6-astra/high`) graded both answers Pass. An independent `gpt-6.1-sol/high` reviewer confirmed both grades and found no actionable finding.
The raw answers are in [2026-10-08-ready-queue-discovery-answers.txt](2026-10-08-ready-queue-discovery-answers.txt).

## Controlled pagination check

GitHub CLI `2.101.0` ran the documented GraphQL query against a local HTTPS fixture with an isolated home and a synthetic token.
The first response had 100 items, `hasNextPage: true`, and cursor `cursor-100`. The next request carried that cursor. Its response had one Ready issue and `hasNextPage: false`.
In failure mode, the fixture returned HTTP 502 on page two. `gh` exited 1, but its output still contained page one and the error response. The caller must discard that output.
The command logs and fixture files are under `/private/tmp/ghflow-issue27-demo/`; `summary.txt` records the sanitized results.
This check demonstrates local cursor traversal and error handling. It does not validate GitHub's GraphQL schema or test a live board.

## Limits

Each decision scenario was sampled once. These results do not establish general reliability or task execution behavior.
The fixture used synthetic data and does not test an atomic board snapshot. Board changes during retrieval can still produce inconsistent data.

## Checks

`make check` passed on the committed source tree before this result record was added: 134 CLI tests, 10 script tests, `scripts/check.py`, and whitespace checks. The result and raw-answer files do not change the evaluated skill or scenarios.

## Coverage records

These records summarize the evidence in this report. Null values identify information that the report does not establish.

```scenario-results
[
  {"scenario": "ready-queue-beyond-default-limit", "date": null, "skill_commit": "3c011eac6e56e0524b36a5b009343a35b79550a9", "runner": "collaboration.spawn_agent", "model": "gpt-6.1-sol", "grade": "Pass", "phase": "sample", "note": "Dispatch selection, no runtime model attestation. Run date not stated; filename alone does not establish chronology.", "order": null},
  {"scenario": "ready-queue-later-page-failure", "date": null, "skill_commit": "3c011eac6e56e0524b36a5b009343a35b79550a9", "runner": "collaboration.spawn_agent", "model": "gpt-6.1-sol", "grade": "Pass", "phase": "sample", "note": "Dispatch selection, no runtime model attestation. Run date not stated; filename alone does not establish chronology.", "order": null}
]
```
