def main(data, part, log):
    graph = {}
    for line in data:
        a, b = line.strip().split('-')
        graph[a] = graph.get(a, []) + [b]
        graph[b] = graph.get(b, []) + [a]
    paths = extend_path(graph, ['start'], part)
    print(f'There are {len(paths)} paths')

def extend_path(graph, path, maxrepeats):
    extensions = []
    last = path[-1]
    if check_for_dups(path):
        maxrepeats = 1
    for dest in graph[last]:
        if dest == 'start':
            continue
        elif dest == 'end':
            extensions.append(path + ['end'])
        elif dest.isupper() or path.count(dest) < maxrepeats:
            newpath = path + [dest]
            if dest == 'end':
                extensions.append(newpath)
            else:
                extensions = extensions + extend_path(graph, newpath, maxrepeats)
    return extensions

# Yeah, it's n^2. This could be done better with a different data structure but, it works
def check_for_dups(path):
    for i in range(len(path)):
        for j in range(i+1,len(path)):
            if path[i] == path[j] and path[i].islower():
                return True
    return False