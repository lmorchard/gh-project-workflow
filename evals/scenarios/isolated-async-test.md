---
skills: [implement-issue]
source: 2026-10-02 retrospective, browser test design (#894)
---

## Situation

You are implementing issue #883, which migrates schedule management to generated API calls. The project's browser tests live mostly in one 1,000-line test that runs many scenarios against a single page. Earlier scenarios leave requests in flight and state behind. You need a browser test that shows the schedule page saves through the generated client. The easiest option is to append a scenario to the long test and wait 500 ms after clicking Save.

## Expected

Write the scenario as a separate test with its own page and state. Wait for an explicit completion signal, such as the save response or a visible saved state, instead of a fixed delay. Confirm that the test fails without the change, for the reason it names.

## Not acceptable

- Appending to the long shared test.
- Waiting a fixed delay for the save to complete.
