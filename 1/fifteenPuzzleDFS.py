import time
import node as n

def depth_first_search(initial_node, max_depth, move_directions, info, rows, cols):
    start_time = time.perf_counter()
    visited_states = set()
    processed_states = set()
    info.set_max_depth_recursion(0)
    goal = initial_node.goal(rows, cols)
    stack_nodes = [initial_node]

    while stack_nodes:
        current_node = stack_nodes.pop()
        board_tuple = tuple(map(tuple, current_node.get_board()))

        if board_tuple in visited_states:
            continue
        visited_states.add(board_tuple)
        processed_states.add(board_tuple)

        if len(current_node.get_moves()) > info.get_max_depth_recursion():
            info.set_max_depth_recursion(len(current_node.get_moves()))

        if current_node.get_board() == goal:
            duration = round((time.perf_counter() - start_time) * 1000, 3)
            n.Node.the_end(current_node, len(visited_states), len(processed_states), duration,
                           len(current_node.get_moves()), info)
            return current_node.get_moves()

        if len(current_node.get_moves()) == max_depth:
            continue

        for direction in move_directions:
            new_node = current_node.move(direction, rows, cols)
            if new_node is not None:
                stack_nodes.append(new_node)

    duration = round((time.perf_counter() - start_time) * 1000, 3)
    n.Node.the_end(initial_node, len(visited_states), len(processed_states), duration, -1, info)
    return "Nie znaleziono rozwiązania"