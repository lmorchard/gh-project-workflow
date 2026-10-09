# Repository maintenance

These commands maintain the workflow source checkout and remote branches.
For changes to the skills, read [Skill style](skill-style.md) and [Skill evaluations](skill-evaluations.md).
Repository checks do not assess skill quality.

## Repository checks

Run `make check` before you commit.
It runs the Python tests, examines skill frontmatter and local Markdown links, and makes sure that the scenario index is current.
Frontmatter is metadata at the start of a Markdown file.
It also finds whitespace errors.

## Merged branch cleanup

Use `scripts/delete-merged-branches.sh OWNER/REPO` from the source checkout to list remote branches that qualify for removal.
A branch qualifies when its current tip matches the head of a merged pull request from the same repository.
Without `--yes`, the command only prints the plan. Add `--yes` to request deletion.

The command reads all branch and pull request pages and excludes the default branch.
Before it reports or deletes a candidate, it refreshes open pull requests and reads the branch tip again.
A new open pull request or push can still occur between those reads and GitHub processing the deletion.
The command cannot remove that race.
