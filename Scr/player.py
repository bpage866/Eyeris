from entity import Entity
from stateMachine import StateMachine
from Dependencies import PLAYER
from Dependencies import DASHATTACKEFFECT
from Dependencies import SWINGATTACKEFFECT

from animator import Animation
import pygame
import os
import sys
path = os.path.abspath("")
path += "\Scr\States\Entity states"

sys.path.append(path)
path += "\PlayerStates"
sys.path.append(path)
from playerRollingState import PlayerRollingState
from playerAttackingState import PlayerSwingAttackingState
from playerAttackingState import PlayerDashAttackingState
from playerWalkingState import PlayerWalkingState
from stillState import PlayerStillState
from hurtState import LivingHurtState
from weaponEffect import WeaponEffect
from stateMachine import EnitiyStateMachine
from Util import TrueFalseTimer
class Player(Entity):
    def __init__(self, postion):
        playerWidth =  PLAYER[0].get_width()
        playerHeight =   PLAYER[0].get_height()
        playerDashAttackSpeed = 0.3
        playerSwingAttackSpeed = 0.3

        super().__init__(postion, 5, 30, 30, 0.2, PLAYER[0], playerWidth * 0.25, playerHeight * 0.8, playerWidth * 0.5, playerHeight * 0.2, playerWidth * -0.25,0,playerWidth * 0.75, playerHeight * 0.7)
        self.enitiyStateMachine = EnitiyStateMachine({"still":PlayerStillState(self, self.stillImage), "walking":PlayerWalkingState(self, Animation(PLAYER[1:9], 0.6, True)), "swingAttacking":PlayerSwingAttackingState(self, Animation(PLAYER[9:15], playerSwingAttackSpeed, False), 0), "dashAttacking":PlayerDashAttackingState(self, Animation(PLAYER[16:21], playerDashAttackSpeed, False), 0), "rolling":PlayerRollingState(self, Animation(PLAYER[22:28], 0.45, False)),"hurt": LivingHurtState(self, PLAYER[28], 1) })
        self.enitiyStateMachine.change("still", [self.enitiyStateMachine])
        self.moveDirections = []
        self.directionAsInt = 1
        self.rollCoolDown = TrueFalseTimer(0.5)
        self.canBlink = False
        self.rolling = False

        self.dungeonToGoTo = None

        #attackCollison

        self.leftHitBox = pygame.Rect(self.postion[0], self.postion[1], playerWidth/2, playerHeight/2)
        self.rightHitBox = pygame.Rect(self.postion[0] + playerWidth/2, self.postion[1], playerWidth / 2, playerHeight / 2)

        self.poweredUpAttack = False
        self.currentWeaponEffect = None
        self.dashAttackEffect = WeaponEffect(Animation(DASHATTACKEFFECT, playerDashAttackSpeed, False))
        self.swingAttackEffect = WeaponEffect(Animation(SWINGATTACKEFFECT, playerSwingAttackSpeed, False))
        self.inventory = []
        self.inventoryIndex = 0
        self.justSwitched = True
        self.flagStrings = []

    def update(self, dt, keys, extras):
        self.dungeonToGoTo = None
        super().update(dt, keys, extras)
        for drop in extras["pickUps"]:
            if drop.pickUpType == "consumable":
                drop.pickUpFunction(self)
            elif drop.pickUpType == "item":
                self.inventory.append(drop)
                drop.pickUpInstantFunction(self)
        for item in self.inventory:
            item.inventoryUpdate(self, dt)
        if keys[pygame.K_LEFT]:
            if not self.justSwitched:
                self.justSwitched = True
                self.inventoryIndex -= 1
                if self.inventoryIndex < 0:
                    self.inventoryIndex = len(self.inventory) -1




        if keys[pygame.K_RIGHT]:

            if not self.justSwitched:
                self.justSwitched = True
                self.inventoryIndex += 1

                if self.inventoryIndex >= len(self.inventory):
                    self.inventoryIndex = 0
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.justSwitched = False
    def getDungeonToGoTo(self):
        return self.dungeonToGoTo
    def getFlagStrings(self):
        return self.flagStrings
    def blockBlinkBool(self):
        return self.rolling or self.canBlink
    def itemCooledDown(self):
        return self.inventory[self.inventoryIndex].coolDownTimer > self.inventory[self.inventoryIndex].coolDown

    def prematureEndCurrentItem(self):
        self.inventory[self.inventoryIndex].lastForTimer = self.inventory[self.inventoryIndex].getCoolDownTime() + 0.1
    def checkItemOverHeat(self):
        #returns the bool value of weather the items last for timer has execced how long it can last for
        #returns true for statement above
        return self.inventory[self.inventoryIndex].lastForTimer > self.inventory[self.inventoryIndex].lastFor
    def getInventoryUIInfo(self):
        inventoryImages = []
        for item in self.inventory:
            if item.coolDownTimer > 0:
                gap = (104  * (item.coolDownTimer / max(item.coolDown,1)))
                inventoryImages.append({"image":item.inventoryImage, "gap":gap, "height": 104 - gap})
            else:
                gap = 104
                inventoryImages.append({"image": item.inventoryImage, "gap": gap, "height": 104 - gap})




        return inventoryImages, self.inventoryIndex
    def updatePlayerPostion(self, keys, playerCollision):
        self.moveDirections = []
        if keys[pygame.K_w]:
            self.postion = (self.postion[0], self.postion[1] - self.speed)
            self.updateRects()
            if not self.topMovementCollision(playerCollision["top"]):
                self.moveDirections.append("top")



        if keys[pygame.K_s]:
            self.postion = (self.postion[0], self.postion[1] + self.speed)
            self.updateRects()
            if not self.bottomMovementCollision(playerCollision["bottom"]):
                self.moveDirections.append("bottom")

        if keys[pygame.K_a]:
            self.postion = (self.postion[0] - self.speed, self.postion[1])
            self.updateRects()
            if not self.leftMovementCollision(playerCollision["left"]):
                self.moveDirections.append("left")

            self.directionScale = True
            self.directionAsInt = -1


        if keys[pygame.K_d]:
            self.postion = (self.postion[0] + self.speed, self.postion[1])
            self.updateRects()

            if not self.rightMovementCollision(playerCollision["right"]):
                self.moveDirections.append("right")

            self.directionScale = False
            self.directionAsInt = 1
    def  rollMovement(self, startSpeed, currentDivision, keys, playerCollision, canMoveVertical):
        self.postion = (self.postion[0] + (startSpeed / currentDivision) * self.directionAsInt *  0.7, self.postion[1])
        self.updateRects()
        if self.directionScale:
            self.moveDirections.append("left")
            self.leftMovementCollision(playerCollision["left"])




        elif not self.directionScale:
            self.moveDirections.append("right")

            self.rightMovementCollision(playerCollision["right"])


        if canMoveVertical:
            if keys[pygame.K_w]:
                self.postion = (self.postion[0], self.postion[1] - self.speed)
                self.updateRects()
                if not self.topMovementCollision(playerCollision["top"]):
                    self.moveDirections.append("top")



            if keys[pygame.K_s]:
                self.postion = (self.postion[0], self.postion[1] + self.speed)
                self.updateRects()
                if not self.bottomMovementCollision(playerCollision["bottom"]):
                    self.moveDirections.append("bottom")


    def setScreenOffset(self, screenOffset):
        super().setScreenOffset(screenOffset)
        if self.currentWeaponEffect != None:
            self.currentWeaponEffect.setScreenOffset(screenOffset)

    def checkCanBlink(self):

        return self.canBlink
    def getMoveDirections(self):

        return self.moveDirections

    def getPlayerPostion(self):

        return (self.postion[0] + self.stillImage.get_width() / 2, self.postion[1] + self.stillImage.get_height() / 2)
    def getRealPlayerPosition(self):
        return self.postion
    def getAttacking(self):
        attack = super().getAttacking()

        if self.currentWeaponEffect != None and len(attack) > 0 and self.poweredUpAttack:
                attack.append([self.currentWeaponEffect.getHitBox(), attack[0][1], attack[0][2]])

                return attack
        else:
            return attack


