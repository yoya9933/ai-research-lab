# Experiment 005: unblinded external exercise completion

Date: 2026-11-01
External benchmark baseline commit: [2167eae](https://github.com/yoya9933/ai-research-lab/commit/2167eae37aff936b0cc9895f4a8add21bbf2dc14)
Source: [Exercism Python pinned commit](https://github.com/exercism/python/commit/6105f6d9d3ef66ce3d5c8f529d2882af3d76b706)
Candidate module set: `benchmarks/exercism/attempt_001/`
Status: awaiting GitHub Actions verification

## Method and predictions

The assistant read the three public task descriptions and upstream tests. It then created the smallest standard-library implementations of: `is_isogram` (case-insensitive alphabetic uniqueness), `to_rna` (DNA->RNA complement), and sum-of-squares arithmetic.

Prediction: the unchanged upstream starters fail all **29** public unit tests, and the chat-authored attempt passes all **29**. Run the pinned offline tests and `lab.report` to check for regressions.

```bash
python -m benchmarks.exercism.runner starter --output results/exercism-starter.json
python -m benchmarks.exercism.runner attempt_001 --output results/exercism-attempt.json --require-all-pass
python -m lab.report results/exercism-starter.json results/exercism-attempt.json
```

## Interpretation

This is evidence of completing three **published educational exercises**, not real-world debugging and **not a blind evaluation**. Public tests were exposed before the attempt, and the assistant may have encountered similar tasks during training. A 29/29 score does not prove improved reasoning ability. Git commits preserve when external fixtures were imported and when the candidate was added.
