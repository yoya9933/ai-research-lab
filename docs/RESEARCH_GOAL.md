# Core research goal and measurement gates

## Question

**Can a ChatGPT-only, GitHub-MCP-assisted workflow that reuses verified lessons from past work outperform an otherwise comparable fresh-chat workflow on genuinely new problems?**

The outcome of interest is improved **task performance with external memory and feedback**, not changing the model's weights, consuming more invisible reasoning tokens, or counting commits. No Work, model API, paid inference, autonomous daemon or hidden Chat token API is involved.

## What already exists

The repository provides deterministic grading, source-pinned historical bug replays, preserved failure reports and GitHub Actions. See [source-attributed evidence](REAL_WORLD_CASES.md). These are successful *engineering checks*, not proof that the method improves across unseen tasks. [Issue #7](https://github.com/yoya9933/ai-research-lab/issues/7) remains open for independent held-out evaluation.

## The improvement mechanism

1. **Observe and log.** Treat unexpected output or CI failure as evidence. Capture the exact task, model/workflow condition, hypothesis, original source commit, candidate SHA, grader command, source links, and what failed.
2. **Distill a transferable lesson.** Record the smallest *general* rule supported by evidence in [strategy memory](STRATEGY_MEMORY.md), with a link to a real experiment, a limitation and a counterexample when known. No copied hidden answer keys.
3. **Freeze that memory.** Before evaluating on new tasks, select a specific memory Git blob and make no alterations to it during the experiment.
4. **Compare fairly.** A fresh-chat control uses the same tools and fixed instructions without strategy memory; the treatment gets only the frozen, previously learned strategy memory. Separate fresh conversations, same model configuration, problem description, allowed tools, visible tests and attempt budget. Record model/version and any leakage.
5. **Let an independent assessor grade.** Tasks, hidden regression tests and expected behavior are selected and withheld by a person external to the repairing sessions. Both candidates are committed *before* test disclosure. Never expose confidential test sources in public CI; use only tests the assessor permits publication of.
6. **Learn from the complete result.** Record successes, failures, unchanged errors and regressions, and evaluate whether memory actually improved new-task outcomes. A failed comparative trial is useful evidence and must not be erased.

## First controlled comparison (preregister before any repair)

| Design dimension | Rule |
| --- | --- |
| Unit | One independently selected defect family, **not** a unittest method or test input |
| Conditions | A: Chat + GitHub MCP, no curated memory; B: same setup + frozen `STRATEGY_MEMORY.md` |
| Selection | Assessor chooses cases under published inclusion/exclusion criteria without consulting candidate outcomes |
| Pilot | 6 distinct defects to test procedure only; do not infer superiority from this pilot |
| Confirmatory goal | 20 independent defect families, chosen **in advance**; no early stopping for good results |
| Attempts | One frozen first-attempt patch per task/condition; post-feedback fixes tracked separately |
| Budget | Fixed number of interactive turns/tool invocations per task; **do not claim to measure internal reasoning tokens** |
| Primary endpoint | Binary: all preregistered hidden regression assertions pass, with no regression in existing visible tests |
| Secondary endpoints | Number of fixed/regressed cases, time, tool calls, failed first attempts and assessor intervention |
| Analysis | Per-family A/B wins, losses and ties; effect-size difference. Statistical uncertainty only if sampling and independence assumptions justify it |
| Disclosure | Task IDs, candidate SHAs, exact frozen memory hash, assessor provenance, reveal chronology, CI evidence and all failures |

The design does **not** guarantee total independence: pretrained model knowledge, cross-conversation memory, unequal context length and assessor influence can confound the result. Report any such violations; do not label the study blind if the relevant criteria were not met.

## Success criteria

- **Engineering gate (mostly achieved):** all reproducible tests pass; failures, external licenses and code provenance remain traceable.
- **Memory gate:** a versioned, evidence-linked strategy memory is usable by a new Chat session without relying on the current conversation.
- **Trial gate:** an assessor-run paired pilot is completed and **all** outcomes, including failures, are preserved.
- **Evidence gate:** the pre-registered comparison on new independent tasks is executed, with honest uncertainty and no cherry-picking. The result may be *negative*: the system must be able to conclude that memory did not help.
- **Transfer gate:** repeat on a different domain (e.g., data analysis or mathematical reasoning), without assuming debugging results generalize.
- **Publication gate:** v1.0 report describes protocol, outcomes, failure cases, limitations and exact reproducible references.

## Autonomous iteration policy

At the start of each Chat + MCP session, read this goal, the [roadmap](ROADMAP.md), the existing [protocol](PROTOCOL.md), open issues and CI. Select the next step with the **highest impact on an unverified gate**, not the easiest new commit. Use Ponytail: prefer reusing tests, Python standard library and GitHub-native CI; avoid new dependencies or a custom orchestration framework unless existing tools cannot meet the requirement.

Only merge a scoped PR after the **current PR head** passes CI and meaningful tests. Preserve rejected candidates, failed CI and unresolved findings. Do not create synthetic measurements and call them real trials. No ongoing work can occur without an actual Chat/automation trigger; do not silently substitute Work or a paid API.

**Important blocker:** The independent assessor and their withheld cases cannot be created or impersonated by this same repairing assistant. Preparatory code can be implemented autonomously; claims of independent evaluation must wait until that gate is genuinely satisfied.
