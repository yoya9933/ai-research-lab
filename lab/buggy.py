"""Intentionally incorrect implementations. Do not use in production."""


def clamp(value, low, high):
    return min(low, max(value, high))


def is_prime(n):
    if n < 2:
        return True
    return all(n % d for d in range(2, n))


def median(values):
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def unique(values):
    return sorted(set(values))


def normalize(values):
    total = sum(values)
    return [v / total for v in values] if total else []


def fibonacci(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def chunks(values, size):
    return [values[i:i + size] for i in range(0, len(values) - size + 1, size)]


def palindrome(value):
    return value == value[::-1]


def longest(words):
    return max(words, default="")


def factorial(n):
    result = 1
    for i in range(1, n):
        result *= i
    return result
