# Experiment 028 — unittest fixture failures versus real subtest errors

Date: 2026-11-01. Grader-integrity investigation; **not an AI repair trial**.

## Mechanism

A `unittest` `tearDownClass`/`tearDownModule` failure is recorded
without `startTest` and, unlike an assertion failure in the test itself,
should **invalidate** the score instead of being assigned to the final test.
A `setUpClass` failure similarly produces no genuine started test.

## Initial CI failure (preserved)

[PR #67 initial CI #41295132783](https://github.com/yoya9933/ai-research-lab/actions/runs/41295132783)
**failed** (one existing unittest error) because its first implementation
classified *all* `result.errors` identities absent from `startTest`
as fixture errors. Real failed `subTest` callbacks appear under separate
subtest IDs in `result.errors`. The unchanged existing test
`test_subtest_errors_and_successful_subtests_are_classified` caught the
false positive, reporting `value=123` as incorrectly unscored.

## Correction and declared acceptance

On a failing `addSubTest`, explicitly remember `subtest.id()` from
the stdlib callback. Reject only error IDs that are neither a started
parent `test.id()` nor a recorded failing subtest ID. Continue to keep
fixture exceptions out of the previous case and preserve their traceback.

- Synthetic **`setUpClass`, `tearDownClass`, `tearDownModule`** errors
  are rejected, not reported as candidate incorrectness.
- Real failed `subTest` is still a valid scored parent failure,
  including an error raised inside a subtest.
- The unmodified frozen 29/44 Exercism upstream test suites must remain
  executable with identical recorded outcomes.

Reproduce with `python -m unittest tests.test_exercism_runner_isolation -v`
or the repository's complete standard-library unittest discovery.
**Do not claim final success until PR CI passes**, and retain links to
all failing runs. No independent held-out tests, throughput, or AI
capability claim is made.
