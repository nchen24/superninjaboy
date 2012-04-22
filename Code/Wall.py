import pygame, sys, os, Spritesheet
from pygame.locals import *
from Spritesheet import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.screen = screen
        self.ss = spritesheet("../Assets/Walls/all_wall_sm.png")
        self.image_w, self.image_h = self.image.get_size()

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

        self.floor_active = False
        self.wall_active = False

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
    
    def setimage(self, bin_wall):
        val = 0
        imageloc = [0, 0]
        xpos = self.x/16
        ypos = self.y/16

        if bin_wall[xpos + 1][ypos - 1] == 1:
            val += 1
        if bin_wall[xpos + 1][ypos + 1] == 1:
            val += 2
        if bin_wall[xpos - 1][ypos - 1] == 1:
            val += 4
        if bin_wall[xpos - 1][ypos - 1] == 1:
            val += 8

        if bin_wall[xpos][ypos - 1] == 1:
            val += 16
        if bin_wall[xpos + 1][ypos] == 1:
            val += 32
        if bin_wall[xpos][ypos + 1] == 1:
            val += 64
        if bin_wall [xpos - 1][ypos] == 1:
            val += 128 


        if val > 240:
            imageloc = [0, 1]
        elif val < 16:
            imageloc = [0, 0]
        elif val < 32:
            imageloc = [1, 0]
        elif val < 48:
            imageloc = [1, 1]
        elif val < 64:
            if val % 2 == 0:
                imageloc = [4, 0]
            else:
                imageloc = [6, 0]
        elif val < 80:
            imageloc = [2, 0]
        elif val < 96:
            imageloc = [7, 0]
        elif val < 112:
            if val % 4 < 2:
                imageloc = [3, 0]
            else:
                imageloc = [5, 0]
        elif val < 128:
            imageloc = [9, 0]
        elif val < 144:
            imageloc = [2, 1]
        elif val < 160:
            if val % 16 < 8:
                imageloc = [4, 1]
            else:
                imageloc = [6, 1]
        elif val < 176:
            imageloc = [7, 1]
        elif val < 192:
            imageloc = [8, 1]
        elif val < 208:
            if val % 8 < 4:
                imageloc = [5, 1]
            else:
                imageloc = [3, 1]
        elif val < 224:
            imageloc = [9, 1]
        elif val < 240:
            imageloc = [8, 0]

        self.image = self.ss.image_at((18*imageloc[1], 18*imageloc[0], 16, 16), colorkey = (255, 255, 255))
