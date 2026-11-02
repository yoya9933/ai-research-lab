# Research batch 030 — two distinct source-attributed defects

**Status: candidate frozen, post-freeze local checks pending CI. Not a blind study or independent A/B trial.**

Candidate snapshot: [4939deccc45a839e969d53a0cd33bda4f6685b10](https://github.com/yoya9933/ai-research-lab/commit/4939deccc45a839e969d53a0cd33bda4f6685b10).
The original source/license and first candidate wrappers were committed together **before** the follow-up test source in this repository.

| External report | Pre-report source commit | First-attempt repair | Observable controls |
| --- | --- | --- | --- |
| [boltons #348](https://github.com/mahmoud/boltons/issues/348) (2023-10-10), LRI/LRU linked-list and dict value mismatch | `1372434369025e6ace5ba0925b8fa88f0f55469b` (BSD, full cacheutils.py) | On replacing an existing key, update the inherited dict backing store too | getitem, eviction, capacity and two cache classes |
| [more-itertools #1214](https://github.com/more-itertools/more-itertools/issues/1214) (2026-07-16), one-element equality/hash | `07eb790b4aa1aee88d78963fc4f740b03a9fb4a1` (MIT, verbatim numeric_range class excerpt with standard-library imports) | Treat one-element sequences as equal independent of step and normalize their hash | 0-element/2-element and differing sequences |

## Method and limitations

Both publicly available reporter descriptions were read **before** coding, including the reporter's suggested direction for single-element equality and hashing. Consequently **these are not blind repair attempts**. The excerpt contains the original class body, not an entire upstream distribution. No upstream test suite has been run, no comparison to a fresh-chat control exists, and no independent assessor or secret grader participated.

The post-freeze local test was investigator-authored in this Chat; it checks the visible reproduction and ordinary controls, not an independently withheld oracle. Passing such tests establishes only bounded repair correctness. The main purpose is a single coherent two-defect batch rather than many tiny infrastructure PRs.

Run `python -m unittest tests.test_two_defect_batch tests.test_batch_source_integrity -v`.
The full repository CI also executes `python -m unittest discover -s tests -v`.

## Provenance

- boltons original `boltons/cacheutils.py` Git blob `27a19cb9e63b41663d7ad500c67a0485d55ade13`, BSD LICENSE `6a4c9d2496f53c61c99ae7c113e6ed94b15b038c`.
- more-itertools original `more_itertools/more.py` Git blob `7ce276ac417426a419e84d31fe73e4681e81f973`; extracted unmodified `numeric_range` class to standalone `numeric_range.py` with standard-library imports, MIT LICENSE `0a523bece3e50519653c4d7a38399baa487fefa1`.
- Candidate patch blobs frozen at `341df8927a7235d62acf74c8ba867870394509e0` and `3b35cafbe1c720bfde8a3a72c2ce863a1afc0702`.
- Original external issue reporters are not the authors of our local tests; avoid counting these as independent blind tasks.

**Outcome field:** fill with actual PR CI outcome and failures; do not claim success merely because a candidate commit exists.

## Post-merge PR #86 P1 provenance and eviction audit (2026-11-02)

The historical claim above about the class excerpt must **not** be read as
authentication of a complete, unmodified upstream module. At PR #86 merge,
`upstream/numeric_range.py` was already a **derived standalone replay**:
its class body was copied verbatim but imports were minimized; its local
blob hash `e207d3e6742042c39f88a617c7e665788ce255c6` pinned those
derived bytes, not the complete upstream source.

The subsequent audit vendors pristine `upstream/more_itertools/more.py`
exactly as Git blob `7ce276ac417426a419e84d31fe73e4681e81f973`
from upstream commit `07eb790b4aa1aee88d78963fc4f740b03a9fb4a1`.
The source-integrity test pins that blob **and** independently verifies
that the numeric_range class body matches the historical replay exactly.
The baseline test now compiles only the pristine class AST with its required
standard-library imports, since the complete upstream module imports
`.recipes` and is not independently importable without the full package.
This verifies a source-identical **class-level reproduction**, not full
upstream-distribution integration or upstream-suite success.

The derived replay retains its legacy path so frozen
`more_itertools_1214/patch.py` continues to read **unchanged** input.
Neither first-attempt patch wrapper was edited; the original candidate-freeze
commit, local grading chronology, and earlier limitations stand.

The cache check now captures keys **after** inserting the overflowing
`"c"` entry, and explicitly checks `"b"` was evicted, `"a"` and
`"c"` remain, and capacity is exactly two, for original and candidate
LRU/LRI. Thus a wrong linked-list eviction order fails the test rather
than passing through pre-overflow observations.

These are post-merge quality corrections to public, investigator-authored
replays. **G2 remains 0/6**: no independent assessor-held hidden scores,
blinded comparison, or new first-attempt candidates were established.
