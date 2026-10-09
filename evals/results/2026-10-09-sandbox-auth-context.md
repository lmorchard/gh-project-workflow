# Sandboxed GitHub authentication

One baseline sample was Partial. Both changed-skill samples passed. The baseline answer preserved the account and avoided a credential change, but it repeated `ghflow exec` outside the sandbox instead of checking the host keyring.

## Source and method

The baseline used the skill at `751e8d54ea5aeef2204c3bf1c95d1307a4e865e0`. The revised identity rule and scenario criteria are at `fa2ca6e1bb9f03d0ed4084a4188743edc0dc10e1`.
The parent dispatched fresh collaboration-agent contexts with `gpt-6.1-sol/high`, based on dispatch metadata. Runtime model attestation and native session IDs were unavailable. The parent authored the skill change, but its model variant was not recorded.

After the baseline answer, the parent clarified the criteria to require a host-keyring check without a `GH_TOKEN` override. The answer itself and situation did not change. The parent accepted this clarification because repeating the configured token-file command does not check the host keyring result.

Actors received the situation and paths to the relevant skill files. The prompts prohibited task commands, edits, network access, dispatch, and user questions. Read-only source inspection was allowed. Tool isolation and link traversal were not verified. Exact answers are in the [raw answers file](2026-10-09-sandbox-auth-context-answers.txt).

## Results

| Scenario | Phase | Run | Grade |
| --- | --- | --- | --- |
| [Sandboxed authentication](../scenarios/submit-pr-sandbox-auth-context.md) | Baseline | `baseline_sandbox_auth` | Partial: recognized a possible sandbox limit but repeated `ghflow exec` instead of checking the host keyring |
| [Sandboxed authentication](../scenarios/submit-pr-sandbox-auth-context.md) | Changed skill | `post_sandbox_auth_r1` | Pass |
| [Sandboxed authentication](../scenarios/submit-pr-sandbox-auth-context.md) | Changed skill | `post_sandbox_auth_r2` | Pass |

## Limits

These decision samples do not test real GitHub access or prove that credentials work in other execution environments. They used one baseline answer and two changed-skill answers from the same selected model. The parent graded the answers. Runtime identity and tool isolation were not verified.

## Checks

`make check` passed on the final source commit. It ran 134 CLI tests, 10 script tests, `scripts/check.py`, and the whitespace check.
