# Experiment protocol

## Question

Can a chat-based model improve defect repair through explicit hypotheses, deterministic tests and preserved feedback, without using model APIs?

## Method

1. Select a bug from `lab.buggy` with known cases. Don't read `lab.solutions` until the attempt is complete.
2. Record the attempt date, code commit, exact prompt, hypothesis, patch, test command, test output, and whether any answer-key information was exposed.
3. Run the evaluator on trusted candidate code. A case passes only when the result exactly equals the expected value; exceptions count as failures. The local toy evaluator takes a deep copy of the **full case suite** before invoking candidate functions, so a candidate's side effect on a shared external expected-value object cannot rewrite the oracle for the current grade. It also snapshots **each returned value immediately**, so later calls that reuse and mutate the same result object cannot retroactively rewrite previously recorded observations. It cannot prevent a trusted module from mutating the caller's global objects or sandbox that module; use a fresh process for independent runs.
4. Report passed cases / total cases. Keep failed attempts and note threats to validity.
5. Re-run all tests after changes and review the diff in a pull request.

## Limitations

The 10 tasks are small and hand-authored, not representative of real software engineering. The answer key exists in this repository, so blinding relies on process discipline and cannot be enforced. Tests may miss bugs. The grader imports candidate modules and must not execute untrusted code. ChatGPT internal token budgets cannot be controlled or retrieved. Claims about model improvement require independent repeated attempts and separate held-out tasks.

## Deterministic property validation

In addition to example cases, tests can check program properties with bounded, reproducible inputs. Use a mathematically or specification-defined oracle rather than copying the repaired implementation as the expected result. Record the input domain, count, and whether the repair author also authored the properties. Never describe hundreds of test inputs as hundreds of independent AI trials.

## External-source exercise intake

The `benchmarks/exercism` source corpus is MIT-licensed and pinned to a Git SHA. Preserve upstream tests and copyright, and store candidate implementations separately. Comparing the original stubs and candidate shows completion on *public upstream tests*, not genuine real-world bug repair or a blinded ability measurement. Real-world issue reproduction remains an open research goal.

The offline [Exercism source-integrity check](../tests/test_exercism_source_integrity.py)
verifies both the expected upstream **Git blob bytes** and the **exact
inventory** of Python files across the two starter and two test-fixture
trees. An unlisted extra `.py` (including a nested helper) is not
silently accepted as part of the frozen external suite. Mutable
candidate implementations remain separate and are not included in this
external-source allowlist.

The Exercism runner supports sequential grading within one trusted Python
process. It temporarily removes potentially cached candidate/test imports,
then restores the prior `sys.path` and module entries after each track,
including on failures. This includes nested candidate/test Python packages
(`pkg/__init__.py` and `pkg/mod.py`), not just top-level modules:
each track's package and its submodules are removed/restored from
`sys.modules` to prevent the next named candidate from receiving
another track's cached results. It is **not** a security sandbox;
modules imported through other global names can still have side effects.

Skipped, expected-failure and unexpected-success unittest outcomes are **not
valid scored observations** in this external benchmark. The runner refuses
the entire score with a clear `RuntimeError` if any such test is present,
rather than silently misrepresenting a skipped test as an ordinary failed
exercise. Existing pinned upstream suites contain no such annotations.
This fails closed on unsupported test semantics; it does not certify
unseen assertions or prevent contamination.

A third-party test **import or syntax error** is not a valid failed
candidate test: unittest can create a synthetic `_FailedTest` whose count
accidentally matches the expected real-test count. The loader checks its
native `TestLoader.errors` and **rejects the whole evaluation before
executing a partial test suite**, preserving the discovery traceback.
This guards test infrastructure errors, not model correctness.

Unittest suite-level fixture exceptions such as `setUpClass`,
`tearDownClass` and `tearDownModule` are also **unscored**. They may
occur without a corresponding `startTest` while the ordinary test count
still matches the expected number. The runner now rejects these
results with their original traceback instead of attaching the error
to the last scored case. Ordinary errors raised *inside* a named test
or an `addSubTest` callback still count as failed candidate
observations. The runner records subtest error IDs directly from
the stdlib callback; it does not infer them from traceback formatting.

Unittest's native `load_tests` hook can also return **two instances of
the same test identifier**, so `testsRun` can match the expected count
without identifying the intended distinct cases. The runner now rejects
missing or duplicated test IDs. This prevents duplicate-case inflation
of the external score; it does not prove that a unique test ID corresponds
to an independent defect or a hidden test. A test that called
`startTest` but never reported success, failure or error (its actual
status remains `incomplete`) is also rejected as **unscored**, rather
than assigned a legitimate failed-candidate result.

