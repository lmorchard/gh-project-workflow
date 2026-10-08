import argparse
import json
from pathlib import Path


def list_tasks(tasks, owner=None, include_completed=False):
    return [task for task in tasks
            if (include_completed or not task["completed"])
            and (owner is None or task["owner"] == owner)]


def build_parser():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list")
    listing.add_argument("--data", default="sample.json")
    listing.add_argument("--owner")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    tasks = json.loads(Path(args.data).read_text())
    for task in list_tasks(tasks, owner=args.owner):
        print(f"{task['id']}: {task['title']}")


if __name__ == "__main__":
    main()
