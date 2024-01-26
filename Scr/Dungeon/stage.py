import math

class Stage():
    def __init__(self):
        self.stagePeices = []

    def setOffset(self, screenOffset):
        for enemy in self.stagePeices:
            enemy.setScreenOffset(screenOffset)

    def render(self, screen):
        for enemy in self.stagePeices:
            enemy.render(screen)

    def update(self, dt, keys, extras):
        for i, peice in enumerate(self.stagePeices):
            peice.update(dt, keys, extras)

    def getDrops(self):
        returning = []
        for stagePeice in self.stagePeices:
            if stagePeice.setPeiceType == "itemDropper" and stagePeice.shouldDropItem:
                returning.append(stagePeice.dropItem())
        return returning




    def updateCollisionsWithSetPeices(self, collisionsDict, targetPos):
        for setPeice in self.stagePeices:
            yDistance = setPeice.getCollisionRectCenter()[1] - targetPos[1]
            xDistance = setPeice.getCollisionRectCenter()[0] - targetPos[0]

            if yDistance < xDistance:


                if setPeice.getCollisionRectCenter()[1] < targetPos[1]:


                    collisionsDict["top"].append(setPeice.collisionRect)
            return collisionsDict










