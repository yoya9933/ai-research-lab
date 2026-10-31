"""Historical source integrity and no-EOL byte-offset reproduction."""

from hashlib import sha1
import unittest

from benchmarks.bugs.tokenize_rt_33.reproduce import UPSTREAM_COMMIT, VENDOR, observe

BASELINE = {
    "number_without_eol": {"newline": [1, 0, ""], "roundtrip": True},
    "assignment_without_eol": {"newline": [1, 0, ""], "roundtrip": True},
    "unicode_without_eol": {"newline": [1, 0, ""], "roundtrip": True},
    "number_with_eol": {"newline": [1, 1, "\n"], "roundtrip": True},
    "assignment_with_eol": {"newline": [1, 3, "\n"], "roundtrip": True},
    "unicode_with_eol": {"newline": [1, 4, "\n"], "roundtrip": True},
}
SOURCE_SHA = "98f72cee984b23f138dd88208dbdb438e1745673"
LICENSE_SHA = "522fbe20b89911bb8d68b4a684a51225dd571764"


def blob_sha(path):
    content = path.read_bytes()
    return sha1(f"blob {len(content)}\0".encode() + content).hexdigest()


class TokenizeRt33BaselineTests(unittest.TestCase):
    def test_unmodified_snapshot_matches_upstream_blob(self):
        self.assertEqual(
            UPSTREAM_COMMIT, "7f89433be049d73e189a903485a93bdf3e56f1a0"
        )
        self.assertEqual(
            {p.name for p in VENDOR.iterdir() if p.is_file()}, {"tokenize_rt.py"}
        )
        self.assertEqual(blob_sha(VENDOR / "tokenize_rt.py"), SOURCE_SHA)
        self.assertEqual(
            blob_sha(VENDOR.parent / "LICENSE"), LICENSE_SHA
        )

    def test_reported_no_eol_error_and_controls(self):
        actual = observe()
        self.assertEqual(actual.keys(), BASELINE.keys())
        for key, expected in BASELINE.items():
            with self.subTest(case=key):
                self.assertEqual(actual[key], expected)


if __name__ == "__main__":
    unittest.main()
