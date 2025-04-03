import fifteenPuzzleDFS as d
import node as n
import searchInfo as i
import aStar

def loadBoard(fileName):
    with open(fileName, 'r') as file:
        lines = file.readlines()
        rows, cols = map(int, lines[0].split())
        board = []

        for line in lines[1:]:
            board.append(list(map(int, line.split())))

    return board, (rows, cols)


def main():
    tabe = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]
    # firstNode = n.node(tabe, "")
    #
    # if firstNode.isSolved():
    #     print(":)")
    #
    # inf = i.info()
    # print(d.depth_first_search(firstNode, 20, "RLUD", inf))
    # print(inf)

    initialNode = n.node(tabe, "")

    # Wybór heurystyki
    heuristic = "manhattan"

    # Tworzymy obiekt klasy info
    info = i.info()

    # Uruchamiamy A*
    solution = aStar.solveAStar(tabe, heuristic, initialNode, "LURD", info)


if __name__ == "__main__":
    main()


"""
[[1, 2, 3, 4], 
[5, 6, 7, 8], 
[9, 10, 11, 12], 
[0, 13, 14, 15]]
"""