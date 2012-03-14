import pygame, os, sys
from pygame.locals import *

###############################
# Constants for image loading #
###############################
IDLE = "../assets/idle.gif"
FALL = "../assets/fall.gif"
JUMP = "../assets/jump.gif"

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
        self.image = self.load_image(IDLE)
        self.screen = screen
        self.x   = x
        self.y   = y
        self.dx  = 0
        self.dy  = 0
        self.ddx = .1
        self.ddy = 0
        self.dx_max = .8
        self.dy_max = .8
        self.image_w, self.image_h = self.image.get_size()

        self.rect = self.image.get_rect()
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

        self.boundwidth = 5
        self.left = pygame.Rect((self.x, self.y), (self.boundwidth, self.image_h))
        #self.left.rect.move(self.x, self.y)
        #self.left.rect.topleft = (self.x, self.y)
        #self.left.rect.bottomright = (self.x + self.boundwidth, self.y + self.image_h)

        # pygame.Rect takes in ((start_x, start_y), (width, height)
        self.right = pygame.Rect((self.x + self.image_w - self.boundwidth, self.y), (self.boundwidth, self.image_h))
        #self.right.rect.move(self.x + self.image_w, self.y)
        #self.right.rect.topleft = (self.x + self.image_w - self.boundwidth, self.y) 
        #self.right.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

        self.alive = True
        self.jumped = False
        self.apex = False
        self.jumptimer = 0
        self.direction = "Right"

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def update(self, pressed, screenDimensions):
        if pressed['Space'] == True and not(self.jumped) and not(self.apex):
            if self.jumptimer > 100:
                self.apex = True
            else:
                self.jumptimer += 1

            if self.direction == "Right":
                self.image = self.load_image(JUMP)
                self.dy = -.8
            elif self.direction == "Left":
                self.image = pygame.transform.flip(self.load_image(JUMP), True, False)
                self.dy = -.8

        elif self.rect.bottomright[1] < screenDimensions[1]:
            if self.direction == "Right":
                self.image = self.load_image(FALL)
                self.dy = .8 
            elif self.direction == "Left":
                self.image = pygame.transform.flip(self.load_image(FALL), True, False)
                self.dy = .8
        else:
            if self.direction == "Right":
                self.image = self.load_image(IDLE)
            elif self.direction == "Left":
                self.image = pygame.transform.flip(self.load_image(IDLE), True, False)
            self.dy = 0
            self.jumped = False
            self.apex = False
            self.jumptimer = 0
        
        if pressed['Left'] == True:
            self.direction = "Left"
            if pressed ['Right'] == True:
                self.dx = 0 
            if abs(self.dx) < self.dx_max:
                self.dx = self.dx - self.ddx
        elif pressed['Right'] == True:
            self.direction = "Right"
            if pressed ['Left'] == True:
                self.dx = 0 
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

        self.left.top = self.left.top + self.dy
        self.left.left = self.left.left + self.dx

        self.right.top = self.right.top + self.dy
        self.right.left = self.right.left + self.dx
    #def jump(self):

