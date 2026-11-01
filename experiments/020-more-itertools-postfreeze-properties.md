# Experiment 020 — post-freeze property matrix for more-itertools #1342

Date: 2026-11-01. **Not a blind model benchmark.**

## Chronology and source

- The independently filed and upstream-merged [more-itertools PR #1342](https://github.com/more-itertools/more-itertools/pull/1342)
  was publicly available before the candidate was written.
- The original function-only excerpt is from MIT-licensed upstream commit
  `4aeb4338ae1407d8da9723e86da99efeb446f719`, as described in
  [the baseline](../benchmarks/bugs/more_itertools_1342/README.md). This
  is **not** a complete upstream package or its original pytest suite.
- The local fix was frozen in [PR #44](https://github.com/yoya9933/ai-research-lab/pull/44)
  at source commit `33cd99acfdf62b13033db865f4b0302a6a7ebd96`
  (patch Git blob `b26e35b35a8911e8a117e3f7f10a703291b4b585`),
  merged into `main` at `3d0cc1c0bb500bbf2de604305c9cff269fc92dd7`.
- The **current property matrix was authored after that candidate was frozen**;
  the Git blob check in `tests/test_frozen_candidate_sources.py` protects
  against accidental subsequent changes to that candidate's source bytes.

## Hypothesis and verification

With the candidate unchanged, test input lengths 0–30 and chunk sizes -3–8:
**372 deterministic input pairs** on both the pinned baseline and candidate.
For **248 positive-size pairs**, outputs should be byte-for-byte equivalent
in JSON and independently satisfy ordering, no loss/duplication, exhaustion,
`ceil(length / size)` chunk count, maximum size and size imbalance <= 1.
For **31 zero-size pairs**, candidate output should be empty without
consumption; for **93 negative-size pairs**, it should raise
`ValueError('n must be at least 0')` without consuming the input.
The original baseline's known invalid-size behavior is recorded but not
mistaken for a regression.

Run `python -m unittest tests.test_more_itertools_1342_followup -v`
or the repository's full `python -m unittest discover -s tests -v`.
The [PR #45 CI run](https://github.com/yoya9933/ai-research-lab/actions/runs/41285743823)
and the [post-merge main run](https://github.com/yoya9933/ai-research-lab/actions/runs/41285778031)
both completed **success**. The five focused standard-library test methods
therefore verified the declared **248 unchanged positive-size controls**,
**31 zero-size cases** with no source consumption, and **93 negative-size
cases** with the specific error and no consumption, over 372 ordered inputs.
These are bounded test observations, not a confidence interval or independent
model trials.

## Limits

These 372 test inputs are **not** 372 independent bug reports or AI trials.
The candidate was informed by a public fix, and the property oracle was
written by the same assistant after the fix was already visible. This
checks bounded behavior for a standalone function excerpt only;
it does not prove correct behavior for arbitrary iterables, non-integer
size values, other Python versions, or the full third-party library.
No model APIs, extra package installs, external writes, or blind claims.

## Targeted, non-overlapping edge checks after PR #45

[PR #45](https://github.com/yoya9933/ai-research-lab/pull/45)
merged a 372-pair property matrix for sizes -3..8 and lengths 0..30.
A concurrent [PR #46](https://github.com/yoya9933/ai-research-lab/pull/46)
covered overlapping files and was CI-green but deliberately **closed
without merge** to avoid duplicate test modules.

The follow-on `tests/test_more_itertools_1342_guard_boundaries.py` tests
**18 previously untested buffer-threshold inputs**: sizes 9..14 and
lengths one below, equal to, and one above `(n-1)*(n-2)`. It also
checks **two poisoned iterables** whose `__iter__` raises: the original
source consults them, while the frozen candidate must handle zero
and negative sizes before calling them. Both versions use the same
inputs, and no candidate source changes. This is not blind or a
representative performance benchmark.
