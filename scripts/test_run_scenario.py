import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

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
        (self.repo / "evals/scenarios").mkdir(parents=True)
        (self.repo / "scripts/run_scenario.py").write_bytes(
            (ROOT / "scripts/run_scenario.py").read_bytes(),
        )
        (self.repo / "references/tasks/review-changes.md").write_text(
            "Review the supplied changes.\n", encoding="utf-8",
        )
        (self.repo / "evals/scenarios/runner-case.md").write_text(
            "---\nskills: [review-changes]\nsource: test fixture\n---\n\n"
            "## Situation\n\nSituation sentinel.\n\n"
            "## Expected\n\nExpected sentinel.\n\n"
            "## Not acceptable\n\nNot acceptable sentinel.\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "Test"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.repo), "-c", "commit.gpgsign=false",
                        "commit", "-qm", "fixture source"], check=True)

    @property
    def runner_script(self):
        return self.repo / "scripts/run_scenario.py"

    def install_fake_runner(self, name, body):
        path = self.bin / name
        path.write_text("#!" + sys.executable + "\n" + body, encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path

    def test_every_scenario_uses_known_task_names(self):
        self.assertEqual(check.check_scenario_skills(ROOT), [])

    def test_fingerprint_uses_sorted_path_nul_digest_lines(self):
        snapshot = self.temp_path / "snapshot"
        snapshot.mkdir()
        (snapshot / "z.txt").write_text("z", encoding="utf-8")
        (snapshot / "a.txt").write_text("a", encoding="utf-8")
        stream = b"a.txt\0" + hashlib.sha256(b"a").hexdigest().encode() + b"\n"
        stream += b"z.txt\0" + hashlib.sha256(b"z").hexdigest().encode() + b"\n"
        expected = hashlib.sha256(stream).hexdigest()
        self.assertEqual(run_scenario.source_fingerprint(snapshot), expected)

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

    def test_prompt_contains_situation_but_not_grading_sections(self):
        with tempfile.TemporaryDirectory() as temp:
            snapshot = Path(temp)
            (snapshot / "references/tasks").mkdir(parents=True)
            skill = snapshot / "references/tasks/review-changes.md"
            skill.write_text("skill")
            scenario = snapshot / "scenario.md"
            scenario.write_text(
                "---\nskills: [review-changes]\n---\n\n"
                "## Situation\n\nSituation sentinel.\n\n"
                "## Expected\n\nExpected sentinel.\n\n"
                "## Not acceptable\n\nNot acceptable sentinel.\n"
            )
            skills, situation = run_scenario.scenario_parts(scenario)
            prompt = run_scenario.make_prompt(
                run_scenario.resolve_tasks(snapshot, skills), situation,
            )
            self.assertIn("Situation sentinel.", prompt)
            self.assertNotIn("Expected sentinel.", prompt)
            self.assertNotIn("Not acceptable sentinel.", prompt)

    def test_dry_run_prints_prompt_and_does_not_launch_runner(self):
        marker = self.temp_path / "invoked"
        self.install_fake_runner("codex", """
import os
from pathlib import Path
Path(os.environ['FAKE_MARKER']).write_text('called')
print('fake version')
""")
        env = os.environ.copy()
        env["PATH"] = str(self.bin) + os.pathsep + env.get("PATH", "")
        env["FAKE_MARKER"] = str(marker)
        result = subprocess.run(
            [sys.executable, str(self.runner_script),
             "runner-case", "--runner", "codex",
             "--model", "fake-model", "--dry-run"],
            cwd=self.repo, env=env, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("resolved_skill_paths:", result.stdout)
        self.assertIn("references/tasks/review-changes.md", result.stdout)
        self.assertIn("Situation sentinel.", result.stdout)
        self.assertNotIn("Expected sentinel.", result.stdout)
        self.assertNotIn("Not acceptable", result.stdout)
        self.assertFalse(marker.exists())

    def test_codex_fake_records_provenance_and_scrubbed_environment(self):
        invocation_log = self.temp_path / "invocations.jsonl"
        self.install_fake_runner("codex", """
import json
import os
import sys
from pathlib import Path
if '--version' in sys.argv:
    print('codex fake-1')
else:
    prompt = sys.stdin.read()
    with open(os.environ['FAKE_LOG'], 'a') as log:
        log.write(json.dumps({'prompt': prompt, 'keys': sorted(os.environ)}) + '\\n')
    Path(sys.argv[sys.argv.index('--output-last-message') + 1]).write_text('fake answer')
    print(json.dumps({'type': 'thread.started', 'thread_id': 'fake-session', 'model': 'reported-model'}))
""")
        output = self.temp_path / "run"
        env = os.environ.copy()
        env.update({
            "PATH": str(self.bin) + os.pathsep + env.get("PATH", ""),
            "FAKE_LOG": str(invocation_log),
            "GH_TOKEN": "do-not-log-this-gh-token",
            "GITHUB_TOKEN": "do-not-log-this-github-token",
            "GHFLOW_IDENTITY_LOGIN": "do-not-log-this-login",
            "GIT_AUTHOR_NAME": "do-not-log-this-author",
        })
        result = subprocess.run(
            [sys.executable, str(self.runner_script),
             "runner-case", "--runner", "codex",
             "--model", "fake-model", "--repeat", "2", "--output-dir", str(output)],
            cwd=self.repo, env=env, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        provenance = json.loads((output / "provenance.json").read_text())
        self.assertEqual(provenance["runner_version"], "codex fake-1")
        self.assertEqual(provenance["repeat_count"], 2)
        self.assertEqual(provenance["source_commit"], run_scenario.git(self.repo, "rev-parse", "HEAD"))
        self.assertEqual(len(provenance["source_fingerprint_sha256"]), 64)
        self.assertEqual([run["session_id"] for run in provenance["runs"]],
                         ["fake-session", "fake-session"])
        self.assertEqual([run["exit_code"] for run in provenance["runs"]], [0, 0])
        self.assertEqual(provenance["runs"][0]["runner_model"], "reported-model")
        answer = (output / "answers.txt").read_text()
        self.assertEqual(answer.count("fake answer"), 2)
        self.assertNotIn("Expected sentinel.", answer)
        records = [json.loads(line) for line in invocation_log.read_text().splitlines()]
        self.assertEqual(len(records), 2)
        for record in records:
            self.assertIn("Situation sentinel.", record["prompt"])
            self.assertNotIn("Expected sentinel.", record["prompt"])
            self.assertNotIn("Not acceptable", record["prompt"])
            for key in ("GH_TOKEN", "GITHUB_TOKEN", "GHFLOW_IDENTITY_LOGIN", "GIT_AUTHOR_NAME"):
                self.assertNotIn(key, record["keys"])
        all_output = result.stdout + result.stderr + answer + (output / "provenance.json").read_text()
        for secret in ("do-not-log-this-gh-token", "do-not-log-this-github-token",
                       "do-not-log-this-login", "do-not-log-this-author"):
            self.assertNotIn(secret, all_output)

    def test_claude_fake_extracts_answer_and_session(self):
        self.install_fake_runner("claude", """
import json
import sys
if '--version' in sys.argv:
    print('claude fake-2')
else:
    sys.stdin.read()
    print(json.dumps({'type': 'result', 'session_id': 'claude-session', 'result': 'claude answer'}))
""")
        code, session, model, answer = run_scenario.run_claude(
            "prompt", "fake-model", self.temp_path, {
                "PATH": str(self.bin) + os.pathsep + os.environ.get("PATH", ""),
            },
        )
        self.assertEqual((code, session, answer), (0, "claude-session", "claude answer"))
        self.assertIsNone(model)


if __name__ == "__main__":
    unittest.main()
