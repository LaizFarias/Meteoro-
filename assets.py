import pygame
import os
from config import *

BACKGROUND = "background"
METEOR_IMG = "meteor_img"
METEOR_IMG = "meteor_img"
METEOR_ROXO_IMG = "meteor_roxo_img"
METEOR_ROXO_IMG = "meteor_roxo_img"
SHIP_IMG = "ship_img"
SHIP_IMG = "ship_img"
BULLET_IMG = "bullet_img"
EXPLOSION_ANIM = "explosion_anim"
SCORE_FONT = "score_font"
BOOM_SOUND = "boom_sound"
DESTROY_SOUND = "destroy_sound"
PEW_SOUND = "pew_sound"
STARTSC_ANIM = "startsc_anim"
LIFE_IMG = "life_img"

def load_assets():
    assets = {}
    assets[BACKGROUND] = pygame.image.load(os.path.join(IMG_DIR, "starfield.png")).convert()
    assets[METEOR_IMG] = pygame.image.load(os.path.join(IMG_DIR, "meteorBrown_med1.png")).convert_alpha()
    assets[METEOR_IMG] = pygame.transform.scale(assets["meteor_img"], (METEOR_WIDTH, METEOR_HEIGHT))
    assets[METEOR_ROXO_IMG] = pygame.image.load(os.path.join(IMG_DIR, "asteroid_roxo.png")).convert_alpha()
    assets[METEOR_ROXO_IMG] = pygame.transform.scale(assets["meteor_roxo_img"], (METEOR_ROXO_WIDTH, METEOR_ROXO_HEIGHT))
    assets[SHIP_IMG] = pygame.image.load(os.path.join(IMG_DIR,"playerShip1_orange.png")).convert_alpha()
    assets[SHIP_IMG] = pygame.transform.scale(assets["ship_img"], (SHIP_WIDTH, SHIP_HEIGHT))
    assets[BULLET_IMG] = pygame.image.load(os.path.join(IMG_DIR,"laserRed16.png")).convert_alpha()
    assets[LIFE_IMG] = pygame.image.load(os.path.join(IMG_DIR,"life.png")).convert_alpha()
    assets[LIFE_IMG] = pygame.transform.scale(assets["life_img"], (LIFE_WIDTH, LIFE_HEIGHGT))

    # animação da explosão
    explosion_anim = []
    for i in range(9):
        # Os arquivos de animação são numerados de 00 a 08
        filename = os.path.join(IMG_DIR, "regularExplosion0{}.png".format(i))
        img = pygame.image.load(filename).convert()
        img = pygame.transform.scale(img, (32, 32))
        explosion_anim.append(img)
    assets[EXPLOSION_ANIM] = explosion_anim
    assets[SCORE_FONT] = pygame.font.Font("assets/font/PressStart2P.ttf", 28)

    # animação da tela inicial
    startsc_anim = []
    for i in range(2):
        # os arquivos da animação são numerados de 00 a 01
        filename = os.path.join(IMG_DIR, "tela_instrucoes0{}.png".format(i))
        img = pygame.image.load(filename).convert()
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        startsc_anim.append(img)
    assets[STARTSC_ANIM] = startsc_anim 

    # carrega os sons do jogo
    pygame.mixer.music.load(os.path.join(SND_DIR, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
    pygame.mixer.music.set_volume(0.4)
    assets[BOOM_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, "expl3.wav"))
    assets[DESTROY_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, "expl6.wav"))
    assets[PEW_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, "pew.wav"))
    return assets