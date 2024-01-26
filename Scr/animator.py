
class Animation():
    def __init__(self, frames, length, loop):
        self.frames = frames.copy()
        self.wait = length / len(frames)
        self.timer = 0
        self.frame = 0
        self.loop = loop
        self.running = True

    def update(self, dt):


        #checks if there are frames and if the animation is looping
        if len(self.frames) > 0 and self.running:

            #using delta time the time is counted until the time between the wait has passed
            self.timer += dt/1000
            if self.timer > self.wait:

                self.timer = 0



                if self.frame == len(self.frames) - 1:

                    # checks if the animation loops and if not sets looping to false
                    if not self.loop:
                        self.running = False
                    else:
                        self.frame = 0

                else:
                    self.frame = self.frame + 1


                #checks if the last frame in the animation



                    #puts the current frame back to the first one and resets the timer


    def currentFrame(self):
        #frames is the list of framess in the animation and the frame is returned at the index of self.frame is returned
        print(self.frames, "ff", self.frames[self.frame])
        return self.frames[self.frame]
    def currentFrameIndex(self):
        return self.frame

    def lenOfAnimationFrames(self):
        return len(self.frames)
    def restartAnimation(self):
        self.running = True
        self.frame = 0
    def endOfAnimation(self):
        #returns True when running is false
        return not self.running
    def revrseAnimation(self):
        self.frames.reverse()

class puaseAnimation(Animation):
    #makes it so an anatiom holds either until an event or a passage of time, then contiues
    def __init__(self, frames, length, loop, stopAt):
        super().__init__(frames, length, loop)
        self.stopAt  = stopAt
        self.passStopAt = False
    def canPassStopAt(self):
        self.passStopAt = True
    def restartAnimation(self):
        super().restartAnimation()
        self.passStopAt = False
    def update(self, dt):
        #doesnt update when the current frame index is that of the stopAt buit can be passed when it is allowed to pass
        if self.frame != self.stopAt or self.passStopAt:
            super().update(dt)


