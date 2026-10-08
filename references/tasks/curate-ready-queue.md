# Curate the ready queue

Select high-priority (`P0`/`P1`) issues from the project board's `Backlog` and advance them to `Ready`. Maintain a bounded work-in-progress (WIP) queue (typically 3 to 5 items) so implementers have a clear, prioritized pipeline without overwhelming the board. This skill does not start implementation or submit pull requests.

Apply [Authorization](../shared/authorization.md), [Evidence](../shared/evidence.md), [Board status](../shared/board-status.md), and [Agent identity](../shared/identity.md) throughout. The parent agent discusses candidate tasks with the user; subagents execute board transitions in the subject repository. Before changing GitHub records, apply [GitHub writes](../shared/github-writes.md).

## Audit current board WIP

Query the project board for items in active columns:

- Count items currently in `Ready`, `In progress`, and `In review`.
- If the `Ready` column is already at capacity (e.g. 5 items), report the current queue and stop, or propose swapping a blocked or deprioritized item back to `Backlog`.
- Calculate available slots in `Ready` based on the target WIP limit (default 3 to 5 items).

## Select candidates from Backlog

Query the board for items with status `Backlog` and priority `P0` or `P1`:

1. Sort candidates:
   - `P0` items before `P1`.
   - Small, self-contained tasks (`XS`/`S`) that unblock other work.
   - Tasks with satisfied prerequisites.
2. If the `P0`/`P1` Backlog is empty, recommend running [sweep-prioritize](sweep-prioritize.md) to evaluate unprioritized issues or re-sweep deferred `P2`/`P3` issues.

## Review selection with the user

Present the candidate queue in conversation:

| Issue | Title | Priority | Size | Why Next |
|---|---|:---:|:---:|---|

Highlight sequencing logic (e.g., test guards before new feature tests). Confirm the batch with the user and adjust based on current project goals.

## Advance status on the board

Once approved, dispatch a subagent to move the selected issues from `Backlog` to `Ready` under the machine identity:

```bash
python3 "$GHFLOW_CLI" board set-status ISSUE_URL --owner OWNER --project NUMBER --status "Ready"
```

The tool verifies the transition and guards against accidental backward moves. Confirm that the readback shows status `Ready`.

## Return and hand off

Display the final `Ready` queue:
- Issues currently staged in `Ready` with their priority, size, and titles.
- Total count of active items in `Ready` against the WIP limit.

Hand off to [implement-issue](implement-issue.md) or [express-issue](express-issue.md) to pick up the top item in the `Ready` queue.
