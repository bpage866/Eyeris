from enemyBase import TwoLegEnemyBase
from Dependencies import POKEY

from animator import Animation
class Pokey(TwoLegEnemyBase):
    def __init__(self, postion, score,  localLetterMap, localRoomPos):

        width = POKEY[0].get_width()
        height = POKEY[0].get_height()
        self.directionAsInt = -1
        super().__init__(Animation(POKEY[1:7], 0.4, True),Animation(POKEY[8:-1],0.2, False), 2, localLetterMap, localRoomPos, 600, postion, score,  3, 4, 10,0.5, POKEY[0], POKEY[-1], 4, width * 0.25, height * 0.8, width * 0.5, height * 0.2, 0, 0, width * 0.5, height * 0.8)
