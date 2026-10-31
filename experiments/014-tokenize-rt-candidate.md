# Experiment 014: tokenize-rt no-EOL offset candidate

- **Date:** 2026-11-01 (Taiwan).
- **Public original issue:** https://github.com/asottile/tokenize-rt/issues/33
- **Frozen source:** `asottile/tokenize-rt@7f89433be049d73e189a903485a93bdf3e56f1a0` (before public fix), MIT; copied module hash `98f72cee984b23f138dd88208dbdb438e1745673`.
- **Baseline frozen in Git:** [PR #26](https://github.com/yoya9933/ai-research-lab/pull/26), squash commit `b450fb5b6917a0f038a297940892d984fd77dda3`; six cases were asserted before candidate code.
- **Initial hypothesis:** for the artificial terminal `NEWLINE` without actual EOL, Python's tokenizer supplies an empty `line`, so `len(line[:scol].encode())` returns zero even when `scol` is the end of a nonempty input line.
- **Intended local candidate:** when `tok_name == "NEWLINE"` and `tok_text == ""`, take the UTF-8 prefix length from the original `lines[sline]`; otherwise preserve the original computation. Only a temporary bytecode-cache-free copy is changed, using an exact one-occurrence anchor.
- **Same six inputs and expected candidate evidence:** three no-EOL incorrect offsets corrected (1, 3, and 4 UTF-8 bytes for ASCII number, assignment, and Unicode identifier), three ordinary EOL controls unchanged, and roundtrip preserved for all six. CI status is recorded in the PR, not presumed here.
- **Exposure/limitations:** The upstream report and existence of upstream fix were already public. These are the same hand-selected regression inputs before and after, not blind, held-out, repeated AI trials or a claim of model capability growth. Source is a one-file subset; Python stdlib / GitHub Actions Ubuntu, no pytest or network installation.
- **Earlier baseline harness failure:** [CI #41252891585](https://github.com/yoya9933/ai-research-lab/actions/runs/41252891585) failed 3 of 79 tests because the author encoded the three EOL controls' expected newline as literal `\\n` instead of an actual newline. The corrected baseline passed [PR CI #41252930201](https://github.com/yoya9933/ai-research-lab/actions/runs/41252930201); the failed run remains linked in PR #26.
