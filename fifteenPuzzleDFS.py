import time
import node as n

def depth_first_search(initialNode, maxDepth, moveDirections, info):
    startTime = time.time()
    visitedStates = set()
    processedStates = set()
    info.setMaxDepthRecursion(0)

    stackNodes = [initialNode]
    visitedStates.add(tuple(map(tuple, initialNode.getBoard())))

    while stackNodes:
        currentNode = stackNodes.pop()
        processedStates.add(tuple(map(tuple, currentNode.getBoard())))

        if len(currentNode.getMoves()) > info.getMaxDepthRecursion():
            info.setMaxDepthRecursion(len(currentNode.getMoves()))

        if currentNode.isSolved():
            time1 = round((time.time() - startTime) * 1000, 3)
            n.node.theEnd(currentNode, visitedStates, processedStates, time1, len(currentNode.getMoves()), info)
            return currentNode.getPath()

        if len(currentNode.getMoves()) == maxDepth:
            continue

        for d in moveDirections:
            newNode = n.node(currentNode.getBoard(), currentNode.getMoves())
            newBoard = newNode.move(d)
            if newBoard is not None:
                if tuple(map(tuple, newNode.getBoard())) not in visitedStates:
                    stackNodes.append(newNode)
                    visitedStates.add(tuple(map(tuple, newNode.getBoard())))


    time1 = round((time.time() - startTime) * 1000, 3)
    info.setLengthFound(-1)
    n.node.theEnd(initialNode, visitedStates, processedStates, time1, -1, info)
    return "Nie znaleziono rozwiązania"

