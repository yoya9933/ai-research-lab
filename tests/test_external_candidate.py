"""Reproduce the external corpus results for the chat-authored attempt."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from lab.report import compare


class ExercismCandidateTests(unittest.TestCase):
    def test_chat_attempt_fixes_all_pinned_public_cases(self):
        with tempfile.TemporaryDirectory() as directory:
            reports = {}
            for candidate in ("starter", "attempt_001"):
                path = Path(directory) / f"{candidate}.json"
                command = [sys.executable, "-m", "benchmarks.exercism.runner",
                           candidate, "--output", str(path)]
                if candidate == "attempt_001":
                    command.append("--require-all-pass")
                result = subprocess.run(command, capture_output=True, text=True,
                                        check=False, timeout=30)
                self.assertEqual(result.returncode, 0, result.stderr)
                reports[candidate] = json.loads(path.read_text(encoding="utf-8"))
            summary = compare(reports["starter"], reports["attempt_001"])
            self.assertEqual((summary["baseline"], summary["candidate"]), (0, 29))
            self.assertEqual((summary["fixed"], summary["regressed"]), (29, 0))


if __name__ == "__main__":
    unittest.main()
