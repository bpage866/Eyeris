from enemyBase import BouncingEnemyBase
from animator import Animation
from Dependencies import BUNNY


class Bunny(BouncingEnemyBase):
    def __init__(self, postion, score, localLetterMap, localRoomPos):

        width = BUNNY[0].get_width()
        height = BUNNY[0].get_height()
        self.directionAsInt = -1
        super().__init__(False, localLetterMap, localRoomPos, 0, postion, score,  1, 12, 15, 1, BUNNY[0], BUNNY[-1], Animation(BUNNY[1:-2], 1, True), 1, 0, height/2, width, height/2, 0, height/2, width/2, height/2)
