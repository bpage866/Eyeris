import pygame
import cv2

#creates paths to Scr and States folder so there files can be imported
import sys
import os
#uses abspath which fins the path to V1 on the users device so will work for anyone
path = os.path.abspath("Scr")
sys.path.append(path)
states = path + "\States"
sys.path.append(states + "\Game states")
#import all the varibles from Dependecies
from Dependencies import*
from stateMachine import StateMachine
from menuState import MenuState
from loadState import LoadState
from mainGameState import MainGameState
from endScreenState import EndScreenState
pygame.init()
#sets a displau and a background
pygame.display.set_caption('Eyeris')
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
virtualScreen = pygame.Surface((1920, 1080))
#creates a state machine with all the states in it
gStateMachine = StateMachine({"start": MenuState(), "load": LoadState(), "end":EndScreenState()})
#sets the state to to the start state and gives the state its own statemachine so it can switch states later along with a blank name
gStateMachine.change("start", ["", gStateMachine])

clock = pygame.time.Clock()
fps = []
cnt = 0





running = True
while running:
    print("________________________________________________________")
    virtualScreen.fill(pygame.Color('#1a2125'))
    #blits background to wipe old screen
    #checks in the exit button has been clicked in teh window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    #keys[pygame.K_ESCAPE] is bool value and this method is more effiecnt at picking up button press
    if keys[pygame.K_ESCAPE]:
        running = False
    #delta time is the time that has elasped betwen each frame
    dt = clock.tick(FRAMERATE)
    event = pygame.event.get()
    #gives the state machine the delta time, all keys that have been pressed and all events
    gStateMachine.update(dt,keys, virtualScreen)
    #renders what ever the state the state machien is rendering and pass it the screen to blit to
    gStateMachine.render(virtualScreen)
    #shows frame rate

    if SCREENWIDTH == VIRTUALWIDTH and SCREENHEIGHT == VIRTUALHEIGHT:
        screen.blit(virtualScreen, (0, 0))
    else:
        screen.blit(pygame.transform.scale(virtualScreen, (SCREENWIDTH, SCREENHEIGHT)), (0, 0))
    fps.append(int(1000 / dt))
    cnt += 1
    #screen.blit((MENUFONT.render(str(fps[-1]), True, (0, 0, 0))), (0, 0))
    pygame.display.update()

    sm = 0
    for frame in fps:
        sm += frame
