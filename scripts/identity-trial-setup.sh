#!/usr/bin/env bash
# Set up the scratch repository and board for the agent identity trial.
# See docs/research/agent-identity.md, "Trial proposal". Safe to run again: each step
# skips work that already exists.
#
# Runs as the current gh login (Les), except accepting the repository
# invitation, which runs as the machine account from TOKEN_FILE.
set -euo pipefail

OWNER=lmorchard
REPO="$OWNER/ghflow-identity-trial"
BOT=MokaGnome
BOARD_TITLE="ghflow identity trial"
TOKEN_FILE="${TOKEN_FILE:-$HOME/.config/ghflow/mokagnome.token}"

bot_gh() { GH_TOKEN="$(tr -d '[:space:]' < "$TOKEN_FILE")" gh "$@"; }

echo "== repository"
if gh repo view "$REPO" >/dev/null 2>&1; then
  echo "exists: $REPO"
else
  gh repo create "$REPO" --public --add-readme \
    --description "Scratch repository for the gh-project-workflow agent identity trial"
fi

echo "== CI workflow"
if gh api "repos/$REPO/contents/.github/workflows/ci.yml" >/dev/null 2>&1; then
  echo "exists: .github/workflows/ci.yml"
else
  # The job name is the required status check in the ruleset below.
  ci=$(cat <<'YAML'
name: ci
on:
  pull_request:
  push:
    branches: [main]
jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: test -f README.md
YAML
)
  gh api -X PUT "repos/$REPO/contents/.github/workflows/ci.yml" \
    -f message="Add a minimal CI check for the identity trial" \
    -f content="$(printf '%s\n' "$ci" | base64 -w0)" >/dev/null
  echo "created: .github/workflows/ci.yml"
fi

echo "== ruleset (copied from lmorchard/decafclaw ruleset 20481246)"
if gh api "repos/$REPO/rulesets" --jq '.[].name' | grep -qx main; then
  echo "exists: ruleset main"
else
  gh api -X POST "repos/$REPO/rulesets" --input - >/dev/null <<'JSON'
{
  "name": "main",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
  "bypass_actors": [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}],
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {"type": "required_status_checks", "parameters": {
      "do_not_enforce_on_create": false,
      "strict_required_status_checks_policy": false,
      "required_status_checks": [{"context": "lint-and-test", "integration_id": 15368}]}},
    {"type": "pull_request", "parameters": {
      "allowed_merge_methods": ["merge", "squash", "rebase"],
      "dismiss_stale_reviews_on_push": false,
      "require_code_owner_review": false,
      "require_extra_approval_for_unattributed_changes": true,
      "require_last_push_approval": false,
      "required_approving_review_count": 0,
      "required_review_thread_resolution": false}},
    {"type": "copilot_code_review", "parameters": {
      "review_draft_pull_requests": false,
      "review_on_push": true}}
  ]
}
JSON
  echo "created: ruleset main"
fi

echo "== board"
number=$(gh project list --owner "$OWNER" --format json \
  --jq ".projects[] | select(.title == \"$BOARD_TITLE\") | .number" | head -1)
if [ -n "$number" ]; then
  echo "exists: project $number"
else
  number=$(gh project create --owner "$OWNER" --title "$BOARD_TITLE" --format json --jq .number)
  echo "created: project $number"
fi
project_id=$(gh project view "$number" --owner "$OWNER" --format json --jq .id)
gh project link "$number" --owner "$OWNER" --repo "$REPO" >/dev/null 2>&1 || true

status_field=$(gh project field-list "$number" --owner "$OWNER" --format json \
  --jq '.fields[] | select(.name == "Status") | .id')
want="Backlog,Ready,In progress,In review,Done"
have=$(gh project field-list "$number" --owner "$OWNER" --format json \
  --jq '[.fields[] | select(.name == "Status") | .options[].name] | join(",")')
if [ "$have" = "$want" ]; then
  echo "Status options already: $have"
else
  gh api graphql -f field="$status_field" -f query='
    mutation($field: ID!) {
      updateProjectV2Field(input: {fieldId: $field, singleSelectOptions: [
        {name: "Backlog", color: GRAY, description: ""},
        {name: "Ready", color: BLUE, description: ""},
        {name: "In progress", color: YELLOW, description: ""},
        {name: "In review", color: PURPLE, description: ""},
        {name: "Done", color: GREEN, description: ""}
      ]}) { projectV2Field { ... on ProjectV2SingleSelectField { name } } }
    }' >/dev/null
  echo "set Status options: $want"
fi

echo "== $BOT access to the repository"
if gh api "repos/$REPO/collaborators/$BOT" >/dev/null 2>&1; then
  echo "already a collaborator"
else
  gh api -X PUT "repos/$REPO/collaborators/$BOT" -f permission=push >/dev/null
  invitation=$(bot_gh api user/repository_invitations \
    --jq ".[] | select(.repository.full_name == \"$REPO\") | .id" | head -1)
  if [ -n "$invitation" ] && bot_gh api -X PATCH "user/repository_invitations/$invitation" >/dev/null 2>&1; then
    echo "invited and accepted as $BOT"
  else
    echo "invited. Accept it as $BOT at https://github.com/$REPO/invitations"
  fi
fi
gh api "repos/$REPO/collaborators/$BOT/permission" --jq '"permission: \(.permission)"' || true

echo "== $BOT access to the board"
bot_id=$(gh api "users/$BOT" --jq .node_id)
gh api graphql -f project="$project_id" -f user="$bot_id" -f query='
  mutation($project: ID!, $user: ID!) {
    updateProjectV2Collaborators(input: {projectId: $project,
      collaborators: [{userId: $user, role: WRITER}]}) { clientMutationId }
  }' >/dev/null
echo "board collaborator: $BOT (writer)"

echo
echo "repository: https://github.com/$REPO"
echo "board: owner $OWNER, project $number"
