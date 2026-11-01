"""Run two original upstream assertions on before/after frozen source."""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.humanize_30.reproduce import observe as run_script
from benchmarks.bugs.pygments_3190.patch import make_candidate
from benchmarks.bugs.pygments_3190.reproduce import VENDOR

SCRIPT = """
import json
from contextlib import redirect_stdout
from io import StringIO
from benchmarks.bugs.pygments_3190.upstream_tests import (
    test_duplicates, test_duplicate_single_chars,
)

results = {}
for key, case in (
    ("duplicates", test_duplicates),
    ("duplicate_single_chars", test_duplicate_single_chars),
):
    try:
        with redirect_stdout(StringIO()):
            case()
    except Exception as exc:
        results[key] = {"passed": False, "error": type(exc).__name__}
    else:
        results[key] = {"passed": True}
print(json.dumps(results))
"""

BASELINE = {
    "duplicates": {"passed": False, "error": "AssertionError"},
    "duplicate_single_chars": {"passed": False, "error": "AssertionError"},
}
CANDIDATE = {
    "duplicates": {"passed": True},
    "duplicate_single_chars": {"passed": True},
}


class Pygments3190UpstreamReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = run_script(vendor=VENDOR, script=SCRIPT)
        cls.tmp = tempfile.TemporaryDirectory()
        try:
            cls.after = run_script(
                vendor=make_candidate(Path(cls.tmp.name) / "candidate"),
                script=SCRIPT,
            )
        except BaseException:
            cls.tmp.cleanup()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_original_assertions_fail_on_pinned_pre_fix_source(self):
        self.assertEqual(self.before, BASELINE)

    def test_original_assertions_pass_on_frozen_candidate(self):
        self.assertEqual(self.after, CANDIDATE)


if __name__ == "__main__":
    unittest.main()
