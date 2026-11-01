# Experiment 025: post-freeze Pygments literal-language matrix

Date: 2026-11-01. Explicitly NOT BLIND.

## Provenance

Pygments upstream PR #3190 was publicly merged and its fix was known before
this lab began. The original BSD module is pinned to upstream pre-fix commit
c97c0b54f58d496e34f4b37eb9d0c482e79e21b3. The local candidate was frozen
in PR #50 (patch Git blob 59d075d0763feb68fb2385b71f95cf2835c68afe).
PR #51 subsequently replayed two upstream-authored tests on that candidate.
Its first CI run 41286453516 FAILED due to our missing Python dictionary brace
in the source-integrity test. Corrected PR CI 41286548196 and merged main CI
41286575592 both SUCCEEDED without altering the candidate.

## Hypothesis and input domain

Eight literal token values include empty text, Unicode, a backslash, a square
bracket, and a plus sign. For each first/second token pair, test one duplicate
list [first, first, second] (64 lists). Add eight singleton control lists. Test
each with no regex wrapper and with start/end anchors: 144 deterministic
observations per source variant, consisting of 128 duplicate rows and 16
singleton controls.

For every input compare the unchanged baseline and the same frozen candidate.
The candidate pattern should equal the corresponding pattern generated from
unique words. Both variants should exactly match the original literal words
among a declared fixed probe set. All 16 singleton observations must be equal
before/after. Do not assume every duplicate list changes serialized output:
some may already have a canonical pattern.

Run python -m unittest tests.test_pygments_3190_properties -v or the full
standard-library unittest discovery. The hypotheses above are NOT measured
results until independently verified by GitHub Actions.

## Remaining limits

This is a post-commit, investigator-authored test, NOT a blinded/independent
model trial. A hundred-plus inputs do not make a hundred independent defects.
It tests only this BSD single-module excerpt, fixed literals and two anchors;
it does not establish regex DoS safety, speed, arbitrary Unicode or full
upstream Pygments correctness. No paid model APIs or agents were used.
