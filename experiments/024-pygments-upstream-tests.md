# Experiment 024: upstream Pygments regression cases after candidate freeze

Date: 2026-11-01. **Not blind**: the accepted upstream fix
`sorted(set(strings))` was known before the candidate was written.

- Pinned BSD pre-fix source: `c97c0b54f58d496e34f4b37eb9d0c482e79e21b3`;
  original module Git blob `9010eb3fb517ff4134b4f52581179fa80b0f7540`.
  Baseline merged via [PR #49](https://github.com/yoya9933/ai-research-lab/pull/49).
- Previously frozen candidate: [PR #50](https://github.com/yoya9933/ai-research-lab/pull/50),
  candidate commit `94a4c403456de093d3350d1d65fb8939f1873849`,
  merged `cfee0d1f07f65172385b1df0cb27114a10dd080b`;
  patch Git blob `59d075d0763feb68fb2385b71f95cf2835c68afe`.
  [Candidate PR CI](https://github.com/yoya9933/ai-research-lab/actions/runs/41286237343)
  and [main CI](https://github.com/yoya9933/ai-research-lab/actions/runs/41286264647)
  both passed on earlier seven investigator-written observations.
- **After candidate freeze**, read upstream [PR #3190 test file](https://github.com/pygments/pygments/blob/64226095eb736dbf23e16786f04c82f3a3a86b92/tests/test_regexopt.py),
  Git blob `f2d566541c37ac8b7ab35b239bdea4aeea565b56`.
  Copy exact function bodies `test_duplicates` and
  `test_duplicate_single_chars`, only adapting the import.
- **Pre-CI expectation:** 0/2 original assertions passing on pinned
  pre-fix source; 2/2 passing on unchanged candidate. The harness
  suppresses the original tests' `print` statements for JSON capture,
  preserving all their original assertions.
- Reproduce with `python -m unittest tests.test_pygments_3190_upstream -v`.
  Do not report actual counts until GitHub Actions proves them.

Limits: This imports two original third-party test functions, **not the
complete upstream test suite**. Source/test exposure order is better
controlled than before, but the public patch and pretrained model
knowledge remain visible; not an independently administered blind task,
speed measurement, or general capability trial.
