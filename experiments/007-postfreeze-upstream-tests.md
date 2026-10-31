# Experiment 007: upstream tests imported after candidate freeze

Date: 2026-11-01
Frozen candidate commit on main: [f714ff6](https://github.com/yoya9933/ai-research-lab/commit/f714ff61474145f50036a6a77351baf0e441ff93)
Source commit: [Exercism Python 6105f6d9d3ef66ce3d5c8f529d2882af3d76b706](https://github.com/exercism/python/commit/6105f6d9d3ef66ce3d5c8f529d2882af3d76b706)
Status: CI verified; candidate remained unchanged

## Protocol

The Luhn, Pangram and Armstrong Numbers implementations were committed and merged *before* the assistant fetched any of these exercises' upstream test file content. This PR imports three **unmodified original test files** containing **44 test methods** (23 + 12 + 9). A separate runner track compares the original upstream stubs to the **unchanged** candidate.

```bash
python -m benchmarks.exercism.runner starter_002 --output results/starter_002.json
python -m benchmarks.exercism.runner attempt_002 --output results/attempt_002.json
python -m lab.report results/starter_002.json results/attempt_002.json
```

Any failures must be recorded. Do not alter `trial_002/attempt_002/` to improve the frozen score; use `attempt_003/` for later repairs.

## Verified outcomes

[GitHub Actions run #41222595587](https://github.com/yoya9933/ai-research-lab/actions/runs/41222595587) ran **31 unit tests** successfully, then evaluated the second trial: `starter_002: 0/44` and frozen `attempt_002: 44/44`. The comparator reported **44 fixes and 0 regressions** on these tests. There were no changes to `attempt_002` after its earlier merge.

This measures performance on this published suite, not future or unseen software defects.

## Limitations

External authorship and commit chronology can be verified. This is *not* a double-blind or training-contamination-free evaluation: both tasks and tests are publicly available and the model may have encountered them before. Educational exercise completion is not real-world defect repair.
