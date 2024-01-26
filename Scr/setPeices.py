from entity import Entity
from Dependencies import CHEST
from Dependencies import TEXTFONT
from Dependencies import XBUTTON
from Dependencies import LAVACRYSTAL
from Dependencies import PIPE
from Dependencies import EYEFRAME
from Dependencies import EYEFRAMEEYES
from Dependencies import EYESTANDS
from Dependencies import MONOLITH
from Dependencies import MONOLITHSYMBOLS
from Dependencies import EYEDOOR
from stateMachine import EnitiyStateMachine
from animator import Animation

import os
import sys
import pygame
path = os.path.abspath("")
path += "\Scr\States\Entity states"
sys.path.append(path)
from stillState import ChestStillState
from stillState import LavaCyrstalStillState
from stillState import PipeStillState
from stillState import EyeStandStillTaken
from stillState import EyeStandStillState
from stillState import EyeFrameStillState
from stillState import MonolithStillState
from stillState import EyeDoorStillState
from setPeiceStates import ChestInteractedState
from setPeiceStates import PipeInteractedState
from setPeiceStates import EyeDoorOpenState

class LavaCrystal(Entity):
    def __init__(self, postion):

        super().__init__(postion, 5, None, None, None, LAVACRYSTAL[0], 0, 0, LAVACRYSTAL[0].get_width(), LAVACRYSTAL[0].get_height() * 0.2, 0, 0, 1, 1)
        self.setPeiceType = "painFull"
        self.enitiyStateMachine = EnitiyStateMachine({"still": LavaCyrstalStillState(self, LAVACRYSTAL)})
        self.enitiyStateMachine.change("still", [self.enitiyStateMachine])
    def setPos(self, pos):
        self.postion = pos
        self.updateRects()

class Monolith(Entity):
    def __init__(self, postion, sacredOrder):

        super().__init__(postion, 5, None, None, None, MONOLITH, 0, 0, MONOLITH.get_width(), MONOLITH.get_height() * 0.2, 0, 0, 1, 1)
        self.setPeiceType = "static"
        self.sacredOrder = []
        for item in sacredOrder:
            self.sacredOrder.append(MONOLITHSYMBOLS[item])

        self.enitiyStateMachine = EnitiyStateMachine({"still": MonolithStillState(self, MONOLITH, self.sacredOrder)})
        self.enitiyStateMachine.change("still", [self.enitiyStateMachine])

    def setPos(self, pos):
        self.postion = pos
        self.updateRects()


class movingSetPeice(Entity):

    def __init__(self, postion, interactble, allFrames):
        super().__init__(postion, None, None, None, None, allFrames[0], 0, 0, allFrames[0].get_width(), allFrames[0].get_height()
                         , 0, 0, allFrames[0].get_width(), allFrames[0].get_height() / 2)
        self.setPeiceType = "movingSetPeice"
        self.screenOffset = (0,0)
        self.interactble = interactble
        self.interactbleRect = pygame.Rect(postion[0] - allFrames[0].get_width() * 2 +  allFrames[0].get_width() / 2, postion[1] - allFrames[0].get_height() * 2 +  allFrames[0].get_height() / 2, allFrames[0].get_width() * 4, allFrames[0].get_height() * 4)
        self.targetInZone = False
        self.xButtonAnimation = Animation(XBUTTON, 0.5, True)

    def setPos(self, pos):
        self.postion = pos
        self.updateRects()
        self.interactbleRect.update(pos[0] - self.interactbleRect.width /2 , pos[1] - self.interactbleRect.height/4,self.interactbleRect.width, self.interactbleRect.height)
    def isTargetInInteractZone(self, target):

        if self.interactbleRect.collidepoint(target):
            self.targetInZone = True
        else:
            self.targetInZone = False

    def setInteractable(self, bool):
        self.interactble = bool

    def update(self, dt, keys, extras):
        super().update(dt, keys, extras)
        self.xButtonAnimation.update(dt)

    def renderXButton(self, screen):
        screen.blit(self.xButtonAnimation.currentFrame(), (self.screenOffset[0] - self.xButtonAnimation.currentFrame().get_width()/2 + self.stillImage.get_width()/2, self.screenOffset[1] - self.xButtonAnimation.currentFrame().get_height() * 1.2))

