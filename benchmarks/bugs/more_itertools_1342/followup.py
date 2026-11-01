"""Post-freeze input-domain checks for the unchanged more-itertools candidate.

This suite was authored *after* candidate commit 33cd99a; it is not blind.
"""

import json
from pathlib import Path
import tempfile

from benchmarks.bugs.humanize_30.reproduce import observe as run_script
from .patch import make_candidate
from .reproduce import VENDOR

SCRIPT = """
import json
from chunked_even import chunked_even

failures = []
total = 0
for n in range(1, 15):
    for length in range(41):
        total += 1
        data = list(range(length))
        try:
            chunks = list(chunked_even(iter(data), n))
            sizes = [len(chunk) for chunk in chunks]
            correct = (
                all(isinstance(chunk, list) for chunk in chunks)
                and [item for chunk in chunks for item in chunk] == data
                and all(0 < size <= n for size in sizes)
                and (not sizes or max(sizes) - min(sizes) <= 1)
            )
            if not correct:
                failures.append({"size": n, "length": length, "chunks": chunks})
        except Exception as exc:
            failures.append({
                "size": n, "length": length,
                "error": type(exc).__name__, "message": str(exc),
            })

class Poison:
    def __iter__(self):
        raise AssertionError("ignored iterable was inspected")

def ignored_input(n):
    try:
        return {"chunks": list(chunked_even(Poison(), n))}
    except Exception as exc:
        return {"error": type(exc).__name__, "message": str(exc)}

print(json.dumps({
    "positive_sizes": {
        "total": total, "passed": total - len(failures), "failures": failures,
    },
    "ignored_inputs": {"zero": ignored_input(0), "negative": ignored_input(-1)},
}))
"""


def observe(vendor=VENDOR):
    """Run trusted pinned or patched source without loading installed dependencies."""
    return run_script(vendor=vendor, script=SCRIPT)


def compare():
    before = observe()
    with tempfile.TemporaryDirectory() as name:
        after = observe(make_candidate(Path(name) / "patched"))
    return {"baseline": before, "candidate": after}


def main():
    print(json.dumps(compare(), indent=2))


if __name__ == "__main__":
    main()
