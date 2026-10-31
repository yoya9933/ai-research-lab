"""Local, unblinded candidate for tokenize-rt issue #33.

Only an ephemeral copy of the exact upstream snapshot is modified.
"""

from pathlib import Path
from shutil import copytree, ignore_patterns

from .reproduce import VENDOR

OLD = "        utf8_byte_offset = len(line[:scol].encode())\n"
NEW = "        if tok_name == 'NEWLINE' and not tok_text:\n            utf8_byte_offset = len(lines[sline][:scol].encode())\n        else:\n            utf8_byte_offset = len(line[:scol].encode())\n"


def make_candidate(destination: Path) -> Path:
    destination = Path(destination)
    copytree(VENDOR, destination, ignore=ignore_patterns("__pycache__", "*.pyc"))
    target = destination / "tokenize_rt.py"
    original = target.read_text(encoding="utf-8")
    if original.count(OLD) != 1:
        raise ValueError("Pinned NEWLINE source anchor missing or duplicated")
    target.write_text(original.replace(OLD, NEW), encoding="utf-8")
    return destination
