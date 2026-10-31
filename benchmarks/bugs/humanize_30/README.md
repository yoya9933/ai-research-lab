# Real-world issue reproduction: python-humanize/humanize #30

- **External report:** https://github.com/python-humanize/humanize/issues/30
- **Title:** precisedelta unusual results when rounding
- **Reported:** 2022-06-28; upstream subsequently closed it with a fix on 2025-08-25.
- **Frozen unfixed source:** [9528daf55fd7178c025f7294b8e349f8b3524175](https://github.com/python-humanize/humanize/commit/9528daf55fd7178c025f7294b8e349f8b3524175) from 2025-03-16 (before the upstream rounding fix).
- **Upstream copyright and license:** [LICENCE](LICENCE), MIT. The six Python modules in `upstream/humanize` are copied verbatim; `_version.py` is a generated metadata stub because the original uses Hatch VCS for versioning.
- **Dependencies:** Python standard library only, no model API, no PyPI install.

The report gives the reproduction `precisedelta(32399, minimum_unit="minutes", format="%0.0f")`, expected **"9 hours"**, previously observed **"8 hours and 60 minutes"**. Another commenter observed `precisedelta(91500, minimum_unit="hours", format="%0.0f")` producing **"1 day and 1 hours"**.

Run with `python -m benchmarks.bugs.humanize_30.reproduce`; the subprocess imports the pinned, copied package and prints the observed results. `tests/test_humanize_30.py` verifies the *buggy baseline*, so a passing test here means that a defect was reproduced, **not repaired**.

This is a real third-party bug report with a reproduction, but not independent of model training; the historical issue and fix are public. The original upstream fix code was not used to design this baseline.

## Local candidate repair

```bash
python -m benchmarks.bugs.humanize_30.reproduce --candidate
```

The repair is stored as a small, anchored [patch](patch.py). It creates a temporary copy of the pinned upstream package, rounds whole minutes/hours **before** decomposition, and runs the original caller-visible API. The pristine baseline remains unchanged. See [experiment 009](../../../experiments/009-historical-humanize-repair.md). Only the scope of the historical report is claimed, not a general replacement for the upstream maintainer's fix.

Another independent human submitted a [related singular-minute report (#20)](https://github.com/python-humanize/humanize/issues/20): `precisedelta(3633, minimum_unit="minutes", format="%0.0f")` produced `1 hour and 1 minutes` instead of `1 hour and 1 minute`. The previously committed candidate is re-tested against this case *without being modified*. See [experiment 010](../../../experiments/010-related-humanize-report.md). These are related symptoms, not independent underlying defects.

## Offline source integrity check

`python -m unittest tests.test_humanize_source_integrity -v` compares the
Git blob hashes of all six copied Python modules against the **upstream**
`src/humanize/` blobs at the pinned commit above. It separately checks the
generated `_version.py` stub and the verbatim upstream MIT `LICENCE`.
The check is included in the normal CI unit-test discovery. It fails if
the pinned commit identifier, copied source, stub, or license changes
without revisiting the provenance assertions.

This is a **partial source snapshot** (no locale catalogs, type marker or
packaging files), not the full upstream repository. SHA-1 is used solely
to reproduce Git object identifiers, not as a security signature.
