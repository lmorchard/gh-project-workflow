# Reconstructed fixture setup

The original setup notes recorded the base and head identifiers, synthetic identity, fixed dates, and isolated environment. They did not preserve every command or the base source. This recipe reconstructs those commands from the preserved fixture and session context. I ran it in a new temporary repository. It produced the same base and head identifiers and passed the two tests.

Set `SOURCE_ROOT` to this workflow checkout. Set `FIXTURE_ROOT` to a new path that does not exist. These commands use `/private/tmp/ghflow-issue32-reconstructed` for the validation run.

```sh
export SOURCE_ROOT=/Users/lmorchard/devel/mine/gh-project-workflow/.claude/worktrees/issue-32-unpublished-handoff-trial
export FIXTURE_ROOT=/private/tmp/ghflow-issue32-reconstructed
mkdir -p "$FIXTURE_ROOT/repo" "$FIXTURE_ROOT/home"
cp "$SOURCE_ROOT/docs/research/trials/2026-10-08-issue-32-fixture/ISSUE.md" "$FIXTURE_ROOT/repo/ISSUE.md"
cat > "$FIXTURE_ROOT/repo/labels.py" <<'EOF'
def format_item_count(count):
    return f"{count} items"
EOF
env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin HOME="$FIXTURE_ROOT/home" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C "$FIXTURE_ROOT/repo" init --initial-branch=main
env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin HOME="$FIXTURE_ROOT/home" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C "$FIXTURE_ROOT/repo" -c user.name='Trial Fixture' -c user.email='trial-fixture@example.invalid' add ISSUE.md labels.py
env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin HOME="$FIXTURE_ROOT/home" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_DATE='2026-10-08T10:00:00-07:00' GIT_COMMITTER_DATE='2026-10-08T10:00:00-07:00' git -C "$FIXTURE_ROOT/repo" -c user.name='Trial Fixture' -c user.email='trial-fixture@example.invalid' -c commit.gpgsign=false commit -m 'Add item count formatter fixture'
env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin HOME="$FIXTURE_ROOT/home" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C "$FIXTURE_ROOT/repo" branch -m trial/item-count-singular
cp "$SOURCE_ROOT/docs/research/trials/2026-10-08-issue-32-fixture/labels.py" "$FIXTURE_ROOT/repo/labels.py"
cp "$SOURCE_ROOT/docs/research/trials/2026-10-08-issue-32-fixture/test_labels.py" "$FIXTURE_ROOT/repo/test_labels.py"
env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin HOME="$FIXTURE_ROOT/home" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C "$FIXTURE_ROOT/repo" add labels.py test_labels.py
env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin HOME="$FIXTURE_ROOT/home" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_DATE='2026-10-08T10:01:00-07:00' GIT_COMMITTER_DATE='2026-10-08T10:01:00-07:00' git -C "$FIXTURE_ROOT/repo" -c user.name='Trial Fixture' -c user.email='trial-fixture@example.invalid' -c commit.gpgsign=false commit -m 'Use singular item label for count one'
env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin HOME="$FIXTURE_ROOT/home" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C "$FIXTURE_ROOT/repo" rev-parse HEAD^ HEAD
cd "$FIXTURE_ROOT/repo"
env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin HOME="$FIXTURE_ROOT/home" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_labels
env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin HOME="$FIXTURE_ROOT/home" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git status --short --branch
env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin HOME="$FIXTURE_ROOT/home" GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git remote -v
```

The base source is the `labels.py` written in the recipe. The changed source and test are copied from [the preserved fixture](2026-10-08-issue-32-fixture/). The recipe uses explicit Git identity, fixed author and committer dates, no system or global Git config, a temporary home, and no remote. It does not use the `ghflow` wrapper or any credentials.

The validation run returned base `654dda1dc68426c4f4081fb6d5b4d031700418b0` and head `aa4d2736388edd34051bcbbce6bb417678d16683`. Both tests passed, the branch was clean, and `git remote -v` returned no output.

The first setup attempt in the original session failed with `Couldn't get agent socket?` and `fatal: failed to write commit object`. The exact original command was not retained in the setup notes. The error output alone does not establish which inherited Git setting caused the failure. The reconstructed recipe disables system and global Git config and disables signing for its two commits. It does not attempt to reproduce that failure.
