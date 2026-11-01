"""Evaluate deterministic cases against a trusted Python module."""

import argparse
from copy import deepcopy
import importlib
import json
from pathlib import Path

from .cases import CASES, FOLLOWUP_CASES
from .report import same_value


def evaluate(module, cases=CASES):
    cases = deepcopy(cases)
    results = []
    for name, samples in cases.items():
        function = getattr(module, name, None)
        if not callable(function):
            raise ValueError(f"Missing callable: {name}")
        for args, expected in samples:
            try:
                actual = deepcopy(function(*deepcopy(args)))
                passed = same_value(actual, expected)
                error = None
                # Preserve failed type distinctions that JSON would erase.
                try:
                    json_stable = same_value(
                        actual, json.loads(json.dumps(actual, allow_nan=False))
                    )
                except (TypeError, ValueError):
                    json_stable = False
                if not json_stable:
                    error = f"Non-JSON-stable output: {type(actual).__name__}"
                    actual = repr(actual)
                    passed = False
            except Exception as exc:
                actual, passed, error = None, False, f"{type(exc).__name__}: {exc}"
            results.append({"task": name, "args": args, "expected": expected,
                            "actual": actual, "passed": passed, "error": error})
    return {"passed": sum(r["passed"] for r in results), "total": len(results),
            "cases": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["evaluate"])
    parser.add_argument("--module", required=True, help="Trusted importable Python module")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--suite", choices=("published", "followup"), default="published")
    parser.add_argument("--require-all-pass", action="store_true",
                        help="Exit with error code 1 when any case fails")
    args = parser.parse_args()
    selected_cases = CASES if args.suite == "published" else FOLLOWUP_CASES
    report = evaluate(importlib.import_module(args.module), selected_cases)
    report["suite"] = args.suite
    print(f"{report['passed']}/{report['total']} cases passed")
    for item in report["cases"]:
        print(f"{'PASS' if item['passed'] else 'FAIL'} {item['task']}: {item['args']}")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n",
                               encoding="utf-8")
    if args.require_all_pass and report["passed"] != report["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
