from Dependencies import VIRTUALWIDTH
from Dependencies import VIRTUALHEIGHT
from Dependencies import TILESIZE
import pygame
import math
class GameCamera():
    def __init__(self, cameraPostion, backGroundOffset):
        self.cameraPostion = (-cameraPostion[0] + backGroundOffset[0], -cameraPostion[1] + backGroundOffset[1])
        self.justMoved = False
        self.backGroundOffset = backGroundOffset
        self.xLagVar = 0
        self.xMoved = False
        self.yLagVar = 0
        self.yMoved = False
        self.cameraLag = (0,0)
        self.ogMaxLag = 60
        self.maxLag = self.ogMaxLag
        self.rollTracking = False

    def __cameraSinEquation(self, value):
        # \sin\left(0.05x\ -\ \frac{50\pi}{100}\right)100\ +\ 100
        # Above is the visulastion of this graph in desmos graphing calculator
        valueForSin = (value * 0.05) - ((math.pi * 25) / 50)
        return int(math.sin(valueForSin) * 50 + 50)


    def smoothCameraPostionUpdate(self, indexXorY, newCameraOffset):

        if self.cameraPostion[indexXorY] - 40 >= -newCameraOffset or self.cameraPostion[indexXorY] + 40 <= -newCameraOffset:

            if indexXorY == 0:

                self.cameraPostion = (self.cameraPostion[0] - (self.cameraPostion[0] + newCameraOffset) // 8, self.cameraPostion[1])

            elif indexXorY == 1:

                self.cameraPostion = (self.cameraPostion[0], self.cameraPostion[1] - (self.cameraPostion[1] + newCameraOffset) // 8)
        else:



            if indexXorY == 0:
                self.cameraPostion = (-newCameraOffset, self.cameraPostion[1])

            elif indexXorY == 1:
                self.cameraPostion = (self.cameraPostion[0], -newCameraOffset)



    def moveCameraDown(self, oldPlayerOffset, newCameraOffset, room, moved):
        #all moveCamera functions work the same way with only the numbers a varibles being use and changed
        #just to fit the axis it trying to move in

        #the camera checks if the new offset is in the greater then the current cameraPostion
        #example when the camera is locked to the top of the screen and the player is moving free of the camera
        #with out the first statement the camera would update to the using the current postion of the player
        #which is higher then when it stopped tracking meaning the camera will jolt up to refocus when it shouldnt as it locked
        #so we check that the new postion will actually be lower then the current postion
        if -newCameraOffset[1] < self.cameraPostion[1]:
            #when the camera is at the edge of the screen so to "not see outside of the room" the camera will lock
            if (-self.cameraPostion[1] + VIRTUALHEIGHT <= room.bottomBound and moved)  or room.roomType == "corridor":
                #newcamerOffset is derived from the player postion where as a offset is negative so we make it minus
                self.smoothCameraPostionUpdate(1, newCameraOffset[1])
                self.yLagVar += 8
                self.yMoved = True
            #not all rooms have every door
            elif room.doors["bottom"] != None:
                #find the location of the the door in terms of true x we only need the axis that it is on
                doorX = (room.doors["bottom"][0] * TILESIZE) + room.roomPosition[0]
                if (doorX - TILESIZE * 2 < oldPlayerOffset[0]  and doorX + TILESIZE * 4 > oldPlayerOffset[0]):
                    if moved:
                        self.smoothCameraPostionUpdate(1, newCameraOffset[1])
                        self.yLagVar += 8
                        self.yMoved = True

                    #when the player is at a door but their camera was locked we correct for this by locating it back
                    #to focus on the player
    def moveCameraLeft(self, oldPlayerOffset, newCameraOffset, room, moved):

        if -newCameraOffset[0] > self.cameraPostion[0]:

            if (-self.cameraPostion[0] >= room.leftBound and moved) or room.roomType == "corridor":

                self.smoothCameraPostionUpdate(0, newCameraOffset[0])
                self.xLagVar -= 8
                self.xMoved = True

            elif room.doors["left"] != None:
                doorY = (room.doors["left"][1] * TILESIZE) + room.roomPosition[1]
                if (doorY - TILESIZE < oldPlayerOffset[1]  and doorY + TILESIZE * 6 > oldPlayerOffset[1]):
                    if moved:
                        self.smoothCameraPostionUpdate(0, newCameraOffset[0])
                        self.xLagVar -= 8
                        self.xMoved = True





    def moveCameraRight(self, oldPlayerOffset, newCameraOffset, room, moved):

        if -newCameraOffset[0] < self.cameraPostion[0]:
            if (-self.cameraPostion[0] + VIRTUALWIDTH <= room.rightBound and moved) or room.roomType == "corridor":

                self.smoothCameraPostionUpdate(0, newCameraOffset[0])
                self.xLagVar += 8
                self.xMoved = True

            elif room.doors["right"] != None:
                doorY = (room.doors["right"][1] * TILESIZE) + room.roomPosition[1]
                if (doorY - TILESIZE < oldPlayerOffset[1]   and doorY + TILESIZE * 6 > oldPlayerOffset[1]):
                    if moved:
                        self.smoothCameraPostionUpdate(0, newCameraOffset[0])
                        self.xLagVar += 8
                        self.xMoved = True








    def moveCameraUp(self, oldPlayerOffset, newCameraOffset, room, moved):

        if -newCameraOffset[1] > self.cameraPostion[1]:

            if  (-self.cameraPostion[1] >= room.topBound and moved)  or room.roomType == "corridor":

                self.smoothCameraPostionUpdate(1, newCameraOffset[1])
                self.yLagVar -= 8
                self.yMoved = True

            elif room.doors["top"] != None:
                doorX = (room.doors["top"][0] * TILESIZE) + room.roomPosition[0]
                if (doorX - TILESIZE * 2 < oldPlayerOffset[0] and doorX + TILESIZE * 4 > oldPlayerOffset[0]):
                    if moved:
                        self.smoothCameraPostionUpdate(1, newCameraOffset[1])
                        self.yLagVar -= 8
                        self.yMoved = True



    def lagCamera(self):

        if not self.xMoved:
            if self.xLagVar > 0:
                self.xLagVar -=2

            if self.xLagVar < 0:
                self.xLagVar += 2

        if self.xLagVar <= self.maxLag and self.xLagVar >= 0:
            self.cameraLag = (self.__cameraSinEquation(self.xLagVar), self.cameraLag[1])
        elif self.xLagVar >= -self.maxLag  and self.xLagVar < 0:
            self.cameraLag = (-self.__cameraSinEquation(self.xLagVar), self.cameraLag[1])
        elif self.xLagVar > self.maxLag:
            self.xLagVar = self.maxLag
        elif self.xLagVar < -self.maxLag:
            self.xLagVar = -self.maxLag

        if not self.yMoved:
            if self.yLagVar > 0:
                self.yLagVar -=2

            if self.yLagVar < 0:
                self.yLagVar += 2

        if self.yLagVar <= self.maxLag and self.yLagVar >= 0:
            self.cameraLag = (self.cameraLag[0], self.__cameraSinEquation(self.yLagVar))
        elif self.yLagVar >= -self.maxLag  and self.yLagVar < 0:
            self.cameraLag = (self.cameraLag[0], -self.__cameraSinEquation(self.yLagVar))
        elif self.yLagVar > self.maxLag:
            self.yLagVar = self.maxLag
        elif self.yLagVar < -self.maxLag:
            self.yLagVar = -self.maxLag

        self.xMoved = False
        self.yMoved = False

    def getOffsetForCamera(self):
        return (self.cameraPostion[0] + self.cameraLag[0], self.cameraPostion[1] + self.cameraLag[1])


    def update(self, dt , playeraMovements, playerOffset, currentroom):


        newCameraOffset = (playerOffset[0] - self.backGroundOffset[0], playerOffset[1] - self.backGroundOffset[1])
        if len(playeraMovements) > 0:

            self.moveCameraUp(playerOffset, newCameraOffset, currentroom, "top" in playeraMovements)

            self.moveCameraDown(playerOffset, newCameraOffset, currentroom, "bottom" in playeraMovements)


            self.moveCameraLeft(playerOffset, newCameraOffset, currentroom, "left" in playeraMovements)

            self.moveCameraRight(playerOffset, newCameraOffset, currentroom, "right" in playeraMovements)
        self.lagCamera()
