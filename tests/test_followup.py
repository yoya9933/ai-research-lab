"""Post-commit cases; the frozen candidate is not adjusted after these checks."""

import unittest
from lab import attempt_001, buggy, solutions
from lab.__main__ import evaluate
from lab.cases import FOLLOWUP_CASES


class FollowupTests(unittest.TestCase):
    def test_covers_all_tasks(self):
        self.assertEqual(len(FOLLOWUP_CASES), 10)
        self.assertTrue(all(len(samples) == 2 for samples in FOLLOWUP_CASES.values()))

    def test_reference_passes(self):
        report = evaluate(solutions, FOLLOWUP_CASES)
        self.assertEqual((report["passed"], report["total"]), (20, 20))

    def test_frozen_candidate_improves_on_followup(self):
        baseline = evaluate(buggy, FOLLOWUP_CASES)
        attempt = evaluate(attempt_001, FOLLOWUP_CASES)
        self.assertEqual((baseline["passed"], baseline["total"]), (8, 20))
        self.assertEqual((attempt["passed"], attempt["total"]), (11, 20))


if __name__ == "__main__":
    unittest.main()
