from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        return self.merge(lists, 0, len(lists) - 1)

    def merge(self, lists, start, end):
        if start == end:
            return lists[start]
        mid = start + (end - start) // 2
        left = self.merge(lists, start, mid)
        right = self.merge(lists, mid + 1, end)
        return self.merge_two_lists(left, right)

    def merge_two_lists(self, left, right):
        dummy = ListNode()
        current = dummy
        while left and right:
            if left.val < right.val:
                current.next = left
                left = left.next
            else:
                current.next = right
                right = right.next
            current = current.next
        current.next = left or right
        return dummy.next

