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
Explicit `GHFLOW_*` values take precedence over configuration-file values.
The selected token file takes precedence over inherited `GH_TOKEN` and `GITHUB_TOKEN` values.
If the selected file is missing, unreadable, or empty, `ghflow exec` stops before it starts the child command.
Without a selected token file, `GH_TOKEN` can supply the token.
`ghflow exec` removes inherited `GITHUB_TOKEN` values.
The selected author name and email replace inherited Git author and committer values.
The selected name falls back to the selected login.
`identity --export` removes inherited `GITHUB_TOKEN` from the shell that evaluates its output.
The `identity` result reports `configured` for configuration presence.
It reports `ready` when a login and non-empty token are available.
`ready` checks local inputs. It does not confirm that GitHub accepts the token.

Inspect the active identity configuration with:

```sh
python3 "$GHFLOW_CLI" identity
```

## Running commands under the identity

Use `ghflow exec` to run Git or `gh` commands with the identity environment:

```sh
python3 "$GHFLOW_CLI" exec -- gh pr create ...
python3 "$GHFLOW_CLI" exec -- git commit -m "..."
python3 "$GHFLOW_CLI" exec -- git push origin BRANCH
```

`ghflow exec` sets:

- `GH_TOKEN` from the selected token file, when one is selected.
- `GIT_AUTHOR_NAME`, `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_NAME`, and `GIT_COMMITTER_EMAIL` from the selected identity fields.
- `GIT_CONFIG_PARAMETERS` so GitHub HTTPS operations use `gh auth git-credential`.
  Other Git configuration parameters remain available.

Before a direct `git commit`, `ghflow exec` requires a selected author name and email.
This check does not require a GitHub read, so a local commit can remain offline.
The command does not inspect scripts or other arbitrary subprocesses for hidden writes.

Before a GitHub write, confirm that the active token belongs to the selected login.
Run `gh api user` under the selected identity and compare its `login` value.
The CLI confirms this account before its board status writes.
The CLI does not infer write intent in arbitrary `ghflow exec` commands.

The `ghflow` commands `pr-state`, `verify-commit`, and `board set-status` apply the configured identity to their own `gh` calls. They do not need `ghflow exec`.
`board set-status` also checks the authenticated login before it adds or edits a board item.

Alternatively, export the environment into the current shell:

```sh
eval "$(python3 "$GHFLOW_CLI" identity --export)"
```

`identity --export` writes POSIX shell statements. You can evaluate them in a
POSIX-compatible shell, including `sh`, `bash`, or `zsh`. The output quotes each
value so shell characters in the configured identity remain literal.

Do not print, log, or echo raw token content. Do not run `gh auth login`, `gh auth switch`, or `gh auth logout`.

## Personal approval

Do not submit a GitHub APPROVED review as the repository owner from an agent. A formal GitHub approval is the user's personal action.
Follow [Review](review.md) for review sources and requirements.

## Access failures

The machine account needs repository and project access before a task starts. [Machine account access](../../README.md#machine-account-access) describes setup.
If access is missing, report the required action. Do not switch accounts or change credentials to bypass the failure.

### Sandboxed GitHub checks

A sandbox can block access to the host keyring or GitHub. A failed GitHub check inside a sandbox does not by itself show that the token is invalid.

Compare `gh auth status` inside the configured identity with the result from an approved command outside the sandbox. Use the same host and configured login for both checks.
If the host result shows the configured login and required scopes, treat the failure as a sandbox access limit. Use an approved host context for authorized GitHub commands when available.
If both checks fail, report each result and follow the access-failure rule above.
Do not copy tokens between stores or change credentials only because a sandbox check fails.
