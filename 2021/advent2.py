def parsedata(data):
    parsed = []
    for line in data:
        item = line.strip().split(' ')
        item[1] = int(item[1])
        parsed.append(item)
    return parsed

def main(data, part, log):
    data = parsedata(data)
    if part == 1:
        part1(data)
    else:
        part2(data)

def part1(data):
    x = 0
    depth = 0
    for instruction, param in data:
        if instruction == 'forward':
            x += param
        elif instruction == 'down':
            depth += param
        elif instruction == 'up':
            depth -= param
    print('x', x, 'depth', depth, 'product', x * depth)


def part2(data):
    x = 0
    depth = 0
    aim = 0
    for instruction, param in data:
        if instruction == 'forward':
            x += param
            depth += (aim * param)
        elif instruction == 'down':
            aim += param
        elif instruction == 'up':
            aim -= param
    print('x', x, 'depth', depth, 'aim', aim, 'product', x * depth)