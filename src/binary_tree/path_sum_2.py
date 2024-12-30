from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        def dfs(node, path, target):
            if not node:
                return
            if not node.left and not node.right and node.val == target:
                res.append(path + [node.val])
                return
            dfs(node.left, path + [node.val], target - node.val)
            dfs(node.right, path + [node.val], target - node.val)
        res = []
        dfs(root, [], targetSum)
        return res