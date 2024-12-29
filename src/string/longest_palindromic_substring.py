class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n == 0:
            return ""
        start = 0
        end = 0
        for i in range(n):
            len1 = self.expandAroundCenter(s, i, i)
            len2 = self.expandAroundCenter(s, i, i + 1)
            length = max(len1, len2)
            if length > end - start:
                start = i - (length - 1) // 2
                end = i + length // 2
        return s[start:end + 1]

    def expandAroundCenter(self, s: str, i1: int, i2: int) -> int:
        while i1 >= 0 and i2 < len(s) and s[i1] == s[i2]:
            i1 -= 1
            i2 += 1
        return i2 - i1 - 1