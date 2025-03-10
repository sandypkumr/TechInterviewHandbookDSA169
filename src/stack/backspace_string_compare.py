class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        def build(s: str) -> str:
            stack = []
            for c in s:
                if c == '#':
                    if stack:
                        stack.pop()
                else:
                    stack.append(c)
            return ''.join(stack)
        return build(s) == build(t)