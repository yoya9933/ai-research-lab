"""Publicly described #3190 deduplication guard on an isolated copy, not vendor."""

from pathlib import Path
from shutil import copytree, ignore_patterns

from .reproduce import VENDOR

OLD = "    strings = sorted(strings)\n"
NEW = "    strings = sorted(set(strings))\n"


def make_candidate(destination: Path) -> Path:
    """Clone the trusted pre-fix module without bytecode and fail closed on drift."""
    destination = Path(destination)
    copytree(VENDOR, destination, ignore=ignore_patterns("__pycache__", "*.pyc"))
    target = destination / "regexopt.py"
    source = target.read_text(encoding="utf-8")
    if source.count(OLD) != 1:
        raise ValueError("Pinned regex_opt sorting anchor missing or duplicated")
    target.write_text(source.replace(OLD, NEW), encoding="utf-8")
    return destination
