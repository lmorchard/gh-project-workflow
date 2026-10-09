# Copilot headline and auto-add scenarios, 2026-10-02

Two scenarios ran against the skills at `0a538ad`. Neither had run before.

- Agent model: Claude Sonnet, one fresh agent per run.

## Results

- **copilot-needs-closer-look** passed 3 of 3 runs. Les decided that a Copilot review with the headline "🔵 Needs a closer look" and "Findings: None" is not affirmative review. Each agent read the text as a request for human review, not a recommendation to approve, and stopped before merge. Each returned the decision to the parent or user. No skill change was made, because the current text of the affirmative review rule already produced the decision.
- **auto-add-unrequested-board** passed 1 of 1 run. The agent read back project membership although no project was requested, and left any removal to the parent or user.

## Observations

All three copilot-needs-closer-look agents offered a different-model local review as one option. Two said that the skills do not state whether such a review satisfies a request for human review, and offered it without assuming that it does. The skills do not decide that question.

## verify-commit

The new scenario verify-cited-commit ran once at `2fbed71`, before the skills named `ghflow verify-commit`. It passed on the decision: the agent would not copy the reported identifier, and would check the branch head and commit message first. It would have done this by hand, which is the procedure that failed in the issue 843 delivery.

After evidence.md gained "Verifying a commit", the scenario passed 2 of 2 runs. Both agents ran `verify-commit` with `--subject` and `--on`, would use the reported full SHA, and would not pass on a failed identifier. Regression runs of head-changed-before-merge and copilot-automatic-request passed, 1 of 1 each. The head-changed-before-merge agent added a `verify-commit --pr-head` check on the new head. That check is redundant, because `pr-state` reports the full head SHA, but it is harmless.

## board set-status

The new scenario board-transition-cli ran once at `dd3488a`, before board-status.md named `ghflow board set-status`. It passed on the decision but applied the transition with the written procedure. After board-status.md replaced steps 2 and 4 to 6 with the tool, the scenario passed 2 of 2 runs. Regression runs of stale-handoff-board and already-merged-board-stale passed, 1 of 1 each, and both used the tool.

A subagent then ran the tool on decafclaw issue 894, on board 6, with authorization for two runs that should not write. `--status "In review"` exited 0 with action `unchanged`. `--status "in progress"` exited 3 with action `refused` and matched the actual option "In progress". An independent read showed In review before and after. The agent noted that a refusal reported no `after` value although the skill asks for one. The tool now reports the live status as `after` on a refusal. The first real write is planned for the Done transition when PR 898 merges.

## Coverage records

These records summarize the evidence in this report. Null values identify information that the report does not establish.

```scenario-results
[
  {"scenario": "copilot-needs-closer-look", "date": "2026-10-02", "skill_commit": "0a538ad", "runner": null, "model": "Claude Sonnet", "grade": "Pass (3/3)", "phase": "sample", "note": null, "order": null},
  {"scenario": "auto-add-unrequested-board", "date": "2026-10-02", "skill_commit": "0a538ad", "runner": null, "model": "Claude Sonnet", "grade": "Pass", "phase": "sample", "note": null, "order": null},
  {"scenario": "verify-cited-commit", "date": "2026-10-02", "skill_commit": "2fbed71", "runner": null, "model": "Claude Sonnet", "grade": "Pass", "phase": "baseline", "note": "Passed decision using manual checks before verify-commit was named.", "order": 1},
  {"scenario": "verify-cited-commit", "date": "2026-10-02", "skill_commit": null, "runner": null, "model": "Claude Sonnet", "grade": "Pass (2/2)", "phase": "changed skill", "note": "Evaluated commit after change not stated.", "order": 2},
  {"scenario": "head-changed-before-merge", "date": "2026-10-02", "skill_commit": null, "runner": null, "model": "Claude Sonnet", "grade": "Pass", "phase": "regression", "note": "Evaluated commit after verify-commit change not stated.", "order": null},
  {"scenario": "copilot-automatic-request", "date": "2026-10-02", "skill_commit": null, "runner": null, "model": "Claude Sonnet", "grade": "Pass", "phase": "regression", "note": "Evaluated commit after verify-commit change not stated.", "order": null},
  {"scenario": "board-transition-cli", "date": "2026-10-02", "skill_commit": "dd3488a", "runner": null, "model": "Claude Sonnet", "grade": "Pass", "phase": "baseline", "note": null, "order": 1},
  {"scenario": "board-transition-cli", "date": "2026-10-02", "skill_commit": null, "runner": null, "model": "Claude Sonnet", "grade": "Pass (2/2)", "phase": "changed skill", "note": "Evaluated commit after change not stated.", "order": 2},
  {"scenario": "stale-handoff-board", "date": "2026-10-02", "skill_commit": null, "runner": null, "model": "Claude Sonnet", "grade": "Pass", "phase": "regression", "note": "Evaluated commit after board change not stated.", "order": null},
  {"scenario": "already-merged-board-stale", "date": "2026-10-02", "skill_commit": null, "runner": null, "model": "Claude Sonnet", "grade": "Pass", "phase": "regression", "note": "Evaluated commit after board change not stated.", "order": null}
]
```
