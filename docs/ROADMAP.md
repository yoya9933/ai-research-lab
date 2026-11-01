# Roadmap

- [x] v0.1.0: Small reproducible debugging benchmark; Python-only grader; tests and CI.
- [x] v0.1.1: Isolate mutable inputs, add strict evaluator exit status, and regression tests.
- [x] v0.1.2: Record a partial, explicitly unblinded chat-authored repair with CI-verifiable counts.
- [x] v0.1.3: Evaluate frozen candidate on a separately scored post-commit follow-up suite.
- [x] v0.1.4: Compare versioned evaluator reports, detect regressions, reject mismatched suites.
- [x] v0.1.5: Add deterministic property validation across 411 inputs for repaired functions.
- [ ] v0.2: Blinded held-out cases and more diverse defects; improve contamination controls.
- [ ] v0.3: Compare repair workflows using manually recorded chat sessions, not API calls.
- [ ] v0.4: Error taxonomy, result aggregation and uncertainty estimates.
- [ ] v1.0: Publish a reproducible, reviewed case study with limitations.

Versions indicate scope, **not** demonstrated improvements in AI capability.
- [x] v0.2.0 (partial): Pin 3 Exercism tasks and 29 original MIT-licensed tests; verify incomplete baseline.
- [x] v0.2.1: Record a chat-authored candidate and externally sourced test scores, disclose exposure.
- [x] v0.2.2: Commit a second exercise candidate before viewing upstream test files.
- [x] v0.2.3: Import original upstream tests after candidate freeze; preserve actual scores.
- [ ] v0.3: Investigate source-attributed real-world defects and independent regression evidence.
- [x] v0.3.0: Reproduce a real upstream issue (#30 in humanize) using a pinned pre-fix source snapshot and external reporter's test case.
- [x] v0.3.1: Commit a minimal candidate fix separate from baseline and run correctness/regression tests.
- [x] v0.3.2: Replay a second human-reported formatting regression on the unchanged candidate; disclose shared root cause.

## External bug corpus status (2026-11-01)

- [x] **Non-blind reproducibility milestone:** Eight distinct locally replayed
  defect families across five upstream projects (counting humanize #20/#30 as
  one family, and explicitly flagging unmerged humanize PR #486). Sources,
  licenses, pinned commits, candidate comparisons and statuses are audited in
  [the evidence ledger](REAL_WORLD_CASES.md).
- [x] **Post-freeze bounded checks:** more-itertools has 372 deterministic
  input pairs validated after the candidate was committed; the frozen
  candidate source is hash-checked. Boltons and tokenize-rt retained their
  unsuccessful post-freeze property outcomes and separate later candidates.
- [x] **Pygments exposure chronology:** Two original third-party tests were
  fetched only after the candidate was committed, and 144 further
  investigator-authored input observations passed in CI. The public fix
  was already known, so neither result is a blinded ability score.
- [ ] **Not yet achieved:** Independently authored and withheld grading
  material for multiple real defects, uncontaminated repeated model trials,
  statistically defensible uncertainty estimates or a general AI-improvement
  claim. Keep v0.2 and the broader v0.3 research goals open.
