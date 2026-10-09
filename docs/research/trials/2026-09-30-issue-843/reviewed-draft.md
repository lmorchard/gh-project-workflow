# Use the generated API client for the browser session check

Parent issue: [#843](https://github.com/lmorchard/decafclaw/issues/843).

Make `AuthClient.checkSession()` use the generated client for `GET /api/auth/me`. An incompatible change to the response must cause the frontend type check to fail before release. The generated client must also load in the browser.

## Current problem

The endpoint already declares its response through `UserResponse`. However, `checkSession()` uses `fetch` and reads JSON without the generated type information. The generated client contains TypeScript files, but the project does not produce JavaScript for browser use.

The current type check can accept an import that the browser cannot load. Existing tests detect some missing files. They do not demonstrate that the generated client executes in the browser.

## Scope

This issue covers only the session check through `GET /api/auth/me`. Login, logout, other endpoints, and authentication-rule changes are outside its scope. Keep the current endpoint responses and session behavior.

The implementation includes these changes:

- Use the generated session method in `AuthClient.checkSession()` without discarding its response type.
- Produce JavaScript that the browser can load.
- Connect generation and browser-asset checks to `make check`.
- Replace the temporary test that prohibits imports of the generated client.

Select the compilation method during implementation. Keep the existing FastAPI and OpenAPI generator. Other endpoint migrations remain in #843.

## Success conditions

### Session behavior stays the same

An authenticated session returns the username and updates `currentUser`. An unsuccessful lookup returns `null` and clears `currentUser`. Add frontend tests for these results, including a failed request after an earlier successful lookup.

### An incompatible response change fails the type check

Add an isolated test that renames the consumed `username` field in the backend response model. Regenerate the client without changing the frontend caller. Make sure that `make check-js` fails because the caller uses the old field.

Examine the compiler error so an installation problem cannot satisfy this test. The unchanged application must pass the same generation and type-check steps. This proposed test does not exist in the inspected files.

### The browser loads and uses the client

Start without previously generated output. Produce the browser files through the normal build procedure. Use a real browser to load the migrated client through `/static` and do a session lookup against a test server.

The lookup must succeed without missing modules or JavaScript errors. The existing test for file paths does not establish this behavior. Add a browser test for this result.

### Project checks detect outdated or missing output

CI is the service that does automated project checks. Its `make check` command must use types from the current backend definitions. It must also detect missing browser files.

Add isolated tests for outdated and missing generated output. The checks can rebuild that output or fail with an error. They must not pass while the caller uses incompatible types or the browser lacks a required module.

## Existing behavior to protect

Keep the static module import test. Keep the authenticated and unauthenticated session assertions in `tests/test_web_auth.py`. Do the normal project checks during implementation.

This issue proves response typing for one real caller and browser use of the client. It does not prove typing for other endpoints or request parameters. Compatible additions to the API do not have to fail the type check.

## Evidence and limits

The review inspected revision `41811db089682a2952aa9573efeedfa263a3b05a`. It did not execute tests, builds, or browser checks. The proposed new tests require implementation.

Relevant files include:

- `src/decafclaw/http_server.py:450`: response model and session endpoint.
- `src/decafclaw/web/static/lib/auth-client.js:20`: current session request.
- `src/decafclaw/web/static/lib/api-client/services/DefaultService.ts`: generated session method.
- `scripts/gen_api_client.py`: schema and client generation.
- `src/decafclaw/web/static/tsconfig.json`: frontend type-check configuration.
- `Makefile`: generation and project-check commands.
- `tests/test_api_codegen.py`: generated-file tests and temporary import prohibition.
- `tests/test_web_static_module_graph.py`: local import-path tests.
