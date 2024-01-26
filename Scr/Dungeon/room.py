import random

from datetime import datetime


from tile import Tile
import sys
import os
#uses abspath which fins the path to V1 on the users device so will work for anyone

path = os.path.abspath("")[:-8]

sys.path.append(path)

#import all the varibles from Dependecies
from Dependencies import*

from pickUpsHolder import PickUpsHolder
from enemyCage import EnemyCage
from enemyCage import BossCage
from stage import Stage
class Room():
    def __init__(self, offset, dungeonScore):
        self.roomPosition = offset

        self.doors = {"top": None, "bottom": None, "left": None, "right": None}
        self.offset = (0,0)

        self.connections = {"top":None, "bottom":None, "left":None, "right":None}
        #dataStructure for any Enemies in the room
        self.pickUps = PickUpsHolder()
        self.enemyCage = EnemyCage(dungeonScore)
        self.projectiles = EnemyCage(0)
        self.stage = Stage()

    def randomSeed(self):
        self.seed = datetime.now().timestamp()
        random.seed(self.seed)
        print(self.seed)

    def setSeed(self, seed):
        #if the seed being set was that of a prevoius save, the room desgin can be precoudually generated again and will look the same
        self.seed = seed
        random.seed(self.seed)

    def roundShape(self, leftx, rightx, y):
        # changes the left and right side wall in this contect to make them somewhat curve
        olds = [leftx, rightx]

        xS = [0,0]

        for i in range(2):
            #random option of changing or staying the same
            option = random.randrange(0, 2)
            #if the option is more then half of the room plus or minus 3 a change can happen
            print(olds[i], "olds")
            if y < (self.height/2) - 3:


                if option == 0:
                    # if the old value was more then 3 it must stay the so it doesnt dip bellow the index
                    if olds[i] > 3:
                        while xS[i] <= 2:
                            #from the old value a random new value is subtracted for new value
                            xS[i] = olds[i]  -random.randrange(1, 3)

                    else:
                        xS[i] = olds[i]
                elif option == 1:
                    #if option two stay the same
                    xS[i] = olds[i]

            elif y > (self.height/2) + 3:

                if option == 0:

                    if olds[i] < (self.width / 2) - 4:
                        while xS[i] <= 0:
                            xS[i] = olds[i] + random.randrange(1, 3)

                    else:
                        xS[i] = olds[i]
                elif option == 1:
                    #stays the same
                    xS[i] = olds[i]
            #when betwen the values stated above the wall is forced to 1 so the door can gernate properly
            else:
                xS[i] = 1
        return xS[0], xS[1]

    class Labyrinth():
        #generates rooms with extra walls
        def __init__(self, width, height):
            self.height = height
            self.width = width
            self.lastWall = 0
        def shape(self, y):
            #checks value is not at the centre of the height with an addation
            if y < (self.height/2) - 3 or y > (self.height/2) + 3:
                #checks is not to close to other walls or gaps
                if y >= self.lastWall + 5 and (y < (self.height/2) - 1 or (y < self.height - 6 and y > (self.height/2) + 3)):
                    option = random.randrange(0,4)
                    if option == 0:
                        #no extra wall is generated
                        return 2, 2
                    elif option == 1:
                        #two symetrical walls are generated
                        newX = random.randrange(4, (self.width/2) - 3)
                        self.lastWall = y
                        return newX, newX
                    elif option == 2:

                        leftOrRight = random.randrange(0,2)
                        if leftOrRight == 0:
                            # places wall on both side with long length for right
                            left = random.randrange(2,int(self.width/4) - 2)
                            right = random.randrange(2, (self.width - 6 - left))
                            self.lastWall = y
                            return left, right
                        elif leftOrRight == 1:
                            # places wall on both side with long length for left
                            right = random.randrange(2, int(self.width / 4) - 2)
                            left = random.randrange(2, (self.width - 6 - right))
                            self.lastWall = y
                            return left, right
                    elif option == 3:
                        leftOrRight = random.randrange(0, 2)
                        if leftOrRight == 0:
                            # places wall on both side with long length for right
                            right = random.randrange(2, (self.width - 6))
                            self.lastWall = y
                            return 2, right
                        elif leftOrRight == 1:
                            # places wall on both side with long length for left
                            left = random.randrange(2, (self.width - 10))
                            self.lastWall = y
                            return left, 2
                else:
                    return 2, 2
            else:
                return 1,1
    class Junction():
        def __init__(self, doors, width, height):
            self.straight = False
            if ("left" in doors or "right" in doors) and (("top" not in doors and "bottom" not in doors)):


                self.height = height
                self.width = int(self.height / 2)
                if self.width % 2 != 0:
                    self.width += 1
                self.straight = True
            elif ("top" in doors or "bottom" in doors) and (("left" not in doors and "right" not in doors)):
                self.width =  width
                self.height = int(self.width / 2)
                if self.height % 2 != 0:
                    self.height += 1
                self.straight = True
            else:
                self.width = width
                self.height = int(self.width)

                if len(doors) > 0:

                    doorArray = [0,0,0,0]
                    if "top" in doors:

                        doorArray[0] = "d"
                    if "left" in doors:

                        doorArray[1] = "d"
                    if "right" in doors:
                        doorArray[2] = "d"
                    if "bottom" in doors:

                        doorArray[3] = "d"
                    if doorArray[1] == "d" and doorArray [2] == 0:
                        lefx = random.randrange(int(self.width/4), self.width/2)
                        rightx = 1
                    elif doorArray[2] == "d" and doorArray[1] == 0:
                        rightx = random.randrange(int(self.width / 4), self.width / 2)
                        lefx = 1
                    else:
                        rightx = random.randrange(int(self.width / 4), int(self.width / 3))
                        lefx = random.randrange(int(self.width / 4), int(self.width / 3))

                    if doorArray[0] == "d" and doorArray [3] == 0:
                        topy = random.randrange(int(self.height/3), self.height/2)
                        bottomy = self.height - 2
                    elif doorArray[3] == "d" and doorArray [0] == 0:
                        bottomy =  self.height -  1 - random.randrange(int(self.height/3), self.height/2)
                        topy = 1
                    else:
                        topy = random.randrange(int(self.height / 4), int(self.height / 3))
                        bottomy = self.height - random.randrange(int(self.height / 4), int(self.height / 3)) - 1
                    self.wallPoints =[lefx, rightx, topy, bottomy]
                else:
                    self.straight = True

        def getDimensions(self):

            return self.height,self.width
        def shape(self, y):
            if self.straight == True:
                print(self.height, self.width)
                return 1,1
            else:



                if self.wallPoints[2] -1 <= y  and  self.wallPoints[3] >= y:

                    return 1, 1
                else:

                    return self.wallPoints[0], self.wallPoints[1]

    def placeInitializedSetPiece(self, setPeice):
        possibleChecks = (self.width - 4) * (self.height - 4)


        validSpot = False
        count = 0
        while not validSpot or count == possibleChecks:
            count += 1
            x = random.randrange(TILESIZE * 3, (self.width - 3) * TILESIZE, TILESIZE * 3) + self.roomPosition[0]
            y = random.randrange(TILESIZE * 3, (self.height - 3) * TILESIZE, TILESIZE * 3) + self.roomPosition[1]

            surroundings, throwAway = self.getSurroundingTiles((x, y), True)

            if len(surroundings["left"]) == 0 and len(surroundings["right"]) == 0 and len(
                    surroundings["top"]) == 0 and len(surroundings["bottom"]) == 0:


                validSpot = True

                setPeice.setPos((x,y))
                setPeice.updateRects()

                self.stage.stagePeices.append(setPeice)

    def validPlayerPostion(self):
        possibleChecks = (self.width - 6) * (self.height - 6)


        validSpot = False
        count = 0
        while not validSpot or count == possibleChecks:
            count += 1
            x = random.randrange(TILESIZE * 5, (self.width - 5) * TILESIZE, TILESIZE * 1) + self.roomPosition[0]
            y = random.randrange(TILESIZE * 5, (self.height - 5) * TILESIZE, TILESIZE * 1) + self.roomPosition[1]

            surroundings, throwAway = self.getSurroundingTiles((x, y), True)

            if len(surroundings["left"]) == 0 and len(surroundings["right"]) == 0 and len(
                    surroundings["top"]) == 0 and len(surroundings["bottom"]) == 0:



                return  (x,y)


    def placeEnemies(self, enemiesList):
        #must be done last in room Creation
        possibleChecks = (self.width - 4) * (self.height - 4)
        previousPositions = []
        for enemyClassAndScoreList in enemiesList:
            #enemyClassAndScore list as [enemy class, score]
            validSpot = False
            count = 0
            while not validSpot or count == possibleChecks:
                count += 1
                x = random.randrange(TILESIZE * 2, (self.width -3) * TILESIZE, TILESIZE * 2) + self.roomPosition[0]
                y = random.randrange(TILESIZE * 2, (self.height - 3) * TILESIZE, TILESIZE * 2) + self.roomPosition[1]

                surroundings, throwAway = self.getSurroundingTiles((x, y), True)



                if len(surroundings["left"]) == 0 and len(surroundings["right"]) == 0 and len(surroundings["top"]) == 0 and len(surroundings["bottom"]) == 0:

                    if (x,y) not in previousPositions:
                        validSpot = True
                        previousPositions.append((x,y))

                        self.enemyCage.enemyList.insert(-1, enemyClassAndScoreList[0]((x,y), enemyClassAndScoreList[1], self.roomShape, self.roomPosition))


                if count == possibleChecks - 1:
                    print(count, possibleChecks, enemiesList)

                    raise Exception("room is to small to Fit any Enemies ")


        #orders by score using bubbleSort
        for i in range(len(self.enemyCage.enemyList) - 1):
            for ii in range(0, len(self.enemyCage.enemyList) - i - 1):

                if self.enemyCage.enemyList[ii].getScore() > self.enemyCage.enemyList[ii + 1].getScore() :

                    self.enemyCage.enemyList[ii], self.enemyCage.enemyList[ii + 1] = self.enemyCage.enemyList[ii + 1], self.enemyCage.enemyList[ii]






    def genrateRoomShape(self, shape, doors, minRoomSize, maxRoomSize):
        self.roomType = "room"

        self.width = random.randrange(minRoomSize,maxRoomSize,2)
        self.height = random.randrange(minRoomSize, maxRoomSize,2)

        self.roomShape = []
        self.shape = shape

        # left x and right x are where sides of the walls are placed in each row
        # based of the shape of room the staring leftx and rightx are set
        if self.shape == "square":
            leftX = 1
            rightX = 1

        elif self.shape == "round":
            maxs = int(self.width/2) - 2
            leftX = random.randrange(int(maxs/2),maxs)
            rightX = random.randrange(int(maxs/2),maxs)

        elif self.shape == "labyrinth":
            leftX = 1
            rightX = 1
            laby = self.Labyrinth(self.width, self.height)
        elif self.shape ==  "junction":
            junct = self.Junction(doors, self.width, self.height)
            self.width, self.height = junct.getDimensions()
            leftX, rightX = junct.shape(1)
        oldLeftX = leftX
        for i in range(self.height):
            row = []

            for ii in range(self.width):

                if i == 0 or i == self.height -1:
                    row.append("b")
                elif ii < leftX or ii > self.width - rightX -1:
                    if self.roomShape[i-1][ii] == "f":
                        row.append("w")
                    elif ((self.roomShape[i-1][ii] == "w" and row[ii-1] == "b") and self.roomShape[i-1][ii+1] == "f") or ((self.roomShape[i-1][ii] == "w" and row[ii-1] == "w") and self.roomShape[i-1][ii-1] == "f"):
                        row.append("w")


                    else:
                        row.append("b")



                elif ii == leftX or ii == self.width - rightX -1:
                    row.append("w")
                elif ii > leftX or ii < self.width - rightX -1:


                    if i == self.height - 2:
                        row.append("w")


                    else:
                        if row[ii-1] == "w" and self.roomShape[i-1][ii-1] == "b":
                            row.append("w")

                        else:
                            if self.roomShape[i - 1][ii + 1] == "b":

                                if ii < oldLeftX   and ii > leftX:
                                    row.append("w")
                                elif self.roomShape[i-1][ii + 1] == "b":
                                    row.append("w")
                                else:
                                    row.append("f")



                            else:
                                row.append("f")


            oldLeftX = leftX
            if self.shape != "square":

                if self.shape == "round":
                    leftX, rightX = self.roundShape(leftX, rightX, i)
                elif self.shape == "labyrinth":
                    leftX, rightX = laby.shape(i)
                elif self.shape == "junction":
                    leftX, rightX = junct.shape(i)
            self.roomShape.append(row)



    def corridor(self, vertexs, roomGap):
        self.roomType = "corridor"
        dirrections = list(vertexs.keys())

        startPoint = vertexs[dirrections[0]]
        endPoint = vertexs[dirrections[1]]


        if "top" in dirrections or "bottom" in dirrections:
            xAdd = 4
            yAdd = 0
            self.roomPosition = (self.roomPosition[0] - 2, self.roomPosition[1] + 1)
            startX = vertexs["bottom"][0] - self.roomPosition[0] - 1
            finalX = vertexs["top"][0] - self.roomPosition[0] - 1
            #from now we dont care about the y of th door as we only ever use the x from colisision


        elif "left" in dirrections or "right" in dirrections:
            yAdd = 7
            xAdd = 0
            self.roomPosition = (self.roomPosition[0] + 1, self.roomPosition[1] - 2)

            startY = vertexs["right"][1] - self.roomPosition[1]
            finalY = vertexs["left"][1]  - self.roomPosition[1]
            # from now we dont care about the x of th door as we only ever use the y from colisision

        self.width = max(startPoint[0], endPoint[0]) - self.roomPosition[0] + xAdd
        self.height = max(startPoint[1], endPoint[1]) - self.roomPosition[1] + yAdd
        self.roomShape = []

        if "top" in dirrections or "bottom" in dirrections:
            self.doors["top"] = (startX + 2, 0)
            self.doors["bottom"] = (finalX + 1, self.height)


        elif "left" in dirrections or "right" in dirrections:
            self.doors["left"] = (0, startY)
            self.doors["right"] = (self.width, finalY)


        #we create a cut out to check in case there are any so we can check for any colision
        cutOut = []
        #here we use the offsets to move back the cutout to inclued the starting point door and then using the other offset
        #we can tell if we need to increase the size by two as the only possibliets for the ofste is -1 or 0
        #if the offset is 0 it wil have no effect when mutiplied but if it isnt it will increase by 2

        remberPoints = {}

        if xAdd == 4:
            #caluations needed to adjust for a left or right turn
            if startX > finalX:
                startXAdd = 3
                finalXAdd = 0
            else:
                startXAdd = 0
                finalXAdd = 3

            #mid point where  the corrior turn to meet next door
            if self.height <= 6:
                midPoint = int(self.height / 2) - 1
            else:
                midPoint = random.randrange(3, self.height-4)

        elif yAdd == 7:
            #finds which wall the gap needs to be put in
            if self.width <= 6:
                midPoint = int(self.width / 2) - 1
            else:
                midPoint = random.randrange(3, self.width - 2)



        #creation of the roomshape array

        for y in range(self.height):
            row = []
            if xAdd == 4:
                #some of these do not need to be placed when the corridor is straight
                if y == midPoint - 2 and startX != finalX:
                    for newX in range(min(startX + finalXAdd, finalX), max(startX, finalX + finalXAdd + 1)):
                        remberPoints[newX] = "w"
                elif y >= midPoint - 1 and y <=  midPoint + 2:
                    remberPoints[startX + startXAdd] = "w"
                    remberPoints[finalX + finalXAdd] = "w"
                    for newX in range(min(startX + 1, finalX + 1), max(startX + startXAdd, finalX + finalXAdd)):

                        remberPoints[newX] = "f"

                elif y == midPoint + 3 and startX != finalX:
                    for newX in range(min(startX, finalX + startXAdd), max(startX + startXAdd, finalX)):
                        remberPoints[newX] = "w"
            elif yAdd == 7:

                if y == startY - 1:

                    for newX in range(midPoint - 1):

                        remberPoints[newX] = "w"


                if y == startY + 4:

                    for newX in range(midPoint - 1):
                        remberPoints[newX] = "w"

                if y == finalY - 1:
                    for newX in range(midPoint + 1, self.width):
                        remberPoints[newX] = "w"
                if y == finalY + 4:
                    for newX in range(midPoint + 1, self.width):
                        remberPoints[newX] = "w"

                if (y >= startY and y < startY + 4):
                    for newX in range(midPoint - 1):
                        remberPoints[newX] = "f"



                if (y >= finalY and y < finalY + 4):
                    for newX in range(midPoint + 1, self.width):
                        remberPoints[newX] = "f"



            for x in range(self.width):
                #xAdd is only 4 when it is top to bottom situation

                if x in remberPoints:
                    row.append(remberPoints[x])
                    remberPoints.pop(x)
                elif xAdd == 4:

                    if y <= midPoint - 2 and x == startX:
                        row.append("w")
                        remberPoints[x + 1] = "f"
                        remberPoints[x + 2] = "f"
                        remberPoints[x + 3] = "w"
                    elif y >= midPoint + 3 and x == finalX:
                        row.append("w")
                        remberPoints[x + 1] = "f"
                        remberPoints[x + 2] = "f"
                        remberPoints[x + 3] = "w"

                    else:
                        row.append("b")
                elif yAdd == 7:
                    if x == midPoint - 1 or midPoint == x:
                        if y == 1 or y == self.height-3:
                            row.append("w")
                        elif y > 1 and y < self.height-3:
                            row.append("f")
                        else:
                            row.append("b")
                    elif (x == midPoint - 2 and "w" not in row and "f" not in row) and (y >= 1 and y <= self.height-3):
                        row.append("w")
                    elif (x == midPoint + 1 and len(remberPoints) == 0) and (y >= 1 and y <= self.height-3):
                        row.append("w")
                    else:
                        row.append("b")
                else:
                    row.append("b")

            self.roomShape.append(row)


        self.roomPosition = ((self.roomPosition[0] + roomGap) * TILESIZE, (self.roomPosition[1] + roomGap) * TILESIZE)



    def addSideWalls(self):
        y = 0
        for i in self.roomShape:
            x = 0

            for ii in i:

                if ii == "f" and y>1:
                    if self.roomShape[y-1][x] == "w" or  self.roomShape[y-2][x] == "w":
                        self.roomShape[y][x] = "s"
                x += 1
            y += 1

    def getYAsRow(self, x):
        row = []
        for i in range(self.height):
            row.append(self.roomShape[i][x])
        return row


    def randomMid(self, row, xOrY):
        count = 0
        minX = 0
        maxX = 0

        lowerLimit = 3
        upperLimit = 3



        if xOrY == "y":
            lowerLimit = 2
            upperLimit = 4

        for i in row:

            if minX == 0 and i == "w":
                minX = count
            elif (minX > 0 and maxX == 0) and i == "b":
                maxX = count
            count += 1

        #returns valid mid point if random is not valid
        if minX + 6 >= maxX:
            if xOrY == "x":

                return int(self.width / 2)

            elif xOrY == "y":

                return int(self.height / 2)
        else:

            return random.randrange(minX + lowerLimit, (maxX - upperLimit))


    def addDoors(self, doors):
        print(doors)
        if "top" in doors:
            row = 1
            midx = self.randomMid(self.roomShape[row], "x")
            for localY in range(2):

                self.roomShape[localY][midx] = "f"
                self.roomShape[localY][midx + 1] = "f"
                if localY == 0:
                    self.roomShape[localY][midx - 1] = "w"
                    self.roomShape[localY][midx + 2] = "w"
            self.doors["top"] = (midx, 0)

        if "bottom" in doors:
            row = self.height - 1
            midx = self.randomMid(self.roomShape[row -1], "x")
            for localY in range(2):
                self.roomShape[row - localY][midx] = "f"
                self.roomShape[row - localY][midx + 1] = "f"
                if localY == 0:
                    self.roomShape[row - localY][midx - 1] = "w"
                    self.roomShape[row - localY][midx + 2] = "w"
            self.doors["bottom"] = (midx, row)
        if "left" in doors:
            column = 0
            midy = self.randomMid(self.getYAsRow(column + 1), "y")

            for localX in range(0, 2):

                self.roomShape[midy][localX] = "f"
                self.roomShape[midy + 1][localX] = "f"
                self.roomShape[midy +2][localX] = "f"
                self.roomShape[midy + 3][localX] = "f"
                if localX == 0:
                    self.roomShape[midy - 1][localX] = "w"
                    self.roomShape[midy + 4][localX] = "w"
            self.doors["left"] = (column, midy)


        if "right" in doors:

            column = self.width - 2
            midy = self.randomMid(self.getYAsRow(column), "y")

            for localX in range(2):
                self.roomShape[midy][localX + column] = "f"
                self.roomShape[midy + 1][localX + column] = "f"
                self.roomShape[midy + 2][localX + column] = "f"
                self.roomShape[midy + 3][localX + column] = "f"
                if localX == 1:
                    self.roomShape[midy - 1][localX + column] = "w"
                    self.roomShape[midy + 4][localX + column] = "w"
            self.doors["right"] = (column +1, midy)
    def addWater(self):
        # this will be every "y" index of the room shape list
        for y in range(self.height):
            # this will be every "y" index of the room shape list
            for x in range(self.width):
                #function only continues if the letter at teh current index is a "f" floor tile and is with in the x and y or the room itself
                if self.roomShape[y][x] == "f" and ((y > 3 and y < self.height -2) and (x > 1 and x < self.width -2)):


                        surrondings = []
                        for yAdd in range(-4,3):
                            row = []
                            for xAdd in range(-2,3):

                                row.append(self.roomShape[y + yAdd][x + xAdd])
                            surrondings.append(row)
                        isntDoorway = True

                        count = 0
                        for door, val in self.doors.items():
                            if val != None:
                                if door == "top":
                                    if (val[0] > x - 3 and val[0] < x + 2) and y < self.height/2:
                                        isntDoorway = False

                                elif door == "bottom":
                                    if (val[0] > x - 3 and val[0] < x + 2) and y > self.height/2:
                                        isntDoorway = False

                                elif door == "left":

                                    if (val[1] > y - 5 and val[1] < y) and x < self.width/2:
                                        isntDoorway = False

                                elif door ==  "right":
                                    if (val[1] > y - 5 and val[1] < y) and x > self.width / 2:
                                        isntDoorway = False



                                count += 1



                                    #if (i[1] > x - 3 and i[1] < x + 2) or (i[0] > y - 4 and i[0] < y + 3):
                                        #isntDoorway = False
                        if isntDoorway:
                            for indexY in range(7):
                                rangeJump = 1
                                if indexY > 1 or indexY == 6:
                                    rangeJump = 4

                                validWater = False

                                for indexX in range(0,5, rangeJump):
                                    for i in surrondings:

                                        if surrondings[indexY][indexX] == ("w") and (surrondings[3][2] != "w" and surrondings[2][2] != "w"):
                                            validWater = True

                                if validWater:
                                    self.roomShape[y][x] = "l"










