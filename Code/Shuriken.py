import pygame, sys, os, Spritesheet
from pygame.locals import *
from Spritesheet import *

SHURI = ((0,0,16,16), (18,0,16,16))
class Shuriken(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, type):
        self.x = x
        self.y = y
        self.active = True
        self.timer = 0
        if type == "L" or type == "R":
            self.dx = 8
            self.dy = 0
            if type == "L": self.dx *= -1
        elif type == "U" or type == "D":
            self.dx = 0
            self.dy = 8
            if type == "U": self.dy += -1
        else:
            self.dx = 0
            self.dy = 0
        
        self.screen = screen
        self.ss = spritesheet("../assets/misc_sprite.png")
        self.IMGS = self.ss.images_at(SHURI, colorkey = -1)
        self.image = self.IMGS[0] 
        self.image_w, self.image_h = self.image.get_size()

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
    
    def update(self):
        if self.timer < 10:
            self.image = self.IMGS[0] 
        elif self.timer < 20:
            self.image = self.IMGS[1]
        else:
            self.timer = 0
        self.timer += 1
        self.image_w, self.image_h = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)
            
        self.x += self.dx
        self.y += self.dy

