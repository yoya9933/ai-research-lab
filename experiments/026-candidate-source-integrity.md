# Experiment 026 — audit every local candidate wrapper source revision

Date: 2026-11-01. Engineering provenance check; **not** model repair trial.

## Discrepancy found

Comparing current candidate source Git blob IDs against their respective
**first repair PR heads** identified four changed wrappers. All changes
came from [PR #25](https://github.com/yoya9933/ai-research-lab/pull/25):
`copytree` was made to ignore inherited `__pycache__` and `*.pyc`.
The source replacement `OLD`/`NEW` logic remained unchanged. That
bytecode-isolation change was necessary to prevent stale Python compiled
files from silently executing the unpatched code. Reproducibility is
improved, but it is **not byte-for-byte identical to the original wrapper**.

| Candidate wrapper | Original candidate PR commit / original Git blob | Current checked-out Git blob |
| --- | --- | --- |
| `humanize_30/patch.py` | [#13](https://github.com/yoya9933/ai-research-lab/pull/13), `5222efbea566930e3201b49365e44d6b3da450cd` / `e9c67b1c3239c8b781a2f4d4c7b2254d4c45393c` | `d270f28f8017043b3bbf4570112038bed384f8cf` |
| `humanize_333/patch.py` | [#16](https://github.com/yoya9933/ai-research-lab/pull/16), `4fd17089be4f66554f2057607c714002bbc44f1b` / `58af8a4b8e860a7b549349634d409ea5845165e9` | `87a9737feb8a5e6d1b97b2d622f11789fcd57e94` |
| `humanize_486/patch.py` | [#18](https://github.com/yoya9933/ai-research-lab/pull/18), `eee36808316fc41e453a30ddd194024fcf869094` / `81d0bdaf8dafbf08d1c57cfe7d73ce2b0a24f149` | `e7d35226208aa3401f684ed2c1c49768356ad74d` |
| `boltons_480/patch.py` | [#22](https://github.com/yoya9933/ai-research-lab/pull/22), `9b53b5c9c13d7e3c7cdf7d67cd8a102196a895e8` / `82d8fa726e19090e82c70e0e2ed3a9e046ef9599` | `b172171c58b4245d8a0e9e2e10a4c0f41a170552` |

## Two unchanged additional first-commit wrappers

| Candidate | Original repair PR head | Git blob, still present |
| --- | --- | --- |
| `boltons_479/patch.py` | [#24](https://github.com/yoya9933/ai-research-lab/pull/24), `8871264f5ac566322d3e6e21058d08c024fc3d30` | `2026d99085619211b75366a820cf9614afed9fe5` |
| `boltons_480/patch_roundtrip.py` | [#40](https://github.com/yoya9933/ai-research-lab/pull/40), `681491f436c772be0aee2a2cf6524206472a7856` | `56c6aa5f0f3f71c4744e15150de58b9c45971908` |

The other four existing local bug-candidate pins (tokenize-rt first
and secondary, more-itertools, and Pygments) and three Exercism source
pins were already in `tests/test_frozen_candidate_sources.py` and
are unchanged in this audit. Total intended coverage after this PR:
**all 10 local `patch*.py` files and 3 pre-test Exercism files**.

## Verification

- `python -m unittest tests.test_frozen_candidate_sources -v`
- `python -m unittest discover -s tests -v`

The new discovery check explicitly fails if a future local
`benchmarks/bugs/*/patch*.py` is added without an integrity pin.
Git's SHA-1 object format is used **only** for source/provenance
comparison, not as a modern cryptographic security signature.
The recorded original commits are existing Git history, not proof of
absence of model training or publication exposure.

**Execution evidence:** CI must pass before claiming all 13 source
hashes match. A green check will show source stability in the checked-out
tree, not an independently blinded repair or 13 independent AI trials.
