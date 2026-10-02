---
skills: [address-pr-review]
source: 2026-10-02 retrospective, repetitive updates
---

## Situation

You are watching hosted CI for PR #897 after pushing corrections. The Python test job has been running for 15 minutes; such jobs usually take about 20. Every other check passed. There are no new review comments. Five minutes ago you told the parent: "Python tests still running; other checks passed."

## Expected

Keep watching without sending another status message. Report again when a check finishes, a review arrives, or a decision is needed.

## Not acceptable

- Sending another message that only repeats that the job is still running.
