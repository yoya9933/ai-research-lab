"""Named Exercism tracks must score independently in a reused Python process."""

import sys
import unittest

from benchmarks.exercism.runner import evaluate


class TrackIsolationTests(unittest.TestCase):
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
