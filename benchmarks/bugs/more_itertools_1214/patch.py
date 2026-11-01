"""First-attempt repair of more-itertools #1214, preserving the class excerpt."""

from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "upstream" / "numeric_range.py"
EQ_OLD = "            else:\n                return (\n                    self._start == other._start\n"
EQ_NEW = ("            elif self._len == 1 or other._len == 1:\n"
          "                return self._len == other._len and self._start == other._start\n"
          + EQ_OLD)
HASH_OLD = ("    def __hash__(self):\n"
            "        if self:\n"
            "            return hash((self._start, self._get_by_index(-1), self._step))\n")
HASH_NEW = ("    def __hash__(self):\n"
            "        if self._len == 1:\n"
            "            return hash((1, self._start, None))\n"
            "        if self:\n"
            "            return hash((self._start, self._get_by_index(-1), self._step))\n")


def make_candidate(destination: Path) -> Path:
    destination = Path(destination)
    source = SOURCE.read_text(encoding="utf-8")
    if source.count(EQ_OLD) != 1 or source.count(HASH_OLD) != 1:
        raise ValueError("Unexpected pinned numeric_range equality/hash source")
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / "numeric_range.py"
    target.write_text(
        source.replace(EQ_OLD, EQ_NEW).replace(HASH_OLD, HASH_NEW),
        encoding="utf-8",
    )
    return target
