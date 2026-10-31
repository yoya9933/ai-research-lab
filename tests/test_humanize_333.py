"""Verify the historic bug exists; these tests do not claim a repair."""

import unittest

from benchmarks.bugs.humanize_333.reproduce import observe


class HumanizeIssue333BaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = observe()

    def test_reported_positive_infinity_raises(self):
        self.assertEqual(self.results["positive_inf"], {"error": "OverflowError"})

    def test_negative_infinity_also_raises(self):
        self.assertEqual(self.results["negative_inf"], {"error": "OverflowError"})

    def test_nan_is_already_handled(self):
        self.assertEqual(self.results["nan"], {"value": "nan"})

    def test_finite_value_still_converts(self):
        self.assertEqual(self.results["finite"], {"value": "30 seconds"})

    def test_non_numeric_text_remains_text(self):
        self.assertEqual(self.results["invalid"], {"value": "bogus"})

    def test_oversized_finite_duration_raises(self):
        self.assertEqual(self.results["too_large"], {"error": "OverflowError"})


if __name__ == "__main__":
    unittest.main()
