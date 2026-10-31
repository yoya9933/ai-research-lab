"""Local candidate for the public negative-ordinal report; pinned upstream stays pristine."""

from pathlib import Path
from shutil import copytree, ignore_patterns

from benchmarks.bugs.humanize_30.reproduce import VENDOR

OLD = '''    if value % 100 in (11, 12, 13):  # special case
        return f"{value}{t[0]}"
    return f"{value}{t[value % 10]}"'''
NEW = '''    magnitude = abs(value)
    if magnitude % 100 in (11, 12, 13):  # special case
        return f"{value}{t[0]}"
    return f"{value}{t[magnitude % 10]}"'''


def make_candidate(destination: Path) -> Path:
    """Copy trusted source, then fail closed if the expected ordinal code has changed."""
    destination = Path(destination)
    copytree(VENDOR, destination, ignore=ignore_patterns("__pycache__", "*.pyc"))
    target = destination / "humanize" / "number.py"
    original = target.read_text(encoding="utf-8")
    if original.count(OLD) != 1:
        raise ValueError("Pinned ordinal source anchor missing or duplicated")
    target.write_text(original.replace(OLD, NEW), encoding="utf-8")
    return destination
