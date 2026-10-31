"""Compare two trusted evaluator JSON reports from the *same* test suite."""

import argparse
import json
from pathlib import Path


def compare(baseline, candidate):
    for report in (baseline, candidate):
        cases = report.get("cases")
        if (
            not isinstance(cases, list)
            or not cases
            or any(type(item.get("passed")) is not bool for item in cases)
            or type(report.get("total")) is not int
            or type(report.get("passed")) is not int
            or report["total"] != len(cases)
            or report["passed"] != sum(item["passed"] for item in cases)
        ):
            raise ValueError("Invalid evaluator report or inconsistent score")

    suite = baseline.get("suite")
    if not isinstance(suite, str) or not suite or suite != candidate.get("suite"):
        raise ValueError("Cannot compare different or unidentified suites")
    for before, after in zip(baseline["cases"], candidate["cases"]):
        if any(before.get(key) != after.get(key) for key in ("task", "args", "expected")):
            raise ValueError("Case order, input or expected answer differs")

    pairs = zip(baseline["cases"], candidate["cases"])
    fixed = sum(not a["passed"] and b["passed"] for a, b in pairs)
    pairs = zip(baseline["cases"], candidate["cases"])
    regressed = sum(a["passed"] and not b["passed"] for a, b in pairs)
    return {
        "suite": suite, "total": baseline["total"],
        "baseline": baseline["passed"], "candidate": candidate["passed"],
        "delta": candidate["passed"] - baseline["passed"],
        "fixed": fixed, "regressed": regressed
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    result = compare(baseline, candidate)
    print(
        f"{result['suite']}: {result['baseline']}/{result['total']} -> "
        f"{result['candidate']}/{result['total']} (delta {result['delta']:+d}); "
        f"fixed={result['fixed']}, regressed={result['regressed']}"
    )


if __name__ == "__main__":
    main()
