neighbors = [(0,1), (0, -1), (1, 0), (-1, 0)]

def main(data, part, log):
    grid = []
    for line in data:
        grid.append([int(x) for x in list(line.strip())])
    height = len(grid)
    width = len(grid[0])
    total = 0
    basin_sizes = []
    for i in range(height):
        for j in range(width):
            v = grid[i][j]
            lowest = True
            for n in neighbors:
                ni, nj = n
                ni += i
                nj += j
                if ni < 0 or ni >= height or nj < 0 or nj >= width:
                    continue
                if grid[ni][nj] <= v:
                    lowest = False
                    break
            if lowest:
                total += v + 1
                if part == 2:
                    basin_sizes.append(find_basin(grid, height, width, i, j))
    if part == 1:
        print(f'Total of low spots is {total}')
    if part == 2:
        basin_sizes.sort()
        p = 1
        for f in basin_sizes[-3:]:
            p *= f
        print(f'Product of largest basic sizes is {p}')

def find_basin(grid, h, w, i, j):
    size = 0
    visited = {}
    tovisit = [(i, j)]
    visited[f'{i},{j}'] = True
    while len(tovisit):
        ci, cj = tovisit.pop(0)
        size += 1
        for ni, nj in neighbors:
            ni += ci
            nj += cj
            if ni < 0 or ni >= h or nj < 0 or nj >= w:
                continue
            if grid[ni][nj] < 9 and f'{ni},{nj}' not in visited:
                visited[f'{ni},{nj}'] = True
                tovisit.append((ni, nj))
    return size
