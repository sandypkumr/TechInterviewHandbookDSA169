from typing import List


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ''
        for i, chars in enumerate(zip(*strs)):
            if len(set(chars)) > 1:
                return strs[0][:i]
        return min(strs)