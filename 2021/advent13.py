def main(data, part, log):
    points = set()
    for line in data:
        line = line.strip()
        if line == '':
            break
        points.add(eval(line))
    folds = []
    for line in data:
        _, _, eq = line.strip().split()
        folds.append(eq.split('='))
    if part == 1:
        points = do_fold(points, folds[0][0], int(folds[0][1]))
        print(f'{len(points)} are visible')
    else:
        for fold in folds:
            points = do_fold(points, fold[0], int(fold[1]))
        mx, my = 0, 0
        for p in points:
            mx, my = max(mx,p[0]), max(my,p[1])
        for y in range(my+1):
            line = ''
            for x in range(mx+1):
                if (x,y) in points:
                    line = line + '#'
                else:
                    line = line + ' '
            print(line)

def do_fold(points, axis, pos):
    newpoints = set()
    for p in points:
        if axis == 'x':
            if p[0] < pos:
                newpoints.add(p)
            else:
                newpoints.add((2*pos - p[0], p[1]))
        else:
            if p[1] < pos:
                newpoints.add(p)
            else:
                newpoints.add((p[0], 2*pos - p[1]))
    return newpoints




