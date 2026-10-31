# Third upstream project: tokenize-rt issue #33 (historical baseline)

- **Externally reported issue:** [asottile/tokenize-rt #33](https://github.com/asottile/tokenize-rt/issues/33), opened 2019-10-07 and closed 2021-10-21.
- **Pinned unfixed upstream commit:** [`7f89433be049d73e189a903485a93bdf3e56f1a0`](https://github.com/asottile/tokenize-rt/commit/7f89433be049d73e189a903485a93bdf3e56f1a0) (2021-10-21 03:25 UTC). The public fix commit `0d214dc28105c35d866e98212e9953221a652d19` followed at 03:33 UTC; this benchmark copied its parent **before** that fix.
- **Provenance/licensing:** `upstream/tokenize_rt.py` is the unmodified upstream Git blob `98f72cee984b23f138dd88208dbdb438e1745673`, with its original [MIT LICENSE](LICENSE), Git blob `522fbe20b89911bb8d68b4a684a51225dd571764`. The offline CI tests verify both byte-for-byte; only this single module is vendored.
- **Original reported defect:** When source has no terminal newline, `tokenize_rt.src_to_tokens("1")` gives its synthetic empty `NEWLINE` token UTF-8 byte offset **0** rather than **1**. A valid byte offset must be measured at the end of the line.
- **Hypothesis:** The old implementation computes an empty `NEWLINE` offset from a `line` value that can be empty, instead of the preceding token's end position. This is an investigator inference from source and the already-public report; no blind claim.
- **Reproduce:** `python -m benchmarks.bugs.tokenize_rt_33.reproduce` and `python -m unittest tests.test_tokenize_rt_33 -v`. A trusted subprocess imports only the pinned module and compares six inputs: three defective no-EOL samples (number, assignment, non-ASCII identifier) and three EOL controls. Each also checks roundtrip preservation. The baseline **expects the buggy output**, not a repair.

**Limits:** The upstream original tests use pytest; no external packages/tests are installed or silently represented as run. These six samples are reporter/investigator-visible, not held-out. Only Python 3.11 on GitHub Ubuntu is tested; this is a separate upstream codebase but not independent blind performance evidence. No model API, key, other agent or external code execution outside GitHub Actions.

## Isolated local candidate (unblinded)

`patch.py` copies the frozen single-module snapshot to a temporary directory
while excluding inherited Python bytecode caches, and changes only the empty
synthetic `NEWLINE` offset computation to use the original source line.
The exact upstream anchor must match once; the vendored module and MIT
license remain byte-for-byte unchanged.

Run `python -m unittest tests.test_tokenize_rt_33_candidate -v`. It
repeats the **same six inputs**: three no-EOL offsets should change from 0
to 1, 3, and 4 UTF-8 bytes, while three EOL offsets and all six
roundtrips should remain unchanged. These are visible, correlated
investigator-controlled samples, **not** blind or independent ability scores.

## Post-commit edge suite (2026-11-01)

The local issue #33 candidate was already merged in
[PR #27](https://github.com/yoya9933/ai-research-lab/pull/27)
before the seven new edge inputs were authored. The candidate is **not
modified** for this follow-up. Run
`python -m benchmarks.bugs.tokenize_rt_33.followup` for full original
and candidate JSON records, corrected/regressed offsets and any remaining
source-roundtrip failures; the same assertions run under standard-library
unittest discovery. The extra cases include trailing spaces, multibyte
Unicode, multiline input, LF, CRLF and an empty input. Report roundtrip
limitations rather than hiding them. This is a post-commit *conversation
exposure* check, **not** independent or blinded evaluation.
