import math
import random

import sys
import os

import pygame.draw

path = os.path.abspath("")


sys.path.append(path)
states =  "\Scr\States\Entity states"
sys.path.append(path + states)


sys.path.append(path + states + "\EnemyStates")

from entity import Entity
from aStarPathFind import aStarPathFind
from aStarPathFind import nodeTileMapWithPostion
from Dependencies import TILESIZE
from stateMachine import EnitiyStateMachine
from stillState import WalkingEnemyStillState
from stillState import BouncingEnemyStillState
from stillState import DeerEnemyStillState
from enemyJumpingState import EnemyJumpingState
from hurtState import LivingHurtState
from enemyAttackingState import TwoLegsAttackingState
from enemyAttackingState import DeerBossAttackingState
from enemyHuntingState import TwoLegsHuntingState
from enemyHuntingState import DeerBossHuntingState
from enemyWalkingState import TwoLegsWalkingState
from enemyWalkingState import DeerBossWalkingState
from enemyTrackingState import TwoLegsTrackingState
from deerBossStates import DeerChangeState
from deerBossStates import LaserEyeState
from deerBossStates import BubbleState
from deerBossStates import DeerEnemyLaserState

class EnemyBase(Entity):

    def __init__(self, localLetterMap, localRoomPos, safeDisatnce, postion, score,  health, speed, knockBack,attackCoolDown, stillImage, collisionX, collisionY, collisionWidth, collisionHeight, hitBoxX, hitBoxY, hitBoxWidth, hitBoxHeight):

        super().__init__(postion, health, speed, knockBack, attackCoolDown, stillImage, collisionX, collisionY, collisionWidth, collisionHeight, hitBoxX, hitBoxY, hitBoxWidth, hitBoxHeight).__init__

        self.scoreVal = score

        self.safeDistance = safeDisatnce

        self.localLetterMap = localLetterMap
        self.localRoomPos = localRoomPos
        #bounds to hold the enemy in its room
        #also could be chnaged to let safe changing between rooms
        #buffer of 1 tile is added
        self.localRoomTopBound = localRoomPos[1] + TILESIZE
        self.localRoomBottomBound = localRoomPos[1] + (len(self.localLetterMap) -1) * TILESIZE
        self.localRoomLeftBound = localRoomPos[0] + TILESIZE
        self.localRoomRightBound = localRoomPos[0] + (len(self.localLetterMap[0]) - 1) * TILESIZE

        self.localRoomRect = pygame.Rect(localRoomPos[0] + TILESIZE, localRoomPos[1] + TILESIZE, (len(localLetterMap[0]) - 2)* TILESIZE, (len(localLetterMap[0]) - 2)* TILESIZE)
        self.tileMapAsNodes = nodeTileMapWithPostion(localLetterMap, localRoomPos, TILESIZE)
        self.trackDistance = 5
        #used in angle calcuation
        self.xScale = -1
        self.yScale = 1
        self.dropHearts = True

    def __calucateAngleBasedOnTarget(self, target):
        feetPostion = self.getCollisionRectCenter()
        yDistanceToTarget = abs(target[0] - feetPostion[0])
        xDistanceToTarget = abs(target[1] - feetPostion[1])
        if yDistanceToTarget == 0:
            # target is directly left or right angle is 0
            angleToTarget = 0

        elif xDistanceToTarget == 0:
            # target is straight up meaning a 90 degree
            angleToTarget = 90
        else:
            angleToTarget = math.atan(yDistanceToTarget / xDistanceToTarget)
        return angleToTarget

    def calucateVectorBasedOnSpeed(self, target, speed):
        angleToTarget = self.__calucateAngleBasedOnTarget(target)
        newX = abs(math.sin(angleToTarget) * speed)
        newY = abs(math.cos(angleToTarget) * speed)

        #cos and sin only goes upto 90 so we must flip the values based on what qudrant were in
        feetPostion = self.getCollisionRectCenter()
        if feetPostion[0] > target[0]:
            xScale = -1

        else:

            xScale = 1

        if feetPostion[1] > target[1]:
            yScale = -1

        else:

            yScale = 1

        return (int(newX) *xScale, int(newY) * yScale)

    def checkInRoom(self):
        centre = self.getCollisionRectCenter()
        #top boundary

        if self.collisionRect.collidepoint((centre[0], self.localRoomTopBound)):

            self.postion = (self.postion[0],   self.localRoomTopBound -
                            self.collisionLocalPos[1])

        elif self.collisionRect.collidepoint((centre[0], self.localRoomBottomBound)):
            self.postion = (self.postion[0], self.localRoomBottomBound- self.collisionRect.height -
                            self.collisionLocalPos[1])

        if self.collisionRect.collidepoint((self.localRoomLeftBound, centre[0])):
            self.postion = (self.localRoomLeftBound - self.collisionLocalPos[0], self.postion[1])
        elif self.collisionRect.collidepoint((self.localRoomRightBound, centre[0])):
            self.postion = (self.localRoomRightBound - self.collisionRect.width - self.collisionLocalPos[0], self.postion[1])

        self.updateRects()
    def checkAllCollisions(self, entityCollisions):
        # if the list is empty it False if the list has anything in its true
        cantDirections = []

        if entityCollisions["left"]:
            if self.leftMovementCollision(entityCollisions["left"]):
                cantDirections.append("left")

        if entityCollisions["right"]:
            if self.rightMovementCollision(entityCollisions["right"]):
                cantDirections.append("right")


        #the enemy sometimes gets stuck on corners so we give them a little push up if thats the case
        if entityCollisions["top"]:
            self.topMovementCollision(entityCollisions["top"])
        else:
            if ("left" in cantDirections or "right" in cantDirections) and entityCollisions["bottom"]:
                self.postion = (self.postion[0], self.postion[1] - 2)

        if entityCollisions["bottom"]:
            self.bottomMovementCollision(entityCollisions["bottom"])
        else:
            if ("left" in cantDirections or "right" in cantDirections) and entityCollisions["top"]:
                self.postion = (self.postion[0], self.postion[1] + 2)

        return cantDirections




    def lookAtTarget(self, target):
        feetPostion = self.getCollisionRectCenter()
        if feetPostion[0] > target[0]:
            self.xScale = -1
            self.directionScale = True
        else:
            self.directionScale = False
            self.xScale = 1

        if feetPostion[1] > target[1]:
            self.yScale = -1

        else:

            self.yScale = 1

    def distanceToTarget(self, target):
        feetPostion = self.getCollisionRectCenter()
        return math.sqrt((feetPostion[0] - target[0]) ** 2 + (feetPostion[1] - target[1]) ** 2)

    def checkForPlayer(self, target):
        distance = self.distanceToTarget(target)

        if distance < self.collisionRect.width * 1.5:
            return "inPersonalSpace"
        elif distance < self.safeDistance:
            return "inRange"

        else:
            return "notInRange"


    def randomLocation(self, width):
        halfWidth = width/2
        enemyX = int(self.getCollisionRectCenter()[0])
        enemyY = int(self.getCollisionRectCenter()[1])
        randomSpot = (random.randrange(enemyX - halfWidth,enemyX + halfWidth), random.randrange(enemyY - halfWidth,enemyY + halfWidth))
        throwAway, goTo = self.canSeePlayer(randomSpot)
        if goTo == self.getCollisionRectCenter():
            goTo = randomSpot
        return goTo
    def followTheFootPrints(self, startPos, target):
        #path finding to the player
        if (target[0] > self.localRoomLeftBound and target[0] < self.localRoomRightBound) and (
                target[1] > self.localRoomTopBound and target[1] < self.localRoomBottomBound):

            nodes = aStarPathFind(startPos, target, self.tileMapAsNodes, self.trackDistance, TILESIZE)
            closestToFurthest = []
            for node in nodes:
                closestToFurthest.append(node.position)

            return closestToFurthest
        else:
            return []


    def canSeePlayer(self, target):

        distance = self.distanceToTarget(target)

        MENUFONT = pygame.font.SysFont(None, 64)
        hypotenuseADD = TILESIZE / 2

        hypotenuse = hypotenuseADD

        #the charcter shouldnt move if the first check fails
        lastValid = self.postion

        while hypotenuse < distance - hypotenuseADD:
            checkPos = self.calucateVectorBasedOnSpeed(target, hypotenuse)

            ogY = self.collisionRect.y   + checkPos[1]
            ogX = self.collisionRect.x + checkPos[0]
            if (ogX > self.localRoomLeftBound and ogX < self.localRoomRightBound) and (ogY > self.localRoomTopBound and ogY < self.localRoomBottomBound):
                y = ((ogY - self.localRoomPos[1]) / TILESIZE)
                x = ((ogX - self.localRoomPos[0]) / TILESIZE)

                if target[1] < self.postion[1]:
                    # round up
                    y = math.ceil(y)
                else:
                    #round down
                    y = math.floor(y)

                if target[0] < self.postion[0]:
                    # round up
                    x = math.ceil(x)
                else:
                    # round down
                    x = math.floor(x)

                y = int(y)
                x = int(x)


                letter = MENUFONT.render(self.localLetterMap[int(y)][int(x)] + str(x) + ","+ str(y), True, (0, 0, 0))

                if self.localLetterMap[y][x] != "f":

                    return False, lastValid
                lastValid = (ogX, ogY)
                hypotenuse += hypotenuseADD
            else:
                #the target is outside of the room so they should stop being tracked
                return False, lastValid
        return True, self.getCollisionRectCenter()

    def getScore(self):
        print(self.scoreVal)
        return self.scoreVal


