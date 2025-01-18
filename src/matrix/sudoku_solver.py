from typing import List


class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = {(i, j): set() for i in range(3) for j in range(3)}

        for row in range(9):
            for col in range(9):
                if board[row][col] == '.':
                    continue
                box = (row // 3, col // 3)
                rows[row].add(board[row][col])
                cols[col].add(board[row][col])
                boxes[box].add(board[row][col])

        self.solve(board, 0, 0, rows, cols, boxes)

    def solve(self, board, row, col, rows, cols, boxes):
        if row == 9:
            return True
        if col == 9:
            return self.solve(board, row + 1, 0, rows, cols, boxes)
        if board[row][col] != '.':
            return self.solve(board, row, col + 1, rows, cols, boxes)
        box = (row // 3, col // 3)
        for num in '123456789':
            if num in rows[row] or num in cols[col] or num in boxes[box]:
                continue
            board[row][col] = num
            rows[row].add(num)
            cols[col].add(num)
            boxes[box].add(num)
            if self.solve(board, row, col + 1, rows, cols, boxes):
                return True
            board[row][col] = '.'
            rows[row].remove(num)
            cols[col].remove(num)
            boxes[box].remove(num)
        return False