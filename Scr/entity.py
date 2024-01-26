import pygame
from datetime import datetime
import sys
import os
#uses abspath which fins the path to V1 on the users device so will work for anyone
path = os.path.abspath("")[:-7]

path += "States\Entity states"
sys.path.append(path)


class Entity():
    def __init__(self, postion, health, speed, knockBack, attackCoolDown, stillImage, collisionX, collisionY, collisionWidth, collisionHeight, hitBoxX, hitBoxY, hitBoxWidth, hitBoxHeight):
        #vector2
        self.postion = postion
        #int
        self.health = health
        self.maxHealth = health
        #int
        self.speed = speed

        self.knockBack = knockBack
        #due to the 2.5d prespective the Enitity collision is normaly only as big as there feet

        self.collisionRect = pygame.Rect(collisionX + postion[0],collisionY + postion[1], collisionWidth,collisionHeight)
        self.hurtBox = pygame.Rect(collisionX + postion[0],postion[1] + stillImage.get_height() * 0.25, collisionWidth,stillImage.get_height() * 0.75)
        self.hitBoxY = hitBoxY
        self.hitBox = pygame.Rect(self.postion[0] + hitBoxX, self.postion[1] + hitBoxY, hitBoxWidth, hitBoxHeight)


        #the location of the colisionRect releative to the player
        self.collisionLocalPos = (collisionX, collisionY)
        self.hitBoxLocalPos = (hitBoxX, hitBoxY)

        #pygame image
        self.stillImage = stillImage


        self.directionScale = False

        self.attacking = False
        self.lastAttackTimeStamp = None
        #records each attack with its unqiue timestamp
        self.hurtTimeStamps = []
        self.attackCoolDown = attackCoolDown
        self.attackTimer = 0


    def setScreenOffset(self,screenOffset):
        self.screenOffset = (self.postion[0] + screenOffset[0], self.postion[1] + screenOffset[1])

    def updateRects(self):
        self.collisionRect.update(self.postion[0] + self.collisionLocalPos[0],
                                  self.postion[1] + self.collisionLocalPos[1], self.collisionRect.width,
                                  self.collisionRect.height)
        #hurtBox is just a heightSized collisionRect
        self.hurtBox.update(self.postion[0] + self.collisionLocalPos[0],
                                  self.postion[1] + self.hurtBox.height/3, self.hurtBox.width,
                                  self.hurtBox.height)
        if not self.directionScale:

            self.hitBox.update(self.postion[0] + self.hitBox.width, self.postion[1] + self.hitBoxY,
                       self.hitBox.width,
                       self.hitBox.height)

        if self.directionScale:
            self.hitBox.update(self.postion[0],self.postion[1] + self.hitBoxY,
                       self.hitBox.width,
                       self.hitBox.height)

    def getMaxHealth(self):
        return self.maxHealth

    def getCollisionRectCenter(self):
        return self.collisionRect.center
    def testCollisions(self, testingRect, listOfRects):
        rectsThatCollide = []
        for rect in listOfRects:
            if rect == "outOfBound":
                rectsThatCollide.append(rect)

            elif testingRect.colliderect(rect):
                rectsThatCollide.append(rect)
        return rectsThatCollide

    def leftMovementCollision(self, listOfRects):
        if len(listOfRects) > 0:
            rectsThatCollide = self.testCollisions(self.collisionRect, listOfRects)
            if len(rectsThatCollide) > 0:
                for rect in rectsThatCollide:
                    if rect == "outOfBound":
                        return True
                self.postion = (rectsThatCollide[0].right - self.collisionLocalPos[0], self.postion[1])
                self.updateRects()
                return True
            else:
                return False
        else:
            return False
    def rightMovementCollision(self, listOfRects):
        if len(listOfRects) > 0:
            rectsThatCollide = self.testCollisions(self.collisionRect, listOfRects)
            if len(rectsThatCollide) > 0:
                for rect in rectsThatCollide:
                    if rect == "outOfBound":
                        return True
                self.postion = (rectsThatCollide[0].left - self.collisionRect.width - self.collisionLocalPos[0], self.postion[1])
                self.updateRects()
                return True
            else:
                return False
        else:
            return False

    def topMovementCollision(self, listOfRects):
        if len(listOfRects) > 0:
            rectsThatCollide = self.testCollisions(self.collisionRect, listOfRects)
            if len(rectsThatCollide) > 0:
                for rect in rectsThatCollide:
                    if rect == "outOfBound":
                        return True
                self.postion = (self.postion[0], rectsThatCollide[0].bottom -
                                self.collisionLocalPos[1])
                self.updateRects()
                return True
            else:
                return False
        else:
            return False


    def bottomMovementCollision(self, listOfRects):
        if len(listOfRects) > 0:
            rectsThatCollide = self.testCollisions(self.collisionRect, listOfRects)
            if len(rectsThatCollide) > 0:
                for rect in rectsThatCollide:
                    if rect == "outOfBound":
                        return True
                self.postion = (self.postion[0], rectsThatCollide[0].top - self.collisionRect.height -
                                self.collisionLocalPos[1])
                self.updateRects()
                return True
            else:
                return False

        else:
            return False

    def checkForHurt(self, listOfRects):
        #list is made up as [rect, knockbackpower, timestamp of attack]
        if len(listOfRects) > 0:
            rectsThatCollide = []
            for rect in listOfRects:
            
                if self.hurtBox.colliderect(rect[0]):
                    rectsThatCollide.append(rect)


            if len(rectsThatCollide) > 0:

                fakeReturningKnockBack = -1
                returningKnockBack = 0
                timeStamp = 0
                valid = False
                for knockBack in rectsThatCollide:
                    #takes the attack with the most powerful knock back
                    #chekcks if the attack has already happend
                    if abs(knockBack[1]) > fakeReturningKnockBack and (knockBack[2] not in self.hurtTimeStamps or knockBack[2] == None):
                        valid = True
                        returningKnockBack = knockBack[1]
                        print(knockBack[1])
                        timeStamp = knockBack[2]
                if valid:


                    self.hurtTimeStamps.append(timeStamp)


                    return True, returningKnockBack
                else:
                    return False, None

            else:
                return False, None
        else:
            return False, None

    def getHealth(self):
        return self.health
    def updateTimers(self, dt):
        self.attackTimer += dt / 1000

    def getAttacking(self):
        #as there are mutiple attacks that can be done on a hurt box at one it loops through the list
        if self.attacking:
            if self.directionScale:
                knockBack = self.knockBack * -1
            else:
                knockBack = self.knockBack

            if knockBack > 0 and self.directionScale:
                self.update()
            hTB = self.hitBox.copy()




            return [[hTB, knockBack,self.lastAttackTimeStamp]]
        #if the entity is not attacking an empty list so when it is added to the rest of the hurt boxs nothing is realy added as there is nothing in the list
        else:
            return []
    def render(self, screen):
        self.enitiyStateMachine.render(screen)

        """
        huB = self.hurtBox.copy()

        huB.update(self.screenOffset[0] + huB.x - self.postion[0], self.screenOffset[1],
                   huB.width,
                   huB.height)

        HTB = self.hitBox.copy()
        HTB.update(self.screenOffset[0] + HTB.x - self.postion[0], self.screenOffset[1] + HTB.y - self.postion[1],
                   HTB.width,
                   HTB.height)

        pygame.draw.rect(screen, (233, 44, 100), huB, 3)
        pygame.draw.rect(screen, (100, 222, 100), HTB, 3)"""
    def renderCollision(self, screen):

        pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.collisionLocalPos[0] + self.screenOffset[0], self.collisionLocalPos[1] + self.screenOffset[1], self.collisionRect.width, self.collisionRect.height))

    def renderAttack(self, screen):
        pass


    def update(self, dt, keys, extras):
        self.enitiyStateMachine.update(dt, keys, extras)
        self.updateTimers(dt)




