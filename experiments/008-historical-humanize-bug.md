# Experiment 008: replay externally reported time-formatting bug

Date: 2026-11-01
Upstream issue: https://github.com/python-humanize/humanize/issues/30
Pinned pre-fix source: `9528daf55fd7178c025f7294b8e349f8b3524175`
Status: baseline reproduced and verified by CI; no repair measured yet.

## Goal

Reproduce a **real user-submitted bug report** in a historical upstream snapshot, not in a self-authored toy problem. Preserve the upstream MIT license and source SHA. Do not read upstream patch contents before recording our candidate fix.

## Published evidence from the reporter

- For 32399 seconds with minimum minute precision and 0 decimal places, expected `9 hours`; reported `8 hours and 60 minutes`.
- Another user reported a related hour/plural artifact: `1 day and 1 hours` for 91500 seconds at minimum hours and zero decimals.

## Reproduction

```bash
python -m benchmarks.bugs.humanize_30.reproduce
python -m unittest discover -s tests -v
```

Test assertions intentionally check that the historical **defective** output is present. This stage is the baseline only; a second Git commit/PR must implement a candidate repair and verify corrected outputs without overwriting the original source snapshot.

## Verified baseline

[GitHub Actions run #41224280254](https://github.com/yoya9933/ai-research-lab/actions/runs/41224280254) ran **35 passing unit tests** and executed the pinned original package. It printed `8 hours and 60 minutes` and `1 day and 1 hours`, matching the reporter and follow-up report. These are reproduced **bugs**, not passing repair cases.

## Validity limitations

The upstream issue was reported by an independent human, but its code and history are public. This is a historical replay, not a genuinely blind model evaluation; AI pretraining exposure cannot be excluded. Historical Python source contains ordinary imports and is executed locally as trusted vendored code, not sandboxed.
