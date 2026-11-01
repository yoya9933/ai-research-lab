"""Post-freeze, investigator-authored roundtrip probe for FilePerms.from_int."""

from .reproduce import VENDOR, observe as run_script

# Evaluate all unsigned nine-bit POSIX modes in the same isolated subprocess.
SCRIPT = """
import json
import os
from pathlib import Path
from boltons import fileutils

assert Path(fileutils.__file__).resolve() == Path(os.environ["REPLAY_FILEUTILS"]).resolve()
print(json.dumps([
    int(fileutils.FilePerms.from_int(mode)) for mode in range(0o1000)
]))
"""


def observe(vendor=VENDOR):
    return run_script(vendor=vendor, script=SCRIPT)
