import pygame, sys, os, Spritesheet
from pygame.locals import *
from Spritesheet import *

SPIKE_U = ((0,18,16,16), (18,18,16,16))
SPIKE_R = ((0,36,16,16), (18,36,16,16))
SPIKE_D = ((0,54,16,16), (18,54,16,16))
SPIKE_L = ((0,72,16,16), (18,72,16,16))
class Spike(pygame.sprite.Sprite):
    def __init__(self,screen,x,y,type):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.screen = screen
        self.ss = spritesheet("../assets/misc_sprite.png")
        if type == "U":
            self.IMGS = self.ss.images_at(SPIKE_U, colorkey = -1)
            self.image = self.IMGS[1] 
        if type == "R":
            self.IMGS = self.ss.images_at(SPIKE_R, colorkey = -1)
            self.image = self.IMGS[1] 
        if type == "D":
            self.IMGS = self.ss.images_at(SPIKE_D, colorkey = -1)
            self.image = self.IMGS[1] 
        if type == "L":
            self.IMGS = self.ss.images_at(SPIKE_L, colorkey = -1)
            self.image = self.IMGS[1] 
        self.image_w, self.image_h = self.image.get_size()

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
