"""Safety checks for deleting branches with evidence from a fake gh command."""
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts/delete-merged-branches.sh"
REPO = "o/r"
MAIN = "a" * 40
MERGED = "b" * 40
CHANGED = "c" * 40


def branch(name, sha):
    return {"name": name, "commit": {"sha": sha}}


def pull(number, ref, sha, repo=REPO, merged=True):
    return {
        "number": number,
        "state": "closed" if merged else "open",
        "merged_at": "2026-01-01T00:00:00Z" if merged else None,
        "head": {
            "ref": ref,
            "sha": sha,
            "repo": {"full_name": repo} if repo else None,
        },
    }


class DeleteMergedBranchesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.state = self.root / "state.json"
        self.calls = self.root / "calls.jsonl"
        self.config = {
            "repo": {"full_name": REPO, "default_branch": "main"},
            "branches": [[branch("main", MAIN), branch("feature", MERGED)]],
            "pulls": [[pull(12, "feature", MERGED)]],
            "branch_reads": {},
            "branch_reads_response": {},
            "fresh_open_pulls": None,
            "fail": None,
            "malformed": None,
            "delete_fail": False,
        }
        self.write_config()
        fake = self.bin / "gh"
        fake.write_text("""#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
state_path = Path(os.environ['FAKE_GH_STATE'])
state = json.loads(state_path.read_text())
calls_path = Path(os.environ['FAKE_GH_CALLS'])
with calls_path.open('a') as f:
    f.write(json.dumps(args) + '\\n')
endpoint = next((arg for arg in args if arg.startswith('repos/')), '')
kind = ('delete' if '-X' in args and 'DELETE' in args else
        'branch' if '/branches/' in endpoint else
        'branches' if endpoint.endswith('/branches?per_page=100') else
        'open_pulls' if endpoint.endswith('/pulls?state=open&per_page=100') else
        'pulls' if endpoint.endswith('/pulls?state=all&per_page=100') else
        'repo' if endpoint == 'repos/o/r' else 'unknown')
if state['fail'] == kind:
    print('simulated ' + kind + ' read failure', file=sys.stderr)
    sys.exit(1)
if kind == 'delete' and state['delete_fail']:
    print('simulated DELETE failure', file=sys.stderr)
    sys.exit(1)
if state['malformed'] == kind:
    print('{not json')
    sys.exit(0)
if kind == 'repo': value = state['repo']
elif kind == 'branches': value = state['branches']
elif kind == 'pulls': value = state['pulls']
elif kind == 'open_pulls':
    value = state['fresh_open_pulls']
    if value is None:
        value = [[pull for pull in page if pull.get('state') == 'open']
                 for page in state['pulls']]
elif kind == 'branch':
    name = endpoint.split('/branches/', 1)[1]
    count = state['branch_reads'].get(name, 0)
    state['branch_reads'][name] = count + 1
    state_path.write_text(json.dumps(state))
    value = state['branch_reads_response'].get(name, state['branches'][0][1])
    if name == 'feature' and state.get('changed_tip') and count == 0:
        value = {'name': name, 'commit': {'sha': state['changed_tip']}}
elif kind == 'delete': value = {}
else:
    print('unexpected gh arguments: ' + repr(args), file=sys.stderr)
    sys.exit(2)
print(json.dumps(value))
""")
        fake.chmod(0o755)

    def write_config(self):
        self.state.write_text(json.dumps(self.config))

    def invoke(self, *args):
        env = os.environ.copy()
        env["PATH"] = str(self.bin) + os.pathsep + env["PATH"]
        env["FAKE_GH_STATE"] = str(self.state)
        env["FAKE_GH_CALLS"] = str(self.calls)
        return subprocess.run([str(SCRIPT), REPO, *args], cwd=ROOT, env=env,
                              text=True, capture_output=True)

    def calls_made(self):
        if not self.calls.exists():
            return []
        return [json.loads(line) for line in self.calls.read_text().splitlines()]

    def deletes(self):
        return [args for args in self.calls_made() if "DELETE" in args]

    def test_dry_run_rechecks_tip_and_never_deletes(self):
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("would delete feature", result.stdout)
        self.assertTrue(any("/branches/feature" in arg for args in self.calls_made() for arg in args))
        self.assertEqual(self.deletes(), [])

    def test_yes_deletes_only_after_final_tip_matches_merged_head(self):
        result = self.invoke("--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("deleted feature", result.stdout)
        self.assertEqual(len(self.deletes()), 1)
        calls = self.calls_made()
        tip_read = next(i for i, args in enumerate(calls)
                        if any("/branches/feature" in arg for arg in args))
        delete = next(i for i, args in enumerate(calls) if "DELETE" in args)
        self.assertEqual(tip_read, delete - 1)

    def test_changed_tip_is_skipped(self):
        self.config["changed_tip"] = CHANGED
        self.write_config()
        result = self.invoke("--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("tip changed", result.stdout)
        self.assertEqual(self.deletes(), [])

    def test_open_pr_on_later_page_blocks_deletion(self):
        self.config["pulls"] = [
            [pull(12, "feature", MERGED)],
            [pull(99, "feature", MERGED, merged=False)],
        ]
        self.write_config()
        result = self.invoke("--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.deletes(), [])
        open_call = next(args for args in self.calls_made()
                         if any("/pulls?state=open" in arg for arg in args))
        self.assertIn("--paginate", open_call)
        self.assertIn("--slurp", open_call)

        self.calls.unlink(missing_ok=True)
        self.config["pulls"][1] = []
        self.write_config()
        result = self.invoke("--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(self.deletes()), 1)

    def test_open_pr_added_after_merged_inventory_blocks_deletion(self):
        self.config["pulls"] = [[pull(12, "feature", MERGED)]]
        self.config["fresh_open_pulls"] = [[pull(99, "feature", "d" * 40, merged=False)]]
        self.write_config()
        result = self.invoke("--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.deletes(), [])

    def test_open_pr_from_another_source_repository_does_not_match(self):
        self.config["pulls"] = [
            [pull(12, "feature", MERGED),
             pull(13, "feature", "d" * 40, repo="fork/r", merged=False)],
        ]
        self.write_config()
        result = self.invoke("--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(self.deletes()), 1)

    def test_merged_pr_from_another_source_repository_is_not_proof(self):
        self.config["pulls"] = [[pull(12, "feature", MERGED, repo="fork/r")]]
        self.write_config()
        result = self.invoke("--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.deletes(), [])

    def test_api_read_error_fails_closed(self):
        for kind in ("repo", "branches", "pulls", "open_pulls"):
            with self.subTest(kind=kind):
                self.config["fail"] = kind
                self.write_config()
                result = self.invoke("--yes")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("simulated", result.stderr)
                self.assertEqual(self.deletes(), [])
                self.calls.unlink(missing_ok=True)
        self.config["fail"] = None

    def test_malformed_inventory_fails_closed(self):
        for kind in ("repo", "branches", "pulls", "open_pulls"):
            with self.subTest(kind=kind):
                self.config["malformed"] = kind
                self.write_config()
                result = self.invoke("--yes")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.deletes(), [])
                self.calls.unlink(missing_ok=True)
        self.config["malformed"] = None

    def test_invalid_branch_or_pr_fields_fail_closed(self):
        self.config["branches"] = [[branch("feature", "not-a-commit")]]
        self.write_config()
        result = self.invoke("--yes")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.deletes(), [])
        self.calls.unlink(missing_ok=True)

        self.config["branches"] = [[branch("main", MAIN), branch("feature", MERGED)]]
        self.config["pulls"] = [[{"number": 12}]]
        self.write_config()
        result = self.invoke("--yes")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.deletes(), [])

    def test_final_tip_read_error_or_malformed_data_fails_closed(self):
        for field, value in (("fail", "branch"), ("malformed", "branch")):
            with self.subTest(field=field):
                self.config[field] = value
                self.write_config()
                result = self.invoke("--yes")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("failed to verify feature", result.stderr)
                self.assertEqual(self.deletes(), [])
                self.calls.unlink(missing_ok=True)
        self.config["fail"] = None
        self.config["malformed"] = None

    def test_default_branch_is_never_deleted(self):
        self.config["repo"]["default_branch"] = "feature"
        self.config["branches"] = [[branch("feature", MERGED)]]
        self.config["pulls"] = [[pull(12, "feature", MERGED)]]
        self.write_config()
        result = self.invoke("--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.deletes(), [])

    def test_failed_delete_is_reported_and_returns_failure(self):
        self.config["delete_fail"] = True
        self.write_config()
        result = self.invoke("--yes")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("failed to delete feature", result.stderr)


if __name__ == "__main__":
    unittest.main()
