from typing import List


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        for row in range(9):
            for col in range(9):
                if board[row][col] == '.':
                    continue
                box = (row // 3) * 3 + col // 3
                if board[row][col] in rows[row] or board[row][col] in cols[col] or board[row][col] in boxes[box]:
                    return False
                rows[row].add(board[row][col])
                cols[col].add(board[row][col])
                boxes[box].add(board[row][col])
        return True