"""Baseline regression: green tests mean a public defect was reproduced."""

import hashlib
import unittest

from benchmarks.bugs.boltons_480.reproduce import UPSTREAM_COMMIT, VENDOR, observe

BASELINE = {
    "initial_mode": "0o644",
    "after_revoke_other": "0o644",
    "after_revoke_group": "0o644",
    "display": "FilePerms(user='rw', group='', other='')",
    "chmod_mode": "0o644",
    "construct": "0o644",
    "widen": "0o640",
    "empty": "0o0",
    "invalid": "ValueError",
}
UPSTREAM_BLOBS = {
    "boltons/__init__.py": "374bf7d90741c988c0a67126eea3ab3928d4982c",
    "boltons/fileutils.py": "ba5d0789d8bc2865f34786bda3a3f3c7ebcd7299",
}


def blob_hash(path):
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


class Boltons480BaselineTests(unittest.TestCase):
    def test_observed_historical_defect_and_controls(self):
        actual = observe()
        self.assertEqual(actual.keys(), BASELINE.keys())
        for key, expected in BASELINE.items():
            with self.subTest(case=key):
                self.assertEqual(actual[key], expected)

    def test_vendored_source_and_bsd_license_are_pristine(self):
        self.assertEqual(
            UPSTREAM_COMMIT, "967864f89791509f9eb36b22b4579d36b72a6df2"
        )
        self.assertEqual(
            {p.name for p in (VENDOR / "boltons").glob("*.py")},
            {"__init__.py", "fileutils.py"},
        )
        for path, expected in UPSTREAM_BLOBS.items():
            with self.subTest(path=path):
                self.assertEqual(blob_hash(VENDOR / path), expected)
        self.assertEqual(
            blob_hash(VENDOR.parent / "LICENSE"),
            "6a4c9d2496f53c61c99ae7c113e6ed94b15b038c",
        )


if __name__ == "__main__":
    unittest.main()
