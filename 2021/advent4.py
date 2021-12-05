def parsedata(data):
    text = data.read()
    sections = text.split('\n\n')
    numbers = list(map(int, sections[0].split(',')))
    boards = []
    for section in sections[1:]:
        if section.strip() == '':
            continue
        boards.append(list(map(lambda x: list(map(int, x.split())), section.split('\n'))))
    return (numbers, boards)

class Board:
    def __init__(self, rows):
        self.rows = rows[:5]
        self.finished = False

    def winner(self):
        rows = self.rows
        for i in range(5):
            if (rows[i][0] == 'x' and rows[i][1] == 'x' and rows[i][2] == 'x' and rows[i][3] == 'x' and rows[i][
                4] == 'x'):
                self.finished = True
                return True
            if (rows[0][i] == 'x' and rows[1][i] == 'x' and rows[2][i] == 'x' and rows[3][i] == 'x' and rows[4][
                i] == 'x'):
                self.finished = True
                return True
        # if (rows[0][0] == 'x' and rows[1][1] == 'x' and rows[2][2] == 'x' and rows[3][3] == 'x' and rows[4][4] == 'x'):
        #    self.finished = True
        #    return True
        # if (rows[0][4] == 'x' and rows[1][3] == 'x' and rows[2][2] == 'x' and rows[3][1] == 'x' and rows[4][0] == 'x'):
        #    self.finished = True
        #    return True
        return False

    def mark(self, num):
        for row in self.rows:
            for i in range(5):
                if row[i] == num:
                    row[i] = 'x'
                    return True
        return False

    def sum(self):
        t = 0
        for row in self.rows:
            for val in row:
                if val != 'x':
                    t += val
        return t


def main(data, part, log):
    numbers, boards = parsedata(data)
    for i in range(len(boards)):
        boards[i] = Board(boards[i])
    for call in numbers:
        boards = [board for board in boards if board.finished == False]
        for board in boards:
            board.mark(call)
            if board.winner():
                if part == 1:
                    s = board.sum()
                    print('Call', call, 'Sum', s, 'Product', call * s)
                    return
                elif len(boards) == 1:
                    s = board.sum()
                    print('Call', call, 'Sum', s, 'Product', call * s)
                    return