# Exercism Python: pinned external benchmark

**Upstream:** https://github.com/exercism/python

**Pinned commit:** [`6105f6d9d3ef66ce3d5c8f529d2882af3d76b706`](https://github.com/exercism/python/commit/6105f6d9d3ef66ce3d5c8f529d2882af3d76b706)

**License:** MIT, Copyright (c) 2021 Exercism. See the adjacent [LICENSE](LICENSE), reproduced from upstream.

## What is copied

These **unmodified upstream files** are copied from the pinned commit:

| Exercise | Starter source | Test source |
| --- | --- | --- |
| Isogram | [isogram.py](https://github.com/exercism/python/blob/6105f6d9d3ef66ce3d5c8f529d2882af3d76b706/exercises/practice/isogram/isogram.py) | [isogram_test.py](https://github.com/exercism/python/blob/6105f6d9d3ef66ce3d5c8f529d2882af3d76b706/exercises/practice/isogram/isogram_test.py) |
| RNA Transcription | [rna_transcription.py](https://github.com/exercism/python/blob/6105f6d9d3ef66ce3d5c8f529d2882af3d76b706/exercises/practice/rna-transcription/rna_transcription.py) | [rna_transcription_test.py](https://github.com/exercism/python/blob/6105f6d9d3ef66ce3d5c8f529d2882af3d76b706/exercises/practice/rna-transcription/rna_transcription_test.py) |
| Difference of Squares | [difference_of_squares.py](https://github.com/exercism/python/blob/6105f6d9d3ef66ce3d5c8f529d2882af3d76b706/exercises/practice/difference-of-squares/difference_of_squares.py) | [difference_of_squares_test.py](https://github.com/exercism/python/blob/6105f6d9d3ef66ce3d5c8f529d2882af3d76b706/exercises/practice/difference-of-squares/difference_of_squares_test.py) |

The starter modules are intentionally incomplete upstream, not examples of genuine bugs from deployed software. The 29 tests are independently authored or compiled by Exercism contributors, **not independently blinded from the model**. This assistant read their published assertions before writing its candidate and must not claim otherwise.

## Run locally (no network, API, SDK or paid tokens)

```bash
python -m benchmarks.exercism.runner starter --output results/exercism-starter.json
```

The first chat-authored candidate was committed in a **separate version** after the starter corpus:

```bash
python -m benchmarks.exercism.runner attempt_001 --output results/exercism-attempt.json --require-all-pass
python -m lab.report results/exercism-starter.json results/exercism-attempt.json
```

The runner executes only checked-in, named Python modules. It is **not a sandbox** and must not evaluate arbitrary user-submitted code.