#meant for enemies with two legsw
class TwoLegEnemyBase(EnemyBase):
    def __init__(self, walkingAnimation, atackingAnimation, hitWhenFrameIs, localLetterMap, localRoomPos, safeDisatnce, postion, score,  health, speed, knockBack, attackCoolDown, stillImage, hurtImage, knockBackResist, collisionX, collisionY, collisionWidth, collisionHeight, hitBoxX, hitBoxY, hitBoxWidth, hitBoxHeight):

        super().__init__(localLetterMap, localRoomPos, safeDisatnce, postion, score,  health, speed, knockBack, attackCoolDown, stillImage, collisionX, collisionY, collisionWidth, collisionHeight, hitBoxX, hitBoxY, hitBoxWidth, hitBoxHeight)

        self.enitiyStateMachine = EnitiyStateMachine({"still": WalkingEnemyStillState(self, self.stillImage),
                                                      "hurt": LivingHurtState(self, hurtImage, knockBackResist)})

        self.enitiyStateMachine.change("still", [self.enitiyStateMachine])

        self.enitiyStateMachine.addState("hunting", TwoLegsHuntingState(self, walkingAnimation))
        self.enitiyStateMachine.addState("walking", TwoLegsWalkingState(self, walkingAnimation))
        self.enitiyStateMachine.addState("tracking", TwoLegsTrackingState(self, walkingAnimation))

        self.enitiyStateMachine.addState("attacking", TwoLegsAttackingState(self, atackingAnimation, hitWhenFrameIs))
