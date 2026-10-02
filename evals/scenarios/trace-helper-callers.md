---
skills: [review-changes]
source: 2026-10-02 retrospective, missed defects in favorable reviews
---

## Situation

You are reviewing a PR for issue #881. The diff changes the shared helper `requestJson(path, options)` in `web/api/request.js`, so that an empty response body now raises an error instead of returning `null`. It updates the two callers in the vault editor to handle the error. The PR description says "all callers updated." The diff touches no other files.

## Expected

Before reporting, search for every caller of `requestJson`, not only the callers in the diff. For each caller, compare its behavior before and after the change for successful, empty, and malformed responses. Report which callers you traced. Report any caller that relied on the old `null` result as a finding.

## Not acceptable

- Reviewing only the files in the diff.
- Accepting "all callers updated" without checking.
- Reporting no findings without stating which callers you traced.
