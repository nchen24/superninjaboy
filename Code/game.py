import pygame, sys, os, Player
from pygame.locals import *
from Player import *

def quit():
    pygame.quit()
    sys.exit(0)

pygame.init()
screenDimensions = (800, 600)
window = pygame.display.set_mode(screenDimensions, pygame.RESIZABLE)
pygame.display.set_caption('Super Ninja Boy!')
screen = pygame.display.get_surface()
background = pygame.Surface(screen.get_size())

# The player
snb = Player(screen, 350, 300)
pressed = {'Left' : False, 'Right' : False, 'Shift' : False, 'Space' : False}

while True:
    screen.fill((0,0,0))

    snb.update(pressed, screenDimensions)
    snb.draw()

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit()
            if event.key == K_LEFT:
                pressed['Left'] = True
            if event.key == K_RIGHT:
                pressed['Right'] = True
            if event.key == K_LSHIFT:
                pressed['Shift'] = True
            if event.key == K_SPACE:
                pressed['Space'] = True
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                pressed['Left'] = False
            if event.key == K_RIGHT:
                pressed['Right'] = False
            if event.key == K_LSHIFT:
                pressed['Shift'] = False
            if event.key == K_SPACE:
                pressed['Space'] = False

