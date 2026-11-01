"""Assert the actual unfixed behavior; passing here is not a repair."""

from hashlib import sha1
from pathlib import Path
import unittest

from benchmarks.bugs.more_itertools_1342.reproduce import observe, VENDOR

SOURCE_GIT_BLOB = "1335bf7be6f2d884791bb1168a012c6257887fb8"
LICENSE_GIT_BLOB = "0a523bece3e50519653c4d7a38399baa487fefa1"

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
        for path, expected in (
            (VENDOR / "chunked_even.py", SOURCE_GIT_BLOB),
            (VENDOR.parent / "LICENSE", LICENSE_GIT_BLOB),
        ):
            with self.subTest(path=path.name):
                content = path.read_bytes()
                actual = sha1(
                    f"blob {len(content)}\0".encode("ascii") + content
                ).hexdigest()
                self.assertEqual(actual, expected)

    def test_unfixed_boundary_failures_and_controls(self):
        self.assertEqual(observe(), BASELINE)


if __name__ == "__main__":
    unittest.main()
