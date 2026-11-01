"""Post-commit bounded properties; not externally authored held-out tests."""

import unittest

from benchmarks.bugs.more_itertools_1342.followup import compare


class MoreItertools1342FollowupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = compare()

    def test_574_positive_size_cases_match_and_satisfy_properties(self):
        before = self.report["baseline"]["positive_sizes"]
        after = self.report["candidate"]["positive_sizes"]
        self.assertEqual(before, after)
        self.assertEqual(before, {"total": 574, "passed": 574, "failures": []})

    def test_ignored_source_and_negative_size_are_fixed_without_iterating(self):
        before = self.report["baseline"]["ignored_inputs"]
        after = self.report["candidate"]["ignored_inputs"]
        self.assertEqual(before, {
            "zero": {"error": "AssertionError", "message": "ignored iterable was inspected"},
            "negative": {"error": "AssertionError", "message": "ignored iterable was inspected"},
        })
        self.assertEqual(after, {
            "zero": {"chunks": []},
            "negative": {"error": "ValueError", "message": "n must be at least 0"},
        })


if __name__ == "__main__":
    unittest.main()
