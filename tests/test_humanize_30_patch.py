"""Check a chat-authored repair against a pinned real-world upstream defect."""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.humanize_30.patch import make_candidate
from benchmarks.bugs.humanize_30.reproduce import VENDOR, observe


class HumanizeIssue30RepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        directory = tempfile.TemporaryDirectory()
        cls.addClassCleanup(directory.cleanup)
        cls.candidate_path = make_candidate(Path(directory.name) / "candidate")
        cls.candidate = observe(cls.candidate_path)

    def test_rounding_carries_minutes_into_hours(self):
        self.assertEqual(self.candidate["round_minutes"], "9 hours")

    def test_rounded_hour_uses_singular_noun(self):
        self.assertEqual(self.candidate["round_hours"], "1 day and 1 hour")

    def test_related_issue_20_plural_regression(self):
        self.assertEqual(self.candidate["singular_minute"], "1 hour and 1 minute")

    def test_default_precision_is_preserved(self):
        self.assertEqual(self.candidate["default"], "8 hours, 59 minutes and 59 seconds")

    def test_fractional_minutes_are_preserved(self):
        self.assertEqual(self.candidate["fractional"], "8 hours and 59.98 minutes")

    def test_original_source_remains_unmodified(self):
        baseline = observe(VENDOR)
        self.assertEqual(baseline["round_minutes"], "8 hours and 60 minutes")
        self.assertNotEqual(self.candidate_path, VENDOR)

    def test_candidate_modifies_only_time_module(self):
        files = ["__init__.py", "i18n.py", "number.py", "filesize.py", "lists.py", "_version.py"]
        for name in files:
            self.assertEqual(
                (VENDOR / "humanize" / name).read_bytes(),
                (self.candidate_path / "humanize" / name).read_bytes(),
                name,
            )


if __name__ == "__main__":
    unittest.main()
