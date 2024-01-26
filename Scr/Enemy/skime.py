from enemyBase import TwoLegEnemyBase
from Dependencies import SKIME

from animator import Animation
class Skime(TwoLegEnemyBase):
    def __init__(self, postion, score,  localLetterMap, localRoomPos):

        width = SKIME[0].get_width()
        height = SKIME[0].get_height()
        self.directionAsInt = -1
        super().__init__(Animation(SKIME[1:8], 0.4, True),Animation(SKIME[9:16], 0.3, False), 2, localLetterMap, localRoomPos, 600, postion, score,  2, 4, 10,0.5, SKIME[0], SKIME[-1], 1, width * 0.25, height * 0.8, width * 0.5, height * 0.2, 0, 0, width * 0.5, height * 0.8)
