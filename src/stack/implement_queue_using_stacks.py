class MyQueue:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.stack = []
        self.queue = []

    def push(self, x: int) -> None:
        """
        Push element x to the back of queue.
        """
        self.stack.append(x)

    def pop(self) -> int:
        """
        Removes the element from in front of queue and returns that element.
        """
        if not self.queue:
            while self.stack:
                self.queue.append(self.stack.pop())
        return self.queue.pop()

    def peek(self) -> int:
        """
        Get the front element.
        """
        if not self.queue:
            while self.stack:
                self.queue.append(self.stack.pop())
        return self.queue[-1]

    def empty(self) -> bool:
        """
        Returns whether the queue is empty.
        """
        return not self.stack and not self.queue