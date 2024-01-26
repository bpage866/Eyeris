from enemyBase import DeerBossBase
from slime import BunnySlime
from porjectileEnemy import LaserEye
from porjectileEnemy import Bubble
from Dependencies import DEERBOSS
from pickUp import AllKaleidoscopes
from lavaPit import LavaPit
from animator import Animation
class DeerBoss(DeerBossBase):
    def __init__(self, postion, score,  localLetterMap, localRoomPos):
        self.BunnySlime = BunnySlime
        self.LavaPit = LavaPit
        self.LaserEye = LaserEye
        self.Bubble = Bubble
        self.itemDrop = AllKaleidoscopes

        width = DEERBOSS[0].get_width()
        height = DEERBOSS[0].get_height()
        self.directionAsInt = -1
        #items, enemies, set peices are put in here to be accessed
        #when an enemy is placed into the transfer dict it should be put in a list with its placement type[enemyClass, "random"/"placed", (if targted put the coridinate to place at as the 3rd item]


        super().__init__({"eyeztec":Animation(DEERBOSS[8:11], 0.4, False),"sewer":Animation(DEERBOSS[28:31], 0.4, False),"sunny":Animation(DEERBOSS[48:51], 0.4, False),"cave":Animation(DEERBOSS[68:71], 0.4, False)},{"eyeztec":Animation(DEERBOSS[11:19], 0.4, True),"sewer":Animation(DEERBOSS[31:39], 0.4, True),"sunny":Animation(DEERBOSS[51:59], 0.4, True),"cave":Animation(DEERBOSS[71:79], 0.4, True)},{"eyeztec":Animation([DEERBOSS[0]] + DEERBOSS[1:7],0.4, False), "sewer":Animation([DEERBOSS[20]] + DEERBOSS[21:27],0.4, False),"sunny":Animation([DEERBOSS[40]] + DEERBOSS[41:47],0.4, False),"cave":Animation([DEERBOSS[60]] + DEERBOSS[61:67],0.4, False),}, 7, localLetterMap, localRoomPos, 600, postion, score,  40, 10, 25,0.5, {"eyeztec":DEERBOSS[0], "sewer":DEERBOSS[20], "sunny":DEERBOSS[40], "cave":DEERBOSS[60]}, DEERBOSS[-1], 4, width * 0.25, height * 0.8, width * 0.5, height * 0.2, 0, height/2, width * 0.5,height/2)


