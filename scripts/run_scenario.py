#!/usr/bin/env python3
"""Run one decision scenario against a snapshot of committed skill source."""

import argparse
import hashlib
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TASK_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)")
SKIPPED_SOURCE_PREFIXES = ("evals/", "docs/research/trials/")
SKIPPED_SOURCE_FILES = {"docs/dev/skill-evaluations.md"}
MAX_DIAGNOSTIC_CHARS = 2000
SECRET_FIELD = re.compile(r"(?i)(token|api[_ -]?key|secret|password|credential|authorization)")
SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(api[_ -]?key|access[_ -]?token|refresh[_ -]?token|token|secret|password|authorization|credential)"
    r"(\s*[:=]\s*)(?:\"[^\"]*\"|'[^']*'|[^\s,;]+)"
)
BEARER_TOKEN = re.compile(r"(?i)\bBearer\s+[^\s,;]+")
JWT_TOKEN = re.compile(r"\beyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b")
PROVIDER_TOKEN = re.compile(
    r"\b(?:sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|"
    r"github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16})\b"
)
URL_CREDENTIAL = re.compile(r"(?i)(https?://)[^/@\s]+:[^/@\s]+@")


class ScenarioError(Exception):
    """An input or source snapshot could not be used."""


def git(root, *args):
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True,
    )
    if result.returncode:
        raise ScenarioError("Git could not read the requested source commit")
    return result.stdout.strip()


def source_paths(root, commit):
    result = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-r", "-z", "--full-tree", commit],
        capture_output=True,
    )
    if result.returncode:
        raise ScenarioError("Git could not list the requested source commit")
    paths = {}
    for entry in result.stdout.split(b"\0"):
        if not entry:
            continue
        metadata, path = entry.split(b"\t", 1)
        mode, object_type, object_id = metadata.split()
        if object_type == b"blob" and mode in (b"100644", b"100755"):
            paths[path.decode("utf-8")] = object_id.decode("ascii")
    return paths


def allowed_source_path(path):
    return (
        path.endswith(".md")
        and not path.startswith(SKIPPED_SOURCE_PREFIXES)
        and path not in SKIPPED_SOURCE_FILES
    )


def linked_source_paths(root, commit, skills):
    available = source_paths(root, commit)
    pending = [f"references/tasks/{name}.md" for name in skills]
    included = set()
    while pending:
        path = pending.pop()
        if path in included:
            continue
        if not allowed_source_path(path) or path not in available:
            raise ScenarioError(f"Required skill source is unavailable: {path}")
        included.add(path)
        content = subprocess.run(
            ["git", "-C", str(root), "cat-file", "blob", available[path]],
            capture_output=True,
        )
        if content.returncode:
            raise ScenarioError(f"Git could not read skill source: {path}")
        base = posixpath.dirname(path)
        for target in MARKDOWN_LINK.findall(content.stdout.decode("utf-8")):
            if target.startswith("#") or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                continue
            target_path = target.split("#", 1)[0].split("?", 1)[0]
            if not target_path:
                continue
            resolved = posixpath.normpath(posixpath.join(base, target_path))
            if resolved == ".." or resolved.startswith("../") or resolved.startswith("/"):
                continue
            if allowed_source_path(resolved) and resolved in available:
                pending.append(resolved)
    return {path: available[path] for path in sorted(included)}


def extract_source_snapshot(root, commit, skills, destination):
    paths = linked_source_paths(root, commit, skills)
    destination.mkdir(parents=True)
    for relative, object_id in paths.items():
        output = destination / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        source = subprocess.run(
            ["git", "-C", str(root), "cat-file", "blob", object_id],
            capture_output=True,
        )
        if source.returncode:
            raise ScenarioError(f"Git could not copy skill source: {relative}")
        output.write_bytes(source.stdout)
    return list(paths)


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


def scenario_parts(text):
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
        "Read only these skills from the committed source snapshot and the references they link:\n"
        f"{path_list}\n\n"
        "You are the agent applying them. Here is the current situation:\n\n"
        f"{situation}\n\n"
        "What do you do next, and why? Name the skill rule that decides it.\n"
        "Do not run commands, make edits, use network tools, dispatch agents, or ask the user questions.\n"
        "Use only the skill source and linked references that are available in the session source directory.\n"
    )


