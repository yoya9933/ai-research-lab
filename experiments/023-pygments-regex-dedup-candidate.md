# Experiment 023: isolated Pygments regex deduplication candidate

Date: 2026-11-01.

## Provenance and chronology

- The original upstream merged [Pygments PR #3190](https://github.com/pygments/pygments/pull/3190)
  and its suggested `sorted(set(strings))` fix were already public
  **before** this local reconstruction. This is **not blind**.
- Historical baseline was pinned in [PR #49](https://github.com/yoya9933/ai-research-lab/pull/49)
  and merged into main at `c5f9ba2362deaa19251540003fcf80714486e34d`
  before the current patch was authored. Exact pristine source Git blob
  `9010eb3fb517ff4134b4f52581179fa80b0f7540`, BSD LICENSE
  `446a1a805c8a949579fb8a9799f2bec7777349dc`.
- The separate `patch.py` builds a temporary copy, strips inherited
  Python bytecode, and changes exactly one checked sorting line; the pinned
  upstream module and license remain byte-identical.
- **Original upstream test code for this PR has not been fetched in this
  conversation before this candidate commit.** The public fix was already
  seen; any later test replay controls current conversation exposure only.

## Testable prediction

For the **same seven** already exposed baseline observations:
three duplicates should become identical to their distinct-input regexes,
while all **four controls** remain byte-for-byte unchanged. The returned
regex strings should continue matching the original input words.

Run `python -m unittest tests.test_pygments_3190_candidate -v`
and `python -m unittest discover -s tests -v`.
[PR #50 CI](https://github.com/yoya9933/ai-research-lab/actions/runs/41286237343)
and [merged main CI](https://github.com/yoya9933/ai-research-lab/actions/runs/41286264647)
both completed **success**: three duplicate-pattern records changed and four
controls did not. No performance speedup, W117 linter pass, upstream
package-wide correctness, or AI-repair ability improvement is claimed.
