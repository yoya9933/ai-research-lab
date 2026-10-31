"""Verify the same rotation observations after a local, unblinded repair."""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.boltons_479.patch import make_candidate
from benchmarks.bugs.boltons_479.reproduce import observe
from tests.test_boltons_479 import BASELINE

CORRECTED = {
    "keep_one_names": ["f.1.txt"],
    "keep_one_data": "CRITICAL DATA",
    "keep_five_names": [
        "f.1.txt", "f.2.txt", "f.3.txt", "f.4.txt", "f.5.txt"
    ],
    "keep_five_data": ["current", "gen 1", "gen 2", "gen 3", "gen 4"],
}


class Boltons479CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = observe()
        cls.temp = tempfile.TemporaryDirectory()
        try:
            cls.candidate = observe(make_candidate(Path(cls.temp.name) / "patched"))
        except BaseException:
            cls.temp.cleanup()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_pristine_source_still_reproduces_report(self):
        self.assertEqual(self.baseline, BASELINE)

    def test_data_is_retained_at_requested_generation_count(self):
        for key, expected in CORRECTED.items():
            with self.subTest(case=key):
                self.assertNotEqual(self.baseline[key], expected)
                self.assertEqual(self.candidate[key], expected)

    def test_all_five_controls_are_unchanged(self):
        self.assertEqual(self.candidate.keys(), BASELINE.keys())
        for key, expected in BASELINE.items():
            if key not in CORRECTED:
                with self.subTest(case=key):
                    self.assertEqual(self.candidate[key], expected)

    def test_only_four_reported_outputs_change(self):
        changed = {
            key for key in BASELINE
            if self.candidate[key] != self.baseline[key]
        }
        self.assertEqual(changed, set(CORRECTED))
        self.assertEqual(len(changed), 4)


if __name__ == "__main__":
    unittest.main()
