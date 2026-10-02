import unittest

from ghflow import GhError, pr_state

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


def fake(pr_data, rules_data=None, reviews=(), comments=(), timeline=(), fail=()):
    def gh(args):
        if args[0] == "pr":
            if "pr" in fail:
                raise GhError("not found")
            return pr_data
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


if __name__ == "__main__":
    unittest.main()
