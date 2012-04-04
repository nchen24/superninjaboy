import pygame, sys, os
from pygame.locals import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.screen = screen
        self.image = pygame.image.load("../Assets/Walls/onewall.gif")
        self.image_w, self.image_h = self.image.get_size()

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

        self.floor_active = False
        self.wall_active = False

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
