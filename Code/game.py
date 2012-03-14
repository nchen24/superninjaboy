import pygame, sys, os, Player
from pygame.locals import *
from Player import *

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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
snb = Player(screen, 350, 300)
pressed = {'Left' : False, 'Right' : False, 'Shift' : False, 'Space' : False}

while True:
    screen.fill(WHITE)

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
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                pressed['Left'] = False
            elif event.key == K_RIGHT:
                pressed['Right'] = False
            elif event.key == K_LSHIFT:
                pressed['Shift'] = False
            elif event.key == K_SPACE:
                pressed['Space'] = False

