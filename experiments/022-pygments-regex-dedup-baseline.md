# Experiment 022: accepted Pygments regex deduplication — frozen baseline

Date: 2026-11-01. External project `pygments/pygments`.

- Research question: does the accepted upstream [PR #3190](https://github.com/pygments/pygments/pull/3190)
  demonstrate a distinct real defect in output canonicalization on the exact
  unmodified source, without relying on the upstream installation?
- Copyright/license: BSD; upstream `LICENSE` Git blob
  `446a1a805c8a949579fb8a9799f2bec7777349dc`.
- Frozen pre-fix commit: `c97c0b54f58d496e34f4b37eb9d0c482e79e21b3`;
  `pygments/regexopt.py` Git blob `9010eb3fb517ff4134b4f52581179fa80b0f7540`.
  Only this standalone stdlib module was copied, not the complete package.
- Investigator-visible upstream bug description: `regex_opt` does not
  deduplicate input; a repeated string can form a redundant character class.
  The published PR already disclosed its fix. The seven investigator-written
  probes therefore **do not count as blind evaluation**.
- Pre-CI hypothesis: three duplicated input lists should produce a different
  pattern than the same sets with duplicates removed; four controls should
  produce the same patterns. The original patterns should still match the
  listed words. The baseline and license SHA checks must hold.
- Commands: `python -m benchmarks.bugs.pygments_3190.reproduce` and
  `python -m unittest tests.test_pygments_3190 -v` under the full GitHub
  Actions standard-library test discovery.
- Results: **await CI**. If any original behavior differs, preserve the
  failure and revisit the hypothesis. Baseline passing is reproduction,
  not repair, and no performance/throughput claim is tested.
