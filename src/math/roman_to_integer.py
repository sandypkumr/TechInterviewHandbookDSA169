class Solution:
    def romanToInt(self, s: str) -> int:
        roman_to_int = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }
        result = 0
        prev = 0
        for c in s:
            curr = roman_to_int[c]
            result += curr
            if curr > prev:
                result -= 2 * prev
            prev = curr
        return result