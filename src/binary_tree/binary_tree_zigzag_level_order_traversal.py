from collections import deque
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        res = []
        q = deque([root])
        level = 0
        while q:
            level += 1
            new_q = deque()
            level_res = []
            for node in q:
                level_res.append(node.val)
                if node.left:
                    new_q.append(node.left)
                if node.right:
                    new_q.append(node.right)
            if level % 2 == 0:
                level_res = level_res[::-1]
            res.append(level_res)
            q = new_q
        return res