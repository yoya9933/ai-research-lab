"""Replay externally reported boltons FilePerms permission-revocation defect.

All filesystem writes occur under a TemporaryDirectory in a child process.
"""

import json
import os
from pathlib import Path
import subprocess
import sys

UPSTREAM_COMMIT = "967864f89791509f9eb36b22b4579d36b72a6df2"
ISSUE = "https://github.com/mahmoud/boltons/issues/480"
VENDOR = Path(__file__).resolve().parent / "upstream"

SCRIPT = """
import json
import os
from pathlib import Path
import stat
import tempfile
from boltons import fileutils

assert Path(fileutils.__file__).resolve() == Path(os.environ["REPLAY_FILEUTILS"]).resolve()
FilePerms = fileutils.FilePerms

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "fixture.txt"
    path.write_text("test fixture", encoding="utf-8")
    os.chmod(path, 0o644)
    permissions = FilePerms.from_path(path)
    before = oct(stat.S_IMODE(path.stat().st_mode))
    permissions.other = ""
    after_other = oct(int(permissions))
    permissions.group = ""
    after_group = oct(int(permissions))
    display = repr(permissions)
    os.chmod(path, int(permissions))
    on_disk = oct(stat.S_IMODE(path.stat().st_mode))

widened = FilePerms(user="rw")
widened.group = "r"
try:
    FilePerms(user="invalid")
except ValueError:
    invalid = "ValueError"
else:
    invalid = "no error"

print(json.dumps({
    "initial_mode": before,
    "after_revoke_other": after_other,
    "after_revoke_group": after_group,
    "display": display,
    "chmod_mode": on_disk,
    "construct": oct(int(FilePerms("rw", "r", "r"))),
    "widen": oct(int(widened)),
    "empty": oct(int(FilePerms())),
    "invalid": invalid,
}))
"""


def observe(vendor=VENDOR):
    """Run only the trusted pinned local source in a separate process."""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(vendor)
    environment["REPLAY_FILEUTILS"] = str(Path(vendor) / "boltons" / "fileutils.py")
    completed = subprocess.run(
        [sys.executable, "-c", SCRIPT], env=environment, capture_output=True,
        text=True, check=True, timeout=15,
    )
    return json.loads(completed.stdout)


def main():
    print(json.dumps({
        "external_report": ISSUE, "upstream_commit": UPSTREAM_COMMIT,
        "variant": "unchanged historical baseline", "observed": observe(),
    }, indent=2))


if __name__ == "__main__":
    main()
