def main(data, part, log):
    template = data.readline().strip()
    data.readline()
    rules = {}
    for line in data:
        pair, insertion = line.strip().split(' -> ')
        rules[pair] = insertion
    if part == 1:
        #part1(template, rules)
        part2(template, rules, 10)
    else:
        part2(template, rules)

# Naive slow implementation
def part1(template, rules):
    for i in range(10):
        newtemplate = ''
        for j in range(len(template) - 1):
            pair = template[j:j+2]
            newtemplate += pair[0]
            if pair in rules:
                newtemplate += rules[pair]
        template = newtemplate + template[-1]
    counts = {}
    for l in template:
        counts[l] = counts.get(l, 0) + 1
    least = 100000000
    most = 0
    for count in counts.values():
        if count < least:
            least = count
        if count > most:
            most = count
    print(f'Difference between most and least is {most - least}')

# Should of seen the need for this coming
def part2(template, rules, iterations=40):
    pair_counts = {}
    for i in range(len(template) - 1):
        pair = template[i:i+2]
        pair_counts[pair] = pair_counts.get(pair, 0) + 1
    for i in range(iterations):
        new_pair_counts = pair_counts.copy()
        for pair, insertion in rules.items():
            if pair in pair_counts:
                oldcount = pair_counts[pair]
                new_pair_counts[pair] -= oldcount
                new_pair_counts[pair[0] + insertion] = new_pair_counts.get(pair[0] + insertion, 0) + oldcount
                new_pair_counts[insertion + pair[1]] = new_pair_counts.get(insertion + pair[1], 0) + oldcount
        pair_counts = new_pair_counts
    # I guess I could have maintained counts all along, but eh, this works
    counts = {}
    for pair, count in pair_counts.items():
        counts[pair[0]] = counts.get(pair[0], 0) + count
        counts[pair[1]] = counts.get(pair[1], 0) + count
    counts[template[0]] += 1
    counts[template[-1]] += 1
    least = 1e16
    most = 0
    for count in counts.values():
        count = count // 2
        if count < least:
            least = count
        if count > most:
            most = count
    print(f'Difference between most and least is {most - least}')


