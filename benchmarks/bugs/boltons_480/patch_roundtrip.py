"""Secondary local candidate: fix from_int positional padding after PR #22 patch."""

from pathlib import Path

from .patch import make_candidate as make_permission_candidate

OLD = """        parts.reverse()
        return cls(*parts)"""
NEW = """        parts.extend([""] * (3 - len(parts)))
        parts.reverse()
        return cls(*parts)"""


def make_candidate(destination: Path) -> Path:
    """Keep the first candidate intact; patch only its temporary source copy."""
    vendor = make_permission_candidate(destination)
    target = vendor / "boltons" / "fileutils.py"
    source = target.read_text(encoding="utf-8")
    if source.count(OLD) != 1:
        raise ValueError("Pinned from_int source anchor missing or duplicated")
    target.write_text(source.replace(OLD, NEW), encoding="utf-8")
    return vendor
