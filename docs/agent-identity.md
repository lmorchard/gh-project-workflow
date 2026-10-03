# Agent identity: research and trial proposal

This document records research for [issue 1](https://github.com/lmorchard/gh-project-workflow/issues/1). It is a proposal. Les has not decided to adopt a separate identity.

A research subagent did the work on 2026-10-03. It read agent-sessions at commit `4379832`, live GitHub data for lmorchard repositories, and current GitHub documentation. The parent examined two of its claims against live data. Labels show the source of each claim:

- **[docs]**: current GitHub documentation.
- **[AS]**: agent-sessions records or live GitHub data.
- **[inferred]**: reasoning that nobody has tested.

## Problem

Agents run `gh` and `git` as `lmorchard`. GitHub records do not show whether Les or an agent did an action. On 2026-10-02, a decafclaw priority change had no known cause. Les also cannot approve a PR that an agent opened as him.

## What agent-sessions did

A **machine user** is an ordinary GitHub account that a person operates for automation. `MokaGnome`, a machine user, opened decafclaw PRs #812 to #837 from 2026-08-09 to 2026-08-14 [AS]. The GitHub App `mokagnomebot` then opened PRs #839 to #848 until 2026-08-18 [AS]. After that, `lmorchard` opened every PR again. No record gives the reason [AS].

The main purpose was containment, not attribution. The agent received a read-only token, and a driver did every write ([agent-sessions#191](https://github.com/lmorchard/agent-sessions/issues/191)) [AS]. The project moved to an App because a fine-grained token cannot reach another user's repositories ([usage.md](https://github.com/lmorchard/agent-sessions/blob/4379832e4d7003cd7bbc6fb73c30b83d4354ed57/docs/usage.md#L381-L391)) [AS]. The App could not change Les's user-owned board, so a separate board token was necessary ([credentials.py](https://github.com/lmorchard/agent-sessions/blob/4379832e4d7003cd7bbc6fb73c30b83d4354ed57/src/agent_sessions/driver/credentials.py#L32-L33)) [AS].

Results from that period:

- Les approved PRs that the App opened, for example #839 [AS, examined by the parent].
- Copilot did not review the separate identities' PRs automatically. Les requested each Copilot review, for example on #812 [AS, examined by the parent].
- The machine user's commits were unsigned [AS].

## Comparison

| Operation | Machine user with a classic token | GitHub App |
|---|---|---|
| Push, open PRs, comment | Works as a collaborator with Write access. A fine-grained token cannot work on another user's repository [docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens). | Works [docs] [AS]. |
| Change Les's user-owned board | Works with the `project` and `read:org` scopes. Les must add the account to the board [AS]. | Does not work. The user-project endpoints reject App tokens [docs](https://docs.github.com/en/rest/projects/items). |
| Request Copilot review | Copilot bills the requester. Copilot Free does not include PR review, so the account probably needs a paid seat [docs](https://docs.github.com/en/copilot/concepts/agents/code-review) [inferred]. | Copilot bills an organization for a bot request [docs]. decafclaw has no organization, so this probably fails [inferred]. |
| Copilot automatic review | Copilot bills the PR author [docs]. It did not occur for `MokaGnome` [AS]. | It did not occur for the App [AS]. |
| Merge under the ruleset | Write access is sufficient, and required checks still apply [AS]. The ruleset setting `require_extra_approval_for_unattributed_changes` can block mixed-identity PRs [inferred from third-party reports]. | Same [inferred]. |
| Les approves the PR | Possible [docs]. | Possible [AS]. |
| Select the identity in `gh` | `GH_TOKEN` takes precedence over stored credentials [docs: `gh help environment`]. Les's login stays unchanged. | Same, but the token has no user, so `gh api user` fails [AS]. |
| Terms of service | One free machine account is permitted for each person [docs](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service). | No limit applies. |

## Conclusions

A GitHub App does not work while the boards are user-owned. A machine user can do every operation in this workflow. It has three costs:

- It needs a classic token with broad scopes.
- Les must add it to each board.
- It probably needs a paid Copilot seat. Without one, agent PRs lose Copilot review, which the merge policy prefers.

A separate identity makes board changes attributable and lets Les approve agent PRs. It does not show whether a Copilot request came from automation. The ruleset records the PR author as the actor of its automatic request [AS]. A timing check in `pr-state` must solve that problem separately.

Moving the repositories and boards to an organization would make fine-grained tokens and Apps possible. That change is much larger, and nobody proposes it now.

## Trial proposal

We propose one trial before Les decides. The trial uses a separate test repository, so it does not change decafclaw.

### Setup by Les

`scripts/identity-trial-setup.sh` does steps 2 to 5. `scripts/identity-trial-teardown.sh` removes the repository and the board after the trial.

1. Use the existing machine account `MokaGnome`, which Les owns. Revoke any personal access tokens that remain from agent-sessions. Make sure that two-factor authentication is on. Record its Copilot plan.
2. Create the public repository `lmorchard/ghflow-identity-trial` with one file and a `main` branch.
3. Copy the decafclaw ruleset to it, with its required checks, its Copilot code review rule, and `require_extra_approval_for_unattributed_changes`. Add a short CI workflow that the required check names.
4. Create a user-owned project board with a Status field. Use the options Backlog, Ready, In progress, In review, and Done.
5. Give `MokaGnome` Write access to the repository and to the board. On 2026-10-03, it still had Write access to decafclaw from agent-sessions.
6. On the machine account, create one classic token with the `public_repo`, `project`, and `read:org` scopes. Do not add the `workflow` scope. Set a short expiry.
7. Store the token outside every repository, in a file that only Les can read. Tell the parent its path. Do not paste the token into the conversation.
8. Do not buy a Copilot seat yet. The trial first measures the result without one.

### Checks by a subagent

The subagent sets `GH_TOKEN` from the file and sets the git author and committer to the machine account. It examines each result:

1. `gh api user` returns the machine login. Les's `gh auth status` stays unchanged.
2. The subagent creates an issue, adds it to the board, and opens a PR that closes it. `git push` uses the machine account.
3. `ghflow board set-status` moves the issue to In progress and then In review. The board history shows the machine login.
4. `ghflow pr-state` reads the PR. It shows whether the ruleset requested Copilot automatically.
5. `gh pr edit --add-reviewer "@copilot"` succeeds or fails. The subagent records the error text.
6. Les submits an APPROVED review.
7. Les pushes one commit to the PR branch. `ghflow pr-state` and the merge result show whether the ruleset requires another approval.
8. `gh pr merge --match-head-commit` succeeds or fails as the machine user.

After the trial, Les decides on the Copilot seat and on adoption. If Les buys a seat, the subagent repeats checks 4 and 5.

On 2026-10-03, Les judged the agent-sessions read and write separation unnecessary for this workflow. Agents in this workflow do authorized writes themselves, and no driver exists to do writes for them. The trial uses one classic token.

## Trial results

The trial ran on 2026-10-03 in `lmorchard/ghflow-identity-trial` with board 11. `MokaGnome` had one classic token and no Copilot seat. Subagents did each step as `MokaGnome`, except check 6. Les did check 6 and also edited the PR in the web interface.

| Check | Result |
|---|---|
| 1. Identity | With the token, `gh api user` returned `MokaGnome`. Without it, `gh api user` returned `lmorchard`. |
| 2. Issue, push, PR | GitHub recorded `MokaGnome` as the issue author, PR author, commit author, and committer. The activity API recorded `MokaGnome` as the actor of the push. The commits were unsigned. |
| 3. Board | `ghflow board set-status` added the issue to the board and set each status. The Status value records `creator: MokaGnome`. |
| 4. Automatic Copilot review | No request occurred when `MokaGnome` opened the PR. No request occurred when Les pushed a commit to the PR. |
| 5. Requested Copilot review | `gh pr edit --add-reviewer "@copilot"` exited 0 but made no request, and no review arrived in 10 minutes. |
| 6. Approval | Les submitted an APPROVED review. |
| 7. Mixed authors | Les edited `NOTE.md` in the web interface, so the PR had commits from both accounts. The merge state stayed `CLEAN`. |
| 8. Merge | `gh pr merge --match-head-commit` as `MokaGnome` succeeded. GitHub records `mergedBy: MokaGnome`. |

Conclusions from the trial:

- A machine user with one classic token gives attribution for every write in this workflow, and lets Les approve agent PRs.
- Without a Copilot seat, agent PRs get no Copilot review. `--add-reviewer "@copilot"` fails without an error, so only a read-back shows the failure. submit-pr already requires that read-back.
- The global git credential helper on this machine is the VS Code container helper, and git asks it before the clone's `gh` helper. The push used the machine token, but the configuration did not guarantee that. An agent clone must clear inherited helpers with `-c credential.helper=` before it adds `gh auth git-credential`.
- The trial board did not move the closed issue to Done automatically. The setup script replaced the Status options, which probably removed the target of the default workflow for closed items.

## Delivery trial

Les chose to try `MokaGnome` on one real decafclaw issue before a decision on adoption. On 2026-10-03, Les added it to decafclaw board 6 with `scripts/add-board-writer.sh`. It already had Write access to decafclaw from agent-sessions. The token expires on 2026-11-02.

## Open questions

1. The trial showed that agent PRs get no Copilot review without a seat. Can a machine account have a paid Copilot seat, and does Les accept that cost? If not, does Les accept agent PRs without Copilot review, or request reviews himself?
2. Does Les accept a classic token with broad scopes?
3. Do agents merge as the machine user, or does Les do every merge?
4. Does `require_extra_approval_for_unattributed_changes` stay on if mixed-identity PRs become common?
