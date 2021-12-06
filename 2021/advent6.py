gentime = 7
newborn_bonus = 2

def main(data, part, log):
    data = [int(x) for x in data.read().strip().split(',')]
    if part == 1:
        part1(data, 80, log)
    if part == 2:
        part2(data, 256, log)

# Naive way (well, it worked)
def part1(fishes, span, log):
    for i in range(span):
        nextgen = []
        for fish in fishes:
            if fish == 0:
                nextgen.append(gentime - 1)
                nextgen.append(gentime + newborn_bonus - 1)
            else:
                nextgen.append(fish - 1)
        fishes = nextgen
        log.info(f'After {i+1} days there are {len(fishes)} fish')
    print(f'After {span} days there are {len(fishes)} fish')

# Saner, more scalable way
def part2(data, span, log):
    fishes = {}
    for i in range(gentime + newborn_bonus):
        fishes[i] = 0
    for fish in data:
        fishes[fish] += 1
    for i in range(span):
        newborns = parents = fishes[0]
        for i in range(gentime + newborn_bonus - 1):
            fishes[i] = fishes[i+1]
        fishes[gentime - 1] += parents
        fishes[gentime + newborn_bonus - 1] = newborns
    count = 0
    for age, num in fishes.items():
        count += num
    print(f'After {span} days there are {count} fish')
