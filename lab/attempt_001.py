"""First chat-authored repair attempt, unblinded; see experiments/001-debugging.md."""

from .buggy import fibonacci, is_prime, longest, median, normalize, palindrome, unique


def clamp(value, low, high):
    return max(low, min(value, high))


def chunks(values, size):
    return [values[i:i + size] for i in range(0, len(values), size)]


def factorial(n):
    result = 1
    for value in range(2, n + 1):
        result *= value
    return result
