"""Reproduce humanize issue #333 against an unmodified, pinned source tree."""

import json

from benchmarks.bugs.humanize_30.reproduce import (
    UPSTREAM_COMMIT,
    VENDOR,
    observe as run_script,
)

ISSUE = "https://github.com/python-humanize/humanize/issues/333"

SCRIPT = """
import humanize
import json

def outcome(value):
    try:
        return {"value": humanize.naturaldelta(value)}
    except Exception as exc:
        return {"error": type(exc).__name__}

print(json.dumps({
    "positive_inf": outcome(float("inf")),
    "negative_inf": outcome(float("-inf")),
    "nan": outcome(float("nan")),
    "finite": outcome(30),
    "invalid": outcome("bogus"),
    "too_large": outcome(10**20),
}))
"""


def observe(vendor=VENDOR):
    """Run exact public reporter cases and controls in an isolated subprocess."""
    return run_script(vendor=vendor, script=SCRIPT)


def main():
    print(json.dumps({
        "issue": ISSUE,
        "upstream_commit": UPSTREAM_COMMIT,
        "variant": "unmodified baseline",
        "observed": observe(),
    }, indent=2))


if __name__ == "__main__":
    main()
