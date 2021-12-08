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
        # realmean = sum(data) / len(data)
        # i = 0
        # while data[i] < realmean:
        #     i += 1
        # print(f'{i} numbers below mean of {realmean}, {len(data) - i} higher')