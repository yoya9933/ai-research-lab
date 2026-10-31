# External boltons FilePerms bug — historical baseline (#480)

- **Independent source:** [mahmoud/boltons issue #480](https://github.com/mahmoud/boltons/issues/480), filed 2026-09-07 by an external reporter and closed 2026-10-25.
- **Reporter-tested pre-fix commit:** [`967864f89791509f9eb36b22b4579d36b72a6df2`](https://github.com/mahmoud/boltons/commit/967864f89791509f9eb36b22b4579d36b72a6df2) (2026-08-19).
- **Provenance:** Unmodified `boltons/__init__.py` and `boltons/fileutils.py` from that commit; copied upstream BSD-3-Clause-style [LICENSE](LICENSE). Git blob SHA-1s are asserted offline in `tests/test_boltons_480.py`. This is a **partial vendored subset**, not a full repository snapshot.
- **Public defect:** `FilePerms.from_path` reads mode `0o644`; setting `other = ""` and `group = ""` changes the displayed object but leaves `int(permissions)` at `0o644`. A following `os.chmod` therefore does not revoke read permission.
- **Hypothesis:** Descriptor updates only OR new permission bits, never clearing previously assigned bits. This explanation and the proposed fix were already publicly visible; **not blind**.
- **Run:** `python -m benchmarks.bugs.boltons_480.reproduce` or `python -m unittest tests.test_boltons_480 -v`. The full CI discovery also runs the tests without external packages, paid model APIs or network access.

The nine recorded observations include three buggy revocation outcomes (`after_revoke_other`, `after_revoke_group`, `chmod_mode`) and six controls (initial mode, representation, construction, widening, empty permissions, invalid input). All writes and chmod operations are restricted to a temporary directory; GitHub CI executes on Ubuntu. A successful **baseline** asserts historical wrong behavior, not a repaired candidate.

**Limitations:** Reporter assertions plus investigator-written controls were read before writing these tests; this is neither an independent held-out score nor evidence of AI improvement. The external issue already discloses its diagnosis and proposed solution. No upstream changes or independent security audit are claimed. This reproduces a permission-state discrepancy on a pinned Python implementation, not every platform or permission feature.
