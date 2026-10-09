import contextlib
import io
import unittest
from pathlib import Path

from tasks import list_tasks, main


class TaskTests(unittest.TestCase):
    def setUp(self):
        self.tasks = [
            {"id": 1, "title": "Open", "owner": "Ana", "completed": False},
            {"id": 2, "title": "Closed", "owner": "Bo", "completed": True},
            {"id": 3, "title": "Another", "owner": "Bo", "completed": False},
        ]

    def test_default_list_only_includes_open_tasks(self):
        self.assertEqual([t["id"] for t in list_tasks(self.tasks)], [1, 3])

    def test_owner_filter(self):
        self.assertEqual([t["id"] for t in list_tasks(self.tasks, owner="Bo")], [3])

    def test_helper_can_include_completed_tasks(self):
        self.assertEqual([t["id"] for t in list_tasks(self.tasks, include_completed=True)], [1, 2, 3])

    def test_public_list_command(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            main(["list", "--data", str(Path(__file__).with_name("sample.json"))])
        self.assertEqual(output.getvalue(), "1: Open\n3: Another\n")


if __name__ == "__main__":
    unittest.main()
