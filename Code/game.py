#what up?
import pygame, sys, os, Player
from pygame.locals import *
from Player import *
from Platform import *

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAT1 = "../assets/platform1-2.gif"
PLAT2 = "../assets/platform1-3.gif"

def quit():
    pygame.quit()
    sys.exit(0)

pygame.init()
screenDimensions = (1200, 700)
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

while True:
    screen.fill(WHITE)

    if plat1.top.colliderect(snb.bottom) or plat2.top.colliderect(snb.bottom) or plat3.top.colliderect(snb.bottom):
        snb.dy = 0
        snb.jumped = False
        snb.jumptimer = 0
        snb.apex = False 
        snb.onplat = True
    else: snb.onplat = False

    if plat1.left.colliderect(snb.right) or plat1.right.colliderect(snb.left):
        snb.dx = 0
        snb.jumped = False
        snb.jumptimer = 0
        snb.apex = False 
        snb.onwall = True
        print ("on tha wall")
    else: snb.onwall = False

    if plat2.left.colliderect(snb.right) or plat2.right.colliderect(snb.left):
        snb.dx = 0
        snb.jumped = False
        snb.jumptimer = 0
        snb.apex = False 
        snb.onwall = True
        print ("on tha wall")
    else: snb.onwall = False

    if plat3.left.colliderect(snb.right) or plat3.right.colliderect(snb.left):
        snb.dx = 0
        snb.jumped = False
        snb.jumptimer = 0
        snb.apex = False 
        snb.onwall = True
        #print ("on tha wall")
    else: snb.onwall = False

    plat1.update()
    plat1.draw()

    plat2.update()
    plat2.draw()

    plat3.update()
    plat3.draw()

    snb.update(pressed, screenDimensions)
    snb.draw()

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
                snb.canJump = True

