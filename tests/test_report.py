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

    def test_reject_shorter_report(self):
        changed = copy.deepcopy(self.candidate)
        removed = changed["cases"].pop()
        changed["total"] -= 1
        changed["passed"] -= int(removed["passed"])
        with self.assertRaisesRegex(ValueError, "Case count differs"):
            compare(self.original, changed)

    def test_reject_inconsistent_score(self):
        self.candidate["passed"] = 999
        with self.assertRaisesRegex(ValueError, "Invalid"):
            compare(self.original, self.candidate)

    def test_reject_equal_but_different_json_types(self):
        for task, expected, replacement in (
            ("clamp", 5, 5.0),
            ("fibonacci", 1, True),
        ):
            with self.subTest(task=task, replacement=repr(replacement)):
                changed = copy.deepcopy(self.candidate)
                case = next(
                    c for c in changed["cases"]
                    if c["task"] == task and type(c["expected"]) is type(expected)
                    and c["expected"] == expected
                )
                self.assertEqual(case["expected"], replacement)
                case["expected"] = replacement
                case["actual"] = replacement
                with self.assertRaisesRegex(ValueError, "differs"):
                    compare(self.original, changed)

    def test_reject_missing_case_identity_from_both_reports(self):
        before = copy.deepcopy(self.original)
        after = copy.deepcopy(self.candidate)
        del before["cases"][0]["expected"]
        del after["cases"][0]["expected"]
        with self.assertRaisesRegex(ValueError, "Invalid"):
            compare(before, after)

    def test_reject_non_mapping_case_with_value_error(self):
        changed = copy.deepcopy(self.candidate)
        changed["cases"][0] = None
        with self.assertRaisesRegex(ValueError, "Invalid"):
            compare(self.original, changed)

    def test_detect_regression(self):
        changed = copy.deepcopy(self.candidate)
        good = next(c for c in changed["cases"] if c["task"] == "is_prime" and c["passed"])
        good["passed"] = False
        good["actual"] = "simulated regression"
        changed["passed"] -= 1
        result = compare(self.original, changed)
        self.assertEqual((result["fixed"], result["regressed"], result["delta"]), (5, 1, 4))

    def test_reject_forged_success_with_corrected_total(self):
        changed = copy.deepcopy(self.original)
        failing = next(case for case in changed["cases"] if not case["passed"])
        self.assertNotEqual(failing["actual"], failing["expected"])
        failing["passed"] = True
        changed["passed"] += 1
        with self.assertRaisesRegex(ValueError, "Invalid"):
            compare(changed, self.candidate)

    def test_reject_forged_failure_with_corrected_total(self):
        changed = copy.deepcopy(self.candidate)
        passing = next(case for case in changed["cases"] if case["passed"])
        passing["passed"] = False
        changed["passed"] -= 1
        with self.assertRaisesRegex(ValueError, "Invalid"):
            compare(self.original, changed)

    def test_reject_success_with_recorded_error(self):
        changed = copy.deepcopy(self.candidate)
        passing = next(case for case in changed["cases"] if case["passed"])
        passing["error"] = "RuntimeError: hidden failure"
        with self.assertRaisesRegex(ValueError, "Invalid"):
            compare(self.original, changed)

    def test_reject_missing_observation_fields(self):
        for field in ("actual", "error"):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.candidate)
                del changed["cases"][0][field]
                with self.assertRaisesRegex(ValueError, "Invalid"):
                    compare(self.original, changed)



if __name__ == "__main__":
    unittest.main()
