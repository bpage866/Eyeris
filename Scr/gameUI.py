from Dependencies import UI
from Dependencies import PICKUPHEART
from Dependencies import VIRTUALWIDTH
from Dependencies import VIRTUALHEIGHT
import pygame
class GameUI():
    def __init__(self, numOfHearts):
        self.playerHeart = PICKUPHEART
        self.heartGap = self.playerHeart.get_width()
        self.maxNumOfHearts = numOfHearts
        self.numOfHearts = numOfHearts
        self.hotBarItemsDictInList = {}
        self.hotBarIndex = 0
        self.lastHotBarIndex = 0

        self.alphaTakeAway = 0
        self.hotBarWidth = UI["hotBar"][1].get_width()

        self.coolDownOverLay = pygame.Surface((104,0))
        self.coolDownOverLay.set_alpha(51)
        self.coolDownOverLay.fill((51, 51, 51))
        self.coolDownOverLayPos = (0,0)
        self.bossHealthBar = None
        self.bossHealthBarPos = (VIRTUALWIDTH/2  - UI["bossHealthBar"].get_width()/2, VIRTUALHEIGHT - UI["bossHealthBar"].get_height() * 1.5)

    def update(self, numOfHearts, hotBarItemsDict, hotBarIndex, healthBarFraction):
        if healthBarFraction != None:
            self.bossHealthBar = pygame.Rect(self.bossHealthBarPos[0] + 28, self.bossHealthBarPos[1] + 16, 844 * healthBarFraction, 64)
        else:
            self.bossHealthBar = None

        self.numOfHearts = numOfHearts
        self.lastHotBarIndex = self.hotBarIndex
        self.lasthotBarItemslen = len(self.hotBarItemsDictInList)
        self.hotBarItemsDictInList = hotBarItemsDict

        self.hotBarIndex = hotBarIndex
        #when full is perfect Square
        if len(self.hotBarItemsDictInList) > 1:
            if (self.hotBarIndex != self.lastHotBarIndex or self.lasthotBarItemslen != len(self.hotBarItemsDictInList)) :


                UI["hotBar"][0].set_alpha(255)
                UI["hotBar"][1].set_alpha(255)
                for item in self.hotBarItemsDictInList:
                    item["image"].set_alpha(255)
                self.alphaTakeAway = 0
            else:
                self.alphaTakeAway += 1

                UI["hotBar"][0].set_alpha(255 - ((self.alphaTakeAway / 10) ** 4))
                UI["hotBar"][1].set_alpha(255 - ((self.alphaTakeAway / 10) ** 4))
                for item in self.hotBarItemsDictInList:
                    item["image"].set_alpha(255 - ((self.alphaTakeAway / 10) ** 4))




    def render(self, screen):
        for i, item in enumerate(self.hotBarItemsDictInList):

            hotBarPos = ((i * (self.hotBarWidth  -4), 0))
            if i == self.hotBarIndex:
                #the second image in "hotbar" is the selected verision


                screen.blit(UI["hotBar"][1], hotBarPos)

            else:

                screen.blit(UI["hotBar"][0], hotBarPos)
            #a item must be 96 by 96 pixels in size

            screen.blit(item["image"], (hotBarPos[0] + 16, hotBarPos[1] + 16))
            if item["height"] > 0:
                coolDownOverLay = pygame.Surface((104, item["height"]))
                coolDownOverLay.set_alpha((150 * (255 - ((self.alphaTakeAway / 10) ** 4)) / 255))
                coolDownOverLay.fill((50, 50, 50))
                coolDownOverLayPos = (hotBarPos[0] + 12, hotBarPos[1] + 13 + item["gap"])

                screen.blit(coolDownOverLay, coolDownOverLayPos)
        for i in range(self.numOfHearts):
            screen.blit(self.playerHeart, (VIRTUALWIDTH - (i + 1 )* self.heartGap, 0))
        if self.bossHealthBar != None:
            screen.blit(UI["bossHealthBar"], self.bossHealthBarPos)
            pygame.draw.rect(screen, (225, 50, 0), self.bossHealthBar, self.bossHealthBar.width)