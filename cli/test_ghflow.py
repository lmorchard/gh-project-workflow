import io
import json
import os
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from ghflow import GhError, board_set_status, identity_env, main, pr_state, resolve_identity, run_gh, verify_commit

HEAD = "a" * 40
OLD = "b" * 40


def pr(**overrides):
    data = {
        "number": 7,
        "url": "https://github.com/o/r/pull/7",
        "state": "OPEN",
        "isDraft": False,
        "mergeable": "MERGEABLE",
        "headRefOid": HEAD,
        "headRefName": "task",
        "baseRefName": "main",
        "reviewRequests": [],
        "statusCheckRollup": [
            {"__typename": "CheckRun", "name": "test", "status": "COMPLETED", "conclusion": "SUCCESS"},
        ],
    }
    data.update(overrides)
    return data


def rules(*contexts):
    return [{"type": "required_status_checks", "parameters": {"required_status_checks": [{"context": c} for c in contexts]}}]


def fake(pr_data, rules_data=None, reviews=(), comments=(), timeline=(), fail=(), behind_by=0):
    def gh(args):
        if args[0] == "pr":
            if "pr" in fail:
                raise GhError("not found")
            return pr_data
        if "/compare/" in args[1]:
            if "compare" in fail:
                raise GhError("HTTP 404")
            return {"behind_by": behind_by, "ahead_by": 1}
        if "rules" in fail:
            raise GhError("HTTP 403")
        return rules_data if rules_data is not None else rules("test")

    def gh_paginated(path):
        if path.endswith("/reviews"):
            if "reviews" in fail:
                raise GhError("HTTP 502")
            return list(reviews)
        if path.endswith("/comments"):
            return list(comments)
        if "timeline" in fail:
            raise GhError("rate limited")
        return list(timeline)

    return {"gh": gh, "gh_paginated": gh_paginated}


def review(rid, author, commit, submitted, state="COMMENTED", body=""):
    return {"id": rid, "user": {"login": author}, "state": state, "commit_id": commit, "submitted_at": submitted, "body": body}


def requested(reviewer, at, event="review_requested"):
    return {"event": event, "requested_reviewer": {"login": reviewer}, "created_at": at, "actor": {"login": "les"}}


class CiTests(unittest.TestCase):
    def test_green_when_required_checks_pass(self):
        result, status = pr_state("o/r", 7, **fake(pr()))
        self.assertEqual(result["ci"], "green")
        self.assertEqual(status, 0)

    def test_required_check_without_result_is_missing(self):
        result, _ = pr_state("o/r", 7, **fake(pr(), rules_data=rules("test", "typecheck")))
        self.assertEqual(result["ci"], "missing")
        self.assertIn({"name": "typecheck", "state": "missing", "required": True}, result["checks"])

    def test_skipped_optional_check_stays_green(self):
        rollup = [
            {"__typename": "CheckRun", "name": "test", "status": "COMPLETED", "conclusion": "SUCCESS"},
            {"__typename": "CheckRun", "name": "preview", "status": "COMPLETED", "conclusion": "SKIPPED"},
        ]
        result, _ = pr_state("o/r", 7, **fake(pr(statusCheckRollup=rollup)))
        self.assertEqual(result["ci"], "green")

    def test_running_check_is_pending(self):
        rollup = [{"__typename": "CheckRun", "name": "test", "status": "IN_PROGRESS", "conclusion": None}]
        result, _ = pr_state("o/r", 7, **fake(pr(statusCheckRollup=rollup)))
        self.assertEqual(result["ci"], "pending")

    def test_failure_outranks_pending(self):
        rollup = [
            {"__typename": "CheckRun", "name": "test", "status": "IN_PROGRESS", "conclusion": None},
            {"__typename": "StatusContext", "context": "lint", "state": "FAILURE"},
        ]
        result, _ = pr_state("o/r", 7, **fake(pr(statusCheckRollup=rollup), rules_data=[]))
        self.assertEqual(result["ci"], "failing")

    def test_no_checks_is_none_not_green(self):
        result, _ = pr_state("o/r", 7, **fake(pr(statusCheckRollup=[]), rules_data=[]))
        self.assertEqual(result["ci"], "none")

    def test_head_current_with_base(self):
        result, _ = pr_state("o/r", 7, **fake(pr()))
        self.assertEqual(result["base_behind_by"], 0)

    def test_head_behind_base_is_reported(self):
        result, status = pr_state("o/r", 7, **fake(pr(), behind_by=2))
        self.assertEqual(result["base_behind_by"], 2)
        self.assertEqual(result["ci"], "green")
        self.assertEqual(status, 0)

    def test_unreadable_compare_leaves_behind_unknown(self):
        result, status = pr_state("o/r", 7, **fake(pr(), fail={"compare"}))
        self.assertIsNone(result["base_behind_by"])
        self.assertEqual(status, 2)

    def test_unreadable_rules_leave_required_unknown(self):
        result, status = pr_state("o/r", 7, **fake(pr(), fail={"rules"}))
        self.assertIsNone(result["required_checks"])
        self.assertIsNone(result["checks"][0]["required"])
        self.assertEqual(status, 2)


