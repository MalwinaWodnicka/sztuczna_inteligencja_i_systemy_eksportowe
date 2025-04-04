import time
from collections import deque
import node as n

def breadth_first_search(initialNode, moveDirections, info):
    startTime = time.time()
    visitedStates = set()
    processedStates = set()
    queueNodes = deque([initialNode])
    visitedStates.add(tuple(map(tuple, initialNode.getBoard())))

    while queueNodes:
        currentNode = queueNodes.popleft()
        processedStates.add(tuple(map(tuple, currentNode.getBoard())))

        if currentNode.isSolved():
            time1 = round((time.time() - startTime) * 1000, 3)
            n.node.theEnd(currentNode, len(visitedStates), len(processedStates), time1, len(currentNode.getMoves()), info)
            return currentNode.getPath()

        for d in moveDirections:
            newNode = n.node(currentNode.getBoard(), currentNode.getMoves())
            newBoard = newNode.move(d)
            if newBoard is not None:
                if tuple(map(tuple, newNode.getBoard())) not in visitedStates:
                    queueNodes.append(newNode)
                    visitedStates.add(tuple(map(tuple, newNode.getBoard())))


    time1 = round((time.time() - startTime) * 1000, 3)
    info.setLengthFound(-1)
    n.node.theEnd(initialNode, len(visitedStates), len(processedStates), time1, -1, info)
    return "Nie znaleziono rozwiązania"
