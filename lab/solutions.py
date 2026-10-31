"""Reference answer key. Read only after completing a blinded attempt."""


def clamp(value, low, high):
    return max(low, min(value, high))


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def median(values):
    ordered = sorted(values)
    mid = len(ordered) // 2
    return ordered[mid] if len(ordered) % 2 else (ordered[mid - 1] + ordered[mid]) / 2


def unique(values):
    return list(dict.fromkeys(values))


def normalize(values):
    total = sum(values)
    return [v / total for v in values] if total else [0 for _ in values]


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def chunks(values, size):
    return [values[i:i + size] for i in range(0, len(values), size)]


def palindrome(value):
    normalized = "".join(ch.lower() for ch in value if ch.isalnum())
    return normalized == normalized[::-1]


def longest(words):
    return max(words, key=len, default="")


def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
