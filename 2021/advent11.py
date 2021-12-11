def main(data, part, log):
    grid = []
    for line in data:
        grid.append([int(x) for x in list(line.strip())])
    flashes = 0
    step = 0
    done = False
    while (part == 1 and step < 100) or (part == 2 and not done):
        step += 1
        has_flashed = set()
        to_be_flashed = set()
        for r in range(10):
            for c in range(10):
                grid[r][c] += 1
                if grid[r][c] > 9:
                    to_be_flashed.add((r,c))
        while len(to_be_flashed) > 0:
            r, c = to_be_flashed.pop()
            for dr, dc in neighbors:
                nr = dr + r
                nc = dc + c
                if nr < 0 or nr > 9 or nc < 0 or nc > 9:
                    continue
                if (nr,nc) not in has_flashed:
                    grid[nr][nc] += 1
                    if grid[nr][nc] > 9:
                        to_be_flashed.add((nr,nc))
            has_flashed.add((r,c))
            grid[r][c] = 0
        if part == 1:
            flashes += len(has_flashed)
        elif len(has_flashed) == 100:
            done = True
    if part == 1:
        print(f'{flashes} total flashes')
    else:
        print(f'All flash on step {step}')

neighbors = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]