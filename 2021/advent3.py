def parsedata(data):
    parsed = []
    for line in data:
        item = line.strip()
        parsed.append(item)
    return parsed

def main(data, part, log):
    if part == 1:
        part1(parsedata(data))
    else:
        part2(parsedata(data))

def part1(data):
    halflen = len(data) // 2
    bitcounts = [0] * 12
    for n in data:
        for i in range(12):
            if n[i] == '1':
                bitcounts[i] += 1
    gamma = 0  # most common
    epsilon = 0  # least common
    for i in range(12):
        power = 2 ** (11 - i)
        if bitcounts[i] > halflen:
            gamma += power
        else:
            epsilon += power
    print('Gamma', gamma, 'Epsilon', epsilon, 'Product', gamma * epsilon)


def part2(data):
    ox = filterdata_ox(data, 0)
    co = filterdata_co(data, 0)
    print('Ox Gen', ox, 'Co scrub', co, 'Product', ox * co)

def filterdata_ox(data, pos):
    onecount = 0
    for n in data:
        if n[pos] == '1':
            onecount += 1
    zerocount = len(data) - onecount
    ox = []
    for n in data:
        if (onecount >= zerocount and n[pos] == '1') or (onecount < zerocount and n[pos] == '0'):
            ox.append(n)
    if len(ox) == 1:
        return int(ox[0], 2)
    else:
        return filterdata_ox(ox, pos + 1)


def filterdata_co(data, pos):
    onecount = 0
    for n in data:
        if n[pos] == '1':
            onecount += 1
    zerocount = len(data) - onecount
    co = []
    for n in data:
        if (zerocount <= onecount and n[pos] == '0') or (zerocount > onecount and n[pos] == '1'):
            co.append(n)
    if len(co) == 1:
        return int(co[0], 2)
    else:
        return filterdata_co(co, pos + 1)