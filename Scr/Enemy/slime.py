from enemyBase import BouncingEnemyBase
from animator import Animation
from Dependencies import EYESLIME
from Dependencies import BUNNYSLIME
from Dependencies import LAVASLIME
from Dependencies import SEWERSLIME


class SlimeBase(BouncingEnemyBase):
    def __init__(self, images, postion, score, localLetterMap, localRoomPos):
        print(images)
        width = images[0].get_width()
        height = images[0].get_height()
        self.directionAsInt = -1
        super().__init__(True, localLetterMap, localRoomPos, 600, postion, score,  1, 12, 15, 1, images[0], images[-1], Animation(images[1:-2], 0.5, True), 1, 0, height/2, width, height/2, 0, height/2, width/2, height/2)



class EyeSlime(SlimeBase):
    def __init__(self, postion, score, localLetterMap, localRoomPos):
        super().__init__(EYESLIME, postion, score,  localLetterMap, localRoomPos)

class BunnySlime(SlimeBase):
    def __init__(self, postion, score, localLetterMap, localRoomPos):
        super().__init__(BUNNYSLIME, postion, score,  localLetterMap, localRoomPos)

class SewerSlime(SlimeBase):
    def __init__(self, postion, score, localLetterMap, localRoomPos):
        super().__init__(SEWERSLIME, postion, score,  localLetterMap, localRoomPos)

class LavaSlime(SlimeBase):
    def __init__(self, postion, score, localLetterMap, localRoomPos):
        super().__init__(LAVASLIME, postion, score,  localLetterMap, localRoomPos)


