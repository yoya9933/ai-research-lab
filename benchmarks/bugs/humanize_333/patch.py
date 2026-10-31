"""Minimal candidate for external humanize issue #333; upstream remains unchanged."""

from pathlib import Path
import shutil

from benchmarks.bugs.humanize_30.reproduce import VENDOR

OLD = '''        try:
            int(value)  # Explicitly don't support string such as "NaN" or "inf"
            value = float(value)
            delta = dt.timedelta(seconds=value)
        except (ValueError, TypeError):
            return str(value)'''
NEW = '''        try:
            int(value)  # Explicitly don't support string such as "NaN" or "inf"
        except (ValueError, TypeError, OverflowError):
            return str(value)
        value = float(value)
        delta = dt.timedelta(seconds=value)''' 

def make_candidate(destination: Path) -> Path:
    """Copy trusted pinned vendor tree and change one guarded conversion block."""
    destination = Path(destination)
    shutil.copytree(VENDOR, destination)
    target = destination / "humanize" / "time.py"
    original = target.read_text(encoding="utf-8")
    if original.count(OLD) != 1:
        raise ValueError("Pinned source anchor changed; refusing speculative patch")
    target.write_text(original.replace(OLD, NEW), encoding="utf-8")
    return destination
