"""Assert the historical negative-ordinal bug, not a claimed repair."""

import unittest

from benchmarks.bugs.humanize_486.reproduce import observe

BASELINE = {
    "minus_one": "-1th",
    "minus_two": "-2th",
    "minus_three": "-3th",
    "minus_twenty_one": "-21th",
    "minus_hundred_one": "-101th",
    "minus_eleven": "-11th",
    "minus_twelve": "-12th",
    "minus_thirteen": "-13th",
    "positive_one": "1st",
    "positive_twenty_one": "21st",
    "positive_111": "111th",
    "zero": "0th",
    "invalid": "bogus",
    "negative_string": "-21th",
    "negative_female": "-1th",
}


class Humanize486BaselineTests(unittest.TestCase):
    def test_pinned_original_behavior(self):
        actual = observe()
        self.assertEqual(actual.keys(), BASELINE.keys())
        for key, expected in BASELINE.items():
            with self.subTest(case=key):
                self.assertEqual(actual[key], expected)


if __name__ == "__main__":
    unittest.main()
