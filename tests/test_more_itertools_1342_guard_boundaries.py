"""Focused post-freeze checks beyond PR #45's finite-iterator matrix.

These investigator-authored cases are not blind and never modify the candidate.
"""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.humanize_30.reproduce import observe as run_script
from benchmarks.bugs.more_itertools_1342.patch import make_candidate
from benchmarks.bugs.more_itertools_1342.reproduce import VENDOR

SCRIPT = """
import json
from chunked_even import chunked_even

class Poison:
    def __iter__(self):
        raise AssertionError("ignored source inspected")

def invalid_case(n):
    try:
        return {"chunks": list(chunked_even(Poison(), n))}
    except Exception as exc:
        return {"error": type(exc).__name__, "message": str(exc)}

cases = []
for n in range(9, 15):
    boundary = (n - 1) * (n - 2)
    for length in (boundary - 1, boundary, boundary + 1):
        try:
            chunks = list(chunked_even(iter(range(length)), n))
            cases.append({"size": n, "length": length, "chunks": chunks})
        except Exception as exc:
            cases.append({
                "size": n, "length": length,
                "error": type(exc).__name__, "message": str(exc),
            })
print(json.dumps({
    "thresholds": cases,
    "poison": {"zero": invalid_case(0), "negative": invalid_case(-1)},
}))
"""


class MoreItertools1342GuardBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = run_script(vendor=VENDOR, script=SCRIPT)
        cls.temp = tempfile.TemporaryDirectory()
        try:
            vendor = make_candidate(Path(cls.temp.name) / "patched")
            cls.after = run_script(vendor=vendor, script=SCRIPT)
        except BaseException:
            cls.temp.cleanup()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_eighteen_buffer_thresholds_preserve_content_and_chunk_balance(self):
        before = self.before["thresholds"]
        after = self.after["thresholds"]
        self.assertEqual(before, after)  # No regressions for positive sizes.
        self.assertEqual(len(after), 18)
        for case in after:
            n, length = case["size"], case["length"]
            with self.subTest(size=n, length=length):
                self.assertIn(length, ((n - 1) * (n - 2) - 1,
                                       (n - 1) * (n - 2),
                                       (n - 1) * (n - 2) + 1))
                self.assertNotIn("error", case)
                chunks = case["chunks"]
                sizes = [len(chunk) for chunk in chunks]
                self.assertEqual([x for chunk in chunks for x in chunk],
                                 list(range(length)))
                self.assertEqual(len(chunks), (length + n - 1) // n)
                self.assertTrue(all(1 <= size <= n for size in sizes))
                self.assertLessEqual(max(sizes) - min(sizes), 1)

    def test_rejected_sizes_never_call_iter_on_poisoned_source(self):
        expected_before = {
            "error": "AssertionError", "message": "ignored source inspected"
        }
        self.assertEqual(self.before["poison"]["zero"], expected_before)
        self.assertEqual(self.before["poison"]["negative"], expected_before)
        self.assertEqual(self.after["poison"]["zero"], {"chunks": []})
        self.assertEqual(self.after["poison"]["negative"], {
            "error": "ValueError", "message": "n must be at least 0"
        })


if __name__ == "__main__":
    unittest.main()
