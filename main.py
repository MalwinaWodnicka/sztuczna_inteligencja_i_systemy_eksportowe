import os

import fifteenPuzzleDFS as d
import node as n
import searchInfo as i
import aStar
import fifteenPuzzleBFS as b

def loadBoard(fileName):
    with open(fileName, 'r') as file:
        lines = file.readlines()
        rows, cols = map(int, lines[0].split())
        board = []

        for line in lines[1:]:
            board.append(list(map(int, line.split())))

    return board, rows, cols


def main():
    tabe, r, c = loadBoard("fifteen")
    firstNode = n.node(tabe, "")
    inf = i.info()

    while True:
        print("bfs - breadth first search \ndfs - depth first search\nA* (A-star) - astr\nq - quit")
        wybor = input("Wybierz strategię: ").lower()
        if wybor == "bfs":
            directions = input("Podaj porządek przeszukiwania: ").upper()
            print(b.breadth_first_search(firstNode, directions, inf, r, c))
            print(inf)
        elif wybor == "dfs":
            directions = input("Podaj porządek przeszukiwania: ").upper()
            print(d.depth_first_search(firstNode, 20,directions, inf, r, c))
            print(inf)
            print("Maksymalna głębokość rekursji: " + str(inf.getMaxDepthRecursion()))
        elif wybor == "astr":
            while True:
                heuristic = input("Wybierz heurystyke(hamm/manh): ")
                if heuristic == "hamm":
                    print(aStar.solveAStar(tabe, heuristic, firstNode, inf, r, c))
                    print(inf)
                    break
                elif heuristic == "manh":
                    print(aStar.solveAStar(tabe, heuristic, firstNode, inf, r, c))
                    print(inf)
                    break
                else:
                    print("Niepoprawna heurystytka.")
        elif wybor == "q":
            break
        else:
            print("Nie ma takiego wyboru.")
        input("\nNacisnij enter, aby kontynuować...")
        print("\n"*3)




if __name__ == "__main__":
    main()


"""
[[1, 2, 3, 4], 
[5, 6, 7, 8], 
[9, 10, 11, 12], 
[0, 13, 14, 15]]
"""