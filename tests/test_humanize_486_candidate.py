"""Compare the same 15 ordinal observations before and after the local patch."""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.humanize_486.patch import make_candidate
from benchmarks.bugs.humanize_486.reproduce import observe
from tests.test_humanize_486 import BASELINE

CORRECTED = {
    "minus_one": "-1st",
    "minus_two": "-2nd",
    "minus_three": "-3rd",
    "minus_twenty_one": "-21st",
    "minus_hundred_one": "-101st",
    "negative_string": "-21st",
    "negative_female": "-1st",
}


class Humanize486CandidateTests(unittest.TestCase):
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

    def test_source_baseline_is_unchanged(self):
        self.assertEqual(self.baseline, BASELINE)

    def test_reported_negative_cases_are_corrected(self):
        for key, expected in CORRECTED.items():
            with self.subTest(case=key):
                self.assertNotEqual(self.baseline[key], expected)
                self.assertEqual(self.candidate[key], expected)

    def test_all_other_observations_are_unchanged(self):
        self.assertEqual(self.candidate.keys(), BASELINE.keys())
        for key, expected in BASELINE.items():
            if key not in CORRECTED:
                with self.subTest(case=key):
                    self.assertEqual(self.candidate[key], expected)

    def test_change_counts(self):
        changed = {key for key in BASELINE if self.candidate[key] != self.baseline[key]}
        self.assertEqual(changed, set(CORRECTED))
        self.assertEqual(len(changed), 7)


if __name__ == "__main__":
    unittest.main()
