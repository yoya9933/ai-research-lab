"""Same inputs as historical baseline; compare corrected and unchanged outputs."""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.tokenize_rt_33.patch import make_candidate
from benchmarks.bugs.tokenize_rt_33.reproduce import observe
from tests.test_tokenize_rt_33 import BASELINE

CORRECTED = {
    "number_without_eol": {"newline": [1, 1, ""], "roundtrip": True},
    "assignment_without_eol": {"newline": [1, 3, ""], "roundtrip": True},
    "unicode_without_eol": {"newline": [1, 4, ""], "roundtrip": True},
}


class TokenizeRt33CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = observe()
        cls.temp = tempfile.TemporaryDirectory()
        try:
            cls.candidate = observe(
                make_candidate(Path(cls.temp.name) / "patched")
            )
        except BaseException:
            cls.temp.cleanup()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_pristine_historical_baseline_is_still_reproduced(self):
        self.assertEqual(self.original, BASELINE)

    def test_three_incorrect_no_eol_offsets_are_corrected(self):
        for key, expected in CORRECTED.items():
            with self.subTest(case=key):
                self.assertNotEqual(self.original[key], expected)
                self.assertEqual(self.candidate[key], expected)

    def test_three_eol_controls_are_unchanged(self):
        self.assertEqual(self.candidate.keys(), BASELINE.keys())
        for key, expected in BASELINE.items():
            if key not in CORRECTED:
                with self.subTest(case=key):
                    self.assertEqual(self.candidate[key], expected)

    def test_exactly_reported_offsets_change(self):
        changed = {
            key for key in BASELINE
            if self.candidate[key] != self.original[key]
        }
        self.assertEqual(changed, set(CORRECTED))
        self.assertEqual(len(changed), 3)


if __name__ == "__main__":
    unittest.main()
