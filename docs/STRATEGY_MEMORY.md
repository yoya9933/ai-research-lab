# Strategy memory v0 — reusable repair heuristics

This is an **intervention artifact**, not a model fine-tune, a secret answer key, or evidence that AI ability improved. It contains general process lessons from **prior** documented projects. Future comparison tasks must not overlap those solved cases; freeze this file's Git blob before conducting A/B trials.

## Lessons with provenance

1. **Freeze and identify inputs before judging a change.** Pin the original source, candidate commit and third-party license. Run the same inputs against baseline and repair. Do not silently edit a frozen candidate after test disclosure. Evidence: [Exercism trial 002](../experiments/007-postfreeze-upstream-tests.md).
2. **Distinguish a reproducible bug from a repaired bug.** A passing baseline test may intentionally assert the *incorrect* historical behavior. Demand a separate candidate and unchanged control cases. Evidence: [humanize #30](../experiments/008-historical-humanize-bug.md) and [repair](../experiments/009-historical-humanize-repair.md).
3. **When a patch seems ineffective, check execution integrity first.** Python may import stale bytecode from an inherited cache; discard copied `__pycache__` and verify the actual source loaded. Evidence: [boltons reproduction failure](../experiments/012-boltons-rotation-cache-failure.md).
4. **Keep failed follow-ups, not just first successes.** A bounded property matrix can discover residual defects even when published cases pass. Treat the original candidate as fixed evidence; propose a separately versioned second repair. Evidence: [tokenize-rt follow-up](../experiments/015-tokenize-rt-postfreeze.md) and [secondary candidate](../experiments/016-tokenize-rt-roundtrip.md).
5. **Diagnose the grader as well as the code under test.** Import errors, duplicate tests, skips and dropped `subTest` details can make a score misleading. Do not count test-runner defects as target-project failures. Evidence: [unittest subtest evidence](../experiments/027-subtest-failure-context.md) and [fixture error evidence](../experiments/028-unittest-fixture-error-grading.md).
6. **Report regressions and the true unit of analysis.** A fix count is meaningful only against the same suite and expected outputs. Hundreds of correlated property inputs are not hundreds of independent repair trials. Evidence: [study protocol](PROTOCOL.md) and [real-world ledger](REAL_WORLD_CASES.md).

## Applying this memory

Use the smallest relevant lesson as a **hypothesis/checklist** at the start of a new repair. Do not copy an old patch into a new task without reading its actual interface and tests. Test each hypothesis, preserve negative feedback, and log which lesson influenced the decision.

## Treatment versus control

- **Control (A):** fresh Chat session, the same problem statement, coding tools and evaluation rules, **without this strategy memory file or prior experiment logs**.
- **Memory-assisted (B):** fresh Chat session, same problem statement, tools and rules, **plus this exact frozen memory file**.
- Neither condition may view withheld test cases or private assessor answers before its candidate commit is frozen.
- This file must be frozen to a single Git blob/SHA before the first preregistered task and kept identical across the study. Previous public issue/patch exposure and possible pretraining leakage must be disclosed.

Treat results as a test of a **workflow and provided context**, never as a change to the model's trained weights.
