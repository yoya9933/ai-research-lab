# AI Research Lab

A **chat-first, API-free** experiment for AI-assisted debugging.

ChatGPT works on one bug at a time, GitHub records each hypothesis and patch, and Python's standard library grades reproducible cases. **No model API key, paid model calls, or autonomous agent is required.**

## Quick start

Requires Python 3.10+:

```bash
python -m unittest discover -s tests -v
python -m lab evaluate --module lab.buggy --output results/baseline.json
python -m lab evaluate --module lab.solutions --output results/reference.json --require-all-pass
python -m lab evaluate --module lab.attempt_001 --output results/attempt_001.json
```

The intentionally defective baseline is expected to fail some cases. `--require-all-pass` returns exit status 1 if any case fails, so CI can enforce successful repairs. `lab.solutions` is the reference answer key, **not** an AI-generated result. Generated results are excluded from Git by default.

## Chat-first research workflow

1. Choose one function from `lab/buggy.py`; read its cases in `lab/cases.py`. **Do not read `lab/solutions.py` until after your attempt.**
2. Write a prediction, root-cause hypothesis, and intended fix in a new experiment Markdown file.
3. Create a candidate module with the same function names and evaluate it:
   ```bash
   python -m lab evaluate --module lab.candidate --output results/attempt.json
   ```
4. Compare outcomes and retain both successes and failures in the research log.
5. Open a GitHub PR with code changes, tests and evidence.

The [first recorded repair](experiments/001-debugging.md) is explicitly **unblinded** because the assistant had already inspected the reference answer key. It demonstrates the workflow, not independent model ability.

**Security:** `--module` imports and executes Python code in the current process. Only evaluate trusted local modules. This is **not a sandbox**.

## What this project can and cannot measure

This lab can measure correctness on a fixed test suite and record reproducible repair attempts. It **cannot control or measure ChatGPT's internal reasoning tokens**, automatically invoke a chat model from GitHub Actions, or operate unattended. No accuracy claims should be made from the included reference code alone.

Read the [experiment protocol](docs/PROTOCOL.md), [roadmap](docs/ROADMAP.md), and [contributor rules](AGENTS.md).

For third-party defects, see the [real-world evidence ledger](docs/REAL_WORLD_CASES.md)
for pinned sources, upstream acceptance status, exact local test evidence,
preserved failures and limits on blind or general AI-performance claims.

## Post-commit follow-up

Use `--suite followup` to grade 20 additional cases introduced after the first candidate was committed. Read [experiment 002](experiments/002-followup.md) for precise provenance and why the results are **not** independently blinded.

## Compare attempts without hiding regressions

```bash
python -m lab evaluate --module lab.buggy --output results/baseline.json
python -m lab evaluate --module lab.attempt_001 --output results/attempt.json
python -m lab.report results/baseline.json results/attempt.json --output results/comparison.json --fail-on-regression
```

The comparison displays score changes, cases fixed and cases regressed.
The optional JSON summary preserves each fixed/regressed case's task,
input, expected output and both actual/error outcomes. It separately
lists `changed_failures`: cases that **still fail on both versions**
but now return a different wrong value or error. Such cases do **not**
count as repairs or pass-to-fail regressions; recording them preserves
unsuccessful debugging evidence.
It rejects different suites, altered inputs/expected values, and
inconsistent reported totals; invalid comparisons never write the
requested output. The CLI also refuses an `--output` path that would
overwrite either input report (including symlink or hard-link aliases). Use `--fail-on-regression` when a downstream CI job must reject a
candidate that breaks any previously passing case; it exits with status
1 **after** printing counts and writing any requested JSON evidence.
Without the flag, the comparison remains informational. Every
saved comparison includes SHA-256 digests of **both exact original input
files** (`input_sha256`), including when a regression gate exits nonzero;
this allows the inputs used for an audit to be matched byte-for-byte.
These hashes alone do not authenticate who authored the inputs. The tool
supports the existing lab/Exercism evaluator report format; third-party
bug reproducers do not automatically emit that schema. Scores still
reflect **only** the compared cases.

## Deterministic property tests

Run `python -m unittest discover -s tests -v` to check 411 additional input combinations for the three fixed functions using math or specification-based oracles. See [experiment 003](experiments/003-properties.md). These are bounded tests, **not** proof of general correctness or independent model improvement.

## Externally authored exercise benchmark (v0.2 groundwork)

The [pinned Exercism Python corpus](benchmarks/exercism/README.md) includes three MIT-licensed practice exercises and **29 original upstream tests**. It runs fully offline using `unittest` and can use the existing `lab.report` comparator. It is **not a set of real-world bug reports** and the model has already seen the public test assertions; see [provenance notes](experiments/004-external-intake.md).

### Chat-authored external attempt

The first external exercise completion is in `benchmarks/exercism/attempt_001/`. Reproduce 29 pinned, public upstream tests and compare to the incomplete upstream starter:

```bash
python -m benchmarks.exercism.runner starter --output results/exercism-starter.json
python -m benchmarks.exercism.runner attempt_001 --output results/exercism-attempt.json --require-all-pass
python -m lab.report results/exercism-starter.json results/exercism-attempt.json
```

See [experiment 005](experiments/005-external-chat-attempt.md). This is explicitly **unblinded** educational exercise completion, not independent evidence of AI capability growth.

## Pre-registered second trial

The [second exercise trial](benchmarks/exercism/trial_002/README.md) contains three candidates committed **before** the external upstream test files are fetched. The chronology and limitations are recorded in [experiment 006](experiments/006-pretest-candidate.md). This is a stronger exposure-control method, not proof that pretrained model knowledge is absent.

The second trial's [original 44 upstream tests](experiments/007-postfreeze-upstream-tests.md) were imported *after* candidate commit `f714ff6`. Run the `starter_002` and `attempt_002` tracks to compare results without altering the frozen candidate. This controls **current-conversation test exposure only**, not pretrained knowledge.

## Real-world bug reproduction

A [historical, independently reported humanize bug](benchmarks/bugs/humanize_30/README.md) is pinned to its **pre-fix upstream commit**. The code is vendored under MIT terms so CI can reproduce the reporter's output with no package download or model API:

```bash
python -m benchmarks.bugs.humanize_30.reproduce
```

This is a true third-party bug *report*; a replay is not evidence of independent model performance.

To try the [minimal candidate repair](experiments/009-historical-humanize-repair.md) without touching the original snapshot:

```bash
python -m benchmarks.bugs.humanize_30.reproduce --candidate
```
