# Experiment 001: chat-authored debugging demonstration

Date: 2026-11-01
Baseline commit: `9beb8bf0cd4915f7d24af5bd2e5cce11e06c00dc`
Status: submitted for automated verification, **not blinded**
Model interface: ChatGPT conversation; no model API or paid model calls
Candidate: `lab/attempt_001.py`

## Question

Can a small chat-authored patch improve a fixed, deterministic debugging benchmark while preserving evidence in GitHub?

## Contamination disclosure

**The same assistant previously read both `lab/solutions.py` and the published test cases.** This exercise tests the repository workflow, **not independent AI debugging skill**, and cannot establish AI self-improvement or changes in reasoning capability. Answers are intentionally not described as blind.

## Hypotheses before running the candidate

- `clamp` has reversed nested `min`/`max` operations, so values above and within limits are wrong.
- `chunks` omits the final incomplete chunk because the loop's stop condition is too small.
- `factorial` stops multiplying before `n`, yielding an off-by-one error.

## Predicted outcome

- Buggy baseline: **11 of 24** published cases pass.
- Repairing the three selected functions: **16 of 24** pass.
- The seven other functions remain unchanged; no full benchmark pass is claimed.

## Reproduction

```bash
python -m unittest discover -s tests -v
python -m lab evaluate --module lab.buggy --output results/baseline.json
python -m lab evaluate --module lab.attempt_001 --output results/attempt_001.json
```

`tests/test_attempt_001.py` asserts the expected counts, requires all three selected functions to pass, and verifies all other case outcomes remain unchanged.

## Known limitations

Published cases are small and visible. A passing case is not a general correctness proof. The repair is deliberately partial and contaminated by prior access to reference implementations. A future controlled evaluation must use independently authored cases not exposed to the repairing model.
