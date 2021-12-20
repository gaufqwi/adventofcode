from aocpython.problem import AOCProblem

neighbors = [(-1,-1,256),(0,-1,128),(1,-1,64),(-1,0,32),(0,0,16),(1,0,8),(-1,1,4),(0,1,2),(1,1,1)]

class Problem(AOCProblem):
    def common(self):
        self.rest = '.'
        self.lit = set()
        self.algorithm = self.data.readline().strip()
        self.data.readline()
        y = 0
        for line in self.data:
            x = 0
            for pixel in line.strip():
                if pixel == '#':
                    self.lit.add((x,y))
                x += 1
            y += 1
        self.find_bounds()

    def show(self):
        for y in range(self.uly, self.lry + 1):
            line = ''
            for x in range(self.ulx, self.lrx + 1):
                if (x,y) in self.lit:
                    line = line + '#'
                else:
                    line = line + '.'
            print(line)
        print(f'Bounds: ({self.ulx}, {self.uly}) ({self.lrx}, {self.lry}) Rest: {self.rest}')

    def enhance(self):
        newlit = set()
        for x in range(self.ulx-1, self.lry+2):
            for y in range(self.uly-1, self.lry+2):
                index = 0
                for dx, dy, bitval in neighbors:
                    nx, ny = x + dx, y + dy
                    if (nx < self.ulx or nx > self.lry or ny < self.uly or ny > self.lry) and self.rest == '#':
                        index += bitval
                    elif (nx,ny) in self.lit:
                        index += bitval
                if self.algorithm[index] == '#':
                    newlit.add((x,y))
        self.lit = newlit
        self.find_bounds()
        if self.rest == '.':
            self.rest = self.algorithm[0]
        else:
            self.rest = self.algorithm[511]

    def find_bounds(self):
        self.ulx, self.uly, self.lrx, self.lry = 0, 0, 0, 0
        for pixel in self.lit:
            self.ulx = min(self.ulx, pixel[0])
            self.uly = min(self.uly, pixel[1])
            self.lrx = max(self.lrx, pixel[0])
            self.lry = max(self.lry, pixel[1])

    def part1(self):
        iterations = 2
        for i in range(iterations):
            self.enhance()
        print(f'After {iterations} iterations there are {len(self.lit)} lit pixels')

    def part2(self):
        iterations = 50
        for i in range(iterations):
            self.enhance()
        print(f'After {iterations} iterations there are {len(self.lit)} lit pixels')