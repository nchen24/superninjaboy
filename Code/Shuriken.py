import pygame, sys, os, Spritesheet
from pygame.locals import *
from Spritesheet import *

SHURI = ((0,0,16,16), (18,0,16,16))
class Shuriken(pygame.sprite.Sprite):
    def __init__(self, screen, x,y):
        self.x = x
        self.y = y
        self.screen = screen
        self.ss = spritesheet("../assets/misc_sprite.png")
        self.IMGS = self.ss.images_at(SHURI, colorkey = -1)
        self.image = self.IMGS[1] 
        self.image_w, self.image_h = self.image.get_size()

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
