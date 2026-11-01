# Experiment 017: FilePerms.from_int post-freeze roundtrip audit

Date: 2026-11-01. **Investigator-authored follow-up, not an external bug report.**

- Historical third-party source: [boltons #480](https://github.com/mahmoud/boltons/issues/480) and BSD-licensed pinned source at `967864f89791509f9eb36b22b4579d36b72a6df2`.
- Previously frozen *different-root-cause* permission-mutation candidate: [PR #22](https://github.com/yoya9933/ai-research-lab/pull/22).
- New question: for every 9-bit mode `m` in `0..511`, does `int(FilePerms.from_int(m)) == m`? The oracle is the documented numerical roundtrip, not an upstream answer key.
- Pre-test hypothesis from reading pinned implementation: `from_int` drops the missing leading permission fields, causing nonzero modes below `0o100` to be assigned to the wrong classes. Expect **63 mismatches**, with the 449 remaining modes roundtripping. The earlier descriptor-update patch targets a different function, so it should leave all 512 observations unchanged.
- Reproduce offline: `python -m unittest tests.test_boltons_480_roundtrip -v`. The test compares both the pristine source and a temporary copy of the *original* frozen candidate; no patch is made in this baseline study.
- Scope: 512 deterministic input modes are **not 512 independent experiments**. This test was authored after seeing the relevant code and does not establish independent external discovery or model blinding. No change to external source, no API, no package downloads. Test outcomes must be verified in CI before being described as measured results.
