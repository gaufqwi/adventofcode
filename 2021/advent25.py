from aocpython.problem import AOCProblem

class Problem(AOCProblem):
    def common(self):
        self.east_herd = set()
        self.south_herd = set()
        self.data = [line.strip() for line in self.data]
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        for r, line in enumerate(self.data):
            for c, content in enumerate(line):
                if content == '>':
                    self.east_herd.add((r, c))
                elif content == 'v':
                    self.south_herd.add((r, c))

    def step(self):
        changed = False
        new_east_herd = set()
        for r, c in self.east_herd:
            nc = (c + 1) % self.cols
            if (r, nc) in self.east_herd or (r, nc) in self.south_herd:
                new_east_herd.add((r, c))
            else:
                new_east_herd.add((r, nc))
                changed = True
        self.east_herd = new_east_herd
        new_south_herd = set()
        for r, c in self.south_herd:
            nr = (r + 1) % self.rows
            if (nr, c) in self.east_herd or (nr, c) in self.south_herd:
                new_south_herd.add((r, c))
            else:
                new_south_herd.add((nr, c))
                changed = True
        self.south_herd = new_south_herd
        return changed

    def part1(self):
        step_no = 1
        while self.step():
            step_no += 1
        print(f'No change on step {step_no}')
