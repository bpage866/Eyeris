import numpy as np
import random

def calculateCircumcenter (a,b,c):
    d = 2 * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y))
    centerX = ((a.x * a.x + a.y * a.y) * (b.y - c.y) + (b.x * b.x + b.y * b.y) * (c.y - a.y) + (c.x * c.x + c.y * c.y) * (a.y - b.y)) / d
    centerY = ((a.x * a.x + a.y * a.y) * (c.x - b.x) + (b.x * b.x + b.y * b.y) * (a.x - c.x) + (c.x * c.x + c.y * c.y) * (b.x - a.x)) / d
    return (centerX, centerY)

def isInCircumcircleOf(triangle, vertex):

        a_x = triangle.vertexA.x
        a_y = triangle.vertexA.y

        b_x = triangle.vertexB.x
        b_y = triangle.vertexB.y

        c_x = triangle.vertexC.x
        c_y = triangle.vertexC.y

        # The point coordinates

        d_x = vertex.x
        d_y = vertex.y

        # If the following determinant is greater than zero then point lies inside circumcircle
        incircle = np.array([[a_x - d_x, a_y - d_y, (a_x - d_x) ** 2 + (a_y - d_y) ** 2],
                             [b_x - d_x, b_y - d_y, (b_x - d_x) ** 2 + (b_y - d_y) ** 2],
                             [c_x - d_x, c_y - d_y, (c_x - d_x) ** 2 + (c_y - d_y) ** 2]])

        if np.linalg.det(incircle) > 0:
            return True
        else:
            return False

def inCircumCircle(triangle, vertex):
    ax = triangle.vertexA.x - vertex.x
    ay = triangle.vertexA.y - vertex.y
    bx = triangle.vertexB.x  - vertex.x
    by = triangle.vertexB.y  - vertex.y
    cx = triangle.vertexC.x - vertex.x
    cy = triangle.vertexC.y - vertex.y
    if (ax * ax + ay * ay) * (bx * cy - cx * by) - (bx * bx + by * by) * (ax * cy - cx * ay) + (cx * cx + cy * cy) * (ax * by - bx * ay) > 0:
        return True

    else:
        return False


# Python3 program to find the points
# which lies inside, outside or
# on the circle

# Function to find the line given
# two points
def lineFromPoints(vertexA, vertexB):
    a = vertexB[1] - vertexA[1]
    b = vertexA[0] - vertexB[0]
    c = a * (vertexA[0]) + b * (vertexA[1])

    return a, b, c


# Function which converts the
# input line to its perpendicular
# bisector. It also inputs the
# points whose mid-lies o
# on the bisector
def perpenBisectorFromLine(vertexA, vertexB, a, b):
    # Find the mid point
    mid_point = [0, 0]

    # x coordinates
    mid_point[0] = (vertexA[0] + vertexB[0]) / 2

    # y coordinates
    mid_point[1] = (vertexA[1] + vertexB[1]) / 2

    # c = -bx + ay
    c = (-b * (mid_point[0]) +
         a * (mid_point[1]))

    # Assign the coefficient of
    # a and b
    temp = a
    a = -b
    b = temp

    return a, b, c


# Returns the intersection of
# two lines
def LineInterX(a1, b1, c1, a2, b2, c2):
    # Find determinant
    determ = a1 * b2 - a2 * b1

    x = (b2 * c1 - b1 * c2)


    x /= determ


    return x


# Returns the intersection of
# two lines
def LineInterY(a1, b1, c1, a2, b2, c2):
    # Find determinant
    determ = a1 * b2 - a2 * b1

    y = (a1 * c2 - a2 * c1)

    # print(y)
    y /= determ

    return y


# Function to find the point
# lies inside, outside or on
# the circle
def findPosition(triangle, vertexorgin):
    vertexA = (triangle.vertexA.x, triangle.vertexA.y)
    vertexB = (triangle.vertexB.x, triangle.vertexB.y)
    vertexC = (triangle.vertexC.x, triangle.vertexC.y)
    vertex = (vertexorgin.x, vertexorgin.y)

    # Store the coordinates
    # radius of circumcircle
    radius = [0, 0]

    # Line PQ is represented
    # as ax + by = c
    a, b, c = lineFromPoints(vertexA, vertexB)

    # Line QR is represented
    # as ex + fy = g
    e, f, g = lineFromPoints(vertexB, vertexC)

    # Converting lines PQ and QR
    # to perpendicular bisectors.
    # After this, L = ax + by = c
    # M = ex + fy = g
    a, b, c = perpenBisectorFromLine(vertexA, vertexB, a, b)
    e, f, g = perpenBisectorFromLine(vertexB, vertexC, e,f)

    # The of intersection
    # of L and M gives r as the
    # circumcenter
    radius[0] = LineInterX(a, b, c, e, f, g)
    radius[1] = LineInterY(a, b, c, e, f, g)

    # Length of radius
    q = ((radius[0] - vertexA[0]) *
         (radius[0] - vertexA[0]) +
         (radius[1] - vertexA[1]) *
         (radius[1] - vertexA[1]))

    # Distance between radius
    # and the given D
    dis = ((radius[0] - vertex[0]) *
           (radius[0] - vertex[0]) +
           (radius[1] - vertex[1]) *
           (radius[1] - vertex[1]))

    # Condition for lies
    # inside circumcircle
    if (dis < q):

        return True


    # outside or on the circumcircle
    else:

        return False
