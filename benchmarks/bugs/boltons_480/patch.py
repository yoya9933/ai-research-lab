"""Isolated candidate for external boltons FilePerms issue #480.

Only a temporary copy is changed; pinned upstream and BSD license remain intact.
"""

from pathlib import Path
from shutil import copytree

from .reproduce import VENDOR

OLD = "            fp_obj._integer |= mode\n"
NEW = (
    "            mask = 0o7 << (self.offset * 3)\n"
    "            fp_obj._integer = (fp_obj._integer & ~mask) | mode\n"
)


def make_candidate(destination: Path) -> Path:
    destination = Path(destination)
    copytree(VENDOR, destination)
    target = destination / "boltons" / "fileutils.py"
    original = target.read_text(encoding="utf-8")
    if original.count(OLD) != 1:
        raise ValueError("Pinned FilePerms source anchor missing or duplicated")
    target.write_text(original.replace(OLD, NEW), encoding="utf-8")
    return destination
