"""Chat-authored, unblinded completion of the published Exercism task."""


def is_isogram(phrase):
    letters = [character.lower() for character in phrase if character.isalpha()]
    return len(letters) == len(set(letters))
