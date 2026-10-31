"""Preserve original candidate while testing a supplemental roundtrip repair."""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.tokenize_rt_33.followup import EXPECTED_OFFSETS, observe
from benchmarks.bugs.tokenize_rt_33.patch import make_candidate
from benchmarks.bugs.tokenize_rt_33.patch_roundtrip import (
    make_candidate_with_roundtrip,
)

RESIDUAL = {"trailing_space", "unicode_space"}


class TokenizeRtRoundtripTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        try:
            root = Path(cls.temp.name)
            cls.original = observe()
            cls.first = observe(make_candidate(root / "first"))
            cls.second = observe(make_candidate_with_roundtrip(root / "second"))
        except BaseException:
            cls.temp.cleanup()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_initial_candidate_still_shows_original_roundtrip_failures(self):
        for case in RESIDUAL:
            with self.subTest(case=case):
                self.assertFalse(self.original[case]["roundtrip"])
                self.assertFalse(self.first[case]["roundtrip"])

    def test_second_candidate_preserves_all_seven_offset_results(self):
        self.assertEqual(self.second.keys(), EXPECTED_OFFSETS.keys())
        for case, offset in EXPECTED_OFFSETS.items():
            with self.subTest(case=case):
                self.assertEqual(self.first[case]["offset"], offset)
                self.assertEqual(self.second[case]["offset"], offset)

    def test_trailing_space_roundtrips_are_repaired(self):
        for case in RESIDUAL:
            with self.subTest(case=case):
                self.assertTrue(self.second[case]["roundtrip"])

    def test_other_five_observations_are_unmodified(self):
        for case in EXPECTED_OFFSETS:
            if case not in RESIDUAL:
                with self.subTest(case=case):
                    self.assertEqual(self.second[case], self.first[case])

    def test_exactly_two_roundtrip_statuses_change(self):
        changed = {
            case for case in EXPECTED_OFFSETS
            if self.second[case]["roundtrip"] != self.first[case]["roundtrip"]
        }
        self.assertEqual(changed, RESIDUAL)


if __name__ == "__main__":
    unittest.main()
