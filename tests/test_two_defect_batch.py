"""Two externally reported, nonblind defects; same inputs on original/candidate."""
import ast
from collections.abc import Sequence
from functools import cached_property, partial
from itertools import count, takewhile
from operator import gt, lt
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from benchmarks.bugs.boltons_348.patch import make_candidate as boltons_candidate
from benchmarks.bugs.more_itertools_1214.patch import make_candidate as range_candidate

ROOT = Path(__file__).resolve().parents[1] / "benchmarks" / "bugs"


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def observe_lru(path):
    module = load_module(path, "replay_cacheutils")
    result = {}
    for typ in (module.LRU, module.LRI):
        cache = typ(max_size=2)
        cache["a"] = 1
        cache["b"] = 2
        cache["a"] = 200
        result[typ.__name__] = {
            "getitem": cache["a"],
            "dict": dict(cache)["a"],
            "values": dict(cache).get("a"),
        }
        before = set(cache)
        cache["c"] = 3
        after = set(cache)
        result[typ.__name__].update({
            "eviction": sorted(before - after),
            "remaining": sorted(after),
            "size": len(cache),
            "new": cache["c"],
        })
    return result


def load_pristine_numeric_range(path):
    """Execute the upstream class AST with only its needed stdlib imports.

    The pristine more.py is not a standalone module (it imports .recipes).
    This is a constrained class replay, not a full upstream package test.
    """
    source = path.read_text(encoding="utf-8")
    classes = [
        node for node in ast.parse(source, filename=str(path)).body
        if isinstance(node, ast.ClassDef) and node.name == "numeric_range"
    ]
    if len(classes) != 1:
        raise ValueError("Expected exactly one pinned upstream numeric_range class")
    namespace = {
        "__name__": "pinned_more_itertools_class",
        "Sequence": Sequence,
        "cached_property": cached_property,
        "partial": partial,
        "count": count,
        "takewhile": takewhile,
        "gt": gt,
        "lt": lt,
    }
    exec(compile(ast.Module(body=classes, type_ignores=[]), str(path), "exec"), namespace)
    return namespace["numeric_range"]


def observe_range(R):
    pairs = [
        (R(2, 3, 1), R(2, 3, 5)),
        (R(1, 2, 1), R(1, 2, 6)),
        (R(0, 1, 1), R(0, 1, 3)),
        (R(0, 2, 1), R(0, 2, 2)),
        (R(3, 3, 1), R(10, 10, 4)),
    ]
    return [
        {"left": list(a), "right": list(b), "equal": a == b,
         "hash_equal": hash(a) == hash(b)} for a, b in pairs
    ]


class TwoDefectBatchTests(unittest.TestCase):
    def test_boltons_original_fails_and_candidate_corrects(self):
        source = ROOT / "boltons_348" / "upstream" / "cacheutils.py"
        original = observe_lru(source)
        with TemporaryDirectory() as tmp:
            fixed = observe_lru(boltons_candidate(Path(tmp) / "fixed"))
        for typ in ("LRU", "LRI"):
            with self.subTest(type=typ):
                self.assertEqual(original[typ]["getitem"], 200)
                self.assertEqual(original[typ]["dict"], 1)
                self.assertEqual(fixed[typ]["dict"], 200)
                self.assertEqual(fixed[typ]["values"], 200)
                self.assertEqual(fixed[typ]["getitem"], 200)
                self.assertEqual(original[typ]["size"], 2)
                self.assertEqual(fixed[typ]["size"], 2)
                self.assertEqual(fixed[typ]["new"], 3)
                # The overflow insertion must evict b, not a or the new c.
                for observed in (original[typ], fixed[typ]):
                    self.assertEqual(observed["eviction"], ["b"])
                    self.assertEqual(observed["remaining"], ["a", "c"])

    def test_numeric_range_original_fails_and_candidate_corrects(self):
        source = ROOT / "more_itertools_1214" / "upstream" / "more_itertools" / "more.py"
        original = observe_range(load_pristine_numeric_range(source))
        with TemporaryDirectory() as tmp:
            fixed = observe_range(
                load_module(range_candidate(Path(tmp) / "fixed"), "fixed_numeric_range").numeric_range
            )
        self.assertEqual([x["equal"] for x in original], [False, False, False, False, True])
        self.assertEqual([x["equal"] for x in fixed], [True, True, True, False, True])
        for item in fixed[:3]:
            self.assertTrue(item["hash_equal"])
            self.assertEqual(item["left"], item["right"])
        for i in (3, 4):
            self.assertEqual(original[i], fixed[i])

    def test_nonblind_negative_controls(self):
        source = ROOT / "more_itertools_1214" / "upstream" / "more_itertools" / "more.py"
        R = load_pristine_numeric_range(source)
        self.assertNotEqual(R(0, 2, 1), R(0, 2, 2))
        self.assertEqual(R(0, 0), R(20, 20, 5))


if __name__ == "__main__":
    unittest.main()
