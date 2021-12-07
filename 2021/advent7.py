def main(data, part, log):
    data = [int(x) for x in data.read().strip().split(',')]
    data.sort()
    if part == 1:
        median = data[len(data) // 2]
        cost = 0
        for d in data:
            cost += abs(median - d)
        print(f'Cost is {cost}')
    else:
        mean = sum(data) // len(data)
        cost = 0
        for d in data:
            diff = abs(d - mean)
            cost += diff * (diff + 1) // 2
        print(f'Cost is {cost}')