class BouncingEnemyBase(EnemyBase):
    def __init__(self, AttackBool, localLetterMap, localRoomPos, safeDisatnce, postion, score,  health, speed, knockBack, attackCoolDown, stillImage, hurtImage, jumpAnimatiom, knockBackResist, collisionX, collisionY, collisionWidth, collisionHeight, hitBoxX, hitBoxY, hitBoxWidth, hitBoxHeight):

        super().__init__(localLetterMap, localRoomPos, safeDisatnce, postion, score,  health, speed, knockBack, attackCoolDown, stillImage, collisionX, collisionY, collisionWidth, collisionHeight, hitBoxX, hitBoxY, hitBoxWidth, hitBoxHeight)

        self.enitiyStateMachine = EnitiyStateMachine({"still": BouncingEnemyStillState(self, self.stillImage),
                                                      "hurt": LivingHurtState(self, hurtImage, knockBackResist)})

        self.enitiyStateMachine.change("still", [self.enitiyStateMachine])

        self.enitiyStateMachine.addState("bouncing", EnemyJumpingState(self, jumpAnimatiom, TILESIZE, AttackBool))

        self.lastperpendicularDisatnce = 0
        self.jumpTimer = 0

    def updateTimers(self, dt):
        super().updateTimers(dt)
        self.jumpTimer += dt / 1000

    def calucateBouncingVector(self, target, speed, startDistance):
        self.postion = (self.postion[0], self.postion[1] + self.lastperpendicularDisatnce)

        linearMovement = self.calucateVectorBasedOnSpeed(target, speed)

        distanceFromStart = startDistance - self.distanceToTarget(target)
        halfDistanceToStart = startDistance/2
        scale = 128 / (halfDistanceToStart ** 2)

        #quadraticEquation to find y, the first bit makes sure that it will not go more then tile high
        perpendicularDisatnce = -(scale * (distanceFromStart ** 2 - startDistance * distanceFromStart))

        print(perpendicularDisatnce)
        self.lastperpendicularDisatnce = perpendicularDisatnce

        return (linearMovement[0],  linearMovement[1] - perpendicularDisatnce)

