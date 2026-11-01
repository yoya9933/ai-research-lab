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

    def test_multiple_failing_subtests_keep_both_failure_details(self):
        code = (
            "import unittest\n\nclass SyntheticTest(unittest.TestCase):\n"
            "    def test_case(self):\n"
            "        for number in range(3):\n"
            "            with self.subTest(number=number):\n"
            "                self.assertEqual(number, 0)\n"
        )
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "candidate").mkdir()
            test_dir = root / "tests"
            test_dir.mkdir()
            (test_dir / "subtest_case_test.py").write_text(code, encoding="utf-8")
            with mock.patch.object(runner, "ROOT", root), mock.patch.object(
                runner, "TRACKS", {"synthetic": ("candidate", "tests", 1)}
            ):
                report = runner.evaluate("synthetic")
        self.assertEqual((report["passed"], report["total"]), (0, 1))
        case, = report["cases"]
        self.assertEqual(case["actual"], "failure")
        self.assertFalse(case["passed"])
        self.assertIn("number=1", case["error"])
        self.assertIn("number=2", case["error"])
        self.assertEqual(case["error"].count("AssertionError"), 2)

    def test_subtest_errors_and_successful_subtests_are_classified(self):
        cases = {
            "successful": (
                "    def test_case(self):\n"
                "        for value in range(2):\n"
                "            with self.subTest(value=value):\n"
                "                self.assertLess(value, 3)\n"
            ),
            "error": (
                "    def test_case(self):\n"
                "        with self.subTest(value=123):\n"
                "            raise RuntimeError('failure inside subtest')\n"
            ),
        }
        for name, method in cases.items():
            with self.subTest(case=name), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                (root / "candidate").mkdir()
                test_dir = root / "tests"
                test_dir.mkdir()
                (test_dir / "subtest_case_test.py").write_text(
                    "import unittest\n\nclass SyntheticTest(unittest.TestCase):\n"
                    + method, encoding="utf-8",
                )
                with mock.patch.object(runner, "ROOT", root), mock.patch.object(
                    runner, "TRACKS", {"synthetic": ("candidate", "tests", 1)}
                ):
                    report = runner.evaluate("synthetic")
                case, = report["cases"]
                if name == "successful":
                    self.assertEqual((report["passed"], report["total"]), (1, 1))
                    self.assertEqual((case["actual"], case["error"]), ("pass", None))
                else:
                    self.assertEqual((report["passed"], report["total"]), (0, 1))
                    self.assertEqual(case["actual"], "error")
                    self.assertIn("RuntimeError: failure inside subtest", case["error"])
                    self.assertIn("value=123", case["error"])

    def test_parent_failure_after_subtests_preserves_all_diagnostics(self):
        endings = {
            "failure": "self.fail('outer assertion')",
            "error": "raise RuntimeError('outer crash')",
        }
        for name, ending in endings.items():
            with self.subTest(kind=name), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                (root / "candidate").mkdir()
                test_dir = root / "tests"
                test_dir.mkdir()
                code = (
                    "import unittest\n\nclass SyntheticTest(unittest.TestCase):\n"
                    "    def test_case(self):\n"
                    "        for number in (1, 2):\n"
                    "            with self.subTest(number=number):\n"
                    "                self.assertEqual(number, 0)\n"
                    f"        {ending}\n"
                )
                (test_dir / "mixed_case_test.py").write_text(code, encoding="utf-8")
                with mock.patch.object(runner, "ROOT", root), mock.patch.object(
                    runner, "TRACKS", {"synthetic": ("candidate", "tests", 1)}
                ):
                    report = runner.evaluate("synthetic")
                self.assertEqual((report["passed"], report["total"]), (0, 1))
                case, = report["cases"]
                self.assertEqual(case["actual"], name)
                self.assertIn("number=1", case["error"])
                self.assertIn("number=2", case["error"])
                self.assertIn(
                    "outer assertion" if name == "failure" else "outer crash",
                    case["error"],
                )

    def test_failed_test_module_discovery_cannot_be_scored(self):
        sources = {
            "import_error": 'raise ImportError("independent test dependency failed")\n',
            "syntax_error": "def broken(:\n",
        }
        for kind, source in sources.items():
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                (root / "candidate").mkdir()
                test_dir = root / "tests"
                test_dir.mkdir()
                (test_dir / "broken_suite_test.py").write_text(
                    source, encoding="utf-8"
                )
                # unittest represents one module import failure as one
                # synthetic _FailedTest, which can mask a matching count.
                probe = unittest.TestLoader()
                suite = probe.discover(str(test_dir), pattern="*_test.py")
                self.assertEqual(suite.countTestCases(), 1)
                self.assertEqual(len(probe.errors), 1)
                original_path = sys.path[:]
                with mock.patch.object(runner, "ROOT", root), mock.patch.object(
                    runner, "TRACKS", {"synthetic": ("candidate", "tests", 1)}
                ):
                    with self.assertRaisesRegex(
                        RuntimeError, "Upstream test discovery failed"
                    ) as caught:
                        runner.evaluate("synthetic")
                self.assertIn("broken_suite_test", str(caught.exception))
                self.assertEqual(sys.path, original_path)

    def test_duplicate_test_ids_do_not_inflate_the_score(self):
        source = (
            "import unittest\n\n"
            "class SyntheticTest(unittest.TestCase):\n"
            "    def test_case(self):\n"
            "        self.assertTrue(True)\n\n"
            "def load_tests(loader, tests, pattern):\n"
            "    return unittest.TestSuite([\n"
            "        SyntheticTest('test_case'), SyntheticTest('test_case')\n"
            "    ])\n"
        )
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "candidate").mkdir()
            tests = root / "tests"
            tests.mkdir()
            (tests / "synthetic_test.py").write_text(source, encoding="utf-8")
            original_path = sys.path[:]
            # Native unittest permits load_tests to return the same test ID
            # twice, so testsRun can equal the declared count misleadingly.
            with mock.patch.object(runner, "ROOT", root), mock.patch.object(
                runner, "TRACKS", {"synthetic": ("candidate", "tests", 2)}
            ):
                with self.assertRaisesRegex(
                    RuntimeError, "Missing or duplicate upstream test identities"
                ):
                    runner.evaluate("synthetic")
            self.assertEqual(sys.path, original_path)

    def test_fixture_errors_are_rejected_not_attributed_to_last_test(self):
        fixtures = {
            "tearDownModule": (
                "def tearDownModule():\n"
                "    raise RuntimeError('module cleanup failed')\n"
            ),
            "tearDownClass": (
                "def tearDownClass():\n"
                "    raise RuntimeError('class cleanup failed')\n"
            ),
            "setUpClass": (
                "def setUpClass():\n"
                "    raise RuntimeError('class initialization failed')\n"
            ),
        }
        for fixture, body in fixtures.items():
            with self.subTest(fixture=fixture), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                (root / "candidate").mkdir()
                test_dir = root / "tests"
                test_dir.mkdir()
                normal = (
                    "import unittest\n\n"
                    "class SyntheticTest(unittest.TestCase):\n"
                    "    def test_case(self):\n"
                    "        self.assertTrue(True)\n"
                )
                if fixture == "tearDownModule":
                    source = normal + "\n" + body
                else:
                    # Keep a single bona fide method; add a class fixture.
                    source = normal + "\n" + "".join(
                        "    " + line + "\n" for line in body.splitlines()
                    )
                (test_dir / "fixture_test.py").write_text(source, encoding="utf-8")
                original_path = sys.path[:]
                with mock.patch.object(runner, "ROOT", root), mock.patch.object(
                    runner, "TRACKS", {"synthetic": ("candidate", "tests", 1)}
                ):
                    with self.assertRaisesRegex(
                        RuntimeError, "Unscored upstream fixture errors"
                    ) as caught:
                        runner.evaluate("synthetic")
                self.assertIn(fixture, str(caught.exception))
                self.assertIn("failed", str(caught.exception))
                self.assertEqual(sys.path, original_path)

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