class ReviewTests(unittest.TestCase):
    def test_copilot_request_matches_bot_review_after_it(self):
        data = fake(
            pr(),
            reviews=[review(1, "copilot-pull-request-reviewer[bot]", HEAD, "2026-10-02T03:45:00Z")],
            timeline=[requested("Copilot", "2026-10-02T03:41:00Z")],
        )
        result, _ = pr_state("o/r", 7, **data)
        self.assertEqual(result["latest_review_requests"], [{"reviewer": "Copilot", "requested_at": "2026-10-02T03:41:00Z", "answered": True}])
        self.assertTrue(result["reviews"][0]["covers_head"])

    def test_review_before_latest_request_does_not_answer_it(self):
        data = fake(
            pr(reviewRequests=[{"login": "Copilot"}]),
            reviews=[review(1, "copilot-pull-request-reviewer[bot]", OLD, "2026-10-02T03:00:00Z")],
            timeline=[requested("Copilot", "2026-10-02T02:50:00Z"), requested("Copilot", "2026-10-02T03:30:00Z")],
        )
        result, _ = pr_state("o/r", 7, **data)
        self.assertFalse(result["latest_review_requests"][0]["answered"])
        self.assertFalse(result["reviews"][0]["covers_head"])
        self.assertEqual(result["pending_review_requests"], ["Copilot"])

    def test_removed_request_is_not_latest(self):
        data = fake(pr(), timeline=[requested("alice", "2026-10-02T01:00:00Z"), requested("alice", "2026-10-02T01:05:00Z", "review_request_removed")])
        result, _ = pr_state("o/r", 7, **data)
        self.assertEqual(result["latest_review_requests"], [])

    def test_inline_comments_count_per_review(self):
        data = fake(
            pr(),
            reviews=[review(1, "bot", HEAD, "t1"), review(2, "les", HEAD, "t2")],
            comments=[{"pull_request_review_id": 1}, {"pull_request_review_id": 1}],
        )
        result, _ = pr_state("o/r", 7, **data)
        self.assertEqual([r["inline_comments"] for r in result["reviews"]], [2, 0])

    def test_failed_review_read_is_null_not_empty(self):
        result, status = pr_state("o/r", 7, **fake(pr(), timeline=[requested("Copilot", "t")], fail={"reviews"}))
        self.assertIsNone(result["reviews"])
        self.assertIsNone(result["latest_review_requests"][0]["answered"])
        self.assertEqual(result["errors"][0]["part"], "reviews")
        self.assertEqual(status, 2)

    def test_failed_timeline_read_is_null(self):
        result, status = pr_state("o/r", 7, **fake(pr(), fail={"timeline"}))
        self.assertIsNone(result["review_request_events"])
        self.assertIsNone(result["latest_review_requests"])
        self.assertEqual(status, 2)


