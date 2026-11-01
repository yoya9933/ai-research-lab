# more-itertools: accepted chunked_even size-validation bug (PR #1342)

- **Public external source:** [more-itertools PR #1342](https://github.com/more-itertools/more-itertools/pull/1342), opened 2026-10-26 and merged upstream on 2026-10-30. This is a real upstream-accepted repair, unlike rejected issue #1339.
- **Frozen pre-fix commit:** [4aeb4338ae1407d8da9723e86da99efeb446f719](https://github.com/more-itertools/more-itertools/commit/4aeb4338ae1407d8da9723e86da99efeb446f719) (2026-10-14), which is the original PR's base commit. Original `more_itertools/more.py` Git blob: `9c56ab37558733ece94d676f71d502d8048bc1d5`.
- **Reused third-party code:** The entire original `chunked_even(iterable, n)` **function body and docstring are copied verbatim** into [upstream/chunked_even.py](upstream/chunked_even.py). Only `from itertools import islice` is added to make that excerpt importable standalone. **This is a function-only snapshot, not an unchanged full upstream package** (the original file is 175 KB and also imports a 46 KB recipes module). The excerpt's local Git blob is `1335bf7be6f2d884791bb1168a012c6257887fb8`, checked in offline tests. The original [MIT LICENSE](LICENSE) is preserved, and its Git blob
`0a523bece3e50519653c4d7a38399baa487fefa1` was independently
verified with GitHub MCP against the same upstream pre-fix commit;
both the local function excerpt and the exact original license bytes
are checked by offline CI tests.
- **Hypothesis from public patch:** For `n=0`, the current generator takes two source items and eventually raises `ValueError`; for negative `n`, it consumes up to six items and raises a low-level `islice` error. These cases should instead yield no chunks without consuming, or raise a domain-specific `ValueError` before consuming.
- **Reproduce baseline:** `python -m benchmarks.bugs.more_itertools_1342.reproduce` or `python -m unittest tests.test_more_itertools_1342 -v`. The 10 fixed observations cover five invalid-size/ignored-input manifestations and five ordinary-size/type controls. Each includes source remainder when applicable.
- **Scope / limits:** The reporter's public PR and upstream test patch were **read before** this reproduction; our ten probes are investigator-authored, not blind or upstream's complete original tests. We only test the exact imported function excerpt, not the full upstream package; dependencies and import side effects of that package are therefore **not** covered. The local pinned excerpt is executed as trusted Python code, not a sandbox. Baseline CI passed in [PR #43](https://github.com/yoya9933/ai-research-lab/pull/43); a first integrity-test failure was fixed before merging (see [experiment 019](../../../experiments/019-more-itertools-chunk-size.md)). No paid APIs, model keys, or upstream code changes.

A green **baseline** check means the incorrect historical behavior is reproduced; it does **not** demonstrate repair or an improvement in AI reasoning.

## Separate accepted-fix reconstruction (unblinded)

`patch.py` makes a disposable copy of the frozen upstream function excerpt,
excludes inherited bytecode caches, and inserts the exact two input-size
guards proposed in the already-public upstream PR #1342. An exact anchor
check refuses unknown source changes. The original file remains unchanged.

Run `python -m unittest tests.test_more_itertools_1342_candidate -v`.
Across the **same ten baseline observations**, four change to the expected
results (two zero-size failures, one negative-size source-consumption
failure, and the zero-size ignored noniterable), while six coarse
observations remain identical. The negative/empty input still raises
`ValueError` in both versions, so its *message* change is checked
separately. The candidate additionally checks that all negative inputs,
including `None`, produce the specific `n must be at least 0`
validation error before touching the source.

These tests are investigator-authored with the upstream solution already
public. This is **not blind**, not a model performance trial, and not a
complete upstream-package regression run.

## Post-candidate property check

After the local candidate was frozen in PR #44, a separate
[372-input property matrix](../../../experiments/020-more-itertools-postfreeze-properties.md)
was authored: 248 ordinary-size regression controls, 31 zero-size and
93 negative-size boundary cases. Run
`python -m unittest tests.test_more_itertools_1342_followup -v`.
The frozen patch source is hash-checked. This is **post-freeze, not blind**.
