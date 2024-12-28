from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        if not head or not head.next:
            return
        slow = head
        fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        mid = slow.next
        slow.next = None
        mid = self.reverse(mid)
        self.merge(head, mid)

    def reverse(self, node: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        while node:
            next_node = node.next
            node.next = prev
            prev = node
            node = next_node
        return prev

    def merge(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> None:
        while list1 and list2:
            next1 = list1.next
            next2 = list2.next
            list1.next = list2
            list1 = next1
            list2.next = list1
            list2 = next2
