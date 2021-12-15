from aocpython.problem import AOCProblem

class Problem(AOCProblem):
    def common(self):
        self.data = [int(x) for x in self.data.read().strip().split('\n')]

    def part1(self):
        for i in range(len(self.data)):
            for j in range(i+1, len(self.data)):
                if self.data[i] + self.data[j] == 2020:
                    print(f'Product is {self.data[i]*self.data[j]}')
                    return
    def part2(self):
        for i in range(len(self.data)):
            for j in range(i+1, len(self.data)):
                for k in range(j+1, len(self.data)):
                    if self.data[i] + self.data[j] + self.data[k] == 2020:
                        print(f'Product is {self.data[i]*self.data[j]*self.data[k]}')
                        return