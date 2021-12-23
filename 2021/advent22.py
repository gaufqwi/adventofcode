from aocpython.problem import AOCProblem

class Problem(AOCProblem):
    def common(self):
        self.instructions = []
        for line in self.data:
            state, rest = line.split()
            instruction = [state]
            for pair in rest.split(','):
                instruction += [int(n) for n in pair[2:].split('..')]
            self.instructions.append(tuple(instruction))

    def part1(self):
        # Naive implementation
        grid = set()
        for state, xmin, xmax, ymin, ymax, zmin, zmax in self.instructions:
            # Sloppy test but applies to this data
            if xmin > 50 or xmin < - 50:
                continue
            for x in range(xmin, xmax+1):
                for y in range(ymin, ymax+1):
                    for z in range(zmin,zmax+1):
                        if state == 'on':
                            grid.add((x, y, z))
                        else:
                            try:
                                grid.remove((x, y, z))
                            except KeyError:
                                pass
        print(f'There are {len(grid)} cubes one')

    def part2(self):
        for i in range(len(self.instructions)):
            self.instructions[i] = self.instructions[i] + (i,)
        xlayers = []
        by_start = self.instructions[:]
        by_start.sort(key=lambda x: x[1])
        by_end=self.instructions[:]
        by_end.sort(key=lambda x: x[2])
        while len(by_end) > 0:
            if len(by_start) == 0:
                ins = by_end.pop(0)
                xlayers.append((ins[2]+1, 'e', ins[0], ins[3], ins[4], ins[5], ins[6], ins[7]))
            elif by_start[0][1] < by_end[0][2]:
                ins = by_start.pop(0)
                xlayers.append((ins[1], 's', ins[0], ins[3], ins[4], ins[5], ins[6], ins[7]))
            else:
                ins = by_end.pop(0)
                xlayers.append((ins[2]+1, 'e', ins[0], ins[3], ins[4], ins[5], ins[6], ins[7]))
        lastx = xlayers[0][0]
        active_layers = [xlayers[0][2:]]
        volume = 0
        for layer in xlayers[1:]:
            newx = layer[0]
            thickness = newx - lastx
            lastx = newx
            area = self.calc_area(active_layers)
            volume += thickness * area
            if layer[1] == 's':
                active_layers.append(layer[2:])
            else:
                active_layers.remove(layer[2:])
        print(f'{volume} cubes are on')

    def calc_area(self, layers):
        yrows = []
        by_start = layers[:]
        by_start.sort(key=lambda x: x[1])
        by_end = layers[:]
        by_end.sort(key=lambda x: x[2])
        while len(by_end) > 0:
            if len(by_start) == 0:
                ins = by_end.pop(0)
                yrows.append((ins[2]+1, 'e', ins[0], ins[3], ins[4], ins[5]))
            elif by_start[0][1] < by_end[0][2]:
                ins = by_start.pop(0)
                yrows.append((ins[1], 's', ins[0], ins[3], ins[4], ins[5]))
            else:
                ins = by_end.pop(0)
                yrows.append((ins[2]+1, 'e', ins[0], ins[3], ins[4], ins[5]))
        lasty = yrows[0][0]
        active_rows = [yrows[0][2:]]
        area = 0
        for row in yrows[1:]:
            newy = row[0]
            height = newy - lasty
            lasty = newy
            length = self.calc_length(active_rows)
            area += height * length
            if row[1] == 's':
                active_rows.append(row[2:])
            else:
                active_rows.remove(row[2:])
        return area

    # SLLLOOOWWW brute force
    def calc_length(self, segments):
        segments.sort(key=lambda x: x[3])
        points = set()
        for seg in segments:
            for i in range(seg[1], seg[2]+1):
                if seg[0] == 'on':
                    points.add(i)
                else:
                    try:
                        points.remove(i)
                    except KeyError:
                        pass
        return len(points)