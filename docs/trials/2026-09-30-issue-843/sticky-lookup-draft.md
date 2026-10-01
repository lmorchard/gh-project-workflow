# Reviewed issue draft

Title: Use typed generated API calls for sticky-state lookup by conversation ID

Parent: https://github.com/lmorchard/decafclaw/issues/843
Repository: lmorchard/decafclaw
Readiness: ready for implementation. Les confirmed this operation and its existing caller. No material user decisions remain. This assessment does not authorize implementation or filing.

## Proposed body

Parent: #843.

The web UI restores its pinned widget through `GET /api/sticky/{conv_id}`. Its hand-written request discards generated types. The generated method also accepts no identifier and returns `any`.

Make `sticky-state.js:setActiveConv()` use a generated method with usable identifier and response types. Incompatible contract changes must fail at this unchanged application caller. Preserve sticky-slot behavior.

### Scope

Cover this GET operation and its existing caller only. Keep the current FastAPI, OpenAPI generation, esbuild output, and session migration from #861/#862.

The response contract covers its envelope: required `widget_type` and `data` properties. `widget_type` is a nullable string. `data` holds a nullable object with heterogeneous widget content. Preserve that content, including nested values and unknown properties. Do not make the whole response `any` or erase its type at the caller.

This slice does not type each widget's payload fields or their relationship to `widget_type`. Keep existing widget validation. Widget-schema redesign, other routes, conversation listing, and WebSocket protocol changes are excluded.

### Success conditions

**The real caller uses a usable generated contract.**

The generated method requires a string conversation identifier and returns the typed envelope. `setActiveConv()` passes the identifier and reads generated response properties without casts that discard their types.

Add a runtime test through `setActiveConv()` and the real generated method. Verify the requested identifier reaches the correct path, with no unresolved placeholder. Preserve path-segment encoding and same-origin session credentials. Confirm the returned widget type and payload reach `currentSnapshot()`.

Use a safe identifier for successful server lookup. Separately test characters needing encoding, so they cannot become query strings or fragments. This encoding check does not broaden accepted server identifiers.

**Incompatible inputs and outputs fail at the unchanged caller.**

Add isolated tests following `tests/test_api_codegen.py`'s existing response-drift pattern. Begin with successful generation and `make check-js`.

Change the backend identifier contract incompatibly, such as changing its type from string to integer. Regenerate without editing the application caller. Require the type check to fail at the caller's argument.

Separately rename the consumed `widget_type` response field in the backend contract. Regenerate without editing the application caller. Require a missing-property error at its existing field access.

Inspect compiler diagnostics in both tests. Installation failures or unrelated errors cannot satisfy them. Compatible additions need not fail. These checks establish envelope and argument protection, not widget-specific payload typing.

**Sticky-state behavior stays the same.**

Add frontend tests for these results:

- Successful lookup restores widget type and payload. An empty response clears the cached widget.
- No active identifier sends no request and publishes an empty snapshot.
- A failed HTTP response retains cached state and publishes without adding a warning.
- Transport or JSON-decoding failure retains cached state, warns, and publishes.
- Conversation switches preserve separate caches and collapse preferences. Reconnection reloads the active conversation.

Keep subscription publication and existing WebSocket sticky updates working. Do not introduce new request triggers or change unrelated request handling.

**The route retains its current behavior.**

Keep the existing pinned-widget, empty-state, authentication, and ownership tests in `tests/test_http_sticky.py`.

Strengthen authentication coverage to assert the current 401 response. Add coverage for invalid identifiers returning 400 and missing conversations returning 404. Preserve other-user 404 responses.

Exercise nested heterogeneous payloads and confirm the response preserves them. Keep the absent/corrupt-sidecar behavior covered by `tests/test_sticky.py`.

**Existing build and session guarantees remain intact.**

Run `make check`, `make test-js`, and `make test` during implementation. Preserve #862's browser-loading, regeneration, and session response-drift regressions. Update relevant API-build documentation for this additional typed caller.

### Evidence and limits

Definition inspected GitHub main `9909cf1997c7ba8fd0c31e86cbc627c4cd5c1aeb`. No tests or builds ran during definition; new caller and drift tests require implementation.

Relevant sources at that revision:

