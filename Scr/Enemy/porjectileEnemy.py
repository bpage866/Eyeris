from enemyBase import LaserEyeBase
from enemyBase import BubbleBase
from Dependencies import LASEREYE
from Dependencies import BUBBLE
class LaserEye(LaserEyeBase):
    def __init__(self, postion, localLetterMap, localRoomPos):
        super().__init__(localLetterMap, localRoomPos, 0,
                 postion, 0, 1, 50, 1, None, LASEREYE,
                 0, 0, LASEREYE.get_width(), LASEREYE.get_height(), 0, 0, LASEREYE.get_width(), LASEREYE.get_height())

class Bubble(BubbleBase):
    def __init__(self, postion, localLetterMap, localRoomPos):
        super().__init__(2, localLetterMap, localRoomPos, 0,
                 postion, 0, 1, 20, 1, None, BUBBLE[0], BUBBLE[1],
                 0, 0, BUBBLE[0].get_width(), BUBBLE[0].get_height(), 0, 0, BUBBLE[0].get_width(), BUBBLE[0].get_height())
