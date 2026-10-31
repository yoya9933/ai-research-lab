"""Post-candidate-freeze edge suite for the historical tokenize-rt no-EOL issue."""

import json
from pathlib import Path
import tempfile

from benchmarks.bugs.tokenize_rt_33.reproduce import (
    VENDOR,
    observe as run_script,
)

SCRIPT = """
import json
import os
from pathlib import Path
import tokenize_rt

assert Path(tokenize_rt.__file__).resolve() == Path(
    os.environ["REPLAY_TOKENIZER"]
).resolve()
samples = {
    "trailing_space": "x=1 ",
    "unicode_space": "ä=1 ",
    "multiline_no_eol": "x=1" + chr(10) + "ä=2",
    "unicode_string_no_eol": "s='😀'",
    "multiline_lf": "x=1" + chr(10) + "ä=2" + chr(10),
    "unicode_crlf": "ä=1" + chr(13) + chr(10),
    "empty_input": "",
}
out = {}
for label, source in samples.items():
    tokens = tokenize_rt.src_to_tokens(source)
    newlines = [token for token in tokens if token.name == "NEWLINE"]
    out[label] = {
        "offset": newlines[-1].utf8_byte_offset if newlines else None,
        "roundtrip": tokenize_rt.tokens_to_src(tokens) == source,
    }
print(json.dumps(out, ensure_ascii=False))
"""

EXPECTED_OFFSETS = {
    "trailing_space": 4,
    "unicode_space": 5,
    "multiline_no_eol": 4,
    "unicode_string_no_eol": 8,
    "multiline_lf": 4,
    "unicode_crlf": 4,
    "empty_input": None,
}
NEW_NO_EOL = (
    "trailing_space", "unicode_space",
    "multiline_no_eol", "unicode_string_no_eol",
)


def observe(vendor=VENDOR):
    return run_script(vendor=vendor, script=SCRIPT)


def main():
    from benchmarks.bugs.tokenize_rt_33.patch import make_candidate

    original = observe()
    with tempfile.TemporaryDirectory() as directory:
        candidate = observe(make_candidate(Path(directory) / "patched"))

    fixed = sum(
        original[key]["offset"] != expected and candidate[key]["offset"] == expected
        for key, expected in EXPECTED_OFFSETS.items()
    )
    regressed = sum(
        original[key]["offset"] == expected and candidate[key]["offset"] != expected
        for key, expected in EXPECTED_OFFSETS.items()
    )
    print(json.dumps({
        "source": "tokenize-rt issue #33, post-candidate-freeze investigator tests",
        "sample_count": len(EXPECTED_OFFSETS),
        "offsets_fixed": fixed,
        "offsets_regressed": regressed,
        "original": original,
        "candidate": candidate,
        "original_roundtrip_failures": [
            key for key, result in original.items() if not result["roundtrip"]
        ],
        "candidate_roundtrip_failures": [
            key for key, result in candidate.items() if not result["roundtrip"]
        ],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
