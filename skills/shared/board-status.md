# Board status

Three skills move a linked issue on the project board:

| Skill | When | Target state |
|---|---|---|
| [implement-issue](../implement-issue/SKILL.md) | Implementation starts | In progress |
| [submit-pr](../submit-pr/SKILL.md) | The PR exists and is ready for review | In review |
| [merge-pr](../merge-pr/SKILL.md) | GitHub confirms the merge | Done |

The transition is part of that skill's task unless the user restricts GitHub or board writes. [file-issue](../file-issue/SKILL.md) also sets a status when the filing request includes one, using the same procedure.

## Procedure

1. Identify the board from the user, the project instructions, or the issue's existing membership when it has only one.
2. Read the board's fields and status options. Use the actual option name, not an assumed spelling or capitalization.
3. If the board or the option is ambiguous, return the choice to the parent or user.
4. If the issue already has the target state, leave it unchanged. Automation may have already moved it.
5. Add the issue to the board if necessary, then set its status.
6. Read the status back.

## Limits

Move only the issue that the task implements. Do not move a broader parent because a PR mentions it or a child finished. A parent changes state only when its full scope is complete and the update is authorized.

Do not move an issue backward, such as from Done to In review, without a reason and authorization. Do not move an issue because you only inspected it or found no remaining work. Do not mark unfinished work In review because a draft PR exists.

A transition does not authorize any other GitHub change. Do not create a board or change its fields to make a transition possible. If access fails or no suitable state exists, report it separately and continue the main task. A failed board update does not make the main task fail.
