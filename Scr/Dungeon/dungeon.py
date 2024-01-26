import random
import sys
import os
path = os.path.abspath("Scr")
print(path)

sys.path.append(path +  "\Enemy" )
print(path + "\Enemy")
sys.path.append(path +  "\Dungeon" )
print(path + "\Dungeon")



import bowyerwaston
import prims
import room
import pygame

from Dependencies import  TILESIZE

from setPeices import LavaCrystal
from setPeices import Pipe
from setPeices import EyeStand
from setPeices import EyeFrame
from setPeices import Monolith
from setPeices import EyeDoor
from kneyeght  import Kneyeght
from skime import Skime
from pokey import Pokey
from golilla import Golilla
from bunny import Bunny
from boss import DeerBoss
from slime import EyeSlime
from slime import LavaSlime
from slime import SewerSlime
from slime import BunnySlime
from lavaPit import LavaPit

from currentSection import CurrentSection
class BaseDungeon():
    def generateNewDunegon(self, numOfRooms, minRoomScore, maxRoomScore, maxNumEnemiesInRoom, seed):
        self.seed = seed
        random.seed(self.seed)
        validDungeon = False
        if not validDungeon:
            if True:
                self.dungeonOffset = (0,0)
                self.roomSeed = random.random()
                self.numOfRooms = numOfRooms
                self.maxNumEnemies = maxNumEnemiesInRoom
                self.minRoomScore = minRoomScore
                self.maxRoomScore = maxRoomScore
                self.totalPossibleScore = 0
                self.currentDungeonScore = 0


                validRoom = False
                while not validRoom:

                    self.rooms = []
                    self.roomShellPoints = []
                    self.dungeonTableWidth = random.randrange(int(self.numOfRooms / 4), int(self.numOfRooms / 1.5))
                    self.dungeonTableHeight = 0
                    roomsInArray = 0


                    while roomsInArray < self.numOfRooms:

                        self.dungeonTableHeight += 1
                        row = []


                        for x in range(self.dungeonTableWidth):

                            if random.randrange(0,3) == 0 and roomsInArray < self.numOfRooms:

                                self.roomShellPoints.append(bowyerwaston.Vertex(x + 1, self.dungeonTableHeight))
                                roomsInArray += 1
                                row.append("r")

                            elif ("r" not in row and x + 1 == self.dungeonTableWidth):
                                self.roomShellPoints.append(bowyerwaston.Vertex(x + 1, self.dungeonTableHeight))
                                roomsInArray += 1
                                row.append("r")

                            else:
                                row.append("0")


                    triangles = bowyerwaston.triangulate(self.roomShellPoints)


                    connectedPointsAndEdges =  prims.connectPointsAndEdges(self.roomShellPoints, triangles)


                    corridorsEdge, roomPointsAndDoors, validRoom, rejects = prims.primMst(connectedPointsAndEdges)

                    corridorsEdge = prims.addExtraEdges(corridorsEdge, rejects, roomPointsAndDoors, 10)

                    roomPointAndDoorPos = {}
                    roomPostionWithRoom = {}
                    for roomPostion, doors in roomPointsAndDoors.items():
                        #placeRoom doent do anything within this classes but insteaded is overwriten with personal code for
                        #dungeon classes that inherit this class, it is meant to create a room.
                        oneRoom = self.placeRoom((roomPostion.x * self.roomGap  * TILESIZE, roomPostion.y  * self.roomGap * TILESIZE,), doors)

                        #we find each the updated connection for point in the tirgulation graph so we know where to put a door
                        roomPointAndDoorPos[roomPostion] = oneRoom.doors
                        #room is connected with its postion to make them easier to find later in this function.
                        roomPostionWithRoom[roomPostion] = oneRoom

                        self.rooms.append(oneRoom)
                        self.roomSeed = random.random()


                    startRoom = self.rooms[random.randrange(0, len(self.rooms))]


                    self.dungeonPosition = startRoom.validPlayerPostion()
                    self.corridors = []
                    first = 1
                    for edge in  corridorsEdge:
                        first -= 1
                        #creates a "fake vertex" with the direction of the vertex and then the update door postion
                        vertexs = {edge.directionA: roomPointAndDoorPos[edge.vertexA][edge.directionA], edge.directionB: roomPointAndDoorPos[edge.vertexB][edge.directionB]}


                        vertexs[edge.directionA] = (vertexs[edge.directionA][0] + (edge.vertexA.x -1) * self.roomGap,   vertexs[edge.directionA][1] + (edge.vertexA.y -1) * self.roomGap)
                        vertexs[edge.directionB] = (vertexs[edge.directionB][0] + (edge.vertexB.x -1) * self.roomGap, vertexs[edge.directionB][1] + (edge.vertexB.y -1) * self.roomGap)

                        topx = min(vertexs[edge.directionA][0], vertexs[edge.directionB][0])
                        topy =  min(vertexs[edge.directionA][1], vertexs[edge.directionB][1])


                        #creates corroidor at the most left x between both door and the the y between them nearest to the top
                        thisCorridor = room.Room((topx, topy), 0)
                        thisCorridor.corridor(vertexs, self.roomGap)
                        thisCorridor.addSideWalls()
                        thisCorridor.paint(self.pallete)
                        #interconnects the corridors to the rooms
                        thisCorridor.setConnections(edge.directionB, roomPostionWithRoom[edge.vertexA])
                        thisCorridor.setConnections(edge.directionA, roomPostionWithRoom[edge.vertexB])
                        #interconnects the rooms to the corridors
                        roomPostionWithRoom[edge.vertexA].setConnections(edge.directionA, thisCorridor)
                        roomPostionWithRoom[edge.vertexB].setConnections(edge.directionB, thisCorridor)

                        self.rooms.append(thisCorridor)

            else:

                validDungeon = True


        for currentRoom in self.rooms:

            currentRoom.setOffset(self.dungeonOffset)
            currentRoom.createRoomBounds()

        # currentSelection is class for optimisie the rendering the Dungeon and updating the dungeon
        # specialising the update and render logic for if the room is on screen, just off or if the player is in the room
        self.currentDungeonSection = CurrentSection(startRoom)






    def randomEnemiesAndScoreScore(self, possibleEnemiesDict):
        #roomscore betwen minRoomScore and maxRoomScore, that is also a mutiple of 100
        #possibleEnemiesDict is a dict of enemy class itseld (uninitialised) : score

        roomScore = random.randrange(self.minRoomScore,self.maxRoomScore +1, 100)

        tempScore = roomScore
        enemiesList = list(possibleEnemiesDict.keys())
        enemiesListWithScore = []
        while len(enemiesList) >self.maxNumEnemies or tempScore != 0:
            enemy = random.sample(enemiesList, 1)

            score = possibleEnemiesDict[enemy[0]]

            #checks if the room has enough score to fund this type of enemy


            if score <= tempScore:

                enemiesListWithScore.append([enemy[0], score])
                tempScore -= score


        self.totalPossibleScore += (roomScore - tempScore)



        return enemiesListWithScore




    def getAllHitBoxes(self):
        return self.currentDungeonSection.getAllHitBoxes()

    def getCurrentRoomSurroundingTiles(self, position):
        return self.currentDungeonSection.getCurrentRoomSurroundingTiles(position)

    def render(self, screen):
        self.currentDungeonSection.render(screen)




    def update(self, dt, keys, playerPostion, extras):
        self.rightDoorCheck(playerPostion)
        self.leftDoorCheck(playerPostion)
        self.bottomDoorCheck(playerPostion)
        self.topDoorCheck(playerPostion)


        self.currentDungeonSection.update(dt, keys, extras)
        newScore = 0
        for room in self.rooms:
            if room.roomType != "corridor":
                newScore += room.getScore()
        self.currentDungeonScore = newScore






    def setOffset(self, offset):
        self.dungeonOffset = offset
        self.currentDungeonSection.setOffset(offset)
    def setDungeonPosition(self, pos):
        self.dungeonPosition = pos
    def getDungeonPosition(self):
        return self.dungeonPosition

    def getCurrentRoomOffset(self):
        currentRoom = self.getCurrentRoom()

        return currentRoom.getRoomPostion()

    def getUiInfo(self):
        return self.currentDungeonSection.getUiInfo()

    def leftDoorCheck(self, postion):
        self.currentDungeonSection.leftDoorCheck(postion)
    def rightDoorCheck(self, postion):
        self.currentDungeonSection.rightDoorCheck(postion)
    def topDoorCheck(self, postion):
        self.currentDungeonSection.topDoorCheck(postion)

    def bottomDoorCheck(self, postion):
        self.currentDungeonSection.bottomDoorCheck(postion)
    def roomChangeUpdate(self):
        self.currentDungeonSection.roomChangeUpdate()

    def getCurrentRoom(self):
        return self.currentDungeonSection.currentRoom

    def getCurrentRoomLetterMap(self):
        currentRoom = self.getCurrentRoom()
        return currentRoom.getLetterMap()

    def getReturnIfItemsPickedUp(self):
        return self.currentDungeonSection.getReturnIfItemsPickedUp()

