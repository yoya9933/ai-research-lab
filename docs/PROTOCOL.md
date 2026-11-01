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

The evaluator records non-JSON-stable return values (for example a tuple
instead of a required list) as failed outcomes with a type diagnostic and
printable representation, rather than allowing JSON coercion to turn a failure
into a superficially equal result during report comparison. The current suite's
expected values are JSON-stable; this does not make arbitrary Python objects
safe to serialize or authenticate JSON reports.

## Frozen candidate source integrity

`tests/test_frozen_candidate_sources.py` checks Git blob hashes of the
three Exercism trial-002 candidate files at their pre-test commit, the
first `tokenize-rt` patch at its pre-follow-up commit, and the distinct
later roundtrip patch. These offline checks catch accidental changes to
candidate source bytes after their recorded freeze points. The historical
Git commits establish chronology; hashing alone does **not** prove the
model had no prior exposure, authenticate the oracle, or prevent a reviewer
from intentionally changing both code and checksum in a future PR.

## Manual independent-assessor protocol (not yet performed)

This is the **next experiment design**, not a report of a completed blinded
trial. It requires an external human assessor who has **not** authored the
candidate or revealed the grading assertions to the repairing conversation.
No extra agent, model API, scheduling service, or automation is needed.

1. **Pre-register and separate roles.** The assessor chooses a reproducible,
   appropriately licensed real-world defect and privately owns independent
   test cases and their expected outcomes. Record the external reporter and
   pre-fix source Git SHA, license, defect family, selection rule, number of
   planned tasks, test-generation origin, and whether the public upstream fix
   was already seen. Publish only the task specification and visible examples
   before candidate freeze. Do **not** upload a withheld answer key, private
   source, secrets or identifiable assessor information into this chat.
2. **Freeze the task and baseline first.** Pin the unmodified original
   source and original third-party license by their Git blob IDs. Reproduce
   visible examples on that source, including a few ordinary controls.
   Record any baseline setup failure; never silently replace the upstream
   snapshot or label a deliberately failing baseline a successful repair.
3. **Run one Chat-only repair attempt.** Before reading the assessor's
   hidden assertions, record the exact task prompt, visible evidence,
   hypothesis, timestamp, patch and any unsuccessful attempts. Keep changes
   in a **separate temporary candidate**, not the pinned source. Run only
   exposed tests. Commit the candidate to Git and record both the candidate
   commit SHA and the patch Git blob SHA. No model API or background agent.
4. **Release independent tests only after commit freeze.** The assessor
   records a dated release/reveal event after verifying the frozen commit
   exists and has not moved. Only then provide publishable, legally reusable
   held-out tests and expected outputs. If tests cannot be legally published,
   do not claim public reproducibility or print confidential assertions into
   public CI logs; record the visibility limitation instead.
5. **Grade without modifying the frozen candidate.** Evaluate **the same
   test names, input values and expected results** on the pinned baseline and
   frozen candidate, using trusted Python standard-library test runners.
   Record passing/total cases, *each* fixed case, *each* regression,
   exception types, full test commands, and actual GitHub Actions run IDs.
   Use `python -m lab.report baseline.json candidate.json` only when both
   results use the comparator's compatible schema and identical suite.
   Other upstream replays should use their existing isolated tests.
   Do not execute untrusted Python through the evaluator: subprocess use is
   **not** a security sandbox.
6. **Freeze scores and preserve failures.** After revealing tests, never
   revise the trial's original candidate or erase failed attempts. A revised
   patch is a **new, explicitly post-feedback** candidate/trial, not a
   retroactive improvement to the original grade. Preserve CI failures,
   bad test assumptions, skipped/unavailable assertions, and reviewer
   disagreements in an experiment log with links.
7. **Classify exposure and statistical unit.** Mark independently authored
   test bodies as withheld only if the assessor, not this repairing chat,
   controlled their pre-commit access. Public upstream patches, previously
   read tests and training-data exposure still limit any claim of
   **blinding**. Count independent defect families or pre-registered trial
   units for aggregate analyses, **not** hundreds of correlated test inputs.
   Do not infer an AI improvement rate or confidence interval from one
   candidate, one conversation, cherry-picked tasks, or a reference key.

### Per-trial evidence checklist

| Field | Required record |
| --- | --- |
| Case selection | Reporter/source URLs, license, distinct root cause, task inclusion rule |
| Freeze | Pre-fix upstream commit and original source blobs; candidate commit and patch blob |
| Exposure | Who authored the tests, what the chat saw before candidate commit, reveal timestamp |
| Execution | Trusted test command, CI run URL, Python version, input-suite identity |
| Results | Baseline and candidate case counts, individual repairs and regressions, failed cases |
| Limits | Unchecked paths, hidden-test confidentiality, model prior exposure, exclusions |

**Current status:** The [real-world case ledger](REAL_WORLD_CASES.md)
documents reproducible **non-blind** source-attributed replays. Pygments
original test bodies were revealed after its candidate freeze, but the
public solution had been seen before candidate creation. No experiment
here has yet satisfied all independent-assessor gates above; Issue #7
must remain open. This procedure alone is **not evidence of model
improvement**.
