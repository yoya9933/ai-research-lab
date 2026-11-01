"""Apply the accepted boundary guard to a temporary copy, not the pinned excerpt."""

from pathlib import Path
from shutil import copytree, ignore_patterns

from .reproduce import VENDOR

ANCHOR = "    iterator = iter(iterable)\n\n    # Initialize a buffer to process the chunks"
GUARDS = """    if n < 0:
        raise ValueError('n must be at least 0')
    if n == 0:
        return

"""


def make_candidate(destination: Path) -> Path:
    """Copy trusted source without inherited bytecode; refuse an unexpected anchor."""
    destination = Path(destination)
    copytree(VENDOR, destination, ignore=ignore_patterns("__pycache__", "*.pyc"))
    target = destination / "chunked_even.py"
    original = target.read_text(encoding="utf-8")
    if original.count(ANCHOR) != 1:
        raise ValueError("Pinned chunked_even source anchor missing or duplicated")
    target.write_text(original.replace(ANCHOR, GUARDS + ANCHOR), encoding="utf-8")
    return destination
