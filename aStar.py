import heapq
import time


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


def get_choices(state, r, c):
    new_states = []
    for d in "LURD":
        moving = state.move(d, r, c)
        if moving is not None:
            new_states.append(moving)
    return new_states


def solve_a_star(start_board, heuristic, node, info, r, c):
    start_time = time.time()
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

    queue = []
    heapq.heappush(queue, (0 + heuristic_func(start_board, goal, r, c), 0, "", node))

    while queue:
        f, cost, path, current = heapq.heappop(queue)
        processed_states += 1

        if len(current.get_moves()) > info.get_max_depth_recursion():
            info.set_max_depth_recursion(len(current.get_moves()))

        if current.get_board() == goal:
            elapsed_time = round((time.time() - start_time) * 1000, 3)
            node.the_end(len(visited_states), processed_states, elapsed_time, len(current.get_path()), info)
            return current.get_path()

        board = get_choices(current, r, c)
        for choice in board:
            board_tuple = tuple(map(tuple, choice.get_board()))
            if board_tuple not in visited_states and board_tuple is not None:
                visited_states.add(board_tuple)
                new_cost = cost + 1
                h_value = heuristic_func(choice.get_board(), goal, r, c)
                heapq.heappush(queue, (new_cost + h_value, new_cost, current.get_path() + choice.get_path(), choice))

    elapsed_time = round((time.time() - start_time) * 1000, 3)
    node.the_end(start_board, len(visited_states), processed_states, elapsed_time, -1, info)
    return "Nie znaleziono rozwiązania"
