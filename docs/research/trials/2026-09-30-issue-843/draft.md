# Proposed child of #843: prove REST contract checking and browser delivery with authentication

Status: needs one scope decision. This is a proposed first increment, not a replacement for #843's full REST migration. No GitHub edits have been made. The original issue body remains unchanged at https://github.com/lmorchard/decafclaw/issues/843.

## Intended result

An incompatible backend API change must make the frontend type check fail before release. The generated client must load in the browser. Prove both with the complete authentication route group first: POST `/api/auth/login`, POST `/api/auth/logout`, and GET `/api/auth/me`.

## Problem

The generated client currently cannot submit the login token and returns `any` for login/logout. The frontend uses untyped `fetch` responses. Although `/api/auth/me` has a response model, its generated client is unused. Generation produces TypeScript without browser JavaScript. The existing type checker does not emit JavaScript and can accept imports that browsers cannot resolve.

## Included work

- Describe the authentication request and success response shapes in FastAPI/OpenAPI, preserving current cookies, status codes, error handling, and wire responses. Define expected behavior for missing/invalid input explicitly in tests; do not accidentally replace current responses with FastAPI validation errors.
- Generate useful request and response types and migrate all three `AuthClient` operations to the generated client. Keep typed values intact through callers rather than casting them to `any`.
- After route typing, add a reproducible browser emit step and connect generation, emitted-asset verification, and frontend type checking to `make check`. The build must work from a clean checkout without relying on a developer's previously generated files. If outputs are committed, detect stale output rather than silently accepting it.
- Replace the temporary test forbidding generated-client imports with checks proving the migrated client is loadable. Keep the general static module graph guard.

Use the existing FastAPI and OpenAPI generator decisions. Recommended emit implementation: use the installed esbuild to produce a browser ESM client artifact and retain TypeScript declarations for checking. This avoids copying extensionless generated imports into raw-served JavaScript. A different emit implementation is acceptable if it meets the same checks; this tool choice does not require a separate user decision.

## Success conditions

1. The generated authentication methods accept the login body and return concrete response models. Add schema/client tests for the actual token and response fields, not merely file existence or a text search for a model name. Confirm that invalid typed arguments/field accesses fail compilation.
2. With the unmodified application, generation and `make check-js` succeed. In an isolated test checkout, change a consumed backend response field incompatibly (for example, rename `username`), regenerate, and assert that `make check-js` fails at the unchanged real frontend caller. Assert a relevant compiler diagnostic, so an installation error cannot satisfy the test. Restore the fixture and demonstrate success. Add this test; no existing inspected test proves it.
3. Starting with clean generated outputs, the normal build produces assets that a real browser can import through the application's `/static` mount. Add a browser smoke check that imports the migrated client/app graph and performs an authentication request against a test server, with no module-load error or missing asset. The structural module graph test remains useful but alone does not prove JavaScript executes.
4. CI invokes the composed `make check` gate. A backend-only incompatible change is caught using freshly generated types before release. Include an isolated stale-output or missing-output check that proves the gate cannot accept an obsolete client.
5. Authentication behavior remains compatible: valid token login sets the session cookie and returns the username; invalid tokens are rejected; authenticated session lookup returns the username; unauthenticated lookup is rejected; logout clears the session. Run the existing assertions in `tests/test_web_auth.py` plus frontend coverage for `currentUser`, login/logout events, and failure behavior. Run the repository's normal regression gates during implementation.

## Limits and dependencies

This increment does not type conversation, workspace, schedule, or other REST routes and does not change WebSocket contracts. It does not claim every API change must fail compilation: additive compatible changes can pass, and untouched routes remain outside this increment's guarantee. Follow-up route-group migrations remain in #843, including path/query parameters hidden by `_authenticated` wrappers. The auth slice proves request/response typing and browser delivery, but does not solve that decorator problem.

Depends on the already merged FastAPI/codegen work (#785 / #825) and the hotfix/guards (#844). No new framework decision is needed. Authentication changes warrant careful review but do not require redesigning authentication.

## Decision needed

Approve authentication as the first separately useful increment while retaining #843 for the full route migration? Recommended: yes. It gives a small end-to-end proof near the original broken importer; the tradeoff is that conversation path/query typing remains for a later increment. If all route groups must ship together, this child scope should not be adopted.

## Evidence

Inspected revision: `41811db089682a2952aa9573efeedfa263a3b05a` (matched GitHub main during this review).

- `src/decafclaw/http_server.py:101`: decorator presents only a Request argument; `:426` authentication handlers; `:450` UserResponse; `:2422` auth route registrations; `:2496` raw static mount.
- `src/decafclaw/web/static/lib/auth-client.js:20`: frontend session/login/logout calls use fetch and read username.
- `src/decafclaw/web/static/lib/api-client/services/DefaultService.ts:60`: generated login takes no arguments; auth-me is typed.
- `src/decafclaw/web/static/tsconfig.json`: noEmit with bundler resolution; `scripts/gen_api_client.py:11`: generation writes schema/client into the checkout.
- `tests/test_api_codegen.py:24`: output existence test; `:38`: temporary no-import guard. Neither proves type safety.
- `tests/test_web_static_module_graph.py:89`: filesystem resolution guard, excluding vendor and bare imports.
- `Makefile:66`, `:105`, `:224`; `.github/workflows/ci.yml`: frontend check is composed into make check, but API generation is currently separate.

History: https://github.com/lmorchard/decafclaw/issues/785 ; https://github.com/lmorchard/decafclaw/pull/825 ; https://github.com/lmorchard/decafclaw/pull/844 . All proposed new checks above remain to be implemented and executed.
