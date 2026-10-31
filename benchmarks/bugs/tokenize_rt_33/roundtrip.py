"""Evaluate a second candidate for a residual *investigator-discovered* defect."""

import json
from pathlib import Path
import tempfile

from .followup import EXPECTED_OFFSETS, observe
from .patch import make_candidate
from .patch_roundtrip import make_candidate_with_roundtrip

ROUNDTRIP_CASES = ("trailing_space", "unicode_space")


def main():
    original = observe()
    with tempfile.TemporaryDirectory() as directory:
        first = observe(make_candidate(Path(directory) / "first"))
        extended = observe(
            make_candidate_with_roundtrip(Path(directory) / "extended")
        )
    print(json.dumps({
        "source": "investigator-discovered trailing-whitespace roundtrip gap",
        "preexisting_upstream_roundtrip_failures": [
            k for k, v in original.items() if not v["roundtrip"]
        ],
        "frozen_first_candidate_roundtrip_failures": [
            k for k, v in first.items() if not v["roundtrip"]
        ],
        "extended_candidate_roundtrip_failures": [
            k for k, v in extended.items() if not v["roundtrip"]
        ],
        "roundtrip_fixed": sum(
            not first[k]["roundtrip"] and extended[k]["roundtrip"]
            for k in EXPECTED_OFFSETS
        ),
        "roundtrip_regressed": sum(
            first[k]["roundtrip"] and not extended[k]["roundtrip"]
            for k in EXPECTED_OFFSETS
        ),
        "first_candidate": first,
        "extended_candidate": extended,
        "inputs": len(EXPECTED_OFFSETS),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
