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


def check_skills():
    errors = []
    for path in sorted(ROOT.glob("skills/*/SKILL.md")):
        rel = path.relative_to(ROOT)
        fields = frontmatter(path.read_text())
        if fields is None:
            errors.append(f"{rel}: missing frontmatter")
            continue
        name = fields.get("name", "")
        if name != path.parent.name:
            errors.append(f"{rel}: name {name!r} does not match directory")
        if not NAME.match(name):
            errors.append(f"{rel}: name {name!r} is not lowercase-hyphenated")
        description = fields.get("description", "")
        if not description:
            errors.append(f"{rel}: missing description")
        elif len(description) > 1024:
            errors.append(f"{rel}: description exceeds 1024 characters")
    return errors


def check_links():
    errors = []
    files = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.md"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    for name in files:
        path = ROOT / name
        if not path.exists():
            continue
        for target in LINK.findall(path.read_text()):
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
