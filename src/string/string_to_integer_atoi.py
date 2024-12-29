class Solution:
    def myAtoi(self, s: str) -> int:
        s = s.lstrip()
        if not s:
            return 0
        sign = 1
        if s[0] == '-':
            sign = -1
            s = s[1:]
        elif s[0] == '+':
            s = s[1:]
        num = 0
        for char in s:
            if not char.isdigit():
                break
            num = num * 10 + int(char)
        num = num * sign
        if num < -2 ** 31:
            return -2 ** 31
        if num > 2 ** 31 - 1:
            return 2 ** 31 - 1
        return num