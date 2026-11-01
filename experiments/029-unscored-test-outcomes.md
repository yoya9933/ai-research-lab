# Experiment 029 — distinguish unfinished unittest cases from excluded outcomes

Date: 2026-11-02. This tests evaluator integrity, **not AI skill**.

## Problem and initial failed CI

The third-party Exercism grader initializes each test record as
`actual="incomplete"`. An overridden `unittest.TestCase.run` can invoke
`result.startTest` and `result.stopTest` without any outcome callback.
The previous score checks could accept that record as an ordinary failed
test when the total count and unique identity matched.

[Initial PR #75 CI #41348215243](https://github.com/yoya9933/ai-research-lab/actions/runs/41348215243)
**failed** its full unittest discovery: three existing tests covering
native `@skip`, `@expectedFailure` and unexpected success expected
the prior `Unscorable upstream test outcomes` diagnostic. The first
implementation checked the generic `incomplete` state *before* those
specific exclusion flags, so it returned a less informative exception.
This was a **local validation-order mistake**, not a new upstream bug.

## Correction and explicit scope

Run the existing skip/expected-failure/unexpected-success rejection
**first**, then reject remaining `actual="incomplete"` records with
their test IDs. A separate synthetic `TestCase.run` reproduces the
missing-outcome callback case; ordinary failed test methods retain their
recorded failure/error and still score as failures.

Checks:
- `python -m unittest tests.test_exercism_runner_isolation -v`
- `python -m unittest discover -s tests -v`

**CI outcomes must be independently checked before merger.** No new
hidden grading cases, external assessor, blind trials or general model
improvement are claimed.
