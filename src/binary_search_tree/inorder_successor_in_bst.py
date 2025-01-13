"""

Problem Statement:
    Given the root of a binary search tree and a node p in it, return the in-order successor of that node in the BST.
    If the given node has no in-order successor in the tree, return null.

    The successor of a node p is the node with the smallest key greater than p.val.

    Example 1:

    Input: root = [2,1,3], p = 1
    Output: 2

    Example 2:

    Input: root = [5,3,6,2,4,null,null,1], p = 6
    Output: null

    Constraints:

    The number of nodes in the tree is in the range [1, 104].
    -105 <= Node.val <= 105
    All Nodes will have unique values.

"""
from typing import Optional


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def inorderSuccessor(self, root: Optional['TreeNode'], p: Optional['TreeNode']) -> Optional['TreeNode']:
        ans = None
        while root:
            if root.val > p.val:
                ans = root
                root = root.left
            else:
                root = root.right
        return ans