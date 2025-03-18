
def checkWin(board, fifteenCorrect):
    for i in len(board):
        for j in len(board[0]):
            if board[i][j] != fifteenCorrect[i][j]:
                return False

    return True

