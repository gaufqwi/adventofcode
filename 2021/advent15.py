from aocpython.problem import AOCProblem
from numpy import array, zeros
from heapq import heappop, heappush

neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class Problem(AOCProblem):
    def common(self):
        source = []
        for line in self.data:
            row = [int(x) for x in line.strip()]
            source.append(row)
        self.size = len(source)
        self.map = array(source)

    def part1(self):
        frontier = []
        heappush(frontier, (0,0,0))
        dest = False
        visited = set()
        while not dest:
            #frontier.sort()
            #first = frontier.pop(0)
            first = heappop(frontier)
            for dx, dy in neighbors:
                nx = first[1] + dx
                ny = first[2] + dy
                if nx < 0 or ny < 0 or nx >= self.size or ny >= self.size or (nx,ny) in visited:
                    continue
                #frontier.append((first[0] + self.map[ny,nx], nx, ny))
                if nx == self.size-1 and ny == self.size-1:
                   print(f'Safest path has {first[0] + self.map[ny,nx]} risk')
                   return
                else:
                    heappush(frontier, (first[0] + self.map[ny,nx], nx, ny))
                visited.add((nx,ny))
            dest = self.check_frontier(frontier)
        print(f'Safest path has {dest[0]} risk')

    # Not very efficient; can be improved
    def oldpart1(self):
        frontier = [(0, 0, 0)]
        dest = False
        visited = set()
        while not dest:
            frontier.sort()
            first = frontier.pop(0)
            for dx, dy in neighbors:
                nx = first[1] + dx
                ny = first[2] + dy
                if nx < 0 or ny < 0 or nx >= self.size or ny >= self.size or (nx,ny) in visited:
                    continue
                frontier.append((first[0] + self.map[ny,nx], nx, ny))
                visited.add((nx,ny))
            dest = self.check_frontier(frontier)
        print(f'Safest path has {dest[0]} risk')

    def part2(self):
        newmap = zeros(shape=(self.size*5, self.size*5))
        for i in range(5):
            for j in range(5):
                for r in range(self.size):
                    for c in range(self.size):
                        v = ((self.map[r][c] + i + j - 1) % 9) + 1
                        newmap[self.size*i + r, self.size*j + c] = v
        self.map = newmap
        self.size *= 5
        self.part1()

    def check_frontier(self, frontier):
        for f in frontier:
            if f[1] == self.size-1 and f[2]==self.size-1:
                return f
        return False