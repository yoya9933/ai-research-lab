# Real-world issue reproduction: humanize #333

- **Independent external report:** https://github.com/python-humanize/humanize/issues/333
- **Reported:** 2026-06-28 (after this project's pinned snapshot).
- **Issue:** `naturaldelta(float("inf"))` raises `OverflowError` although its
  documented fallback returns non-convertible inputs as text.
- **Pinned source:** `9528daf55fd7178c025f7294b8e349f8b3524175`
  (2025-03-16, prior to the report and upstream correction).
- **Source and license:** Reuses the **unchanged** MIT-licensed tree under
  [../humanize_30/upstream/humanize](../humanize_30/upstream/humanize)
  and [MIT LICENCE](../humanize_30/LICENCE), without copying it a second time.
- **Dependencies:** Python standard library only; no online packages or model API.

Run `python -m benchmarks.bugs.humanize_333.reproduce` to observe both signs
of infinity, NaN, an ordinary duration, bad text and a very large **finite**
duration. `tests/test_humanize_333.py` asserts **baseline failures** exactly.
Successful baseline tests therefore mean that the bug was *reproduced*, not
that the issue was repaired. The shared subprocess runner imports only the
pinned local code.

This is another real independently filed report, with a different code path
and failure mode from rounding issue #30; it is **not blind** because the report
and its suggested fix are public. Preserve the pristine source snapshot when
testing a candidate. Do not silently turn the intentionally failing baseline
cases into expected successes.
