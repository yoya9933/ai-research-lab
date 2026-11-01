# Roadmap — research gates, not commit counts

**Active milestone: G2, independent six-defect A/B pilot — 0/6 externally graded.**
The previous engineering work is sufficient to start a trial. The missing
ingredient is **an external assessor controlling new defect selection and
withheld test answers**, not another evaluator, CI feature or benchmark count.

## Success gates (in order)

| Gate | Acceptance evidence | Status |
| --- | --- | --- |
| G0: Reproducible baseline | Pinned source, license, runnable offline tests, CI and failed-attempt records | **Complete** |
| G1: Reusable frozen memory | [Strategy memory](STRATEGY_MEMORY.md) and its pinned Git blob; [Study 001 preregistration](STUDY_001.md) | **Complete** |
| **G2: Independent pilot (6 defects)** | Independent assessor selected 6 new defect families; 12 separate first-attempt Chat candidate SHAs frozen; same private tests applied to A and B only after both freezes; all 6 paired outcomes and failures recorded | **BLOCKED: 0/6; no external assessor or withheld tests yet** |
| G3: Preregistered comparison (20 *further* defects) | G2 procedure validated, independent assessor runs all 20 selected families with complete A/B outcomes, exclusions and contamination disclosures | **Not started** |
| G4: Domain transfer | Same comparison tested outside Python debugging under a predeclared scoring rule | **Not started** |
| G5: v1.0 report | Reproducible results, null findings, limitations and reviewed evidence | **Not started** |

The [research success criteria](RESEARCH_GOAL.md) and [frozen pilot
protocol](STUDY_001.md) govern these gates. Historical public bug replays,
the 24-case toy benchmark, Exercism exercises and case-level statistics
**do not satisfy G2**, even if their CI is green.

## The next deliverable, not another version bump

An independent assessor must provide six **public task briefs** while
keeping each private grading suite and expected output outside this repo
and all repairing chats. For each task, run two isolated fresh Chat
sessions with the exact preregistered A/B instructions and budget, freeze
both candidate commits, then let the assessor privately grade the **same
tests** and visible controls. Publish all six sanitized paired outcomes,
including failures and skipped tasks. [The operator handoff](STUDY_001.md#g2-operator-handoff--not-yet-executed)
specifies the evidence and commands.

**Current division of work:** Chat + GitHub MCP can prepare public briefs
and candidate commits once supplied, but cannot impersonate an independent
assessor, secretly create unseen answers, or launch separate fresh human
Chat sessions. Until the external role exists, report **G2 blocked**;
do not fill the gap with synthetic blind claims.

## Iteration budget and stop rule

- **One meaningful deliverable per PR:** combine related implementation,
  documentation and regression tests. Keep separate immutable candidate
  commits where test-exposure chronology requires them.
- **No speculative infrastructure work:** a new grader feature,
  serialization check, CI action or version tag requires a reproduced
  blocker that prevents an active G2 trial.
- **Gate-based completion:** G2 is done only with **6/6 valid assessor-run
  paired results**, not a passing CI alone. Do not declare G3/G4 complete
  or v1.0 because unrelated utilities have improved.
- **When blocked:** name the missing external action and stop generating
  filler commits. Preserve existing successful and failed evidence.

## Historical work (completed engineering, not independent A/B evidence)

- [Real-world issue ledger](REAL_WORLD_CASES.md): eight non-blind
  root-cause families across five upstream projects, with pinned
  source/license provenance and both successes and failures.
- [Protocol](PROTOCOL.md): original local toy evaluator, Exercism
  cases, post-freeze properties, comparison reports and GitHub Actions.
- Earlier v0.1–v0.4 implementation labels describe **engineering scope
  only**. A partially implemented error taxonomy is not a completed
  comparative research milestone.