class PrTests(unittest.TestCase):
    def test_unreadable_pr_exits_1(self):
        result, status = pr_state("o/r", 7, **fake(pr(), fail={"pr"}))
        self.assertEqual(status, 1)
        self.assertEqual(result["errors"][0]["part"], "pr")


def commit_fake(message="Fix the thing\n\nDetails.", compare="behind", head=HEAD, fail=()):
    def gh(args):
        path = args[1] if args[0] == "api" else None
        if args[0] == "pr":
            if "pr" in fail:
                raise GhError("not found")
            return {"headRefOid": head}
        if "/compare/" in path:
            if "compare" in fail:
                raise GhError("HTTP 404")
            return {"status": compare}
        if "commit" in fail:
            raise GhError("No commit found for SHA: abc (HTTP 422)")
        return {"sha": HEAD, "commit": {"message": message, "author": {"date": "2026-10-02T12:00:00Z"}}, "parents": [{"sha": OLD}]}

    return {"gh": gh}


class VerifyCommitTests(unittest.TestCase):
    def test_resolves_prefix_to_full_commit(self):
        result, status = verify_commit("o/r", "aaaaaaa", **commit_fake())
        self.assertEqual((result["sha"], result["subject"], result["parents"]), (HEAD, "Fix the thing", [OLD]))
        self.assertEqual(result["expectations"], {})
        self.assertEqual(status, 0)

    def test_all_expectations_hold(self):
        result, status = verify_commit("o/r", "aaaaaaa", subject="Fix the thing", on="main", pr_head=("o/r", 7), **commit_fake())
        self.assertEqual(result["expectations"], {"subject_matches": True, "on_branch": True, "is_pr_head": True})
        self.assertEqual(status, 0)

    def test_wrong_subject_exits_3(self):
        result, status = verify_commit("o/r", "aaaaaaa", subject="Something else", **commit_fake())
        self.assertFalse(result["expectations"]["subject_matches"])
        self.assertEqual(status, 3)

    def test_commit_not_in_branch_history(self):
        for compare in ("ahead", "diverged"):
            result, status = verify_commit("o/r", "aaaaaaa", on="main", **commit_fake(compare=compare))
            self.assertFalse(result["expectations"]["on_branch"])
            self.assertEqual(status, 3)

    def test_identical_to_branch_is_on_it(self):
        result, _ = verify_commit("o/r", "aaaaaaa", on="main", **commit_fake(compare="identical"))
        self.assertTrue(result["expectations"]["on_branch"])

    def test_pr_head_moved(self):
        result, status = verify_commit("o/r", "aaaaaaa", pr_head=("o/r", 7), **commit_fake(head=OLD))
        self.assertEqual(result["pr_head"], OLD)
        self.assertFalse(result["expectations"]["is_pr_head"])
        self.assertEqual(status, 3)

    def test_failed_expectation_read_is_null(self):
        result, status = verify_commit("o/r", "aaaaaaa", on="main", **commit_fake(fail={"compare"}))
        self.assertIsNone(result["expectations"]["on_branch"])
        self.assertEqual(result["errors"][0]["part"], "on_branch")
        self.assertEqual(status, 2)

    def test_false_expectation_outranks_read_error(self):
        _, status = verify_commit("o/r", "aaaaaaa", subject="Other", on="main", **commit_fake(fail={"compare"}))
        self.assertEqual(status, 3)

    def test_missing_commit_exits_1_with_prefix_note(self):
        result, status = verify_commit("o/r", "abc", **commit_fake(fail={"commit"}))
        self.assertEqual(status, 1)
        self.assertNotIn("sha", result)
        self.assertIn("full SHA", result["note"])


BOARD_OPTIONS = ["Backlog", "Ready", "In progress", "In review", "Done"]


