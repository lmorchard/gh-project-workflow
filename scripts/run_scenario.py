#!/usr/bin/env python3
"""Run one decision scenario against a snapshot of committed skill source."""

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
TASK_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ScenarioError(Exception):
    """An input or source snapshot could not be used."""


def git(root, *args):
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True,
    )
    if result.returncode:
        raise ScenarioError("Git could not read the requested source commit")
    return result.stdout.strip()


def extract_archive(root, commit, destination):
    archive = subprocess.run(
        ["git", "-C", str(root), "archive", "--format=tar", commit],
        capture_output=True,
    )
    if archive.returncode:
        raise ScenarioError("Git could not create the source snapshot")

    destination.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode="r:") as bundle:
        for member in bundle.getmembers():
            relative = PurePosixPath(member.name)
            if relative.is_absolute() or ".." in relative.parts:
                raise ScenarioError("Source snapshot contains an unsafe path")
            target = destination.joinpath(*relative.parts)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                source = bundle.extractfile(member)
                if source is None:
                    raise ScenarioError("Source snapshot contains an unreadable file")
                with source, target.open("wb") as output:
                    shutil.copyfileobj(source, output)
            elif member.issym():
                link_target = PurePosixPath(member.linkname)
                if link_target.is_absolute():
                    raise ScenarioError("Source snapshot contains an unsafe link")
                parts = list(relative.parent.parts)
                for part in link_target.parts:
                    if part == "..":
                        if not parts:
                            raise ScenarioError("Source snapshot contains an unsafe link")
                        parts.pop()
                    elif part not in ("", "."):
                        parts.append(part)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.symlink_to(member.linkname)
            else:
                raise ScenarioError("Source snapshot contains an unsupported entry")


def source_fingerprint(snapshot):
    entries = []
    for path in snapshot.rglob("*"):
        if path.is_file():
            relative = path.relative_to(snapshot).as_posix()
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            entries.append((relative, digest))
    stream = b"".join(
        relative.encode("utf-8") + b"\0" + digest.encode("ascii") + b"\n"
        for relative, digest in sorted(entries)
    )
    return hashlib.sha256(stream).hexdigest()


