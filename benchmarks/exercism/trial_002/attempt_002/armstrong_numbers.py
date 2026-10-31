"""Chat-authored candidate based on public instructions, prior to reading tests."""


def is_armstrong_number(number):
    if number < 0:
        return False
    digits = str(number)
    return sum(int(digit) ** len(digits) for digit in digits) == number
