import pygame
import os
import sys
path = os.path.abspath("")
path += "\Scr\States\Entity states"


path += "\PlayerStates"
sys.path.append(path)
from playerBloodDanceState import PlayerBloodDanceState
from Dependencies import PICKUPHEART
from Dependencies import KEY
from Dependencies import BONECHAR
from Dependencies import CONTACTLENSE
from Dependencies import BLOODVILE
from Dependencies import BLOODDANCE
from Dependencies import KAlEIDOSCOPES
from animator import Animation
from weaponEffect import WeaponEffect
class pickUp():

    def __init__(self, position, displayImage , alphaAdd):
        #as the image is shared we must make a copy of the iamge as its alapha value can be effected
        self.displayImage = displayImage.copy()
        self.position = (position[0] - displayImage.get_width()/2, position[1] - displayImage.get_height()/2)
        self.rectGetAbleRect = pygame.Rect(self.position[0], self.position[1], self.displayImage.get_width() , self.displayImage.get_height() * 2)
        self.pickedUp = False
        self.aplhaValue = 0
        self.aplhaAdd = alphaAdd

    def setScreenOffset(self,screenOffset):
        self.screenOffset = (self.position[0] + screenOffset[0], self.position[1] + screenOffset[1])

    def update(self, playerPos):
        if self.aplhaValue < 255:
            self.aplhaValue += self.aplhaAdd
            if self.aplhaValue >= 255:
                self.aplhaValue = 255
            self.displayImage.set_alpha(self.aplhaValue)

        if self.rectGetAbleRect.collidepoint(playerPos) and self.aplhaValue >= 255:
            self.pickedUp = True
            self.aplhaValue = 255

    def render(self,screen):

        screen.blit(self.displayImage, self.screenOffset)



class consumable(pickUp):
    def __init__(self, position, image, alphaAdd):
        self.pickUpType = "consumable"
        super().__init__(position, image, alphaAdd)


class pickUpHeart(consumable):
    def __init__(self, position):
        super().__init__(position, PICKUPHEART, 40)

    def pickUpFunction(self, entity):
        if entity.health < entity.maxHealth:
            entity.health += 1

class Item(pickUp):
    def __init__(self, position, image, inventoryImage, fallDistance, fallSpeed, alphaAdd):
        self.pickUpType = "item"

        self.inventoryImage = inventoryImage
        self.fallDistance = fallDistance
        self.fallSpeed = fallSpeed
        self.howFarFallen = 0
        self.coolDown = 0
        self.coolDownTimer = 0
        self.lastFor = 0
        self.lastForTimer = 0

        super().__init__(position, image, alphaAdd)
    def update(self, playerPos):
        super().update(playerPos)
        if self.aplhaValue == 255 and self.howFarFallen < self.fallDistance:
            self.position = (self.position[0], self.position[1] + self.fallSpeed)
            self.rectGetAbleRect.y = self.rectGetAbleRect.y + self.fallSpeed
            self.howFarFallen += self.fallSpeed

    def pickUpInstantFunction(self, itemHolder):
        #called when the item is picked up
        pass
    def pickUpFunction(self, itemHolder):
        pass



    def inventoryUpdate(self, itemHolder, dt):
        pass


    def getColdownAndTimer(self):
        return 0,0

    def getCoolDownTime(self):
        return self.coolDown

class BoneChar(Item):
    def __init__(self, postion):
        super().__init__(postion, BONECHAR, BONECHAR, 196, 7, 10)

    def pickUpInstantFunction(self, itemHolder):
        # called when the item is picked up
        itemHolder.poweredUpAttack = True



class Key(Item):
    def __init__(self, postion):
        super().__init__(postion, KEY,KEY, 196, 7, 10)

    def pickUpInstantFunction(self, itemHolder):
            # called when the item is picked up
        itemHolder.flagStrings.append("eyeKey")


class ContactLense(Item):
    def __init__(self, postion):
        super().__init__(postion, CONTACTLENSE,CONTACTLENSE, 196, 7, 10)
        self.coolDown = 24
        self.coolDownTimer = 25
        self.lastFor = 5
        self.lastForTimer = 0

    def pickUpInstantFunction(self, itemHolder):
        #called when the item is picked up
        pass
    def pickUpFunction(self, itemHolder):
        itemHolder.canBlink = True
        self.lastForTimer = 0



    def inventoryUpdate(self, itemHolder, dt):
        #inventoryUpdate is called when it is in the inventory for any update function for the item in the inventory
        dt = dt/1000

        if self.lastFor < self.lastForTimer:
            if itemHolder.canBlink:
                itemHolder.canBlink = False

                self.coolDownTimer = 0
            else:
                self.coolDownTimer += dt

        else:
            self.lastForTimer += dt


class BloodVile(Item):
    def __init__(self, postion):
        super().__init__(postion, BLOODVILE,BLOODVILE, 196, 7, 10)
        self.coolDown = 24
        self.coolDownTimer = 25
        self.lastFor = 5
        self.lastForTimer = 0
        self.using = False

    def pickUpInstantFunction(self, itemHolder):
        #called when the item is picked up
        itemHolder.bloodDanceEffect = WeaponEffect(Animation(BLOODDANCE, 0.4, True))
        itemHolder.enitiyStateMachine.addState("bloodDance", PlayerBloodDanceState(itemHolder))
    def pickUpFunction(self, itemHolder):
        itemHolder.enitiyStateMachine.change("bloodDance", [itemHolder.enitiyStateMachine])
        self.lastForTimer = 0
        self.using = True



    def inventoryUpdate(self, itemHolder, dt):
        #inventoryUpdate is called when it is in the inventory for any update function for the item in the inventory
        dt = dt/1000

        if self.lastFor < self.lastForTimer:
            if self.using:
                self.using = False


                self.coolDownTimer = 0
            else:
                self.coolDownTimer += dt

        else:
            self.lastForTimer += dt

class AllKaleidoscopes(Item):
    def __init__(self, postion):
        super().__init__(postion, KAlEIDOSCOPES[0],KAlEIDOSCOPES[0], 196, 7, 10)
    def pickUpInstantFunction(self, itemHolder):
        #called when the item is picked up
        #the player is given 4 kaleidoscopes each with a diffrent image to represent which dungeon they go to
        #AllKaleidoscopes is just a delivery veichal so it is just deleted after
        itemHolder.inventory.append(Kaleidoscope(KAlEIDOSCOPES[1], "sewer"))
        itemHolder.inventory.append(Kaleidoscope(KAlEIDOSCOPES[2], "eyeztec"))
        itemHolder.inventory.append(Kaleidoscope(KAlEIDOSCOPES[3], "sunny"))
        itemHolder.inventory.append(Kaleidoscope(KAlEIDOSCOPES[4], "cave"))
        itemHolder.inventory.remove(self)


class Kaleidoscope(Item):
    def __init__(self, inventoryImage, dungeonToGoTo):
        super().__init__((0,0), inventoryImage,inventoryImage, 196, 7, 10)
        self.coolDown = 5
        self.coolDownTimer = 6
        self.lastFor = 0
        self.lastForTimer = 0
        self.using = False
        self.dungeonToGoTo = dungeonToGoTo

    def pickUpFunction(self, itemHolder):
        itemHolder.dungeonToGoTo = self.dungeonToGoTo
        self.using = True


    def inventoryUpdate(self, itemHolder, dt):
        #inventoryUpdate is called when it is in the inventory for any update function for the item in the inventory
        dt = dt/1000

        if self.using:
            self.using = False


            self.coolDownTimer = 0
        else:
            self.coolDownTimer += dt







