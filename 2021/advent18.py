from aocpython.problem import AOCProblem
import re
from math import floor, ceil

num_re = re.compile('\d+')

class Problem(AOCProblem):
    def common(self):
        temp = []
        for line in self.data:
            temp.append(line.strip().replace(' ', ''))
        self.data = temp

    def reduce(self, sfsum):
        needs_reducing = True
        while needs_reducing:
            (newsfsum, needs_reducing) = self.reduce_explode(sfsum)
            if needs_reducing:
                sfsum = newsfsum
                continue
            else:
                (newsfsum, needs_reducing) = self.reduce_split(sfsum)
                if needs_reducing:
                    sfsum = newsfsum
        return sfsum

    def reduce_explode(self, sfsum):
        reduced = False
        newsfsum = None
        i = 0
        depth = 0
        while i < len(sfsum) and not reduced:
            if sfsum[i] == '[':
                depth += 1
            elif sfsum[i] == ']':
                depth -= 1
            if depth == 5:
                reduced = True
                pairend = i + 1
                while sfsum[pairend] != ']':
                    pairend += 1
                left, right = eval(sfsum[i:pairend+1])
                leftside = sfsum[:i]
                rightside = sfsum[pairend+1:]
                matches = list(num_re.finditer(leftside))
                if len(matches):
                    m = matches[-1]
                    newval = str(left + int(m.group()))
                    leftside = leftside[:m.start()] + newval + leftside[m.end():]
                matches = list(num_re.finditer(rightside))
                if len(matches):
                    m = matches[0]
                    newval = str(right + int(m.group()))
                    rightside = rightside[:m.start()] + newval + rightside[m.end():]
                newsfsum = leftside + '0' + rightside
            i += 1
        return (newsfsum, reduced)

    def reduce_split(self, sfsum):
        reduced = False
        newsfsum = None
        for m in num_re.finditer(sfsum):
            val = int(m.group())
            if val >= 10:
                reduced = True
                leftside = sfsum[:m.start()]
                rightside = sfsum[m.end():]
                pair = f'[{floor(val/2)},{ceil(val/2)}]'
                newsfsum = leftside + pair + rightside
                break
        return (newsfsum, reduced)

    def magnitude(self, sfnum):
        if type(sfnum) == int:
            return sfnum
        else:
            return 3*self.magnitude(sfnum[0]) + 2*self.magnitude(sfnum[1])

    def part1(self):
        sfsum = self.data[0]
        for num in self.data[1:]:
            sfsum = f'[{sfsum},{num}]'
            sfsum = self.reduce(sfsum)
        print(f'Magnitude is {self.magnitude(eval(sfsum))}')

    def part2(self):
        biggest = 0
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if i == j:
                    continue
                sfnum = self.reduce(f'[{self.data[i]},{self.data[j]}]')
                biggest = max(biggest, self.magnitude(eval(sfnum)))
        print(f'Max magnitude of any sum is {biggest}')