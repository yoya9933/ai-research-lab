"""Reproducible grading for the first chat-authored repair demonstration."""

import unittest

from lab import attempt_001, buggy
from lab.__main__ import evaluate


class FirstRepairTests(unittest.TestCase):
    def test_report_shows_real_partial_improvement(self):
        baseline = evaluate(buggy)
        attempt = evaluate(attempt_001)
        self.assertEqual((baseline["passed"], baseline["total"]), (11, 24))
        self.assertEqual((attempt["passed"], attempt["total"]), (16, 24))

    def test_three_chosen_tasks_pass_every_published_case(self):
        selected = {"clamp", "chunks", "factorial"}
        report = evaluate(attempt_001)
        self.assertTrue(
            all(case["passed"] for case in report["cases"] if case["task"] in selected)
        )

    def test_unselected_tasks_are_unchanged(self):
        selected = {"clamp", "chunks", "factorial"}
        before = evaluate(buggy)
        after = evaluate(attempt_001)
        self.assertEqual(
            [(c["task"], c["passed"]) for c in before["cases"] if c["task"] not in selected],
            [(c["task"], c["passed"]) for c in after["cases"] if c["task"] not in selected]
        )


if __name__ == "__main__":
    unittest.main()
