
class node:
    def __init__(self, board, root, direction):
        self.board = board
        self.root = root
        self.direction = direction
        self.level = root.level + 1 if root else 0

    def whereZero(self, board):
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if board[r][c] == 0:
                    return r, c
        return None

    def getDirection(self):
        return self.direction

    def getLevel(self):
        return self.level

    def getRoot(self):
        return self.root

    def getBoard(self):
        return self.board

    def move(self, board, direction, currentNode):
        r, c = self.whereZero(board)
        newR, newC = r, c

        if currentNode.getDirection() == "L" and direction == "R":
            return None, None
        if currentNode.getDirection() == "R" and direction == "L":
            return None, None
        if currentNode.getDirection() == "U" and direction == "D":
            return None, None
        if currentNode.getDirection() == "D" and direction == "U":
            return None, None

        if (r == 0 and direction == "U"):
            return None, None
        if (r == 3 and direction == "D"):
            return None, None
        if (c == 0 and direction == "L"):
            return None, None
        if (c == 3 and direction == "R"):
            return None, None

        newBoard = [row[:] for row in board]

        newBoard[r][c], newBoard[newR][newC] = newBoard[newR][newC], newBoard[r][c]

        return newBoard, (newR, newC)

    def isSolved(self, board):
        goal = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        return board == goal

    def getPath(self):
        path = []
        node = self
        while node:
            path.append(node.direction)
            node = node.root
        return ''.join(reversed(path))
