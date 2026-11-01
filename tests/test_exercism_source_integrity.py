"""Verify the external Exercism starters, tests and license are upstream bytes.

All SHA-1 Git blob IDs were checked against exercism/python at the pinned commit.
The test runs offline, without importing or changing third-party fixtures.
"""

from hashlib import sha1
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from benchmarks.exercism.runner import UPSTREAM_SHA

ROOT = Path(__file__).resolve().parents[1] / "benchmarks" / "exercism"
ORIGINAL_COMMIT = "6105f6d9d3ef66ce3d5c8f529d2882af3d76b706"

UPSTREAM_BLOBS = {
    "LICENSE": "90e73be03b5e239275cce1821bbd742e63a502a3",
    "starter/isogram.py": "3cd2ad82b2888a70bf0711e3e5f1271e60aae07f",
    "starter/rna_transcription.py": "bb7be7795daaab1f866c9291a1338fc2bd03a6a9",
    "starter/difference_of_squares.py": "2b2ec944808ac1f1bb853c414a3b11743cc09b48",
    "tests/isogram_test.py": "c65984f6e6448f375b76c0a841c49147f6ccb971",
    "tests/rna_transcription_test.py": "766f20299e21906a0483684c7faeca1b29f07c06",
    "tests/difference_of_squares_test.py": "3536a20f8f8f8a4c87e226ce9597f0418de5c449",
    "trial_002/starter/luhn.py": "8675eaa85e48a2aef5287e2f781d00283d74ea20",
    "trial_002/starter/pangram.py": "5377191ef56fe59689dbd8d22d192d5c4368f25c",
    "trial_002/starter/armstrong_numbers.py": "b8829fac575b993a090aaa897b5cdb31644c1f2d",
    "trial_002/tests/luhn_test.py": "7d26c9ae02f830f83e934e26468fe0f09f341e38",
    "trial_002/tests/pangram_test.py": "09e303d44075af3b4ee28ac915653cc8c622329d",
    "trial_002/tests/armstrong_numbers_test.py": "402476671dbad5a4df4220057b56b730bb8f707d",
}


def fixture_python_files(root):
    directories = ("starter", "tests", "trial_002/starter", "trial_002/tests")
    return {
        str(path.relative_to(root))
        for directory in directories
        for path in (root / directory).rglob("*.py")
    }


class ExercismSourceIntegrityTests(unittest.TestCase):
    def test_external_python_file_inventory_is_exact(self):
        pinned = {path for path in UPSTREAM_BLOBS if path.endswith(".py")}
        self.assertEqual(fixture_python_files(ROOT), pinned)

    def test_inventory_notices_unlisted_nested_test_module(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            extra = root / "tests" / "nested" / "unlisted_test.py"
            extra.parent.mkdir(parents=True)
            extra.write_text("def test_unlisted(): pass\n", encoding="utf-8")
            self.assertEqual(
                fixture_python_files(root), {"tests/nested/unlisted_test.py"}
            )

    def test_all_external_benchmark_source_blobs_are_unchanged(self):
        self.assertEqual(UPSTREAM_SHA, ORIGINAL_COMMIT)
        for name, expected_sha in UPSTREAM_BLOBS.items():
            with self.subTest(file=name):
                content = (ROOT / name).read_bytes()
                header = f"blob {len(content)}\0".encode("ascii")
                self.assertEqual(sha1(header + content).hexdigest(), expected_sha)


if __name__ == "__main__":
    unittest.main()
