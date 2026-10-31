"""Reproduce a third-party user-reported issue using a pinned source snapshot."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

VENDOR = Path(__file__).resolve().parent / "upstream"
ISSUE = "https://github.com/python-humanize/humanize/issues/30"
UPSTREAM_COMMIT = "9528daf55fd7178c025f7294b8e349f8b3524175"

SCRIPT = """
import humanize
import json

print(json.dumps({
    "round_minutes": humanize.precisedelta(32399, minimum_unit="minutes", format="%0.0f"),
    "round_hours": humanize.precisedelta(91500, minimum_unit="hours", format="%0.0f"),
    "singular_minute": humanize.precisedelta(3633, minimum_unit="minutes", format="%0.0f"),
    "default": humanize.precisedelta(32399),
    "fractional": humanize.precisedelta(32399, minimum_unit="minutes"),
}))
"""


def observe(vendor=VENDOR):
    """Import the pinned code in a separate Python process; never use installed humanize."""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(vendor)
    completed = subprocess.run(
        [sys.executable, "-c", SCRIPT], env=environment, capture_output=True,
        text=True, check=True, timeout=15,
    )
    return json.loads(completed.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", action="store_true",
                        help="Evaluate a patched temporary copy, leaving the upstream snapshot pristine")
    args = parser.parse_args()
    if args.candidate:
        from .patch import make_candidate
        with tempfile.TemporaryDirectory() as directory:
            observed = observe(make_candidate(Path(directory) / "patched"))
    else:
        observed = observe()
    print(json.dumps({
        "issue": ISSUE, "upstream_commit": UPSTREAM_COMMIT,
        "variant": "candidate" if args.candidate else "baseline",
        "observed": observed,
    }, indent=2))


if __name__ == "__main__":
    main()
