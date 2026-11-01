"""Pin historical candidate source bytes independently of later follow-up tests.

Blob IDs were checked against the stated Git commits using GitHub MCP.
This verifies local source stability, not absence of model pretraining exposure.
"""

from hashlib import sha1
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

# Candidate committed before the trial_002 upstream test files were read:
# f714ff61474145f50036a6a77351baf0e441ff93.
# tokenize-rt first candidate before its post-freeze follow-up suite:
# 9e539f746a023e64fa252677895e8bc7791eddc5.
# Secondary tokenizer candidate after that follow-up, at:
# d189e4826609fa9d063b42155170167880036ca3.
# more-itertools #1342 candidate committed before this property matrix:
# 33cd99acfdf62b13033db865f4b0302a6a7ebd96.
# Pygments #3190 candidate was committed before fetching its original test file:
# 94a4c403456de093d3350d1d65fb8939f1873849.
FROZEN_BLOBS = {
    "benchmarks/exercism/trial_002/attempt_002/armstrong_numbers.py":
        "53f48efbe999d4891a2537c9f44b6f62f5c6a6bb",
    "benchmarks/exercism/trial_002/attempt_002/luhn.py":
        "0311b45fa9c1b6dc00559876419e999b10225011",
    "benchmarks/exercism/trial_002/attempt_002/pangram.py":
        "1f146541b1eb3ecbe97e6f7a604b7348bcd6063b",
    "benchmarks/bugs/tokenize_rt_33/patch.py":
        "778fa86aebcf6c525eec2f711b04c1ec0f671a2a",
    "benchmarks/bugs/tokenize_rt_33/patch_roundtrip.py":
        "e85619f2dbc03545cfdb7d3c8cb98181e8df2398",
    "benchmarks/bugs/more_itertools_1342/patch.py":
        "b26e35b35a8911e8a117e3f7f10a703291b4b585",
    "benchmarks/bugs/pygments_3190/patch.py":
        "59d075d0763feb68fb2385b71f95cf2835c68afe",
    # Current reproducible wrappers, not all byte-identical to original
    # candidate commits: PR #25 excluded stale inherited bytecode.
    "benchmarks/bugs/humanize_30/patch.py":
        "d270f28f8017043b3bbf4570112038bed384f8cf",
    "benchmarks/bugs/humanize_333/patch.py":
        "87a9737feb8a5e6d1b97b2d622f11789fcd57e94",
    "benchmarks/bugs/humanize_486/patch.py":
        "e7d35226208aa3401f684ed2c1c49768356ad74d",
    "benchmarks/bugs/boltons_480/patch.py":
        "b172171c58b4245d8a0e9e2e10a4c0f41a170552",
    # Exploratory two-defect batch: first-attempt candidate SHA 4939deccc45a839e969d53a0cd33bda4f6685b10.
    "benchmarks/bugs/boltons_348/patch.py":
        "341df8927a7235d62acf74c8ba867870394509e0",
    "benchmarks/bugs/more_itertools_1214/patch.py":
        "3b35cafbe1c720bfde8a3a72c2ce863a1afc0702",
    # The following wrappers also match their original candidate-PR blobs.
    "benchmarks/bugs/boltons_479/patch.py":
        "2026d99085619211b75366a820cf9614afed9fe5",
    "benchmarks/bugs/boltons_480/patch_roundtrip.py":
        "56c6aa5f0f3f71c4744e15150de58b9c45971908",
}


class FrozenCandidateSourceTests(unittest.TestCase):
    def test_every_local_candidate_patch_is_listed(self):
        discovered = {
            str(path.relative_to(ROOT))
            for path in (ROOT / "benchmarks" / "bugs").glob("*/patch*.py")
        }
        pinned = {
            path for path in FROZEN_BLOBS
            if path.startswith("benchmarks/bugs/")
        }
        self.assertEqual(discovered, pinned)

    def test_historical_candidates_remain_byte_for_byte_frozen(self):
        for relative_path, expected in FROZEN_BLOBS.items():
            with self.subTest(path=relative_path):
                content = (ROOT / relative_path).read_bytes()
                header = f"blob {len(content)}\0".encode("ascii")
                actual = sha1(header + content).hexdigest()
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
