"""First-attempt repair of upstream boltons #348; only the copied module changes."""

from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "upstream" / "cacheutils.py"
OLD = "            else:\n                link[VALUE] = value\n"
NEW = OLD + "                super(LRI, self).__setitem__(key, value)\n"


def make_candidate(destination: Path) -> Path:
    destination = Path(destination)
    source = SOURCE.read_text(encoding="utf-8")
    if source.count(OLD) != 1:
        raise ValueError("Unexpected pinned LRI __setitem__ source")
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / "cacheutils.py"
    target.write_text(source.replace(OLD, NEW), encoding="utf-8")
    return target
