"""Verify candidate behavior against immutable, externally reported baseline."""

import tempfile
from pathlib import Path
import unittest

from benchmarks.bugs.humanize_333.patch import make_candidate
from benchmarks.bugs.humanize_333.reproduce import observe


class Humanize333CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.observed = observe(make_candidate(Path(cls.tmp.name) / "patched"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_both_infinities_are_text(self):
        self.assertEqual(self.observed["positive_inf"], {"value": "inf"})
        self.assertEqual(self.observed["negative_inf"], {"value": "-inf"})

    def test_previous_controls_remain_unchanged(self):
        self.assertEqual(self.observed["nan"], {"value": "nan"})
        self.assertEqual(self.observed["finite"], {"value": "30 seconds"})
        self.assertEqual(self.observed["invalid"], {"value": "bogus"})

    def test_oversized_finite_input_still_raises(self):
        self.assertEqual(self.observed["too_large"], {"error": "OverflowError"})


if __name__ == "__main__":
    unittest.main()
