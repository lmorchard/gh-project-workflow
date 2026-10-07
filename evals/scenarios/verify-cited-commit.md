---
skills: [express-issue]
source: 2026-10-02 issue 843 delivery retrospective, a commit identifier copied incorrectly
---

## Situation

You are coordinating express-issue for issue #912 in `acme/widgets`. The implementation subagent's final report says: "Pushed commit `4f3c2a9` ('Cache parsed templates per request') to `task/912-template-cache`. All tests pass." You are now writing the handoff to the review subagent, which needs the commit to review.

## Expected

Before putting the identifier in the handoff, verify that it exists and names the commit described. Run `python3 "$GHFLOW_CLI" verify-commit 4f3c2a9 --repo acme/widgets --subject "Cache parsed templates per request" --on task/912-template-cache` from the target project after resolving `GHFLOW_CLI` through the entry skill. Use the full SHA it reports in the handoff. If it exits 1 or 3, do not pass the identifier on; read the branch again or return the mismatch to the implementer.

## Not acceptable

- Copying the identifier from the report into the handoff without checking it.
- Checking only that the commit exists, not that it is the described commit on the task branch.
