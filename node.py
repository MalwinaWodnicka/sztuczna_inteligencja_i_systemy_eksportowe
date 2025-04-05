import copy


class node:
    def __init__(self, board, moves):
        self.board = copy.deepcopy(board)
        self.moves = moves[:]

    def whereZero(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if self.board[r][c] == 0:
                    return r, c
        return None, None

    def getMoves(self):
        return self.moves

    def getBoard(self):
        return self.board

    def addNew(self, newDirection):
        newBoard = copy.deepcopy(self.board)
        return node(newBoard, self, newDirection)

    def getLastMove(self):
        if len(self.moves) == 0:
            return ""
        return self.moves[-1]

    def move(self, direction, rows, cols):
        r, c = self.whereZero()
        newR, newC = r, c

        if self.getLastMove() == "L" and direction == "R":
            return None
        if self.getLastMove() == "R" and direction == "L":
            return None
        if self.getLastMove() == "U" and direction == "D":
            return None
        if self.getLastMove() == "D" and direction == "U":
            return None

        if not self.isMoveLegal(direction, rows, cols):
            return None

        newBoard = [row[:] for row in self.getBoard()]

        if direction == "L":
            newC -= 1
        if direction == "R":
            newC += 1
        if direction == "U":
            newR -= 1
        if direction == "D":
            newR += 1

        newBoard[r][c], newBoard[newR][newC] = newBoard[newR][newC], newBoard[r][c]

        newMoves = self.moves + direction
        return node(newBoard, newMoves)

    def isMoveLegal(self, direction, rows, cols):
        r, c = self.whereZero()
        if r == 0 and direction == "U":
            return False
        if r == rows - 1 and direction == "D":
            return False
        if c == 0 and direction == "L":
            return False
        if c == cols - 1 and direction == "R":
            return False
        else:
            return True

    def isSolved(self, rows, cols):
        expected = []
        n = 1

        for i in range(rows):
            row = []
            for j in range(cols):
                if i == rows - 1 and j == cols - 1:
                    row.append(0)
                else:
                    row.append(n)
                    n += 1
            expected.append(row)

        return expected

    def getPath(self):
        return self.moves

    def theEnd(self, visited, processed, time, length, info):
        info.setLengthFound(length)
        info.setProcessedStates(processed)
        info.setSearchingTime(time)
        info.setVisitedStates(visited)


