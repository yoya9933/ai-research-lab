"""Reproduce upstream Pygments PR #3190 on its exact pre-fix regex optimizer."""

import json
from pathlib import Path

from benchmarks.bugs.humanize_30.reproduce import observe as run_script

UPSTREAM_COMMIT = "c97c0b54f58d496e34f4b37eb9d0c482e79e21b3"
UPSTREAM_BLOB = "9010eb3fb517ff4134b4f52581179fa80b0f7540"
REPORT = "https://github.com/pygments/pygments/pull/3190"
VENDOR = Path(__file__).resolve().parent / "upstream"

SCRIPT = """
import json
import re
from regexopt import regex_opt

SAMPLES = {
    "duplicate_single": ["a", "a", "b"],
    "duplicate_suffix": ["as", "as", "bs"],
    "duplicate_prefix": ["car", "car", "cat"],
    "unique_single": ["a", "b"],
    "unique_suffix": ["as", "bs"],
    "empty": [],
    "regex_escaping": ["a+b", "a.b"],
}
results = {}
for key, words in SAMPLES.items():
    pattern = regex_opt(words)
    unique_pattern = regex_opt(sorted(set(words)))
    results[key] = {
        "words": words,
        "pattern": pattern,
        "unique_pattern": unique_pattern,
        "same_as_unique": pattern == unique_pattern,
        "matched": sorted(word for word in set(words) if re.fullmatch(pattern, word)),
    }
print(json.dumps(results, sort_keys=True))
"""


def observe(vendor=VENDOR):
    """Import the exact local module in the existing trusted subprocess runner."""
    return run_script(vendor=vendor, script=SCRIPT)


if __name__ == "__main__":
    print(json.dumps({
        "upstream_commit": UPSTREAM_COMMIT,
        "upstream_blob": UPSTREAM_BLOB,
        "report": REPORT,
        "variant": "unchanged upstream baseline",
        "observed": observe(),
    }, indent=2))
