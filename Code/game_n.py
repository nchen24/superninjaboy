import pygame, sys, os, Player
from pygame.locals import *
from Player import *
from Platform import *

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAT1 = "../assets/platform1-2.gif"
PLAT2 = "../assets/platform1-3.gif"

class Wall(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.screen = screen
        self.image = pygame.image.load("../Assets/Walls/onewall.png")
        self.image_w, self.image_h = self.image.get_size()

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)
    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

walls = []

def quit():
    pygame.quit()
    sys.exit(0)
def genwall(screen):
    mapFile = open("../Levels/Level4.txt", 'r') 
    vc = 0
    hc = 0
    for line in mapFile:
        vc += 1
        hc =  0
        for character in line:
            hc +=1
            if character == "#":
                walls.append(Wall(screen, hc*16, vc*16))

pygame.init()
screenDimensions = (1024, 640)
window = pygame.display.set_mode(screenDimensions, pygame.RESIZABLE)
pygame.display.set_caption('Super Ninja Boy!')
screen = pygame.display.get_surface()
background = pygame.Surface(screen.get_size())

# The player
snb = Player(screen, 350, 500)
pressed = {'Left' : False, 'Right' : False, 'Shift' : False, 'Space' : False}
plat1 = Platform(screen, PLAT1, 400, 650)
plat2 = Platform(screen, PLAT2, 600, 600)
plat3 = Platform(screen, PLAT2, 100, 600)

genwall(screen)
while True:
    screen.fill(WHITE)

    if plat1.top.colliderect(snb.bottom) or plat2.top.colliderect(snb.bottom) or plat3.top.colliderect(snb.bottom):
        snb.dy = 0
        snb.jumped = False
        snb.jumptimer = 0
        snb.apex = False 
        snb.onplat = True
    else: snb.onplat = False

    plat1.update()
    plat1.draw()

    plat2.update()
    plat2.draw()

    plat3.update()
    plat3.draw()

    snb.update(pressed, screenDimensions)
    snb.draw()

    for w in walls:
        w.draw()
        if w.rect.colliderect(snb.bottom):
            snb.dy = 0
            snb.jumped = False
            snb.jumptimer = 0
            snb.apex = False 
            snb.onplat = True
        else: snb.onplat = False

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit()
            if event.key == K_LEFT:
                pressed['Left'] = True
            elif event.key == K_RIGHT:
                pressed['Right'] = True
            elif event.key == K_LSHIFT:
                pressed['Shift'] = True
            elif event.key == K_SPACE:
                pressed['Space'] = True
                snb.jumped = True
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                pressed['Left'] = False
            elif event.key == K_RIGHT:
                pressed['Right'] = False
            elif event.key == K_LSHIFT:
                pressed['Shift'] = False
            elif event.key == K_SPACE:
                pressed['Space'] = False

