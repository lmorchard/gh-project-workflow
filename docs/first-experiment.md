# First experiment

This trial is complete. The [trial results](trials/2026-09-30-issue-843/review.md) record its outcome.

On 2026-09-30, Les selected issue definition as the first skill trial. The earlier PR review proposal is deferred. The trial uses [decafclaw issue 843](https://github.com/lmorchard/decafclaw/issues/843).

## Purpose

The skill must help an agent assess and improve an issue before implementation. A new agent session will use the draft skill. It will produce an issue draft without changes to GitHub or application code.

Les confirmed the intended result. An incompatible API change must cause the frontend type check to fail before release. The generated client must also load in the browser.

## Trial method

Give the agent the skill, issue URL, checkout path, and confirmed goal. Do not supply the earlier diagnosis or proposed first endpoint. This prevents the trial from supplying its own expected answer.

The agent can read GitHub and local code. It can write trial output in a separate temporary directory. It must return open questions rather than invent human approval.

## Evaluation

Examine the output for these results:

- Technical claims have sources in current code or issue records.
- Existing tests and proposed tests remain distinct.
- The draft preserves the confirmed goal.
- A smaller task has explicit limits and a relationship to the original issue.
- Unresolved product decisions remain visible.
- The agent does not change GitHub or application code.

Record missing information, unnecessary investigation, and repeated operations that a tool can help with. Do not build a CLI from guesses about those operations. One trial supplies an example, not proof that the skill works for every issue.
