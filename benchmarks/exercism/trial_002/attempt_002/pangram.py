"""Chat-authored candidate based on public instructions, prior to reading tests."""

from string import ascii_lowercase


def is_pangram(sentence):
    return set(ascii_lowercase) <= set(sentence.lower())
