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
    # More-itertools candidate committed before the 574-case follow-up suite:
    # 33cd99acfdf62b13033db865f4b0302a6a7ebd96.
    "benchmarks/bugs/more_itertools_1342/patch.py":
        "b26e35b35a8911e8a117e3f7f10a703291b4b585",
}


class FrozenCandidateSourceTests(unittest.TestCase):
    def test_historical_candidates_remain_byte_for_byte_frozen(self):
        for relative_path, expected in FROZEN_BLOBS.items():
            with self.subTest(path=relative_path):
                content = (ROOT / relative_path).read_bytes()
                header = f"blob {len(content)}\0".encode("ascii")
                actual = sha1(header + content).hexdigest()
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
