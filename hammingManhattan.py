def whereZero(self):
    for r in range(len(self.board)):
        for c in range(len(self.board[0])):
            if self.board[r][c] == 0:
                return r, c
    return None

def correctBoard():
    board = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]
    return board

def hamming(board, goal):
    zeroX, zeroY = board.whereZero()

    count = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != 0 and board[i][j] != goal[i][j]:
                count += 1

    return count


def manhattan(board, goal, w, k):
    dist = 0
    positions = {goal[i][j]: (i, j) for i in range(w) for j in range(k)}

    for i in range(w):
        for j in range(k):
            if board[i][j] != 0:
                goal_x, goal_y = positions[board[i][j]]
                dist += abs(i - goal_x) + abs(j - goal_y)
    return dist

