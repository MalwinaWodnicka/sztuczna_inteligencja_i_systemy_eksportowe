import itertools
import time
from heapq import heappush, heappop


def hamming(board, goal, r, c):
    count = 0
    for i in range(r):
        for j in range(c):
            if board[i][j] != 0 and board[i][j] != goal[i][j]:
                count += 1
    return count


def manhattan(board, goal, r, c):
    dist = 0
    positions = {goal[i][j]: (i, j) for i in range(r) for j in range(c)}

    for i in range(r):
        for j in range(c):
            if board[i][j] != 0:
                goal_x, goal_y = positions[board[i][j]]
                dist += abs(i - goal_x) + abs(j - goal_y)
    return dist


def solve_a_star(start_board, heuristic, node, info, r, c):
    start_time = time.perf_counter()
    goal = node.goal(r, c)
    info.set_max_depth_recursion(0)
    visited_states = set()
    processed_states = 0

    if heuristic == "manh":
        heuristic_func = manhattan
    elif heuristic == "hamm":
        heuristic_func = hamming
    else:
        raise ValueError("Invalid heuristic")

    counter = itertools.count()
    queue = []

    initial_h = heuristic_func(start_board, goal, r, c)
    heappush(queue, (initial_h, next(counter), node))

    while queue:
        _, _, current = heappop(queue)
        processed_states += 1

        if len(current.get_moves()) > info.get_max_depth_recursion():
            info.set_max_depth_recursion(len(current.get_moves()))

        if current.get_board() == goal:
            elapsed_time = round((time.perf_counter() - start_time) * 1000, 3)
            node.the_end(len(visited_states), processed_states, elapsed_time, len(current.get_moves()), info)
            return current.get_moves()

        for direction in "LURD":
            choice = current.move(direction, r, c)
            if choice is not None:
                board_tuple = tuple(map(tuple, choice.get_board()))
                if board_tuple in visited_states:
                    continue

                visited_states.add(board_tuple)
                g = len(choice.get_moves())
                h = heuristic_func(choice.get_board(), goal, r, c)
                f = g + h
                heappush(queue, (f, next(counter), choice))

    elapsed_time = round((time.perf_counter() - start_time) * 1000, 3)
    node.the_end(start_board, len(visited_states), processed_states, elapsed_time, -1, info)
    return "Nie znaleziono rozwiązania"
