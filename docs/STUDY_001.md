# Study 001 — does experience memory improve fresh-chat repair?

**Status: PREREGISTERED, NOT RUN.** No independent judge, withheld test file, pilot task result or confirmatory success exists yet. The purpose of this commit is to fix the evaluation rules *before* observing outcomes.

- Goal: [research objective](RESEARCH_GOAL.md)
- Treatment material: [strategy memory](STRATEGY_MEMORY.md)
- **Frozen strategy Git blob:** `405e418906d0bb81ce8324b341d6d73f593ae571`
- Study ID: `paired-memory-001`
- Model interface: ChatGPT **Chat**, GitHub MCP, Python standard-library tests and GitHub Actions; **no Work, paid model API, or unattended inference**.
- Eligible cases: new-to-this-study, independently reported Python defects with a legal, pinned pre-fix source snapshot and independent grading assertions withheld by an external assessor. Previously solved lab cases are **excluded**.

## Conditions

Both sides must use fresh separate Chat conversations, the same model/configuration if accessible, the same issue description, identical source access and tool permissions, and the same visible test requirements. The assessor randomizes whether A or B runs first per task and discloses the complete allocation after scoring. Record contamination/memory concerns.

**Common initial instruction (both arms):**

> Repair the supplied source-pinned bug using ChatGPT Chat and GitHub MCP only. Read the permitted task specification and repository code; do not access private/held-out tests, published fix commits, prior candidate patches or another arm's work. Write your hypothesis, apply the smallest justified patch, run only visible tests, and freeze exactly one first-attempt candidate to a Git commit before the assessor reveals held-out assertions. Preserve all errors and regressions. Do not use Work, paid model APIs or paid services.

**A — control additional instruction:**

> Do not consult this project's historical experiment logs or docs/STRATEGY_MEMORY.md. Use the common instruction and task evidence only.

**B — memory-assisted additional instruction:**

> Before editing the candidate, read docs/STRATEGY_MEMORY.md at frozen Git blob 405e418906d0bb81ce8324b341d6d73f593ae571. Use its process rules as a checklist; do not retrieve historical task solutions or hidden answer keys.

The difference between arms is deliberately the **availability of previously verified process memory**. Because B has additional context, the inference is about the value of that workflow aid, not model weights or equal tokens.

## Precommitted rules

- **Pilot:** 6 distinct independently selected defect families, used only to verify the logistics and grader. Do **not** pool its scores into the confirmatory result.
- **Confirmatory target:** 20 further independently selected defect families. Selection and exclusions are recorded by the assessor *before* either condition starts. Do not stop early due to observed outcomes or substitute easy cases.
- **Visible feedback:** at most two visible-test cycles per condition, before its first candidate freeze. Record each failure, tool call count, model configuration when available, and deviations; the cap does **not** measure hidden reasoning tokens.
- **Hidden grading:** same assessor-held, previously undisclosed assertions applied to both frozen candidates only **after both commit SHAs exist**. Do not alter either frozen candidate after reveal. Unsupported confidential grader materials must not be printed to public CI logs.
- **Primary endpoint per defect family:** one binary score per condition: all preregistered hidden tests pass **and** no originally passing visible control regresses.
- **Analysis:** report A-only wins, B-only wins, ties, the paired percentage-point difference and all exclusions. Include full per-family results and disclose source/memory leakage. Do not claim statistical significance unless the assessor's sampling and independence assumptions support an appropriate preselected analysis.
- **Negative results count.** If B is worse, tied or unusable, publish that result. Post-feedback revisions are new experiments, not edits to the original outcome.
- **Human intervention:** assessor controls case selection and held-out grading but cannot coach one arm's implementation. Any coaching or model-memory carryover is disclosed.

## Minimum evidence for each case

Assessor identity by non-sensitive role, external issue and pinned-source URLs/SHAs, origin/availability of hidden tests, declared inclusion rule, condition order, exact prompts or redacted links, model/version where known, candidate SHA for A and B, frozen memory blob, visible CI run URLs, independent reveal event, hidden score, regressions, attempt/tool counts, and all protocol deviations.

## Integrity and limitations

`tests/test_strategy_freeze.py` recomputes the Git object hash of the actual strategy file using the Python standard library. A change to the treatment source will fail CI until **a new registered study version** and explicitly new hash are introduced. A Git hash verifies exact bytes within this repository, **not** that a hidden assessor was independent or that ChatGPT's prior training did not already contain the task.

GitHub cannot secretly grade a truly private answer key merely because a PR was merged. This study remains in **awaiting independent assessor** status until someone genuinely outside both repairing conversations controls the withheld cases. Do not synthesize such an assessor or present this registration as completed AI improvement.
