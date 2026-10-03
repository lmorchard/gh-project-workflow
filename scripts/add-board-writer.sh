#!/usr/bin/env bash
# Add a user as a Write collaborator on a user-owned Projects v2 board,
# then optionally read back write access as that user.
# Usage: scripts/add-board-writer.sh OWNER PROJECT_NUMBER LOGIN
set -euo pipefail
owner=$1 number=$2 login=$3

project_id=$(gh project view "$number" --owner "$owner" --format json --jq .id)
user_id=$(gh api "users/$login" --jq .node_id)
gh api graphql -f project="$project_id" -f user="$user_id" -f query='
  mutation($project: ID!, $user: ID!) {
    updateProjectV2Collaborators(input: {projectId: $project,
      collaborators: [{userId: $user, role: WRITER}]}) { clientMutationId }
  }' >/dev/null
# Read back as the added user: viewerCanUpdate is true only with write access.
# Set READBACK_TOKEN_FILE to that user's token file to run this check.
if [ -n "${READBACK_TOKEN_FILE:-}" ]; then
  GH_TOKEN="$(tr -d '[:space:]' < "$READBACK_TOKEN_FILE")" gh api graphql -f project="$project_id" -f query='
    query($project: ID!) { viewer { login } node(id: $project) { ... on ProjectV2 { title viewerCanUpdate } } }' \
    --jq '"\(.data.viewer.login) on \(.data.node.title): viewerCanUpdate=\(.data.node.viewerCanUpdate)"'
else
  echo "added $login. Set READBACK_TOKEN_FILE to check viewerCanUpdate as $login."
fi
