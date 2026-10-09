# Revision after confirmed scope decision

Preserved draft.md and evidence-report.md. Created revised-draft.md using the confirmed scope: GET /api/auth/me through AuthClient.checkSession() only.

The revised child is ready for implementation. No remaining user decision is necessary. Compilation method and generated-output handling are implementation choices constrained by clean-build, type-check, and browser checks.

Removed login/logout migration and all authentication-rule changes. Kept the actual backend-change-to-frontend-failure test and browser execution requirement. Explained that this proves response-type coupling and browser delivery, while other endpoints, request bodies, path/query parameters, and decorated handlers remain in #843.

No further investigation or checks were performed. Evidence and execution limits from evidence-report.md still apply. No GitHub, application, project-document, or git-ref changes were made.
