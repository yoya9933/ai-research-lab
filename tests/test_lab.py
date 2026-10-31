import unittest

from lab import buggy, solutions
from lab.__main__ import evaluate
from lab.cases import CASES


class EvaluatorTests(unittest.TestCase):
    def test_ten_tasks_exist(self):
        self.assertEqual(len(CASES), 10)

    def test_answer_key_passes_all_cases(self):
        report = evaluate(solutions)
        self.assertEqual(report["passed"], report["total"])

    def test_buggy_baseline_fails_at_least_one_case_per_task(self):
        report = evaluate(buggy)
        failing = {case["task"] for case in report["cases"] if not case["passed"]}
        self.assertEqual(failing, set(CASES))

    def test_missing_function_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing callable"):
            evaluate(object())

    def test_results_include_expected_and_actual(self):
        item = evaluate(buggy)["cases"][0]
        self.assertTrue({"task", "args", "expected", "actual", "passed", "error"} <= item.keys())


if __name__ == "__main__":
    unittest.main()
