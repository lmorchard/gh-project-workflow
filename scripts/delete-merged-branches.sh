#!/usr/bin/env bash
# Delete remote branches whose PRs have merged, but only when the branch
# still points at the exact head that merged and no open PR uses it.
# Prints the plan by default; pass --yes to delete.
# Usage: scripts/delete-merged-branches.sh OWNER/REPO [--yes]
set -euo pipefail
if [ $# -lt 1 ] || [ $# -gt 2 ] || { [ $# -eq 2 ] && [ "$2" != "--yes" ]; }; then
  echo "Usage: $0 OWNER/REPO [--yes]" >&2
  exit 2
fi
repo=$1 apply=${2:-}

default=$(gh api "repos/$repo" --jq .default_branch)
branches=$(gh api "repos/$repo/branches" --paginate --jq '.[] | "\(.name) \(.commit.sha)"')
merged=$(gh pr list --repo "$repo" --state merged --limit 1000 \
  --json headRefName,headRefOid,number,isCrossRepository \
  --jq '.[] | select(.isCrossRepository | not) | "\(.headRefName) \(.headRefOid) \(.number)"')
open=$(gh pr list --repo "$repo" --state open --limit 1000 --json headRefName --jq '.[].headRefName')

count=0
while read -r name sha; do
  [ "$name" = "$default" ] && continue
  grep -qxF "$name" <<<"$open" && continue
  pr=$(awk -v n="$name" -v s="$sha" '$1 == n && $2 == s { print $3; exit }' <<<"$merged")
  [ -z "$pr" ] && continue
  count=$((count + 1))
  if [ "$apply" = "--yes" ]; then
    gh api -X DELETE "repos/$repo/git/refs/heads/$name" >/dev/null
    echo "deleted $name (PR #$pr, ${sha:0:7})"
  else
    echo "would delete $name (PR #$pr, ${sha:0:7})"
  fi
done <<<"$branches"

if [ "$apply" = "--yes" ]; then
  echo "$count branches deleted."
else
  echo "$count branches match. Run again with --yes to delete them."
fi
