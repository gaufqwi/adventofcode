from aocpython.problem import AOCProblem

def axis_transform(i, c):
    dir, turn = i // 8, i % 8
    sign, turn = -2*(turn // 4) + 1, turn % 4
    x, y, z = sign*c[dir], c[(dir+1)%3], sign*c[(dir+2)%3]
    for j in range(turn):
        y, z = z, -y
    return (x, y, z)

class Scanner:
    def __init__(self, number, beacons):
        self.number = number
        self.beacons = beacons
        self.coords = (0, 0, 0)

    def gen_orientations(self):
        self.orientations = []
        for i in range(24):
            orientation = []
            for b in self.beacons:
                orientation.append(axis_transform(i, b))
            self.orientations.append(orientation)

    def set_canonical_coords(self, orientation, x, y, z):
        self.beacons = []
        self.coords = (x, y, z)
        for b in self.orientations[orientation]:
            self.beacons.append((b[0]+x, b[1]+y, b[2]+z))

    def __repr__(self):
        return f'<{self.number}>: {self.beacons[:4]}... ({len(self.beacons)}'

class Problem(AOCProblem):
    def common(self):
        blocks = self.data.read().strip().split('\n\n')
        self.scanners = []
        for i, block in enumerate(blocks):
            lines = block.split('\n')
            self.scanners.append(Scanner(i, [eval(x) for x in lines[1:]]))
        for s in self.scanners[1:]:
            s.gen_orientations()
        newly_known = set([self.scanners[0]])
        unknown = set(self.scanners[1:])
        self.log.debug(f'Initialized at {self.elapsed()}')
        while len(unknown) > 0:
            #self.log.debug(f'{len(unknown)} at {self.elapsed()}')
            known = newly_known
            newly_known = set()
            for known_scanner in known:
                for unknown_scanner in unknown:
                    self.log.debug(f'Comparing known {known_scanner.number} to {unknown_scanner.number} at {self.elapsed()}')
                    for o in range(24):
                        difference_counts = {}
                        for k_beacon in known_scanner.beacons:
                            for u_beacon in unknown_scanner.orientations[o]:
                                diff = (k_beacon[0] - u_beacon[0], k_beacon[1] - u_beacon[1], k_beacon[2] - u_beacon[2])
                                difference_counts[diff] = difference_counts.get(diff, 0) + 1
                        sorted_count = [(count, diff) for diff, count in difference_counts.items()]
                        sorted_count.sort()
                        if sorted_count[-1][0] >= 12:
                            self.log.debug(f'Found match {known_scanner.number}={unknown_scanner.number} at {self.elapsed()}')
                            offset = sorted_count[-1][1]
                            unknown_scanner.set_canonical_coords(o, offset[0], offset[1], offset[2])
                            newly_known.add(unknown_scanner)
                            break
                unknown = unknown - newly_known

    def part1(self):
        beacons = set()
        for scanner in self.scanners:
            for beacon in scanner.beacons:
                beacons.add(beacon)
        print(f'There are {len(beacons)} beacons')

    def part2(self):
        l = len(self.scanners)
        greatest = 0
        for i in range(l):
            for j in range(i+1, l):
                d = abs(self.scanners[i].coords[0] - self.scanners[j].coords[0])
                d += abs(self.scanners[i].coords[1] - self.scanners[j].coords[1])
                d += abs(self.scanners[i].coords[2] - self.scanners[j].coords[2])
                greatest = max(greatest, d)
        print(f'Greatest Manhattan distance is {greatest}')
