from typing import List


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        rows, cols = len(board), len(board[0])
        trie = {}
        for word in words:
            node = trie
            for char in word:
                node = node.setdefault(char, {})
            node['#'] = word

        def backtrack(row: int, col: int, parent: dict) -> None:
            char = board[row][col]
            node = parent[char]
            word = node.pop('#', False)
            if word:
                found_words.append(word)
            board[row][col] = '#'
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < rows and 0 <= new_col < cols and board[new_row][new_col] in node:
                    backtrack(new_row, new_col, node)
            board[row][col] = char
            if not node:
                parent.pop(char)

        found_words = []
        for i in range(rows):
            for j in range(cols):
                if board[i][j] in trie:
                    backtrack(i, j, trie)
        return found_words