# Independent external boltons rotation report — historical baseline (#479)

- **Source:** [mahmoud/boltons issue #479](https://github.com/mahmoud/boltons/issues/479), filed 2026-09-07; public reporter reproduced data loss with `rotate_file(keep=1)` and N-1 retained generations when the rotation is full.
- **Frozen source:** Reuses the *unchanged* BSD-licensed `boltons/fileutils.py`, `__init__.py` and [LICENSE](../boltons_480/LICENSE) at upstream commit [`967864f89791509f9eb36b22b4579d36b72a6df2`](https://github.com/mahmoud/boltons/commit/967864f89791509f9eb36b22b4579d36b72a6df2), already pinned and hash-verified in [boltons_480](../boltons_480/README.md). No second copy is added.
- **Hypothesis:** The rotation loop renames the newest generation into `.keep` and then deletes `.keep`, discarding the data it just moved.
- **Reproduce:** `python -m benchmarks.bugs.boltons_479.reproduce` or `python -m unittest tests.test_boltons_479 -v`. The same trusted subprocess runner loads the pinned source offline, with all file operations inside `TemporaryDirectory`.

The baseline records nine deterministic observations: **four data-loss / retention manifestations** (`keep_one_names`, `keep_one_data`, `keep_five_names`, `keep_five_data`) and **five controls** (a nonfull two-slot rotation, its content, absent file, invalid keep, and non-file path). These are individual observations, **not nine independent AI trials**. A passing baseline confirms the wrong historical behavior, not a fix.

**Provenance/limits:** This is a new root cause separate from FilePerms #480, but the same upstream project and frozen source. The issue's diagnosis and suggested repair were already public and read before a candidate; **not blind**. Reporter inputs plus investigator-written controls are not hidden evaluation. No paid API, upstream submission, or claim of generalized model capability.
