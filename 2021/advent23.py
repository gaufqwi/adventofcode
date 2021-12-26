from aocpython.problem import AOCProblem

costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

class CantMove(Exception):
    pass

class State:
    def __init__(self, depth=2, locations={}, cost=0, locks=set(), parent=None, move_desc=None):
        self.depth = depth
        self.locations = locations
        self.occupied = set(locations.values())
        self.cost = cost
        self.locks = locks
        self.parent = parent
        self.move_desc = move_desc

    def fp(self):
        key = str(self.cost)
        for k, v in self.locations.items():
            key += k + v
        return key

    def move(self, paths, amp, dest):
        current = self.locations[amp]
        if dest == current or amp in self.locks:
            raise CantMove
        path, dist = paths[current][dest]
        if len(path.intersection(self.occupied)) > 0:
            raise CantMove
        if current[0] == 'H':
            locks = self.locks.copy()
            locks.add(amp)
        else:
            locks = self.locks
        locations = self.locations.copy()
        locations[amp] = dest
        move_desc = f'Move {amp} from {current} to {dest}'
        return State(self.depth, locations, self.cost + dist * costs[amp[0]], locks, self, move_desc)

    def can_go_home(self, amp):
        species = amp[0]
        friends = []
        for other, loc in self.locations.items():
            if loc[1] != species:
                continue
            if other[0] != species:
                return False
            friends.append(int(loc[-1]))
        if len(friends) == 0:
            return f'R{species}{self.depth-1}'
        top = min(friends)
        if top > 0:
            return f'R{species}{top-1}'
        else:
            return False

    def everybody_home(self):
        for amp, loc in self.locations.items():
            if loc[1] != amp[0]:
                return False
        return True

class WorstState(State):
    def __init__(self):
        self.cost = int(1e9)

class Problem(AOCProblem):
    def common(self):
        self.initial_positions =  [[], [], [], []]
        self.data.readline()
        self.data.readline()
        for i in range(2):
            line = self.data.readline()
            for j in range(4):
                self.initial_positions[j].append(line[2*j+3])

    def dfsearch(self, state, best=WorstState(), cache={}, depth=0):
        #self.log.debug(f'DFsearch depth {depth}')
        self.log.debug(f'DFsearch cost {depth} - {state.cost}')
        fp = state.fp()
        if fp in cache:
            return cache[fp]
        for amp in self.amps:
            # Always try to go home
            home = state.can_go_home(amp)
            #print(amp, '->', home, '|', state.locations)
            if home:
                try:
                    newstate = state.move(self.paths, amp, home)
                    if newstate.everybody_home():
                        # if newstate.cost == 18195:
                        #print('Win', newstate.cost, newstate.locations)
                        if newstate.cost < best.cost:
                            best = newstate
                    else:
                        if newstate.cost < best.cost: # Prune
                            candidate = self.dfsearch(newstate, best, cache, depth+1)
                            if candidate.cost < best.cost:
                                best = candidate
                except CantMove:
                    pass
            # If in a room, try to move to the hall
            if state.locations[amp][0] == 'R':
                for hall in ['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6']:
                    try:
                        newstate = state.move(self.paths, amp, hall)
                        if newstate.cost < best.cost: # Prune
                            candidate = self.dfsearch(newstate, best, cache, depth+1)
                            if candidate.cost < best.cost:
                                best = candidate
                    except CantMove:
                        pass
        cache[fp] = best
        return best

    def make_graph(self, room_depth=2):
        self.room_depth = room_depth
        self.amps = []
        for species in ['A', 'B', 'C', 'D']:
            for i in range(room_depth):
                self.amps.append(f'{species}{i}')
        self.graph = {}
        # Hall
        for i in range(7):
            node = f'H{i}'
            if i == 0:
                self.graph[node] = [('H1', 1)]
            elif i == 1:
                self.graph[node] = [('H0', 1), ('H2', 2)]
            elif i <= 4:
                self.graph[node] = [(f'H{i-1}', 2), (f'H{i+1}', 2)]
            elif i == 5:
                self.graph[node] = [('H4', 2), ('H6', 1)]
            else:
                self.graph[node] = [('H5', 1)]
        # Rooms
        for i in range(4):
            nodestem = 'R' + chr(ord('A') + i)
            for d in range(room_depth):
                node = nodestem + str(d)
                lhall, rhall = f'H{i+1}', f'H{i+2}'
                if d == 0:
                    self.graph[node] = [(lhall, 2), (rhall, 2)]
                    self.graph[lhall].append((node, 2))
                    self.graph[rhall].append((node, 2))
                else:
                    self.graph[node] = [(f'{nodestem}{d-1}', 1)]
                if d != room_depth-1:
                    self.graph[node].append((f'{nodestem}{d+1}', 1))

    def make_paths(self):
        nodes = self.graph.keys()
        self.paths = {}
        for source, neighbors in self.graph.items():
            self.paths[source] = {}
            for node in nodes:
                if node == source:
                    continue
                self.paths[source][node] = (set(), 1e9)
            reachable = []
            for node, dist in neighbors:
                reachable.append(node)
                self.paths[source][node] = ({node}, dist)
            reachable.sort(key=lambda x: self.paths[source][x][1])
            visited = set()
            while len(reachable) > 0:
                dest = reachable.pop(0)
                pathset, dist = self.paths[source][dest]
                visited.add(dest)
                # something?
                for node, hop_dist in self.graph[dest]:
                    if node == source:
                        continue
                    if node not in visited:
                        reachable.append(node)
                    if dist + hop_dist < self.paths[source][node][1]:
                        self.paths[source][node] = (pathset.union({node}), dist + hop_dist)
                reachable.sort(key=lambda x: self.paths[source][x][1])

    def part1(self):
        self.make_graph()
        self.make_paths()
        names = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        locations = {}
        for i in range(self.room_depth):
            for j, room in enumerate(['RA', 'RB', 'RC', 'RD']):
                species = self.initial_positions[j][i]
                n = names[species]
                names[species] += 1
                locations[species + str(n)] = f'{room}{i}'
        initial_state = State(self.room_depth, locations)
        best = self.dfsearch(initial_state)
        print(f'Best cost is {best.cost}')

    def part2(self):
        self.make_graph(room_depth=4)
        self.make_paths()
        names = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        #print(self.initial_positions)
        splices = [['D', 'D'], ['C', 'B'], ['B', 'A'], ['A', 'C']]
        for i in range(4):
            self.initial_positions[i][1:-1] = splices[i]
        #print(self.initial_positions)
        locations = {}
        for i in range(self.room_depth):
            for j, room in enumerate(['RA', 'RB', 'RC', 'RD']):
                species = self.initial_positions[j][i]
                n = names[species]
                names[species] += 1
                locations[species + str(n)] = f'{room}{i}'
        initial_state = State(self.room_depth, locations)
        best = self.dfsearch(initial_state)
        print(f'Best cost is {best.cost}')