class EyeDoor(movingSetPeice):
    def __init__(self, postion):
        super().__init__(postion, False, EYEDOOR)

        self.enitiyStateMachine = EnitiyStateMachine({"still": EyeDoorStillState(self, EYEDOOR[0]),
                                                      "open": EyeDoorOpenState(self,Animation(EYEDOOR[1:], 2, False))})

        self.enitiyStateMachine.change("still", [self.enitiyStateMachine])



class EyeStand(movingSetPeice):
    def __init__(self, postion, eyeLink, eyeColourIndex):
        super().__init__(postion, True, EYESTANDS)

        self.enitiyStateMachine = EnitiyStateMachine({"still": EyeStandStillState(self, EYESTANDS[eyeColourIndex]),
                                                      "open": EyeStandStillTaken(self,EYESTANDS[-1])})

        self.enitiyStateMachine.change("still", [self.enitiyStateMachine])
        self.taken = eyeLink

class EyeFrame(movingSetPeice):
    def __init__(self, postion, linkedGreenEye, linkedRedEye, linkedOrangeEye, linkedBlueEye, linkedPurpleEye, linkedYellowEye):
        super().__init__(postion, True, EYEFRAME)

        self.enitiyStateMachine = EnitiyStateMachine({"still": EyeFrameStillState(self, EYEFRAME[0])})
        self.enitiyStateMachine.change("still", [self.enitiyStateMachine])

        self.greenEye = False
        self.redEye = False
        self.orangeEye = False
        self.blueEye = False
        self.purpleEye = False
        self.yellowEye = False
        #when deciding on rendering the eyes we check the "colour"Eye for when we should render it
        #however we only want to update the eyes when the player has collected them and also clicks
        #on the eye frame, we can just have a shared vaible for its the eyes pillar is collected,
        #and then just look at that vairble when it turns true and the player clicks on the eye

        self.linkedGreenEye = linkedGreenEye
        self.linkedRedEye = linkedRedEye
        self.linkedOrangeEye = linkedOrangeEye
        self.linkedBlueEye = linkedBlueEye
        self.linkedPurpleEye = linkedPurpleEye
        self.linkedYellowEye = linkedYellowEye


    def updateEyes(self):
        if self.linkedGreenEye:
            self.greenEye = True
        if self.linkedRedEye:
            self.redEye = True
        if self.linkedOrangeEye:
            self.orangeEye = True
        if self.linkedBlueEye:
            self.blueEye = True
        if self.linkedPurpleEye:
            self.purpleEye = True
        if self.linkedYellowEye:
            self.yellowEye = True

    def updateLinked(self, linkedGreenEye, linkedRedEye, linkedOrangeEye, linkedBlueEye, linkedPurpleEye, linkedYellowEye):
        self.linkedGreenEye = linkedGreenEye
        self.linkedRedEye = linkedRedEye
        self.linkedOrangeEye = linkedOrangeEye
        self.linkedBlueEye = linkedBlueEye
        self.linkedPurpleEye = linkedPurpleEye
        self.linkedYellowEye = linkedYellowEye

    def checkIfAllEyes(self):

        return self.redEye and self.greenEye and self.blueEye and self.blueEye and self.purpleEye and self.yellowEye



    def renderEyes(self, screen):
        if self.greenEye:
            screen.blit(EYEFRAMEEYES[5], self.screenOffset)
        if self.redEye:
            screen.blit(EYEFRAMEEYES[0], self.screenOffset)
        if self.orangeEye:
            screen.blit(EYEFRAMEEYES[1], self.screenOffset)
        if self.blueEye:
            screen.blit(EYEFRAMEEYES[2], self.screenOffset)
        if self.purpleEye:
            screen.blit(EYEFRAMEEYES[3], self.screenOffset)
        if self.yellowEye:
            screen.blit(EYEFRAMEEYES[4], self.screenOffset)






