"""Deterministic input/output cases for the ten debugging tasks."""

CASES = {
    "clamp": [((5, 1, 10), 5), ((-2, 1, 10), 1), ((20, 1, 10), 10)],
    "is_prime": [((1,), False), ((2,), True), ((9,), False)],
    "median": [(([1, 2, 3, 4],), 2.5), (([9, 1, 5],), 5)],
    "unique": [(([3, 1, 3, 2],), [3, 1, 2]), (([],), [])],
    "normalize": [(([1, 1],), [0.5, 0.5]), (([0, 0],), [0, 0])],
    "fibonacci": [((0,), 0), ((1,), 1), ((7,), 13)],
    "chunks": [(([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]), (([1, 2], 2), [[1, 2]])],
    "palindrome": [(("A man, a plan, a canal: Panama",), True), (("hello",), False)],
    "longest": [((["z", "alpha", "cat"],), "alpha"), (([],), "")],
    "factorial": [((0,), 1), ((4,), 24), ((5,), 120)],
}

# Post-commit edge cases. The repair under test was already frozen; see experiment 002.
FOLLOWUP_CASES = {
    "clamp": [((100, -5, 5), 5), ((0, 0, 0), 0)],
    "is_prime": [((0,), False), ((97,), True)],
    "median": [(([2, 4],), 3.0), (([0, 0, -2, 2],), 0.0)],
    "unique": [((["b", "a", "b"],), ["b", "a"]), (([1, 1, 1],), [1])],
    "normalize": [(([0, 0, 0],), [0, 0, 0]), (([2, 2],), [0.5, 0.5])],
    "fibonacci": [((2,), 1), ((10,), 55)],
    "chunks": [(([1, 2, 3], 5), [[1, 2, 3]]), (([], 2), [])],
    "palindrome": [(("Never odd or even",), True), (("aba",), True)],
    "longest": [((["abc", "de"],), "abc"), ((["a", "bb", "ccc"],), "ccc")],
    "factorial": [((6,), 720), ((1,), 1)],
}
