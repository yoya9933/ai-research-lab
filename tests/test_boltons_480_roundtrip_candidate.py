"""Verify secondary, explicitly nonblind FilePerms candidate on 512 inputs."""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.boltons_480.patch import make_candidate as make_first
from benchmarks.bugs.boltons_480.patch_roundtrip import make_candidate as make_second
from benchmarks.bugs.boltons_480.reproduce import observe as permissions
from benchmarks.bugs.boltons_480.roundtrip import observe as roundtrips


class BoltonsFromIntSecondaryCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        try:
            root = Path(cls.temp.name)
            first = make_first(root / "first")
            second = make_second(root / "second")
            cls.previous = roundtrips(first)
            cls.corrected = roundtrips(second)
            cls.first_permissions = permissions(first)
            cls.second_permissions = permissions(second)
        except BaseException:
            cls.temp.cleanup()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_all_512_modes_roundtrip(self):
        self.assertEqual(self.corrected, list(range(0o1000)))

    def test_exactly_63_bad_modes_change_and_449_controls_stay(self):
        self.assertEqual(len(self.previous), 0o1000)
        changed = [
            mode for mode, (before, after) in
            enumerate(zip(self.previous, self.corrected)) if before != after
        ]
        self.assertEqual(changed, list(range(1, 0o100)))

    def test_previous_permission_candidate_outputs_unchanged(self):
        self.assertEqual(self.second_permissions, self.first_permissions)


if __name__ == "__main__":
    unittest.main()
