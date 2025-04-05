import heapq
import time



def hamming(board, goal, r, c):
    count = 0
    for i in range(r):
        for j in range(c):
            if board[i][j] != 0 and board[i][j] != goal[i][j]:
                count += 1

    return count


def manhattan(board, goal, r, c):
    dist = 0
    positions = {goal[i][j]: (i, j) for i in range(r) for j in range(c)}

    for i in range(r):
        for j in range(c):
            if board[i][j] != 0:
                goal_x, goal_y = positions[board[i][j]]
                dist += abs(i - goal_x) + abs(j - goal_y)
    return dist


def solveAStar(startBoard, heuristic, node, info, r, c):
    startTime = time.time()
    goal = node.isSolved(r, c)

    if heuristic == "manh":
        heuristicFunc = manhattan
    elif heuristic == "hamm":
        heuristicFunc = hamming
    else:
        raise ValueError("Invalid heuristic")

    queue = []
    heapq.heappush(queue, (0, 0, "", node))  # (f(n), g(n), moves, state)

    visitedStates = set()
    processedStates = 0

    while queue:
        _, cost, path, board = heapq.heappop(queue)
        processedStates += 1

        if board.getBoard() == goal:
            time1 = round((time.time() - startTime) * 1000, 3)
            node.theEnd(len(visitedStates), processedStates, time1, len(board.getMoves()), info)
            return board.getPath()


        for d in "LURD":
            newNode = board.move(d, r, c)
            if newNode is not None and tuple(map(tuple, newNode.getBoard())) not in visitedStates:
                visitedStates.add(tuple(map(tuple, newNode.getBoard())))
                newCost = cost + 1
                hValue = heuristicFunc(newNode.getBoard(), goal, len(startBoard), len(startBoard[0]))
                heapq.heappush(queue, (newCost + hValue, newCost, path + d, newNode))

    time1 = round((time.time() - startTime) * 1000, 3)
    node.theEnd(startBoard, len(visitedStates), processedStates, time1, -1, info)
    return "Nie znaleziono rozwiązania"
