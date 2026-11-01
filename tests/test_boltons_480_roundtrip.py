"""Document a post-freeze, investigator-authored defect without claiming repair."""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.boltons_480.patch import make_candidate
from benchmarks.bugs.boltons_480.roundtrip import observe


class BoltonsFromIntPostfreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = observe()
        with tempfile.TemporaryDirectory() as directory:
            cls.frozen_candidate = observe(make_candidate(Path(directory) / "patched"))

    def test_entire_nine_bit_mode_domain_is_recorded(self):
        self.assertEqual(len(self.baseline), 0o1000)
        self.assertEqual(len(self.frozen_candidate), 0o1000)

    def test_original_misplaces_every_leading_zero_mode_except_zero(self):
        failures = [mode for mode, actual in enumerate(self.baseline)
                    if actual != mode]
        self.assertEqual(failures, list(range(1, 0o100)))
        self.assertEqual(self.baseline[0o007], 0o700)
        self.assertEqual(self.baseline[0o040], 0o400)
        self.assertEqual(self.baseline[0o644], 0o644)

    def test_earlier_frozen_permission_patch_does_not_fix_from_int(self):
        self.assertEqual(self.frozen_candidate, self.baseline)


if __name__ == "__main__":
    unittest.main()