def scenario_parts(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ScenarioError("Scenario is missing frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ScenarioError("Scenario has incomplete frontmatter")
    header = text[4:end]
    skills = []
    in_skills = False
    for line in header.splitlines():
        if line.startswith("skills:"):
            in_skills = True
            value = line.partition(":")[2].strip()
            if value:
                if not (value.startswith("[") and value.endswith("]")):
                    raise ScenarioError("Scenario skills must be a list")
                skills.extend(item.strip().strip("'\" ") for item in value[1:-1].split(",")
                              if item.strip())
            continue
        if in_skills and line.lstrip().startswith("-"):
            skills.append(line.split("-", 1)[1].strip().strip("'\" "))
            continue
        if line and not line[0].isspace():
            in_skills = False

    body = text[end + 5:]
    sections = {}
    current = None
    for line in body.splitlines():
        heading = re.fullmatch(r"## (.+?)\s*", line)
        if heading:
            current = heading.group(1)
            if current in sections:
                raise ScenarioError(f"Scenario repeats the {current!r} section")
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    situation = sections.get("Situation")
    if situation is None:
        raise ScenarioError("Scenario is missing its Situation section")
    if not skills:
        raise ScenarioError("Scenario has no skills task names")
    return skills, "\n".join(situation).strip()


def resolve_tasks(snapshot, skills):
    paths = []
    for name in skills:
        if not TASK_NAME.fullmatch(name):
            raise ScenarioError(f"Unknown task name in scenario skills: {name}")
        path = snapshot / "references" / "tasks" / f"{name}.md"
        if not path.is_file():
            raise ScenarioError(f"Unknown task name in scenario skills: {name}")
        paths.append(path.resolve())
    return paths


def make_prompt(paths, situation):
    path_list = "\n".join(str(path) for path in paths)
    return (
        "Read these skills from this source snapshot and the shared references they link:\n"
        f"{path_list}\n\n"
        "You are the agent applying them. Here is the current situation:\n\n"
        f"{situation}\n\n"
        "What do you do next, and why? Name the skill rule that decides it. Do not run commands or change anything.\n"
    )


def runner_environment():
    env = os.environ.copy()
    for key in list(env):
        upper = key.upper()
        if upper.startswith(("GH_", "GITHUB_", "GHFLOW_", "GIT_")):
            env.pop(key)
    return env


def json_events(stdout):
    for line in stdout.splitlines():
        try:
            value = json.loads(line)
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(value, dict):
            yield value


def cli_version(runner, env):
    try:
        result = subprocess.run(
            [runner, "--version"], capture_output=True, text=True, env=env, timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "unavailable"
    if result.returncode:
        return "unavailable"
    lines = (result.stdout or result.stderr).strip().splitlines()
    return lines[0][:200] if lines else "unavailable"


def run_codex(prompt, model, snapshot, answer_path, env):
    command = [
        "codex", "exec", "--ephemeral", "--sandbox", "read-only",
        "--skip-git-repo-check", "--json", "--model", model,
        "--output-last-message", str(answer_path), "-",
    ]
    try:
        result = subprocess.run(
            command, input=prompt, text=True, capture_output=True, cwd=snapshot,
            env=env,
        )
        stdout = result.stdout
        session = None
        reported_model = None
        for event in json_events(stdout):
            session = session or event.get("session_id") or event.get("thread_id")
            reported_model = reported_model or event.get("model")
        answer = answer_path.read_text(encoding="utf-8") if answer_path.exists() else ""
        return result.returncode, str(session) if session else None, reported_model, answer
    except OSError:
        return None, None, None, ""


def run_claude(prompt, model, snapshot, env):
    command = [
        "claude", "--print", "--model", model, "--permission-mode", "dontAsk",
        "--tools", "Read,Glob,Grep,Skill", "--allowedTools", "Read", "Glob",
        "Grep", "Skill", "--add-dir", str(snapshot), "--strict-mcp-config",
        "--setting-sources", "project", "--no-session-persistence",
        "--output-format", "stream-json", "--verbose",
    ]
    try:
        result = subprocess.run(
            command, input=prompt, text=True, capture_output=True, cwd=snapshot,
            env=env,
        )
        session = None
        reported_model = None
        answer_parts = []
        for event in json_events(result.stdout):
            session = session or event.get("session_id")
            reported_model = reported_model or event.get("model")
            if event.get("type") == "result" and isinstance(event.get("result"), str):
                answer_parts = [event["result"]]
            elif event.get("type") == "assistant":
                message = event.get("message", {})
                for block in message.get("content", []) if isinstance(message, dict) else []:
                    if isinstance(block, dict) and block.get("type") == "text":
                        answer_parts.append(block.get("text", ""))
        answer = "\n".join(part for part in answer_parts if part)
        return result.returncode, str(session) if session else None, reported_model, answer
    except OSError:
        return None, None, None, ""


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("scenario", help="scenario name from evals/scenarios")
    result.add_argument("--runner", required=True, choices=("codex", "claude"))
    result.add_argument("--model", required=True)
    result.add_argument("--repeat", type=int, default=1)
    result.add_argument("--commit", default="HEAD", help="source commit (default: HEAD)")
    result.add_argument("--output-dir", type=Path)
    result.add_argument("--dry-run", action="store_true")
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    if args.repeat < 1:
        parser().error("--repeat must be at least 1")
    if args.output_dir is None and not args.dry_run:
        parser().error("--output-dir is required unless --dry-run is used")
    if "/" in args.scenario or "\\" in args.scenario:
        parser().error("scenario must be a name, not a path")
    scenario_name = args.scenario[:-3] if args.scenario.endswith(".md") else args.scenario

    try:
        commit = git(ROOT, "rev-parse", "--verify", f"{args.commit}^{{commit}}")
        with tempfile.TemporaryDirectory(prefix="ghflow-scenario-") as temp:
            snapshot = Path(temp) / "source"
            extract_archive(ROOT, commit, snapshot)
            fingerprint = source_fingerprint(snapshot)
            scenario = snapshot / "evals" / "scenarios" / f"{scenario_name}.md"
            if not scenario.is_file():
                raise ScenarioError(f"Unknown scenario: {scenario_name}")
            skills, situation = scenario_parts(scenario)
            paths = resolve_tasks(snapshot, skills)
            prompt = make_prompt(paths, situation)
            prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()

            if args.dry_run:
                print(f"source_commit: {commit}")
                print(f"source_fingerprint: {fingerprint}")
                print("resolved_skill_paths:")
                for path in paths:
                    print(f"  {path}")
                print(f"prompt_sha256: {prompt_hash}")
                print("prompt:")
                print(prompt, end="")
                return 0

            output_dir = args.output_dir.expanduser().resolve()
            output_dir.mkdir(parents=True, exist_ok=False)
            env = runner_environment()
            command_name = args.runner
            version = cli_version(command_name, env)
            runs = []
            answers = []
            started_at = datetime.now(timezone.utc).isoformat()
            for index in range(1, args.repeat + 1):
                answer_path = Path(temp) / f"answer-{index}.txt"
                if args.runner == "codex":
                    code, session, runtime_model, answer = run_codex(
                        prompt, args.model, snapshot, answer_path, env,
                    )
                else:
                    code, session, runtime_model, answer = run_claude(
                        prompt, args.model, snapshot, env,
                    )
                runs.append({
                    "repeat": index,
                    "session_id": session,
                    "exit_code": code,
                    "runner_model": runtime_model,
                    "prompt_sha256": prompt_hash,
                })
                answers.append(f"Scenario: {scenario_name}\nSession ID: {session or 'unreported'}\n\n{answer}\n")

            provenance = {
                "scenario": scenario_name,
                "source_commit": commit,
                "source_fingerprint_sha256": fingerprint,
                "runner": args.runner,
                "runner_version": version,
                "model": args.model,
                "prompt_sha256": prompt_hash,
                "repeat_count": args.repeat,
                "resolved_skill_paths": [str(path.relative_to(snapshot.resolve())) for path in paths],
                "runs": runs,
                "started_at_utc": started_at,
                "completed_at_utc": datetime.now(timezone.utc).isoformat(),
                "isolation": {
                    "source": "read-only git archive snapshot",
                    "scrubbed_environment_prefixes": ["GH_", "GITHUB_", "GHFLOW_", "GIT_"],
                },
            }
            (output_dir / "answers.txt").write_text("\n".join(answers), encoding="utf-8")
            (output_dir / "provenance.json").write_text(
                json.dumps(provenance, indent=2) + "\n", encoding="utf-8",
            )
            print(f"Wrote answers and provenance to {output_dir}")
            return 0 if all(run["exit_code"] == 0 for run in runs) else 1
    except (ScenarioError, OSError, tarfile.TarError) as error:
        print(f"run_scenario: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
