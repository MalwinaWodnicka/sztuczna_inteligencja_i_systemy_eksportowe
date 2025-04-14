import time
from collections import deque
import node as n

def breadth_first_search(initial_node, move_directions, info, rows, cols):
    start_time = time.perf_counter()
    visited_states = set()
    processed_states = set()
    goal = initial_node.goal(rows, cols)
    info.set_max_depth_recursion(0)
    queue_nodes = deque([initial_node])
    visited_states.add(tuple(map(tuple, initial_node.get_board())))

    while queue_nodes:
        current_node = queue_nodes.popleft()
        processed_states.add(tuple(map(tuple, current_node.get_board())))

        if len(current_node.get_moves()) > info.get_max_depth_recursion():
            info.set_max_depth_recursion(len(current_node.get_moves()))

        if current_node.get_board() == goal:
            duration = round((time.perf_counter() - start_time) * 1000, 3)
            n.Node.the_end(current_node, len(visited_states), len(processed_states), duration,
                           len(current_node.get_moves()), info)
            return current_node.get_path()

        for direction in move_directions:
            new_node = current_node.move(direction, rows, cols)
            if new_node is not None and tuple(map(tuple, new_node.get_board())) not in visited_states:
                board_tuple = tuple(map(tuple, new_node.get_board()))
                queue_nodes.append(new_node)
                visited_states.add(board_tuple)

    duration = round((time.perf_counter() - start_time) * 1000, 3)
    n.Node.the_end(initial_node, len(visited_states), len(processed_states), duration, -1, info)
    return "Nie znaleziono rozwiązania"
