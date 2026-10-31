"""Check the same nine observations against a separate FilePerms candidate."""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.boltons_480.patch import make_candidate
from benchmarks.bugs.boltons_480.reproduce import observe
from tests.test_boltons_480 import BASELINE

CORRECTED = {
    "after_revoke_other": "0o640",
    "after_revoke_group": "0o600",
    "chmod_mode": "0o600",
}


class Boltons480CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = observe()
        cls.temp = tempfile.TemporaryDirectory()
        try:
            cls.candidate = observe(make_candidate(Path(cls.temp.name) / "patched"))
        except BaseException:
            cls.temp.cleanup()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_pinned_baseline_stays_defective(self):
        self.assertEqual(self.baseline, BASELINE)

    def test_permission_revocations_change_correctly(self):
        for name, expected in CORRECTED.items():
            with self.subTest(case=name):
                self.assertNotEqual(self.baseline[name], expected)
                self.assertEqual(self.candidate[name], expected)

    def test_all_six_controls_remain_unchanged(self):
        self.assertEqual(self.candidate.keys(), BASELINE.keys())
        for name, expected in BASELINE.items():
            if name not in CORRECTED:
                with self.subTest(case=name):
                    self.assertEqual(self.candidate[name], expected)

    def test_exactly_three_outputs_change(self):
        changed = {
            key for key in BASELINE
            if self.candidate[key] != self.baseline[key]
        }
        self.assertEqual(changed, set(CORRECTED))
        self.assertEqual(len(changed), 3)


if __name__ == "__main__":
    unittest.main()
