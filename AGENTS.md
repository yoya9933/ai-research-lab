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
