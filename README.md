# AI Research Lab

A **chat-first, API-free** experiment for AI-assisted debugging.

ChatGPT works on one bug at a time, GitHub records each hypothesis and patch, and Python's standard library grades reproducible cases. **No model API key, paid model calls, or autonomous agent is required.**

## Quick start

Requires Python 3.10+:

```bash
python -m unittest discover -s tests -v
python -m lab evaluate --module lab.buggy --output results/baseline.json
python -m lab evaluate --module lab.solutions --output results/reference.json
```

`lab.buggy` contains 10 deliberate defects. `lab.solutions` is a reference answer key, **not** an AI-generated result. Generated results are excluded from Git by default.

## Chat-first research workflow

1. Choose one function from `lab/buggy.py`; read its cases in `lab/cases.py`. **Do not read `lab/solutions.py` until after your attempt.**
2. Write a prediction, root-cause hypothesis, and intended fix in a new experiment Markdown file.
3. Make a candidate module with the same function names and evaluate it:
   ```bash
   python -m lab evaluate --module lab.candidate --output results/attempt.json
   ```
4. Compare outcomes and retain both successes and failures in the research log.
5. Open a GitHub PR with code changes, tests and evidence.

**Security:** `--module` imports and executes Python code in the current process. Only evaluate trusted local modules. This is **not a sandbox**.

## What this project can and cannot measure

This lab can measure correctness on a fixed test suite and record reproducible repair attempts. It **cannot control or measure ChatGPT's internal reasoning tokens**, automatically invoke a chat model from GitHub Actions, or operate unattended. No accuracy claims should be made from the included reference code alone.

Read the [experiment protocol](docs/PROTOCOL.md), [roadmap](docs/ROADMAP.md), and [contributor rules](AGENTS.md).