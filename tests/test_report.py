"""Report comparisons must not hide regressions or mix incompatible data."""

import copy
import unittest

from lab import attempt_001, buggy
from lab.__main__ import evaluate
from lab.cases import FOLLOWUP_CASES
from lab.report import compare


class CompareTests(unittest.TestCase):
    def setUp(self):
        self.original = evaluate(buggy)
        self.candidate = evaluate(attempt_001)
        self.original["suite"] = "published"
        self.candidate["suite"] = "published"

    def test_real_published_outcomes(self):
        result = compare(self.original, self.candidate)
        self.assertEqual((result["baseline"], result["candidate"]), (11, 16))
        self.assertEqual((result["fixed"], result["regressed"], result["delta"]), (5, 0, 5))

    def test_real_followup_outcomes(self):
        before = evaluate(buggy, FOLLOWUP_CASES)
        after = evaluate(attempt_001, FOLLOWUP_CASES)
        before["suite"] = after["suite"] = "followup"
        result = compare(before, after)
        self.assertEqual((result["baseline"], result["candidate"], result["delta"]), (8, 11, 3))

    def test_reject_different_suites(self):
        self.candidate["suite"] = "followup"
        with self.assertRaisesRegex(ValueError, "different"):
            compare(self.original, self.candidate)

    def test_reject_different_case_data(self):
        changed = copy.deepcopy(self.candidate)
        changed["cases"][0]["args"] = [999, 0, 0]
        with self.assertRaisesRegex(ValueError, "differs"):
            compare(self.original, changed)

    def test_reject_inconsistent_score(self):
        self.candidate["passed"] = 999
        with self.assertRaisesRegex(ValueError, "Invalid"):
            compare(self.original, self.candidate)

    def test_detect_regression(self):
        changed = copy.deepcopy(self.candidate)
        good = next(c for c in changed["cases"] if c["task"] == "is_prime" and c["passed"])
        good["passed"] = False
        changed["passed"] -= 1
        result = compare(self.original, changed)
        self.assertEqual((result["fixed"], result["regressed"], result["delta"]), (5, 1, 4))


if __name__ == "__main__":
    unittest.main()