class BossRoom(BaseDungeon):
    def __init__(self, sacredOrder):
        self.pallete = "eyeztec"
        self.sacredOrder = sacredOrder

        self.generateNewDunegon()


    def placeBossRoom(self, postion, doors):
        thisRoom = room.ChangingRoom(postion, self.currentDungeonScore)
        thisRoom.setSeed(self.roomSeed)
        thisRoom.genrateRoomShape("square", doors, 24, 25)
        thisRoom.addDoors(doors)
        thisRoom.addSideWalls()
        thisRoom.paint(self.pallete)

        thisRoom.placeBossCentred(self.randomEnemiesAndScoreScore({DeerBoss: 1000}))
        thisRoom.placeTopDoorSetPeice(EyeDoor)


        return thisRoom
    def placeMonolithRoom(self, postion, doors):
        thisRoom = room.Room(postion, self.currentDungeonScore)
        thisRoom.setSeed(self.roomSeed)
        thisRoom.genrateRoomShape("square", doors, 14,15)
        thisRoom.addDoors(doors)
        thisRoom.addSideWalls()
        thisRoom.paint(self.pallete)
        thisRoom.centreSetPeiceCentral(Monolith((0,0), self.sacredOrder))

        return thisRoom


    def generateNewDunegon(self):

        random.seed(1)

        self.dungeonOffset = (0, 0)
        self.roomSeed = random.random()
        self.numOfRooms = 2
        self.maxNumEnemies = 1
        self.minRoomScore = 1000
        self.maxRoomScore = 1000
        self.totalPossibleScore = 1000
        self.currentDungeonScore = 0




        self.rooms = []
        self.roomShellPoints = []
        self.dungeonTableWidth = 1
        self.dungeonTableHeight = 2

        roomGap = 42

        self.roomShellPoints = []
        self.roomShellPoints.append(bowyerwaston.Vertex(0, 0))
        self.roomShellPoints.append(bowyerwaston.Vertex(0, 1))


        roomPointsAndDoors = {self.roomShellPoints[0]:["bottom"], self.roomShellPoints[1]:["top"]}
        corridorsEdge= {prims.EdgeV2(prims.Edge(self.roomShellPoints[0], self.roomShellPoints[1]), "bottom", "top"): (0, 0, 0)}
        roomPointAndDoorPos = {}
        roomPostionWithRoom = {}
        cnt = 0
        for roomPostion, doors in roomPointsAndDoors.items():
                        # placeRoom doent do anything within this classes but insteaded is overwriten with personal code for
                        # dungeon classes that inherit this class, it is meant to create a room.
            if cnt == 1:
                oneRoom = self.placeBossRoom(
                                (roomPostion.x * roomGap * TILESIZE, roomPostion.y * roomGap * TILESIZE,), doors)
            else:
                oneRoom = self.placeMonolithRoom(
                    (roomPostion.x * roomGap * TILESIZE, roomPostion.y * roomGap * TILESIZE,), doors)
            cnt += 1


                        # we find each the updated connection for point in the tirgulation graph so we know where to put a door
            roomPointAndDoorPos[roomPostion] = oneRoom.doors
                        # room is connected with its postion to make them easier to find later in this function.
            roomPostionWithRoom[roomPostion] = oneRoom

            self.rooms.append(oneRoom)
            self.roomSeed = random.random()

        startRoom = self.rooms[1]


        self.dungeonPosition = startRoom.validPlayerPostion()
        self.corridors = []
        first = 1

        for edge in corridorsEdge:

            first -= 1
            # creates a "fake vertex" with the direction of the vertex and then the update door postion
            vertexs = {edge.directionA: roomPointAndDoorPos[edge.vertexA][edge.directionA],
                                   edge.directionB: roomPointAndDoorPos[edge.vertexB][edge.directionB]}

            vertexs[edge.directionA] = (vertexs[edge.directionA][0] + (edge.vertexA.x - 1) * roomGap,
                                                    vertexs[edge.directionA][1] + (edge.vertexA.y - 1) * roomGap)
            vertexs[edge.directionB] = (vertexs[edge.directionB][0] + (edge.vertexB.x - 1) * roomGap,
                                                    vertexs[edge.directionB][1] + (edge.vertexB.y - 1) * roomGap)

            topx = min(vertexs[edge.directionA][0], vertexs[edge.directionB][0])
            topy = min(vertexs[edge.directionA][1], vertexs[edge.directionB][1])

            # creates corroidor at the most left x between both door and the the y between them nearest to the top
            thisCorridor = room.Room((topx, topy), 0)
            thisCorridor.corridor(vertexs, 42)
            thisCorridor.addSideWalls()
            thisCorridor.paint(self.pallete)
            # interconnects the corridors to the rooms
            thisCorridor.setConnections(edge.directionB, roomPostionWithRoom[edge.vertexA])
            thisCorridor.setConnections(edge.directionA, roomPostionWithRoom[edge.vertexB])
                        # interconnects the rooms to the corridors
            roomPostionWithRoom[edge.vertexA].setConnections(edge.directionA, thisCorridor)
            roomPostionWithRoom[edge.vertexB].setConnections(edge.directionB, thisCorridor)


            self.rooms.append(thisCorridor)



        for currentRoom in self.rooms:
            currentRoom.setOffset(self.dungeonOffset)
            currentRoom.createRoomBounds()

        # currentSelection is class for optimisie the rendering the Dungeon and updating the dungeon
        # specialising the update and render logic for if the room is on screen, just off or if the player is in the room
        self.currentDungeonSection = CurrentSection(startRoom)




