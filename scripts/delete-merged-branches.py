#!/usr/bin/env python3
"""Delete merged branches only when current GitHub evidence still matches."""

import json
import re
import subprocess
import sys
from urllib.parse import quote


SHA = re.compile(r"^[0-9a-fA-F]{40}$")


class EvidenceError(Exception):
    """GitHub returned unread or invalid evidence."""


def gh_json(args, label):
    try:
        result = subprocess.run(["gh", "api", *args], text=True,
                                capture_output=True, check=False)
    except OSError as error:
        raise EvidenceError(f"could not run gh for {label}: {error}") from error
    if result.returncode:
        detail = result.stderr.strip() or f"gh exited with status {result.returncode}"
        raise EvidenceError(f"could not read {label}: {detail}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise EvidenceError(f"invalid JSON for {label}: {error}") from error


def paginated_json(endpoint, label):
    pages = gh_json(["--paginate", "--slurp", endpoint], label)
    if not isinstance(pages, list) or any(not isinstance(page, list) for page in pages):
        raise EvidenceError(f"invalid {label}: expected a list of paginated lists")
    return [item for page in pages for item in page]


def require_sha(value, label):
    if not isinstance(value, str) or not SHA.fullmatch(value):
        raise EvidenceError(f"invalid {label}: expected a full commit SHA")
    return value.lower()


def validate_repo(data):
    if not isinstance(data, dict):
        raise EvidenceError("invalid repository response: expected an object")
    name = data.get("full_name")
    default = data.get("default_branch")
    if not isinstance(name, str) or not name or not isinstance(default, str) or not default:
        raise EvidenceError("invalid repository response: missing full_name or default_branch")
    return name, default


def validate_branches(items):
    branches = {}
    for item in items:
        if not isinstance(item, dict):
            raise EvidenceError("invalid branch response: expected an object")
        name = item.get("name")
        commit = item.get("commit")
        if not isinstance(name, str) or not name or not isinstance(commit, dict):
            raise EvidenceError("invalid branch response: missing name or commit")
        sha = require_sha(commit.get("sha"), f"branch {name} tip")
        if name in branches:
            raise EvidenceError(f"invalid branch response: duplicate branch {name}")
        branches[name] = sha
    return branches


def validate_pulls(items):
    pulls = []
    for item in items:
        if not isinstance(item, dict):
            raise EvidenceError("invalid pull request response: expected an object")
        number = item.get("number")
        state = item.get("state")
        merged_at = item.get("merged_at")
        head = item.get("head")
        if (type(number) is not int or number < 1 or state not in ("open", "closed")
                or "merged_at" not in item
                or (merged_at is not None and not isinstance(merged_at, str))
                or not isinstance(head, dict)):
            raise EvidenceError("invalid pull request response: missing number, state, merge time, or head")
        if (state == "open" and merged_at is not None) or (merged_at == ""):
            raise EvidenceError(f"invalid pull request #{number}: inconsistent merge state")
        ref = head.get("ref")
        sha = head.get("sha")
        source = head.get("repo")
        if "repo" not in head or not isinstance(ref, str) or not ref or not isinstance(sha, str):
            raise EvidenceError(f"invalid pull request #{number}: missing head ref or SHA")
        require_sha(sha, f"pull request #{number} head")
        if source is not None and (not isinstance(source, dict)
                                   or not isinstance(source.get("full_name"), str)
                                   or not source.get("full_name")):
            raise EvidenceError(f"invalid pull request #{number}: invalid source repository")
        if state == "open" and source is None:
            raise EvidenceError(f"invalid pull request #{number}: open head source repository is unread")
        pulls.append({
            "number": number,
            "state": state,
            "merged": merged_at is not None,
            "ref": ref,
            "sha": sha.lower(),
            "source": source.get("full_name") if source else None,
        })
    return pulls


def current_branch(repo, name):
    escaped = quote(name, safe="")
    data = gh_json([f"repos/{repo}/branches/{escaped}"], f"branch {name} tip")
    if not isinstance(data, dict) or data.get("name") != name or not isinstance(data.get("commit"), dict):
        raise EvidenceError(f"invalid branch {name} tip response")
    return require_sha(data["commit"].get("sha"), f"branch {name} tip")


def delete_branch(repo, name):
    ref = quote(f"heads/{name}", safe="/")
    try:
        result = subprocess.run(["gh", "api", "-X", "DELETE", f"repos/{repo}/git/refs/{ref}"],
                                text=True, capture_output=True, check=False)
    except OSError as error:
        return False, str(error)
    if result.returncode:
        return False, result.stderr.strip() or f"gh exited with status {result.returncode}"
    return True, ""


def run(argv):
    if len(argv) not in (1, 2) or (len(argv) == 2 and argv[1] != "--yes"):
        print("Usage: scripts/delete-merged-branches.sh OWNER/REPO [--yes]", file=sys.stderr)
        return 2
    repo_arg = argv[0]
    if repo_arg.count("/") != 1 or any(not part or part in (".", "..") for part in repo_arg.split("/")):
        print("OWNER/REPO must name one repository", file=sys.stderr)
        return 2
    apply = len(argv) == 2

    try:
        repo, default = validate_repo(gh_json([f"repos/{repo_arg}"], "repository"))
        if repo.lower() != repo_arg.lower():
            raise EvidenceError(f"repository response did not match requested repository {repo_arg}")
        branches = validate_branches(paginated_json(
            f"repos/{repo}/branches?per_page=100", "branch inventory"))
        if default not in branches:
            raise EvidenceError(f"branch inventory did not contain default branch {default}")
        pulls = validate_pulls(paginated_json(
            f"repos/{repo}/pulls?state=all&per_page=100", "pull request inventory"))
    except EvidenceError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    open_sources = {(pull["source"], pull["ref"])
                    for pull in pulls if pull["state"] == "open"}
    merged_by_head = {}
    for pull in pulls:
        if pull["state"] == "closed" and pull["merged"] and pull["source"] == repo:
            key = (pull["ref"], pull["sha"])
            merged_by_head.setdefault(key, []).append(pull["number"])

    count = failures = 0
    for name, listed_sha in branches.items():
        if name == default or (repo, name) in open_sources:
            continue
        numbers = merged_by_head.get((name, listed_sha))
        if not numbers:
            continue
        pr = max(numbers)
        try:
            tip = current_branch(repo, name)
        except EvidenceError as error:
            print(f"failed to verify {name}: {error}", file=sys.stderr)
            failures += 1
            continue
        if tip != listed_sha:
            print(f"skipped {name}: tip changed since the branch inventory")
            continue
        if not apply:
            print(f"would delete {name} (PR #{pr}, {tip[:7]})")
            count += 1
            continue
        deleted, detail = delete_branch(repo, name)
        if deleted:
            print(f"deleted {name} (PR #{pr}, {tip[:7]})")
            count += 1
        else:
            print(f"failed to delete {name} (PR #{pr}): {detail}", file=sys.stderr)
            failures += 1

    if apply:
        print(f"{count} branches deleted; {failures} failures.")
    else:
        print(f"{count} branches match. Run again with --yes to delete them.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
