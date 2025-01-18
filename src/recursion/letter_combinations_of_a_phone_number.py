from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        def backtrack(start, path):
            if start == len(digits):
                res.append(path)
                return
            for c in phone[digits[start]]:
                backtrack(start + 1, path + c)

        if not digits:
            return []
        phone = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}
        res = []
        backtrack(0, '')
        return res