class chestDungeonBase(BaseDungeon):
    #class only used as parent
    def generateNewDunegon(self, numOfRooms, minRoomScore, maxRoomScore, maxNumEnemiesInRoom, seed, chest):
        self.chest = chest

        super().generateNewDunegon(numOfRooms, minRoomScore, maxRoomScore, maxNumEnemiesInRoom, seed)

    def placeChest(self, visted):
        valid = False
        while not valid:
            chestRoom = self.rooms[random.randrange(0, len(self.rooms))]
            #only places a chest in a regular room
            if chestRoom.roomType != "corridor" and chestRoom not in visted:
                chestRoom.placeInitializedSetPiece(self.chest)
                valid = True

                self.dungeonPosition = chestRoom.roomMidPointPos()
                self.currentDungeonSection = CurrentSection(chestRoom)



    def update(self, dt, keys, playerPostion, extras):
        super().update(dt, keys, playerPostion, extras)
        #method is created in child class
        self.checkIfChestOpen()


class EyeztecDungeon(chestDungeonBase):
    def __init__(self,  numOfRooms, minRoomScore, maxRoomScore, maxNumEnemiesInRoom, seed, chest):
        self.pallete = "eyeztec"
        self.roomGap = 36

        self.generateNewDunegon(numOfRooms, minRoomScore, maxRoomScore, maxNumEnemiesInRoom, seed, chest)

        self.redTaken = False
        self.greenTaken = False
        self.orangeTaken = False
        self.blueTaken = False
        self.purpleTaken = False
        self.yellowTaken = False


        self.eyeStands = {"green": EyeStand((0,0), self.greenTaken, 0), "red": EyeStand((0,0), self.redTaken, 1), "orange": EyeStand((0,0), self.orangeTaken, 2), "blue": EyeStand((0,0), self.blueTaken, 3), "purple": EyeStand((0,0), self.purpleTaken, 4), "yellow": EyeStand((0,0), self.yellowTaken, 5)}
        self.eyeFrame = EyeFrame((0,0), self.greenTaken, self.redTaken, self.orangeTaken, self.blueTaken, self.purpleTaken, self.yellowTaken)
        vistedRooms = []
        valid = False
        while not valid:
            room = self.rooms[random.randrange(0, len(self.rooms))]
            # only places  in a regular room
            if room.roomType != "corridor" and room not in vistedRooms:
                room.placeInitializedSetPiece(self.eyeFrame)
                valid = True
                vistedRooms.append(room)



        for stand in self.eyeStands.values():

            valid = False
            while not valid:
                room = self.rooms[random.randrange(0, len(self.rooms))]
                # only places a pipes in a regular room
                if room.roomType != "corridor" and room not in vistedRooms:
                    room.placeInitializedSetPiece(stand)
                    valid = True
                    vistedRooms.append(room)
        self.placeChest(vistedRooms)

    def update(self, dt, keys, playerPostion, extras):
        super().update( dt, keys, playerPostion, extras)
        self.redTaken = self.eyeStands["red"].taken
        self.greenTaken = self.eyeStands["green"].taken
        self.orangeTaken = self.eyeStands["orange"].taken
        self.blueTaken = self.eyeStands["blue"].taken
        self.purpleTaken = self.eyeStands["purple"].taken
        self.yellowTaken = self.eyeStands["yellow"].taken



    def checkIfChestOpen(self):

        self.eyeFrame.updateLinked(self.greenTaken, self.redTaken, self.orangeTaken, self.blueTaken, self.purpleTaken, self.yellowTaken)
        self.chest.updateText(0, int(not self.eyeFrame.redEye) + int(not self.eyeFrame.greenEye) + int(not self.eyeFrame.orangeEye) + int(not self.eyeFrame.blueEye) + int(not self.eyeFrame.purpleEye) + int(not self.eyeFrame.yellowEye))

        self.chest.setInteractable(self.eyeFrame.checkIfAllEyes())
        self.chest.setInteractable(True)
    def placeRoom(self, postion, doors):

        thisRoom = room.Room(postion, self.currentDungeonScore)
        thisRoom.setSeed(self.roomSeed)
        thisRoom.genrateRoomShape("labyrinth", doors, 20, 30)
        thisRoom.addDoors(doors)
        thisRoom.addSideWalls()

        thisRoom.paint(self.pallete)
        thisRoom.placeEnemies(self.randomEnemiesAndScoreScore({Pokey: 400, Kneyeght: 200, EyeSlime:100}))

        return thisRoom



