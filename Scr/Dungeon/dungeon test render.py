import random

import pygame
from dungeon import EyeztecDungeon
#creates paths to Scr and States folder so there files can be imported
import sys
import os
#uses abspath which fins the path to V1 on the users device so will work for anyone
path = os.path.abspath("Scr")
sys.path.append(path)
states = path + "\States"
enemeis = path[:-12] + "\Enemy"
print(enemeis)
sys.path.append(states + "\Game states")
sys.path.append(enemeis)


#import all the varibles from Dependecies
from gameCamera import GameCamera
from Dependencies import*
from player import Player
from gameUI import GameUI
from kneyeght import Kneyeght
from slime import EyeSlime
pygame.init()
#sets a displau and a background
background = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
background.fill(pygame.Color('#1a2125'))
pygame.display.set_caption('Eyeris')
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
background = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
vitualScreen = pygame.Surface((1920,1080))
vitualScreen.fill(pygame.Color('#dd2125'))
background.fill(pygame.Color('#da2125'))
#creates a state machine with all the states in it
randf = random.randrange(0,10000)
print("randf", randf)
d = EyeztecDungeon(9,100, 600, 4,645)



#sets the state to to the start state and gives the state its own statemachine so it can switch states later along with a blank name
offset = d.getDungeonOffset()
player = Player((-offset[0], -offset[1]))


kneyeght = Kneyeght((-offset[0] + 780, -offset[1] - 200), 600,  d.getCurrentRoomLetterMap(), d.getCurrentRoomOffset())
UI = GameUI(player.getHealth())

camera = GameCamera(player.getPlayerPostion(), ((VIRTUALWIDTH)/ 2, (VIRTUALHEIGHT)/2))



d.setOffset(camera.getOffsetForCamera())
player.setScreenOffset(camera.getOffsetForCamera())
kneyeght.setScreenOffset(camera.getOffsetForCamera())
clock = pygame.time.Clock()

running = True
frameRates = []
while running:
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=")


    #blits background to wipe old screen
    vitualScreen.fill(pygame.Color("#1a2125"))
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
    playerCollision = d.getCurrentRoomSurroundingTiles(player.getCollisionRectCenter())

    player.update(dt, keys, {"collisions":playerCollision, "attacks":d.getAllHitBoxes()})

    camera.update(dt, player.getMoveDirections(), player.getPlayerPostion(), d.getCurrentRoom())

    d.update(dt, player.getCollisionRectCenter(), {"targetPos":player.getCollisionRectCenter(), "screen":vitualScreen,  "attacks":player.getAttacking()})
    d.setOffset(camera.getOffsetForCamera())
    player.setScreenOffset(camera.getOffsetForCamera())
    d.render(vitualScreen)
    kneyeght.setScreenOffset(camera.getOffsetForCamera())
    kneyeght.render(vitualScreen)


    player.render(vitualScreen)


    UI.update(player.health)
    UI.render(vitualScreen)

    #kneyeght.update(dt, keys, {"targetPos":player.getCollisionRectCenter(), "screen":vitualScreen, "collisions": kneyeCols, "attacks":player.getAttacking()})
    if SCREENWIDTH == VIRTUALWIDTH and SCREENHEIGHT == VIRTUALHEIGHT:
        screen.blit(vitualScreen, (0,0))
    else:
        screen.blit(pygame.transform.scale(vitualScreen, (SCREENWIDTH,SCREENHEIGHT)), (0, 0))
    screen.blit((MENUFONT.render(str(offset), True, (0, 0, 0))), (90, 0))
    screen.blit((MENUFONT.render(str(int(1000 / dt)), True, (0,0,0))), (0,0))


    #pygame.draw.line(screen, (255,0,255), (player.getCollisionRectCenter()[0] + camera.getOffsetForCamera()[0], player.getCollisionRectCenter()[1] + camera.getOffsetForCamera()[1]), (kneyeght.getCollisionRectCenter()[0] + camera.getOffsetForCamera()[0], kneyeght.getCollisionRectCenter()[1] + camera.getOffsetForCamera()[1]), 4)
    frameRates.append(int(1000 / dt))
    temvar = 0

    for i in frameRates:
        temvar += i
    print("frames", temvar / len(frameRates))

    print("dt", dt)
    pygame.display.update()
