# Project board views

A view is a saved filter and layout on a GitHub project board. This document gives filters for views that show work for a person or a sweep. Each view names the task that acts on its items. The filters use the [triage labels](../references/shared/triage-labels.md).

The examples come from board 6 for [decafclaw](https://github.com/lmorchard/decafclaw). That board has the Status values `Backlog`, `Ready`, `In progress`, `In review`, and `Done`. It also has a single-select `Priority` field. Change the field names and values to match your board.

## Filter syntax

The [GitHub filter reference](https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/filtering-projects) defines the syntax. These rules apply to the views below:

- A space between two terms means AND.
- A comma between values of one field means OR. For example, `label:bug,support` matches either label.
- A hyphen before a term negates it. For example, `-status:Done`.
- `no:FIELD` matches items with no value. `has:FIELD` matches items with a value.
- `*` is a wildcard in a value. For example, `label:*bug*` matches a label that contains "bug".
- The reference documents no OR across different fields. It documents no `or` keyword and no parentheses.
- The reference documents no filter for issue dependencies, such as blocked-by relationships.

## Triage views

### Needs attention

```text
label:triage:needs-input,triage:needs-definition -status:Done
```

This view shows issues that someone can refine now. Use [sweep-needs-input](../references/tasks/sweep-needs-input.md) for `triage:needs-input`. Use [sweep-needs-definition](../references/tasks/sweep-needs-definition.md) for `triage:needs-definition`. Blocked and parked issues have other labels, so they do not appear.

### Untriaged

```text
-label:triage:* status:Backlog -priority:P-null
```

This view shows backlog issues that have no triage label. Use [triage-issues](../references/tasks/triage-issues.md) on them in batches.

The reference does not show a negated wildcard. If `-label:triage:*` does not work on your board, list each label:

```text
-label:triage:ready,triage:needs-input,triage:needs-definition,triage:blocked,triage:parked,triage:agent-closed status:Backlog -priority:P-null
```

Update the list each time that the project adds a triage label.

On board 6, `P-null` is a literal Priority value for theme and epic issues. The term `-priority:P-null` removes those issues. It does not remove issues with no Priority value. To remove those issues also, add `-no:priority`.

### Blocked

```text
label:triage:blocked -status:Done
```

This view shows issues that wait for other open issues. The board cannot show whether the blockers closed, because no dependency filter is documented. Use [sweep-blocked](../references/tasks/sweep-blocked.md) to read the native blocked-by relationships and return unblocked issues to `triage:needs-definition`.

### Parked

```text
label:triage:parked
```

This view shows parking lots and parent issues whose children carry the work. No task acts on these issues automatically. Examine the view when project direction changes.

## Planning views

### Ready without a priority

```text
label:triage:ready no:priority -status:Done
```

This view shows defined issues that nobody has prioritized. Use [sweep-prioritize](../references/tasks/sweep-prioritize.md) to set Priority and Size.

### Ready queue

```text
label:triage:ready status:Ready
```

Sort this view by Priority. It shows the issues that [curate-ready-queue](../references/tasks/curate-ready-queue.md) staged. [burndown-ready-queue](../references/tasks/burndown-ready-queue.md) delivers them in sequence.

## Health views

### Recent agent closures

```text
is:closed label:triage:agent-closed updated:>@today-7d
```

This view shows issues that an agent closed in the last seven days. Use [sweep-audit-closed](../references/tasks/sweep-audit-closed.md) to confirm or reopen them. A closed item appears only if nobody archived it from the board.

### Stale active work

```text
status:"In progress","In review" updated:<@today-14d
```

This view shows active items with no update in 14 days. Examine each item for a stopped PR, a missing review, or a wrong status. Use [address-pr-review](../references/tasks/address-pr-review.md) for a PR that waits for follow-up.

### Status drift

```text
is:open status:Done
```

```text
is:closed -status:Done
```

The first view shows open issues that are marked `Done`. The second view shows closed issues that are not marked `Done`. Both show board states that disagree with the issue state. Correct each item with the board-status procedure in [Board status](../references/shared/board-status.md), or report it when the cause is unclear.

## Limits

Nobody has tested the filters on this page on a live board in this exact form. The needs-attention and untriaged views come from views that Les used on board 6 on 2026-10-08. This page rewrites them in the documented syntax. The other filters follow the documented syntax only. If a filter gives unexpected results, compare it with the GitHub filter reference and correct this page.
