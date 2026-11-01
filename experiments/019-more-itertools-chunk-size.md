# Experiment 019 — more-itertools chunk-size replay and local repair

**Question:** On a third-party accepted upstream bug, can an offline,
temporarily patched excerpt correct boundary behavior while keeping ordinary
outputs unchanged? This is a reproducibility question, **not** a test of
general AI progress.

## Provenance and chronology

- Public [more-itertools PR #1342](https://github.com/more-itertools/more-itertools/pull/1342)
  filed 2026-10-26, upstream merged 2026-10-30. Its author already
  published both the fix and tests **before** this chat attempt.
- The pre-fix upstream commit is `4aeb4338ae1407d8da9723e86da99efeb446f719`;
  upstream `more.py` blob `9c56ab37558733ece94d676f71d502d8048bc1d5`.
  The original function is copied verbatim into a 51-line standalone
  source excerpt with only an `islice` import added. The full upstream
  package is not vendored or tested.
- [Local baseline PR #43](https://github.com/yoya9933/ai-research-lab/pull/43)
  was merged at `d5bc09001b22cbc12007fb9522aaf06a888964ce`
  before this separately named candidate was authored.
- **Failure preserved:** [CI run 41285463183](https://github.com/yoya9933/ai-research-lab/actions/runs/41285463183)
  initially failed because our *integrity test* used a literal backslash
  instead of a Git blob header NUL byte. This was a harness error, not
  an upstream code regression; the follow-up commit fixed it.
  [PR CI 41285501516](https://github.com/yoya9933/ai-research-lab/actions/runs/41285501516)
  and [main CI 41285529580](https://github.com/yoya9933/ai-research-lab/actions/runs/41285529580)
  both subsequently passed.
- The candidate in this experiment inserts two size guards before
  the function's first `iter(iterable)`; it never changes the frozen
  upstream excerpt and deliberately reuses the baseline's ten inputs.

## Hypothesis / validation scope

A nonpositive size should not consume a source iterator; zero should yield
no chunks and negative should fail with the stable domain error
`ValueError('n must be at least 0')`. For the ten **existing** observations,
the hypothesis predicts four changed outcomes and six unchanged outcomes.
The sixth unchanged observation includes the negative/empty input, whose
error **type** was already `ValueError` on baseline; a supplemental check
looks at the error message and noniterable behavior to distinguish those.

**Reproduce:** `python -m unittest discover -s tests -v` and
`python -m unittest tests.test_more_itertools_1342_candidate -v`.
The GitHub Actions logs, not claims in this document, are the execution
evidence. The full upstream pytest suite, other Python interpreters and
other `more-itertools` functions remain unchecked.

**Exposure limitation:** The original PR's patch and test description were
seen before writing this code. Newly written assertions are not hidden,
the excerpt is not the full source tree, and pretrained knowledge cannot
be excluded. No external model API or paid inference was used.

## Post-freeze follow-up

The accepted-fix candidate was frozen at commit
`33cd99acfdf62b13033db865f4b0302a6a7ebd96` before the new
`followup.py` was authored. The frozen patch source Git blob is
`b26e35b35a8911e8a117e3f7f10a703291b4b585`; the standard
frozen-source integrity test now verifies this local copy.
The separate, investigator-authored suite replays exactly the same 574
positive-size/length combinations against both baseline and candidate,
with an independent flattening, chunk-size, and size-balance oracle.
It also probes zero and negative sizes with an iterable that raises on
any `__iter__` access. Failures are returned and displayed, not silently
dropped. Results require actual GitHub Actions execution, and no
pretraining-independence or blind-test status is claimed.
