# Proposed reconsideration of decafclaw #843 — not published

Recommendation: revise and keep the issue open. Browser compilation and the typed session caller have landed, while route typing and migration of the remaining callers are incomplete.

Issue state recommendation: **Open**. Board recommendation: **Backlog, tentative**, depending on the project's conventions for umbrella issues. The current Ready status alone does not establish that it is wrong. Remaining work needs bounded implementation tasks; if Ready intentionally holds actionable parent issues, retaining it is reasonable.

## Proposed title

Complete typed REST routes and migrate remaining frontend callers to the generated client

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

### Remaining work

- Give the remaining route groups explicit path/query parameters and request/response contracts, incrementally.
- Migrate their frontend callers to the generated methods without discarding the generated types.
- Preserve endpoint behavior, authentication rules, and the existing browser-build and session regressions.
- Add checks for each migrated group that exercise generated arguments and demonstrate that incompatible contract changes fail at unchanged callers.

### Proposed success conditions

- Generated methods expose the actual inputs and output contracts for the routes covered by the original REST migration.
- Their frontend callers use those contracts.
- Deliberate incompatible changes to consumed request or response fields fail the frontend check for the expected type error. Compatible additions need not fail.
- Runtime tests preserve the routes’ behavior and demonstrate that migrated generated calls send the required path/query/body data.
- Normal project checks and existing browser-loading regressions pass.

### Next boundary to define

Define a first remaining route group rather than treating this parent as one ready implementation task. A useful next slice is conversation reads: type the relevant path/query/response contracts and migrate their consumers. Keep other route groups tracked by this parent.

Confirm how completion will account for non-JSON responses and legacy aliases. Do not silently drop them from the original scope.

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

Recommend conversation reads as the next slice: it demonstrates path/query/response typing, while login/logout would be smaller. Parent closure does not depend on choosing that slice now; it is clearly incomplete. Resolve treatment of non-JSON routes and legacy aliases before claiming the whole goal complete.
