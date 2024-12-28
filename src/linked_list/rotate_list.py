from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        length = 1
        current = head
        while current.next:
            current = current.next
            length += 1
        current.next = head
        k %= length
        for _ in range(length - k):
            current = current.next
        head = current.next
        current.next = None
        return head
