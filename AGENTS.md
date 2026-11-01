# Agent instructions

Apply the [Ponytail](https://github.com/DietrichGebert/ponytail) principle: understand the affected code first; reuse existing code and Python standard library; make the smallest complete change. Do not sacrifice validation, security, or tests to minimize line count.

- No paid model API, model SDK, API secrets or unattended AI inference.
- Never present reference solutions or mock data as actual ChatGPT research results.
- Do not inspect `lab/solutions.py` before making a blinded repair attempt.
- Preserve failed attempts in experiment logs rather than silently discarding them.
- Every functional change needs a reproducible test. Run `python -m unittest discover -s tests -v`.
- `--module` runs trusted Python code: do not imply the evaluator safely handles untrusted submissions.
- Record what was not checked and any remaining risks in PR descriptions.
- Compare only the exact same case suite and inputs. Track regressions alongside improvements; no cherry-picking results.
- Keep copied third-party tests and license notices intact. Pin upstream commit hashes and do not claim public tests are blind.
- For real-world issue replays, preserve pristine upstream source snapshots and copyright, place local fixes in separate candidate artifacts, and verify the unmodified baseline before claiming a repair.

- Prefer work that advances the [research success gates](docs/RESEARCH_GOAL.md) over increasing commit, case or test counts.
- Freeze [strategy memory](docs/STRATEGY_MEMORY.md) before controlled comparisons; do not expose independently withheld answers to repair sessions.
- Clearly separate an external-memory workflow improvement from a change to model weights or internal reasoning tokens.
## Research-first change policy

- Prioritize **G2** in [the roadmap](docs/ROADMAP.md): six externally selected
  defect families, one frozen first-attempt candidate for each Chat A/B arm,
  and independent assessor-held scoring after both commits. Until a real
  assessor exists, clearly report `0/6 — blocked`; do not simulate one.
- Before writing code, identify the research gate, a measurable completion
  criterion and the real failure preventing that gate. If the change only
  increases test, CI or commit counts, **do not make it**.
- Batch related changes into **one reviewable PR per meaningful deliverable**.
  Separate commits only for necessary candidate-freeze chronology or genuine
  failures; never split a single fix into multiple cosmetic versions.
- Reuse the current standard-library grader and GitHub Actions. Change them
  only when a **reproduced, trial-blocking defect** justifies it.
- Keep G3, G4 and v1.0 pending until their actual acceptance evidence exists.
  A CI pass, public replay or prepared study document is not a hidden score.
- If external participation is the blocker, deliver a precise assessor
  handoff and stop making unrelated engineering edits.
