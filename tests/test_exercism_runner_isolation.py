"""Named Exercism tracks must score independently in a reused Python process."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from benchmarks.exercism import runner
from benchmarks.exercism.runner import evaluate


class TrackIsolationTests(unittest.TestCase):
    def test_runner_rejects_skips_expected_failures_and_unexpected_successes(self):
        cases = {
            "skipped": (
                '    @unittest.skip("unavailable")\n'
                '    def test_case(self):\n'
                '        self.assertTrue(True)\n'
            ),
            "expected_failure": (
                '    @unittest.expectedFailure\n'
                '    def test_case(self):\n'
                '        self.assertTrue(False)\n'
            ),
            "unexpected_success": (
                '    @unittest.expectedFailure\n'
                '    def test_case(self):\n'
                '        self.assertTrue(True)\n'
            ),
        }
        for kind, method in cases.items():
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                (root / "candidate").mkdir()
                tests = root / "tests"
                tests.mkdir()
                (tests / "synthetic_test.py").write_text(
                    "import unittest\n\nclass SyntheticTest(unittest.TestCase):\n"
                    + method, encoding="utf-8",
                )
                before_path = sys.path[:]
                with mock.patch.object(runner, "ROOT", root), mock.patch.object(
                    runner, "TRACKS", {"synthetic": ("candidate", "tests", 1)}
                ):
                    with self.assertRaisesRegex(
                        RuntimeError, "Unscorable upstream test outcomes"
                    ):
                        runner.evaluate("synthetic")
                self.assertEqual(sys.path, before_path)

    def test_repeated_and_reversed_track_order(self):
        original_path = sys.path[:]
        tracks = (
            ("starter", 0, 29),
            ("attempt_001", 29, 29),
            ("attempt_001", 29, 29),
            ("starter", 0, 29),
            ("starter_002", 0, 44),
            ("attempt_002", 44, 44),
            ("attempt_002", 44, 44),
            ("starter_002", 0, 44),
        )
        for track, passed, total in tracks:
            with self.subTest(track=track, passed=passed):
                report = evaluate(track)
                self.assertEqual((report["passed"], report["total"]), (passed, total))
                self.assertEqual(sys.path, original_path)


if __name__ == "__main__":
    unittest.main()
