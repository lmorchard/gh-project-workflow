# Parent issue #843 delivery retrospective

Date: 2026-10-02

[#843 is closed and Done](https://github.com/lmorchard/decafclaw/issues/843). All ten children from this run are merged. A fresh audit confirmed coverage on merged main. Final checks passed: 4,237 Python tests, two skips, and 395 JavaScript tests. No deployment or final manual smoke test occurred.

The process delivered the intended result, but the feedback loop was too expensive. The skills supported sustained work, corrections, recovery, and merges without repeatedly asking for authorization. They also let us preserve the parent’s scope while filing separate follow-ups. That is a useful foundation. We do not need more orchestration machinery to explain the problems we encountered.

Independent review and Copilot provided complementary value. They caught missing type protection, changed error handling, and inaccurate API contracts. However, favorable reviews repeatedly missed defects. Different models helped find more problems; they did not establish completeness. We need stronger inspection of actual callers, especially helper parameters, shared editor branches, and malformed-response behavior.

The largest preventable problem was test design. We accumulated browser scenarios in one roughly 1,000-line test. Shared state and unfinished requests let earlier actions interfere with later scenarios. Local runs passed, while slower hosted execution exposed those assumptions. [#894](https://github.com/lmorchard/decafclaw/issues/894) captures the refactor. The isolated browser scenario used for #884 worked better and gives us a concrete example to follow.

Our contract tests also needed better precision. Some tests allowed an error at one caller to conceal missing protection at another. Others checked deleted fields without checking incompatible field types. Several fixtures relied on globally unique source text that stopped being unique as the migration grew. These are specific lessons for this repository’s tests, not reasons to add a large universal validation scheme.

Scope control came too late on PR #893. Automatic reviews kept examining unchanged code after pushes made for other reasons. We initially treated additional contract precision as another required fix. The unused `content`/`body` combination showed why that needs judgment: the server already rejected it, and no UI caller sent it. Declining extra generator machinery was appropriate. Your decision to separate the Unicode download defect into [#895](https://github.com/lmorchard/decafclaw/issues/895) was another useful boundary.

I recommend small changes to the skills. In [implement-issue](../../skills/implement-issue/SKILL.md), add guidance about isolated asynchronous tests and operation-completion signals. In [review-changes](../../skills/review-changes/SKILL.md), emphasize tracing values through actual callers and comparing prior success and failure behavior. Keep migration-specific type checks in project guidance rather than making every review carry them.

For [address-pr-review](../../skills/address-pr-review/SKILL.md), make the stopping rule more explicit: assess new findings against the agreed result, distinguish regressions from pre-existing defects and optional improvements, and batch accepted corrections where possible. The skill already says to assess findings before editing. Our failure was partly inconsistent application, so more wording alone will not fix it.

Recovery mostly worked well. We survived unavailable models, capacity limits, and a server restart without duplicating implementation or PRs. But stale handoffs briefly moved the parent backward on the board, one commit identifier was copied incorrectly, and some test processes needed follow-up to collect their results. These support a small deterministic CLI utility for reading PR state, verifying commit identifiers, and applying board transitions. They do not yet justify another general-purpose harness.

CI cost and communication also need attention. Later Python jobs took about twenty minutes, making each correction expensive. We should measure test costs, share safe build fixtures, and avoid redundant checks. My updates became repetitive during those waits. Too many messages reported an unchanged pending check without helping you make a decision.

My recommended next step is a small, reviewed skill revision plus the test refactor in #894, then another bounded trial. I have not changed the skills during this retrospective. The aim should be fewer avoidable correction cycles and clearer decisions, with no new documentation ceremony.
