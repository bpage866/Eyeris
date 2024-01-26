import random

import pygame
from room import Room
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
pygame.init()
#sets a displau and a background
background = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
background.fill(pygame.Color('#1a2125'))
pygame.display.set_caption('Eyeris')
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
background = pygame.Surface((VIRTUALWIDTH, VIRTUALHEIGHT))
background.fill(pygame.Color('#1a2125'))
#creates a state machine with all the states in it
r = Room((0,0))
doors = ["top", "bottom", "left", "right"]
r.baseSewer(169639151.590922,doors)

#sets the state to to the start state and gives the state its own statemachine so it can switch states later along with a blank name
offset = (0,0)

clock = pygame.time.Clock()


outline= [["b","w","w","w","w","w","w","b","b","w","w","b","b"],
          ["e","e","e","e","e","e","e","e","e","e","e","e","e"],
          ["e","e","e","e","e","e","e","e","e","e","e","e","e"],
          ["e","e","e","e","e","e","e","e","e","e","e","e","e"],
          ["e","e","e","e","e","e","e","e","e","e","e","e","e"],
          ["e","e","e","e","e","e","e","e","e","e","e","e","e"],
          ["e","e","e","e","e","e","e","e","e","e","e","e","e"],
          ["b","b","b","b","w","f","f","w","w","w","b","e","e"]]

running = True
while running:
    #blits background to wipe old screen

    #checks in the exit button has been clicked in teh window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    #keys[pygame.K_ESCAPE] is bool value and this method is more effiecnt at picking up button press
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_w]:
        offset = (offset[0], offset[1] +20)
        r.setOffset(offset)

    if keys[pygame.K_s]:
        offset = (offset[0], offset[1] - 20)
        r.setOffset(offset)

    if keys[pygame.K_a]:
        offset = (offset[0] + 20, offset[1])
        r.setOffset(offset)
    if keys[pygame.K_d]:
        offset = (offset[0] - 20, offset[1])
        r.setOffset(offset)
    if keys[pygame.K_UP]:
        if "top" in doors:

            doors.remove("top")
        else:
            doors.append("top")
    if keys[pygame.K_DOWN]:
        if "bottom" in doors:

            doors.remove("bottom")
        else:
            doors.append("bottom")
    if keys[pygame.K_RIGHT]:
        if "right" in doors:

            doors.remove("right")
        else:
            doors.append("right")
    if keys[pygame.K_LEFT]:
        if "left" in doors:

            doors.remove("left")
        else:
            doors.append("left")


    if keys[pygame.K_1]:
        r = Room()
        r.baseSunny(random.randrange(0, 100000000), doors)
        r.setOffset(offset)
    if keys[pygame.K_2]:
        r = Room()
        r.baseLabyrinth(random.randrange(0, 100000000), doors)
        r.setOffset(offset)
    if keys[pygame.K_3]:
        r = Room()
        r.baseSewer(random.randrange(0, 100000000), doors)
        r.setOffset(offset)
    if keys[pygame.K_4]:
        r = Room()
        r.baseCave(random.randrange(0, 100000000), doors)
        r.setOffset(offset)

    #delta time is the time that has elasped betwen each frame
    dt = clock.tick(FRAMERATE)
    r.render(background)
    screen.blit(pygame.transform.scale(background, (SCREENWIDTH,SCREENHEIGHT)), (0, 0))
    #r.renderLetters(screen,offset)
    #screen.blit((MENUFONT.render(str(int(1000 / dt)), True, (0,0,0))), (0,0))
    pygame.display.update()
