import math
import random

from bowyerwaston import Edge
def findDirection(point, edge):
    #finds which vertex isn't the current point
    if edge.vertexA == point:
         otherVertex = edge.vertexB
         middle = edge.vertexA
    else:
        otherVertex = edge.vertexA
        middle = edge.vertexB
        #if the other vertex is on the right of the current vertex the dirrection is flipped by change it to a negative
    if (edge.vertexB.x - edge.vertexA.x) != 0:
        gradient = (edge.vertexB.y - edge.vertexA.y) / (edge.vertexB.x - edge.vertexA.x)
    else:
        if otherVertex.y > point.y:
            return "top", "bottom"
        else:
            return "bottom", "top"


    direction = "left"
    oppiste = "right"
    if middle.x > otherVertex.x:
        direction = "right"
        oppiste = "left"







    #if the gradient is less than plus or minus 45 degrees then it must be left or right which is what direction is
    if gradient < 1 and gradient > -1:
        return direction, oppiste
    elif gradient >= 1:

        # a postive gradint on the left side is going up whereas for the right it must be going down
        if direction == "left":
            return "top", "bottom"
        else:
            return "bottom", "top"
    elif  gradient <= -1:
        if direction == "right":
            # a postive gradint on the right side is going up whereas for the left it must be going down
            return "top", "bottom"
        else:
            return "bottom", "top"

def connectPointsAndEdges(points, triangulations):
    pointsAndEdges = {}
    for point in points:

        weigthsAndEdges = {}

        for triangle in triangulations:



            for edge in triangle.calculateEdges():


                if (edge.vertexA.compare(point)  or edge.vertexB.compare(point)):



                    weight = math.sqrt(((edge.vertexA.x - point.x) ** 2) + ((edge.vertexA.y - point.y) ** 2))

                    weigthsAndEdges[edge] = weight






        pointsAndEdges[point] = weigthsAndEdges

    return pointsAndEdges







def findMin(weights):
    minVal = float("inf")
    minIndex = 0
    for weightIndex in range(len(weights)):
        if weights[weightIndex] < minVal:
            minVal = weights[weightIndex]
            minIndex = weightIndex

    return minIndex
def findNewPointsIndex(point, points):
    for i in points:
        if point == i:
            return i



class EdgeV2(Edge):
    #gives these edges new vaibles to rember directions of the edge
    def __init__(self, edge, vertexADirection, vertexBDirection):
        super().__init__(edge.vertexA, edge.vertexB)
        self.directionA = vertexADirection
        self.directionB = vertexBDirection


def primMst(pointAndEdges):

    visted = []
    points = list(pointAndEdges.keys())
    ordered = {}
    weights = []
    edges = []
    pointsAndDoorDirections = {}
    rejects = []
    for edgeAndWeights in pointAndEdges.values():
        for edge in edgeAndWeights:
            if edge not in rejects:

                rejects.append(edge)


    for point in points:

        pointsAndDoorDirections[point] = []
    returningEdges = {}

    currentPoint = points[0]


    while len(ordered) < len(points) -1:


        for edge, weight in pointAndEdges[currentPoint].items():
            weights.append(weight)
            edges.append(edge)
        currentWeights = weights
        currentEdges = edges
        valid = False
        while not valid:
            index = findMin(weights)

            try:
                currentWeights.pop(index)
                currentEdge = currentEdges.pop(index)
            except:

                for key, item in pointsAndDoorDirections.items():
                    ordered[key] = item

                return returningEdges, pointsAndDoorDirections, False, rejects
            vertexAnotVisted = False
            vertexBnotVisted = False
            if currentEdge.vertexA != currentPoint and currentEdge.vertexA not in visted:
                vertexAnotVisted = True

                direction, oppsite = findDirection(currentEdge.vertexB, currentEdge)
            elif currentEdge.vertexB != currentPoint and currentEdge.vertexB not in visted:
                vertexBnotVisted = True

                direction, oppsite = findDirection(currentEdge.vertexA, currentEdge)

            if vertexAnotVisted and (oppsite not in pointsAndDoorDirections[currentEdge.vertexB] and direction not in pointsAndDoorDirections[currentEdge.vertexA]):
                if edge in rejects:
                    rejects.remove(edge)
                visted.append(currentPoint)

                pointsAndDoorDirections[currentEdge.vertexB].append(oppsite)
                currentPoint =  findNewPointsIndex(currentEdge.vertexA, points)
                ordered[currentPoint] = []
                pointsAndDoorDirections[currentPoint].append(direction)
                returningEdges[EdgeV2(currentEdge, direction, oppsite)] = (0,0,0)
                valid = True
            elif vertexBnotVisted and (oppsite not in pointsAndDoorDirections[currentEdge.vertexA] and direction not in pointsAndDoorDirections[currentEdge.vertexB]):
                if edge in rejects:
                    rejects.remove(edge)

                visted.append(currentPoint)

                pointsAndDoorDirections[currentEdge.vertexA].append(oppsite)
                currentPoint =  findNewPointsIndex(currentEdge.vertexB, points)
                pointsAndDoorDirections[currentPoint].append(direction)
                ordered[currentPoint] = []
                returningEdges[EdgeV2(currentEdge, oppsite, direction)] = (0,0,0)
                valid = True


    for key, item in pointsAndDoorDirections.items():
        ordered[key] = item

    print(len(rejects), len(returningEdges), (len(rejects) - len(returningEdges)))
    return returningEdges, ordered, True, rejects


def addExtraEdges(realEdges, fakeEdges, points , randomness):


    for edge in fakeEdges:
        direction, oppiste = findDirection(edge.vertexA, edge)
        if (oppiste not in points[edge.vertexA] and direction not in points[edge.vertexB])and random.randrange(0, randomness) == 0:
            realEdges[Edge(edge, oppiste, direction)] = (0, 255, 0)
            points[edge.vertexA].append(oppiste)
            points[edge.vertexB].append(direction)

    return realEdges








