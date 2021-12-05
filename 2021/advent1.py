class Window:
    def __init__(self, size=3):
        self.size = size
        self.items = []

    def isfull(self):
        return len(self.items) == self.size

    def sum(self):
        t = 0
        for n in self.items:
            t += n
        return t

    def push(self, n):
        if self.isfull():
            self.items.pop(0)
        self.items.append(n)

def main(data, part, log):
    data = map(int, data.read().strip().split('\n'))
    if part == 1:
        window = Window(1)
    else:
        window = Window(3)
    count = 0
    for d in data:
        if window.isfull():
            oldsum = window.sum()
            window.push(d)
            newsum = window.sum()
            if newsum > oldsum:
                count += 1
        else:
            window.push(d)
    print('Count', count)