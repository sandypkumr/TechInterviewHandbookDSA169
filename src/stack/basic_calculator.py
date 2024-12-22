class Solution:
    def calculate(self, s: str) -> int:
        num_stack, sign_stack = [], []
        res, num, sign = 0, 0, '+'

        for i, c in enumerate(s):
            if c.isdigit():
                num = num * 10 + int(c)
            if c in '+-' or i == len(s) - 1:
                res = res + num if sign == '+' else res - num
                num, sign = 0, c
            if c == '(':
                num_stack.append(res)
                sign_stack.append(sign)
                res, num, sign = 0, 0, '+'
            if c == ')':
                res = res + num if sign == '+' else res - num
                prv_res = num_stack.pop()
                res = prv_res + res if sign_stack.pop() == '+' else prv_res - res
                num = 0
        return res