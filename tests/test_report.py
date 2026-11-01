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

    def test_changes_name_exact_fixes_and_keep_both_outcomes(self):
        compared = compare(self.original, self.candidate)
        self.assertEqual(len(compared["changes"]), 5)
        self.assertTrue(all(c["change"] == "fixed" for c in compared["changes"]))
        for item in compared["changes"]:
            with self.subTest(task=item["task"], args=item["args"]):
                original = next(
                    case for case in self.original["cases"]
                    if case["task"] == item["task"]
                    and case["args"] == item["args"]
                    and case["expected"] == item["expected"]
                )
                candidate = next(
                    case for case in self.candidate["cases"]
                    if case["task"] == item["task"]
                    and case["args"] == item["args"]
                    and case["expected"] == item["expected"]
                )
                self.assertFalse(original["passed"])
                self.assertTrue(candidate["passed"])
                self.assertEqual(item["baseline_actual"], original["actual"])
                self.assertEqual(item["candidate_actual"], candidate["actual"])
                self.assertEqual(item["baseline_error"], original["error"])
                self.assertEqual(item["candidate_error"], candidate["error"])
        self.assertEqual(compare(self.original, self.original)["changes"], [])

    def test_outcome_taxonomy_counts_all_cases_without_changing_scores(self):
        before = {
            "suite": "descriptive-only", "passed": 1, "total": 3,
            "cases": [
                {"task": "success", "args": [], "expected": 1,
                 "actual": 1, "passed": True, "error": None},
                {"task": "wrong_value", "args": [], "expected": 2,
                 "actual": 3, "passed": False, "error": None},
                {"task": "reported_error", "args": [], "expected": "pass",
                 "actual": "failure", "passed": False,
                 "error": "AssertionError: expected pass"},
            ],
        }
        after = copy.deepcopy(before)
        after["cases"][1]["actual"] = 2
        after["cases"][1]["passed"] = True
        after["cases"][2]["error"] = "RuntimeError: changed but still failed"
        after["passed"] = 2
        result = compare(before, after)
        self.assertEqual(result["outcome_counts"], {
            "baseline": {"passed": 1, "wrong_output": 1, "reported_error": 1},
            "candidate": {"passed": 2, "wrong_output": 0, "reported_error": 1},
        })
        self.assertEqual((result["fixed"], result["regressed"]), (1, 0))
        self.assertEqual(len(result["changed_failures"]), 1)
        for phase in ("baseline", "candidate"):
            self.assertEqual(sum(result["outcome_counts"][phase].values()), 3)

    def test_real_suite_outcome_counts_agree_with_scores(self):
        result = compare(self.original, self.candidate)
        for phase in ("baseline", "candidate"):
            counts = result["outcome_counts"][phase]
            self.assertEqual(counts["passed"], result[phase])
            self.assertEqual(sum(counts.values()), result["total"])

    def test_changed_still_failing_case_is_recorded_without_score_inflation(self):
        after = copy.deepcopy(self.original)
        failed = next(item for item in after["cases"] if not item["passed"])
        before = next(item for item in self.original["cases"]
                      if item["task"] == failed["task"] and item["args"] == failed["args"])
        failed["actual"] = {"new_wrong_output": True}
        failed["error"] = "RuntimeError: different unsuccessful behavior"
        failed["passed"] = False
        result = compare(self.original, after)
        self.assertEqual(
            (result["baseline"], result["candidate"], result["fixed"], result["regressed"]),
            (11, 11, 0, 0),
        )
        self.assertEqual(result["changes"], [])
        self.assertEqual(len(result["changed_failures"]), 1)
        item = result["changed_failures"][0]
        self.assertEqual(item["change"], "still_failing_changed")
        self.assertEqual(item["baseline_actual"], before["actual"])
        self.assertEqual(item["candidate_actual"], failed["actual"])
        self.assertEqual(item["baseline_error"], before["error"])
        self.assertEqual(item["candidate_error"], failed["error"])
        self.assertEqual(compare(self.original, self.original)["changed_failures"], [])

    def test_regressed_cases_are_exposed_with_original_values(self):
        changed = copy.deepcopy(self.candidate)
        control = next(
            item for item in changed["cases"]
            if item["passed"] and any(
                prior["task"] == item["task"]
                and prior["args"] == item["args"]
                and prior["passed"] for prior in self.original["cases"]
            )
        )
        control["actual"] = "broken after patch"
        control["passed"] = False
        changed["passed"] -= 1
        result = compare(self.original, changed)
        self.assertEqual((result["fixed"], result["regressed"]), (5, 1))
        regressions = [item for item in result["changes"] if item["change"] == "regressed"]
        self.assertEqual(len(regressions), 1)
        self.assertEqual(regressions[0]["task"], control["task"])
        self.assertEqual(regressions[0]["candidate_actual"], "broken after patch")
        self.assertEqual(len(result["changes"]), 6)

    def test_json_cli_writes_comparison_with_case_level_changes(self):
        import json
        import subprocess
        import sys
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            baseline = path / "baseline.json"
            candidate = path / "candidate.json"
            output = path / "results" / "comparison.json"
            baseline.write_text(json.dumps(self.original), encoding="utf-8")
            candidate.write_text(json.dumps(self.candidate), encoding="utf-8")
            run = subprocess.run(
                [sys.executable, "-m", "lab.report",
                 str(baseline), str(candidate), "--output", str(output)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn("fixed=5, regressed=0", run.stdout)
            summary = json.loads(output.read_text(encoding="utf-8"))
            from hashlib import sha256
            self.assertEqual(summary.pop("input_sha256"), {
                "baseline": sha256(baseline.read_bytes()).hexdigest(),
                "candidate": sha256(candidate.read_bytes()).hexdigest(),
            })
            self.assertEqual(summary, compare(
                json.loads(baseline.read_text(encoding="utf-8")),
                json.loads(candidate.read_text(encoding="utf-8")),
            ))
            self.assertEqual(len(summary["changes"]), 5)

    def test_optional_cli_regression_gate_preserves_report_and_failed_status(self):
        import json
        import subprocess
        import sys
        import tempfile
        from pathlib import Path

        changed = copy.deepcopy(self.candidate)
        control = next(
            item for item in changed["cases"]
            if item["passed"] and any(
                original["task"] == item["task"]
                and original["args"] == item["args"]
                and original["passed"] for original in self.original["cases"]
            )
        )
        control["actual"] = "regression observed"
        control["passed"] = False
        changed["passed"] -= 1
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            before = root / "before.json"
            after = root / "after.json"
            output = root / "audit.json"
            before.write_text(json.dumps(self.original), encoding="utf-8")
            after.write_text(json.dumps(changed), encoding="utf-8")
            args = [
                sys.executable, "-m", "lab.report",
                str(before), str(after), "--output", str(output),
            ]
            default = subprocess.run(
                args, capture_output=True, text=True, check=False
            )
            self.assertEqual(default.returncode, 0, default.stderr)
            gate = subprocess.run(
                args + ["--fail-on-regression"],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(gate.returncode, 1, gate.stderr)
            self.assertIn("fixed=5, regressed=1", gate.stdout)
            audit = json.loads(output.read_text(encoding="utf-8"))
            from hashlib import sha256
            self.assertEqual(audit["input_sha256"], {
                "baseline": sha256(before.read_bytes()).hexdigest(),
                "candidate": sha256(after.read_bytes()).hexdigest(),
            })
            self.assertEqual(audit["regressed"], 1)
            self.assertEqual(audit["fixed"], 5)
            self.assertEqual(
                [c["candidate_actual"] for c in audit["changes"]
                 if c["change"] == "regressed"],
                ["regression observed"],
            )

    def test_optional_regression_gate_allows_zero_regressions(self):
        import json
        import subprocess
        import sys
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            before, after = root / "before.json", root / "after.json"
            before.write_text(json.dumps(self.original), encoding="utf-8")
            after.write_text(json.dumps(self.candidate), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "lab.report", str(before), str(after),
                 "--fail-on-regression"],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("fixed=5, regressed=0", result.stdout)

    def test_cli_rejects_overwriting_inputs_and_file_aliases(self):
        import json
        import subprocess
        import sys
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            baseline = root / "baseline.json"
            candidate = root / "candidate.json"
            baseline.write_text(json.dumps(self.original), encoding="utf-8")
            candidate.write_text(json.dumps(self.candidate), encoding="utf-8")
            baseline_bytes, candidate_bytes = (
                baseline.read_bytes(), candidate.read_bytes()
            )
            symbolic = root / "baseline-symbolic.json"
            symbolic.symlink_to(baseline)
            hardlink = root / "candidate-hardlink.json"
            hardlink.hardlink_to(candidate)

            for label, output in (
                ("baseline", baseline),
                ("candidate", candidate),
                ("symbolic link", symbolic),
                ("hard link", hardlink),
            ):
                with self.subTest(output=label):
                    run = subprocess.run(
                        [sys.executable, "-m", "lab.report",
                         str(baseline), str(candidate),
                         "--output", str(output)],
                        capture_output=True, text=True, check=False,
                    )
                    self.assertNotEqual(run.returncode, 0)
                    self.assertIn("must not overwrite", run.stderr)
                    self.assertEqual(baseline.read_bytes(), baseline_bytes)
                    self.assertEqual(candidate.read_bytes(), candidate_bytes)

    def test_invalid_comparison_never_writes_output(self):
        import json
        import subprocess
        import sys
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            baseline = path / "baseline.json"
            candidate = path / "candidate.json"
            output = path / "comparison.json"
            baseline.write_text(json.dumps(self.original), encoding="utf-8")
            invalid = copy.deepcopy(self.candidate)
            invalid["passed"] = 999
            candidate.write_text(json.dumps(invalid), encoding="utf-8")
            run = subprocess.run(
                [sys.executable, "-m", "lab.report",
                 str(baseline), str(candidate), "--output", str(output)],
                capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(run.returncode, 0)
            self.assertFalse(output.exists())

    def test_reject_nonfinite_actual_values_in_programmatic_reports(self):
        for number in (float("nan"), float("inf"), -float("inf")):
            with self.subTest(value=repr(number)):
                malformed = copy.deepcopy(self.original)
                failed = next(case for case in malformed["cases"] if not case["passed"])
                failed["actual"] = number
                with self.assertRaisesRegex(ValueError, "Non-finite"):
                    compare(malformed, self.candidate)

    def test_cli_rejects_duplicate_input_fields(self):
        import json
        import subprocess
        import sys
        import tempfile
        from pathlib import Path

        for name, original, replacement in (
            ("baseline", '"suite": "published"',
             '"suite": "published", "suite": "published"'),
            ("candidate", '"error": null', '"error": null, "error": null'),
        ):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                before, after = root / "before.json", root / "after.json"
                output = root / "audit.json"
                before.write_text(json.dumps(self.original), encoding="utf-8")
                after.write_text(json.dumps(self.candidate), encoding="utf-8")
                path = before if name == "baseline" else after
                payload = path.read_text(encoding="utf-8")
                self.assertIn(original, payload)
                path.write_text(payload.replace(original, replacement, 1), encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, "-m", "lab.report", str(before), str(after),
                     "--output", str(output)],
                    capture_output=True, text=True, check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Duplicate JSON object key", result.stderr)
                self.assertFalse(output.exists())

    def test_cli_rejects_nonstandard_json_constants_before_writing_evidence(self):
        import json
        import subprocess
        import sys
        import tempfile
        from pathlib import Path

        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                before, after = root / "before.json", root / "after.json"
                output = root / "audit.json"
                malformed = copy.deepcopy(self.original)
                failed = next(case for case in malformed["cases"] if not case["passed"])
                failed["actual"] = float(constant)
                before.write_text(json.dumps(malformed), encoding="utf-8")
                after.write_text(json.dumps(self.candidate), encoding="utf-8")
                self.assertIn(constant, before.read_text(encoding="utf-8"))
                run = subprocess.run(
                    [sys.executable, "-m", "lab.report", str(before), str(after),
                     "--output", str(output)],
                    text=True, capture_output=True, check=False,
                )
                self.assertNotEqual(run.returncode, 0)
                self.assertIn("Non-finite", run.stderr)
                self.assertFalse(output.exists())

    def test_reject_different_suites(self):
        self.candidate["suite"] = "followup"
        with self.assertRaisesRegex(ValueError, "different"):
            compare(self.original, self.candidate)

    def test_reject_json_key_coercion_in_case_identity(self):
        for change_field in ("args", "expected"):
            with self.subTest(field=change_field):
                before = {
                    "suite": "typed-keys", "passed": 1, "total": 1,
                    "cases": [{
                        "task": "typed-map",
                        "args": [{"1": "value"}],
                        "expected": {"1": "value"}, "actual": {"1": "value"},
                        "passed": True, "error": None,
                    }],
                }
                after = copy.deepcopy(before)
                after_case = after["cases"][0]
                if change_field == "args":
                    after_case["args"] = [{1: "value"}]
                else:
                    after_case["expected"] = {1: "value"}
                    after_case["actual"] = {1: "value"}
                # JSON coerces integer mapping keys to strings, hiding
                # this mismatch in the canonical string alone.
                import json
                self.assertEqual(
                    json.dumps(before["cases"][0][change_field]),
                    json.dumps(after_case[change_field]),
                )
                with self.assertRaisesRegex(ValueError, "differs"):
                    compare(before, after)

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


    def test_reject_forged_nested_numeric_equality(self):
        forged = {
            "suite": "nested", "passed": 1, "total": 1,
            "cases": [{
                "task": "nested", "args": [], "expected": [0, 0],
                "actual": [False, False], "passed": True, "error": None,
            }],
        }
        self.assertEqual(forged["cases"][0]["actual"], [0, 0])
        with self.assertRaisesRegex(ValueError, "Invalid"):
            compare(forged, copy.deepcopy(forged))

    def test_reject_forged_dict_key_numeric_equality(self):
        forged = {
            "suite": "nested-map", "passed": 1, "total": 1,
            "cases": [{
                "task": "nested-map", "args": [],
                "expected": {0: "value"}, "actual": {False: "value"},
                "passed": True, "error": None,
            }],
        }
        self.assertEqual(forged["cases"][0]["actual"], forged["cases"][0]["expected"])
        with self.assertRaisesRegex(ValueError, "Invalid"):
            compare(forged, copy.deepcopy(forged))

    def test_reject_duplicate_cases_even_when_both_reports_match(self):
        before = copy.deepcopy(self.original)
        after = copy.deepcopy(self.candidate)
        for report in (before, after):
            duplicate = copy.deepcopy(report["cases"][0])
            report["cases"].append(duplicate)
            report["total"] += 1
            report["passed"] += int(duplicate["passed"])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            compare(before, after)



if __name__ == "__main__":
    unittest.main()
