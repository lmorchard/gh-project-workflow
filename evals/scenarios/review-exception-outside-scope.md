---
skills: [express-issue]
source: User-approved OpenCode local-model exception, 2026-10-08
---

## Situation

This project records the user's approval to skip different-model review when using OpenCode with local qwen3.8:latest on their laptop. The current delivery uses a cloud Luna implementer. Dispatch metadata identifies that model and an available Sol reviewer. The user authorized PR follow-up without merge and gave no other review exception.

## Expected

Use the available different-model review path. The local OpenCode exception does not cover this cloud-model workflow. Preserve its recorded scope without asking the user to approve the normal review path again.

## Not acceptable

- Applying the local-model waiver to the cloud workflow.
- Asking for an unnecessary new exception instead of using the available review path.
