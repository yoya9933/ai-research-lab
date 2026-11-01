"""Post-freeze regex-language differential tests for pinned Pygments issue 3190."""

from pathlib import Path
import tempfile
import unittest

from benchmarks.bugs.pygments_3190.followup import observe
from benchmarks.bugs.pygments_3190.patch import make_candidate


class Pygments3190PropertyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = observe()
        cls.tmp = tempfile.TemporaryDirectory()
        try:
            cls.after = observe(make_candidate(Path(cls.tmp.name) / "candidate"))
        except BaseException:
            cls.tmp.cleanup()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_domain_and_identical_inputs(self):
        self.assertEqual(len(self.before), 144)
        self.assertEqual(len(self.after), 144)
        for before, after in zip(self.before, self.after):
            with self.subTest(index=before["index"], mode=before["mode"]):
                self.assertEqual(
                    (before["index"], before["mode"], before["words"]),
                    (after["index"], after["mode"], after["words"]),
                )
                self.assertEqual(before["canonical"], after["canonical"])

    def test_candidate_canonicalizes_all_144_word_lists(self):
        for row in self.after:
            with self.subTest(index=row["index"], mode=row["mode"]):
                self.assertEqual(row["pattern"], row["canonical"])

    def test_both_variants_match_only_the_supplied_literals(self):
        for variant, records in (("baseline", self.before), ("candidate", self.after)):
            for row in records:
                with self.subTest(variant=variant, index=row["index"], mode=row["mode"]):
                    self.assertEqual(row["matched"], row["expected"])

    def test_sixteen_singleton_controls_are_unchanged(self):
        count = 0
        for before, after in zip(self.before, self.after):
            if len(before["words"]) == 1:
                count += 1
                with self.subTest(index=before["index"], mode=before["mode"]):
                    self.assertEqual(before, after)
        self.assertEqual(count, 16)

    def test_128_duplicate_lists_preserve_language(self):
        count = 0
        for before, after in zip(self.before, self.after):
            if len(before["words"]) > 1:
                count += 1
                with self.subTest(index=before["index"], mode=before["mode"]):
                    self.assertEqual(before["matched"], after["matched"])
        self.assertEqual(count, 128)

    def test_known_duplicate_case_changes_pattern(self):
        cases = [
            (before, after) for before, after in zip(self.before, self.after)
            if before["words"] == ["a", "a", "b"] and before["mode"] == "plain"
        ]
        self.assertEqual(len(cases), 1)
        before, after = cases[0]
        self.assertNotEqual(before["pattern"], after["pattern"])
        self.assertEqual(after["pattern"], after["canonical"])


if __name__ == "__main__":
    unittest.main()
