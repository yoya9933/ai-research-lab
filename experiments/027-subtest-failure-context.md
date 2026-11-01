# Experiment 027 — preserve unittest subTest failures with context

Date: 2026-11-01. Engineering grader integrity, **not** a repair/AI trial.

## Root cause and testable hypothesis

The existing `RecordingResult` recorded `startTest`, `addFailure`,
`addError` and `addSuccess`, but not the **`addSubTest`** callback.
A parent with two failed `subTest()` contexts could be marked failing
while leaving its recorded actual value `"incomplete"` and error `null`.
To preserve diagnostically useful failures, attach every subtest traceback
and its exact `subtest.id()` (which contains named context parameters)
to the same parent result. A `subTest()` does **not** create a new
independent score or an AI experiment.

## Actual first CI failure, retained

- [PR #61 first CI #41292399954](https://github.com/yoya9933/ai-research-lab/actions/runs/41292399954)
  completed **failure** on two synthetic assertions.
- The initial candidate did capture both `AssertionError` tracebacks
  and classify a `RuntimeError` as an error, but Python's
  `_exc_info_to_string(err, subtest)` omitted the named subtest context
  from those tracebacks. The tests required `number=1`, `number=2`
  and `value=123`; none appeared. This was a **new local formatting
  oversight**, not an upstream Exercism regression.
- A follow-up commit prefixes each traceback with `subtest.id()` rather
  than weakening those tests. The original two failure assertions,
  the successful-subtest control, and the entire existing pinned
  29/44 Exercism score suite remain in place. Verify the corrected
  PR head with GitHub Actions before merging.

## Verification and limitations

```bash
python -m unittest tests.test_exercism_runner_isolation -v
python -m unittest discover -s tests -v
```

The synthetic parent test is **one** scored unit despite multiple
`subTest` failures. The failed tracebacks and intermediate CI run
remain part of this experiment's provenance. This procedure does
not establish independent hidden tests, full upstream coverage,
untrusted Python sandboxing or AI debugging capability improvements.
