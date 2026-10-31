"""Replay externally reported boltons rotate_file data loss on a pinned source."""

import json

from benchmarks.bugs.boltons_480.reproduce import (
    UPSTREAM_COMMIT,
    VENDOR,
    observe as run_script,
)

ISSUE = "https://github.com/mahmoud/boltons/issues/479"

SCRIPT = """
import json
import os
from pathlib import Path
import tempfile
from boltons import fileutils

assert Path(fileutils.__file__).resolve() == Path(os.environ["REPLAY_FILEUTILS"]).resolve()
rotate_file = fileutils.rotate_file
observed = {}

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "f.txt"
    path.write_text("CRITICAL DATA", encoding="utf-8")
    rotate_file(str(path), keep=1)
    names = sorted(p.name for p in Path(directory).iterdir())
    observed["keep_one_names"] = names
    backup = Path(directory) / "f.1.txt"
    observed["keep_one_data"] = backup.read_text(encoding="utf-8") if backup.exists() else None

with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    for index in range(1, 6):
        (root / f"f.{index}.txt").write_text(f"gen {index}", encoding="utf-8")
    (root / "f.txt").write_text("current", encoding="utf-8")
    rotate_file(str(root / "f.txt"), keep=5)
    names = sorted(p.name for p in root.iterdir())
    observed["keep_five_names"] = names
    observed["keep_five_data"] = [
        (root / name).read_text(encoding="utf-8") for name in names
    ]

with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    (root / "f.txt").write_text("single", encoding="utf-8")
    rotate_file(str(root / "f.txt"), keep=2)
    observed["fresh_two_names"] = sorted(p.name for p in root.iterdir())
    observed["fresh_two_data"] = (root / "f.1.txt").read_text(encoding="utf-8")
    rotate_file(str(root / "missing.txt"), keep=2)
    observed["missing_unchanged"] = sorted(p.name for p in root.iterdir())
    try:
        rotate_file(str(root / "not_a_file"), keep=0)
    except ValueError:
        observed["invalid_keep"] = "ValueError"
    else:
        observed["invalid_keep"] = "no error"
    (root / "directory.txt").mkdir()
    try:
        rotate_file(str(root / "directory.txt"), keep=2)
    except ValueError:
        observed["directory_error"] = "ValueError"
    else:
        observed["directory_error"] = "no error"

print(json.dumps(observed))
"""


def observe(vendor=VENDOR):
    """Reuse the FilePerms replay's subprocess; load the same pristine source."""
    return run_script(vendor=vendor, script=SCRIPT)


def main():
    print(json.dumps({
        "external_report": ISSUE,
        "upstream_commit": UPSTREAM_COMMIT,
        "variant": "unchanged historical baseline",
        "observed": observe(),
    }, indent=2))


if __name__ == "__main__":
    main()
