from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        can_start_here = len(nums) - 1
        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= can_start_here:
                can_start_here = i
        return can_start_here == 0