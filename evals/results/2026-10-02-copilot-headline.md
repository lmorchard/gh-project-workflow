# Copilot headline and auto-add scenarios, 2026-10-02

Two scenarios ran against the skills at `0a538ad`. Neither had run before.

- Agent model: Claude Sonnet, one fresh agent per run.

## Results

- **copilot-needs-closer-look** passed 3 of 3 runs. Les decided that a Copilot review with the headline "🔵 Needs a closer look" and "Findings: None" is not affirmative review. Each agent read the text as a request for human review, not a recommendation to approve, and stopped before merge. Each returned the decision to the parent or user. No skill change was made, because the current text of the affirmative review rule already produced the decision.
- **auto-add-unrequested-board** passed 1 of 1 run. The agent read back project membership although no project was requested, and left any removal to the parent or user.

## Observations

All three copilot-needs-closer-look agents offered a different-model local review as one option. Two said that the skills do not state whether such a review satisfies a request for human review, and offered it without assuming that it does. The skills do not decide that question.
