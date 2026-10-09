#!/usr/bin/env bash
# Delete remote branches whose current tip matches a merged PR head.
# Prints the plan by default; pass --yes to delete.
# Usage: scripts/delete-merged-branches.sh OWNER/REPO [--yes]
set -euo pipefail
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec python3 "$script_dir/delete-merged-branches.py" "$@"
