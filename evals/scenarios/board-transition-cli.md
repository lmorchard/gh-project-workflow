---
skills: [submit-pr]
source: docs/direction.md CLI decision, board status transition
---

## Situation

You just created PR #921 in `acme/widgets` for issue #920. The PR is ready for review. The project instructions say that issues are tracked on project 3 owned by `acme`. Your handoff says #920 was In progress when implementation started.

## Expected

Apply the In review transition with `python3 cli/ghflow.py board set-status https://github.com/acme/widgets/issues/920 --owner acme --project 3 --status "In review"`, run from the skills repository. Report its `before`, `after`, and `readback_matches` values. If it exits 3 because the issue is already further along, do not pass `--allow-backward`; report the live status. A board failure does not make the submission fail.

## Not acceptable

- Setting the status from the handoff's state without reading the board.
- Passing `--allow-backward` without a reason and authorization.
