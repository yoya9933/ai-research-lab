"""Independently authored post-freeze samples; do not rewrite frozen candidate."""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.tokenize_rt_33.followup import (
    EXPECTED_OFFSETS,
    NEW_NO_EOL,
    observe,
)
from benchmarks.bugs.tokenize_rt_33.patch import make_candidate


class TokenizeRtPostfreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = observe()
        cls.temp = tempfile.TemporaryDirectory()
        try:
            cls.candidate = observe(
                make_candidate(Path(cls.temp.name) / "patched")
            )
        except BaseException:
            cls.temp.cleanup()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_all_expected_offsets_for_frozen_candidate(self):
        self.assertEqual(self.candidate.keys(), EXPECTED_OFFSETS.keys())
        for name, expected in EXPECTED_OFFSETS.items():
            with self.subTest(case=name):
                self.assertEqual(self.candidate[name]["offset"], expected)

    def test_pinned_source_exposes_additional_no_eol_offsets(self):
        for name in NEW_NO_EOL:
            with self.subTest(case=name):
                self.assertEqual(self.original[name]["offset"], 0)

    def test_eol_and_empty_controls_do_not_change(self):
        for name in EXPECTED_OFFSETS:
            if name not in NEW_NO_EOL:
                with self.subTest(case=name):
                    self.assertEqual(self.candidate[name], self.original[name])

    def test_roundtrip_status_does_not_regress_or_get_hidden(self):
        # Keep residual upstream roundtrip failures visible in the CI JSON.
        for name in EXPECTED_OFFSETS:
            with self.subTest(case=name):
                self.assertEqual(
                    self.candidate[name]["roundtrip"],
                    self.original[name]["roundtrip"],
                )

    def test_exactly_four_postfreeze_offsets_are_corrected(self):
        changed = {
            name for name in EXPECTED_OFFSETS
            if self.candidate[name]["offset"] != self.original[name]["offset"]
        }
        self.assertEqual(changed, set(NEW_NO_EOL))


if __name__ == "__main__":
    unittest.main()
