"""One-use fixture setup for the issue 32 identity execution trial.

Usage: python3 setup.py SOURCE_CHECKOUT NEW_TEMP_DIRECTORY
Uses cli/fake_gh.py from the supplied source. No live credentials or network.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


source = Path(sys.argv[1]).resolve()
root = Path(sys.argv[2]).resolve()
root.mkdir()  # Refuse to overwrite a previous trial.
for directory in ("bin", "home", "repo", "logs"):
    (root / directory).mkdir()
python = str(Path(sys.executable).resolve())
git = shutil.which("git")
env = {
    "PATH": f"{Path(git).parent}:/usr/bin:/bin:/usr/sbin:/sbin",
    "HOME": str(root / "home"),
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_AUTHOR_NAME": "Fixture Setup",
    "GIT_AUTHOR_EMAIL": "setup@example.invalid",
    "GIT_COMMITTER_NAME": "Fixture Setup",
    "GIT_COMMITTER_EMAIL": "setup@example.invalid",
    "GIT_AUTHOR_DATE": "2026-10-09T12:00:00-07:00",
    "GIT_COMMITTER_DATE": "2026-10-09T12:00:00-07:00",
}


def git_setup(*args):
    return subprocess.check_output([git, "-C", str(root / "repo"), *args], env=env, text=True).strip()


issue = """# Item count wording

format_item_count must return '1 item' for one and '<count> items' for other non-negative integer counts.
Add deterministic local tests. Preserve the function name and signature.
Issue URL: https://github.com/trial-owner/identity-fixture/issues/1
Board: trial-owner project 1. Initial status: Backlog.
"""
(root / "repo" / "ISSUE.md").write_text(issue)
(root / "repo" / "labels.py").write_text('def format_item_count(count):\n    return f"{count} items"\n')
(root / "repo" / ".gitignore").write_text(".ghflow/\n.claude/\n__pycache__/\n")
(root / "repo" / "AGENTS.md").write_text("Use python3 -m unittest discover -v for local checks.\nKeep the implementation in the supplied trial/item-count worktree.\n")
git_setup("init", "--initial-branch=main")
git_setup("add", ".")
git_setup("-c", "commit.gpgsign=false", "commit", "-m", "Seed item count fixture")
base = git_setup("rev-parse", "HEAD")
checkout = root / "repo" / ".claude" / "worktrees" / "item-count"
git_setup("worktree", "add", "-b", "trial/item-count", str(checkout))
config = root / "repo" / ".ghflow"
config.mkdir()
token = root / "configured-token"
token.write_text("synthetic-configured-token\n")
token.chmod(0o600)
(config / "identity.json").write_text(json.dumps({
    "login": "TrialBot", "name": "Trial Bot", "email": "trial-bot@example.invalid", "token_file": str(token),
}, indent=2) + "\n")
(root / "board.json").write_text(json.dumps({
    "project_id": "PROJECT", "options": ["Backlog", "In progress", "In review", "Done"],
    "status": "Backlog", "on_board": True,
}) + "\n")
shutil.copyfile(source / "cli" / "fake_gh.py", root / "fake_gh.py")

boundary = f'''#!{python}
import json, os, pathlib, runpy, sys
ROOT = pathlib.Path({str(root)!r})
kind = pathlib.Path(sys.argv[0]).name
token = os.environ.get("GH_TOKEN")
token_source = {{"synthetic-configured-token": "configured-file", "synthetic-inherited-token": "inherited-GH_TOKEN"}}.get(token, "absent-or-other")
account = "TrialBot" if token_source == "configured-file" else "InheritedUser"
entry = {{"tool": kind, "argv": sys.argv[1:], "token_source": token_source,
    "github_token_present": "GITHUB_TOKEN" in os.environ,
    "author": [os.environ.get("GIT_AUTHOR_NAME"), os.environ.get("GIT_AUTHOR_EMAIL")],
    "committer": [os.environ.get("GIT_COMMITTER_NAME"), os.environ.get("GIT_COMMITTER_EMAIL")],
    "git_config_parameters": os.environ.get("GIT_CONFIG_PARAMETERS")}}
if kind == "gh":
    entry["account"] = account
with (ROOT / "logs" / "boundary.jsonl").open("a") as log:
    log.write(json.dumps(entry) + "\\n")
if kind == "git":
    os.execv({git!r}, [{git!r}, *sys.argv[1:]])
args = sys.argv[1:]
if args[:2] == ["api", "user"]:
    print(account if "--jq" in args else json.dumps({{"login": account}}))
elif args[:2] == ["issue", "view"]:
    print(json.dumps({{"number": 1, "title": "Item count wording", "body": (ROOT / "repo" / "ISSUE.md").read_text(), "url": "https://github.com/trial-owner/identity-fixture/issues/1", "comments": [], "labels": []}}))
else:
    os.environ["GHHOW_BOARD"] = str(ROOT / "board.json")
    runpy.run_path(str(ROOT / "fake_gh.py"), run_name="__main__")
'''
for tool in ("gh", "git"):
    path = root / "bin" / tool
    path.write_text(boundary)
    path.chmod(0o755)
# Explicit allowlist: no ambient credentials, keyring, user Git config, or SSH agent.
actor_env = dict(env)
actor_env.update({
    "PATH": f"{root / 'bin'}:{Path(python).parent}:/usr/bin:/bin:/usr/sbin:/sbin",
    "GH_TOKEN": "synthetic-inherited-token",
    "GITHUB_TOKEN": "synthetic-inherited-github-token",
    "GIT_AUTHOR_NAME": "Inherited Author", "GIT_AUTHOR_EMAIL": "inherited-author@example.invalid",
    "GIT_COMMITTER_NAME": "Inherited Committer", "GIT_COMMITTER_EMAIL": "inherited-committer@example.invalid",
    "GIT_CONFIG_PARAMETERS": "'credential.https://github.com.helper=!false' 'core.quotePath=false'",
    "PYTHONDONTWRITEBYTECODE": "1",
})
launcher = root / "run.py"
launcher.write_text(f'''#!{python}
import json, pathlib, subprocess, sys
ROOT = pathlib.Path({str(root)!r})
env = {actor_env!r}
result = subprocess.run(sys.argv[1:], cwd={str(checkout)!r}, env=env, capture_output=True, text=True)
entry = {{"argv": sys.argv[1:], "cwd": {str(checkout)!r}, "code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}}
for token in ("synthetic-configured-token", "synthetic-inherited-token", "synthetic-inherited-github-token"):
    entry["stdout"] = entry["stdout"].replace(token, "[synthetic-token-redacted]")
    entry["stderr"] = entry["stderr"].replace(token, "[synthetic-token-redacted]")
with (ROOT / "logs" / "commands.jsonl").open("a") as log:
    log.write(json.dumps(entry) + "\\n")
print(entry["stdout"], end="")
print(entry["stderr"], end="", file=sys.stderr)
sys.exit(result.returncode)
''')
print(json.dumps({"checkout": str(checkout), "base": base, "branch": "trial/item-count", "launcher": str(launcher), "source": str(source), "python": python}, indent=2))
