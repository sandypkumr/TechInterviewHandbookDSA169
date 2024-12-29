from typing import List


class Solution:
    def palindromePairs(self, words: List[str]) -> List[List[int]]:
        def is_palindrome(s : str) -> bool:
            return s == s[::-1]

        word_to_index = {word: i for i, word in enumerate(words)}
        result = []
        for i, word in enumerate(words):
            for j in range(len(word) + 1):
                prefix, suffix = word[:j], word[j:]
                if is_palindrome(prefix):
                    reversed_suffix = suffix[::-1]
                    if reversed_suffix in word_to_index and word_to_index[reversed_suffix] != i:
                        result.append([word_to_index[reversed_suffix], i])
                if j != len(word) and is_palindrome(suffix):
                    reversed_prefix = prefix[::-1]
                    if reversed_prefix in word_to_index and word_to_index[reversed_prefix] != i:
                        result.append([i, word_to_index[reversed_prefix]])
        return result