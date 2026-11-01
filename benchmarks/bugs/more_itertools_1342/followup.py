"""Post-candidate property matrix for accepted more-itertools issue #1342.

31 input lengths x 12 chunk sizes; code executes only a trusted pinned excerpt.
This matrix was authored after the accepted-fix candidate was committed; not blind.
"""

import json

from benchmarks.bugs.humanize_30.reproduce import observe as run_script
from .reproduce import VENDOR

SCRIPT = """
import json
from chunked_even import chunked_even


def run_case(length, size):
    source = iter(range(length))
    try:
        outcome = {"chunks": list(chunked_even(source, size))}
    except Exception as exc:
        outcome = {"error": type(exc).__name__, "message": str(exc)}
    outcome["remaining"] = list(source)
    return outcome


print(json.dumps([
    {"length": length, "size": size, **run_case(length, size)}
    for length in range(31)
    for size in range(-3, 9)
]))
"""


def observe(vendor=VENDOR):
    """Return identical ordered input-domain observations for a source variant."""
    return run_script(vendor=vendor, script=SCRIPT)


if __name__ == "__main__":
    observations = observe()
    print(json.dumps({
        "kind": "post-freeze investigator-written property inputs, not blind",
        "cases": len(observations),
        "positive_cases": sum(item["size"] > 0 for item in observations),
        "zero_cases": sum(item["size"] == 0 for item in observations),
        "negative_cases": sum(item["size"] < 0 for item in observations),
    }, indent=2))
