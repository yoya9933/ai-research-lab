"""Replay the accepted upstream more-itertools PR #1342 on an exact function excerpt.

The vendored function body is copied verbatim from the pinned upstream file.
Only the standard-library islice import is added to make it independently importable.
"""

import json
from pathlib import Path

from benchmarks.bugs.humanize_30.reproduce import observe as run_script

UPSTREAM_COMMIT = "4aeb4338ae1407d8da9723e86da99efeb446f719"
UPSTREAM_BLOB = "9c56ab37558733ece94d676f71d502d8048bc1d5"
REPORT = "https://github.com/more-itertools/more-itertools/pull/1342"
VENDOR = Path(__file__).resolve().parent / "upstream"

SCRIPT = """
import json
from chunked_even import chunked_even

def probe(items, n):
    source = iter(items)
    try:
        result = {"chunks": list(chunked_even(source, n))}
    except Exception as exc:
        result = {"error": type(exc).__name__}
    result["remaining"] = list(source)
    return result

def ignored_noniterable():
    try:
        return {"chunks": list(chunked_even(None, 0))}
    except Exception as exc:
        return {"error": type(exc).__name__}

print(json.dumps({
    "zero_nonempty": probe("abcd", 0),
    "zero_empty": probe("", 0),
    "negative_nonempty": probe("abcd", -1),
    "negative_empty": probe("", -1),
    "zero_none": ignored_noniterable(),
    "normal_seven_three": probe([1, 2, 3, 4, 5, 6, 7], 3),
    "normal_six_two": probe([1, 2, 3, 4, 5, 6], 2),
    "normal_empty": probe([], 3),
    "normal_one": probe("ab", 1),
    "invalid_type": probe("abcd", "bad"),
}))
"""


def observe(vendor=VENDOR):
    """Execute only the pinned trusted excerpt using the existing subprocess runner."""
    return run_script(vendor=vendor, script=SCRIPT)


def main():
    print(json.dumps({
        "upstream_commit": UPSTREAM_COMMIT,
        "upstream_blob": UPSTREAM_BLOB,
        "external_pr": REPORT,
        "variant": "pre-fix function excerpt",
        "observed": observe(),
    }, indent=2))


if __name__ == "__main__":
    main()
