# Agent identity

These rules apply to every subagent that runs Git commands or interacts with GitHub.

## Overview

Subagents perform subject-repository actions under a designated machine account (such as `MokaGnome`). This distinguishes agent contributions from human actions on GitHub and allows the user to submit approving reviews on agent PRs.

## Configuration

Configure the agent identity using environment variables or a configuration file.

### Environment variables

- `GHFLOW_IDENTITY_LOGIN` (or `GHFLOW_LOGIN`): machine account GitHub username.
- `GHFLOW_IDENTITY_NAME` (or `GHFLOW_NAME`): name for Git commit author and committer.
- `GHFLOW_IDENTITY_EMAIL` (or `GHFLOW_EMAIL`): email for Git commit author and committer.
- `GHFLOW_TOKEN_FILE`: path to a file containing the machine account personal access token.

### Configuration file

If environment variables are not set, `ghflow` reads `./.ghflow/identity.json` or `~/.config/ghflow/identity.json`:

```json
{
  "login": "MokaGnome",
  "name": "MokaGnome",
  "email": "me+mokagnome@lmorchard.com",
  "token_file": "~/.config/ghflow/mokagnome.token"
}
```

The token file must have mode 600 permissions. The token needs `public_repo`, `project`, and `read:org` scopes.

Inspect the active identity configuration with:

```sh
python3 cli/ghflow.py identity
```

## Running commands under the identity

Use `ghflow exec` to run Git or `gh` commands with the identity environment:

```sh
python3 cli/ghflow.py exec -- gh pr create ...
python3 cli/ghflow.py exec -- git commit -m "..."
python3 cli/ghflow.py exec -- git push origin BRANCH
```

`ghflow exec` sets:

- `GH_TOKEN` from the token file.
- `GIT_AUTHOR_NAME`, `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_NAME`, and `GIT_COMMITTER_EMAIL`.
- `GIT_CONFIG_PARAMETERS` so Git HTTPS operations use `gh auth git-credential` without interference from other system credential helpers.

The `ghflow` commands `pr-state`, `verify-commit`, and `board set-status` apply the configured identity to their own `gh` calls. They do not need `ghflow exec`.

Alternatively, export the environment into the current shell:

```sh
eval "$(python3 cli/ghflow.py identity --export)"
```

Do not print, log, or echo raw token content. Do not run `gh auth login`, `gh auth switch`, or `gh auth logout`.

## Code review

A machine account without a paid Copilot seat does not trigger automatic Copilot reviews on pull requests.

Follow [Review](review.md): an independent different-model local review is the primary review source for agent pull requests. The user may manually request a Copilot review in the GitHub web interface if desired.

Do not submit a GitHub APPROVED review as the repository owner from an agent. A formal GitHub approval is the user's personal action.

## Repository and board access

Before an agent works in a repository or project board, the repository owner must grant access:

- Add the machine user as a repository collaborator with Write access.
- For user-owned project boards, add the machine user as a writer with `scripts/add-board-writer.sh OWNER PROJECT_NUMBER LOGIN`.
