# Experiment 002: post-commit follow-up

Date: 2026-11-01
Candidate: `lab.attempt_001`
Candidate frozen before test authoring: [main commit bd7eb01](https://github.com/yoya9933/ai-research-lab/commit/bd7eb01cf6f0f9c9d89bd569794dcc99b7482ee9)
Status: pending CI verification; **not independently blinded**

## Purpose

Evaluate the *unchanged* repair candidate on 20 additional inputs created after the patch commit. The time ordering is auditable.

## Expected counts to verify

| Version | Original 24 cases | Additional 20 cases |
| --- | ---: | ---: |
| Buggy baseline | 11 | 8 |
| Chat-authored partial patch | 16 | 11 |
| Reference answer key (not AI work) | 24 | 20 |

## Reproduce

```bash
python -m unittest discover -s tests -v
python -m lab evaluate --module lab.buggy --suite followup
python -m lab evaluate --module lab.attempt_001 --suite followup
python -m lab evaluate --module lab.solutions --suite followup --require-all-pass
```

## Threats to validity

The same assistant saw the reference answer key, wrote the repair, and authored these follow-up tests. This **is not a blind or independent experiment** and does not prove model improvement or generalization. The 24-case and 20-case results come from different test suites and must not be compared as if they were the same denominator. Future research needs externally authored tasks and an answer key never exposed to the repair model.
