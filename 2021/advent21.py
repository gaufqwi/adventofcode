from aocpython.problem import AOCProblem

class Problem(AOCProblem):
    def common(self):
        self.positions = [int(self.data.readline().strip().split()[4]), int(self.data.readline().strip().split()[4])]
        self.scores = [0, 0]
        self.turn = 0
        self.detdie_val = 1

    def detdie(self, n=1):
        r = 0
        for i in range(n):
            r += self.detdie_val
            self.detdie_val = self.detdie_val % 100 + 1
        return r

    def part1(self):
        rollcount = 0
        while self.scores[0] < 1000 and self.scores[1] < 1000:
            move = self.detdie(3)
            rollcount += 3
            self.positions[self.turn] = (self.positions[self.turn] - 1 + move) % 10 + 1
            self.scores[self.turn] += self.positions[self.turn]
            self.turn = (self.turn + 1) % 2
        print(f'Product is {rollcount * self.scores[self.turn]}')

    def part2(self):
        winscore = 21
        dirac_sum_counts = {}
        for i in range(1,4):
            for j in range(1,4):
                for k in range(1,4):
                    s = i + j + k
                    dirac_sum_counts[s] = dirac_sum_counts.get(s, 0) + 1
        dirac_sum_counts = dirac_sum_counts.items()
        finished_universes = {}
        # (p1 pos, p1 score, p2 pos, p2 score, whose turn)
        unfinished_universes = {(self.positions[0], 0, self.positions[1], 0, 0): 1}
        while len(unfinished_universes) > 0:
            uu, ucount = unfinished_universes.popitem()
            turn = uu[4]
            otherturn = (turn + 1) % 2
            pos_i = 2*turn
            score_i = pos_i + 1
            pos = uu[pos_i]
            score = uu[score_i]
            for roll, rollcount in dirac_sum_counts:
                nextu = list(uu)
                nextu[pos_i] = (pos - 1 + roll) % 10 + 1
                nextu[score_i] = score + nextu[pos_i]
                nextu[4] = otherturn
                nextu = tuple(nextu)
                if nextu[score_i] >= winscore:
                    finished_universes[nextu] = finished_universes.get(nextu, 0) + ucount * rollcount
                else:
                    unfinished_universes[nextu] = unfinished_universes.get(nextu, 0) + ucount * rollcount
        p1_wins, p2_wins = 0, 0
        for u, count in finished_universes.items():
            if u[1] >= winscore:
                p1_wins += count
            elif u[3] >= winscore:
                p2_wins += count
            else:
                raise "Uh oh. Unfinished universe in the finished pile"
        print(f'Best Dirac Dice player wins {max(p1_wins, p2_wins)} times')


