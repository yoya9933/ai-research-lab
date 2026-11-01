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
        self.cases[-1].update(actual="failure", error=self._exc_info_to_string(err, test))

    def addError(self, test, err):
        super().addError(test, err)
        self.cases[-1].update(actual="error", error=self._exc_info_to_string(err, test))

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err is not None:
            case = self.cases[-1]
            kind = "failure" if issubclass(err[0], test.failureException) else "error"
            case["actual"] = "error" if "error" in (case["actual"], kind) else "failure"
            detail = self._exc_info_to_string(err, subtest)
            case["error"] = "\n".join(filter(None, (case["error"], detail)))

    def __init__(self):
        super().__init__()
        self.cases = []


def evaluate(candidate):
    if candidate not in TRACKS:
        raise ValueError("Only named, reviewed in-repository candidates are supported")
    code_dir, test_dir, expected_tests = TRACKS[candidate]
    directory = ROOT / code_dir
    if not directory.is_dir():
        raise FileNotFoundError(directory)
    test_directory = ROOT / test_dir
    module_names = {path.stem for path in directory.glob("*.py")}
    module_names.update(path.stem for path in test_directory.glob("*_test.py"))
    previous_modules = {
        name: sys.modules.pop(name) for name in module_names if name in sys.modules
    }
    previous_path = sys.path[:]
    try:
        sys.path.insert(0, str(directory))
        suite = unittest.TestLoader().discover(str(test_directory), pattern="*_test.py")
        result = RecordingResult()
        suite.run(result)
        if result.testsRun != expected_tests:
            raise RuntimeError(f"Expected {expected_tests} upstream tests; got {result.testsRun}")
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
