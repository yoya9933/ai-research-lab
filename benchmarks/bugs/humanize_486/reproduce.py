"""Replay a public negative-ordinal bug report on the unchanged pinned humanize tree."""

import json

from benchmarks.bugs.humanize_30.reproduce import (
    UPSTREAM_COMMIT,
    VENDOR,
    observe as run_script,
)

REPORT = "https://github.com/python-humanize/humanize/pull/486"

SCRIPT = """
import humanize
import json

print(json.dumps({
    "minus_one": humanize.ordinal(-1),
    "minus_two": humanize.ordinal(-2),
    "minus_three": humanize.ordinal(-3),
    "minus_twenty_one": humanize.ordinal(-21),
    "minus_hundred_one": humanize.ordinal(-101),
    "minus_eleven": humanize.ordinal(-11),
    "minus_twelve": humanize.ordinal(-12),
    "minus_thirteen": humanize.ordinal(-13),
    "positive_one": humanize.ordinal(1),
    "positive_twenty_one": humanize.ordinal(21),
    "positive_111": humanize.ordinal(111),
    "zero": humanize.ordinal(0),
    "invalid": humanize.ordinal("bogus"),
    "negative_string": humanize.ordinal("-21"),
    "negative_female": humanize.ordinal(-1, gender="female"),
}))
"""


def observe(vendor=VENDOR):
    """Use the trusted local source in a separate process, not installed humanize."""
    return run_script(vendor=vendor, script=SCRIPT)


def main():
    print(json.dumps({
        "external_report": REPORT,
        "upstream_commit": UPSTREAM_COMMIT,
        "variant": "unchanged historical baseline",
        "observed": observe(),
    }, indent=2))


if __name__ == "__main__":
    main()