#palette
    def paint(self, palette):
        waterPalette = WATER[palette]
        regPalette = TILES[palette]
        self.palette = palette
        x = 0
        y = 0


        self.roomTiles = []
        checksTiles = []

        for i in self.roomShape:
            row = []
            for ii in range(len(i)):
                row.append("0")
            checksTiles.append(row)
        #firstAll the Tiles that are added
        #then at the end when All the real tiles have been genrated, their positions are removed from the list


        for i in self.roomShape:
            row = []
            last2 = None
            last3 = None
            for ii in i:

                #finds the value of every tile around it
                #if the value is not in index range it is set to b (blank)

                if y > 1:

                    top = self.roomShape[y-1][x]

                else:

                    top = "b"
                if y > 1 and x > 1:
                    topLeft = self.roomShape[y-1][x-1]
                else:
                    topLeft = "b"
                if y > 1 and x < self.width - 1:
                    topRight = self.roomShape[y-1][x+1]
                else:
                    topRight = "b"

                if x > 1:
                    left = self.roomShape[y][x-1]
                else:
                    left = "b"
                if x < self.width - 1:

                    right = self.roomShape[y][x+1]
                else:
                    right = "b"

                if y < self.height - 1:
                    bottom = self.roomShape[y+1][x]
                else:
                    bottom = "b"
                if y < self.height - 1 and x > 1:
                    bottomLeft = self.roomShape[y+1][x-1]
                else:
                    bottomLeft = "b"
                if y < self.height - 1 and x < self.width - 1:
                    bottomRight = self.roomShape[y+1][x+1]
                else:
                    bottomRight = "b"

                surrondings = [topLeft, top, topRight, left, self.roomShape[y][x], right, bottomLeft, bottom, bottomRight]


                #if a tile isnt a floor it could be colidable and theoretically all tiles could be collided with
                #checks if the tile isnt a floor and use a bool to dictacte whether the tile should have a collision
                collidable = surrondings[4] != "f"


                roomOffset = self.roomPosition


                if (surrondings[4] == "w" or surrondings[4] == "b"):
                    if (surrondings[1] == "b" and ((surrondings[7] == "f" or surrondings[7] == "l") or surrondings[7] == "s")):

                        if (surrondings[3] == "w" or surrondings[3] == "b")  and (surrondings[5] == "w" or surrondings[5] == "b"):
                            row.append(Tile(regPalette[4], x, y, roomOffset, collidable))

                        elif surrondings[0] == "w" and (surrondings[5] == "w" or surrondings[8] == "w"):
                            row.append(Tile(regPalette[13], x, y, roomOffset, collidable))

                        elif surrondings[2] == "w" and (surrondings[3] == "w" or surrondings[6] == "w"):
                            row.append(Tile(regPalette[12], x, y, roomOffset, collidable))
                        elif  ((surrondings[3] == "f" or surrondings[3] == "l") or surrondings[3] == "s"):
                            row.append(Tile(regPalette[13], x, y, roomOffset, collidable))
                        elif ((surrondings[5] == "f" or surrondings[5] == "l") or surrondings[5] == "s"):
                            row.append(Tile(regPalette[12], x, y, roomOffset, collidable))

                    # top edges
                    elif (surrondings[1] == "w" and ((surrondings[7] == "f" or surrondings[7] == "l") or surrondings[7] == "s")):


                        if ((surrondings[3] == "f" or surrondings[3] == "l") or surrondings[3] == "s") and ((surrondings[6] == "f" or surrondings[6] == "l") or surrondings[6] == "s"):
                            row.append(Tile(regPalette[13], x, y, roomOffset, collidable))


                        elif (((surrondings[8] == "f" or surrondings[8] == "l") or surrondings[8] == "s") and ((surrondings[5] == "f" or surrondings[5] == "l") or surrondings[5] == "s")):
                            row.append(Tile(regPalette[12], x, y, roomOffset, collidable))

                    #bottom corners
                    elif (surrondings[1] == "w" and surrondings[7] == "b"):

                        if  (surrondings[3] == "b" and surrondings[6] == "b") and (surrondings[5] == "w" and ((surrondings[2] == "f" or surrondings[2] == "l") or surrondings[2] == "s")):
                            row.append(Tile(regPalette[8], x, y, roomOffset, collidable))
                        elif (surrondings[5] == "b" and surrondings[8] == "b") and (surrondings[3] == "w" and ((surrondings[0] == "f" or surrondings[0] == "l") or surrondings[0] == "s")):
                            row.append(Tile(regPalette[15], x, y, roomOffset, collidable))
                        elif surrondings[5] == "b" and (
                                (surrondings[3] == "f" or surrondings[3] == "l") or surrondings[3] == "s"):
                            row.append(Tile(regPalette[9], x, y, roomOffset, collidable))
                        elif surrondings[3] == "b" and ((surrondings[5] == "f" or surrondings[5] == "l") or surrondings[5] == "s"):
                            row.append(Tile(regPalette[5], x, y, roomOffset, collidable))





                        #right edge

                    #side edeges
                    elif surrondings[1] == "w" and (surrondings[7] == "w"):
                        if surrondings[4] == "w":
                            if surrondings[3] == "w" or surrondings[5] == "w":
                                if surrondings[5] == "b":
                                    row.append(Tile(regPalette[31], x, y, roomOffset, collidable))

                                elif surrondings[3] == "b":
                                    row.append(Tile(regPalette[30], x, y, roomOffset, collidable))

                            #right edge
                            elif surrondings[5] == "b":
                                row.append(Tile(regPalette[9], x, y, roomOffset, collidable))
                            #left edge
                            elif surrondings[3] == "b":
                                row.append(Tile(regPalette[5], x, y, roomOffset, collidable))



                    # bottom side edges
                    elif surrondings[1] == "b" and (surrondings[7] == "w"):
                        if surrondings[4] == "w":
                            #right edge
                            if surrondings[5] == "b" and (surrondings[3] == "f" or surrondings[3] == "l"):
                                row.append(Tile(regPalette[9], x, y, roomOffset, collidable))
                            elif surrondings[5] == "b" and surrondings[3] == "w":
                                row.append(Tile(regPalette[14], x, y, roomOffset, collidable))
                            #left edge
                            elif surrondings[3] == "b" and (surrondings[5] == "f" or surrondings[5] == "l"):
                                row.append(Tile(regPalette[5], x, y, roomOffset, collidable))
                            elif surrondings[3] == "b" and surrondings[5] == "w":
                                row.append(Tile(regPalette[2], x, y, roomOffset, collidable))


                        elif surrondings[4] == "b":
                            if (surrondings[0] == "b" and surrondings[3] == "b") and ((surrondings[8] == "f" or surrondings[8] == "l") or surrondings[8] == "s"):
                                row.append(Tile(regPalette[2], x, y, roomOffset, collidable))
                            elif (surrondings[2] == "b" and surrondings[5] == "b") and ((surrondings[6] == "f" or surrondings[6] == "l") or surrondings[6] == "s"):
                                row.append(Tile(regPalette[14], x, y, roomOffset, collidable))


                    #bottomEdges
                    elif ((surrondings[1] == "f" or surrondings[1] == "l") or surrondings[1] == "s") and surrondings[7] == "b":
                        #bottom right
                        if (surrondings[8] == "b" and (surrondings[3] == "f" or surrondings[3] == "l")):
                            row.append(Tile(regPalette[10], x, y, roomOffset, collidable))
                        #bottom left
                        elif  surrondings[6] == "b" and (surrondings[5] == "f" or surrondings[5] == "l"):
                            row.append(Tile(regPalette[11], x, y, roomOffset, collidable))
                        #bottom
                        else:
                            row.append(Tile(regPalette[6], x, y, roomOffset, collidable))
                    #floor above and wall bellow
                    elif ((surrondings[1] == "f" or surrondings[1] == "l") or surrondings[1] == "s") and (surrondings[7] == "w" and surrondings[4] == "w"):

                        if ((surrondings[5] == "f" or surrondings[5] == "l") or surrondings[5] == "s"):
                                row.append(Tile(regPalette[11], x, y, roomOffset, collidable))
                        elif ((surrondings[3] == "f" or surrondings[3] == "l") or surrondings[3] == "s"):
                                row.append(Tile(regPalette[10], x, y, roomOffset, collidable))
                        elif surrondings[8] == "s":
                                row.append(Tile(regPalette[32], x, y, roomOffset, collidable))
                        elif surrondings[6] == "s":
                                row.append(Tile(regPalette[33], x, y, roomOffset, collidable))


                    elif (surrondings[1] == "f" or surrondings[1] == "l"):

                        if surrondings[5] == "f":
                            row.append(Tile(regPalette[0], x, y, roomOffset, collidable))
                        elif surrondings[3] == "f":
                            row.append(Tile(regPalette[7], x, y, roomOffset, collidable))
                        else:
                            row.append(Tile(regPalette[1], x, y, roomOffset, collidable))


                elif surrondings[4] == "s":

                    if surrondings[1] == "w":
                        if ((self.roomShape[y+2][x] == "l" and random.randrange(0,2) == 0) and (checksTiles[y-1][x+1] != "waterWall" and checksTiles[y-1][x-1] != "waterWall")) and  (((self.roomShape[y+2][x+1] == "l"  and self.roomShape[y+2][x-1] == "w") or (self.roomShape[y+2][x+1] == "w"  and self.roomShape[y+2][x-1] == "l")) or (self.roomShape[y+2][x+1] == "l"  and self.roomShape[y+2][x-1] == "l")):
                            row.append(Tile(regPalette[17], x, y, roomOffset, collidable))
                            checksTiles[y - 1][x] = "waterWall"
                        else:
                           valid = False
                           while not valid:
                                wallType = random.randrange(0,5)
                                if wallType <= 2:
                                    row.append(Tile(regPalette[17], x, y, roomOffset, collidable))
                                    checksTiles[y - 1][x] = "regWall"

                                    valid = True
                                elif wallType == 3 and (last2 != x - 1 and last3 != x - 1):
                                    row.append(Tile(regPalette[19], x, y, roomOffset, collidable))
                                    last2 = x
                                    checksTiles[y - 1][x] = "aWall"

                                    valid = True
                                elif wallType == 4 and (last2 != x - 1 and last3 != x - 1):
                                    row.append(Tile(regPalette[21], x, y, roomOffset, collidable))
                                    last3 = x
                                    checksTiles[y - 1][x] = "bWall"

                                    valid = True

                    #checks if bottom of wall
                    elif checksTiles[y-2][x] == "regWall":
                        row.append(Tile(regPalette[18], x, y, roomOffset, collidable))


                    elif checksTiles[y-2][x] == "aWall":
                        row.append(Tile(regPalette[20], x, y, roomOffset, collidable))


                    elif checksTiles[y-2][x] == "bWall":
                        row.append(Tile(regPalette[22], x, y, roomOffset, collidable))

                    elif checksTiles[y-2][x] == "waterWall":
                        row.append(Tile(regPalette[34], x, y, roomOffset, collidable))

                elif surrondings[4] == "f":




                    #places floor tiles down
                    if checksTiles[y][x] == "4":
                        row.append(Tile(regPalette[27], x, y, roomOffset, collidable))

                    elif checksTiles[y][x] == "5":
                        row.append(Tile(regPalette[28], x, y, roomOffset, collidable))

                    elif checksTiles[y][x] == "6":
                        row.append(Tile(regPalette[29], x, y, roomOffset, collidable))

                    else:
                        valid = False
                        while not valid:
                            floorType = random.randrange(0, 20)
                            if floorType <= 14:
                                row.append(Tile(regPalette[23 + random.randrange(0, 2)], x, y, roomOffset, collidable))
                                valid = True
                            elif floorType < 18 and floorType > 14:
                                row.append(Tile(regPalette[25], x, y, roomOffset, collidable))
                                valid = True
                            elif floorType == 19 and (y < self.height - 1 and x < self.width - 1):
                                #checks if large tile can be place

                                if (((self.roomShape[y+1][x+1] == "f" and self.roomShape[y+1][x] == "f") and (self.roomShape[y][x+1] == "f")) and
                                            ((checksTiles[y+1][x+1] == "0" and checksTiles[y+1][x] == "0") and (checksTiles[y][x+1] == "0"))):
                                    row.append(Tile(regPalette[26], x, y, roomOffset, collidable))
                                    checksTiles[y][x+1] = "4"
                                    checksTiles[y + 1][x] = "5"
                                    checksTiles[y + 1][x + 1] = "6"
                                    valid = True


                elif surrondings[4] == "l":

                    if surrondings[1] == "f" and self.roomShape[y -3][x] != "w":
                        if (x > 2 and x < self.width - 3):
                            if surrondings[3] == "f":
                                row.append(Tile(waterPalette[11], x, y, roomOffset, collidable))
                            elif surrondings[5] == "f":
                                row.append(Tile(waterPalette[8], x, y, roomOffset, collidable))
                            else:
                                row.append(Tile(waterPalette[10], x, y, roomOffset, collidable))

                        else:
                            row.append(Tile(waterPalette[10], x, y, roomOffset, collidable))
                    elif surrondings[7] == "f":
                        if x > 2  and x < self.width - 3:
                            if surrondings[3] == "f":
                                row.append(Tile(waterPalette[2], x, y, roomOffset, collidable))
                            elif surrondings[5] == "f":
                                row.append(Tile(waterPalette[5], x, y, roomOffset, collidable))
                            else:
                                row.append(Tile(waterPalette[7], x, y, roomOffset, collidable))
                        else:
                            row.append(Tile(waterPalette[7], x, y, roomOffset, collidable))


                    elif surrondings[3] == "f":
                        row.append(Tile(waterPalette[1], x, y, roomOffset, collidable))
                    elif surrondings[5] == "f":
                        row.append(Tile(waterPalette[4], x, y, roomOffset, collidable))
                    elif y > 4 and (x > 2  and x < self.width - 3):
                            if surrondings[0] == "f":
                                row.append(Tile(waterPalette[0], x, y, roomOffset, collidable))
                            elif surrondings[2] == "f":
                                row.append(Tile(waterPalette[3], x, y, roomOffset, collidable))
                            elif surrondings[6] == "f":
                                row.append(Tile(waterPalette[9], x, y, roomOffset, collidable))
                            elif surrondings[8] == "f":
                                row.append(Tile(waterPalette[6], x, y, roomOffset, collidable))
                            else:
                                row.append(Tile(waterPalette[12], x, y, roomOffset, collidable))



                    else:
                        row.append(Tile(waterPalette[12], x, y, roomOffset, collidable))




                else:
                    row.append(Tile(regPalette[16], x, y, roomOffset, collidable))
                x += 1


            self.roomTiles.append(row)

            y += 1
            x = 0
        self.roomTilesWithPostions = {}
        self.emptyTiles = []
        for y in range(self.height):
            for x in range(self.width):
                self.emptyTiles.append((x,y))

        print(self.emptyTiles)
        for i in self.roomTiles:
            for ii in i:
                self.roomTilesWithPostions[(ii.tablex, ii.tableY)] = ii
                print((ii.tablex, ii.tableY))
                self.emptyTiles.remove((ii.tablex, ii.tableY))





    def createRoomBounds(self):
        # thesese are the coridants where the player has left the room
        self.topBound = self.roomPosition[1]
        self.leftBound = self.roomPosition[0]
        # the width/height is in listLength rather then the tile lenght so we times it by the TILESIZE
        # we add the lentgh of the room to find the right and bottom bound
        self.rightBound = self.roomPosition[0] + (self.width * TILESIZE)
        self.bottomBound = self.roomPosition[1] + (self.height * TILESIZE)
        print(self.roomPosition[1], (self.height * TILESIZE))


    def getLeftBound(self):
        return self.leftBound
    def getRightBound(self):
        return  self.rightBound
    def getTopBound(self):
        return self.topBound
    def getBottomBound(self):
        return self.bottomBound


    def setConnections(self, direction, room):
        self.connections[direction] = room

    def getConnections(self):
        return self.connections

    def getScore(self):
        return self.enemyCage.getScore()


    def setOffset(self, offset):
        self.offset = offset

        for i in self.roomTiles:
            for ii in i:
                ii.setOffset(offset)

        self.enemyCage.setOffset(offset)
        self.pickUps.setScreenOffset(offset)
        self.projectiles.setOffset(offset)
        self.stage.setOffset(offset)
    def getRoomPostion(self):
        return self.roomPosition

    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height

    def getSurroundingTiles(self, position, checkIfBlank):
        tileMapPostionX = (position[0] - self.roomPosition[0]) // TILESIZE
        tileMapPostionY = (position[1] - self.roomPosition[1]) // TILESIZE
        returningTiles = {"left":[],"right":[],"top":[],"bottom":[]}
        extraChecks = []
        for y in range(-1, 2):


            temp = []
            if tileMapPostionY + y >= 0 and tileMapPostionY + y < self.height:
                for x in range(-1, 2):
                    notBlank = True
                    if checkIfBlank:
                        if (tileMapPostionX + x, tileMapPostionY + y) in self.emptyTiles:
                            #when we return none we are basically saying this isnt a valid postion
                            return {"left":["outOfBound"],"right":["outOfBound"],"top":["outOfBound"],"bottom":["outOfBound"]}, None

                    tileMapPostionY= int(tileMapPostionY)
                    tileMapPostionX = int(tileMapPostionX)

                    if (tileMapPostionX + x >= 0 and tileMapPostionX + x < self.width) and notBlank:
                        temp.append(self.roomShape[tileMapPostionY + y][tileMapPostionX + x])
                        position = (tileMapPostionX + x, tileMapPostionY + y)
                        if self.roomShape[tileMapPostionY + y][tileMapPostionX + x] != "f":
                            try:

                                if y == -1:
                                    returningTiles["top"].append(self.roomTilesWithPostions[position].getCollisionRect())
                                if y == 1:
                                    returningTiles["bottom"].append(self.roomTilesWithPostions[position].getCollisionRect())

                                if x == -1:
                                    returningTiles["left"].append(self.roomTilesWithPostions[position].getCollisionRect())
                                if x == 1:
                                    returningTiles["right"].append(self.roomTilesWithPostions[position].getCollisionRect())
                            except:
                                return{"left":["outOfBound"],"right":["outOfBound"],"top":["outOfBound"],"bottom":["outOfBound"]}, None



                    elif tileMapPostionX + x < 0:
                        extraChecks.append("left")

                    elif tileMapPostionX + x >= self.width:
                        extraChecks.append("right")


            elif tileMapPostionY + y < 0:
                extraChecks.append("top")
            elif tileMapPostionY + y >= self.height:
                extraChecks.append("bottom")

        return returningTiles, extraChecks

    def getAllHitBoxes(self):

        return self.enemyCage.getAllHitBoxes() + self.projectiles.getAllHitBoxes()

    def renderRoom(self, screen):
        for i in self.roomTiles:
            for ii in i:
                ii.render(screen)

    def render(self, screen):
        self.renderRoom(screen)
        self.stage.render(screen)
        self.pickUps.render(screen)
        self.enemyCage.render(screen)
        self.projectiles.render(screen)
    def updateProjectiles(self, dt, keys, extras):
        positions = self.projectiles.getAllPostions()
        collisions = []
        for pos in positions:
            surrondings, thowAway = self.getSurroundingTiles(pos, False)
            collisions.append(surrondings)

        self.projectiles.update(dt, extras, collisions)

    def updateEnemies(self, dt, keys, extras):
        positions = self.enemyCage.getAllPostions()
        collisions = []
        for pos in positions:
            surrondings, thowAway = self.getSurroundingTiles(pos, False)
            collisions.append(surrondings)

        self.enemyCage.update(dt, extras, collisions)




    def update(self, dt, keys, extras):
        if self.roomType != "corridor":
            self.updateEnemies(dt, keys, extras)
            self.updateProjectiles(dt, keys, extras)






            self.stage.update(dt, keys, extras)
            drops = self.enemyCage.getDrops() + self.stage.getDrops()

            self.pickUps.update(extras["targetPos"], drops)


    def roomMidPointPos(self):
        #returns midPoint of the room
        return ((self.roomPosition[0] + (self.width * TILESIZE) / 2), (self.roomPosition[1] + (self.height * TILESIZE) / 2))

    def getLetterMap(self):
        return self.roomShape
    def sr(self):
        for i in self.roomShape:
            row = []
            for ii in i:
                if ii == "w":
                    row.append("∎")
                else:
                    row.append(ii)


    def getReturnIfItemsPickedUp(self):
        return self.pickUps.returnIfItemsPickedUp()

    def centreSetPeiceCentral(self, setPeice):
        setPeice.setPos((self.roomPosition[0] + (self.width/2 -1) * TILESIZE, self.roomPosition[1] + (self.height/2 -1) * TILESIZE))
        self.stage.stagePeices.append(setPeice)


    def placeTopDoorSetPeice(self, doorClass):

        self.stage.stagePeices.append(doorClass((self.doors["top"][0] * TILESIZE  + self.roomPosition[0], self.doors["top"][1] * TILESIZE + self.roomPosition[1])))
    def getUiInfo(self):
        pass

    def roomChangeUpdate(self):
        pass

