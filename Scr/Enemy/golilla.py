from enemyBase import TwoLegEnemyBase
from Dependencies import GOLILLA

from animator import Animation
class Golilla(TwoLegEnemyBase):
    def __init__(self, postion, score,  localLetterMap, localRoomPos):

        width = GOLILLA[0].get_width()
        height = GOLILLA[0].get_height()
        self.directionAsInt = -1
        super().__init__(Animation(GOLILLA[12:-2], 0.4, True),Animation([GOLILLA[0]] + GOLILLA[1:11],0.4, False), 7, localLetterMap, localRoomPos, 600, postion, score,  4, 3, 25,0.5, GOLILLA[0], GOLILLA[-1], 4, width * 0.25, height * 0.8, width * 0.5, height * 0.2, 0, height/2, width * 0.5,height/2)
