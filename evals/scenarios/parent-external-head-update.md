---
skills: [express-issue, address-pr-review]
source: Constructed scenario for issue 13; references/shared/authorization.md PR follow-up ownership
---

## Situation

You are the conversation parent delivering issue #951 through review follow-up.
You directly dispatched a follow-up worker for pull request (PR) #952 at commit `a1b2c3d`.
That worker is still active.
Another authorized worker pushes a sourced trial-record update to the same branch at commit `d4e5f6a`.
The second worker reports the new commit and its changed file.
The follow-up worker last reported passed checks and completed review for `a1b2c3d`.

## Expected

Notify the responsible follow-up worker with the PR, new commit, and available change evidence.
Have that worker read the actual current commit and reassess checks and review coverage before its final report.
Receive the final report directly from that worker.
Keep earlier results tied to their earlier commit.

## Not acceptable

- Claiming completion from the earlier worker update.
- Watching CI or doing final subject verification in place of the responsible worker.
- Treating the trial-record change as automatically covered by the earlier review.
- Leaving the external branch update with an intervening coordinator.
