import fifteenPuzzleDFS as dfs
import node as n
import searchInfo as i


def loadBoard(fileName):
    with open(fileName, 'r') as file:
        lines = file.readlines()
        rows, cols = map(int, lines[0].split())
        board = []

        for line in lines[1:]:
            board.append(list(map(int, line.split())))

    return board, (rows, cols)


def main():
    inf = i.info()
    tablica, wymiary = loadBoard("fifteen")
    print(tablica)
    print(wymiary)

    dfsInfo = i.info()

    tab = n.node(tablica, None, "RULD")
    inf = i.info()
    path = dfs.dfs(tab, 7, "RULD", inf)

    if path is None:
        print("No path found")
    else:
        print(path, inf)

if __name__ == "__main__":
    main()


"""
[[1, 2, 3, 4], 
[5, 6, 7, 8], 
[9, 10, 11, 12], 
[0, 13, 14, 15]]
"""