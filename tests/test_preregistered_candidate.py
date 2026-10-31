"""Smoke checks derived from published instructions, not hidden test files."""

import unittest

from benchmarks.exercism.trial_002.attempt_002.luhn import Luhn
from benchmarks.exercism.trial_002.attempt_002.pangram import is_pangram
from benchmarks.exercism.trial_002.attempt_002.armstrong_numbers import is_armstrong_number


class PreregisteredCandidateTests(unittest.TestCase):
    def test_luhn_instruction_examples(self):
        self.assertTrue(Luhn("4539 3195 0343 6467").valid())
        self.assertFalse(Luhn("066 123 478").valid())

    def test_pangram_obvious_examples(self):
        self.assertTrue(is_pangram("The quick brown fox jumps over the lazy dog"))
        self.assertFalse(is_pangram("abcdefghijklmnopqrstuvwxyz"[:-1]))

    def test_armstrong_instruction_examples(self):
        self.assertTrue(is_armstrong_number(153))
        self.assertFalse(is_armstrong_number(154))


if __name__ == "__main__":
    unittest.main()
