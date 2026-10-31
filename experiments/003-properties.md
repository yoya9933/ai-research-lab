# Experiment 003: deterministic property checks

Date: 2026-11-01
Frozen repair: `lab.attempt_001` (committed before these tests)
Status: pending CI verification; **not a blinded experiment**

## Question

Do the three already repaired functions behave according to their specifications on more than a few hand-authored examples?

## Tests and independent oracles

- `clamp`: **147** combinations of lower/upper bounds and input values. Expected result is defined by piecewise interval logic.
- `chunks`: **248** combinations of input length and chunk size. Checks lossless flattening and exact chunk lengths.
- `factorial`: **16** non-negative integer values checked against Python's `math.factorial`.

Total: **411 deterministic property inputs** across three unittest methods. These are *not* 411 independent AI experiments.

The same inputs are also fed to the original buggy implementations, which must fail at least one check per function. Candidate implementation is unchanged.

## Reproduction

```bash
python -m unittest discover -s tests -p test_properties.py -v
python -m unittest discover -s tests -v
```

## Limits

Property checks are stronger than the 24 published examples but still cover only bounded integer domains and the three selected functions. The author of the repair also wrote these tests and previously saw the reference answer key. This tests engineering behavior, not unbiased AI performance.
