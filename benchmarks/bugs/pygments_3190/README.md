# Pygments PR #3190: duplicate input yields redundant regex classes

- **Independent upstream source:** [Pygments PR #3190](https://github.com/pygments/pygments/pull/3190), filed and merged 2026-07-07.
- **Pre-fix upstream commit:** [`c97c0b54f58d496e34f4b37eb9d0c482e79e21b3`](https://github.com/pygments/pygments/commit/c97c0b54f58d496e34f4b37eb9d0c482e79e21b3).
- **Provenance:** `upstream/regexopt.py` is the entire unmodified upstream single module, original Git blob `9010eb3fb517ff4134b4f52581179fa80b0f7540`. [Original BSD LICENSE](LICENSE) also copied unchanged (blob `446a1a805c8a949579fb8a9799f2bec7777349dc`). Source and license hashes are checked by a standard-library test.
- **Original external behavior:** Repeated input words produce regex classes with repeated letters such as `[aab]`, violating input-set idempotence and creating redundant regex syntax despite equivalent matches. The public report mentions a W117 overlap warning; this subset tests only pattern generation, not the upstream linter.
- **Method:** `python -m benchmarks.bugs.pygments_3190.reproduce` and `python -m unittest tests.test_pygments_3190 -v`. Three duplicate-word cases reproduce the historical anomaly and four controls check unique input, empty input, and escaping. Literal word matching is checked independently. No packages downloaded; the existing subprocess runner imports only the pinned local module.
- **Interpretation and limits:** This is a **fifth** external codebase, but these seven inputs are investigator-written after the upstream PR's public diagnosis and its suggested `sorted(set(strings))` correction were already seen. **Not blind**, not a measured AI improvement, and not full upstream CI or a regex-linter run. An accepted upstream PR supports the report's provenance; this file is merely an immutable *pre-fix* reproduction. Python GitHub Actions results must be checked before claiming measured success.

A green baseline test here confirms the **wrong original output**, not a local repair.

## Separate candidate (unblinded)

`patch.py` copies the exact pre-fix module into a disposable directory
without inherited bytecode and replaces `sorted(strings)` with
`sorted(set(strings))` only if the pinned source anchor occurs once.
`tests/test_pygments_3190_candidate.py` runs **the same seven inputs**
as the frozen baseline: three duplicate-generated patterns should become
identical to their deduplicated counterparts while **four controls**
remain unchanged, with literal-word matching preserved.

Run `python -m unittest tests.test_pygments_3190_candidate -v`.
The public upstream fix was already known before writing this patch,
so these observations are **not blind**; they check a narrow,
single-module property and do not establish a performance improvement.

## Post-freeze original upstream regression cases

Only **after** the candidate commit
`94a4c403456de093d3350d1d65fb8939f1873849`, two
original Pygments PR #3190 test function bodies were read from
[upstream tests/test_regexopt.py](https://github.com/pygments/pygments/blob/64226095eb736dbf23e16786f04c82f3a3a86b92/tests/test_regexopt.py)
(Git blob `f2d566541c37ac8b7ab35b239bdea4aeea565b56`).
They are copied **verbatim** into `upstream_tests.py`, apart from module
imports necessary to use the pinned standalone source. The `print`
statements are retained; the stdlib test runner redirects their output
before JSON scoring.

Run `python -m unittest tests.test_pygments_3190_upstream -v`.
The two original assertions should fail on historical baseline and
pass after the frozen candidate. This tests only current-conversation
exposure chronology; the public repair was already visible and
**no blind AI ability measurement is claimed**.
