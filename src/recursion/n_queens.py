from typing import List


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        def backtrack(row, cols, diags, anti_diags, board):
            if row == n:
                result.append(["".join(row) for row in board])
                return
            for col in range(n):
                diag = row - col
                anti_diag = row + col
                if col in cols or diag in diags or anti_diag in anti_diags:
                    continue
                board[row][col] = "Q"
                cols.add(col)
                diags.add(diag)
                anti_diags.add(anti_diag)
                backtrack(row + 1, cols, diags, anti_diags, board)
                board[row][col] = "."
                cols.remove(col)
                diags.remove(diag)
                anti_diags.remove(anti_diag)
        if n == 1:
            return [["Q"]]
        if n < 4:
            return []
        result = []
        board = [["." for _ in range(n)] for _ in range(n)]
        backtrack(0, set(), set(), set(), board)
        return result