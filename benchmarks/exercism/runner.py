"""Run pinned Exercism tests against a trusted in-repository candidate."""

import argparse
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent
UPSTREAM_SHA = "6105f6d9d3ef66ce3d5c8f529d2882af3d76b706"
TRACKS = {
    "starter": ("starter", "tests", 29),
    "attempt_001": ("attempt_001", "tests", 29),
    "starter_002": ("trial_002/starter", "trial_002/tests", 44),
    "attempt_002": ("trial_002/attempt_002", "trial_002/tests", 44),
}


class RecordingResult(unittest.TestResult):
    def startTest(self, test):
        super().startTest(test)
        self.cases.append({
            "task": test.id(), "args": [], "expected": "pass",
            "actual": "incomplete", "passed": False, "error": None
        })

    def addSuccess(self, test):
        super().addSuccess(test)
        self.cases[-1].update(actual="pass", passed=True)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        case = self.cases[-1]
        case["actual"] = "error" if case["actual"] == "error" else "failure"
        case["error"] = "\n".join(filter(
            None, (case["error"], self._exc_info_to_string(err, test))
        ))

    def addError(self, test, err):
        super().addError(test, err)
        # setUpClass/tearDownClass and module fixtures do not call startTest.
        if not self.cases or self.cases[-1]["task"] != test.id():
            return
        case = self.cases[-1]
        case["actual"] = "error"
        case["error"] = "\n".join(filter(
            None, (case["error"], self._exc_info_to_string(err, test))
        ))

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err is not None:
            self.scored_subtest_errors.add(subtest.id())
            case = self.cases[-1]
            kind = "failure" if issubclass(err[0], test.failureException) else "error"
            case["actual"] = "error" if "error" in (case["actual"], kind) else "failure"
            detail = f"{subtest.id()}\n{self._exc_info_to_string(err, subtest)}"
            case["error"] = "\n".join(filter(None, (case["error"], detail)))

    def __init__(self):
        super().__init__()
        self.cases = []
        self.scored_subtest_errors = set()


def evaluate(candidate):
    if candidate not in TRACKS:
        raise ValueError("Only named, reviewed in-repository candidates are supported")
    code_dir, test_dir, expected_tests = TRACKS[candidate]
    directory = ROOT / code_dir
    if not directory.is_dir():
        raise FileNotFoundError(directory)
    test_directory = ROOT / test_dir
    module_names = set()
    for root in (directory, test_directory):
        for path in root.rglob("*.py"):
            parts = path.relative_to(root).with_suffix("").parts
            if parts[-1] == "__init__":
                parts = parts[:-1]
            if parts:
                module_names.add(".".join(parts))
    previous_modules = {
        name: sys.modules.pop(name) for name in module_names if name in sys.modules
    }
    previous_path = sys.path[:]
    try:
        sys.path.insert(0, str(directory))
        loader = unittest.TestLoader()
        suite = loader.discover(str(test_directory), pattern="*_test.py")
        if loader.errors:
            raise RuntimeError(
                "Upstream test discovery failed:\n" + "\n".join(loader.errors)
            )
        result = RecordingResult()
        suite.run(result)
        identities = [case["task"] for case in result.cases]
        unscored = [
            (test.id(), detail) for test, detail in result.errors
            if test.id() not in identities
            and test.id() not in result.scored_subtest_errors
        ]
        if unscored:
            raise RuntimeError(
                "Unscored upstream fixture errors:\n"
                + "\n".join(f"{name}:\n{detail}" for name, detail in unscored)
            )
        if result.testsRun != expected_tests:
            raise RuntimeError(f"Expected {expected_tests} upstream tests; got {result.testsRun}")
        if len(identities) != result.testsRun or len(set(identities)) != result.testsRun:
            raise RuntimeError("Missing or duplicate upstream test identities")
        if result.skipped or result.expectedFailures or result.unexpectedSuccesses:
            raise RuntimeError(
                "Unscorable upstream test outcomes: "
                f"skipped={len(result.skipped)}, "
                f"expected_failures={len(result.expectedFailures)}, "
                f"unexpected_successes={len(result.unexpectedSuccesses)}"
            )
        return {
            "suite": f"exercism/python@{UPSTREAM_SHA}" + (":trial-002" if candidate.endswith("_002") else ""),
            "passed": sum(item["passed"] for item in result.cases),
            "total": result.testsRun,
            "cases": result.cases,
        }
    finally:
        sys.path[:] = previous_path
        for name in module_names:
            sys.modules.pop(name, None)
        sys.modules.update(previous_modules)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", choices=tuple(TRACKS))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-all-pass", action="store_true")
    args = parser.parse_args()
    report = evaluate(args.candidate)
    print(f"{args.candidate}: {report['passed']}/{report['total']} external tests passed")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.require_all_pass and report["passed"] != report["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
