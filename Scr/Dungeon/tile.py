import os
import sys

import pygame

path = os.path.abspath("")[:-8]

sys.path.append(path)
#import all the varibles from Dependecies
from Dependencies import TILESIZE
from Dependencies import TILES
class Tile():
    def __init__(self, image, tablex, tabley, offset, collisions):
        self.image = image
        self.tablex = tablex
        self.tableY = tabley
        self.tileOffset = offset

        self.x = (tablex) * TILESIZE + self.tileOffset[0]
        self.y = (tabley) * TILESIZE + self.tileOffset[1]

        self.offset = (0,0)
        if collisions:
            self.collisionRect = pygame.Rect(self.x, self.y, TILESIZE, TILESIZE)

    def getCollisionRect(self):

        return self.collisionRect

    def render(self, screen):
        #renders the tile with its postion plus that off the world offset

        screen.blit(self.image, (self.x + self.offset[0], self.y+ self.offset[1]))
        #try:
            #pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.collisionRect.x + self.offset[0],self.collisionRect.y + self.offset[1], TILESIZE, TILESIZE))
        #except:
            #pass

    def setOffset(self, vectr2):


        self.offset = vectr2
