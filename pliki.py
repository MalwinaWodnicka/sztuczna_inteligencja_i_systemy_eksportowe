import sys
from collections import deque

import fifteenPuzzleBFS as b
import fifteenPuzzleDFS as d
import aStar as a
import node as n
import searchInfo as i
import os
import subprocess

def load_board(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        rows, cols = map(int, lines[0].split())
        board = []

        for line in lines[1:]:
            board.append(list(map(int, line.split())))

    return board, rows, cols

def write_stats(file_name, length, visited, processed, depth, time_ms):
    with open(file_name, "w") as f:
        f.write(f"{length}\n{visited}\n{processed}\n{depth}\n{round(time_ms, 3)}\n")


def write_solution(file_name, moves):
    with open(file_name, "w") as f:
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
# input_file = sys.argv[3]
# solution_file = sys.argv[4]
# stats_file = sys.argv[5]
#
# board, rows, cols = load_board(input_file)
# start_node = n.node(board, "")
# info = i.info()
#
# if strategy == "bfs":
#     path = b.breadth_first_search(start_node, param, info, rows, cols)
# elif strategy == "dfs":
#     path = d.depth_first_search(start_node, param, 20, info, rows, cols)
# elif strategy == "astr":
#     path = a.solve_a_star(board, param, start_node, info, rows, cols)
# else:
#     print("Nieznana strategia:", strategy)
#     sys.exit(1)
#
#
# solution_length = len(path)
# visited = info.get_visited_states()
# processed = info.get_processed_states()
# depth = info.get_max_depth_recursion()
# time = info.get_searching_time()
#
# write_solution(solution_file, path if path else -1)
# solution_length = len(path) if path else -1
# write_stats(statsFile, solution_length, visited, processed, depth, time)





