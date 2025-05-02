import os
from collections import deque

import node as n
from pliki import load_board


def generator():
    max_depth = 7
    output_dir = "generated_states"
    os.makedirs(output_dir, exist_ok=True)


    board, rows, cols = load_board("plansze/fifteen")
    initial = n.node(board, "")
    goal_board_list = initial.goal(rows, cols)
    goal_board = n.node(goal_board_list, "")

    queue = deque()
    queue.append((initial, 0))

    visited = set()
    visited.add(tuple(map(tuple, goal_board.get_board())))

    found = {i: [] for i in range(1, max_depth + 1)}

    while queue:
        current, depth = queue.popleft()
        if depth > max_depth:
            continue

        if 1 <= depth <= max_depth:
            found[depth].append(current)

        for d in "LURD":
            new_node = current.move(d, rows, cols)
            if new_node is not None:
                boardTuple = tuple(map(tuple, new_node.getBoard()))
                if boardTuple not in visited:
                    visited.add(boardTuple)
                    queue.append((new_node, depth + 1))

    for depth in found:
        for i, state in enumerate(found[depth]):
            f_name = f"{output_dir}/{rows}x{cols}_0{depth}_{i+1:04}.txt"
            with open(f_name, "w") as f:
                f.write(f"{rows} {cols}\n")
                for row in state.getBoard():
                    f.write(" ".join(map(str, row)) + "\n")

generator()
