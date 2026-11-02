"""Pin pristine upstream sources separately from derived replay and candidates."""
import ast
from hashlib import sha1
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "benchmarks/bugs/boltons_348/upstream/cacheutils.py":
        "27a19cb9e63b41663d7ad500c67a0485d55ade13",
    "benchmarks/bugs/boltons_348/LICENSE":
        "6a4c9d2496f53c61c99ae7c113e6ed94b15b038c",
    # This is the pristine, complete module from upstream at the pinned commit.
    "benchmarks/bugs/more_itertools_1214/upstream/more_itertools/more.py":
        "7ce276ac417426a419e84d31fe73e4681e81f973",
    # The historical standalone replay was derived by minimizing imports.
    "benchmarks/bugs/more_itertools_1214/upstream/numeric_range.py":
        "e207d3e6742042c39f88a617c7e665788ce255c6",
    "benchmarks/bugs/more_itertools_1214/LICENSE":
        "0a523bece3e50519653c4d7a38399baa487fefa1",
}


class BatchSourceIntegrityTests(unittest.TestCase):
    def test_original_sources_and_licenses_stay_frozen(self):
        for rel, expected in SOURCES.items():
            with self.subTest(path=rel):
                content = (ROOT / rel).read_bytes()
                self.assertEqual(
                    sha1(f"blob {len(content)}\0".encode() + content).hexdigest(),
                    expected,
                )

    def test_pristine_numeric_range_class_matches_standalone_replay(self):
        case = ROOT / "benchmarks" / "bugs" / "more_itertools_1214" / "upstream"
        pristine = case / "more_itertools" / "more.py"
        replay = case / "numeric_range.py"

        def class_source(path):
            source = path.read_text(encoding="utf-8")
            classes = [
                node for node in ast.parse(source, filename=str(path)).body
                if isinstance(node, ast.ClassDef) and node.name == "numeric_range"
            ]
            self.assertEqual(len(classes), 1)
            return ast.get_source_segment(source, classes[0])

        # Same exact class text, but distinct import context and file provenance.
        self.assertEqual(class_source(pristine), class_source(replay))


if __name__ == "__main__":
    unittest.main()
