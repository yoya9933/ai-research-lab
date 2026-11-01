"""Compare two trusted evaluator JSON reports from the *same* test suite."""

import argparse
import json
from pathlib import Path


def same_value(actual, expected):
    """Compare nested outcomes without Python's bool/int numeric coercion."""
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, (list, tuple)):
        return len(actual) == len(expected) and all(
            same_value(a, b) for a, b in zip(actual, expected)
        )
    if isinstance(expected, dict):
        return len(actual) == len(expected) and all(
            any(type(key) is type(expected_key) and key == expected_key
                and same_value(actual[key], value) for key in actual)
            for expected_key, value in expected.items()
        )
    return actual == expected


def _case_identity(item):
    """Canonical JSON identity preserves bool/int/float differences in cases."""
    try:
        return json.dumps(
            [item["task"], item["args"], item["expected"]],
            sort_keys=True, ensure_ascii=False, allow_nan=False,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid evaluator case identity") from exc


def compare(baseline, candidate):
    for report in (baseline, candidate):
        if not isinstance(report, dict):
            raise ValueError("Invalid evaluator report or inconsistent score")
        cases = report.get("cases")
        if (
            not isinstance(cases, list)
            or not cases
            or any(
                not isinstance(item, dict)
                or not isinstance(item.get("task"), str)
                or not item["task"]
                or not isinstance(item.get("args"), (tuple, list))
                or "expected" not in item
                or "actual" not in item
                or "error" not in item
                or type(item.get("passed")) is not bool
                or (item["error"] is not None and not isinstance(item["error"], str))
                or item["passed"] != (
                    item["error"] is None
                    and same_value(item["actual"], item["expected"])
                )
                for item in cases
            )
            or type(report.get("total")) is not int
            or type(report.get("passed")) is not int
            or report["total"] != len(cases)
            or report["passed"] != sum(item["passed"] for item in cases)
        ):
            raise ValueError("Invalid evaluator report or inconsistent score")

    suite = baseline.get("suite")
    if not isinstance(suite, str) or not suite or suite != candidate.get("suite"):
        raise ValueError("Cannot compare different or unidentified suites")
    if baseline["total"] != candidate["total"]:
        raise ValueError("Case count differs")
    before_ids = [_case_identity(item) for item in baseline["cases"]]
    after_ids = [_case_identity(item) for item in candidate["cases"]]
    if len(set(before_ids)) != len(before_ids) or len(set(after_ids)) != len(after_ids):
        raise ValueError("Duplicate evaluator case identity")
    if before_ids != after_ids:
        raise ValueError("Case order, input or expected answer differs")

    changes, changed_failures = [], []
    for before, after in zip(baseline["cases"], candidate["cases"]):
        if before["passed"] != after["passed"]:
            change = "fixed" if after["passed"] else "regressed"
            target = changes
        elif not before["passed"] and (
            not same_value(before["actual"], after["actual"])
            or before["error"] != after["error"]
        ):
            change = "still_failing_changed"
            target = changed_failures
        else:
            continue
        target.append({
            "change": change,
            "task": before["task"], "args": before["args"],
            "expected": before["expected"],
            "baseline_actual": before["actual"], "candidate_actual": after["actual"],
            "baseline_error": before["error"], "candidate_error": after["error"],
        })
    return {
        "suite": suite, "total": baseline["total"],
        "baseline": baseline["passed"], "candidate": candidate["passed"],
        "delta": candidate["passed"] - baseline["passed"],
        "fixed": sum(item["change"] == "fixed" for item in changes),
        "regressed": sum(item["change"] == "regressed" for item in changes),
        "changes": changes,
        "changed_failures": changed_failures,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path,
                        help="Save validated case-level comparison as JSON")
    parser.add_argument("--fail-on-regression", action="store_true",
                        help="Exit 1 if any previously passing case regresses")
    args = parser.parse_args()
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    result = compare(baseline, candidate)
    if args.output and any(
        args.output.resolve() == path.resolve()
        or (args.output.exists() and args.output.samefile(path))
        for path in (args.baseline, args.candidate)
    ):
        parser.error("--output must not overwrite an input report")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(
        f"{result['suite']}: {result['baseline']}/{result['total']} -> "
        f"{result['candidate']}/{result['total']} (delta {result['delta']:+d}); "
        f"fixed={result['fixed']}, regressed={result['regressed']}; "
        f"changed failures={len(result['changed_failures'])}"
    )
    if args.fail_on_regression and result["regressed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
