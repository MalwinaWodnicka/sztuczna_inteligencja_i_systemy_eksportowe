import searchInfo as i
import node as n


def dfs(startNode, maxDepth, direction, inf):
    visited = set()
    processed = set()
    inf.setMaxDepthRecursion(0)

    stack = [startNode]
    visited.add(tuple(map(tuple, startNode.getBoard())))

    while stack:
        currentNode = stack.pop()
        processed.add(tuple(map(tuple, currentNode.getBoard())))


        if len(currentNode.moves) > inf.getMaxDepthRecursion():
            inf.setMaxDepthRecursion(len(currentNode.moves))

        if currentNode.isSolved():
            inf.setVisitedStates(len(visited))
            inf.setProcessedStates(len(processed))
            return currentNode.getPath()

        if len(currentNode.getMoves()) == maxDepth:
            continue

        for d in direction:
            new = n.node(currentNode.getBoard(), currentNode.getMoves())
            newBoard, newZeroPos = new.move(d)
            if newBoard is not None:
                if tuple(map(tuple, new.getBoard())) not in visited:
                    stack.append(new)
                    visited.add(tuple(map(tuple, new.getBoard())))

    inf.setVisitedStates(len(visited))
    inf.setProcessedStates(len(processed))
    return "Nie znaleziono rozwiązania"
