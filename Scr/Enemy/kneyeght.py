from enemyBase import TwoLegEnemyBase
from Dependencies import KNEYEGHT

from animator import Animation
class Kneyeght(TwoLegEnemyBase):
    def __init__(self, postion, score,  localLetterMap, localRoomPos):

        width = KNEYEGHT[0].get_width()
        height = KNEYEGHT[0].get_height()
        self.directionAsInt = -1
        super().__init__(Animation(KNEYEGHT[7:13], 0.4, True),Animation(KNEYEGHT[1:7], 0.3, False), 2, localLetterMap, localRoomPos, 600, postion, score,  2, 7, 10,0.5, KNEYEGHT[0], KNEYEGHT[0], 1, width * 0.25, height * 0.8, width * 0.5, height * 0.2, 0, 0, width * 0.5, height * 0.8)
