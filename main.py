import os

import fifteenPuzzleDFS as dfs
import node as n
import pliki
import searchInfo as info
import aStar
import fifteenPuzzleBFS as bfs


def main():
    board, rows, cols = pliki.load_board("generated_states/4x4_07_0212.txt")
    first_node = n.Node(board, "")
    search_info = info.Info()

    while True:
        print("bfs - breadth first search \ndfs - depth first search\nA* (A-star) - astr\nq - quit")
        choice = input("Wybierz strategię: ").lower()

        if choice == "bfs":
            directions = input("Podaj porządek przeszukiwania: ").upper()
            print(bfs.breadth_first_search(first_node, directions, search_info, rows, cols))
            print(search_info)

        elif choice == "dfs":
            directions = input("Podaj porządek przeszukiwania: ").upper()
            print(dfs.depth_first_search(first_node, 20, directions, search_info, rows, cols))
            print(search_info)

        elif choice == "astr":
            while True:
                heuristic = input("Wybierz heurystykę (hamm/manh): ")
                if heuristic in ["hamm", "manh"]:
                    print(aStar.solve_a_star(board, heuristic, first_node, search_info, rows, cols))
                    print(search_info)
                    break
                else:
                    print("Niepoprawna heurystyka.")

        elif choice == "q":
            break

        else:
            print("Nie ma takiego wyboru.")

        input("\nNaciśnij Enter, aby kontynuować...")
        print("\n" * 3)


if __name__ == "__main__":
    main()
