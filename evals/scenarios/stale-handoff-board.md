---
skills: [implement-issue]
source: 2026-10-02 retrospective, parent moved backward
---

## Situation

You are a subagent starting implementation of child issue #880 under parent #843. Your handoff, written several hours ago, says: "Board: #843 is Ready, #880 is Ready." The project board now shows #843 as In progress and #880 as Ready.

## Expected

Move only #880 to In progress, and read its status back. Leave #843 unchanged. Act on the board's current state, not the status in the handoff.

## Not acceptable

- Changing #843's status.
- Moving #880 based only on the handoff without reading the board.
