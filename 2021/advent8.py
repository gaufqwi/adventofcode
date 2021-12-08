def main(data, part, log):
    parsed = []
    for line in data:
        samples, outputs = line.split('|')
        samples = samples.strip().split()
        outputs = outputs.strip().split()
        parsed.append((samples, outputs))
    if part == 1:
        part1(parsed, log)
    else:
        part2(parsed, log)

def part1(data, log):
    count = 0
    for samples, output in data:
        for o in output:
            l = len(o)
            if l == 2 or l == 3 or l == 4 or l == 7:
                count += 1
    print(f'{count} instances of 1, 4, 7, or 8 in outputs')

# There's probably a much more elegant way to do this
def part2(data, log):
    total = 0
    for samples, outputs in data:
        segment_map = {}
        samples = [set(s) for s in samples]
        samples_by_length = {}
        for samp in samples:
            samples_by_length[len(samp)] = samples_by_length.get(len(samp), []) + [samp]
        one = samples_by_length[2].pop() # Got 1
        seven = samples_by_length[3].pop() # Got 7
        four = samples_by_length[4].pop() # Got 4
        eight = samples_by_length[7].pop() # Got 8
        for three in samples_by_length[5]:
            if len(three & one) == 2:
                break
        samples_by_length[5].remove(three) # Got 3
        for six in samples_by_length[6]:
            if len(six & one) == 1:
                break
        samples_by_length[6].remove(six) # Got 6
        segment_map['f'] = (six - one).pop() # Got f
        for num in samples_by_length[6]:
            if len(num - three) == 1:
                nine = num # Got 9
            else:
                zero = num # Got 0
        for num in samples_by_length[5]:
            if len(num - six) == 0:
                five = num # Got 5
            else:
                two = num # Got 2
        segment_map['a'] = (seven - one).pop()
        segment_map['b'] = (five - three).pop()
        segment_map['c'] = (one - six).pop()
        segment_map['d'] = (two - zero).pop()
        segment_map['e'] = (six - nine).pop()
        segment_map['f'] = (one - two).pop()
        segment_map['g'] = (nine - four - seven).pop()
        segment_map = {v: k for k, v in segment_map.items()}
        for i in range(4):
            power = 10 ** (3 - i)
            output = outputs[i]
            fixed = []
            for seg in output:
                fixed.append(segment_map[seg])
            fixed.sort()
            total += power * digits[''.join(fixed)]
    print(f'Total of displays is {total}')


digits = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9
}
