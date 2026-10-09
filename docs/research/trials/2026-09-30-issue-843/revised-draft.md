# Proposed child of #843: use the generated client for session lookup

Ready for implementation. Scope confirmed: only GET `/api/auth/me` through `AuthClient.checkSession()`. This draft does not authorize implementation or merge, and no GitHub changes have been made.

## Result

An incompatible change to the session response must cause the frontend type check to fail before release. The generated client used by `AuthClient.checkSession()` must load in a browser.

## Current problem

`/api/auth/me` already returns the typed `UserResponse` model, but `checkSession()` reads untyped JSON from `fetch`. The generated TypeScript client is unused and has no step that produces browser JavaScript. The frontend type checker can accept imports that a browser cannot resolve.

## Work

- Migrate `AuthClient.checkSession()` to the generated `/api/auth/me` method, retaining the generated response type through its use of `username`.
- Produce browser-loadable JavaScript for the generated client. Choose the compilation method during implementation; generated extensionless imports must resolve in the browser.
- Connect API generation, browser asset production or verification, and frontend type checking to `make check`. A clean checkout must work without leftover local output, and an obsolete generated client must not conceal a backend change.
- Replace the temporary test forbidding generated-client imports with appropriate checks. Retain the general static module import check.

## Success conditions

1. Session lookup uses the generated method and preserves existing behavior: an authenticated session returns the username and updates `currentUser`; an unsuccessful lookup returns `null` and clears `currentUser`. Add focused frontend tests, including a failed request after an earlier successful lookup.
2. Generation and `make check-js` pass for the unchanged application. Add an isolated regression test that renames the backend model's consumed `username` field, regenerates the client, and verifies that `make check-js` fails at the unchanged `checkSession()` caller. Check the compiler diagnostic so dependency or setup failures cannot count as success. The unchanged comparison must pass.
3. From clean generated outputs, the normal build creates assets that a real browser can load through `/static`. Add a browser check that imports the migrated client and successfully performs session lookup against a test server, without missing modules or JavaScript errors. The existing filesystem import check alone does not establish this.
4. CI's `make check` uses current backend-derived types and checks the browser assets. Demonstrate that stale or missing generated outputs cannot produce a successful check while leaving an incompatible caller or broken browser import.

Run existing authenticated/unauthenticated `/api/auth/me` assertions in `tests/test_web_auth.py` and the static module graph checks as regression protection. Run normal project checks during implementation. The new checks above must be added; none were executed during issue definition.

## Boundaries

Login, logout, every other endpoint, and authentication-rule changes are out of scope. Preserve current endpoint responses and session behavior. FastAPI and OpenAPI generation are already chosen; no framework decision is required.

This child proves that a consumed backend response type reaches an actual frontend caller, that an incompatible change is detected, and that the generated client can execute in a browser. It does not establish type safety for the rest of the API, request bodies, path/query parameters, or handlers hidden by the authentication decorator. Those remain in #843. Compatible additive API changes need not fail type checking.

## Evidence

Inspected revision: `41811db089682a2952aa9573efeedfa263a3b05a`, matching remote main during review.

- `src/decafclaw/http_server.py:450`: `UserResponse` and `auth_me`; `:2496`: raw static-file serving.
- `src/decafclaw/web/static/lib/auth-client.js:20`: current session lookup.
- `src/decafclaw/web/static/lib/api-client/services/DefaultService.ts`: typed generated session method.
- `scripts/gen_api_client.py`, frontend `tsconfig.json`, and `Makefile`: generation and checking are separate; checking does not produce JavaScript.
- `tests/test_api_codegen.py`: file-existence and temporary no-import checks, not proof of type safety.
- `tests/test_web_static_module_graph.py`: filesystem import-resolution protection, not browser execution.

Parent: https://github.com/lmorchard/decafclaw/issues/843 . Background: https://github.com/lmorchard/decafclaw/issues/785 and https://github.com/lmorchard/decafclaw/pull/844 . Original issue text remains unchanged.
