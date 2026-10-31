"""Offline Git-blob verification of the six vendored humanize modules.

Hashes are from python-humanize/humanize commit
9528daf55fd7178c025f7294b8e349f8b3524175, src/humanize/.
Only the English-facing Python modules were copied. _version.py is a local stub.
"""

from hashlib import sha1
import unittest

from benchmarks.bugs.humanize_30.reproduce import UPSTREAM_COMMIT, VENDOR

UPSTREAM_MODULE_BLOBS = {
    "__init__.py": "6fb9959379d7469d7c5f5d06a6a5d1e51e680939",
    "filesize.py": "5650d02692399aa6fe533447c05c6bdebab8d636",
    "i18n.py": "a6a5cb175516f5f1d6b36ac084b9d4ab0d67d334",
    "lists.py": "3a52f1ecdf992210927ed94172835f8b2dae50b1",
    "number.py": "5154895fe41524fabd4252eb6e269676de9bfa6d",
    "time.py": "3559546c854c5315daa154caa5b2db513c9ab808",
}
LOCAL_VERSION_STUB_BLOB = "1fbcf04785bac3e3443525e51d1087172369de3d"
UPSTREAM_LICENSE_BLOB = "e0687959f9e19e8bee8783424885bca65477fa28"


def git_blob_hash(path):
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return sha1(header + content).hexdigest()


class PinnedHumanizeSourceTests(unittest.TestCase):
    def test_source_commit_not_silently_repointed(self):
        self.assertEqual(
            UPSTREAM_COMMIT, "9528daf55fd7178c025f7294b8e349f8b3524175"
        )

    def test_six_modules_match_upstream_byte_for_byte(self):
        modules = VENDOR / "humanize"
        self.assertEqual(
            {path.name for path in modules.glob("*.py")},
            set(UPSTREAM_MODULE_BLOBS) | {"_version.py"},
        )
        for name, expected in UPSTREAM_MODULE_BLOBS.items():
            with self.subTest(module=name):
                self.assertEqual(git_blob_hash(modules / name), expected)

    def test_generated_version_stub_is_separately_pinned(self):
        self.assertEqual(
            git_blob_hash(VENDOR / "humanize" / "_version.py"),
            LOCAL_VERSION_STUB_BLOB,
        )

    def test_copied_mit_license_matches_upstream(self):
        self.assertEqual(
            git_blob_hash(VENDOR.parent / "LICENCE"), UPSTREAM_LICENSE_BLOB
        )


if __name__ == "__main__":
    unittest.main()
