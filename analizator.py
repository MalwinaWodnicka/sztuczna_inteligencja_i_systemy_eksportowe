import os
import time
import node as n
import pliki
import fifteenPuzzleDFS as d
import fifteenPuzzleBFS as b
import aStar as a
import searchInfo as i

# Definicja kierunków ruchu
move_directions = [
    "RDLU",  # prawo-dół-góra-lewo
    "RDLU",  # prawo-dół-lewo-góra
    "DRLU",  # dół-prawo-góra-lewo
    "DRLU",  # dół-prawo-lewo-góra
    "LUDR",  # lewo-góra-dół-prawo
    "LUDR",  # lewo-góra-prawo-dół
    "ULRD",  # góra-lewo-dół-prawo
    "ULRD"   # góra-lewo-prawo-dół
]

def analyze_all_files(inputDir, outputDir):
    for filename in os.listdir(inputDir):
        if filename.endswith(".txt"):
            file_path = os.path.join(inputDir, filename)

            # Wczytanie planszy
            board, rows, cols = pliki.loadBoard(file_path)
            initial = n.node(board, "")
            info = i.info()

            parts = filename.split("_")
            depth_str = parts[1]  # "01" z pliku "4x4_01_0001.txt"
            number_str = parts[-1].split(".")[0]  # "0001" z pliku "4x4_01_0001.txt"
            base_filename = f"{rows}x{cols}_{depth_str}_{number_str}"


            for direction in move_directions:
                solution = b.breadth_first_search(initial, direction, info, rows, cols)
                # solution, moves, output_dir, base_filename, algorithm, d
                save_solution(solution, len(solution), outputDir, base_filename, "bfs", direction)
                save_additional_info(info, outputDir, base_filename, "bfs", direction)
                # info, output_dir, base_filename, algorithm, d


            for direction in move_directions:
                solution = d.depth_first_search(initial, 20, direction, info, rows, cols)
                save_solution(solution, len(solution), outputDir, base_filename, "dfs", direction)
                save_additional_info(info, outputDir, base_filename, "dfs", direction)


            solution = a.solveAStar(board, "hamm", initial, info, rows, cols)
            save_solution(solution, len(solution), outputDir, base_filename, "astr", "hamm")
            save_additional_info(info, outputDir, base_filename, "astr", "hamm")


            solution = a.solveAStar(board, "manh", initial, info, rows, cols)
            save_solution(solution, len(solution), outputDir, base_filename, "astr", "manh")
            save_additional_info(info, outputDir, base_filename, "astr", "manh")

def save_additional_info(info, output_dir, base_filename, algorithm, d):
    # Pobranie danych z instancji klasy info
    solution_length = info.getLengthFound() if info.getLengthFound() is not None else -1
    visited_count = info.getVisitedStates()
    processed_count = info.getProcessedStates()
    max_depth = info.getMaxDepthRecursion() if info.getMaxDepthRecursion() is not None else 0
    elapsed_time = info.getSearchingTime()

    with open(f"{output_dir}/{base_filename}_{algorithm}_{d}_stats.txt", "w") as f:
        f.write(f"{solution_length}\n")
        f.write(f"{visited_count}\n")
        f.write(f"{processed_count}\n")
        f.write(f"{max_depth}\n")
        f.write(f"{elapsed_time:.3f}\n")

def save_solution(solution, moves, output_dir, base_filename, algorithm, d):
    # Sprawdzenie, czy rozwiązanie jest None
    if solution is None:
        with open(f"{output_dir}/{base_filename}_{algorithm}_{d}_sol.txt", "w") as f:
            f.write("-1\n")
    else:
        # Zapisz rozwiązanie w pliku
        with open(f"{output_dir}/{base_filename}_{algorithm}_{d}_sol.txt", "w") as f:
            f.write(f"{moves}\n")  # Zapisz długość rozwiązania
            f.write("".join(solution) + "\n")  # Zapisz rozwiązanie jako ciąg znaków


input_dir = "generated_states"
output_dir = "analysis_results"
os.makedirs(output_dir, exist_ok=True)



# Uruchomienie analizy wszystkich plików
analyze_all_files(input_dir, output_dir)