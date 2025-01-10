import string
from collections import deque
from typing import List


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        if endWord not in word_set:
            return 0
        queue = deque([(beginWord, 1)])
        while queue:
            word, steps = queue.popleft()
            if word == endWord:
                return steps
            for i in range(len(word)):
                for c in string.ascii_lowercase:
                    next_word = word[:i] + c + word[i + 1:]
                    if next_word in word_set:
                        word_set.remove(next_word)
                        queue.append((next_word, steps + 1))
        return 0