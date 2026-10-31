"""A minimal candidate patch for the *frozen* upstream humanize issue #30."""

from pathlib import Path
from shutil import copytree

from .reproduce import VENDOR

NEEDLE = "    suppress_set = {Unit[s.upper()] for s in suppress}\n"
INSERT = '''    # Round before splitting into hours/minutes so a 60-unit carry is normalized.
    if format == "%0.0f" and minimum_unit in ("minutes", "hours"):
        import datetime as dt

        quantum = 60 if minimum_unit == "minutes" else 3600
        delta = dt.timedelta(
            seconds=round(delta.total_seconds() / quantum) * quantum
        )

'''


def make_candidate(destination: Path) -> Path:
    """Produce an isolated candidate; never overwrite the upstream snapshot."""
    copytree(VENDOR, destination)
    module = destination / "humanize" / "time.py"
    original = module.read_text(encoding="utf-8")
    if original.count(NEEDLE) != 1:
        raise ValueError("Pinned upstream rounding anchor is missing or duplicated")
    module.write_text(original.replace(NEEDLE, INSERT + NEEDLE), encoding="utf-8")
    return destination
