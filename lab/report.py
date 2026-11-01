"""Compare two trusted evaluator JSON reports from the *same* test suite."""

import argparse
from hashlib import sha256
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


def _outcome_counts(report):
    counts = {"passed": 0, "wrong_output": 0, "reported_error": 0}
    for case in report["cases"]:
        if case["passed"]:
            kind = "passed"
        elif case["error"] is not None:
            kind = "reported_error"
        else:
            kind = "wrong_output"
        counts[kind] += 1
    return counts


def compare(baseline, candidate):
    for report in (baseline, candidate):
        if not isinstance(report, dict):
            raise ValueError("Invalid evaluator report or inconsistent score")
        try:
            json.dumps(report, allow_nan=False)
        except (TypeError, ValueError) as exc:
            raise ValueError("Non-finite or non-JSON evaluator report") from exc
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
    if before_ids != after_ids or any(
        before["task"] != after["task"]
        or not same_value(before["args"], after["args"])
        or not same_value(before["expected"], after["expected"])
        for before, after in zip(baseline["cases"], candidate["cases"])
    ):
        raise ValueError("Case order, input or expected answer differs")

    changes, changed_failures = [], []
    by_task = {}
    for before, after in zip(baseline["cases"], candidate["cases"]):
        counts = by_task.setdefault(before["task"], {
            "total": 0, "baseline": 0, "candidate": 0,
            "fixed": 0, "regressed": 0, "changed_failures": 0,
        })
        counts["total"] += 1
        counts["baseline"] += int(before["passed"])
        counts["candidate"] += int(after["passed"])
        if before["passed"] != after["passed"]:
            change = "fixed" if after["passed"] else "regressed"
            counts[change] += 1
            target = changes
        elif not before["passed"] and (
            not same_value(before["actual"], after["actual"])
            or before["error"] != after["error"]
        ):
            change = "still_failing_changed"
            counts["changed_failures"] += 1
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
        "by_task": by_task,
        "outcome_counts": {
            "baseline": _outcome_counts(baseline),
            "candidate": _outcome_counts(candidate),
        },
    }


def _unique_json_keys(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"Duplicate JSON object key: {key}")
        value[key] = item
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path,
                        help="Save validated case-level comparison as JSON")
    parser.add_argument("--fail-on-regression", action="store_true",
                        help="Exit 1 if any previously passing case regresses")
    args = parser.parse_args()
    baseline_bytes = args.baseline.read_bytes()
    candidate_bytes = args.candidate.read_bytes()
    baseline = json.loads(baseline_bytes.decode("utf-8"), object_pairs_hook=_unique_json_keys)
    candidate = json.loads(candidate_bytes.decode("utf-8"), object_pairs_hook=_unique_json_keys)
    result = compare(baseline, candidate)
    if args.output and any(
        args.output.resolve() == path.resolve()
        or (args.output.exists() and args.output.samefile(path))
        for path in (args.baseline, args.candidate)
    ):
        parser.error("--output must not overwrite an input report")
    if args.output:
        result["input_sha256"] = {
            "baseline": sha256(baseline_bytes).hexdigest(),
            "candidate": sha256(candidate_bytes).hexdigest(),
        }
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
