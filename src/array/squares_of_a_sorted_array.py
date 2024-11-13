from typing import List


class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        square_nums = [0] * len(nums)
        left, right = 0, len(nums) - 1
        for i in range(len(nums) - 1, -1, -1):
            if abs(nums[left]) > abs(nums[right]):
                square_nums[i] = nums[left] ** 2
                left += 1
            else:
                square_nums[i] = nums[right] ** 2
                right -= 1
        return square_nums
