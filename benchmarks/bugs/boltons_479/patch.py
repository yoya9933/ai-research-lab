"""Small local candidate for public boltons rotate_file issue #479."""

from pathlib import Path
from shutil import copytree, ignore_patterns

from benchmarks.bugs.boltons_480.reproduce import VENDOR

OLD = "    fns = [filename] + kept_names\n    for orig_name, kept_name in reversed(list(zip(fns, fns[1:]))):\n        if not os.path.exists(orig_name):\n            continue\n        os.rename(orig_name, kept_name)\n\n    if os.path.exists(kept_names[-1]):\n        os.remove(kept_names[-1])"
NEW = "    if os.path.exists(kept_names[-1]):\n        os.remove(kept_names[-1])\n\n    fns = [filename] + kept_names\n    for orig_name, kept_name in reversed(list(zip(fns, fns[1:]))):\n        if not os.path.exists(orig_name):\n            continue\n        os.rename(orig_name, kept_name)"


def make_candidate(destination: Path) -> Path:
    """Patch only a disposable copy, leaving the pinned source byte-identical."""
    destination = Path(destination)
    # Same-size source edits can accidentally reuse timestamp-based .pyc caches.
    copytree(VENDOR, destination, ignore=ignore_patterns("__pycache__", "*.pyc"))
    target = destination / "boltons" / "fileutils.py"
    original = target.read_text(encoding="utf-8")
    if original.count(OLD) != 1:
        raise ValueError("Pinned rotate_file source anchor missing or duplicated")
    target.write_text(original.replace(OLD, NEW), encoding="utf-8")
    return destination
