"""Second, separate local candidate for trailing spaces lost on no-EOL source.

The original tokenize-rt issue #33 offset candidate stays frozen and unchanged.
"""

from pathlib import Path

from .patch import make_candidate

OLD = "            tokens.append(\n                Token(UNIMPORTANT_WS, line[last_col:scol], sline, end_offset),\n            )"
NEW = "            ws_line = line if line else lines[sline]\n            tokens.append(\n                Token(UNIMPORTANT_WS, ws_line[last_col:scol], sline, end_offset),\n            )"


def make_candidate_with_roundtrip(destination: Path) -> Path:
    """Apply the second guard only after recreating the original frozen repair."""
    source_dir = make_candidate(destination)
    target = source_dir / "tokenize_rt.py"
    source = target.read_text(encoding="utf-8")
    if source.count(OLD) != 1:
        raise ValueError("Pinned trailing-whitespace anchor missing or duplicated")
    target.write_text(source.replace(OLD, NEW), encoding="utf-8")
    return source_dir
