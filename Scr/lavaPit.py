import sys
import os

import pygame.draw

path = os.path.abspath("")


sys.path.append(path)
states =  "\Scr\States\Entity states"
sys.path.append(path + states)






from entity import Entity
from Dependencies import LAVAPIT
from stateMachine import  EnitiyStateMachine
from animator import Animation
from stillState import lavaPitStillState
from stillState import LavaPitCreateState

class LavaPit(Entity):
    def __init__(self, postion, score, notNeed, notNeededEither):

        super().__init__(postion, 1, 1, 10, 0, LAVAPIT[0], 0, 0, LAVAPIT[0].get_width(), LAVAPIT[0].get_height()
                         , 0, 0, LAVAPIT[0].get_width(), LAVAPIT[0].get_height()/2)
        self.attacking = True
        self.scoreVal = score
        self.enitiyStateMachine = EnitiyStateMachine({"still": lavaPitStillState(self, Animation(LAVAPIT[0:4], 1.5, True)),"create": LavaPitCreateState(self, Animation(LAVAPIT[5:-1], 0.3, False))})


        self.enitiyStateMachine.change("create", [self.enitiyStateMachine])

    def getScore(self):
        return self.scoreVal



