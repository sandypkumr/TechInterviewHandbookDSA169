class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        for char in s:
            if char == ']':
                substr = ''
                while stack[-1] != '[':
                    substr = stack.pop() + substr
                stack.pop()
                num = ''
                while stack and stack[-1].isdigit():
                    num = stack.pop() + num
                stack.append(int(num) * substr)
            else:
                stack.append(char)
        return ''.join(stack)