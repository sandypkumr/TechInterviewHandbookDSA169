from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        res = 0
        q = deque([(root, 0)])
        while q:
            res = max(res, q[-1][1] - q[0][1] + 1)
            new_q = deque()
            for node, idx in q:
                if node.left:
                    new_q.append((node.left, idx * 2))
                if node.right:
                    new_q.append((node.right, idx * 2 + 1))
            q = new_q
        return res