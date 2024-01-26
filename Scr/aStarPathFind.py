
class Node():

    def __init__(self, tileType=None, parent=None, position=None):
        self.tileType = tileType
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def equalPosition(self, other):
        return self.position == other.position



def nodeTileMapWithPostion(tileMap, tileMapPosition, tileSize):
    updatedMap = {}
    for y in range(len(tileMap)):

        for x in range(len(tileMap[0])):

            pos = (tileMapPosition[0] + (x * tileSize) + (tileSize/2), tileMapPosition[1] + (y * tileSize) + (tileSize/2))
            updatedMap[pos] = Node(tileMap[y][x], None,pos)

    return updatedMap



def aStarPathFind(startPosition, target, nodeTileMap, totalMoved, tileSize):
    startNode = Node(None, None, (startPosition[0] - (startPosition[0] % tileSize) + tileSize/2, startPosition[1] - (startPosition[1] % tileSize) + tileSize/2))
    startNode.g = startNode.h = startNode.f = 0
    startNode.g = 0
    startNode.h = 0
    startNode.f = 0

    endNode = Node(None, None, (target[0] - (target[0] % tileSize) + tileSize/2, target[1] - (target[1] % tileSize) + tileSize/2))
    endNode.g = 0
    endNode.h = 0
    endNode.f = 0

    openList = []
    closedList = []
    # Add the start node
    openList.append(startNode)


    while openList and len(closedList) < totalMoved:

        # Get the current node
        currentNode = openList[0]

        i = 0

        for i, item in enumerate(openList):
            if item.f < currentNode.f:
                currentNode = item
                i = i

        # Pop current off open list, add to closed list
        openList.pop(i)
        closedList.append(currentNode)
        # Found the goal
        if currentNode == endNode:
            print("iiiii")
            aStarPathFind()

            return closedList

        # Generate adjentTiles
        children = []
        #direct adjent Tiles in
        lst = [(0, -tileSize), (0, tileSize), (-tileSize, 0), (tileSize, 0), (tileSize, -tileSize), (-tileSize, tileSize), (-tileSize, -tileSize), (tileSize, tileSize)]
        for new_position in lst:

            # Get node position

            node_position = (currentNode.position[0] + new_position[0], currentNode.position[1] + new_position[1])

            # Make sure within rang

            # Make sure walkable terrain
            if nodeTileMap[node_position].tileType == "f":

            #node is given the current node as its parent
                newNode = nodeTileMap[node_position]
                newNode.parent = currentNode
                # Append
                children.append(newNode)

        # Loop through children

        for child in children:


            # Child is on the closed list
            for closedChild in closedList:

                if child == closedChild:
                    continue

            # Create the f, g, and h values
            child.g = currentNode.g + 1
            child.h = ((child.position[0] - endNode.position[0]) ** 2) + (
                                (child.position[1] - endNode.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list

            for openNode in openList:

                if child == openNode and child.g > openNode.g:

                    continue

            openList.append(child)


    return closedList