class bossRoom(Room):
    def __init__(self, offset, dungeonScore):
        super().__init__(offset, dungeonScore)
        self.bossCage = BossCage()
    def placeBoss(self, bossList):
        self.placeEnemies(bossList)
        self.bossCage.enemyList.append(self.enemyCage.enemyList.pop(-1))

    def placeBossCentred(self, enemies):
        for enemyClassAndScoreList in enemies:
            self.bossCage.enemyList.insert(-1, enemyClassAndScoreList[0]((self.roomPosition[0] + (
                        self.width / 2 - 1) * TILESIZE, self.roomPosition[1] + (self.height / 2 - 1) * TILESIZE),
                                                                         enemyClassAndScoreList[1], self.roomShape,
                                                                         self.roomPosition))

    def render(self, screen):
        self.renderRoom(screen)
        self.stage.render(screen)
        self.pickUps.render(screen)
        self.enemyCage.render(screen)
        self.bossCage.render(screen)
        self.projectiles.render(screen)
    def setOffset(self, offset):
        super().setOffset(offset)
        self.bossCage.setOffset(offset)

    def update(self, dt, keys, extras):
        super().update(dt, keys, extras)
        if self.roomType != "corridor":
            positions = self.bossCage.getAllPostions()
            collisions = []
            for pos in positions:
                surrondings, thowAway = self.getSurroundingTiles(pos, False)
                collisions.append(surrondings)

            self.bossCage.update(dt, extras, collisions)

    def roomChangeUpdate(self):
        if len(self.bossCage.enemyList) > 0:
            boss = self.bossCage.enemyList[0]
            if boss.health < boss.getMaxHealth() /2:
                boss.health = int(boss.getMaxHealth() / 2)