- [Sticky caller and cache](https://github.com/lmorchard/decafclaw/blob/9909cf1997c7ba8fd0c31e86cbc627c4cd5c1aeb/src/decafclaw/web/static/lib/sticky-state.js#L68).
- [Conversation-change trigger](https://github.com/lmorchard/decafclaw/blob/9909cf1997c7ba8fd0c31e86cbc627c4cd5c1aeb/src/decafclaw/web/static/app.js#L98).
- [Sticky GET handler](https://github.com/lmorchard/decafclaw/blob/9909cf1997c7ba8fd0c31e86cbc627c4cd5c1aeb/src/decafclaw/http_server.py#L2047).
- [Generated method](https://github.com/lmorchard/decafclaw/blob/9909cf1997c7ba8fd0c31e86cbc627c4cd5c1aeb/src/decafclaw/web/static/lib/api-client/services/DefaultService.ts#L660).
- [Existing HTTP tests](https://github.com/lmorchard/decafclaw/blob/9909cf1997c7ba8fd0c31e86cbc627c4cd5c1aeb/tests/test_http_sticky.py#L108).
- [Existing response-drift test](https://github.com/lmorchard/decafclaw/blob/9909cf1997c7ba8fd0c31e86cbc627c4cd5c1aeb/tests/test_api_codegen.py#L66).

## Handoff evidence, outside proposed body

Confirmed decision: replace the metadata lookup candidate with GET /api/sticky/{conv_id} and its actual web UI caller. Metadata GET has no observed web UI caller. Do not reopen the selected operation or #862's build decisions.

Source revision: local subject checkout remains clean at `41811db089682a2952aa9573efeedfa263a3b05a`. GitHub main is one commit ahead at `9909cf1997c7ba8fd0c31e86cbc627c4cd5c1aeb`. Read that exact source snapshot under `/tmp/decafclaw-lookup-main`. GitHub comparison shows sticky files unchanged; #862 supplies the current generation and test pattern.

Observed behavior:

- `sticky-state.js:68-86` sets the active identifier immediately, then fetches. A truthy identifier creates or reuses its cache. Successful JSON replaces widget/data using existing falsy-to-null fallback. Non-OK HTTP responses skip assignment. Caught errors warn. All paths publish; empty identifiers publish immediately without fetching.
- `sticky-state.js:118-123` reloads active state on `ws-connected`. Collapse preferences remain in localStorage. `app.js:98-101` triggers on active-conversation changes.
- `http_server.py:2047-2062` checks safe identifiers, then ownership, then returns only widget_type/data. `_authenticated` at line 94 returns 401. `_is_safe_conv_id` at line 61 accepts letters, digits, dot, underscore, and hyphen. `_user_owns_conv` at line 2024 requires an existing owned conversation.
- `sticky.py:38-48` treats missing, unreadable, or invalid-JSON sidecars as empty. `set_sticky` validates widget-specific data before saving. This migration need not add new runtime validation of historical sidecars.
- Existing HTTP tests assert pinned payload, null fields when unset, other-user 404, and auth denial loosely as one of 401/302/403. They do not currently establish generated arguments or frontend types.
- Existing sticky persistence tests assert round-trip, missing/corrupt fallback, pin/clear state, and registry rejection. Their assertions were read, not executed.
- No `sticky-state.test.js` exists in the inspected frontend. New caller coverage is required.
- Generated request runtime defaults to `encodeURI`; the existing caller uses `encodeURIComponent`. Preserve segment encoding within this operation's scope; do not silently change every generated request.
- Generated HTTP errors throw while the old caller silently ignores non-OK responses. Preserve its cache, publication, and warning distinction.
- The caller currently has an unannotated parameter and a broadly inferred cache. Parameter drift requires retaining a concrete string type at the call boundary. Routine annotations are implementation choices.
- `tsconfig.json` checks JavaScript with strict mode disabled. Response-field rename remains a meaningful diagnostic despite loose cache types. Do not claim this slice proves full null-safety or per-widget payload typing.

Checks executed: git status/revision reads, GitHub issue/PR/compare reads, source snapshot extraction, source searches, and test-assertion inspection. No tests, builds, browser sessions, services, subject edits, commits, branch changes, or GitHub writes occurred. Metadata remains unspecified beyond repository and parent.

Self-review: replaced the nonexistent metadata caller with the user-confirmed operation. Distinguished proposed tests from existing evidence. Added cache/error, credential, and encoding preservation after comparing generated runtime behavior. Scoped the type guarantee to the envelope and argument. No material unresolved questions remain.

## Suggested narrow correction to parent #843, not published

Replace only its “Next task to define” operation paragraph with:

> Type `GET /api/sticky/{conv_id}` and migrate its existing web UI caller, `sticky-state.js:setActiveConv()`. Cover the identifier argument and response envelope while preserving current behavior and heterogeneous widget data. Conversation listing and other route groups remain separate work under this parent.

The metadata GET has no web UI caller and remains outside the parent's confirmed completion boundary. Keep the remainder of #843 unchanged. This handoff grants no GitHub-write authorization.
