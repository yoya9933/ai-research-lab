"""Deterministic property checks with independently specified expected behavior."""

import math
import unittest

from lab import attempt_001, buggy


class RepairedFunctionProperties(unittest.TestCase):
    def test_clamp_on_147_boundaries_and_intervals(self):
        buggy_failures = 0
        for low in range(-5, 6, 2):
            for high in range(low, 6, 2):
                for value in range(-9, 10, 3):
                    expected = low if value < low else high if value > high else value
                    with self.subTest(low=low, high=high, value=value):
                        self.assertEqual(attempt_001.clamp(value, low, high), expected)
                    buggy_failures += buggy.clamp(value, low, high) != expected
        self.assertGreater(buggy_failures, 0)

    def test_chunk_partition_for_248_input_size_pairs(self):
        buggy_failures = 0
        for length in range(31):
            items = list(range(length))
            for size in range(1, 9):
                parts = attempt_001.chunks(items, size)
                with self.subTest(length=length, size=size):
                    self.assertEqual([x for group in parts for x in group], items)
                    self.assertEqual(
                        [len(group) for group in parts],
                        [size] * (length // size) + ([length % size] if length % size else []),
                    )
                bad_parts = buggy.chunks(items, size)
                buggy_failures += [x for group in bad_parts for x in group] != items
        self.assertGreater(buggy_failures, 0)

    def test_factorial_matches_standard_library_for_16_inputs(self):
        buggy_failures = 0
        for n in range(16):
            expected = math.factorial(n)
            with self.subTest(n=n):
                self.assertEqual(attempt_001.factorial(n), expected)
            buggy_failures += buggy.factorial(n) != expected
        self.assertGreater(buggy_failures, 0)


if __name__ == "__main__":
    unittest.main()