class ChangingRoom(bossRoom):
    def __init__(self, offset, dungeonScore):
        super().__init__(offset, dungeonScore)
        self.slowPalleteChangeIndex = 0


    def update(self, dt, keys, extras):
        super().update(dt, keys, extras)
        #changes pallete
        if len(self.bossCage.enemyList) > 0:

            if self.bossCage.enemyList[0].getImageSet() != self.palette:
                self.changePalleteSlow(self.bossCage.enemyList[0].getImageSet())
                self.enemyCage.enemyList = self.enemyCage.enemyList[:-2]


            transfers = self.bossCage.enemyList[0].getTransferDict()
            self.bossCage.enemyList[0].resetTransferDict()
            self.pickUps.addItems(transfers["items"])


            for projectile in transfers["projectiles"]:

                #Enemy is a list which contains info on its placement type
                if projectile[1] == "random":
                    self.placeEnemies([projectile[0]])
                elif projectile[1] == "placed":
                    #checks enemy is in room
                    surroundings, throwAway = self.getSurroundingTiles(projectile[2], True)
                    if len(surroundings["left"]) == 0 and len(surroundings["right"]) == 0 and len(
                            surroundings["top"]) == 0 and len(surroundings["bottom"]) == 0:

                        self.projectiles.enemyList = self.projectiles.enemyList + [
                            projectile[0](projectile[2], self.roomShape, self.roomPosition)]
            if self.bossCage.enemyList[0].getImageSet() == self.palette:
                for Enemy in transfers["enemy"]:
                    #Enemy is a list which contains info on its placement type
                    if Enemy[1] == "random":
                        self.placeEnemies([Enemy[0]])
                    elif Enemy[1] == "placed":
                        #checks enemy is in room
                        surroundings, throwAway = self.getSurroundingTiles(Enemy[2], True)

                        if len(surroundings["left"]) == 0 and len(surroundings["right"]) == 0 and len(
                                surroundings["top"]) == 0 and len(surroundings["bottom"]) == 0:

                            self.enemyCage.enemyList = self.enemyCage.enemyList + [
                                Enemy[0](Enemy[2], self.roomShape, self.roomPosition)]


    def changePalleteSlow(self, newPallete):
        #only works without water in room
        if self.palette != newPallete:
            if self.slowPalleteChangeIndex < len(self.roomTilesWithPostions) -3:
                for i in range(3):
                    for i, tileImage in enumerate(TILES[self.palette]):
                        if list(self.roomTilesWithPostions.values())[self.slowPalleteChangeIndex].image == tileImage:
                            list(self.roomTilesWithPostions.values())[self.slowPalleteChangeIndex].image = TILES[newPallete][i]
                            self.slowPalleteChangeIndex += 1
            else:

                for changeIndex in range(4):
                    for i, tileImage in enumerate(TILES[self.palette]):
                        if list(self.roomTilesWithPostions.values())[-changeIndex].image == tileImage:
                            list(self.roomTilesWithPostions.values())[-changeIndex].image = TILES[newPallete][i]
                            self.slowPalleteChangeIndex += 1




                self.palette = newPallete
                self.slowPalleteChangeIndex = 0

    def getUiInfo(self):
        if len(self.bossCage.enemyList) > 0:

            return self.bossCage.enemyList[0].getHealth() /  self.bossCage.enemyList[0].getMaxHealth()


