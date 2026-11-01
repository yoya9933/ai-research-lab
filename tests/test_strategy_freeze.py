"""Guard Study 001's pre-registered memory intervention against silent edits."""

import hashlib
from pathlib import Path
import unittest


EXPECTED_GIT_BLOB = "405e418906d0bb81ce8324b341d6d73f593ae571"
MEMORY_FILE = Path(__file__).resolve().parents[1] / "docs" / "STRATEGY_MEMORY.md"


class StrategyMemoryFreezeTests(unittest.TestCase):
    def test_study_001_uses_unchanged_memory_bytes(self):
        content = MEMORY_FILE.read_bytes()
        # Git's SHA-1 blob identity (not a signature or content-authentication system).
        git_blob = b"blob " + str(len(content)).encode("ascii") + b"\0" + content
        observed = hashlib.sha1(git_blob).hexdigest()
        self.assertEqual(
            observed, EXPECTED_GIT_BLOB,
            "Study 001 is frozen: preregister a NEW study version before editing its memory",
        )


if __name__ == "__main__":
    unittest.main()