class FakeBoard:
    """A board with one Status field. `status` is None when the issue is not on the board."""

    def __init__(self, status=None, on_board=True, fail=(), sticky=True):
        self.status = status
        self.on_board = on_board
        self.fail = set(fail)
        self.sticky = sticky
        self.writes = []

    def __call__(self, args):
        if args[:2] == ["project", "view"]:
            return {"id": "P1"}
        if args[:2] == ["project", "field-list"]:
            options = [{"id": f"opt-{i}", "name": name} for i, name in enumerate(BOARD_OPTIONS)]
            return {"fields": [{"id": "F0", "name": "Title"}, {"id": "F1", "name": "Status", "options": options}]}
        if args[:2] == ["project", "item-add"]:
            self.writes.append("add")
            self.on_board = True
            return {"id": "ITEM"}
        if args[:2] == ["project", "item-edit"]:
            if "write" in self.fail:
                raise GhError("HTTP 403")
            option = args[args.index("--single-select-option-id") + 1]
            self.writes.append(option)
            if self.sticky:
                self.status = BOARD_OPTIONS[int(option.split("-")[1])]
            return {}
        if self.writes and "readback" in self.fail:
            raise GhError("HTTP 502")
        nodes = [{"id": "OTHER", "project": {"id": "P9"}, "fieldValueByName": {"name": "Done"}}]
        if self.on_board:
            value = {"name": self.status} if self.status else {}
            nodes.append({"id": "ITEM", "project": {"id": "P1"}, "fieldValueByName": value})
        return {"data": {"repository": {"issue": {"url": "https://github.com/o/r/issues/5", "projectItems": {"nodes": nodes}}}}}


def set_status(board, status, **kwargs):
    return board_set_status("o/r", 5, "o", 6, status, gh=board, **kwargs)


class BoardSetStatusTests(unittest.TestCase):
    def test_forward_move_sets_and_reads_back(self):
        board = FakeBoard("In progress")
        result, status = set_status(board, "In review")
        self.assertEqual((result["before"], result["action"], result["after"]), ("In progress", "set", "In review"))
        self.assertTrue(result["readback_matches"])
        self.assertEqual(board.writes, ["opt-3"])
        self.assertEqual(status, 0)

    def test_option_name_matched_case_insensitively(self):
        result, _ = set_status(FakeBoard("Backlog"), "in progress")
        self.assertEqual(result["target"], "In progress")

    def test_unknown_option_exits_1_with_options(self):
        board = FakeBoard("Backlog")
        result, status = set_status(board, "Doing")
        self.assertEqual(status, 1)
        self.assertEqual(result["options"], BOARD_OPTIONS)
        self.assertEqual(board.writes, [])

    def test_same_status_is_unchanged_without_write(self):
        board = FakeBoard("In review")
        result, status = set_status(board, "In review")
        self.assertEqual(result["action"], "unchanged")
        self.assertEqual(board.writes, [])
        self.assertEqual(status, 0)

    def test_backward_move_refused(self):
        board = FakeBoard("Done")
        result, status = set_status(board, "In review")
        self.assertEqual((result["action"], result["after"]), ("refused", "Done"))
        self.assertEqual(board.writes, [])
        self.assertEqual(status, 3)

    def test_backward_move_allowed_with_flag(self):
        result, status = set_status(FakeBoard("Done"), "In review", allow_backward=True)
        self.assertEqual((result["action"], result["after"], status), ("set", "In review", 0))

    def test_issue_without_status_moves_forward(self):
        result, status = set_status(FakeBoard(None), "Backlog")
        self.assertEqual((result["before"], result["after"], status), (None, "Backlog", 0))

    def test_issue_not_on_board_is_added(self):
        board = FakeBoard(on_board=False)
        result, status = set_status(board, "In progress")
        self.assertTrue(result["added"])
        self.assertEqual(board.writes, ["add", "opt-2"])
        self.assertEqual((result["after"], status), ("In progress", 0))

    def test_failed_write_exits_1(self):
        result, status = set_status(FakeBoard("Backlog", fail={"write"}), "In progress")
        self.assertEqual(result["errors"][0]["part"], "write")
        self.assertEqual(status, 1)

    def test_write_that_does_not_stick_exits_2(self):
        result, status = set_status(FakeBoard("Backlog", sticky=False), "In progress")
        self.assertEqual(result["after"], "Backlog")
        self.assertFalse(result["readback_matches"])
        self.assertEqual(status, 2)

    def test_failed_readback_exits_2(self):
        result, status = set_status(FakeBoard("Backlog", fail={"readback"}), "In progress")
        self.assertIsNone(result["after"])
        self.assertEqual(result["errors"][0]["part"], "readback")
        self.assertEqual(status, 2)


