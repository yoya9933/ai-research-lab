"""Assert the actual unfixed behavior; passing here is not a repair."""

from hashlib import sha1
from pathlib import Path
import unittest

from benchmarks.bugs.more_itertools_1342.reproduce import observe, VENDOR

SOURCE_GIT_BLOB = "1335bf7be6f2d884791bb1168a012c6257887fb8"

BASELINE = {
    "zero_nonempty": {"error": "ValueError", "remaining": ["c", "d"]},
    "zero_empty": {"error": "ValueError", "remaining": []},
    "negative_nonempty": {"error": "ValueError", "remaining": []},
    "negative_empty": {"error": "ValueError", "remaining": []},
    "zero_none": {"error": "TypeError"},
    "normal_seven_three": {"chunks": [[1, 2, 3], [4, 5], [6, 7]], "remaining": []},
    "normal_six_two": {"chunks": [[1, 2], [3, 4], [5, 6]], "remaining": []},
    "normal_empty": {"chunks": [], "remaining": []},
    "normal_one": {"chunks": [["a"], ["b"]], "remaining": []},
    "invalid_type": {"error": "TypeError", "remaining": ["a", "b", "c", "d"]},
}


class MoreItertools1342BaselineTests(unittest.TestCase):
    def test_pinned_excerpt_integrity(self):
        content = (VENDOR / "chunked_even.py").read_bytes()
        self.assertEqual(
            sha1(f"blob {len(content)}\0".encode("ascii") + content).hexdigest(),
            SOURCE_GIT_BLOB,
        )

    def test_unfixed_boundary_failures_and_controls(self):
        self.assertEqual(observe(), BASELINE)


if __name__ == "__main__":
    unittest.main()
