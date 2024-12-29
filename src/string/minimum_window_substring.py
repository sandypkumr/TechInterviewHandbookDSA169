from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        t_count = Counter(t)
        required = len(t_count)
        window = {}
        formed = 0
        left = 0
        right = 0
        ans = (float('inf'), 0, 0)
        while right < len(s):
            char = s[right]
            window[char] = window.get(char, 0) + 1
            if char in t_count and window[char] == t_count[char]:
                formed += 1
            while formed == required:
                if right - left + 1 < ans[0]:
                    ans = (right - left + 1, left, right + 1)
                char = s[left]
                window[char] -= 1
                if char in t_count and window[char] < t_count[char]:
                    formed -= 1
                left += 1
            right += 1
        return s[ans[1]:ans[2]] if ans[0] != float('inf') else ''