def runner_environment(runner, runtime_root):
    inherited = os.environ
    runtime_root.mkdir(parents=True, exist_ok=True)
    home = runtime_root / "home"
    home.mkdir(exist_ok=True)
    temp_dir = runtime_root / "tmp"
    temp_dir.mkdir(exist_ok=True)
    env = {"PATH": inherited.get("PATH", "/usr/bin:/bin"), "HOME": str(home),
           "TMPDIR": str(temp_dir)}
    for key in ("LANG", "LC_ALL", "LC_CTYPE", "TERM", "NO_COLOR"):
        if key in inherited:
            env[key] = inherited[key]

    if runner == "codex":
        codex_home = runtime_root / "codex-home"
        codex_home.mkdir(exist_ok=True)
        env["CODEX_HOME"] = str(codex_home)
        if inherited.get("OPENAI_API_KEY"):
            env["OPENAI_API_KEY"] = inherited["OPENAI_API_KEY"]
        else:
            original_home = Path(
                inherited.get("CODEX_HOME", Path.home() / ".codex"),
            ).expanduser()
            auth = original_home / "auth.json"
            if auth.is_file():
                shutil.copyfile(auth, codex_home / "auth.json")
                (codex_home / "auth.json").chmod(0o600)
    elif runner == "claude":
        # Claude's safe mode uses its normal authentication store but ignores user settings.
        if inherited.get("ANTHROPIC_API_KEY"):
            env["ANTHROPIC_API_KEY"] = inherited["ANTHROPIC_API_KEY"]
        env["HOME"] = inherited.get("HOME", str(Path.home()))
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


def _secret_values(value):
    values = []
    if isinstance(value, dict):
        for key, child in value.items():
            if SECRET_FIELD.search(str(key)) and isinstance(child, str) and child:
                values.append(child)
            values.extend(_secret_values(child))
    elif isinstance(value, list):
        for child in value:
            values.extend(_secret_values(child))
    return values


def known_secrets(env):
    values = [
        value for key, value in env.items()
        if SECRET_FIELD.search(key) and isinstance(value, str) and value
    ]
    auth_paths = []
    if env.get("CODEX_HOME"):
        auth_paths.append(Path(env["CODEX_HOME"]) / "auth.json")
    if env.get("HOME"):
        auth_paths.append(Path(env["HOME"]) / ".claude" / ".credentials.json")
    for path in auth_paths:
        try:
            values.extend(_secret_values(json.loads(path.read_text(encoding="utf-8"))))
        except (OSError, json.JSONDecodeError):
            continue
    return sorted(set(values), key=len, reverse=True)


def safe_diagnostic(diagnostic, env):
    if not diagnostic:
        return ""
    text = str(diagnostic).replace("\x00", "")
    for secret in known_secrets(env):
        text = text.replace(secret, "[REDACTED]")
    text = JWT_TOKEN.sub("[REDACTED_JWT]", text)
    text = PROVIDER_TOKEN.sub("[REDACTED_TOKEN]", text)
    text = URL_CREDENTIAL.sub(r"\1[REDACTED]@", text)
    text = BEARER_TOKEN.sub("Bearer [REDACTED]", text)
    text = SECRET_ASSIGNMENT.sub(r"\1\2[REDACTED]", text)
    if len(text) > MAX_DIAGNOSTIC_CHARS:
        text = text[:MAX_DIAGNOSTIC_CHARS] + "… [truncated]"
    return text.strip()


