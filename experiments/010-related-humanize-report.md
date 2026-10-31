# Experiment 010: another independently submitted report of the same underlying rounding defect

Date: 2026-11-01
New external report: [humanize issue #20](https://github.com/python-humanize/humanize/issues/20), submitted 2022-05-25.
Reused original pinned pre-fix source: `9528daf55fd7178c025f7294b8e349f8b3524175`
Related first report: [issue #30](https://github.com/python-humanize/humanize/issues/30)
Patch already frozen in main: `c2be95d34bd5271b90b851b38f5d02db00c67086`
Status: CI verified; candidate unchanged

## Human report

Calling `precisedelta(3633, minimum_unit="minutes", format="%0.0f")` was reported to produce `1 hour and 1 minutes`; expected `1 hour and 1 minute`. The user reported this on humanize v4.1.0.

## Verification plan

Re-run the **same untouched source snapshot** and **same already committed patch** on this separate user-provided case. Assert that the baseline still exhibits the plural error and that the candidate prints the requested singular.

```bash
python -m benchmarks.bugs.humanize_30.reproduce
python -m benchmarks.bugs.humanize_30.reproduce --candidate
python -m unittest discover -s tests -v
```

## Verified result

[GitHub Actions run #41224621330](https://github.com/yoya9933/ai-research-lab/actions/runs/41224621330) passed **43 unit tests**. The unchanged baseline printed `1 hour and 1 minutes`, while the same already committed candidate printed `1 hour and 1 minute`. All prior checks also passed.

## Interpretation

The reports #20 and #30 were written by separate external users, but both exhibit zero-decimal formatting and incorrect unit decomposition/pluralization. They are **two reports of a likely shared root cause, not two independent root-cause defects**. The reporter's case was public well before this model was trained; this is not a blind experiment or proof of general model improvement.
