# Experiment 011: reproduce a different humanize defect family

Date: 2026-11-01
Report: https://github.com/python-humanize/humanize/issues/333
Pinned original: `9528daf55fd7178c025f7294b8e349f8b3524175`
Status: proposed baseline; GitHub Actions outcome not yet recorded.

## Hypothesis and explicit predictions

The 2025 original `naturaldelta` calls `int(value)` inside a
`try` that catches `ValueError` and `TypeError`, but not
`OverflowError`. Per the independent reporter's reproduction,
both positive and negative infinity should raise `OverflowError` instead
of returning a string. NaN should return `"nan"`, an ordinary 30-second
duration should return `"30 seconds"`, and an oversized **finite** value
should still raise `OverflowError` when constructing a `timedelta`.

## Reproducibility

```sh
python -m benchmarks.bugs.humanize_333.reproduce
python -m unittest discover -s tests -v
```

The original MIT-licensed 2025 source is reused unchanged from
`benchmarks/bugs/humanize_30/upstream`. Any future candidate must
live in a temporary separate copy, preserve finite-overflow behavior, and
have its own follow-up tests and CI evidence.

## Exposure and limits

Issue #333 was filed on 2026-06-28, after the pinned upstream source date.
Its report includes a proposed remedy, and the author of this intake has
read the report. Therefore these cases are **not blind**, and this replay
cannot isolate model ability from exposure. This baseline stage records
no repair score, no upstream contribution, and no CI success in advance.
