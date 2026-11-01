"""Pin two upstream source snapshots and isolate original from candidate code."""
from hashlib import sha1
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "benchmarks/bugs/boltons_348/upstream/cacheutils.py":
        "27a19cb9e63b41663d7ad500c67a0485d55ade13",
    "benchmarks/bugs/boltons_348/LICENSE":
        "6a4c9d2496f53c61c99ae7c113e6ed94b15b038c",
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


if __name__ == "__main__":
    unittest.main()
