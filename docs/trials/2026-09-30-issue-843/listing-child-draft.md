# Reviewed definition handoff

Readiness: ready for implementation planning. No material user decision remains. This assessment does not authorize implementation or filing.
Repository: lmorchard/decafclaw. Requested parent: #843. Project: repository project 6. Labels, priority, size, and status remain unspecified.

## Proposed title

Use typed generated calls for active, archived, and system conversation folder listings

## Proposed issue body

Conversation browsing still uses handwritten requests and untyped response data. Incompatible backend changes can therefore pass frontend checks and break the sidebar.

Give the three existing listing callers generated contracts that detect incompatible query and response changes. Preserve their current browsing and failure behavior.

Parent: #843. Session and sticky foundations shipped through #861/#862 and #863/#864.

### Scope

- GET `/api/conversations` and `ConversationStore.listConversations()`.
- GET `/api/conversations/archived` and `ConversationStore.listArchivedConversations()`.
- GET `/api/conversations/system` and `ConversationStore.listSystemConversations()`.
- Their listing state, getters, and existing sidebar consumption, wherever annotations are needed to retain generated types.

Expose optional string `folder` query arguments and truthful response contracts. Each success envelope contains `folder`, `folders`, and `conversations`.

Active and archived items contain `conv_id`, `title`, `created_at`, and `updated_at`. System items contain `conv_id`, `title`, `conv_type`, and `updated_at`; they do not contain `created_at`.

Folder entries contain `name` and `path`. Active root virtual entries also contain `virtual: true`. Preserve the existing wire fields without manufacturing defaults or additional fields.

Use generated types through the real callers and listing state. Do not erase checks with `any`, broad objects, casts, or independently maintained replacement contracts.

Exclude conversation mutations, folder mutations, detail/history endpoints, exports, and WebSocket changes. A wider conversation-store or backend abstraction rewrite is not required.

### Success conditions

1. Generated methods accept optional string folders and return typed listing envelopes with the correct item shapes. Normal generation and frontend checks pass.
2. The existing store methods invoke those methods, update their respective state, and publish change events after successful responses.
3. Runtime tests invoke each real store method through the generated transport. Verify its route, query, returned listing state, and change event.
4. Cover omitted and empty root folders, plus nested folders containing spaces, Unicode, `&`, `+`, and `#` for active and archived listings. Verify one decoded `folder` value reaches the route, without truncation or double encoding.
5. Cover system root and its heartbeat, schedule, and delegated categories. Nested or unknown system folders retain HTTP 400; they are not valid browsing destinations.
6. Preserve authentication and user filtering, active/archive separation, virtual root folders, archived ancestor discovery, ordering, and delegated-user filtering. Preserve whitespace trimming and existing invalid-folder errors, including status codes rather than replacement 422 responses.
7. HTTP failures leave listing state unchanged and emit no change event or new error log. Transport and JSON-decoding failures retain their existing error logging and unchanged state.
8. Add isolated backend contract-change tests for every migrated operation. Change `folder` from string to integer, regenerate, and require an argument-type diagnostic at the unchanged store call.
9. Independently rename a consumed response-envelope field, such as `conversations`, regenerate, and require a missing-property diagnostic at the unchanged store read. Cover both regular and system contracts, and all migrated callers.
10. Each contract-change test first proves the baseline passes and verifies caller bytes remain unchanged. Installation, generation, or unrelated failures do not satisfy these tests.
11. Existing session, sticky, browser-build, and reconnect regressions remain green. Update the relevant API/frontend documentation with the implementation.

Use JS caller tests for state, publication, query construction, and failure semantics. Use authenticated HTTP tests for route behavior and filtering.

Include browser coverage using the emitted client against test routes, proving same-origin session cookies and actual query decoding. Extend the existing codegen regression harness for isolated contract changes.

Run `make check`, `make test-js`, and the applicable Python/browser tests during implementation. Follow the repository's normal test policy before review.

### Evidence and dependencies

Evidence revision: `8d8cc161364993d59de30b69472f42510333870b`, verified against GitHub main on 2026-10-01.

- [Store callers and state](https://github.com/lmorchard/decafclaw/blob/8d8cc161364993d59de30b69472f42510333870b/src/decafclaw/web/static/lib/conversation-store.js#L192): handwritten fetch calls, three envelope reads, and unchanged-state failure paths.
- [Listing handlers](https://github.com/lmorchard/decafclaw/blob/8d8cc161364993d59de30b69472f42510333870b/src/decafclaw/http_server.py#L465): folder parsing, success envelopes, authentication wrappers, and distinct system validation.
- [Item serialization and system discovery](https://github.com/lmorchard/decafclaw/blob/8d8cc161364993d59de30b69472f42510333870b/src/decafclaw/web/conversations.py#L63): different item shapes, ordering, and delegated-user filtering.
- [Existing route tests](https://github.com/lmorchard/decafclaw/blob/8d8cc161364993d59de30b69472f42510333870b/tests/test_web_conversations.py#L547): folder filtering, archived separation and ancestors, system categories, and invalid-folder responses.
- [Existing contract-change harness](https://github.com/lmorchard/decafclaw/blob/8d8cc161364993d59de30b69472f42510333870b/tests/test_api_codegen.py#L85): baseline checking, backend mutation, regeneration, expected caller diagnostics, and unchanged caller bytes.
- [Generated transport customization](https://github.com/lmorchard/decafclaw/blob/8d8cc161364993d59de30b69472f42510333870b/scripts/sticky_api_request.ts): current JSON/error compatibility handling applies only to sticky. Listing compatibility must be checked explicitly.

Existing tests provide regression fixtures and patterns. The listing runtime and contract-change tests described above still need implementation.

No new feature dependency is required beyond the delivered generation and browser-build machinery. No unresolved product decision remains.

## Definition evidence and review notes

Executed read-only GitHub queries for main SHA, #843 body/comments, and #861/#863 state. Main still matches the decomposition snapshot; both children are closed.

Inspected the pinned source snapshot at `/tmp/decaf-843-src`, supplied decomposition, skill research guide, and project instructions. No checkout, service, source, or GitHub mutations occurred.

Inspected test assertions in `tests/test_web_conversations.py:547–699`, `tests/test_system_conversations.py:151–160`, and `tests/test_api_codegen.py:68–115`. These demonstrate existing route cases, delegated filtering, and genuine unchanged-caller diagnostic checks respectively. No tests or builds ran during definition.

Generated `DefaultService.ts:100,122,133` currently exposes all three listings with no arguments and `CancelablePromise<any>`. Stock `core/generated-request.ts:50–79` already encodes scalar query values with `encodeURIComponent`; this alone does not prove real callers supply them. The actual migrated store methods must be exercised.

The scope is small enough to retain together: three adjacent handlers, three short parallel callers, one sidebar behavior, and two truthful item shapes. Splitting system into another issue adds overhead without resolving a demonstrated dependency or review-size problem.

Review corrected the decomposition's generic nested-folder criterion: only active/archived support nested browsing; system must preserve its restricted category semantics. Clarified that existing codegen tests are patterns, not completed listing oracles. Added explicit state/publication and malformed-JSON preservation to avoid accepting transport-only success.

Material user questions: none. Routine model names, adapter structure, and test organization remain implementation choices.
