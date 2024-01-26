
import sys
import os

path = os.path.abspath("")[:-8]

sys.path.append(path)
from pickUp import pickUpHeart


class EnemyCage():
    def __init__(self, dungeonScore):
        self.enemyList = []
        self.dungeonScore = dungeonScore
        self.enemeyDrops = []


    def getAllPostions(self):
        lst = []
        for enemy in self.enemyList:
            lst.append(enemy.getCollisionRectCenter())
        return lst
    def setOffset(self, screenOffset):
        for enemy in self.enemyList:
            enemy.setScreenOffset(screenOffset)
    def getAllHitBoxes(self):
        hitBoxes = []
        for enemy in self.enemyList:
            hitBoxes += enemy.getAttacking()
        return hitBoxes

    def render(self, screen):
        for enemy in self.enemyList:
            enemy.render(screen)

    def update(self, dt, extras, collisions):
        self.enemeyDrops = []
        for i, enemy in enumerate(self.enemyList):

            extras["collisions"] = collisions[i]
            enemy.update(dt, None, extras)
            if enemy.getHealth() <= 0:
                self.dungeonScore += enemy.getScore()

                self.enemyList.remove(enemy)
                if 0 == 0 and enemy.dropHearts:
                    self.enemeyDrops.append(pickUpHeart(enemy.getCollisionRectCenter()))

    def getDrops(self):
        return self.enemeyDrops

    def getScore(self):
        return self.dungeonScore


class BossCage(EnemyCage):
    def __init__(self):
        super().__init__(0)

        self.givenItemsChanceToDrop = False
    def update(self, dt, extras, collisions):
        self.enemeyDrops = []
        for i, enemy in enumerate(self.enemyList):

            extras["collisions"] = collisions[i]
            enemy.update(dt, None, extras)
            if enemy.getHealth() <= 0:
                if self.givenItemsChanceToDrop:
                    self.dungeonScore += enemy.getScore()

                    self.enemyList.remove(enemy)
                    if 0 == 0 and enemy.dropHearts:
                        self.enemeyDrops.append(pickUpHeart(enemy.getCollisionRectCenter()))
                else:
                    self.givenItemsChanceToDrop = True