import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import check
import run_scenario


ROOT = Path(__file__).resolve().parent.parent


class ScenarioRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.temp_path = Path(self.temp.name)
        self.bin = self.temp_path / "bin"
        self.bin.mkdir()
        self.repo = self.temp_path / "repo"
        (self.repo / "scripts").mkdir(parents=True)
        (self.repo / "references/tasks").mkdir(parents=True)
        (self.repo / "references/shared").mkdir(parents=True)
        (self.repo / "evals/scenarios").mkdir(parents=True)
        (self.repo / "evals/results").mkdir(parents=True)
        (self.repo / "docs/trials").mkdir(parents=True)
        (self.repo / "scripts/run_scenario.py").write_bytes(
            (ROOT / "scripts/run_scenario.py").read_bytes(),
        )
        (self.repo / "references/tasks/review-changes.md").write_text(
            "Read [Policy](../shared/policy.md).\n", encoding="utf-8",
        )
        (self.repo / "references/tasks/define-issue.md").write_text(
            "Before research, read [Research](research.md).\n", encoding="utf-8",
        )
        (self.repo / "references/tasks/research.md").write_text(
            "Research applies [Authorization](../shared/authorization.md).\n",
            encoding="utf-8",
        )
        (self.repo / "references/tasks/unselected-task.md").write_text(
            "UNSELECTED TASK MARKER\n", encoding="utf-8",
        )
        (self.repo / "references/shared/policy.md").write_text(
            "Use the stated policy.\n", encoding="utf-8",
        )
        (self.repo / "references/shared/authorization.md").write_text(
            "Use existing authorization.\n", encoding="utf-8",
        )
        (self.repo / "evals/scenarios/runner-case.md").write_text(
            "---\nskills: [review-changes]\nsource: test fixture\n---\n\n"
            "## Situation\n\nSituation sentinel.\n\n"
            "## Expected\n\nExpected sentinel.\n\n"
            "## Not acceptable\n\nNot acceptable sentinel.\n",
            encoding="utf-8",
        )
        (self.repo / "evals/results/prior.md").write_text("PRIOR RESULT MARKER\n")
        (self.repo / "docs/trials/prior.md").write_text("PRIOR TRIAL MARKER\n")
        (self.repo / "docs/skill-evaluations.md").write_text("EVALUATION GUIDANCE MARKER\n")
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "Test"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.repo), "-c", "commit.gpgsign=false",
                        "commit", "-qm", "fixture source"], check=True)

    @property
    def runner_script(self):
        return self.repo / "scripts/run_scenario.py"

    def install_fake_runner(self, name, log_path):
        path = self.bin / name
        log_literal = repr(str(log_path))
        path.write_text("#!" + sys.executable + "\n" + f"LOG = {log_literal}\n" + """
import json
import os
import sys
from pathlib import Path
if '--version' in sys.argv:
    print('fake-runner-1')
else:
    model = sys.argv[sys.argv.index('--model') + 1] if '--model' in sys.argv else ''
    if model == 'fake-failure':
        secret = os.environ.get('OPENAI_API_KEY') or os.environ.get('ANTHROPIC_API_KEY')
        if not secret:
            try:
                auth = json.loads((Path(os.environ['CODEX_HOME']) / 'auth.json').read_text())
                secret = auth.get('access_token', 'synthetic-auth-secret')
            except (KeyError, OSError, json.JSONDecodeError):
                secret = 'synthetic-auth-secret'
        print('provider failed: token=' + secret + ' ' + ('x' * 5000), file=sys.stderr)
        sys.exit(7)
    cwd = Path.cwd()
    files = sorted(path.relative_to(cwd).as_posix() for path in cwd.rglob('*') if path.is_file())
    source_arg = sys.argv.index('--add-dir') + 1 if '--add-dir' in sys.argv else None
    source = Path(sys.argv[source_arg]) if source_arg is not None else cwd
    source_files = sorted(path.relative_to(source).as_posix() for path in source.rglob('*') if path.is_file())
    record = {
        'args': sys.argv[1:],
        'cwd': str(cwd),
        'files': files,
        'source_files': source_files,
        'prompt': sys.stdin.read(),
        'env_keys': sorted(os.environ),
        'codex_config_exists': (Path(os.environ.get('CODEX_HOME', '/missing')) / 'config.toml').exists(),
        'codex_auth_exists': (Path(os.environ.get('CODEX_HOME', '/missing')) / 'auth.json').exists(),
        'codex_home': os.environ.get('CODEX_HOME'),
        'home': os.environ.get('HOME'),
        'xdg_config_home': os.environ.get('XDG_CONFIG_HOME'),
    }
    with open(LOG, 'a', encoding='utf-8') as output:
        output.write(json.dumps(record) + '\\n')
    if '--output-last-message' in sys.argv:
        answer = Path(sys.argv[sys.argv.index('--output-last-message') + 1])
        answer.write_text('fake answer', encoding='utf-8')
        event = {'type': 'thread.started', 'thread_id': 'fake-session', 'model': 'reported-model'}
    else:
        event = {'type': 'result', 'session_id': 'fake-session', 'result': 'fake answer'}
    print(json.dumps(event))
""", encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path

    def run_fixture(self, runner, output, model="fake-model", path=None):
        env = os.environ.copy()
        env.update({
            "PATH": (
                str(path) if path is not None
                else str(self.bin) + os.pathsep + env.get("PATH", "")
            ),
            "GH_TOKEN": "synthetic-gh-value",
            "GITHUB_TOKEN": "synthetic-github-value",
            "GHFLOW_IDENTITY_LOGIN": "synthetic-login",
            "GIT_AUTHOR_NAME": "synthetic-author",
        })
        result = subprocess.run(
            [sys.executable, str(self.runner_script), "runner-case", "--runner", runner,
             "--model", model, "--repeat", "1", "--output-dir", str(output)],
            cwd=self.repo, env=env, capture_output=True, text=True,
        )
        return result

    def test_every_scenario_uses_known_task_names(self):
        self.assertEqual(check.check_scenario_skills(ROOT), [])

    def test_unknown_task_name_fails_check(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "references/tasks").mkdir(parents=True)
            (root / "references/tasks/implement-issue.md").write_text("task")
            scenario = root / "evals/scenarios/unknown.md"
            scenario.parent.mkdir(parents=True)
            scenario.write_text("---\nskills: [missing-task]\n---\n")
            self.assertEqual(check.check_scenario_skills(root), [
                "evals/scenarios/unknown.md: unknown task in skills: missing-task",
            ])

    def test_fingerprint_uses_sorted_path_nul_digest_lines(self):
        snapshot = self.temp_path / "snapshot"
        snapshot.mkdir()
        (snapshot / "z.txt").write_text("z", encoding="utf-8")
        (snapshot / "a.txt").write_text("a", encoding="utf-8")
        stream = b"a.txt\0" + hashlib.sha256(b"a").hexdigest().encode() + b"\n"
        stream += b"z.txt\0" + hashlib.sha256(b"z").hexdigest().encode() + b"\n"
        expected = hashlib.sha256(stream).hexdigest()
        self.assertEqual(run_scenario.source_fingerprint(snapshot), expected)

    def test_snapshot_contains_only_selected_skill_and_linked_references(self):
        commit = run_scenario.git(self.repo, "rev-parse", "HEAD")
        snapshot = self.temp_path / "source"
        files = run_scenario.extract_source_snapshot(
            self.repo, commit, ["review-changes"], snapshot,
        )
        self.assertEqual(files, [
            "references/shared/policy.md",
            "references/tasks/review-changes.md",
        ])
        for excluded in (
            "evals/scenarios/runner-case.md", "evals/results/prior.md",
            "docs/trials/prior.md", "docs/skill-evaluations.md",
            "references/tasks/unselected-task.md",
        ):
            self.assertFalse((snapshot / excluded).exists(), excluded)

    def test_snapshot_recursively_includes_linked_task_and_shared_references(self):
        commit = run_scenario.git(self.repo, "rev-parse", "HEAD")
        snapshot = self.temp_path / "linked-source"
        files = run_scenario.extract_source_snapshot(
            self.repo, commit, ["define-issue"], snapshot,
        )
        self.assertEqual(files, [
            "references/shared/authorization.md",
            "references/tasks/define-issue.md",
            "references/tasks/research.md",
        ])
        self.assertFalse((snapshot / "evals/scenarios/runner-case.md").exists())
        self.assertFalse((snapshot / "evals/results/prior.md").exists())

    def test_prompt_contains_situation_and_explicit_limits_only(self):
        text = (self.repo / "evals/scenarios/runner-case.md").read_text()
        skills, situation = run_scenario.scenario_parts(text)
        snapshot = self.temp_path / "prompt-source"
        run_scenario.extract_source_snapshot(
            self.repo, run_scenario.git(self.repo, "rev-parse", "HEAD"), skills, snapshot,
        )
        prompt = run_scenario.make_prompt(
            run_scenario.resolve_tasks(snapshot, skills), situation,
        )
        self.assertIn("Situation sentinel.", prompt)
        self.assertNotIn("Expected sentinel.", prompt)
        self.assertNotIn("Not acceptable sentinel.", prompt)
        for limit in ("Do not run commands", "make edits", "use network tools",
                      "dispatch agents", "ask the user questions"):
            self.assertIn(limit, prompt)

    def test_dry_run_prints_prompt_and_does_not_launch_runner(self):
        marker = self.temp_path / "invoked"
        self.install_fake_runner("codex", marker)
        env = os.environ.copy()
        env["PATH"] = str(self.bin) + os.pathsep + env.get("PATH", "")
        result = subprocess.run(
            [sys.executable, str(self.runner_script), "runner-case", "--runner", "codex",
             "--model", "fake-model", "--dry-run"],
            cwd=self.repo, env=env, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("references/tasks/review-changes.md", result.stdout)
        self.assertIn("Situation sentinel.", result.stdout)
        self.assertNotIn("Expected sentinel.", result.stdout)
        self.assertNotIn("Not acceptable sentinel.", result.stdout)
        self.assertFalse(marker.exists())

    def test_codex_isolates_user_config_and_records_effective_workspace(self):
        log = self.temp_path / "codex.jsonl"
        self.install_fake_runner("codex", log)
        old_home = self.temp_path / "caller-home"
        old_codex_home = old_home / ".codex"
        old_codex_home.mkdir(parents=True)
        (old_codex_home / "config.toml").write_text(
            '[mcp_servers.unrelated]\nurl = "https://example.invalid"\n',
        )
        (old_codex_home / "auth.json").write_text(
            '{"access_token": "synthetic-auth-secret"}',
        )
        output = self.temp_path / "codex-run"
        with patch.dict(os.environ, {
            "HOME": str(old_home), "CODEX_HOME": str(old_codex_home),
            "XDG_CONFIG_HOME": str(old_home / ".config"),
        }, clear=False):
            result = self.run_fixture("codex", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads(log.read_text().splitlines()[0])
        args = record["args"]
        for flag in ("--ignore-user-config", "--ignore-rules", "--no-daemon",
                     "--ephemeral", "--sandbox", "read-only", "--disable", "multi_agent"):
            self.assertIn(flag, args)
        self.assertNotIn("--search", args)
        self.assertTrue(any("shell_environment_policy.inherit=\"none\"" in value for value in args))
        self.assertFalse(record["codex_config_exists"])
        self.assertTrue(record["codex_auth_exists"])
        self.assertNotEqual(record["codex_home"], str(old_codex_home))
        self.assertNotEqual(record["home"], str(old_home))
        self.assertIsNone(record["xdg_config_home"])
        self.assertEqual(record["files"], [
            "references/shared/policy.md", "references/tasks/review-changes.md",
        ])
        self.assertEqual(record["prompt"].count("Situation sentinel."), 1)
        self.assertNotIn("Expected sentinel.", record["prompt"])
        self.assertNotIn("Not acceptable sentinel.", record["prompt"])
        self.assertNotIn("GH_TOKEN", record["env_keys"])
        self.assertNotIn("GITHUB_TOKEN", record["env_keys"])
        self.assertNotIn("GHFLOW_IDENTITY_LOGIN", record["env_keys"])
        self.assertNotIn("GIT_AUTHOR_NAME", record["env_keys"])
        self.assertNotIn("XDG_CONFIG_HOME", record["env_keys"])
        provenance = json.loads((output / "provenance.json").read_text())
        self.assertEqual(provenance["source_snapshot_files"], record["files"])
        self.assertIn("host-wide source access is not enforced",
                      provenance["isolation"]["source_boundary"])
        self.assertIn("prompt-only", provenance["isolation"]["commands"])
        self.assertEqual((output / "answers.txt").read_text().count("fake answer"), 1)

    def test_claude_restricts_tools_and_source_directories(self):
        log = self.temp_path / "claude.jsonl"
        self.install_fake_runner("claude", log)
        old_home = self.temp_path / "claude-home"
        (old_home / ".claude").mkdir(parents=True)
        (old_home / ".claude/settings.json").write_text(
            '{"hooks":{"SessionStart":[{"command":"unrelated"}]}}',
        )
        output = self.temp_path / "claude-run"
        with patch.dict(os.environ, {"HOME": str(old_home)}, clear=False):
            result = self.run_fixture("claude", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads(log.read_text().splitlines()[0])
        args = record["args"]
        for flag in ("--safe-mode", "--restricted", "--strict-mcp-config",
                     "--permission-prompts", "none", "--no-session-persistence",
                     "Read,Glob,Grep"):
            self.assertIn(flag, args)
        self.assertNotIn("--setting-sources", args)
        self.assertNotIn("Bash", args)
        self.assertEqual(record["files"], [])
        self.assertEqual(record["source_files"], [
            "references/shared/policy.md", "references/tasks/review-changes.md",
        ])
        self.assertEqual(record["prompt"].count("Situation sentinel."), 1)
        self.assertNotIn("Expected sentinel.", record["prompt"])
        self.assertNotIn("Not acceptable sentinel.", record["prompt"])
        self.assertNotIn("GH_TOKEN", record["env_keys"])
        self.assertNotIn("GITHUB_TOKEN", record["env_keys"])
        provenance = json.loads((output / "provenance.json").read_text())
        self.assertIn("file tools are confined", provenance["isolation"]["source_boundary"])
        self.assertIn("blocked", provenance["isolation"]["commands_and_edits"])

    def test_runner_failure_keeps_bounded_redacted_diagnostic(self):
        for runner in ("codex", "claude"):
            with self.subTest(runner=runner):
                log = self.temp_path / f"{runner}-failure.jsonl"
                self.install_fake_runner(runner, log)
                caller_home = self.temp_path / f"{runner}-caller-home"
                caller_home.mkdir()
                caller_codex_home = caller_home / ".codex"
                caller_codex_home.mkdir()
                (caller_codex_home / "auth.json").write_text(
                    '{"access_token": "synthetic-auth-secret"}',
                )
                output = self.temp_path / f"{runner}-failure-run"
                with patch.dict(os.environ, {
                    "HOME": str(caller_home), "CODEX_HOME": str(caller_codex_home),
                    "OPENAI_API_KEY": "", "ANTHROPIC_API_KEY": "",
                }, clear=False):
                    result = self.run_fixture(runner, output, model="fake-failure")
                self.assertEqual(result.returncode, 1, result.stderr)
                provenance_text = (output / "provenance.json").read_text()
                answers = (output / "answers.txt").read_text()
                diagnostic = json.loads(provenance_text)["runs"][0]["diagnostic"]
                self.assertIn("provider failed", diagnostic)
                self.assertIn("[REDACTED]", diagnostic)
                self.assertIn("truncated", diagnostic)
                self.assertLessEqual(len(diagnostic), run_scenario.MAX_DIAGNOSTIC_CHARS + 15)
                self.assertIn("Runner diagnostic:", answers)
                for output_text in (result.stdout, result.stderr, provenance_text, answers):
                    self.assertNotIn("synthetic-auth-secret", output_text)

    def test_runner_launch_error_is_recorded_in_answer_and_provenance(self):
        empty_path = self.temp_path / "no-runners"
        empty_path.mkdir()
        (empty_path / "git").symlink_to(shutil.which("git"))
        for runner in ("codex", "claude"):
            with self.subTest(runner=runner):
                output = self.temp_path / f"{runner}-launch-error"
                caller_home = self.temp_path / f"{runner}-missing-home"
                (caller_home / ".codex").mkdir(parents=True)
                with patch.dict(os.environ, {
                    "HOME": str(caller_home),
                    "CODEX_HOME": str(caller_home / ".codex"),
                    "OPENAI_API_KEY": "", "ANTHROPIC_API_KEY": "",
                }, clear=False):
                    result = self.run_fixture(runner, output, path=empty_path)
                self.assertEqual(result.returncode, 1, result.stderr)
                provenance_text = (output / "provenance.json").read_text()
                answer_text = (output / "answers.txt").read_text()
                run = json.loads(provenance_text)["runs"][0]
                self.assertIsNone(run["exit_code"])
                self.assertIn("FileNotFoundError", run["diagnostic"])
                self.assertIn("Runner diagnostic:", answer_text)


if __name__ == "__main__":
    unittest.main()