class SewerDungeon(chestDungeonBase):
    def __init__(self, numOfRooms, minRoomScore, maxRoomScore, maxNumEnemiesInRoom, seed, chest):
        self.pallete = "sewer"
        self.roomGap = 42

        self.generateNewDunegon(numOfRooms, minRoomScore, maxRoomScore, maxNumEnemiesInRoom, seed, chest)

        # pipes are place in half of the rooms, and a list at the same time for easy checking
        self.pipes = []
        vistedRooms = []
        for i in range(int(numOfRooms/2)):
            temp = Pipe((0, 0))
            self.pipes.append(temp)
            valid = False
            while not valid:
                room = self.rooms[random.randrange(0, len(self.rooms))]
                # only places a pipes in a regular room
                if room.roomType != "corridor" and room not in vistedRooms:
                    room.placeInitializedSetPiece(temp)
                    valid = True
                    vistedRooms.append(room)

        self.placeChest(vistedRooms)
        self.chest.setInteractable(True)

    def placeRoom(self, postion, doors):

        thisRoom = room.Room(postion, self.currentDungeonScore)
        thisRoom.setSeed(self.roomSeed)
        thisRoom.genrateRoomShape("junction", doors, 34, 36)
        thisRoom.addDoors(doors)
        thisRoom.addSideWalls()
        thisRoom.addWater()
        thisRoom.paint(self.pallete)
        thisRoom.placeEnemies(self.randomEnemiesAndScoreScore({Skime:300, SewerSlime: 100}))

        return thisRoom

    def checkIfChestOpen(self):
        allTurned = True
        notTurned = 0
        for pipe in self.pipes:
            # checks all crystals to see if their health is less than or equal to meaning it is broke
            allTurned = (pipe.turned and allTurned)
            notTurned += int(not pipe.turned)

        self.chest.updateText(0, notTurned)
        self.chest.setInteractable(allTurned)
        self.chest.setInteractable(True)
