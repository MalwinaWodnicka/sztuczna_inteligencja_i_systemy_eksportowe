import copy


class node:
    def __init__(self, board, moves):
        self.board = board
        self.moves = moves

    def whereZero(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if self.board[r][c] == 0:
                    return r, c
        return None

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

    def move(self, direction):
        r, c = self.whereZero()
        newR, newC = r, c

        if self.getLastMove() == "L" and direction == "R":
            return None, None
        if self.getLastMove() == "R" and direction == "L":
            return None, None
        if self.getLastMove() == "U" and direction == "D":
            return None, None
        if self.getLastMove() == "D" and direction == "U":
            return None, None

        if not self.isMoveLegal(direction):
            return None, None

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

        self.moves += direction
        self.board = newBoard

        return newBoard, (newR, newC)

    def isMoveLegal(self, direction):
        r, c = self.whereZero()
        if r == 0 and direction == "U":
            return False
        if r == 3 and direction == "D":
            return False
        if c == 0 and direction == "L":
            return False
        if c == 3 and direction == "R":
            return False
        else:
            return True

    def isSolved(self):
        goal = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        return self.board == goal

    def getPath(self):
        return self.moves
