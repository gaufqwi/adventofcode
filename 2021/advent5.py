def parsedata(data):
    parsed = []
    for line in data:
        p1, p2 = line.split(' -> ')
        a, b = p1.split(',')
        c, d = p2.split(',')
        parsed.append([int(a), int(b), int(c), int(d)])
    return parsed

def main(data, part, log):
    data = parsedata(data)
    grid = {}
    for d in data:
        if d[0] == d[2]:
            s, e = min(d[1], d[3]), max(d[1], d[3])
            for i in range(s, e+1):
                coords = f'{d[0]},{i}'
                grid[coords] = grid.setdefault(coords, 0) + 1
        elif d[1] == d[3]:
            s, e = min(d[0], d[2]), max(d[0], d[2])
            for i in range(s, e+1):
                coords = f'{i},{d[1]}'
                grid[coords] = grid.setdefault(coords, 0) + 1
        elif part == 2:
            xs, xe = min(d[0], d[2]), max(d[0], d[2])
            if xs == d[0]:
                ys = d[1]
                ye = d[3]
            else:
                ys = d[3]
                ye = d[1]
            if ye > ys:
                slope = 1
            else:
                slope = -1
            for i in range(xs, xe+1):
                coords = f'{i},{ys + slope*(i-xs)}'
                grid[coords] = grid.setdefault(coords, 0) + 1
    count = 0
    for k, v in grid.items():
        if v >=2:
            count += 1
    print(f'Count for part {part}: {count}')