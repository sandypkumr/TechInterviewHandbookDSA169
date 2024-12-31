from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        def dfs(node, cur_sum):
            if not node:
                return
            nonlocal ans
            cur_sum += node.val
            old_sum = cur_sum - targetSum
            ans += sum_map.get(old_sum, 0)
            sum_map[cur_sum] = sum_map.get(cur_sum, 0) + 1
            dfs(node.left, cur_sum)
            dfs(node.right, cur_sum)
            sum_map[cur_sum] -= 1

        if not root:
            return 0
        ans = 0
        sum_map = {0: 1}
        dfs(root, 0)
        return ans