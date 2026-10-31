# Experiment 012: failed rotation candidate and bytecode-cache hypothesis

- **Date:** 2026-11-01 (Taiwan).
- **Public source:** [boltons issue #479](https://github.com/mahmoud/boltons/issues/479), pinned to reporter-tested commit `967864f89791509f9eb36b22b4579d36b72a6df2` (BSD-licensed, unchanged).
- **Initial candidate commit:** [`c761764`](https://github.com/yoya9933/ai-research-lab/commit/c761764ad6f82eeb2886c34fea6d5638c7184b14); copied source and moved the oldest-generation deletion before the rename loop.
- **Failed run:** [GitHub Actions 41252531363](https://github.com/yoya9933/ai-research-lab/actions/runs/41252531363). `python -m unittest discover -s tests -v` ran **75 tests with 5 failures**: all four expected changed outcomes were still identical to baseline, and the change-set assertion failed. The six previously merged source cases were not reclassified as successes.
- **Hypothesis after observing failure:** The unchanged source had been imported in earlier subprocesses, producing `__pycache__`. `shutil.copytree` copied its compiled bytecode into the candidate. Moving the rotation block without adding/removing bytes preserves source length; timestamp-based Python .pyc validation can then reuse stale bytecode if the patch is written within the same timestamp granularity. This is a proposed explanation for the unchanged outputs, not a separately proven causal measurement.
- **Correction for retest:** Ignore `__pycache__` and `*.pyc` when creating the candidate, assert no caches were copied before import, and assert the new source order. Then rerun the **same nine observations** and full CI. If the test still fails, retain this log and investigate further.

**Exposure:** The issue and suggested fix are public, so no blind repair claim. This entry records an unsuccessful intermediate attempt rather than erasing it. GitHub CI is the only execution evidence; no model APIs, other agent or paid inference was used.
