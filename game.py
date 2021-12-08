from itertools import groupby, chain

NONE = '-'
RED = 'R'
YELLOW = 'Y'


def diagonalsPos(matrix, cols, rows):  # gets matrix positive diagonals
    for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if 0 <= i < cols and 0 <= j < rows]


def diagonalsNeg(matrix, cols, rows):  # gets matrix negative diagonals
    for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if 0 <= i < cols and 0 <= j < rows]


class Game:
    def __init__(self, cols=7, rows=6):
        self.cols = cols
        self.rows = rows
        self.board = [[NONE] * rows for _ in range(cols)]

    def insert(self, column, color):
        c = self.board[column]
        while True:
            if c[0] != NONE:
                print("column is full! pick a different one.")
                c = self.board[int(input())]
            else:
                break
        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color
        winner = self.getWinner()
        return winner

    def getWinner(self):
        lines = (
            self.board,  # columns
            zip(*self.board),  # rows
            diagonalsPos(self.board, self.cols, self.rows),  # positive diagonals
            diagonalsNeg(self.board, self.cols, self.rows)  # negative diagonals
        )

        for line in chain(*lines):  # for each line in (chain(*lines)- makes a big list out of all the lines)
            for color, group in groupby(line):  # creates a group by each line that is deviated by color for each of the lines
                if color != NONE and len(list(group)) >= 4:  # checks if the conditions for a win are applying
                    return color

    def printBoard(self):
        print(' | '.join(map(str, range(self.cols))))
        for y in range(self.rows):
            print(' | '.join(str(self.board[x][y]) for x in range(self.cols)))
        print()

    def get_column(self):
        column = input('{}\'s turn: '.format('Red' if turn == RED else 'Yellow'))
        if int(column) < 0 or int(column) > 6:
            print("number entered not in range please try again.")
            return -1
        return column

    def get_percentage_board(self):
        counter = 0
        for y in range(self.rows):
            for x in range(self.cols):
                if str(self.board[x][y]) != NONE:
                    counter += 1
        return (counter / 42) * 100

    def get_highest(self):
        max_col = 0
        num_col = 0
        for col in range(self.cols):
            c = self.board[col]
            i = -1
            while c[i] != NONE:
                i -= 1
            if i < max_col:
                max_col = i
                num_col = col
        return max_col, num_col


if __name__ == '__main__':
    g = Game()
    turn = RED
    while True:
        column = g.get_column()
        if column != -1:
            g.printBoard()
            w = g.insert(int(column), turn)
            if not w:
                turn = YELLOW if turn == RED else RED