class DeerBossBase(EnemyBase):
    def __init__(self, glowingAnimationDict, walkingAnimationDict, atackingAnimationDict, hitWhenFrameIs, localLetterMap, localRoomPos, safeDisatnce, postion, score,  health, speed, knockBack, attackCoolDown, stillImage, hurtImage, knockBackResist, collisionX, collisionY, collisionWidth, collisionHeight, hitBoxX, hitBoxY, hitBoxWidth, hitBoxHeight):

        super().__init__(localLetterMap, localRoomPos, safeDisatnce, postion, score,  health, speed, knockBack, attackCoolDown, stillImage["eyeztec"], collisionX, collisionY, collisionWidth, collisionHeight, hitBoxX, hitBoxY, hitBoxWidth, hitBoxHeight)
        self.setChangeTimer = 0
        self.setChangeWhen = 15
        self.imageSet = "sewer"
        self.imageSetKeys = ["eyeztec", "sewer", "sunny", "cave"]
        self.enitiyStateMachine = EnitiyStateMachine({"still": DeerEnemyStillState(self, stillImage),
                                                      "hurt": LivingHurtState(self, hurtImage, knockBackResist)})

        self.enitiyStateMachine.change("still", [self.enitiyStateMachine])


        self.enitiyStateMachine.addState("walking", DeerBossWalkingState(self, walkingAnimationDict))
        self.enitiyStateMachine.addState("hunting", DeerBossHuntingState(self, walkingAnimationDict))
        self.enitiyStateMachine.addState("changeSet", DeerChangeState(self, glowingAnimationDict))

        self.enitiyStateMachine.addState("attacking", DeerBossAttackingState(self, atackingAnimationDict, hitWhenFrameIs))
        self.enitiyStateMachine.addState("LaserAttack",
                                         DeerEnemyLaserState(self, stillImage))
        self.transferDict = {"enemy": [], "items": [], "setPeice": [], "projectiles": []}

    def getTransferDict(self):

        return self.transferDict
    def resetTransferDict(self):
        self.transferDict = {"enemy": [], "items": [], "setPeice":[], "projectiles":[]}

    def updateTimers(self, dt):
        super().updateTimers(dt)
        self.setChangeTimer += dt/1000
    def getImageSet(self):
        return self.imageSet

    def update(self, dt, keys, extras):

        super().update(dt,keys,extras)
        if self.health <= 0:
            self.transferDict["items"].append(self.itemDrop(self.getCollisionRectCenter()))


class LaserEyeBase(EnemyBase):
    def __init__(self, localLetterMap, localRoomPos, safeDisatnce,
                 postion, score, health, speed, knockBack, attackCoolDown, stillImage,
                 collisionX, collisionY, collisionWidth, collisionHeight, hitBoxX, hitBoxY, hitBoxWidth, hitBoxHeight):

        super().__init__(localLetterMap, localRoomPos, safeDisatnce, postion, score, health, speed, knockBack,
                         attackCoolDown, stillImage, collisionX, collisionY, collisionWidth, collisionHeight, hitBoxX,
                         hitBoxY, hitBoxWidth, hitBoxHeight)
        self.dropHearts = False
        self.enitiyStateMachine = EnitiyStateMachine({"still": LaserEyeState(self, stillImage)})

        self.enitiyStateMachine.change("still", [self.enitiyStateMachine])


class BubbleBase(EnemyBase):
    def __init__(self, howManybounces, localLetterMap, localRoomPos, safeDisatnce,
                 postion, score, health, speed, knockBack, attackCoolDown, stillImage, poppedImage,
                 collisionX, collisionY, collisionWidth, collisionHeight, hitBoxX, hitBoxY, hitBoxWidth, hitBoxHeight):

        super().__init__(localLetterMap, localRoomPos, safeDisatnce, postion, score, health, speed, knockBack,
                         attackCoolDown, stillImage, collisionX, collisionY, collisionWidth, collisionHeight, hitBoxX,
                         hitBoxY, hitBoxWidth, hitBoxHeight)
        self.howManybounces = howManybounces
        self.dropHearts = False
        self.enitiyStateMachine = EnitiyStateMachine({"still": BubbleState(self, stillImage), "hurt": LivingHurtState(self, poppedImage, 2)})

        self.enitiyStateMachine.change("still", [self.enitiyStateMachine])