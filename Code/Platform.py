import pygame, os, sys
from pygame.locals import *

###############################
# Constants for image loading #
###############################

PLAT1 = "../assets/platform1-2.gif"

class Platform(pygame.sprite.Sprite):
    def load_image(self, image_name):
        try:
            image = pygame.image.load(image_name)
        except:
            print "Cannot load image: " + image_name
            raise SystemExit, message
        return image.convert_alpha()

    def __init__(self, screen, image_name, x, y):
        self.image = self.load_image(image_name)
        self.screen = screen
        self.x   = x
        self.y   = y
        self.image_w, self.image_h = self.image.get_size()

        self.rect = self.image.get_rect()
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

        self.boundwidth = 10

        self.top = pygame.Rect((self.x, self.y), (self.image_w, self.boundwidth))
        self.left = pygame.Rect((self.x,self.y), (self.boundwidth,self.image_h))
        self.right = pygame.Rect(((self.x + self.image_w - self.boundwidth),self.y), (self.boundwidth,self.image_h))

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.top = pygame.Rect((self.x, self.y), (self.image_w, self.boundwidth))
        self.left = pygame.Rect((self.x,self.y), (self.boundwidth,self.image_h))
        self.right = pygame.Rect(((self.x + self.image_w - self.boundwidth),self.y), (self.boundwidth,self.image_h))