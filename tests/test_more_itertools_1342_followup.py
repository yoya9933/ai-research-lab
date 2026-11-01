"""Specification-based, post-freeze checks on 372 deterministic input pairs."""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.more_itertools_1342.followup import observe
from benchmarks.bugs.more_itertools_1342.patch import make_candidate


class MoreItertools1342FollowupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        try:
            cls.before = observe()
            cls.after = observe(make_candidate(Path(cls.temp.name) / "patched"))
        except BaseException:
            cls.temp.cleanup()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_domain_and_stable_inputs(self):
        self.assertEqual(len(self.before), 372)
        self.assertEqual(len(self.after), 372)
        expected = [(length, size) for length in range(31) for size in range(-3, 9)]
        self.assertEqual(
            [(case["length"], case["size"]) for case in self.before], expected
        )
        self.assertEqual(
            [(case["length"], case["size"]) for case in self.after], expected
        )

    def test_248_positive_inputs_are_unchanged(self):
        controls = 0
        for baseline, candidate in zip(self.before, self.after):
            if candidate["size"] <= 0:
                continue
            controls += 1
            with self.subTest(length=candidate["length"], size=candidate["size"]):
                self.assertEqual(candidate, baseline)
        self.assertEqual(controls, 248)

    def test_248_positive_inputs_obey_chunk_invariants(self):
        validated = 0
        for case in self.after:
            size, length = case["size"], case["length"]
            if size <= 0:
                continue
            validated += 1
            with self.subTest(length=length, size=size):
                self.assertNotIn("error", case)
                self.assertEqual(case["remaining"], [])
                chunks = case["chunks"]
                self.assertEqual([item for chunk in chunks for item in chunk],
                                 list(range(length)))
                self.assertEqual(len(chunks), (length + size - 1) // size)
                lengths = [len(chunk) for chunk in chunks]
                if lengths:
                    self.assertTrue(all(1 <= count <= size for count in lengths))
                    self.assertLessEqual(max(lengths) - min(lengths), 1)
        self.assertEqual(validated, 248)

    def test_31_zero_sizes_do_not_consume(self):
        validated = 0
        for case in self.after:
            if case["size"] != 0:
                continue
            validated += 1
            with self.subTest(length=case["length"]):
                self.assertNotIn("error", case)
                self.assertEqual(case["chunks"], [])
                self.assertEqual(case["remaining"], list(range(case["length"])))
        self.assertEqual(validated, 31)

    def test_93_negative_sizes_reject_without_consuming(self):
        validated = 0
        for case in self.after:
            if case["size"] >= 0:
                continue
            validated += 1
            with self.subTest(length=case["length"], size=case["size"]):
                self.assertEqual(case["error"], "ValueError")
                self.assertEqual(case["message"], "n must be at least 0")
                self.assertEqual(case["remaining"], list(range(case["length"])))
        self.assertEqual(validated, 93)


if __name__ == "__main__":
    unittest.main()
