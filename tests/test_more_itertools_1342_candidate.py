"""Check the local accepted candidate on the same 10 pinned observations."""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.humanize_30.reproduce import observe as run_script
from benchmarks.bugs.more_itertools_1342.patch import make_candidate
from benchmarks.bugs.more_itertools_1342.reproduce import observe
from tests.test_more_itertools_1342 import BASELINE

FIXED = {
    "zero_nonempty": {"chunks": [], "remaining": list("abcd")},
    "zero_empty": {"chunks": [], "remaining": []},
    "negative_nonempty": {"error": "ValueError", "remaining": list("abcd")},
    "zero_none": {"chunks": []},
}

NEGATIVE_DETAILS = """
import json
from chunked_even import chunked_even

results = {}
for label, source in (("noniterable", None), ("empty", ""), ("nonempty", "abc")):
    try:
        list(chunked_even(source, -1))
        results[label] = {"error": None}
    except Exception as exc:
        results[label] = {"error": type(exc).__name__, "message": str(exc)}
print(json.dumps(results))
"""


class MoreItertools1342CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = observe()
        cls.temp = tempfile.TemporaryDirectory()
        try:
            cls.vendor = make_candidate(Path(cls.temp.name) / "candidate")
            cls.after = observe(cls.vendor)
        except BaseException:
            cls.temp.cleanup()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_immutable_baseline(self):
        self.assertEqual(self.before, BASELINE)

    def test_corrected_and_unchanged_cases(self):
        self.assertEqual(self.after.keys(), BASELINE.keys())
        for key, expected in BASELINE.items():
            with self.subTest(case=key):
                self.assertEqual(self.after[key], FIXED.get(key, expected))

    def test_exactly_four_of_ten_observations_change(self):
        changed = {k for k in BASELINE if self.before[k] != self.after[k]}
        self.assertEqual(changed, set(FIXED))
        self.assertEqual(len(changed), 4)

    def test_negative_validation_is_specific_even_without_input(self):
        details = run_script(vendor=self.vendor, script=NEGATIVE_DETAILS)
        for key in ("noniterable", "empty", "nonempty"):
            with self.subTest(input=key):
                self.assertEqual(
                    details[key], {"error": "ValueError", "message": "n must be at least 0"}
                )


if __name__ == "__main__":
    unittest.main()
