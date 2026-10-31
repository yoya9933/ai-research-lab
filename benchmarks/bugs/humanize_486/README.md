# Historical third-party negative-ordinal report (humanize PR #486)

- **External source and author report:** [python-humanize/humanize PR #486](https://github.com/python-humanize/humanize/pull/486), submitted 2026-10-25.
- **Reported behavior:** `ordinal(-1)` yields `-1th`, but `-1st` is expected; similarly -2 and -21. The public report includes a diagnosis and proposed fix.
- **Important upstream status:** This is a **closed, unmerged pull request**, not an accepted upstream change or an independently adjudicated test verdict. We test the reported input-output contract on our own pinned copy.
- **Frozen upstream snapshot:** `9528daf55fd7178c025f7294b8e349f8b3524175` (2025-03-16), already kept unchanged in [humanize_30/upstream/humanize](../humanize_30/upstream/humanize); reused under [MIT license](../humanize_30/LICENCE), without a second vendor copy.
- **Hypothesis:** Signed modulo selects a non-semantic last digit of negative input, giving the default `th` suffix even outside 11–13. Positive ordinals, the teen exception, an invalid input and zero provide controls.
- **Reproduce:** `python -m benchmarks.bugs.humanize_486.reproduce` and `python -m unittest tests.test_humanize_486 -v`.
- **Expected baseline:** Six negative last-digit examples give erroneous `th`, while nine controls remain unchanged. The 15 observations include the public -1/-2/-21 examples, additional investigator-written boundaries and a gender variant.
- **Limitations:** All assertions are public or investigator-written and were visible before the candidate is authored, so this is **not blind**. Potential model pretraining exposure cannot be ruled out. This is a separate arithmetic root cause from issue #30`s rounding and #333`s overflow, but all three reports concern the *same upstream project*, reducing external diversity. Source code executes in a subprocess; this is not an isolation sandbox for untrusted code.

A passing baseline test demonstrates **reproduction** on the historical source, not a fix or general AI improvement.
