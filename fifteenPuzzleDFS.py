import time
import node as n

def depth_first_search(initialNode, maxDepth, moveDirections, info, r, c):
    startTime = time.time()
    visitedStates = set()
    processedStates = set()
    info.setMaxDepthRecursion(0)
    goal = initialNode.goal(r, c)
    stackNodes = [initialNode]
    visitedStates.add(tuple(map(tuple, initialNode.getBoard())))

    while stackNodes:
        currentNode = stackNodes.pop()
        processedStates.add(tuple(map(tuple, currentNode.getBoard())))

        if len(currentNode.getMoves()) > info.getMaxDepthRecursion():
            info.setMaxDepthRecursion(len(currentNode.getMoves()))

        if currentNode.getBoard() == goal:
            time1 = round((time.time() - startTime) * 1000, 3)
            n.node.theEnd(currentNode, len(visitedStates), len(processedStates), time1, len(currentNode.getMoves()), info)
            return currentNode.getPath()

        if len(currentNode.getMoves()) == maxDepth:
            continue

        for d in moveDirections:
            newNode = currentNode.move(d, r, c)
            if newNode is not None and tuple(map(tuple, newNode.getBoard())) not in visitedStates:
                boardTuple = tuple(map(tuple, newNode.getBoard()))
                stackNodes.append(newNode)
                visitedStates.add(boardTuple)


    time1 = round((time.time() - startTime) * 1000, 3)
    info.setLengthFound(-1)
    n.node.theEnd(initialNode, len(visitedStates), len(processedStates), time1, -1, info)
    return "Nie znaleziono rozwiązania"

