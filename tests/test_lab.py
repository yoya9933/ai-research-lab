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
from lab.report import compare


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

    def test_nested_boolean_is_not_integer_in_evaluator(self):
        sample = {"normalize": [(([0, 0],), [0, 0])]}
        module = SimpleNamespace(normalize=lambda values: [False, False])
        report = evaluate(module, sample)
        self.assertEqual((report["passed"], report["total"]), (0, 1))
        self.assertFalse(report["cases"][0]["passed"])

    def test_dictionary_key_type_is_not_coerced(self):
        sample = {"nested": [((), {0: "value"})]}
        module = SimpleNamespace(nested=lambda: {False: "value"})
        report = evaluate(module, sample)
        self.assertEqual((report["passed"], report["total"]), (0, 1))

    def test_tuple_mismatch_remains_failure_after_json_serialization(self):
        sample = {"unique": [(([],), [])]}
        module = SimpleNamespace(unique=lambda values: ())
        report = evaluate(module, sample)
        report["suite"] = "synthetic"
        serialized = json.loads(json.dumps(report))
        self.assertEqual((serialized["passed"], serialized["total"]), (0, 1))
        self.assertIn("Non-JSON-stable output: tuple", serialized["cases"][0]["error"])
        self.assertEqual(compare(serialized, serialized)["baseline"], 0)

    def test_missing_function_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing callable"):
            evaluate(object())

    def test_results_include_expected_and_actual(self):
        item = evaluate(buggy)["cases"][0]
        self.assertTrue({"task", "args", "expected", "actual", "passed", "error"} <= item.keys())

    def test_candidate_reusing_mutable_output_cannot_rewrite_prior_result(self):
        shared = {"value": None}

        def reuse(value):
            shared["value"] = value
            return shared

        samples = {"reuse": [
            ((1,), {"value": 1}),
            ((2,), {"value": 2}),
        ]}
        report = evaluate(SimpleNamespace(reuse=reuse), samples)
        self.assertEqual((report["passed"], report["total"]), (2, 2))
        self.assertEqual(
            [case["actual"] for case in report["cases"]],
            [{"value": 1}, {"value": 2}],
        )
        self.assertIsNot(report["cases"][0]["actual"], shared)
        self.assertIsNot(report["cases"][1]["actual"], shared)
        report["suite"] = "mutable-result-snapshot"
        self.assertEqual(compare(report, report)["baseline"], 2)

    def test_candidate_cannot_rewrite_expected_answer_in_current_score(self):
        expected = {"value": 0}
        samples = {"rewrite": [((), expected)]}

        def rewrite():
            # A trusted module can still hold an external reference to
            # the oracle; grading must use its pre-call snapshot.
            expected["value"] = 42
            return {"value": 42}

        report = evaluate(SimpleNamespace(rewrite=rewrite), samples)
        self.assertEqual((report["passed"], report["total"]), (0, 1))
        case = report["cases"][0]
        self.assertEqual(case["expected"], {"value": 0})
        self.assertEqual(case["actual"], {"value": 42})
        self.assertFalse(case["passed"])

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
