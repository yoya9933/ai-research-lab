"""Compare the same seven pinned regex-optimizer observations before and after."""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.pygments_3190.patch import make_candidate
from benchmarks.bugs.pygments_3190.reproduce import observe
from tests.test_pygments_3190 import PROBLEM_CASES, CONTROLS


class Pygments3190CandidateTests(unittest.TestCase):
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

    def test_three_duplicate_inputs_are_canonical(self):
        for key in PROBLEM_CASES:
            with self.subTest(case=key):
                before, after = self.baseline[key], self.candidate[key]
                self.assertFalse(before["same_as_unique"])
                self.assertTrue(after["same_as_unique"])
                self.assertEqual(after["pattern"], before["unique_pattern"])
                self.assertEqual(after["matched"], before["matched"])
                self.assertEqual(after["words"], before["words"])

    def test_all_four_unique_input_controls_unchanged(self):
        self.assertEqual(self.candidate.keys(), self.baseline.keys())
        for key in CONTROLS:
            with self.subTest(case=key):
                self.assertEqual(self.candidate[key], self.baseline[key])

    def test_exactly_three_results_change(self):
        changed = {
            key for key in self.baseline
            if self.baseline[key] != self.candidate[key]
        }
        self.assertEqual(changed, set(PROBLEM_CASES))
        self.assertEqual(len(changed), 3)


if __name__ == "__main__":
    unittest.main()
