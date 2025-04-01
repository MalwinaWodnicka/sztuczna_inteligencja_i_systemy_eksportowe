import fifteenPuzzleDFS as d
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
    # inf = i.info()
    # tablica, wymiary = loadBoard("fifteen")
    # print(tablica)
    # print(wymiary)
    #
    # dfsInfo = i.info()
    #
    # tab = n.node(tablica, None)
    # inf = i.info()
    # path = dfs.dfs(tab, 7, "RULD", inf)
    #
    # if path is None:
    #     print("No path found")
    # else:
    #     print(path, inf)


    tabe = [
        [1, 2, 3, 4],
        [5, 7, 11, 8],
        [9, 6, 0, 12],
        [13, 10, 14, 15]
    ]
    firstNode = n.node(tabe, "")

    if firstNode.isSolved():
        print(":)")

    inf = i.info()
    print(d.depth_first_search(firstNode, 7, "LDUR", inf))
    print(inf)

if __name__ == "__main__":
    main()


"""
[[1, 2, 3, 4], 
[5, 6, 7, 8], 
[9, 10, 11, 12], 
[0, 13, 14, 15]]
"""