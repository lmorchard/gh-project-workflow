#!/usr/bin/env python3
"""Check skill frontmatter and local Markdown links."""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def check_skills(root=ROOT):
    errors = []
    inventory = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "*SKILL.md"],
        cwd=root, capture_output=True, text=True,
    )
    if inventory.returncode == 0:
        paths = sorted(root / name for name in inventory.stdout.split("\0")
                       if name and (root / name).is_file())
    else:
        paths = sorted(root.glob("**/SKILL.md"))
    expected = root / "SKILL.md"
    if paths != [expected]:
        errors.append("skills: expected only root SKILL.md")
    task_dir = root / "references/tasks"
    tasks = set(task_dir.glob("*.md")) - {task_dir / "research.md"}
    if not tasks:
        errors.append("skills: no task references")
    if expected.exists():
        routed = {(expected.parent / target.split("#")[0]).resolve()
                  for target in LINK.findall(expected.read_text())}
        for task in sorted(tasks):
            if task.resolve() not in routed:
                errors.append(f"{task.relative_to(root)}: not reachable from entry skill")
            if frontmatter(task.read_text()) is not None:
                errors.append(f"{task.relative_to(root)}: task reference has skill frontmatter")
    for path in paths:
        rel = path.relative_to(root)
        fields = frontmatter(path.read_text())
        if fields is None:
            errors.append(f"{rel}: missing frontmatter")
            continue
        name = fields.get("name", "")
        if name != "ghflow":
            errors.append(f"{rel}: name {name!r} must be ghflow")
        if not NAME.match(name):
            errors.append(f"{rel}: name {name!r} is not lowercase-hyphenated")
        description = fields.get("description", "")
        if not description:
            errors.append(f"{rel}: missing description")
        elif len(description) > 1024:
            errors.append(f"{rel}: description exceeds 1024 characters")
    return errors


def check_links(root=ROOT):
    errors = []
    files = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.md"],
        cwd=root, capture_output=True, text=True, check=True,
    ).stdout.split()
    for name in files:
        path = root / name
        if not path.exists():
            continue
        text = path.read_text()
        if path.is_relative_to(root / "evals/scenarios"):
            for line in text.splitlines():
                if line.startswith("source:"):
                    for source in re.findall(r"\b(?:skills|references)/[a-zA-Z0-9_/.-]+", line):
                        if not (root / source).exists():
                            errors.append(f"{name}: broken scenario source {source}")
        for target in LINK.findall(text):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            if not (path.parent / target.split("#")[0]).exists():
                errors.append(f"{name}: broken link {target}")
    return errors


def main():
    errors = check_skills() + check_links()
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