def run_codex(prompt, model, snapshot, answer_path, env):
    command = [
        "codex", "exec", "--ephemeral", "--sandbox", "read-only",
        "--ask-for-approval", "never", "--skip-git-repo-check",
        "--ignore-user-config", "--ignore-rules", "--no-daemon",
        "--disable", "apps", "--disable", "plugins", "--disable", "multi_agent",
        "--disable", "web_search_request", "--disable", "browser_use",
        "--config", 'shell_environment_policy.inherit="none"',
        "--config", "shell_environment_policy.ignore_default_excludes=false",
        "--config", 'shell_environment_policy.filters.PATH="include"',
        "--config", 'shell_environment_policy.filters.CODEX_HOME="exclude"',
        "--config", 'shell_environment_policy.filters.HOME="exclude"',
        "--config", 'shell_environment_policy.filters.OPENAI_API_KEY="exclude"',
        "--config", "sandbox_workspace_write.network_access=false",
        "--json", "--model", model,
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
        diagnostic = safe_diagnostic(result.stderr, env) if result.returncode else ""
        if result.returncode and not diagnostic:
            diagnostic = f"Runner exited with status {result.returncode} and no stderr diagnostic."
        return result.returncode, str(session) if session else None, reported_model, answer, diagnostic
    except OSError as error:
        return None, None, None, "", safe_diagnostic(f"{type(error).__name__}: {error}", env)


def run_claude(prompt, model, snapshot, session_cwd, env):
    command = [
        "claude", "--print", "--model", model, "--safe-mode", "--restricted",
        "--permission-mode", "dontAsk", "--tools", "Read,Glob,Grep",
        "--allowedTools", "Read", "Glob", "Grep", "--add-dir", str(snapshot),
        "--strict-mcp-config", "--permission-prompts", "none",
        "--no-session-persistence",
        "--output-format", "stream-json", "--verbose",
    ]
    try:
        result = subprocess.run(
            command, input=prompt, text=True, capture_output=True, cwd=session_cwd,
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
        diagnostic = safe_diagnostic(result.stderr, env) if result.returncode else ""
        if result.returncode and not diagnostic:
            diagnostic = f"Runner exited with status {result.returncode} and no stderr diagnostic."
        return result.returncode, str(session) if session else None, reported_model, answer, diagnostic
    except OSError as error:
        return None, None, None, "", safe_diagnostic(f"{type(error).__name__}: {error}", env)


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


def isolation_record(runner, source_files):
    shared = {
        "model_visible_source_files": source_files,
        "scenario_input": "Situation only; scenario criteria and evaluation records are not copied",
        "identity_and_github_environment": "removed by a minimal runner environment",
    }
    if runner == "claude":
        return {
            **shared,
            "runner_controls": [
                "--safe-mode", "--restricted", "--tools Read,Glob,Grep",
                "--allowedTools Read Glob Grep", "--strict-mcp-config",
                "--permission-prompts none", "--add-dir SOURCE_SNAPSHOT",
                "--no-session-persistence",
            ],
            "commands_and_edits": "blocked by restricted mode and the explicit read-only tool list",
            "network_and_dispatch": "no web, code, MCP, or agent tools are enabled; the runner still calls its model provider",
            "user_questions": "prompt-only; this noninteractive run has no user messaging tool",
            "source_boundary": "file tools are confined to the empty session directory and source snapshot",
            "authentication": "normal Claude authentication is available to the CLI; restricted file tools cannot read the home directory",
        }
    return {
        **shared,
        "runner_controls": [
            "--ephemeral", "--sandbox read-only", "--ask-for-approval never",
            "--ignore-user-config", "--ignore-rules", "--no-daemon",
            "--disable apps/plugins/multi_agent/web_search_request/browser_use",
            "shell_environment_policy.inherit=none",
        ],
        "edits_and_network": "blocked by the Codex read-only sandbox; MCP, apps, browser, and web search integrations are disabled",
        "commands": "prompt-only; the installed Codex CLI exposes shell commands without a tool allowlist",
        "agent_dispatch": "disabled by the multi_agent feature flag and isolated configuration",
        "user_questions": "prompt-only; this noninteractive run has no user messaging tool",
        "source_boundary": "the session workspace contains only allowed linked skill files; the Codex read-only sandbox can read files outside the workspace, so host-wide source access is not enforced",
        "authentication": "only OPENAI_API_KEY or auth.json is provided to the CLI; shell commands inherit neither CODEX_HOME nor HOME nor OPENAI_API_KEY",
    }


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
            tree = source_paths(ROOT, commit)
            scenario_path = f"evals/scenarios/{scenario_name}.md"
            scenario_object = tree.get(scenario_path)
            if scenario_object is None:
                raise ScenarioError(f"Unknown scenario: {scenario_name}")
            scenario_result = subprocess.run(
                ["git", "-C", str(ROOT), "cat-file", "blob", scenario_object],
                capture_output=True, text=True,
            )
            if scenario_result.returncode:
                raise ScenarioError(f"Git could not read scenario: {scenario_name}")
            skills, situation = scenario_parts(scenario_result.stdout)
            snapshot = Path(temp) / "source"
            snapshot_files = extract_source_snapshot(ROOT, commit, skills, snapshot)
            fingerprint = source_fingerprint(snapshot)
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
            env = runner_environment(args.runner, Path(temp) / "runtime")
            command_name = args.runner
            version = cli_version(command_name, env)
            session_cwd = Path(temp) / "session"
            session_cwd.mkdir()
            runs = []
            answers = []
            started_at = datetime.now(timezone.utc).isoformat()
            for index in range(1, args.repeat + 1):
                answer_path = Path(temp) / f"answer-{index}.txt"
                if args.runner == "codex":
                    code, session, runtime_model, answer, diagnostic = run_codex(
                        prompt, args.model, snapshot, answer_path, env,
                    )
                else:
                    code, session, runtime_model, answer, diagnostic = run_claude(
                        prompt, args.model, snapshot, session_cwd, env,
                    )
                runs.append({
                    "repeat": index,
                    "session_id": session,
                    "exit_code": code,
                    "runner_model": runtime_model,
                    "prompt_sha256": prompt_hash,
                    "diagnostic": diagnostic or None,
                })
                diagnostic_text = f"\nRunner diagnostic: {diagnostic}\n" if diagnostic else ""
                answers.append(
                    f"Scenario: {scenario_name}\nSession ID: {session or 'unreported'}\n\n"
                    f"{answer}{diagnostic_text}\n"
                )

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
                "source_snapshot_files": snapshot_files,
                "runs": runs,
                "started_at_utc": started_at,
                "completed_at_utc": datetime.now(timezone.utc).isoformat(),
                "isolation": isolation_record(args.runner, snapshot_files),
            }
            (output_dir / "answers.txt").write_text("\n".join(answers), encoding="utf-8")
            (output_dir / "provenance.json").write_text(
                json.dumps(provenance, indent=2) + "\n", encoding="utf-8",
            )
            print(f"Wrote answers and provenance to {output_dir}")
            return 0 if all(run["exit_code"] == 0 for run in runs) else 1
    except (ScenarioError, OSError) as error:
        print(f"run_scenario: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