The unittest runner records a **single parent test** even if the parent
executes multiple `self.subTest()` contexts. Failed subtests are now
attached to that parent's error text (including every failing context),
and errors are distinguished from assertion failures; successful subtests
do not add extra scored cases. Do not count individual subtests as
independent defect reports or AI repair attempts.

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
fixed/regressed cases. Beyond the JSON-canonical ID, it compares nested
input arguments and expected answers with `same_value` to reject
numeric-key versus string-key Python mappings that JSON would otherwise
coerce into identical case IDs. With `python -m lab.report BEFORE AFTER --output
results/comparison.json`, it also emits a **case-level change audit** with
both observed values/errors for every fix and regression, plus
`changed_failures` for inputs that **still fail both versions** but
produce a different wrong value/exception. Such unresolved changes are
not counted as fixes or pass-to-fail regressions and are not omitted
from the saved evidence. `outcome_counts` separately accounts for every
case as passed, wrong output without error, or any reported error
(including assertion failures and serialization diagnostics). The three
categories sum to each report's total. They describe test outcomes,
**not independent repair attempts**, and are not suitable for confidence
intervals from the existing correlated cases. The `by_task` breakdown
groups the same exact cases by existing task label and reconciles each
task's baseline/candidate passes, fixes, regressions and unresolved changes.
These groups expose concentration of repairs; **task labels are not
evidence of statistical independence or separate real-world root causes**. Output is written
only after the existing same-suite validation succeeds. When saved,
the comparison JSON includes SHA-256 hashes of the exact baseline and
candidate input *file bytes*, read once for scoring and hashing. These
bind a report to input artifacts but are neither signed provenance nor
proof that the upstream source or scorer was independently controlled.

The CI workflow additionally archives the **three exact-suite comparison
JSON files and their six original input reports** as one GitHub Actions
`scored-comparisons` artifact. It uses a SHA-pinned official
`actions/upload-artifact` action, preserves evidence even when the
regression gate exits nonzero (`if: always()`), limits retention to
seven days, and lists only these nine known public-test JSON paths.
Reproducing historical comparisons after artifact expiration requires
rerunning the same pinned commit and its public tests. This retention
is a convenience, **not** long-term storage or a guarantee of blind
grading. It cannot overwrite
either original input report, even via a filesystem link: both original JSON
inputs remain available for independent comparison and later audit. When
`--fail-on-regression` is also given, **any** regressed case makes
the CLI exit with status 1 **after** it has written valid audit evidence.
Without that flag the command remains informational. The built-in
CI comparisons use this optional gate on all three known no-regression
lab/Exercism comparisons. This supports
reports in the lab/Exercism schema, **not** the heterogeneous third-party
source-replay JSON dictionaries. This catches
internally inconsistent JSON records, **not** falsified matching values,
unauthenticated reports, contamination, or a misleading test oracle.
It also rejects Python's nonstandard JSON `NaN`, `Infinity` and
`-Infinity` constants before scoring or writing evidence, even though
Python's default `json.loads` silently accepts them. The CLI also
rejects repeated JSON object keys at any depth, avoiding ambiguous
first-value/last-value interpretations. These checks do not authenticate
source authorship or replace a full JSON schema validator.

The evaluator records non-JSON-stable return values (for example a tuple
instead of a required list) as failed outcomes with a type diagnostic and
printable representation, rather than allowing JSON coercion to turn a failure
into a superficially equal result during report comparison. The current suite's
expected values are JSON-stable; this does not make arbitrary Python objects
safe to serialize or authenticate JSON reports.

## Frozen candidate source integrity

`tests/test_frozen_candidate_sources.py` checks Git blob hashes of all
three frozen Exercism trial-002 candidate source files **and every present
`benchmarks/bugs/*/patch*.py` candidate wrapper**, rejecting newly added
patch files that lack a declared pin. The hashes verify the checked-out
**current wrapper bytes**; historical candidate-commit SHAs establish
earlier freeze points.

Four older candidate wrappers (humanize #30, #333, #486 and boltons #480)
were legitimately edited in [PR #25](https://github.com/yoya9933/ai-research-lab/pull/25)
*after* their original repair PRs, solely to exclude inherited Python
bytecode caches when copying pinned source trees. The actual replacement
code, expected outputs, and source snapshots were not changed by that PR.
The [source-integrity audit](../experiments/026-candidate-source-integrity.md)
records **both initial and current** blob identities and review provenance
rather than falsely claiming those four wrappers remained byte-identical
since first submission.

These tests detect later byte changes and missing pin registration,
but not malicious simultaneous edits to code and pins, pretraining
contamination, grading-oracle problems, or untrusted-code execution.

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

## GitHub Actions event coverage

The same standard-library regression suite runs on **pull requests targeting
`main`** and on **pushes to `main` after merge**. Arbitrary branch
pushes without an open PR are **not** evidence of a passing check.
This avoids running the full CI matrix twice for every pushed PR commit,
while preserving the pre-merge PR check and independent post-merge
confirmation. Always verify the actual PR **head SHA** and successful
GitHub Actions conclusion before merging; do not infer success from
a different branch's earlier run.

The single job has a **10-minute wall-clock timeout**. Ordinary verified
full runs complete far below that limit (e.g.
[main CI #41292853363](https://github.com/yoya9933/ai-research-lab/actions/runs/41292853363)
passed), but a future infinite loop in trusted candidate/tests should not
consume GitHub-hosted runner resources until the platform's much longer
default limit. The timeout is a GitHub Actions native safeguard, **not** a
Python sandbox, protection against malicious files, or a guarantee that
every supported machine will finish within 10 minutes.
