"""Reject unpinned additions to the five historical upstream Python subsets.

Original source bytes and license notices are independently pinned by
case-specific integrity tests. This check closes the file-inventory gap.
"""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1] / "benchmarks" / "bugs"
PINNED_SOURCES = {
    "boltons_480/upstream": {
        "boltons/__init__.py", "boltons/fileutils.py",
    },
    "humanize_30/upstream": {
        "humanize/__init__.py", "humanize/_version.py",
        "humanize/filesize.py", "humanize/i18n.py",
        "humanize/lists.py", "humanize/number.py", "humanize/time.py",
    },
    "more_itertools_1342/upstream": {"chunked_even.py"},
    "pygments_3190/upstream": {"regexopt.py"},
    "tokenize_rt_33/upstream": {"tokenize_rt.py"},
}


def python_files(root):
    return {path.relative_to(root).as_posix() for path in root.rglob("*.py")}


class UpstreamSourceInventoryTests(unittest.TestCase):
    def test_five_upstream_python_subsets_have_exact_file_sets(self):
        for subset, expected in PINNED_SOURCES.items():
            with self.subTest(subset=subset):
                root = ROOT / subset
                self.assertTrue(root.is_dir())
                self.assertEqual(python_files(root), expected)

    def test_recursive_inventory_detects_unlisted_nested_modules(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "source.py").write_text("VALUE = 1\n", encoding="utf-8")
            self.assertEqual(python_files(root), {"source.py"})
            nested = root / "extra" / "helper.py"
            nested.parent.mkdir()
            nested.write_text("VALUE = 2\n", encoding="utf-8")
            self.assertIn("extra/helper.py", python_files(root))
            self.assertNotEqual(python_files(root), {"source.py"})


if __name__ == "__main__":
    unittest.main()