class IdentityTests(unittest.TestCase):
    def test_identity_unconfigured_when_no_env_and_no_config(self):
        ident = resolve_identity(env={}, config_paths=[])
        self.assertFalse(ident["configured"])
        self.assertIsNone(ident["login"])
        self.assertIsNone(ident["token_file"])

    def test_identity_from_config_file(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
            json.dump({"login": "BotUser", "email": "bot@example.com"}, f)
            cfg_path = f.name
        try:
            ident = resolve_identity(env={}, config_paths=[cfg_path])
            self.assertTrue(ident["configured"])
            self.assertEqual(ident["login"], "BotUser")
            self.assertEqual(ident["name"], "BotUser")
            self.assertEqual(ident["email"], "bot@example.com")
        finally:
            os.unlink(cfg_path)

    def test_identity_env_overrides_config(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
            json.dump({"login": "BotUser", "email": "bot@example.com"}, f)
            cfg_path = f.name
        try:
            env = {"GHFLOW_IDENTITY_LOGIN": "EnvBot", "GHFLOW_IDENTITY_EMAIL": "env@example.com"}
            ident = resolve_identity(env=env, config_paths=[cfg_path])
            self.assertEqual(ident["login"], "EnvBot")
            self.assertEqual(ident["email"], "env@example.com")
        finally:
            os.unlink(cfg_path)

    def test_identity_env_sets_variables(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
            f.write("secret-token\n")
            token_path = f.name
        try:
            ident = {
                "login": "BotUser",
                "name": "Bot User",
                "email": "bot@example.com",
                "token_file": token_path,
            }
            env = identity_env(ident, base_env={})
            self.assertEqual(env["GH_TOKEN"], "secret-token")
            self.assertEqual(env["GIT_AUTHOR_NAME"], "Bot User")
            self.assertEqual(env["GIT_COMMITTER_NAME"], "Bot User")
            self.assertEqual(env["GIT_AUTHOR_EMAIL"], "bot@example.com")
            self.assertEqual(env["GIT_COMMITTER_EMAIL"], "bot@example.com")
            self.assertIn("GIT_CONFIG_PARAMETERS", env)
        finally:
            os.unlink(token_path)

    def test_identity_command_export(self):
        ident = {
            "login": "BotUser",
            "name": "Bot User",
            "email": "bot@example.com",
            "token_file": None,
            "configured": True,
        }
        with patch("ghflow.resolve_identity", return_value=ident):
            stdout = io.StringIO()
            with patch("sys.stdout", stdout):
                status = main(["identity", "--export"])
            self.assertEqual(status, 0)
            out = stdout.getvalue()
            self.assertIn('export GIT_AUTHOR_NAME="Bot User"', out)
            self.assertIn('export GIT_AUTHOR_EMAIL="bot@example.com"', out)

    def test_run_gh_uses_configured_identity(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
            f.write("bot-token\n")
            token_path = f.name
        try:
            ident = {"login": "BotUser", "name": "BotUser", "email": None, "token_file": token_path}
            completed = subprocess.CompletedProcess([], 0, stdout='{"ok": true}', stderr="")
            with patch("ghflow.resolve_identity", return_value=ident), \
                    patch.dict(os.environ, {}, clear=True), \
                    patch("ghflow.subprocess.run", return_value=completed) as run:
                self.assertEqual(run_gh(["api", "user"]), {"ok": True})
            self.assertEqual(run.call_args.kwargs["env"]["GH_TOKEN"], "bot-token")
        finally:
            os.unlink(token_path)


if __name__ == "__main__":
    unittest.main()
