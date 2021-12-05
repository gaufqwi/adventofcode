import re

def main(data, part, log):
    dir_re = re.compile('e|w|se|sw|ne|nw')
    hexgrid = {}
    for line in data:
        x, y = 0, 0
        for dir in dir_re.findall(line):
            if dir == 'w':
                x -= 1
            elif dir == 'e':
                x += 1
            elif dir == 'nw':
                y += 1
            elif dir == 'se':
                y -= 1
            elif dir == 'ne':
                x += 1
                y += 1
            elif dir == 'sw':
                x -= 1
                y -= 1
        coords = f'{x},{y}'
        hexgrid[coords] = hexgrid.setdefault(coords, 1) * -1
    if part == 1:
        count = 0
        for coords, state in hexgrid.items():
            if state == -1:
                count += 1
        print('Part 1 Count', count)
        return
    adj = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, -1)]
    for i in range(100):
        log.info(f'Simulation Day {i+1} Grid Size: {len(hexgrid)}')
        # Make sure all black hexes have neighbors
        frontier = []
        for coords, state in hexgrid.items():
            if state == 1:
                continue
            x, y = [int(c) for c in coords.split(',')]
            for a in adj:
                frontier.append(f'{x+a[0]},{y+a[1]}')
                #hexgrid.setdefault(f'{x+a[0]},{y+a[1]}', 1)
        for f in frontier:
            hexgrid.setdefault(f, 1)
        newhexgrid = {}
        for coords, state in hexgrid.items():
            blackcount = 0
            x, y = [int(c) for c in coords.split(',')]
            for a in adj:
                if hexgrid.get(f'{x+a[0]},{y+a[1]}', 1) == -1:
                    blackcount += 1
            if (state == -1 and (blackcount == 0 or blackcount > 2)):
                newhexgrid[coords] = 1
            elif (state == 1 and blackcount == 2):
                newhexgrid[coords] = -1
            else:
                newhexgrid[coords] = state
        hexgrid = newhexgrid
    count = 0
    for coords, state in hexgrid.items():
        if state == -1:
            count += 1
    print('Part 2 Count', count)
