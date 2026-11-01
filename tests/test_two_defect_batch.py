"""Two externally reported, nonblind defects; same inputs on original/candidate."""
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
            "eviction": sorted(cache.keys()),
        }
        cache["c"] = 3
        result[typ.__name__]["size"] = len(cache)
        result[typ.__name__]["new"] = cache["c"]
    return result


def observe_range(path):
    R = load_module(path, "replay_numeric_range").numeric_range
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
                self.assertEqual(fixed[typ]["size"], 2)
                self.assertEqual(fixed[typ]["new"], 3)
                self.assertEqual(fixed[typ]["eviction"], original[typ]["eviction"])

    def test_numeric_range_original_fails_and_candidate_corrects(self):
        source = ROOT / "more_itertools_1214" / "upstream" / "numeric_range.py"
        original = observe_range(source)
        with TemporaryDirectory() as tmp:
            fixed = observe_range(range_candidate(Path(tmp) / "fixed"))
        self.assertEqual([x["equal"] for x in original], [False, False, False, False, True])
        self.assertEqual([x["equal"] for x in fixed], [True, True, True, False, True])
        for item in fixed[:3]:
            self.assertTrue(item["hash_equal"])
            self.assertEqual(item["left"], item["right"])
        for i in (3, 4):
            self.assertEqual(original[i], fixed[i])

    def test_nonblind_negative_controls(self):
        source = ROOT / "more_itertools_1214" / "upstream" / "numeric_range.py"
        R = load_module(source, "range_negative_controls").numeric_range
        self.assertNotEqual(R(0, 2, 1), R(0, 2, 2))
        self.assertEqual(R(0, 0), R(20, 20, 5))


if __name__ == "__main__":
    unittest.main()
