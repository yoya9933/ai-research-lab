"""Reproduce a historically reported third-party defect on unfixed upstream code."""

import unittest

from benchmarks.bugs.humanize_30.reproduce import observe


class HumanizeIssue30Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.observed = observe()

    def test_original_user_report_is_reproduced(self):
        self.assertEqual(self.observed["round_minutes"], "8 hours and 60 minutes")

    def test_related_plural_artifact_is_reproduced(self):
        self.assertEqual(self.observed["round_hours"], "1 day and 1 hours")

    def test_independent_issue_20_report_is_reproduced(self):
        self.assertEqual(self.observed["singular_minute"], "1 hour and 1 minutes")

    def test_default_precision_is_unchanged(self):
        self.assertEqual(self.observed["default"], "8 hours, 59 minutes and 59 seconds")

    def test_fractional_format_without_rounding(self):
        self.assertEqual(self.observed["fractional"], "8 hours and 59.98 minutes")


if __name__ == "__main__":
    unittest.main()
