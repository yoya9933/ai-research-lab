# Experiment 009: repair an independently reported, reproducible historical bug

Date: 2026-11-01
Report: https://github.com/python-humanize/humanize/issues/30
Frozen baseline on main: `58df7c5dcb480791fab4f7d76fa398e278470ebb`
Upstream source: `9528daf55fd7178c025f7294b8e349f8b3524175`
Status: candidate submitted for CI verification

## Hypothesis

The original `precisedelta` separates days, hours, and minutes **before** applying the caller's `%0.0f` rounding. Therefore 59.98 minutes is rendered as 60 minutes but is not carried into hours. It also chooses pluralization from the pre-rounded floating value, so 1.42 hours can render as “1 hours”.

## Candidate change

A [small patch](../benchmarks/bugs/humanize_30/patch.py) applied to a temporary, separately imported copy of the exact pinned source. For `%0.0f` with minimum `minutes` or `hours`, round the total duration to whole minimum units *before* decomposing into larger units. Leave other formats unchanged. The unmodified upstream baseline remains committed and tested.

## Predicted tests

| Case | Original output | Candidate expected output |
| --- | --- | --- |
| Reporter's 32399 seconds | `8 hours and 60 minutes` | `9 hours` |
| Commenter's 91500 seconds | `1 day and 1 hours` | `1 day and 1 hour` |
| Default precision | `8 hours, 59 minutes and 59 seconds` | Unchanged |
| Two-decimal minutes | `8 hours and 59.98 minutes` | Unchanged |

```bash
python -m benchmarks.bugs.humanize_30.reproduce
python -m benchmarks.bugs.humanize_30.reproduce --candidate
python -m unittest discover -s tests -v
```

## Limitations

This candidate fixes the **two reported whole-unit formatting cases**, not every `precisedelta` rounding mode or locale. The author read the public issue description but **has not read the upstream fixing patch** before preparing the candidate. Public issue text and model training data are potential sources of leakage, so this is **not a blind scientific benchmark**. This project does not claim to replace the actual upstream fix or to submit changes to that external repository.
