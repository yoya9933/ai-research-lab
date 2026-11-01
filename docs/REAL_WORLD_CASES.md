# Real-world defect evidence ledger — 2026-11-01

This page separates **externally published software defects** from this
project's **investigator-authored tests and local reconstructions**. It is
a source-linked, reproducible **engineering audit**, **not** a blinded
AI-performance leaderboard.

## Independent upstream projects and root-cause families

| Upstream report and observed root cause | Pinned pre-fix source and scope | Local before/after evidence | Upstream status |
| --- | --- | --- | --- |
| [humanize #30](https://github.com/python-humanize/humanize/issues/30) and [#20](https://github.com/python-humanize/humanize/issues/20): rounded duration carries / pluralisation; **one shared family** | `9528daf55fd7178c025f7294b8e349f8b3524175`, partial MIT package | [Baseline/repair](../benchmarks/bugs/humanize_30/README.md): 3 corrected formatting outcomes, 2 unchanged controls on the same five observations | #30 closed; two reports are not two independent root causes |
| [humanize #333](https://github.com/python-humanize/humanize/issues/333): infinity overflows integer guard | Same source, different function | [Baseline/repair](../benchmarks/bugs/humanize_333/README.md): 2 corrected non-finite outcomes, 4 controls | Issue closed |
| [humanize PR #486](https://github.com/python-humanize/humanize/pull/486): signed ordinal suffix lookup | Same source, different function | [Baseline/repair](../benchmarks/bugs/humanize_486/README.md): 7 corrected suffixes, 8 controls | **Closed without merge**; externally proposed but not upstream-accepted |
| [boltons #479](https://github.com/mahmoud/boltons/issues/479): file rotation discards newest retained backup | `967864f89791509f9eb36b22b4579d36b72a6df2`, BSD-licensed subset | [Baseline/repair](../benchmarks/bugs/boltons_479/README.md): 4 changed retention observations, 5 controls | Issue closed; closure alone does not prove upstream acceptance |
| [boltons #480](https://github.com/mahmoud/boltons/issues/480): file permission descriptor fails to clear bits | Same BSD subset, different function | [Baseline/repair](../benchmarks/bugs/boltons_480/README.md): 3 corrected revocations, 6 controls | Issue closed; no claim of upstream patch adoption |
| [tokenize-rt #33](https://github.com/asottile/tokenize-rt/issues/33): no-EOL token has wrong UTF-8 byte offset | `7f89433be049d73e189a903485a93bdf3e56f1a0`, single MIT module | [Baseline/repair](../benchmarks/bugs/tokenize_rt_33/README.md): 3 corrected byte offsets, 3 unchanged input controls | Issue closed with subsequent fix commit; see case README |
| [more-itertools PR #1342](https://github.com/more-itertools/more-itertools/pull/1342): zero/negative chunk sizes lack validation | `4aeb4338ae1407d8da9723e86da99efeb446f719`, standalone MIT **function excerpt**, not full package | [Baseline/repair](../benchmarks/bugs/more_itertools_1342/README.md): 4 changed observations, 6 coarse controls; [post-freeze 372-input property matrix](../experiments/020-more-itertools-postfreeze-properties.md) | **Upstream PR merged** on 2026-10-30 |

This is **seven locally replayed root-cause families across four external
projects** when #30 and #20 are grouped and the **unmerged #486 claim is
clearly marked provisional**. The observations within one family are correlated:
their before/after counts **must not** be added into an AI accuracy metric,
nor mistaken for seven independent repair trials. A passing historical
baseline test deliberately asserts **wrong behavior**, not a repaired build.

## Run and verification evidence

All suites use the existing Python standard-library test runner:

```bash
python -m unittest discover -s tests -v
python -m unittest tests.test_more_itertools_1342_followup -v
```

[PR #45 Actions](https://github.com/yoya9933/ai-research-lab/actions/runs/41285743823)
and its [merged main Actions](https://github.com/yoya9933/ai-research-lab/actions/runs/41285778031)
both completed **success** on 2026-11-01. The specific case files above
describe their baseline observations, pinned source files, licenses,
subprocess or temporary-file boundaries, and original versus candidate
expectations. This does **not** mean the complete upstream test suites ran.

Failures remain visible rather than being rewritten as initial successes:

- [More-itertools CI #41285463183](https://github.com/yoya9933/ai-research-lab/actions/runs/41285463183):
  a **failed harness-integrity check** (incorrect Git blob header) was corrected
  before baseline merge, not misattributed to upstream.
- [Tokenize-rt follow-up CI #41253159050](https://github.com/yoya9933/ai-research-lab/actions/runs/41253159050)
  exposed remaining no-EOL trailing-space roundtrip failures **after**
  the first offset candidate; a **separate** secondary candidate was later
  evaluated. These are investigator-discovered residuals, not external reports.
- [Boltons experiments 017/018](../experiments/017-boltons-from-int-postfreeze.md):
  the first permission candidate still had **63 incorrect roundtrips among
  512** numeric modes; a separate secondary fix addressed that property.
  These 512 modes are not 512 independent AI trials.

## What remains unproven

All initial external reports and their public fixes/diagnoses were exposed
to the investigator before the corresponding local candidate. The
post-freeze property tests were **authored by the same investigator after
the candidate commit**, not obtained from an independent blinded assessor.
Pretraining contamination cannot be excluded. Case selection and stopping
rules were not registered for a statistically powered performance
comparison, and no repeated independent chat trials were performed.

Therefore **[Issue #7](https://github.com/yoya9933/ai-research-lab/issues/7)
remains open** for genuine independently administered held-out tasks,
candidate-freeze chronology where external tests were not seen first,
and repeated protocolled trials. This corpus establishes source-attributed
reproducibility and bounded local behavior only. No paid model API or
unattended agent execution is required.
