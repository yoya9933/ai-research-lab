# Experiment 004: external task intake

Date: 2026-11-01
Status: starter corpus added, repair attempt not yet recorded
Upstream: https://github.com/exercism/python
Pinned upstream commit: `6105f6d9d3ef66ce3d5c8f529d2882af3d76b706`
Authorization: upstream MIT license, included in `benchmarks/exercism/LICENSE`

## Provenance and limitations

This adds three **externally authored programming exercises**, with 29 upstream unit tests. These are not software defects reported by real users; an upstream starter explicitly contains `pass`. Therefore this is an exercise-completion benchmark, **not real-world bug fixing**.

The assistant has already seen the published test cases, so the upcoming repair is **not blind**. Model pretraining contamination cannot be excluded. Reproducing these results with the same tests cannot establish that ChatGPT improved its general capability.

## Expected baseline

The original upstream starter functions all return `None`, so their 29 assertions should fail. CI checks the exact test count and result. A repair candidate will be committed separately to make the chronology visible.
