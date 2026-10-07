#!/usr/bin/env python3
"""Link the ghflow source skill into explicitly selected agent directories."""
import argparse
import os
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "skills/ghflow"
PERSONAL = {"claude": ".claude/skills", "codex": ".agents/skills", "opencode": ".config/opencode/skills"}
PROJECT = {"claude": ".claude/skills", "codex": ".agents/skills", "opencode": ".opencode/skills"}


def install(destinations, source=SOURCE):
    source = source.resolve()
    if not (source / "SKILL.md").is_file():
        raise ValueError(f"Missing source skill: {source}")
    # Check the full request before creating any links.
    for destination in destinations:
        for ancestor in destination.parents:
            if os.path.lexists(ancestor) and not ancestor.is_dir():
                raise ValueError(f"Destination ancestor is not a directory: {ancestor}")
        if os.path.lexists(destination):
            if destination.is_symlink() and destination.resolve() == source:
                continue
            raise ValueError(f"Refusing to overwrite existing entry: {destination}")
    for destination in destinations:
        if destination.is_symlink() and destination.resolve() == source:
            print(f"Already linked: {destination}")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        # symlink_to refuses a destination created after the preflight too.
        destination.symlink_to(source, target_is_directory=True)
        print(f"Linked: {destination} -> {source}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("agents", nargs="+", choices=PERSONAL, help="Agent destinations to install")
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--home", type=Path, default=None, help="Personal home (default: current user's home)")
    scope.add_argument("--project", type=Path, help="Install into this target project")
    args = parser.parse_args()
    root = (args.project or args.home or Path.home()).expanduser().resolve()
    locations = PROJECT if args.project else PERSONAL
    destinations = [root / locations[name] / "ghflow" for name in dict.fromkeys(args.agents)]
    try:
        install(destinations)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
