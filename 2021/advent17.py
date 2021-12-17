from aocpython.problem import AOCProblem
from math import floor, sqrt

class CantReach(BaseException):
    pass

class Problem(AOCProblem):
    def common(self):
        pairs = self.data.read().strip().split()[2:]
        xpair = pairs[0][2:-1]
        ypair = pairs[1][2:]
        self.xlimits = [int(x) for x in xpair.split('..')]
        self.ylimits = [int(y) for y in ypair.split('..')]

    def simulate(self, vx, vy):
        x, y, maxy = 0, 0, 0
        while True:
            x += vx
            y += vy
            maxy = max(y, maxy)
            vx = max(0, vx - 1)
            vy -= 1
            if x >= self.xlimits[0] and x <= self.xlimits[1] and y >= self.ylimits[0] and y <= self.ylimits[1]:
                return maxy
            elif y < self.ylimits[0] or x > self.xlimits[1]:
                raise CantReach()


    def part1(self):
        minvx = floor((sqrt(8*self.xlimits[0])-1)/2)
        maxy = 0
        for vx in range(minvx, self.xlimits[1]+1):
            for vy in range(200):  # Just a guess
                try:
                    y = self.simulate(vx, vy)
                    maxy = max(y, maxy)
                except CantReach:
                    pass
        print(f'Max height is {maxy}')

    def part2(self):
        minvx = floor((sqrt(8*self.xlimits[0])-1)/2)
        count = 0
        for vx in range(minvx, self.xlimits[1]+1):
            for vy in range(-100,100):  # Just a guess
                try:
                    y = self.simulate(vx, vy)
                    count += 1
                except CantReach:
                    pass
        print(f'There are {count} pairs that work')
