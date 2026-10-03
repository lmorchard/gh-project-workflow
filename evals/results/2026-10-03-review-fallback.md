# Review fallback scenarios, 2026-10-03

Les decided that when Copilot is unavailable or its review times out, a different-model local review is the review source, without a question to him. The identity trial supplied the case of a request that GitHub does not record: `gh pr edit --add-reviewer "@copilot"` exited 0 for a PR whose author had no Copilot access, and no request appeared.

- Agent model: Claude Sonnet, one fresh agent per run.

## Baseline at `33463e6`

- **copilot-request-silent-local-covers** failed 1 of 1. The agent correctly did not wait for an unrecorded request, but it returned the fallback choice to the parent, as address-pr-review then required.
- **copilot-unavailable-head-changed** passed 1 of 1. The coordinator dispatched a different-model review of the uncovered change without a question, under express-issue's rule to have the reviewer assess changed code.

## After the changes

review.md now says that a request command can exit 0 without a recorded request, that such a case means Copilot is unavailable, and that a different-model local review is then the review source. address-pr-review uses a local review of the current head, or hands off a review of the uncovered changes, after Copilot is unavailable or a review times out.

- **copilot-request-silent-local-covers** passed 2 of 2.
- **copilot-unavailable-head-changed** passed 1 of 1.
- **review-timeout** passed 2 of 2 after its expected decision changed with Les's timeout decision. The agents reported the timeout as an incomplete review, not as unavailability, and handed off a local review without a question.
- **copilot-automatic-request** (regression) passed 1 of 1. A recorded automatic request is still pending, not unavailable.
- An ad hoc regression, with a request 6 minutes old and a local review that covered the head, passed 1 of 1. The agent kept waiting until the deadline and kept the local review as the fallback.
