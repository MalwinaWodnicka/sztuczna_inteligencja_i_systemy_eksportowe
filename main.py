import fun
from collections import deque

fifteenCorrect = [[1 ,2 ,3 ,4 ],
                   [5 ,6 ,7 ,8 ],
                   [9 ,10,11,12],
                   [13,14,15,0 ]]

queue = deque()

searchingTime = 0
visitedStates = 0
processedStates = 0
maxDepthRecursion = 0
duration = 0

up = [1,0]
down = [-1,0]
left = [0,-1]
right = [0,1]

directions = [up, down, left, right]

#plik z ukladem poczatkowym

def wczytaj_tablice(nazwa_pliku):
    with open(nazwa_pliku, "r") as plik:
        liczby = list(map(int, plik.read().split()))  # Wczytaj i przekonwertuj na int

    # Tworzenie tablicy 4x4 (co 4 liczby nowy wiersz)
    tablica = [liczby[i:i + 4] for i in range(0, len(liczby), 4)]

    return tablica


def where_zero(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i,j
    return None

def right_pos(board, fifteenCorrect):
    num = 0
    pos = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != fifteenCorrect[i][j]:
                num += 1
                pos.append([i,j])
    return pos, num


def solve(board, fifteenCorrect, erMoves):
    # sprawdzamy czy nie ulozylismy 15
    if fun.checkWin(board, fifteenCorrect):
        print(board)
        return True
    else:
        x, y = where_zero(board)
        pos, num = right_pos(board, fifteenCorrect)
        print(x,y,pos,num)

        move = []
        if x != 0:
            move.append("U")
        if y != 0:
            move.append("L")
        if x != len(board[0]) - 1:
            move.append("D")
        if y != len(board) - 1:
            move.append("R")

        for i in range(len(erMoves)):
            if erMoves[i] in move:
                move.remove(erMoves[i])

        print(move)







nazwa_pliku = "fifteen"
tablica = wczytaj_tablice(nazwa_pliku)

for i in range(len(tablica)):
    print(tablica[i])


print(solve(tablica, fifteenCorrect, ['L', 'D']))
