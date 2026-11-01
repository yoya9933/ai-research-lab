"""Post-freeze deterministic regexopt matrix; frozen candidate stays unchanged."""

import json

from benchmarks.bugs.humanize_30.reproduce import observe as run_script
from .reproduce import VENDOR

SCRIPT = """
import json
import re
from regexopt import regex_opt

TOKENS = ("", "a", "b", "ab", "a+", "[", chr(92), "é")
PROBES = tuple(dict.fromkeys(TOKENS + ("x", "aa", "ba", "ab+", "[a", "éa")))
inputs = [[a, a, b] for a in TOKENS for b in TOKENS]
inputs.extend([[a] for a in TOKENS])

records = []
for index, words in enumerate(inputs):
    for mode, prefix, suffix in (("plain", "", ""), ("anchored", "^", "$")):
        pattern = regex_opt(words, prefix=prefix, suffix=suffix)
        canonical = regex_opt(sorted(set(words)), prefix=prefix, suffix=suffix)
        records.append({
            "index": index,
            "mode": mode,
            "words": words,
            "pattern": pattern,
            "canonical": canonical,
            "matched": [bool(re.fullmatch(pattern, word)) for word in PROBES],
            "expected": [word in words for word in PROBES],
        })
print(json.dumps(records, ensure_ascii=False))
"""


def observe(vendor=VENDOR):
    """Run 144 ordered input combinations on an isolated trusted local module."""
    return run_script(vendor=vendor, script=SCRIPT)


if __name__ == "__main__":
    rows = observe()
    print(json.dumps({
        "rows": len(rows),
        "duplicate_rows": sum(len(row["words"]) > 1 for row in rows),
        "control_rows": sum(len(row["words"]) == 1 for row in rows),
        "noncanonical": sum(row["pattern"] != row["canonical"] for row in rows),
    }, indent=2))
