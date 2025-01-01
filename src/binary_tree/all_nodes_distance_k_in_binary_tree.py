from typing import List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> List[int]:
        def dfs(node, parent):
            if not node:
                return
            node.parent = parent
            dfs(node.left, node)
            dfs(node.right, node)

        dfs(root, None)
        cur_arr = [target]
        visited = {target}
        for _ in range(k):
            new_arr = []
            for node in cur_arr:
                for neighbour in node.left, node.right, node.parent:
                    if neighbour and neighbour not in visited:
                        visited.add(neighbour)
                        new_arr.append(neighbour)
            cur_arr = new_arr
        return [x.val for x in cur_arr]