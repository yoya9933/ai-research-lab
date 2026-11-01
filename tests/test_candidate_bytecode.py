"""Regression: temporary repair copies never include compiled source caches."""

from pathlib import Path
from shutil import copytree
import tempfile
import unittest
from unittest.mock import patch as mock_patch

from benchmarks.bugs.humanize_30 import patch as humanize_30
from benchmarks.bugs.humanize_333 import patch as humanize_333
from benchmarks.bugs.humanize_486 import patch as humanize_486
from benchmarks.bugs.boltons_479 import patch as boltons_479
from benchmarks.bugs.boltons_480 import patch as boltons_480
from benchmarks.bugs.tokenize_rt_33 import patch as tokenize_rt
from benchmarks.bugs.tokenize_rt_33.patch_roundtrip import (
    make_candidate_with_roundtrip,
)

SOURCES = (
    ("humanize", humanize_30.VENDOR, (
        humanize_30, humanize_333, humanize_486,
    )),
    ("boltons", boltons_480.VENDOR, (
        boltons_479, boltons_480,
    )),
)


class CandidateBytecodeIsolationTests(unittest.TestCase):
    def test_all_candidate_patches_exclude_copied_python_caches(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for package, original, patchers in SOURCES:
                with self.subTest(package=package):
                    source = root / f"{package}-source"
                    copytree(original, source)
                    cache = source / package / "__pycache__"
                    cache.mkdir(exist_ok=True)
                    (cache / "stale.pyc").write_bytes(b"stale interpreter cache")
                    (source / "orphan.pyc").write_bytes(b"stale bytecode")
                    for index, patcher in enumerate(patchers):
                        with self.subTest(patcher=patcher.__name__):
                            with mock_patch.object(patcher, "VENDOR", source):
                                target = patcher.make_candidate(
                                    root / f"{package}-candidate-{index}"
                                )
                            stale = [
                                str(path) for path in target.rglob("*")
                                if path.name == "__pycache__" or path.suffix == ".pyc"
                            ]
                            self.assertEqual(stale, [])
                    self.assertTrue((cache / "stale.pyc").exists())

    def test_tokenizer_candidates_exclude_inherited_bytecode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "tokenizer-source"
            copytree(tokenize_rt.VENDOR, source)
            cache = source / "__pycache__"
            cache.mkdir()
            (cache / "tokenize_rt.cpython-311.pyc").write_bytes(b"stale code")
            (source / "orphan.pyc").write_bytes(b"stale bytecode")

            with mock_patch.object(tokenize_rt, "VENDOR", source):
                for name, build in (
                    ("offset", tokenize_rt.make_candidate),
                    ("roundtrip", make_candidate_with_roundtrip),
                ):
                    with self.subTest(candidate=name):
                        candidate = build(root / name)
                        inherited = [
                            str(path) for path in candidate.rglob("*")
                            if path.name == "__pycache__" or path.suffix == ".pyc"
                        ]
                        self.assertEqual(inherited, [])

            self.assertTrue((cache / "tokenize_rt.cpython-311.pyc").exists())



if __name__ == "__main__":
    unittest.main()
