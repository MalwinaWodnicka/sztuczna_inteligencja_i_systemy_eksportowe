import os
import time
import node as n
import pliki
import fifteenPuzzleDFS as d
import fifteenPuzzleBFS as b
import aStar as a
import searchInfo as i

move_directions = [
    "RDUL",
    "RDLU",
    "DRUL",
    "DRLU",
    "LURD",
    "LUDR",
    "ULDR",
    "ULRD"
]

def analyze_all_files(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)

            board, rows, cols = pliki.load_board(file_path)
            initial_node = n.Node(board, "")
            search_info = i.Info()

            parts = filename.split("_")
            depth_str = parts[1]
            number_str = parts[-1].split(".")[0]
            base_filename = f"{rows}x{cols}_{depth_str}_{number_str}"

            for direction in move_directions:
                solution = b.breadth_first_search(initial_node, direction, search_info, rows, cols)
                save_solution(solution, len(solution), output_dir, base_filename, "bfs", direction)
                save_additional_info(search_info, output_dir, base_filename, "bfs", direction)

            for direction in move_directions:
                solution = d.depth_first_search(initial_node, 20, direction, search_info, rows, cols)
                save_solution(solution, len(solution), output_dir, base_filename, "dfs", direction)
                save_additional_info(search_info, output_dir, base_filename, "dfs", direction)

            solution = a.solve_a_star(board, "hamm", initial_node, search_info, rows, cols)
            save_solution(solution, len(solution), output_dir, base_filename, "astr", "hamm")
            save_additional_info(search_info, output_dir, base_filename, "astr", "hamm")

            solution = a.solve_a_star(board, "manh", initial_node, search_info, rows, cols)
            save_solution(solution, len(solution), output_dir, base_filename, "astr", "manh")
            save_additional_info(search_info, output_dir, base_filename, "astr", "manh")

def save_additional_info(search_info, output_dir, base_filename, algorithm, direction):
    solution_length = search_info.get_length_found() if search_info.get_length_found() is not None else -1
    visited_count = search_info.get_visited_states()
    processed_count = search_info.get_processed_states()
    max_depth = search_info.get_max_depth_recursion() if search_info.get_max_depth_recursion() is not None else 0
    elapsed_time = search_info.get_searching_time()

    with open(f"{output_dir}/{base_filename}_{algorithm}_{direction}_stats.txt", "w") as f:
        f.write(f"{solution_length}\n")
        f.write(f"{visited_count}\n")
        f.write(f"{processed_count}\n")
        f.write(f"{max_depth}\n")
        f.write(f"{elapsed_time:.3f}\n")

def save_solution(solution, moves, output_dir, base_filename, algorithm, direction):
    file_path = f"{output_dir}/{base_filename}_{algorithm}_{direction}_sol.txt"
    with open(file_path, "w") as f:
        if solution is None:
            f.write("-1\n")
        else:
            f.write(f"{moves}\n")
            f.write("".join(solution) + "\n")


input_dir = "generated_states"
output_dir = "analysis_results"
os.makedirs(output_dir, exist_ok=True)

analyze_all_files(input_dir, output_dir)