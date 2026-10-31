"""Reproduce post-freeze upstream unit tests without rewriting the candidate."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from lab.report import compare


class SecondExternalTrialTests(unittest.TestCase):
    def test_candidate_and_starter_are_scored_on_identical_external_tests(self):
        with tempfile.TemporaryDirectory() as directory:
            reports = {}
            for candidate in ("starter_002", "attempt_002"):
                target = Path(directory) / f"{candidate}.json"
                command = [sys.executable, "-m", "benchmarks.exercism.runner",
                           candidate, "--output", str(target)]
                result = subprocess.run(command, capture_output=True, text=True,
                                        check=False, timeout=30)
                self.assertEqual(result.returncode, 0, result.stderr)
                reports[candidate] = json.loads(target.read_text(encoding="utf-8"))
                self.assertEqual(reports[candidate]["total"], 44)
            summary = compare(reports["starter_002"], reports["attempt_002"])
            self.assertEqual(summary["total"], 44)
            self.assertEqual(summary["fixed"] - summary["regressed"], summary["delta"])


if __name__ == "__main__":
    unittest.main()
