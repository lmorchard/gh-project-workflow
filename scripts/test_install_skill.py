"""Behavior checks for source links, conflicts, and portable dependency access."""
import contextlib
import importlib.util
import io
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

installer = load("installer", ROOT / "scripts/install-skill.py")
checker = load("checker", ROOT / "scripts/check.py")

class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source skill"
        self.source.mkdir()
        (self.source / "SKILL.md").write_text("first")
        self.links = [self.root / "claude/ghflow", self.root / "codex/ghflow"]

    def install(self):
        with contextlib.redirect_stdout(io.StringIO()):
            installer.install(self.links, self.source)

    def test_repeat_keeps_links_and_source_edits_are_live(self):
        self.install()
        before = [p.lstat().st_ino for p in self.links]
        self.install()
        self.assertEqual(before, [p.lstat().st_ino for p in self.links])
        (self.source / "SKILL.md").write_text("changed")
        for p in self.links:
            self.assertEqual((p / "SKILL.md").read_text(), "changed")

    def test_conflicts_preflight_all_destinations(self):
        for kind in ("file", "directory", "dangling", "other-source"):
            with self.subTest(kind=kind):
                conflict = self.links[1]
                conflict.parent.mkdir(exist_ok=True)
                if kind == "file": conflict.write_text("keep")
                elif kind == "directory": conflict.mkdir()
                else: conflict.symlink_to(self.root / kind)
                with self.assertRaises(ValueError): self.install()
                self.assertFalse(self.links[0].exists())
                if kind == "file": self.assertEqual(conflict.read_text(), "keep")
                if kind == "directory": conflict.rmdir()
                else: conflict.unlink()

    def test_project_install_and_cli_from_unrelated_cwd(self):
        result = subprocess.run(["python3", str(ROOT / "scripts/install-skill.py"),
                                 "--project", str(self.root), "claude", "codex"],
                                cwd=self.root, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sorted(p.name for p in (self.root / ".agents/skills").iterdir()), ["ghflow"])
        launcher = self.root / ".agents/skills/ghflow/scripts/ghflow.py"
        result = subprocess.run(["python3", str(launcher), "--help"], cwd=self.root,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("verify-commit", result.stdout)
        # Identity config must come from the caller, not the workflow checkout.
        config = self.root / ".ghflow/identity.json"
        config.parent.mkdir()
        config.write_text('{"login":"target-user","name":"Target","email":"target@example.invalid"}')
        result = subprocess.run(["python3", str(launcher), "identity"], cwd=self.root,
                                text=True, capture_output=True)
        self.assertIn('"login": "target-user"', result.stdout)

class StructureTests(unittest.TestCase):
    def test_missing_entry_fails(self):
        with tempfile.TemporaryDirectory() as path:
            self.assertTrue(checker.check_skills(Path(path)))

    def test_extra_registered_task_fails(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            skill = root / "skills/define-issue/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("---\nname: define-issue\ndescription: draft\n---\n")
            self.assertIn("skills: expected only skills/ghflow/SKILL.md", checker.check_skills(root))

    def test_broken_task_link_fails(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            subprocess.run(["git", "init", "--quiet", str(root)], check=True)
            (root / "entry.md").write_text("[task](references/missing.md)")
            self.assertEqual(checker.check_links(root),
                             ["entry.md: broken link references/missing.md"])

    def test_unrouted_reference_fails(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            skill = root / "skills/ghflow/SKILL.md"
            task = skill.parent / "references/tasks/hidden.md"
            task.parent.mkdir(parents=True)
            skill.write_text("---\nname: ghflow\ndescription: draft\n---\n")
            task.write_text("hidden")
            self.assertTrue(any("not reachable" in error for error in checker.check_skills(root)))

if __name__ == "__main__":
    unittest.main()
