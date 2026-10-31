# Second external exercise trial

Three Exercism Python exercises: Luhn, Pangram, Armstrong Numbers.

- Upstream: https://github.com/exercism/python
- Pinned upstream: [6105f6d9d3ef66ce3d5c8f529d2882af3d76b706](https://github.com/exercism/python/commit/6105f6d9d3ef66ce3d5c8f529d2882af3d76b706)
- Copyright and license: [Exercism MIT License](../LICENSE)
- Before candidate code was frozen, only written problem instructions and starter files were read, not the upstream test files.
- Candidate: `attempt_002/`; original stubs: `starter/`
- Do not edit `attempt_002/` after committing it. Any corrections belong in a separate attempt.
- See [Experiment 006](../../../experiments/006-pretest-candidate.md) for evidence and limits.

These are public educational tasks, not real-world software bug reports.

## Published upstream tests (imported after candidate commit)

Exact test files: [Luhn](https://github.com/exercism/python/blob/6105f6d9d3ef66ce3d5c8f529d2882af3d76b706/exercises/practice/luhn/luhn_test.py), [Pangram](https://github.com/exercism/python/blob/6105f6d9d3ef66ce3d5c8f529d2882af3d76b706/exercises/practice/pangram/pangram_test.py), [Armstrong Numbers](https://github.com/exercism/python/blob/6105f6d9d3ef66ce3d5c8f529d2882af3d76b706/exercises/practice/armstrong-numbers/armstrong_numbers_test.py). They total **44 methods**, are copied verbatim, and remain under the upstream MIT license.

```bash
python -m benchmarks.exercism.runner starter_002 --output results/starter_002.json
python -m benchmarks.exercism.runner attempt_002 --output results/attempt_002.json
python -m lab.report results/starter_002.json results/attempt_002.json
```