class Pipe(movingSetPeice):
    def __init__(self, postion):
        super().__init__(postion, True, PIPE)

        self.enitiyStateMachine = EnitiyStateMachine({"still": PipeStillState(self, PIPE[0]),
                                                      "open": PipeInteractedState(self,
                                                                                   Animation(PIPE[1:], 0.5, False))})

        self.enitiyStateMachine.change("still", [self.enitiyStateMachine])

        self.turned = False



class Chest(movingSetPeice):

    def __init__(self, postion, texts, item):

        super().__init__(postion, False, CHEST)
        self.setPeiceType = "itemDropper"
        self.item = item
        self.enitiyStateMachine = EnitiyStateMachine({"still": ChestStillState(self, CHEST[0]),
                                                      "open": ChestInteractedState(self,
                                                                                   Animation(CHEST[1:], 0.5, False))})
        self.shouldDropItem = False
        self.enitiyStateMachine.change("still", [self.enitiyStateMachine])
        self.secondTextTimer = 0
        self.displaySecondTextAfter = 3

        self.texts = texts

        charsPerLine = 30

        self.splitUpTexts = []
        self.lineHeights = []
        self.lineWidths = []
        self.backings = []
        for i in range(len(self.texts)):
            self.splitUpTexts.append([])

            line = ""
            # we split up text into lines to make them fit better on the screen
            for letterInd in range(len(self.texts[i])):
                if (len(line) > charsPerLine and self.texts[i][letterInd] == " "):
                    self.splitUpTexts[i].append(TEXTFONT.render(line, True, (0, 0, 0)))
                    line = ""
                elif letterInd == len(self.texts[i]) -1:
                    line += self.texts[i][letterInd]
                    self.splitUpTexts[i].append(TEXTFONT.render(line, True, (0, 0, 0)))

                else:
                    line += self.texts[i][letterInd]
            if i == 0:
                self.splitUpTexts[i].append(TEXTFONT.render("x left", True, (0, 0, 0)))
            self.lineHeights.append(0)
            self.lineWidths.append(0)
            for line in self.splitUpTexts[i]:

                self.lineHeights[i] = max(self.lineHeights[i], line.get_height())
                self.lineWidths[i] = max(self.lineWidths[i], line.get_width())

            # we use line height to create some extra space for the background
            self.backings.append(pygame.Surface((self.lineWidths[i] + self.lineHeights[i], (self.lineHeights[i]) * (len(self.splitUpTexts[i]) +1) * 1.1)))

            self.backings[i].set_alpha(128)
            self.backings[i].fill((9, 45, 66))

    def dropItem(self):
        self.shouldDropItem = False


        return self.item((self.getCollisionRectCenter()[0], self.getCollisionRectCenter()[1] - 128))

    def updateText(self, index, numLeft):

        self.splitUpTexts[index][-1] = TEXTFONT.render((str(numLeft) + " " +" left"), True, (0, 0, 0))

    def renderText(self, screen, index):

        screen.blit(self.backings[index], (self.screenOffset[0] - self.backings[index].get_width()/2 + self.stillImage.get_width()/2, self.screenOffset[1] - self.backings[index].get_height() - self.lineHeights[index]))

        lineY = self.screenOffset[1] - self.backings[index].get_height() - self.lineHeights[index] + self.splitUpTexts[index][0].get_height()/2
        for i, line in enumerate(self.splitUpTexts[index]):

            screen.blit(line, (self.screenOffset[0] - line.get_width()/2 + self.stillImage.get_width()/2, lineY))
            lineY += line.get_height() * 1.1






