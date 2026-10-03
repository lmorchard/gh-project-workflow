#!/usr/bin/env python3
"""Deterministic GitHub reads and writes for the gh-project-workflow skills.

The command shells out to an authenticated `gh`. It reports facts and never
judges whether a review is favorable or whether work may merge.

A part that could not be read is null and has an entry in "errors". An empty
list means GitHub returned nothing. Exit status: 0 when every part was read,
2 when some parts failed, 1 when the PR or commit itself could not be read.
verify-commit exits 3 when the commit was read and an expectation is false.
board set-status exits 3 when it refuses a backward move.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

CHECK_RUN_STATES = {
    "SUCCESS": "passed",
    "NEUTRAL": "passed",
    "SKIPPED": "skipped",
    "CANCELLED": "canceled",
    "FAILURE": "failed",
    "TIMED_OUT": "failed",
    "STARTUP_FAILURE": "failed",
    "ACTION_REQUIRED": "failed",
    "STALE": "failed",
}
STATUS_CONTEXT_STATES = {
    "SUCCESS": "passed",
    "PENDING": "pending",
    "EXPECTED": "pending",
    "FAILURE": "failed",
    "ERROR": "failed",
}


class GhError(Exception):
    pass


def run_gh(args):
    """Run gh and return parsed JSON output."""
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise GhError((result.stderr or result.stdout).strip() or f"gh exited {result.returncode}")
    return json.loads(result.stdout) if result.stdout.strip() else None


def run_gh_paginated(path):
    """Read every page of a REST list endpoint."""
    pages = run_gh(["api", path, "--paginate", "--slurp"])
    return [item for page in pages for item in page]


def parse_pr(ref, repo):
    match = re.match(r"https://github\.com/([^/]+/[^/]+)/pull/(\d+)", ref)
    if match:
        return match.group(1), int(match.group(2))
    if ref.isdigit() and repo:
        return repo, int(ref)
    raise SystemExit("Give a PR URL, or a PR number with --repo OWNER/NAME.")


def parse_issue(ref, repo):
    match = re.match(r"https://github\.com/([^/]+/[^/]+)/issues/(\d+)", ref)
    if match:
        return match.group(1), int(match.group(2))
    if ref.isdigit() and repo:
        return repo, int(ref)
    raise SystemExit("Give an issue URL, or an issue number with --repo OWNER/NAME.")


def check_state(item):
    if item.get("__typename") == "StatusContext":
        return item.get("context"), STATUS_CONTEXT_STATES.get(item.get("state"), "unknown")
    if item.get("status") != "COMPLETED":
        return item.get("name"), "pending"
    return item.get("name"), CHECK_RUN_STATES.get(item.get("conclusion"), "unknown")


def summarize_ci(checks, required):
    """Combine check states. "green" needs every check passed or skipped and no required check missing."""
    if checks is None:
        return None
    states = {c["state"] for c in checks}
    if not checks:
        return "none"
    if "failed" in states or "canceled" in states or "unknown" in states:
        return "failing"
    if any(c["state"] == "missing" for c in checks):
        return "missing"
    if "pending" in states:
        return "pending"
    return "green"


def same_reviewer(requested, author):
    """Match a requested reviewer to a review author.

    GitHub records a Copilot request as "Copilot" but its reviews as
    "copilot-pull-request-reviewer".
    """
    requested, author = requested.lower(), author.lower()
    if requested == author:
        return True
    return requested == "copilot" and author.startswith("copilot")


def pr_state(repo, number, gh=run_gh, gh_paginated=run_gh_paginated):
    errors = []

    def part(name, read):
        try:
            return read()
        except (GhError, json.JSONDecodeError, TypeError, KeyError) as error:
            errors.append({"part": name, "error": str(error)})
            return None

    fields = "number,url,state,isDraft,mergeable,headRefOid,headRefName,baseRefName,reviewRequests,statusCheckRollup"
    try:
        pr = gh(["pr", "view", str(number), "--repo", repo, "--json", fields])
    except GhError as error:
        return {"repo": repo, "number": number, "errors": [{"part": "pr", "error": str(error)}]}, 1

    head = pr["headRefOid"]
    base = pr["baseRefName"]

    def read_required():
        rules = gh(["api", f"repos/{repo}/rules/branches/{base}"])
        return sorted(
            check["context"]
            for rule in rules
            if rule.get("type") == "required_status_checks"
            for check in rule["parameters"]["required_status_checks"]
        )

    required = part("required_checks", read_required)

    checks = []
    for item in pr.get("statusCheckRollup") or []:
        name, state = check_state(item)
        checks.append({"name": name, "state": state, "required": None if required is None else name in required})
    for name in required or []:
        if not any(c["name"] == name for c in checks):
            checks.append({"name": name, "state": "missing", "required": True})

    def read_reviews():
        reviews = gh_paginated(f"repos/{repo}/pulls/{number}/reviews")
        comments = gh_paginated(f"repos/{repo}/pulls/{number}/comments")
        counts = {}
        for comment in comments:
            review_id = comment.get("pull_request_review_id")
            counts[review_id] = counts.get(review_id, 0) + 1
        return [
            {
                "id": review["id"],
                "author": review["user"]["login"],
                "state": review["state"],
                "submitted_at": review.get("submitted_at"),
                "commit": review.get("commit_id"),
                "covers_head": review.get("commit_id") == head,
                "inline_comments": counts.get(review["id"], 0),
                "body": review.get("body") or "",
            }
            for review in reviews
        ]

    reviews = part("reviews", read_reviews)

    def read_requests():
        events = gh_paginated(f"repos/{repo}/issues/{number}/timeline")
        requests = []
        for event in events:
            if event.get("event") not in ("review_requested", "review_request_removed"):
                continue
            reviewer = (event.get("requested_reviewer") or {}).get("login") or (event.get("requested_team") or {}).get("slug")
            requests.append({
                "event": event["event"],
                "reviewer": reviewer,
                "requested_at": event.get("created_at"),
                "actor": (event.get("actor") or {}).get("login"),
            })
        return requests

    request_events = part("review_request_events", read_requests)

    latest_requests = None
    if request_events is not None:
        latest = {}
        for event in request_events:
            if event["event"] == "review_requested":
                latest[event["reviewer"]] = event
            else:
                latest.pop(event["reviewer"], None)
        latest_requests = []
        for reviewer, event in sorted(latest.items()):
            answered = None
            if reviews is not None:
                answered = any(
                    same_reviewer(reviewer, r["author"]) and (r["submitted_at"] or "") >= event["requested_at"]
                    for r in reviews
                )
            latest_requests.append({"reviewer": reviewer, "requested_at": event["requested_at"], "answered": answered})

    result = {
        "repo": repo,
        "number": pr["number"],
        "url": pr["url"],
        "state": pr["state"],
        "is_draft": pr["isDraft"],
        "mergeable": pr["mergeable"],
        "head": head,
        "head_branch": pr["headRefName"],
        "base": base,
        "ci": summarize_ci(checks, required),
        "checks": checks,
        "required_checks": required,
        "pending_review_requests": [r.get("login") or r.get("slug") or r.get("name") for r in pr.get("reviewRequests") or []],
        "latest_review_requests": latest_requests,
        "review_request_events": request_events,
        "reviews": reviews,
        "errors": errors,
    }
    return result, 2 if errors else 0


def verify_commit(repo, rev, subject=None, on=None, pr_head=None, gh=run_gh):
    """Resolve a published commit and compare it with what the caller expects it to be."""
    try:
        commit = gh(["api", f"repos/{repo}/commits/{rev}"])
    except GhError as error:
        result = {"repo": repo, "rev": rev, "errors": [{"part": "commit", "error": str(error)}]}
        if "No commit found" in str(error):
            result["note"] = "GitHub gives this error for an unpushed or missing commit and for an ambiguous or too-short prefix. Check that the commit is pushed, then retry with the full SHA."
        return result, 1

    sha = commit["sha"]
    message = commit["commit"]["message"]
    errors = []
    expectations = {}
    result = {
        "repo": repo,
        "rev": rev,
        "sha": sha,
        "subject": message.splitlines()[0] if message else "",
        "author_date": commit["commit"]["author"]["date"],
        "parents": [parent["sha"] for parent in commit.get("parents") or []],
        "expectations": expectations,
        "errors": errors,
    }

    if subject is not None:
        expectations["subject_matches"] = result["subject"] == subject.strip()

    if on is not None:
        try:
            # "behind" or "identical" means the commit is in the branch's history.
            status = gh(["api", f"repos/{repo}/compare/{on}...{sha}", "--jq", "{status}"])["status"]
            expectations["on_branch"] = status in ("behind", "identical")
        except (GhError, TypeError, KeyError) as error:
            errors.append({"part": "on_branch", "error": str(error)})
            expectations["on_branch"] = None

    if pr_head is not None:
        pr_repo, number = pr_head
        try:
            head = gh(["pr", "view", str(number), "--repo", pr_repo, "--json", "headRefOid"])["headRefOid"]
            result["pr_head"] = head
            expectations["is_pr_head"] = head == sha
        except (GhError, TypeError, KeyError) as error:
            errors.append({"part": "is_pr_head", "error": str(error)})
            expectations["is_pr_head"] = None

    if False in expectations.values():
        return result, 3
    return result, 2 if errors else 0


ISSUE_ITEMS_QUERY = """
query($owner: String!, $name: String!, $number: Int!) {
  repository(owner: $owner, name: $name) {
    issue(number: $number) {
      url
      projectItems(first: 50) {
        nodes {
          id
          project { id }
          fieldValueByName(name: "Status") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
        }
      }
    }
  }
}
"""


def board_set_status(repo, number, owner, project, status, allow_backward=False, gh=run_gh):
    """Move one issue to a status on one board, refusing backward moves, and read the result back."""
    result = {"issue": f"{repo}#{number}", "project": f"{owner}/{project}", "requested": status, "errors": []}

    def fail(part, error):
        result["errors"].append({"part": part, "error": str(error)})
        return result, 1

    def read_item():
        """Return the issue URL and its item on this board as (item_id, status), or None."""
        repo_owner, name = repo.split("/")
        data = gh(["api", "graphql", "-f", f"query={ISSUE_ITEMS_QUERY}", "-f", f"owner={repo_owner}", "-f", f"name={name}", "-F", f"number={number}"])
        issue = data["data"]["repository"]["issue"]
        for node in issue["projectItems"]["nodes"]:
            if node["project"]["id"] == project_id:
                return issue["url"], (node["id"], (node.get("fieldValueByName") or {}).get("name"))
        return issue["url"], None

    try:
        project_id = gh(["project", "view", str(project), "--owner", owner, "--format", "json"])["id"]
        fields = gh(["project", "field-list", str(project), "--owner", owner, "--format", "json"])["fields"]
        field = next(f for f in fields if f["name"] == "Status")
    except StopIteration:
        return fail("status_field", "The board has no Status field.")
    except (GhError, TypeError, KeyError) as error:
        return fail("board", error)

    options = [option["name"] for option in field["options"]]
    result["options"] = options
    matches = [name for name in options if name == status] or [name for name in options if name.lower() == status.lower()]
    if len(matches) != 1:
        return fail("status", f"No single Status option matches {status!r}.")
    target = matches[0]
    result["target"] = target

    try:
        url, item = read_item()
    except (GhError, TypeError, KeyError) as error:
        return fail("issue", error)
    result["before"] = item[1] if item else None
    result["added"] = False

    if item and item[1] == target:
        result.update(action="unchanged", after=target, readback_matches=True)
        return result, 0
    if item and item[1] in options and options.index(item[1]) > options.index(target) and not allow_backward:
        result.update(action="refused", after=item[1])
        result["reason"] = f"{item[1]} to {target} is a backward move. Pass --allow-backward only with a reason and authorization."
        return result, 3

    try:
        if item is None:
            item_id = gh(["project", "item-add", str(project), "--owner", owner, "--url", url, "--format", "json"])["id"]
            result["added"] = True
        else:
            item_id = item[0]
        option_id = next(option["id"] for option in field["options"] if option["name"] == target)
        gh(["project", "item-edit", "--id", item_id, "--project-id", project_id, "--field-id", field["id"],
            "--single-select-option-id", option_id, "--format", "json"])
    except (GhError, TypeError, KeyError) as error:
        return fail("write", error)
    result["action"] = "set"

    try:
        _, item = read_item()
        result["after"] = item[1] if item else None
    except (GhError, TypeError, KeyError) as error:
        result["errors"].append({"part": "readback", "error": str(error)})
        result["after"] = None
    result["readback_matches"] = result["after"] == target
    return result, 0 if result["readback_matches"] else 2


def resolve_identity(env=None, config_paths=None):
    """Resolve agent identity from environment variables and config files."""
    if env is None:
        env = os.environ
    if config_paths is None:
        config_paths = [
            Path(".ghflow/identity.json"),
            Path.home() / ".config" / "ghflow" / "identity.json",
        ]

    config_data = {}
    for p in config_paths:
        try:
            expanded = Path(p).expanduser()
            if expanded.is_file():
                with open(expanded, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                break
        except (OSError, json.JSONDecodeError):
            continue

    login = env.get("GHFLOW_IDENTITY_LOGIN") or env.get("GHFLOW_LOGIN") or config_data.get("login")
    name = env.get("GHFLOW_IDENTITY_NAME") or env.get("GHFLOW_NAME") or config_data.get("name") or login
    email = env.get("GHFLOW_IDENTITY_EMAIL") or env.get("GHFLOW_EMAIL") or config_data.get("email")
    token_file = env.get("GHFLOW_TOKEN_FILE") or env.get("GHFLOW_IDENTITY_TOKEN_FILE") or config_data.get("token_file")

    token_path = None
    token_present = False
    if token_file:
        token_path = Path(token_file).expanduser()
        token_present = token_path.is_file()
    elif "GH_TOKEN" in env:
        token_present = bool(env["GH_TOKEN"].strip())

    return {
        "login": login,
        "name": name,
        "email": email,
        "token_file": str(token_path) if token_path else None,
        "token_present": token_present,
        "configured": bool(login or token_path or "GH_TOKEN" in env),
    }


def identity_env(identity, base_env=None):
    """Build environment dict with GH_TOKEN, Git author/committer, and credential config."""
    env = dict(os.environ if base_env is None else base_env)
    token_file = identity.get("token_file")
    if token_file and "GH_TOKEN" not in env:
        p = Path(token_file).expanduser()
        if p.is_file():
            env["GH_TOKEN"] = p.read_text(encoding="utf-8").strip()

    name = identity.get("name")
    if name:
        env.setdefault("GIT_AUTHOR_NAME", name)
        env.setdefault("GIT_COMMITTER_NAME", name)

    email = identity.get("email")
    if email:
        env.setdefault("GIT_AUTHOR_EMAIL", email)
        env.setdefault("GIT_COMMITTER_EMAIL", email)

    if "GH_TOKEN" in env and "GIT_CONFIG_PARAMETERS" not in env:
        env["GIT_CONFIG_PARAMETERS"] = "'credential.https://github.com.helper=' 'credential.https://github.com.helper=!gh auth git-credential'"

    return env


def main(argv=None):
    parser = argparse.ArgumentParser(prog="ghflow", description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    state = commands.add_parser("pr-state", help="Report CI, review requests, and reviews for a PR's current head.")
    state.add_argument("pr", help="PR URL, or PR number with --repo")
    state.add_argument("--repo", help="OWNER/NAME when giving a PR number")
    verify = commands.add_parser("verify-commit", help="Resolve a published commit and check that it is the one you expect.")
    verify.add_argument("rev", help="commit SHA or prefix")
    verify.add_argument("--repo", required=True, help="OWNER/NAME")
    verify.add_argument("--subject", help="expected first line of the commit message")
    verify.add_argument("--on", metavar="BRANCH", help="branch whose history should contain the commit")
    verify.add_argument("--pr-head", metavar="PR", help="PR URL or number whose current head should be the commit")
    board = commands.add_parser("board", help="Project board operations.")
    board_commands = board.add_subparsers(dest="board_command", required=True)
    set_status = board_commands.add_parser("set-status", help="Move one issue to a board status, refusing backward moves, and read it back.")
    set_status.add_argument("issue", help="issue URL, or issue number with --repo")
    set_status.add_argument("--repo", help="OWNER/NAME when giving an issue number")
    set_status.add_argument("--owner", required=True, help="login that owns the project board")
    set_status.add_argument("--project", required=True, type=int, help="project board number")
    set_status.add_argument("--status", required=True, help="target Status option name")
    set_status.add_argument("--allow-backward", action="store_true", help="permit a backward move; use only with a reason and authorization")
    ident = commands.add_parser("identity", help="Report or export the configured agent identity.")
    ident.add_argument("--export", action="store_true", help="output shell export statements")
    exec_cmd = commands.add_parser("exec", help="Run a command under the configured agent identity.")
    exec_cmd.add_argument("exec_args", nargs=argparse.REMAINDER, help="command and arguments to run")
    args = parser.parse_args(argv)

    if args.command == "pr-state":
        repo, number = parse_pr(args.pr, args.repo)
        result, status = pr_state(repo, number)
    elif args.command == "verify-commit":
        pr_head = parse_pr(args.pr_head, args.repo) if args.pr_head else None
        result, status = verify_commit(args.repo, args.rev, args.subject, args.on, pr_head)
    elif args.command == "board":
        repo, number = parse_issue(args.issue, args.repo)
        result, status = board_set_status(repo, number, args.owner, args.project, args.status, args.allow_backward)
    elif args.command == "identity":
        identity = resolve_identity()
        if args.export:
            env = identity_env(identity)
            statements = []
            if "GH_TOKEN" in env:
                statements.append(f'export GH_TOKEN="{env["GH_TOKEN"]}"')
            if "GIT_AUTHOR_NAME" in env:
                statements.append(f'export GIT_AUTHOR_NAME="{env["GIT_AUTHOR_NAME"]}"')
            if "GIT_COMMITTER_NAME" in env:
                statements.append(f'export GIT_COMMITTER_NAME="{env["GIT_COMMITTER_NAME"]}"')
            if "GIT_AUTHOR_EMAIL" in env:
                statements.append(f'export GIT_AUTHOR_EMAIL="{env["GIT_AUTHOR_EMAIL"]}"')
            if "GIT_COMMITTER_EMAIL" in env:
                statements.append(f'export GIT_COMMITTER_EMAIL="{env["GIT_COMMITTER_EMAIL"]}"')
            if "GIT_CONFIG_PARAMETERS" in env:
                statements.append(f'export GIT_CONFIG_PARAMETERS="{env["GIT_CONFIG_PARAMETERS"]}"')
            sys.stdout.write("\n".join(statements) + ("\n" if statements else ""))
            return 0
        json.dump(identity, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0 if identity["configured"] else 1
    elif args.command == "exec":
        cmd_args = args.exec_args
        if cmd_args and cmd_args[0] == "--":
            cmd_args = cmd_args[1:]
        if not cmd_args:
            sys.stderr.write("Give a command to run with exec.\n")
            return 1
        identity = resolve_identity()
        env = identity_env(identity)
        res = subprocess.run(cmd_args, env=env)
        return res.returncode
    else:
        return 1
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return status


if __name__ == "__main__":
    sys.exit(main())
