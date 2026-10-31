"""Ensure external test imports and grading are never silently skipped."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class ExternalBenchmarkTests(unittest.TestCase):
    def test_pinned_exercism_starter_is_incomplete(self):
        with tempfile.TemporaryDirectory() as directory:
            report_path = Path(directory) / "starter.json"
            process = subprocess.run(
                [sys.executable, "-m", "benchmarks.exercism.runner",
                 "starter", "--output", str(report_path)],
                capture_output=True, text=True, check=False, timeout=30,
            )
            self.assertEqual(process.returncode, 0, process.stderr)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual((report["passed"], report["total"]), (0, 29))
            self.assertEqual(len({c["task"] for c in report["cases"]}), 29)
            self.assertTrue(all(c["actual"] == "failure" for c in report["cases"]))

    def test_strict_exit_code_fails_for_starter(self):
        process = subprocess.run(
            [sys.executable, "-m", "benchmarks.exercism.runner",
             "starter", "--require-all-pass"],
            capture_output=True, text=True, check=False, timeout=30,
        )
        self.assertEqual(process.returncode, 1, process.stderr)


if __name__ == "__main__":
    unittest.main()
