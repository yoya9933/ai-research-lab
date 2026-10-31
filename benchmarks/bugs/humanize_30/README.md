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
