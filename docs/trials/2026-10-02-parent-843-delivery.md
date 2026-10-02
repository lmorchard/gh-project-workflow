# Parent issue #843 delivery retrospective

Date: 2026-10-02

This record preserves the session retrospective and the handoff facts. Recommendations remain proposals. No skill changes were made during this wrap-up.

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


## Completion evidence and scope decisions

The subject project was [lmorchard/decafclaw](https://github.com/lmorchard/decafclaw). Its checkout was `/Users/lmorchard/devel/mine/decafclaw`. Subject agents made its code and GitHub changes. The parent agent maintained the workflow and user conversation.

GitHub readback recorded parent #843 as closed and Done at `2026-10-02T05:03:10Z`. The audited main commit was `b8ca40cebaf92838307cd0a49f7a9002ffb12aa0`. All 17 children were closed at that time. Seven children preceded this delivery run.

The ten children delivered in this run are linked here:

| Child | Work | Merged PR |
|---|---|---|
| [#875](https://github.com/lmorchard/decafclaw/issues/875) | Context inspection and text export | [#885](https://github.com/lmorchard/decafclaw/pull/885) |
| [#876](https://github.com/lmorchard/decafclaw/issues/876) | Notifications | [#886](https://github.com/lmorchard/decafclaw/pull/886) |
| [#877](https://github.com/lmorchard/decafclaw/issues/877) | Canvas and widget catalog | [#887](https://github.com/lmorchard/decafclaw/pull/887) |
| [#878](https://github.com/lmorchard/decafclaw/issues/878) | Workspace reads and autocomplete | [#888](https://github.com/lmorchard/decafclaw/pull/888) |
| [#879](https://github.com/lmorchard/decafclaw/issues/879) | Workspace writes | [#889](https://github.com/lmorchard/decafclaw/pull/889) |
| [#880](https://github.com/lmorchard/decafclaw/issues/880) | Vault reads | [#890](https://github.com/lmorchard/decafclaw/pull/890) |
| [#881](https://github.com/lmorchard/decafclaw/issues/881) | Vault writes | [#891](https://github.com/lmorchard/decafclaw/pull/891) |
| [#882](https://github.com/lmorchard/decafclaw/issues/882) | Configuration editing | [#892](https://github.com/lmorchard/decafclaw/pull/892) |
| [#883](https://github.com/lmorchard/decafclaw/issues/883) | Schedules and model choices | [#893](https://github.com/lmorchard/decafclaw/pull/893) |
| [#884](https://github.com/lmorchard/decafclaw/issues/884) | Upload and native file delivery | [#896](https://github.com/lmorchard/decafclaw/pull/896) |

Each merge required affirmative independent review and successful hosted CI for the final commit. CI is the service that runs published checks. Copilot review was preferred, but a literal GitHub approval was not required.

PR #893 is an important exception to a simple “Copilot approved” summary. Its latest review questioned the unused `content` and `body` combination. No web UI caller sent both fields. The agent explained why it left runtime rejection unchanged and declined extra generated TypeScript machinery. Independent review supported that scope decision. Successful CI and affirmative independent review supported the merge.

Les explicitly chose a separate issue for the pre-existing Unicode download failure. Issue #895 remains separate from #884 and parent completion. Issue #894 records the browser-test refactor. Both were filed as P2 triage work outside the active project board. Neither is a new requirement for closing #843.

The audit covered in-repository web UI REST callers, shared editor hosts, standalone pages, text export, multipart upload, and native URL builders. It found no unexplained handwritten requests within that boundary. Unused routes and WebSocket protocols remained excluded. The audit did not establish coverage of unknown externally installed widgets.

The pre-existing schedule navigation race remains a known limitation. The test waits for the prior save to finish before navigating. This test correction does not fix the application race. No separate issue for that race was filed in this session.

No deployment, final manual smoke test, credential copying, branch removal, or worktree cleanup occurred. Branches and worktrees remain available. The shared checkout was intentionally not reset to main.

## Recovery facts for the next session

Native agent dispatch hit capacity limits. A server restart interrupted coordination while a CLI reviewer continued. Recovery inspected existing processes, commits, PRs, and reviews before retrying actions. This prevented duplicate implementations and PRs.

The runtime rejected `gpt-6-astra` during the run. Later implementation used explicitly selected `gpt-5.6-sol`, with `gpt-5.6-terra` for independent review. CLI startup logs supplied model evidence when native dispatch was unavailable. These are historical observations, not permanent model choices. Model availability requires a fresh check in a future session.

Some agents treated sandbox setup failures as evidence limits before trying permitted escalation. One reviewer returned before collecting a yielded tool result. Recovery collected targeted results and made sure that no test process remained active. Tests that install JavaScript packages must stay separate from concurrent tests that use or copy those packages.

GitHub GraphQL rate limits interrupted some board readbacks. Later reads completed those checks. Empty requested-reviewer lists did not mean that Copilot never received a request. Timeline events supplied the original request time. Review deadlines did not restart after corrective pushes.

An HTTPS push failed because of authentication configuration. Explicit `ssh://git@github.com/lmorchard/decafclaw.git` worked in this session. No Git configuration change was needed. A future agent must inspect its own environment rather than assume the same failure.

## Proposed next work

First, revise the few skill passages identified in the retrospective and assess them with another bounded trial. Do not add mandatory reports or another control program. Existing instructions already cover several failures observed here.

Keep project-specific contract-testing lessons near the relevant tests. Examples include helper parameter types, incompatible field types, route-specific mutation targets, and caller-specific response parsing. A general workflow skill does not need all those implementation details.

Issue #894 is the proposed test-maintenance task. Issue #895 is a separate product bug. Neither task started during this session. Skill edits, a new CLI utility, and further delivery also remain proposals for the next session.
