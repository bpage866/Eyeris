import pyautogui
import pygame
import os
import Util
pygame.init()

#path ensures that no matter what computer this is being ran on the correct path will be fond
#grph is a function that shortcuts writting the path for graphics folder and snd does the same for sounds
path = os.path.dirname(__file__)[:-3]

#using pyautogui liabaries size function the players screen demenisons are found
SCREENWIDTH, SCREENHEIGHT = pyautogui.size()
VIRTUALWIDTH = 1920
VIRTUALHEIGHT =  1080

def fnt(name):
    return path + "\Graphics\\" + name
def snd(name):
    return pygame.mixer.Sound(path + "\Sounds\\" + name)
def grph(name):
    return pygame.image.load(path + "\Graphics\\" + name).convert_alpha()
screen = pygame.display.set_mode((0, 0))

def flipAll(images):
    flipped = []
    for image in images:
        flipped.append(pygame.transform.flip(image, True, False))
    return flipped
#setting
FRAMERATE = 30
TILESIZE = 128
SCALE = 2



#graphics
MISC = {
    "theEye":Util.Sheet.cut(grph("theEyeFrames.png"),1280,640,0,6),
    "eyeris":grph("EyerisTitle.png"),
}
TILES = {
    "eyeztec": Util.Sheet.cut(grph("eyeztecAtlas.png"), TILESIZE, TILESIZE, 0, "False"),
    "sewer": Util.Sheet.cut(grph("sewerAtlas.png"), TILESIZE, TILESIZE, 0, "False"),
    "sunny": Util.Sheet.cut(grph("sunnyAtlas.png"), TILESIZE, TILESIZE, 0, "False"),
    "cave": Util.Sheet.cut(grph("caveAtlas.png"), TILESIZE, TILESIZE, 0, "False")
}
WATER = {
    "eyeztec": Util.Sheet.cut(grph("sewerWaterAtlas.png"), TILESIZE, TILESIZE, 0, "False"),
    "sewer": Util.Sheet.cut(grph("sewerWaterAtlas.png"), TILESIZE, TILESIZE, 0, "False"),
    "sunny": Util.Sheet.cut(grph("sewerWaterAtlas.png"), TILESIZE, TILESIZE, 0, "False"),
    "cave": Util.Sheet.cut(grph("lavaAtlas.png"), TILESIZE, TILESIZE, 0, "False")
}

PLAYER = Util.Sheet.cut(grph("player.png"), 200,200,0,"False")
DASHATTACKEFFECT = Util.Sheet.cut(grph("dashAttackEffect.png"), 256,128,0,"False")
SWINGATTACKEFFECT = Util.Sheet.cut(grph("swingAttackeffect.png"), 128,256,0,"False")
BLOODDANCE =  Util.Sheet.cut(grph("bloodEffect.png"), 384,256,0,"False")

CHEST = Util.Sheet.cut(grph("chest.png"), 192,128,0,"False")
CHEST = CHEST[1:] + [CHEST[0]]
EYEFRAME = [Util.Sheet.cut(grph("eyeFrame.png"), 256,192,0,"False")]
EYEFRAMEEYES = Util.Sheet.cut(grph("eyeFrameEyes.png"), 256,192,0,"False")
EYESTANDS =  Util.Sheet.cut(grph("eyeStands.png"), 192,192,0,"False")

PIPE = Util.Sheet.cut(grph("pipe.png"), 128,256,0,"False")
LAVACRYSTAL = Util.Sheet.cut(grph("lavaCrystal.png"), 256,256,0,"False")
LAVAPIT = Util.Sheet.cut(grph("lavaPit.png"), 256,256,0,"False")
MONOLITH = Util.Sheet.cut(grph("pillar.png"), 256,512,0,"False")
EYEDOOR = Util.Sheet.cut(grph("door.png"), 256,384,0,"False")

MONOLITHSYMBOLS = Util.Sheet.cut(grph("pillarSymbols.png"), 80,112,0,"False")
MONOLITHSYMBOLS = {"sunny": MONOLITHSYMBOLS[0], "eyeztec": MONOLITHSYMBOLS[1], "sewer": MONOLITHSYMBOLS[2], "cave": MONOLITHSYMBOLS[3]}


KNEYEGHT = Util.Sheet.cut(grph("kneyeght.png"), 128,128,0,"False")
KNEYEGHT = flipAll(KNEYEGHT)

SKIME = Util.Sheet.cut(grph("skime.png"), 200,240,0,"False")

POKEY =  Util.Sheet.cut(grph("pokeyFrames.png"), 344,288,0,"False")

GOLILLA = Util.Sheet.cut(grph("gol-illa.png"), 384,384,0,"False")
GOLILLA = flipAll(GOLILLA)
DEERBOSS = Util.Sheet.cut(grph("boss.png"), 512,728,0,"False")
DEERBOSS = flipAll(DEERBOSS)
BUNNY =  Util.Sheet.cut(grph("radit.png"), 128,128
                          ,0,"False")
BUNNY = flipAll(BUNNY)
EYESLIME = Util.Sheet.cut(grph("eyeSlime.png"), 192,192
                          ,0,"False")

BUNNYSLIME = Util.Sheet.cut(grph("bunnySlime.png"), 192,192,0,"False")
BUNNYSLIME = flipAll(BUNNYSLIME)
LAVASLIME = Util.Sheet.cut(grph("lavaSlime.png"), 192,192,0,"False")
SEWERSLIME = Util.Sheet.cut(grph("sewerslime.png"), 192,192,0,"False")

LASEREYE = Util.Sheet.cut(grph("laser.png"), 128,128,0,"False")
BUBBLE = Util.Sheet.cut(grph("bubble.png"), 128,128,0,"False")

#pickups
PICKUPHEART = Util.Sheet.cut(grph("groundHeart.png"), 128,128,0,"False")
KEY = Util.Sheet.cut(grph("key.png"), 96,96,0,"False")
BONECHAR = Util.Sheet.cut(grph("boneChar.png"), 96,96,0,"False")
CONTACTLENSE = Util.Sheet.cut(grph("contactLense.png"), 96,96,0,"False")
BLOODVILE = Util.Sheet.cut(grph("vileOfBlood.png"), 96,96,0,"False")
KAlEIDOSCOPES = Util.Sheet.cut(grph("kaleidoscope.png"), 96,96,0,"False")

XBUTTON = Util.Sheet.cut(grph("xButton.png"), 128, 128, 0, "False")
UI = {"heart": grph("PlayerHeart.png"), "hotBar":Util.Sheet.cut(grph("hotBar.png"), 128,128,0,"False"), "bossHealthBar":Util.Sheet.cut(grph("healthBar.png"), 900,96,0,"False")}

#Fonts
TITLEFONT = pygame.font.Font(fnt("FFFFORWA.TTF"), 198)
MENUFONT = pygame.font.Font(fnt("FFFFORWA.TTF"), 54)
TEXTFONT = pygame.font.Font(fnt("FFFFORWA.TTF"), 24)

#Sounds
BLIP = {"wrong": snd("BlipSelectWrong.wav"), "right": snd("BlipSelectCorrect.wav")}