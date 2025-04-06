import sys
from collections import deque

import fifteenPuzzleBFS as b
import fifteenPuzzleDFS as d
import aStar as a
import node as n
import searchInfo as i
import os
import subprocess

def loadBoard(fileName):
    with open(fileName, 'r') as file:
        lines = file.readlines()
        rows, cols = map(int, lines[0].split())
        board = []

        for line in lines[1:]:
            board.append(list(map(int, line.split())))

    return board, rows, cols

def writeStats(filename, length, visited, processed, depth, time_ms):
    with open(filename, "w") as f:
        f.write(f"{length}\n{visited}\n{processed}\n{depth}\n{round(time_ms, 3)}\n")


def writeSolution(filename, moves):
    with open(filename, "w") as f:
        if moves == -1:
            f.write("-1\n")
        else:
            f.write(f"{len(moves)}\n{moves}\n")

# if len(sys.argv) != 6:
#     print("Użycie: program <strategia> <parametr> <plik_wejściowy> <plik_rozwiązania> <plik_statystyk>")
#     sys.exit(1)
#
# strategy = sys.argv[1]
# param = sys.argv[2]
# inputFile = sys.argv[3]
# solutionFile = sys.argv[4]
# statsFile = sys.argv[5]
#
# board, rows, cols = loadBoard(inputFile)
# startNode = n.node(board, "")
# info = i.info()
#
# if strategy == "bfs":
#     b.breadth_first_search(startNode, param, info, rows, cols)
# elif strategy == "dfs":
#     d.depth_first_search(startNode, param, 20, info, rows, cols)
# elif strategy == "astr":
#     a.solveAStar(board, param, startNode, info, rows, cols)
# else:
#     print("Nieznana strategia:", strategy)
#     sys.exit(1)
#
# path = startNode.getPath()
# solutionLength = len(path)
# visited = info.getVisitedStates()
# processed = info.getProcessedStates()
# depth = info.getMaxDepthRecursion()
# time = info.getSearchingTime()
#
# writeSolution(solutionFile, path if path else -1)
# solutionLength = len(path) if path else -1
# writeStats(statsFile, solutionLength, visited, processed, depth, time)





