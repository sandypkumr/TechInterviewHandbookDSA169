"""

There is a new alien language which uses the latin alphabet. However, the order among letters are unknown to you. You
receive a list of non-empty words from the dictionary, where words are sorted lexicographically by the rules of this
new language. Derive the order of letters in this language.

For example, given the following words:

    [
    "wrt",
    "wrf",
    "er",
    "ett",
    "rftt"
    ]

The correct order is: "wertf".

Note:
1. You may assume all letters are in lowercase.
2. If the order is invalid, return an empty string.
3. There may be multiple valid order of letters, return any one of them is fine.

"""
from collections import defaultdict
from typing import List

class Solution:
    def alienOrder(self, words: list[str]) -> str:
        graph = defaultdict(set)
        in_degree = {char: 0 for word in words for char in word}
        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]
            if len(word1) > len(word2) and word1.startswith(word2):
                return ''
            if len(word1) < len(word2) and word2.startswith(word1):
                continue
            for c1, c2 in zip(word1, word2):
                if c1 != c2:
                    if c2 not in graph[c1]:
                        graph[c1].add(c2)
                        in_degree[c2] += 1
                    break

        queue = [char for char in in_degree if in_degree[char] == 0]
        result = []
        while queue:
            char = queue.pop(0)
            result.append(char)
            for next_char in graph[char]:
                in_degree[next_char] -= 1
                if in_degree[next_char] == 0:
                    queue.append(next_char)

        return ''.join(result) if len(result) == len(in_degree) else ''