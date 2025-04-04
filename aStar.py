import heapq
import time


def correctBoard():
    board = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]
    return board


def hamming(board, goal, w, k):
    count = 0
    for i in range(w):
        for j in range(k):
            if board[i][j] != 0 and board[i][j] != goal[i][j]:
                count += 1

    return count


def manhattan(board, goal, w, k):
    dist = 0
    positions = {goal[i][j]: (i, j) for i in range(w) for j in range(k)}

    for i in range(w):
        for j in range(k):
            if board[i][j] != 0:
                goal_x, goal_y = positions[board[i][j]]
                dist += abs(i - goal_x) + abs(j - goal_y)
    return dist


def solveAStar(startBoard, heuristic, node, direction, info):
    startTime = time.time()
    r, c = node.whereZero()
    goal = correctBoard()
    info.setMaxDepthRecursion(0)

    if heuristic == "manhattan":
        heuristicFunc = manhattan
    elif heuristic == "hamming":
        heuristicFunc = hamming
    else:
        raise ValueError("Invalid heuristic")

    queue = []
    heapq.heappush(queue, (0, 0, "", node))  # (f(n), g(n), moves, state)

    visited = set()
    visitedStates = 0
    processedStates = 0

    while queue:
        _, cost, path, board = heapq.heappop(queue)
        processedStates += 1

        if board.getBoard() == goal:
            time1 = round((time.time() - startTime) * 1000, 3)
            node.theEnd(visitedStates, processedStates, time1, len(board.getMoves()), info)
            return board.getPath()

        # visited.add(tuple(map(tuple, board)))

        for d in direction:
            newNode = node.__class__(board.getBoard(), board.getMoves())
            newBoard = newNode.move(d)

            if newBoard is not None and tuple(map(tuple, newBoard)) not in visited:
                visitedStates += 1
                newCost = cost + 1
                hValue = heuristicFunc(newBoard, goal, 4, 4)

                heapq.heappush(queue, (newCost + hValue, newCost, path + d, newNode))

    time1 = round((time.time() - startTime) * 1000, 3)
    node.theEnd(startBoard, visitedStates, processedStates, time1, -1, info)
    return "Nie znaleziono rozwiązania"