class SunnyDungeon(chestDungeonBase):
    def __init__(self, numOfRooms, minRoomScore, maxRoomScore, maxNumEnemiesInRoom, seed, chest):
        self.pallete = "sunny"
        self.roomGap = 26

        self.generateNewDunegon(numOfRooms, minRoomScore, maxRoomScore, maxNumEnemiesInRoom, seed, chest)



        self.placeChest([])

    def placeRoom(self, postion, doors):
        thisRoom = room.Room(postion, self.currentDungeonScore)
        thisRoom.setSeed(self.roomSeed)
        thisRoom.genrateRoomShape("square", doors, 14, 20)
        thisRoom.addDoors(doors)
        thisRoom.addSideWalls()
        thisRoom.paint(self.pallete)
        thisRoom.placeEnemies(self.randomEnemiesAndScoreScore({BunnySlime: 100, Bunny: 0}))

        return thisRoom

    def checkIfChestOpen(self):
        self.chest.updateText(0, int((self.totalPossibleScore - self.currentDungeonScore) / 100))

        if self.currentDungeonScore == self.totalPossibleScore:
            self.chest.setInteractable(True)
        self.chest.setInteractable(True)




class CaveDungeon(chestDungeonBase):
    def __init__(self, numOfRooms, minRoomScore, maxRoomScore, maxNumEnemiesInRoom, seed, chest):
        self.pallete = "cave"
        self.roomGap = 36

        self.generateNewDunegon(numOfRooms, minRoomScore, maxRoomScore, maxNumEnemiesInRoom, seed, chest)


        #cyrstals are place in half of the rooms, and a list at the same time for easy checking
        self.lavaCrystals = []
        vistedRooms = []
        for i in range(int(self.numOfRooms/2)):
            temp = LavaCrystal((0,0))
            self.lavaCrystals.append(temp)
            valid = False
            while not valid:
                room = self.rooms[random.randrange(0, len(self.rooms))]
                # only places a crystal in a regular room
                if room.roomType != "corridor" and room not in vistedRooms:
                    room.placeInitializedSetPiece(temp)
                    valid = True
                    vistedRooms.append(room)

        self.placeChest(vistedRooms)

    def checkIfChestOpen(self):
        allBroke = True
        notBroke = 0
        for crystal in self.lavaCrystals:
            #checks all crystals to see if their health is less than or equal to meaning it is broke
            allBroke = crystal.getHealth() <= 1
            notBroke += int(crystal.getHealth() > 1)

        self.chest.updateText(0, notBroke)
        self.chest.setInteractable(allBroke)
        self.chest.setInteractable(True)



    def placeRoom(self, postion, doors):
        thisRoom = room.Room(postion, self.currentDungeonScore)
        thisRoom.setSeed(self.roomSeed)
        thisRoom.genrateRoomShape("round", doors, 20, 30)
        thisRoom.addDoors(doors)
        thisRoom.addSideWalls()
        if random.randrange(0, 3) == 2:
            thisRoom.addWater()
        thisRoom.paint(self.pallete)
        thisRoom.placeEnemies(self.randomEnemiesAndScoreScore({Golilla: 500, LavaSlime: 100, LavaPit: 0}))

        return thisRoom



