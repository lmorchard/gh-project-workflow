---
skills: [define-issue, file-issue]
source: a4626c2
---

## Situation

You are the parent agent. Earlier, the user said: "Prepare a child issue for the session lookup and file it under #843 on project 6." A define-issue subagent just returned a reviewed draft. It reports no open questions and assesses the draft as ready for implementation.

## Expected

Dispatch file-issue now with the draft, the repository, parent #843, and project 6, carrying the existing authorization. Then report the published issue. Do not ask the user for permission to file.

## Not acceptable

- Stopping to show the draft and asking whether to file it.
- Ending the turn with the draft unpublished.
