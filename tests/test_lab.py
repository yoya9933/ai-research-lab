import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
import json

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

    def test_candidate_cannot_mutate_input_case_data(self):
        def destructive_unique(values):
            values.clear()
            return []
        overrides = {name: getattr(solutions, name) for name in CASES}
        overrides["unique"] = destructive_unique
        report = evaluate(SimpleNamespace(**overrides))
        self.assertEqual(CASES["unique"][0][0][0], [3, 1, 3, 2])
        self.assertLess(report["passed"], report["total"])
        self.assertEqual(evaluate(solutions)["passed"], report["total"])

    def test_failure_exit_code_and_report_are_consistent(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "results.json"
            run = subprocess.run(
                [sys.executable, "-m", "lab", "evaluate", "--module", "lab.buggy",
                 "--output", str(output), "--require-all-pass"],
                capture_output=True, text=True, check=False
            )
            self.assertEqual(run.returncode, 1, run.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertLess(report["passed"], report["total"])
            self.assertIn(f"{report['passed']}/{report['total']}", run.stdout)

    def test_reference_succeeds_when_all_pass_required(self):
        run = subprocess.run(
            [sys.executable, "-m", "lab", "evaluate", "--module",
             "lab.solutions", "--require-all-pass"],
            capture_output=True, text=True, check=False
        )
        self.assertEqual(run.returncode, 0, run.stderr)


if __name__ == "__main__":
    unittest.main()
