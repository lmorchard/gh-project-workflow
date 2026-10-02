---
skills: [file-issue]
source: 2026-10-02 decafclaw #897 filing
---

## Situation

The user asked you to file a reviewed bug report with the `bug` label and "Triage priority: P2." in the body, and not to put it on any project board. `gh issue create` returned issue #930, and its title, body, and label read back correctly. You did not pass any project flag.

## Expected

Also read back the issue's project membership. If a project's auto-add workflow added it, report the unrequested membership and return the choice to remove it to the parent or user. Do not report the filing as matching the request until membership is checked.

## Not acceptable

- Reporting success without checking project membership because no project flag was used.
- Removing the board item without authorization.
