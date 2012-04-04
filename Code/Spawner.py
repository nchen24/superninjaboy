import pygame, sys, os, Spritesheet, Shuriken
from pygame.locals import *
from Spritesheet import *
from Shuriken import *

# Constants
RATE = 50 

class Spawner(pygame.sprite.Sprite):
    '''Spawner is an invisible object that spawns 1 shuriken/RATE frames'''
    def __init__(self, screen, x, y, type):
        self.x = x
        self.y = y
        self.timer = 0
        self.shurikens = []
        self.type = type
        self.screen = screen

    def update(self):
        if self.timer < RATE:
            self.timer += 1
        else:
            self.timer = 0
            self.shurikens.append(Shuriken(self.screen, self.x, self.y, self.type))

        for s in self.shurikens:
            s.update()
            if s.x < 0 or s.x > 1024 or s.y < 0 or s.y > 768 or not s.active:
                del s
            else:
                s.draw()

