"""Green baseline tests demonstrate the reported rotation data loss."""

import unittest

from benchmarks.bugs.boltons_479.reproduce import observe

BASELINE = {
    "keep_one_names": [],
    "keep_one_data": None,
    "keep_five_names": ["f.1.txt", "f.2.txt", "f.3.txt", "f.4.txt"],
    "keep_five_data": ["current", "gen 1", "gen 2", "gen 3"],
    "fresh_two_names": ["f.1.txt"],
    "fresh_two_data": "single",
    "missing_unchanged": ["f.1.txt"],
    "invalid_keep": "ValueError",
    "directory_error": "ValueError",
}


class Boltons479BaselineTests(unittest.TestCase):
    def test_observed_historical_bug_and_controls(self):
        actual = observe()
        self.assertEqual(actual.keys(), BASELINE.keys())
        for key, expected in BASELINE.items():
            with self.subTest(case=key):
                self.assertEqual(actual[key], expected)


if __name__ == "__main__":
    unittest.main()
