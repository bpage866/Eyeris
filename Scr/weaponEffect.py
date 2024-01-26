import pygame

class WeaponEffect():
    def __init__(self, animation):
        self.animation = animation

        self.hitBox = pygame.Rect(0,0,self.animation.currentFrame().get_width(), self.animation.currentFrame().get_height())
        self.width = self.animation.currentFrame().get_width()
        self.height = self.animation.currentFrame().get_height()
        self.screenOffset = (0,0)
        self.directionScale = False

    def setScreenOffset(self, screenOffset):
        self.screenOffset = (self.hitBox.x + screenOffset[0], self.hitBox.y + screenOffset[1])


    def setPosition(self, position):
        self.hitBox.update(position[0],position[1] , self.hitBox.width,self.hitBox.height)

    def setDirectionScale(self, bool):
        self.directionScale = bool

    def getHitBox(self):
        return self.hitBox
    def update(self, dt):
        self.animation.update(dt)
    def endOf(self):
        self.animation.restartAnimation()

    def render(self, screen):



        screen.blit(pygame.transform.flip(self.animation.currentFrame(), self.directionScale, False), self.screenOffset)
