"""Chat-authored candidate based on public instructions, prior to reading tests."""


class Luhn:
    def __init__(self, card_num):
        self.card_num = card_num

    def valid(self):
        digits = self.card_num.replace(" ", "")
        if len(digits) < 2 or not digits.isascii() or not digits.isdigit():
            return False
        total = 0
        for position, character in enumerate(reversed(digits)):
            digit = int(character)
            if position % 2:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit
        return total % 10 == 0
