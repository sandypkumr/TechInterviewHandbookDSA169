class FreqStack:

    def __init__(self):
        self.freq = {}
        self.group = {}
        self.max_freq = 0

    def push(self, val: int) -> None:
        freq = self.freq.get(val, 0) + 1
        self.freq[val] = freq
        if freq > self.max_freq:
            self.max_freq = freq
        if freq not in self.group:
            self.group[freq] = []
        self.group[freq].append(val)

    def pop(self) -> int:
        val = self.group[self.max_freq].pop()
        self.freq[val] -= 1
        if not self.group[self.max_freq]:
            self.max_freq -= 1
        return val

# Your FreqStack object will be instantiated and called as such:
# obj = FreqStack()
# obj.push(val)
# param_2 = obj.pop()