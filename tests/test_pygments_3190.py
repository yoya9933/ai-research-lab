"""Historical Pygments redundant-regex baseline, not a repaired candidate."""

from hashlib import sha1
from pathlib import Path
import unittest

from benchmarks.bugs.pygments_3190.reproduce import VENDOR, observe

SOURCE_BLOB = "9010eb3fb517ff4134b4f52581179fa80b0f7540"
LICENSE_BLOB = "446a1a805c8a949579fb8a9799f2bec7777349dc"
PROBLEM_CASES = ("duplicate_single", "duplicate_suffix", "duplicate_prefix")
CONTROLS = ("unique_single", "unique_suffix", "empty", "regex_escaping")


def git_blob(content):
    return sha1(f"blob {len(content)}\0".encode("ascii") + content).hexdigest()


class Pygments3190BaselineTests(unittest.TestCase):
    def test_unmodified_source_and_license(self):
        for path, sha in (
            (VENDOR / "regexopt.py", SOURCE_BLOB),
            (VENDOR.parent / "LICENSE", LICENSE_BLOB),
        ):
            with self.subTest(path=path.name):
                self.assertEqual(git_blob(path.read_bytes()), sha)

    def test_duplicates_change_generated_pattern(self):
        data = observe()
        for key in PROBLEM_CASES:
            with self.subTest(case=key):
                self.assertFalse(data[key]["same_as_unique"])
        self.assertIn("[aab]", data["duplicate_single"]["pattern"])
        self.assertIn("[aab]", data["duplicate_suffix"]["pattern"])
        self.assertIn("[rrt]", data["duplicate_prefix"]["pattern"])

    def test_unrelated_inputs_are_unchanged(self):
        data = observe()
        for key in CONTROLS:
            with self.subTest(case=key):
                self.assertTrue(data[key]["same_as_unique"])

    def test_original_patterns_still_match_reported_words(self):
        data = observe()
        for key, sample in data.items():
            with self.subTest(case=key):
                self.assertEqual(sample["matched"], sorted(set(sample["words"])))


if __name__ == "__main__":
    unittest.main()
