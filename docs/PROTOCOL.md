# Experiment protocol

## Question

Can a chat-based model improve defect repair through explicit hypotheses, deterministic tests and preserved feedback, without using model APIs?

## Method

1. Select a bug from `lab.buggy` with known cases. Don't read `lab.solutions` until the attempt is complete.
2. Record the attempt date, code commit, exact prompt, hypothesis, patch, test command, test output, and whether any answer-key information was exposed.
3. Run the evaluator on trusted candidate code. A case passes only when the result exactly equals the expected value; exceptions count as failures.
4. Report passed cases / total cases. Keep failed attempts and note threats to validity.
5. Re-run all tests after changes and review the diff in a pull request.

## Limitations

The 10 tasks are small and hand-authored, not representative of real software engineering. The answer key exists in this repository, so blinding relies on process discipline and cannot be enforced. Tests may miss bugs. The grader imports candidate modules and must not execute untrusted code. ChatGPT internal token budgets cannot be controlled or retrieved. Claims about model improvement require independent repeated attempts and separate held-out tasks.

## Deterministic property validation

In addition to example cases, tests can check program properties with bounded, reproducible inputs. Use a mathematically or specification-defined oracle rather than copying the repaired implementation as the expected result. Record the input domain, count, and whether the repair author also authored the properties. Never describe hundreds of test inputs as hundreds of independent AI trials.

## External-source exercise intake

The `benchmarks/exercism` source corpus is MIT-licensed and pinned to a Git SHA. Preserve upstream tests and copyright, and store candidate implementations separately. Comparing the original stubs and candidate shows completion on *public upstream tests*, not genuine real-world bug repair or a blinded ability measurement. Real-world issue reproduction remains an open research goal.

The Exercism runner supports sequential grading within one trusted Python
process. It temporarily removes potentially cached candidate/test imports,
then restores the prior `sys.path` and module entries after each track,
including on failures. This prevents a later named candidate from receiving
results from an earlier track's cached modules; it is **not** a security sandbox.

## Temporary candidate source and Python bytecode

Source-attributed bug replays copy a pinned upstream **source** subset into
a disposable candidate directory. Exclude `__pycache__` directories and
`*.pyc` files when copying. Python can consider timestamp-based bytecode
valid if a patch preserves source length and falls within the timestamp
granularity, causing an apparent candidate to execute old behavior. Use
standard-library `shutil.ignore_patterns` and assert the temporary copy
contains no inherited caches **before** import. See
[experiment 012](../experiments/012-boltons-rotation-cache-failure.md) for
the observed CI failure; hash-verified upstream files remain unchanged.

## Report integrity

The evaluator and report comparator check actual versus expected recursively,
including nested lists and dictionaries. A boolean is not interchangeable with
an integer inside a list (e.g. `[False]` is not `[0]`) or as a mapping
key (e.g. `{False: "x"}` is not `{0: "x"}`).
The report comparator checks that each recorded pass/fail flag agrees with
its reported actual value, expected value, and error status, in addition to
matching case identities, rejecting duplicate observations, and tallying
fixed/regressed cases. This catches
internally inconsistent JSON records, **not** falsified matching values,
unauthenticated reports, contamination, or a misleading test oracle.

## Frozen candidate source integrity

`tests/test_frozen_candidate_sources.py` checks Git blob hashes of the
three Exercism trial-002 candidate files at their pre-test commit, the
first `tokenize-rt` patch at its pre-follow-up commit, and the distinct
later roundtrip patch. These offline checks catch accidental changes to
candidate source bytes after their recorded freeze points. The historical
Git commits establish chronology; hashing alone does **not** prove the
model had no prior exposure, authenticate the oracle, or prevent a reviewer
from intentionally changing both code and checksum in a future PR.
