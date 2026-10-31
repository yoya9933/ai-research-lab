# Experiment 006: freeze a candidate before reading external tests

Date: 2026-11-01
Track: `benchmarks/exercism/trial_002/`
Source: [Exercism Python @ 6105f6d9d3ef66ce3d5c8f529d2882af3d76b706](https://github.com/exercism/python/commit/6105f6d9d3ef66ce3d5c8f529d2882af3d76b706)

## Method: pre-registration

The assistant **read only the upstream written exercise instructions and starter signatures** for Luhn, Pangram, and Armstrong Numbers before writing `attempt_002/`. Upstream test files for these three exercises were **not opened or read in this conversation before candidate code was committed**. These source files are MIT-licensed; the license is included one level above.

The candidate implements:
- Luhn checksum on space-stripped ASCII digit strings, rejecting short or invalid input.
- Case-insensitive English-alphabet coverage for Pangram.
- Digit-power sum equality for nonnegative Armstrong numbers.

The three smoke tests in `tests/test_preregistered_candidate.py` are derived from the *written instructions*, not imported from the upstream test files.

## Next verification (must happen later)

1. Commit and merge this candidate unchanged.
2. Only then fetch the original upstream `luhn_test.py`, `pangram_test.py`, and `armstrong_numbers_test.py` from the pinned commit.
3. Run the candidate and the stubs on the imported tests. Preserve all failures and score differences before any repairs.
4. If errors occur, create a **new attempt** rather than rewriting the frozen candidate.

## Threats to validity

This is a *test-content-unseen-in-this-conversation* protocol, **not guaranteed double-blind research**. Exercises are public, the model may have learned them in training, and the assistant chooses the tasks and writes the code. The three tasks are educational exercises, not field bug reports.
