
import sys
import os

sys.path.append(os.path.abspath("") + "\Scr\Dungeon")



from Dependencies import VIRTUALWIDTH
from Dependencies import VIRTUALHEIGHT
from Dependencies import TILESIZE


#this class is basicly what is on and just off the screen, handing the logic and the rendering for increased effiecny
class CurrentSection():
    def __init__(self, currentRoom):
        #the current room has diffrent checks and logic as we need to acount for the player
        self.currentRoom = currentRoom
        #as we dont need to acount for the player we need to do alot less logic for these rooms so we keep them seprate
        #we keep them linked to there direction so we know what room the player is going into.
        self.surrondingRoom = currentRoom.getConnections()
        self.leftBound = currentRoom.getLeftBound()
        self.rightBound = currentRoom.getRightBound()
        self.topBound = currentRoom.getTopBound()
        self.bottomBound = currentRoom.getBottomBound()


    #private function to change to the next room taking the door the has just walked through in the prevoius room
    def __moveRoom(self, direction):
        
        self.currentRoom = self.surrondingRoom[direction]
        self.surrondingRoom = self.currentRoom.getConnections()
        self.leftBound = self.currentRoom.getLeftBound()
        self.rightBound = self.currentRoom.getRightBound()
        self.topBound = self.currentRoom.getTopBound()
        self.bottomBound = self.currentRoom.getBottomBound()



    #when the player passes one of these bounds they are passing the doorway into the next room
    #so we update the current room to be the new room
    #there is a check for each as we only need to check when the players postion is increased
    def leftDoorCheck(self, postion):
        if postion[0] < self.leftBound and self.surrondingRoom["left"] != None:
            self.__moveRoom("left")

    def rightDoorCheck(self, postion):

        if postion[0] > self.rightBound and self.surrondingRoom["right"] != None:
            self.__moveRoom("right")

    def topDoorCheck(self, postion):

        if postion[1] < self.topBound and self.surrondingRoom["top"] != None:
            self.__moveRoom("top")


    def bottomDoorCheck(self, postion):

        if postion[1] > self.bottomBound and self.surrondingRoom["bottom"] != None:
            self.__moveRoom("bottom")
    def roomChangeUpdate(self):
        self.currentRoom.roomChangeUpdate()
    def getCurrentRoomSurroundingTiles(self, position):
        returningRects, otherRooms = self.currentRoom.getSurroundingTiles(position, False)
        self.currentRoom.stage.updateCollisionsWithSetPeices(returningRects, position)

        return returningRects

    def getUiInfo(self):
        return self.currentRoom.getUiInfo()
    def getCurrentRoomLetterMap(self):
        self.currentRoom.getLetterMap()
    def getReturnIfItemsPickedUp(self):
        return self.currentRoom.getReturnIfItemsPickedUp()
    def getAllHitBoxes(self):
        return self.currentRoom.getAllHitBoxes()
    def render(self, screen):


        for room in self.surrondingRoom.values():
            if room != None:
                room.render(screen)
        self.currentRoom.render(screen)
    def setOffset(self, offset):
        self.currentRoom.setOffset(offset)
        for room in self.surrondingRoom.values():
            if room != None:
                room.setOffset(offset)
    def update(self, dt, keys, extras):
        self.currentRoom.update(dt, keys, extras)

        for room in self.surrondingRoom.values():
            if room != None:
                room.update(dt, keys, extras)


















