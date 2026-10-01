# Proposed reconsideration of decafclaw #843 — not published

Recommendation: revise and keep the issue open. Browser compilation and the typed session caller have landed, while route typing and migration of the remaining callers are incomplete.

Issue state recommendation: **Open**. Board recommendation: **Backlog, tentative**, depending on the project's conventions for umbrella issues. The current Ready status alone does not establish that it is wrong. Remaining work needs bounded implementation tasks; if Ready intentionally holds actionable parent issues, retaining it is reasonable.

## Proposed title

Complete typed API calls used by the web UI

## Proposed body

Follow-up to #785 / PR #825 and the browser-loading hotfix #844. This issue retains the goal of typed REST contracts and frontend callers that detect incompatible backend changes before release.

### Completed

Child #861 was completed by #862, merged at `9909cf1997c7ba8fd0c31e86cbc627c4cd5c1aeb`.

- `make gen-api-client` now generates TypeScript and bundles browser JavaScript with esbuild.
- `AuthClient.checkSession()` uses the generated `GET /api/auth/me` method and retains its `UserResponse` type.
- `make check` regenerates the client and verifies browser module paths.
- Tests cover session success and failure, rebuilding missing generated output, rejecting missing browser modules, an incompatible response-field change at the unchanged caller, and a clean-built client executing in Chromium against test routes.

The missing JavaScript and “generated-but-unimported” descriptions are historical. The compilation method is implemented; choosing it again is not remaining work.

### Remaining problem

Other generated operations still lack usable contracts. For example, `wrapperApiConversationsIdGet()` takes no arguments and returns `CancelablePromise<any>` despite requesting `/api/conversations/{id}`. The backend reads the identifier from `request.path_params`, behind an authentication wrapper whose exposed signature contains only `Request`.

Frontend calls remain hand-written in `conversation-store.js`, and authentication login/logout still use `fetch`. The session migration establishes response typing for one caller; it does not establish request typing or typed coverage of the remaining REST API.

### Confirmed scope

Les selected the web UI boundary in the reconsideration interview. Completion covers REST endpoints used by the web UI and their actual callers. Endpoints without web UI callers remain follow-up work outside this issue. This boundary ties completion to observable caller behavior instead of requiring every backend endpoint to migrate first.

Web UI calls with non-JSON responses remain in scope unless a later decision explicitly excludes them. Legacy aliases matter here only when the web UI uses them. An inventory of callers must identify these cases before claiming completion. This scope decision does not authorize publication or implementation.

### Remaining work

- Give the remaining routes used by the web UI explicit path/query parameters and request/response contracts, incrementally.
- Migrate their frontend callers to the generated methods without discarding the generated types.
- Preserve endpoint behavior, authentication rules, and the existing browser-build and session regressions.
- Add checks for each migrated group that exercise generated arguments and demonstrate that incompatible contract changes fail at unchanged callers.

### Success conditions

- Generated methods expose the actual inputs and output contracts for REST routes used by the web UI.
- Their frontend callers use those contracts.
- Deliberate incompatible changes to consumed request or response fields fail the frontend check for the expected type error. Compatible additions need not fail.
- Runtime tests preserve the routes’ behavior and demonstrate that migrated generated calls send the required path/query/body data.
- Normal project checks and existing browser-loading regressions pass.

### Confirmed next child

Les selected one conversation lookup by ID and its real web UI caller as the next child. Give that call usable generated parameter and response types while preserving existing behavior. Conversation listing and other routes remain outside this child and tracked by the parent.

Identify non-JSON responses and legacy aliases among actual web UI calls during decomposition. Record endpoints outside the confirmed boundary as follow-up work.

## Evidence and execution limits

- Read the issue and comments, [#785](https://github.com/lmorchard/decafclaw/issues/785), [#825](https://github.com/lmorchard/decafclaw/pull/825), [#844](https://github.com/lmorchard/decafclaw/pull/844), child [#861](https://github.com/lmorchard/decafclaw/issues/861), and merged [#862](https://github.com/lmorchard/decafclaw/pull/862). The child explicitly leaves other endpoint migrations in #843.
- Local checkout was clean at `41811db089682a2952aa9573efeedfa263a3b05a`; remote main was `9909cf1997c7ba8fd0c31e86cbc627c4cd5c1aeb`. Inspected an archive of the exact remote revision under `/tmp`; did not update the subject checkout.
- Inspected `scripts/gen_api_client.py`, `Makefile`, `http_server.py`, `auth-client.js`, generated `DefaultService.ts`, `conversation-store.js`, current codegen/session/static-module tests, and CI configuration at that revision. The generated conversation-get method still has no identifier argument and returns `any`.
- Executed both static module graph test functions directly with stdlib `runpy`; both passed. This was not a pytest suite or browser run. Did not locally execute generation, full checks, drift tests, or Chromium.
- GitHub reports successful `lint-and-test`, `js-test`, and `check-tui` checks on the exact merged revision: [main CI run](https://github.com/lmorchard/decafclaw/actions/runs/36807560273). This is historical CI evidence, not a local rerun or deployment evidence.
- Read actual project status options: Backlog, Ready, In progress, In review, Done. No evidence established the project's treatment of partially completed umbrella issues.
- The old acceptance comment should be superseded: the module-path check passes today and guards runtime file resolution; it does not establish complete API typing. Its description of `test_api_codegen.py` as asserting non-`any` models across route groups does not match current assertions.
- No GitHub writes, branch changes, deployment, or service operations were performed.

## Skill feedback and next decision

No blocking ambiguity in the skill. It requires current-revision evidence and correctly separates child completion from parent completion. It leaves umbrella board-status conventions to judgment, so the Backlog recommendation remains tentative.

The user selected one conversation lookup by ID and its web UI caller as the next child. This adds evidence for generated request parameters after the completed session response example. Parent closure does not depend on choosing that slice now; it is clearly incomplete. The web UI boundary is confirmed. Identify its callers before claiming the whole goal complete.
