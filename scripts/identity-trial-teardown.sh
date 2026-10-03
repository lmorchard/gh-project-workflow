#!/usr/bin/env bash
# Remove the scratch repository and board from scripts/identity-trial-setup.sh.
# Deleting a repository needs the delete_repo scope: run
# `gh auth refresh -s delete_repo` first.
set -euo pipefail

OWNER=lmorchard
REPO="$OWNER/ghflow-identity-trial"
BOARD_TITLE="ghflow identity trial"

number=$(gh project list --owner "$OWNER" --format json \
  --jq ".projects[] | select(.title == \"$BOARD_TITLE\") | .number" | head -1)
if [ -n "$number" ]; then
  gh project delete "$number" --owner "$OWNER"
  echo "deleted project $number"
fi

if gh repo view "$REPO" >/dev/null 2>&1; then
  gh repo delete "$REPO" --yes
  echo "deleted $REPO"
fi
