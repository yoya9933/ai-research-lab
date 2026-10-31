"""Reproduce external tokenize-rt issue #33 on the unfixed pinned source.

The subprocess imports only the copied, MIT-licensed module; no downloads.
"""

import json
import os
from pathlib import Path
import subprocess
import sys

UPSTREAM_COMMIT = "7f89433be049d73e189a903485a93bdf3e56f1a0"
ISSUE = "https://github.com/asottile/tokenize-rt/issues/33"
VENDOR = Path(__file__).resolve().parent / "upstream"

SCRIPT = """
import json
import os
from pathlib import Path
import tokenize_rt

assert Path(tokenize_rt.__file__).resolve() == Path(
    os.environ["REPLAY_TOKENIZER"]
).resolve()
samples = {
    "number_without_eol": "1",
    "assignment_without_eol": "x=1",
    "unicode_without_eol": "ä=1",
    "number_with_eol": "1\\n",
    "assignment_with_eol": "x=1\\n",
    "unicode_with_eol": "ä=1\\n",
}
out = {}
for label, source in samples.items():
    tokens = tokenize_rt.src_to_tokens(source)
    newline = [token for token in tokens if token.name == "NEWLINE"]
    assert len(newline) == 1
    token = newline[0]
    out[label] = {
        "newline": [token.line, token.utf8_byte_offset, token.src],
        "roundtrip": tokenize_rt.tokens_to_src(tokens) == source,
    }
print(json.dumps(out, ensure_ascii=False))
"""


def observe(vendor=VENDOR, script=SCRIPT):
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(vendor)
    environment["REPLAY_TOKENIZER"] = str(
        Path(vendor) / "tokenize_rt.py"
    )
    process = subprocess.run(
        [sys.executable, "-c", script], env=environment,
        capture_output=True, text=True, check=True, timeout=15,
    )
    return json.loads(process.stdout)


def main():
    print(json.dumps({
        "external_report": ISSUE, "upstream_commit": UPSTREAM_COMMIT,
        "variant": "unchanged historical baseline", "observed": observe(),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
