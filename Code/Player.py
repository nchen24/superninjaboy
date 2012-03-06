import pygame, os, sys
from pygame.locals import *

#################
# Player Sprite #
#################

class Player(pygame.sprite.Sprite):
    def load_image(self, image_name):
        try:
            image = pygame.image.load(image_name)
        except:
            print "Cannot load image: " + image_name
            raise SystemExit, message
        return image.convert_alpha()

    def __init__(self, screen, x, y):
        self.image = self.load_image("battlecruiser.gif")
        self.screen = screen
        self.x   = x
        self.y   = y
        self.dx  = 0
        self.dy  = 0
        self.ddx = .1
        self.ddy = 0
        self.dx_max = 1.5
        self.dy_max = 1.5
        self.image_w, self.image_h = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

        self.alive = True
        self.jumped = False
        self.apex = False
        self.jumptimer = 0

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def update(self, pressed, screenDimensions):

        if pressed['Space'] == True:
            self.jumptimer = self.jumptimer + 1
            if self.jumptimer == 10:
                self.apex = True
            if not self.apex:
                print "!!"
                self.dy = -1.5
            else:
                self.dy = 0
                self.jumptimer = 0
                #self.jumped = False
        if self.jumptimer > 20:
            self.jumptimer = 0
            self.jumped = False
            self.dy = 0
        if self.rect.bottomright[1] < screenDimensions[1] :
            self.dy = 1
        else:
            self.dy = 0
        
        if pressed['Left'] == True:
            if abs(self.dx) < self.dx_max:
                self.dx = self.dx - self.ddx
        elif pressed['Right'] == True:
            if abs(self.dx) < self.dx_max:
                self.dx = self.dx + self.ddx
        else:
            self.dx = 0

        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect = self.image.get_rect()
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)




