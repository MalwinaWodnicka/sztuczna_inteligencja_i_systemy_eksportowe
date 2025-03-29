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

        if currentNode.getLevel() > inf.getMaxDepthRecursion():
            inf.setMaxDepthRecursion(currentNode.getLevel())

        if currentNode.isSolved(currentNode.getBoard()):
            inf.setVisitedStates(len(visited))
            inf.setProcessedStates(len(processed))
            return currentNode.getPath()

        if currentNode.getLevel() == maxDepth:
            continue

        for d in direction:

            if currentNode.getDirection() == "L" and d == "R":
                continue
            if currentNode.getDirection() == "R" and d == "L":
                continue
            if currentNode.getDirection() == "U" and d == "D":
                continue
            if currentNode.getDirection() == "D" and d == "U":
                continue

            r, c = startNode.whereZero(currentNode.getBoard())

            if r == 0 and d == "U":
                continue
            if r == 3 and d == "D":
                continue
            if c == 0 and d == "L":
                continue
            if c == 3 and d == "R":
                continue

            if newBoard is not None and tuple(map(tuple, newBoard)) not in visited:
                newNode = n.node(newBoard, currentNode, d)
                stack.append(newNode)
                visited.add(tuple(map(tuple, newBoard)))

    inf.setVisitedStates(len(visited))
    inf.setProcessedStates(len(processed))
    return None