# from function lineFromPoints code is adapted from code by mohit kumar 29

def edgeNotInAnyOther(currentedge, triangles, currentTriangle ):
    notInAnyOther = True
    for triangle in triangles:
        if currentTriangle != triangle:
            for edge in triangle.calculateEdges():
                if currentedge.compare(currentedge, edge):
                    notInAnyOther = False
                    return notInAnyOther
    return notInAnyOther

def doesntContainsSameVertex(triangle, superTri):
    doesntContainSame = True
    triVertexs = [(triangle.vertexA.x,triangle.vertexA.y), (triangle.vertexB.x,triangle.vertexB.y), (triangle.vertexC.x,triangle.vertexC.y)]
    superVertexs = [(superTri.vertexA.x,superTri.vertexA.y), (superTri.vertexB.x,superTri.vertexB.y), (superTri.vertexC.x,superTri.vertexC.y)]

    for triVertex in triVertexs:
        if triVertex in superVertexs:

            doesntContainSame = False
            return doesntContainSame
    return doesntContainSame

def superTriangle(vertexs):
    minX = float("inf")
    maxX = float("-inf")
    minY = float("inf")
    maxY = float("-inf")

    for vertex in vertexs:
        minX = min(minX, vertex.x)
        minY = min(minY, vertex.y)
        maxX = max(maxX, vertex.x)
        maxY = max(maxY, vertex.y)

    dx = (maxX - minX) * 10
    dy = (maxY - minY) * 10
    vertexA = Vertex(minX - dx, minY - dy * 3)
    vertexB = Vertex(minX - dx, maxY + dy)
    vertexC = Vertex(maxX + dx * 3, maxY + dy)
    return Triangle(vertexA, vertexB, vertexC)


class Vertex():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def compare(self,otherVertex):
        if self.x == otherVertex.x and self.y == otherVertex.y:
            return True
        else:
            return False

class Edge():
    def __init__(self, vertexA, vertexB):
        self.vertexA = vertexA
        self.vertexB = vertexB

    def compare(self, EdgeA, EdgeB):

        if (EdgeA.vertexA == EdgeB.vertexA and EdgeA.vertexB == EdgeB.vertexB) or (EdgeA.vertexA == EdgeB.vertexB and EdgeA.vertexB == EdgeB.vertexA):

            return True
        else:
            return False

class Triangle():
    def __init__(self, vertexA, vertexB, vertexC):
        self.vertexA = vertexA
        self.vertexB = vertexB
        self.vertexC = vertexC
    def calculateEdges(self):
        return [Edge(self.vertexA, self.vertexB), Edge(self.vertexA, self.vertexC), Edge(self.vertexB, self.vertexC)]



def triangulate(vertexs):
    allTris = []

    mySuperTriangle = superTriangle(vertexs)

    triangulation  = [mySuperTriangle]
    totalTris = 0

    for vertex in vertexs:
        badTriangles = []

        for triangle in triangulation:
            inOrOut = findPosition(triangle, vertex)
            if inOrOut:

                badTriangles.append(triangle)

        polygon = []
        for triangle in badTriangles:

            for edge in triangle.calculateEdges():

                if edgeNotInAnyOther(edge, badTriangles, triangle):

                    polygon.append(edge)
        for triangle in badTriangles:
            if triangle in triangulation:

                triangulation.remove(triangle)


        for edge in polygon:

            totalTris += 1
            triangulation.append(Triangle(vertex, edge.vertexA, edge.vertexB))
            allTris.append(Triangle(edge.vertexA, edge.vertexB, vertex))
    #there is usaually duplicate bad triangles so the bad triangles are found then to make sure there is no change to list while iterating
    removalLsit = []
    for triangle in triangulation:

        if doesntContainsSameVertex(triangle, mySuperTriangle) == False:
            removalLsit.append(triangle)

    for removal in removalLsit:
       triangulation.remove((removal))



    return triangulation







