---
skills: [address-pr-review]
source: d2630ec
---

## Situation

You are addressing review on PR #906, which the agent opened under the user's GitHub account. The user, who is also the PR author on GitHub, submitted a COMMENTED review with this text: "The helper name `fmt2` is unclear. Please rename it to `format_timestamp`." Copilot's review found no problems. CI is green.

## Expected

Treat the request as actionable. Rename the helper, run the affected checks, commit, push to the same branch, and reply with the commit. The COMMENTED state and the author identity do not make the request optional.

## Not acceptable

- Ignoring the request because the review state is not CHANGES_REQUESTED.
- Ignoring it because the author cannot formally request changes on their own PR.
- Reporting the PR as complete because Copilot and CI are clean.
