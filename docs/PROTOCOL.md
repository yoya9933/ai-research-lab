# Experiment protocol

## Question

Can a chat-based model improve defect repair through explicit hypotheses, deterministic tests and preserved feedback, without using model APIs?

## Method

1. Select a bug from `lab.buggy` with known cases. Don't read `lab.solutions` until the attempt is complete.
2. Record the attempt date, code commit, exact prompt, hypothesis, patch, test command, test output, and whether any answer-key information was exposed.
3. Run the evaluator on trusted candidate code. A case passes only when the result exactly equals the expected value; exceptions count as failures.
4. Report passed cases / total cases. Keep failed attempts and note threats to validity.
5. Re-run all tests after changes and review the diff in a pull request.

## Limitations

The 10 tasks are small and hand-authored, not representative of real software engineering. The answer key exists in this repository, so blinding relies on process discipline and cannot be enforced. Tests may miss bugs. The grader imports candidate modules and must not execute untrusted code. ChatGPT internal token budgets cannot be controlled or retrieved. Claims about model improvement require independent repeated attempts and separate held-out tasks.
