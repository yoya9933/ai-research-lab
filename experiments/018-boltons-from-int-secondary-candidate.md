# Experiment 018: secondary, explicitly nonblind FilePerms.from_int candidate

Date: 2026-11-01.

- Pre-existing report [boltons #480](https://github.com/mahmoud/boltons/issues/480) concerns a **different** permission-revocation defect. Upstream BSD-licensed code is pinned at `967864f89791509f9eb36b22b4579d36b72a6df2` and never edited in place.
- [Experiment 017](017-boltons-from-int-postfreeze.md) was written *after* the earlier candidate had been frozen. It tests every 9-bit POSIX numeric mode, and CI verified the earlier candidate retained **63 wrong roundtrips** and **449 unchanged correct modes** on these 512 inputs.
- **Hypothesis:** `from_int` strips leading empty permission groups before positional construction. Appending empty slots *before reversing* the parts restores their user/group/other positions.
- **Method:** `patch_roundtrip.py` builds a temporary copy of the existing isolated candidate and applies one additional exact-anchor change. The earlier candidate and original vendor remain byte-identical.
- **Verification command:** `python -m unittest tests.test_boltons_480_roundtrip_candidate -v`. Compare the same 512 inputs before/after, requiring exactly 63 corrections, 449 unchanged controls, and identical outputs on the first candidate's nine permission-revocation observations.
- **Interpretation:** This investigator read the source and authored the deterministic roundtrip oracle *before* producing this secondary candidate. It is **not blind**, not independent external defect discovery, and not evidence of improved AI repair capability. 512 inputs are not 512 independent trials. Record CI evidence after completion.
