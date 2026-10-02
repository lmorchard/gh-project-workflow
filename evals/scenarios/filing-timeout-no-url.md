---
skills: [file-issue]
source: skills/file-issue resume rules
---

## Situation

You ran `gh issue create` for a reviewed draft titled "Use the generated client for session lookup". The command timed out after 60 seconds and printed no URL. You do not know whether GitHub created the issue.

## Expected

Do not run the create command again yet. Search recent issues in the target repository and compare their title and body with the draft. If a matching issue exists, continue with the remaining requested metadata on it. Create the issue only after you establish that the first attempt did not create it.

## Not acceptable

- Retrying creation immediately.
- Reporting the filing as failed without checking GitHub.
