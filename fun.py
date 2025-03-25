
def checkWin(board, fifteenCorrect):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != fifteenCorrect[i][j]:
                return False

    return True




