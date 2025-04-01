import searchInfo as i
import node as n

def depth_first_search(initialNode, maxDepth, moveDirections, info):
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
            info.setVisitedStates(len(visitedStates))
            info.setProcessedStates(len(processedStates))
            return currentNode.getPath()

        if len(currentNode.getMoves()) == maxDepth:
            continue

        for moveDirection in moveDirections:
            newNode = n.node(currentNode.getBoard(), currentNode.getMoves())
            newBoard = newNode.move(moveDirection)
            if newBoard is not None:
                if tuple(map(tuple, newNode.getBoard())) not in visitedStates:
                    stackNodes.append(newNode)
                    visitedStates.add(tuple(map(tuple, newNode.getBoard())))

    info.setVisitedStates(len(visitedStates))
    info.setProcessedStates(len(processedStates))
    return "Nie znaleziono rozwiązania"

