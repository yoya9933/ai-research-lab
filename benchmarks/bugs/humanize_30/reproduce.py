"""Reproduce a third-party user-reported issue using a pinned source snapshot."""

import json
import os
from pathlib import Path
import subprocess
import sys

VENDOR = Path(__file__).resolve().parent / "upstream"
ISSUE = "https://github.com/python-humanize/humanize/issues/30"
UPSTREAM_COMMIT = "9528daf55fd7178c025f7294b8e349f8b3524175"

SCRIPT = """
import humanize
import json

print(json.dumps({
    "round_minutes": humanize.precisedelta(32399, minimum_unit="minutes", format="%0.0f"),
    "round_hours": humanize.precisedelta(91500, minimum_unit="hours", format="%0.0f"),
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
    print(json.dumps({
        "issue": ISSUE, "upstream_commit": UPSTREAM_COMMIT,
        "observed": observe(),
    }, indent=2))


if __name__ == "__main__":
    main()
